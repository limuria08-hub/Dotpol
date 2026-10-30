"""Explicit live OpenClaw Gateway acceptance check.

Skipped in ordinary CI, which has no OpenClaw installation. Opt in only after
installing, pairing and launching the maintained upstream local Gateway.
This runs read-only health and authenticated status WebSocket RPC; it does not
send any political data, messages, tool calls or device actions.
"""
import os
import pytest
from dotpol_platform import openclaw_gateway


@pytest.mark.skipif(
    os.environ.get("DOTPOL_LIVE_OPENCLAW_TEST") != "1",
    reason="Live OpenClaw gateway test requires user opt-in and installed paired gateway",
)
def test_live_openclaw_health_and_authenticated_status_rpc():
    health = openclaw_gateway.probe_openclaw()
    assert health["ready"], f"Required Gateway is not ready: {health['status']}"
    rpc = openclaw_gateway.verify_openclaw_rpc()
    assert rpc["rpc_verified"], f"Authenticated status RPC failed: {rpc['status']}"
    assert rpc["required_for_release"]
