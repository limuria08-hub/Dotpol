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


def audit_openclaw_security() -> dict:
    """Explicit, read-only baseline audit. Never expose findings or CLI output.

    This is NOT a security clearance: deep/live checks, pairing and per-team
    authorization require their own evidence in P4/P5.
    """
    base = {"component": "openclaw", "required_for_release": True,
            "audit_performed": False, "review_required": True,
            "status": "not-installed"}
    executable = shutil.which("openclaw")
    if not executable:
        return {**base, "detail": "OpenClaw must be installed before its configuration can be audited."}
    try:
        completed = subprocess.run(
            [executable, "security", "audit", "--json"],
            check=False, capture_output=True, text=True, timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired):
        return {**base, "status": "audit-unavailable",
                "detail": "Local OpenClaw security audit could not finish."}
    if completed.returncode != 0 or len(completed.stdout) > 2_000_000:
        return {**base, "status": "audit-unavailable",
                "detail": "OpenClaw security audit failed. Review it locally in the terminal."}
    try:
        report = json.loads(completed.stdout)
    except (ValueError, TypeError):
        return {**base, "status": "invalid-response",
                "detail": "OpenClaw security audit returned an invalid report."}
    if not isinstance(report, dict) or not isinstance(report.get("findings"), list):
        return {**base, "status": "invalid-response",
                "detail": "OpenClaw security audit report did not match the expected schema."}
    summary = report.get("summary")
    if not isinstance(summary, dict):
        return {**base, "status": "invalid-response",
                "detail": "OpenClaw security audit report did not include a valid summary."}
    counts = {key: summary.get(key) for key in ("critical", "warn", "info")}
    if any(type(value) is not int or value < 0 for value in counts.values()):
        return {**base, "status": "invalid-response",
                "detail": "OpenClaw security audit counts were invalid."}
    suppressed = report.get("suppressedFindings", [])
    if not isinstance(suppressed, list):
        return {**base, "status": "invalid-response",
                "detail": "OpenClaw security audit suppression data was invalid."}
    review_required = bool(counts["critical"] or counts["warn"] or suppressed)
    return {
        **base, "audit_performed": True, "review_required": review_required,
        "status": "findings-require-review" if review_required else "baseline-no-findings",
        "critical_count": counts["critical"], "warning_count": counts["warn"],
        "info_count": counts["info"], "suppressed_count": len(suppressed),
        "detail": ("Review OpenClaw's full local security audit before enabling tools or channels."
                   if review_required else
                   "No warnings in the basic OpenClaw audit; deep checks, pairing and tool permissions remain unverified."),
    }

def verify_openclaw_rpc() -> dict:
    """Prove a real authenticated *read-only* OpenClaw WebSocket RPC.

    Delegate credential selection, signed device pairing, scopes, and protocol
    versions to the maintained OpenClaw CLI. Dotpol invokes one fixed RPC
    method only, never routes untrusted method names or model instructions.
    This check does not grant authorization to invoke other RPC methods.
    """
    base = {
        "component": "openclaw", "required_for_release": True,
        "rpc_verified": False, "status": "not-installed",
    }
    executable = shutil.which("openclaw")
    if not executable:
        return {**base, "detail": "Install and configure the required OpenClaw Gateway to verify its RPC connection."}
    try:
        completed = subprocess.run(
            [
                executable, "gateway", "call", "status",
                "--params", '{"includeChannelSummary":false}',
                "--json", "--timeout", "4000",
            ],
            check=False, capture_output=True, text=True, timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired):
        return {**base, "status": "rpc-unavailable",
                "detail": "OpenClaw Gateway authenticated RPC could not be completed."}
    if completed.returncode != 0 or len(completed.stdout) > 1_000_000:
        # The CLI owns auth. Do not return its stdout, stderr, target URL,
        # session identifiers, channel configuration, or gateway token.
        return {**base, "status": "rpc-unavailable",
                "detail": "OpenClaw Gateway RPC failed. Check gateway access locally."}
    try:
        payload = json.loads(completed.stdout)
    except (TypeError, ValueError):
        return {**base, "status": "invalid-response",
                "detail": "OpenClaw Gateway returned an unreadable RPC response."}
    # These required status-summary fields are emitted by OpenClaw's upstream
    # status RPC, as opposed to a local CLI command without a gateway session.
    if (not isinstance(payload, dict) or
            not isinstance(payload.get("sessions"), dict) or
            "heartbeat" not in payload or
            "queuedSystemEvents" not in payload):
        return {**base, "status": "invalid-response",
                "detail": "OpenClaw status response did not match the supported RPC schema."}
    return {
        **base, "rpc_verified": True, "status": "rpc-connected",
        "detail": "OpenClaw authenticated status RPC succeeded. Channel pairing, tool permissions and device actions still require separate tests.",
    }
