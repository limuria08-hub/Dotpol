"""P1.11: real authenticated OpenClaw RPC interface via maintained local CLI.

The tests mock the CLI. A live installed OpenClaw Gateway is a separate
acceptance requirement; passing mocks never certifies that environment.
"""
import json
import subprocess
from types import SimpleNamespace

from fastapi.testclient import TestClient

from app import create_app
from dotpol_platform import openclaw_gateway as gateway

HEADERS = {"X-Dotpol-Local": "1"}


def response(*, sessions=None):
    return json.dumps({
        "heartbeat": {"enabled": True},
        "queuedSystemEvents": 0,
        "sessions": {} if sessions is None else sessions,
        "gateway": {"token": "HIDDEN-GATEWAY-TOKEN"},
        "channels": {"private": "HIDDEN-CHANNEL-NAME"},
    })


def cli(monkeypatch, stdout=None, exit_code=0):
    monkeypatch.setattr(gateway.shutil, "which", lambda name: "/usr/bin/openclaw")
    def run(args, **kwargs):
        assert args == [
            "/usr/bin/openclaw", "gateway", "call", "status",
            "--params", '{"includeChannelSummary":false}',
            "--json", "--timeout", "4000",
        ]
        assert kwargs["check"] is False
        assert kwargs["capture_output"] is True
        assert kwargs["timeout"] <= 15
        assert "shell" not in kwargs
        return SimpleNamespace(
            returncode=exit_code, stdout=response() if stdout is None else stdout,
            stderr="HIDDEN-STDERR-SECRET",
        )
    monkeypatch.setattr(gateway.subprocess, "run", run)


def test_missing_cli_fails_without_action(monkeypatch):
    monkeypatch.setattr(gateway.shutil, "which", lambda name: None)
    monkeypatch.setattr(gateway.subprocess, "run", lambda *a, **kw: (_ for _ in ()).throw(AssertionError("unexpected subprocess")))
    r = gateway.verify_openclaw_rpc()
    assert not r["rpc_verified"] and r["status"] == "not-installed"
    assert r["required_for_release"]


def test_authenticated_gateway_status_succeeds_without_exposing_details(monkeypatch):
    cli(monkeypatch)
    r = gateway.verify_openclaw_rpc()
    assert r["rpc_verified"] and r["status"] == "rpc-connected"
    assert r["required_for_release"]
    assert "HIDDEN" not in repr(r)
    assert "sessions" not in r and "channels" not in r


def test_missing_fields_bad_json_and_cli_failure_fail_closed(monkeypatch):
    for data in ["no-json", "[]", '{"sessions":{}}', '{"heartbeat":{},"queuedSystemEvents":0,"sessions":[]}']:
        cli(monkeypatch, stdout=data)
        r = gateway.verify_openclaw_rpc()
        assert r["status"] == "invalid-response" and not r["rpc_verified"]
    cli(monkeypatch, stdout="HIDDEN-SECRET", exit_code=1)
    r = gateway.verify_openclaw_rpc()
    assert r["status"] == "rpc-unavailable" and "HIDDEN" not in repr(r)


def test_timeout_and_output_limit(monkeypatch):
    cli(monkeypatch, stdout="x"*1_000_001)
    assert gateway.verify_openclaw_rpc()["status"] == "rpc-unavailable"
    monkeypatch.setattr(gateway.subprocess, "run", lambda *a, **kw: (_ for _ in ()).throw(subprocess.TimeoutExpired("openclaw", 15)))
    assert gateway.verify_openclaw_rpc()["status"] == "rpc-unavailable"


def test_api_requires_explicit_local_mutation_header(tmp_path, monkeypatch):
    cli(monkeypatch)
    c = TestClient(create_app(tmp_path / "test.sqlite3"))
    assert c.get("/api/openclaw/rpc-check").status_code == 405
    assert c.post("/api/openclaw/rpc-check").status_code == 403
    assert c.post("/api/openclaw/rpc-check", headers={
        **HEADERS, "Origin": "https://untrusted.invalid",
    }).status_code == 403
    result = c.post("/api/openclaw/rpc-check", headers=HEADERS)
    assert result.status_code == 200
    assert result.json()["rpc_verified"] is True
    assert "HIDDEN" not in result.text
