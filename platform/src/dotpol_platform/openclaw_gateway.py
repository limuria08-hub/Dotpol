"""Read-only readiness for LiOS.Pol's required local OpenClaw Gateway.

OpenClaw itself owns WS handshakes, local credentials, pairing, channels and
device policy. Use its documented read-only CLI health command rather than
emulating privileged protocol calls. No install, downloads, service start or
network access occurs on Dotpol startup.
"""
from __future__ import annotations

import json
import shutil
import subprocess

COMMAND_TIMEOUT_SECONDS = 7


def probe_openclaw() -> dict:
    """Return sanitized gateway health, not credentials or channel metadata.

    This is gateway readiness only; it does not certify paired channels,
    device permissions, skills, tool access or full integration.
    """
    result = {"component": "openclaw", "required_for_release": True,
              "ready": False, "status": "not-installed"}
    executable = shutil.which("openclaw")
    if not executable:
        return {**result, "detail": "OpenClaw CLI is not installed. Required integration is incomplete."}
    try:
        completed = subprocess.run(
            [executable, "health", "--json", "--timeout", "2500"],
            check=False, capture_output=True, text=True,
            timeout=COMMAND_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.TimeoutExpired):
        return {**result, "status": "unreachable",
                "detail": "Local OpenClaw Gateway readiness could not be verified."}
    if completed.returncode != 0:
        # Do not disclose CLI stdout/stderr: they may contain identifiers,
        # filesystem locations, credentials or private diagnostics.
        return {**result, "status": "unreachable",
                "detail": "OpenClaw CLI could not reach a healthy local Gateway."}
    try:
        health = json.loads(completed.stdout)
    except (ValueError, TypeError):
        return {**result, "status": "invalid-response",
                "detail": "OpenClaw returned an unreadable health snapshot."}
    if not isinstance(health, dict):
        return {**result, "status": "invalid-response",
                "detail": "OpenClaw returned an unexpected health snapshot."}
    if health.get("status") == "starting":
        return {**result, "status": "starting",
                "detail": "OpenClaw Gateway is starting; readiness is not yet verified."}
    if health.get("ok") is True:
        return {**result, "status": "gateway-healthy", "ready": True,
                "detail": "OpenClaw health RPC succeeded. Channels, permissions and tools require separate acceptance tests."}
    return {**result, "status": "unhealthy",
            "detail": "OpenClaw Gateway reported an unsuccessful health check."}
