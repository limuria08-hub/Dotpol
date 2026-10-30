#!/usr/bin/env bash
# P1 live acceptance: only user-installed local services, no downloads.
# Run from repository root using: bash scripts/p1-live-acceptance.sh
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ "${DOTPOL_AI_PROVIDER:-ollama}" != "ollama" ]]; then
  echo "ERROR: P1 live gate requires local Ollama, not a remote model provider." >&2
  exit 2
fi
if [[ -z "${DOTPOL_AI_MODEL:-}" ]]; then
  echo "ERROR: set DOTPOL_AI_MODEL to a preinstalled local Ollama model." >&2
  exit 2
fi
if ! command -v openclaw >/dev/null 2>&1; then
  echo "ERROR: required OpenClaw CLI is not installed." >&2
  exit 2
fi
if ! command -v ollama >/dev/null 2>&1; then
  echo "ERROR: local Ollama CLI is not installed." >&2
  exit 2
fi
python -c 'import docling' || {
  echo "ERROR: Docling is not installed. Install local documents extra first." >&2
  exit 2
}

export DOTPOL_AI_PROVIDER=ollama
export DOTPOL_LIVE_OLLAMA_TEST=1
export DOTPOL_LIVE_OPENCLAW_TEST=1
export DOTPOL_LIVE_DOCLING_TEST=1

echo "Running real Ollama, OpenClaw Gateway and Docling tests; all must PASS."
python -m pytest -q -rs \
  tests/test_live_ollama_inference.py \
  tests/test_live_openclaw_rpc.py \
  tests/test_live_docling_conversion.py

echo "P1 live runtime checks passed. Browser CI and manual WCAG review are separate gates."
