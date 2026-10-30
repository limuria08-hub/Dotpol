"""P1.11 OpenClaw assurance: read-only baseline audit with no sensitive payloads."""
import json
import subprocess
from types import SimpleNamespace

from fastapi.testclient import TestClient

from app import create_app
from dotpol_platform import openclaw_gateway as gateway

HEADERS = {"X-Dotpol-Local": "1"}


def mock_cli(monkeypatch, report, *, exit_code=0):
    monkeypatch.setattr(gateway.shutil, "which", lambda name: "/usr/bin/openclaw")
    def run(args, **options):
        assert args == ["/usr/bin/openclaw", "security", "audit", "--json"]
        assert options["capture_output"] is True
        assert options["check"] is False
        assert options["timeout"] <= 15
        return SimpleNamespace(returncode=exit_code, stdout=report, stderr="SECRET-STDERR")
    monkeypatch.setattr(gateway.subprocess, "run", run)


def test_missing_install_has_no_side_effects(monkeypatch):
    monkeypatch.setattr(gateway.shutil, "which", lambda name: None)
    monkeypatch.setattr(gateway.subprocess, "run", lambda *a, **k: (_ for _ in ()).throw(AssertionError("unexpected CLI call")))
    r = gateway.audit_openclaw_security()
    assert r["required_for_release"] and r["review_required"]
    assert not r["audit_performed"] and r["status"] == "not-installed"


def test_clear_basic_report_not_a_full_clearance(monkeypatch):
    report = {"summary": {"critical": 0, "warn": 0, "info": 1},
              "findings": [{"detail": "SECRET-DETAIL", "severity": "info"}],
              "suppressedFindings": [], "secretDiagnostics": ["SECRET-KEY"]}
    mock_cli(monkeypatch, json.dumps(report))
    result = gateway.audit_openclaw_security()
    assert result["audit_performed"] and not result["review_required"]
    assert result["status"] == "baseline-no-findings"
    assert result["info_count"] == 1
    assert "SECRET" not in str(result)
    assert "deep checks" in result["detail"]


def test_critical_warning_or_suppression_requires_review(monkeypatch):
    for summary, suppressed in [
        ({"critical": 2, "warn": 0, "info": 0}, []),
        ({"critical": 0, "warn": 3, "info": 2}, []),
        ({"critical": 0, "warn": 0, "info": 0}, [{"reason": "SECRET-WAIVER"}]),
    ]:
        mock_cli(monkeypatch, json.dumps({"summary": summary, "findings": [], "suppressedFindings": suppressed}))
        r = gateway.audit_openclaw_security()
        assert r["audit_performed"] and r["review_required"]
        assert r["status"] == "findings-require-review"
        assert "SECRET" not in repr(r)


def test_invalid_reports_fail_closed(monkeypatch):
    cases = [
        "not json", "[]", '{"summary":{},"findings":[]}',
        '{"summary":{"critical":true,"warn":0,"info":0},"findings":[]}',
        '{"summary":{"critical":-1,"warn":0,"info":0},"findings":[]}',
        '{"summary":{"critical":0,"warn":0,"info":0},"findings":{}}',
        '{"summary":{"critical":0,"warn":0,"info":0},"findings":[],"suppressedFindings":{}}',
    ]
    for sample in cases:
        mock_cli(monkeypatch, sample)
        r = gateway.audit_openclaw_security()
        assert not r["audit_performed"] and r["review_required"]
        assert r["status"] == "invalid-response"


def test_cli_error_timeout_and_output_limit(monkeypatch):
    mock_cli(monkeypatch, "SECRET-STDOUT", exit_code=1)
    assert gateway.audit_openclaw_security()["status"] == "audit-unavailable"
    mock_cli(monkeypatch, "x" * 2_000_001)
    assert gateway.audit_openclaw_security()["status"] == "audit-unavailable"
    monkeypatch.setattr(gateway.subprocess, "run", lambda *a, **kw: (_ for _ in ()).throw(subprocess.TimeoutExpired("openclaw", 15)))
    assert gateway.audit_openclaw_security()["status"] == "audit-unavailable"


def test_api_requires_local_explicit_post_and_sanitizes_response(tmp_path, monkeypatch):
    mock_cli(monkeypatch, json.dumps({
        "summary": {"critical": 0, "warn": 1, "info": 0},
        "findings": [{"detail": "HIDDEN-CHANNEL-TOKEN"}],
    }))
    c = TestClient(create_app(tmp_path / "test.sqlite3"))
    url = "/api/openclaw/audit"
    assert c.get(url).status_code == 405
    assert c.post(url).status_code == 403
    assert c.post(url, headers={**HEADERS, "Origin": "https://evil.example"}).status_code == 403
    resp = c.post(url, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json()["warning_count"] == 1 and resp.json()["review_required"]
    assert "HIDDEN-CHANNEL-TOKEN" not in resp.text
