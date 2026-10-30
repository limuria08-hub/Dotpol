"""P1.11: required OpenClaw gateway readiness without duplicate AI or secrets."""
import json
import subprocess
from types import SimpleNamespace

from fastapi.testclient import TestClient

from app import create_app
from dotpol_platform import openclaw_gateway as gateway


def test_missing_openclaw_is_not_called_or_marked_ready(monkeypatch):
    monkeypatch.setattr(gateway.shutil, "which", lambda name: None)
    monkeypatch.setattr(gateway.subprocess, "run", lambda *a, **kw: (_ for _ in ()).throw(AssertionError("must not invoke CLI")))
    result = gateway.probe_openclaw()
    assert result["component"] == "openclaw"
    assert result["required_for_release"] is True
    assert result["ready"] is False
    assert result["status"] == "not-installed"


def test_valid_health_uses_documented_cli_and_redacts_sensitive_data(monkeypatch):
    monkeypatch.setattr(gateway.shutil, "which", lambda name: "/usr/local/bin/openclaw")
    def run(args, **opts):
        assert args == ["/usr/local/bin/openclaw", "health", "--json", "--timeout", "2500"]
        assert opts["check"] is False and opts["capture_output"] is True
        assert opts["timeout"] <= 7
        return SimpleNamespace(returncode=0, stdout=json.dumps({"ok": True, "channels": {"token": "DO-NOT-EXPOSE"}}), stderr="secret")
    monkeypatch.setattr(gateway.subprocess, "run", run)
    result = gateway.probe_openclaw()
    assert result["status"] == "gateway-healthy" and result["ready"]
    assert "DO-NOT-EXPOSE" not in repr(result)
    assert "secret" not in repr(result)
    assert "channels" not in result


def test_gateway_starting_not_ready(monkeypatch):
    monkeypatch.setattr(gateway.shutil, "which", lambda name: "/bin/openclaw")
    monkeypatch.setattr(gateway.subprocess, "run", lambda *a, **kw: SimpleNamespace(returncode=0, stdout='{"status":"starting","startupPhase":"loading"}', stderr=""))
    assert gateway.probe_openclaw()["status"] == "starting"
    assert not gateway.probe_openclaw()["ready"]


def test_cli_errors_are_never_echoed(monkeypatch):
    monkeypatch.setattr(gateway.shutil, "which", lambda name: "/bin/openclaw")
    monkeypatch.setattr(gateway.subprocess, "run", lambda *a, **kw: SimpleNamespace(returncode=1, stdout="TOKEN", stderr="HOME=/secret"))
    result = gateway.probe_openclaw()
    assert result["status"] == "unreachable" and not result["ready"]
    assert "TOKEN" not in repr(result) and "/secret" not in repr(result)


def test_timeout_and_bad_payloads(monkeypatch):
    monkeypatch.setattr(gateway.shutil, "which", lambda name: "/bin/openclaw")
    monkeypatch.setattr(gateway.subprocess, "run", lambda *a, **kw: (_ for _ in ()).throw(subprocess.TimeoutExpired("openclaw", 7)))
    assert gateway.probe_openclaw()["status"] == "unreachable"
    monkeypatch.setattr(gateway.subprocess, "run", lambda *a, **kw: SimpleNamespace(returncode=0, stdout="not-json", stderr=""))
    assert gateway.probe_openclaw()["status"] == "invalid-response"
    monkeypatch.setattr(gateway.subprocess, "run", lambda *a, **kw: SimpleNamespace(returncode=0, stdout='{"ok":false}', stderr=""))
    assert gateway.probe_openclaw()["status"] == "unhealthy"


def test_local_api_exposes_only_sanitized_readiness(tmp_path, monkeypatch):
    monkeypatch.setattr(gateway.shutil, "which", lambda name: "/bin/openclaw")
    monkeypatch.setattr(gateway.subprocess, "run", lambda *a, **kw: SimpleNamespace(returncode=0, stdout='{"ok":true,"tokens":["HIDDEN"]}', stderr=""))
    client = TestClient(create_app(tmp_path / "data.sqlite3"))
    response = client.get("/api/openclaw/status")
    assert response.status_code == 200 and response.json()["ready"] is True
    assert response.json()["required_for_release"] is True
    assert "HIDDEN" not in response.text
    assert client.get("/api/openclaw/status", headers={"Origin": "https://untrusted.invalid"}).status_code == 403
