"""P1.05 optional *real* Ollama inference acceptance gate.

Default CI skips this test. To run it, explicitly install and launch Ollama,
pull an installed compatible model, then set DOTPOL_LIVE_OLLAMA_TEST=1,
DOTPOL_AI_PROVIDER=ollama and DOTPOL_AI_MODEL=<installed model>. It never
downloads a model or contacts an external provider automatically.
"""
import os
import asyncio
import pytest

from dotpol_platform import ai


@pytest.mark.skipif(
    os.getenv("DOTPOL_LIVE_OLLAMA_TEST") != "1",
    reason="Real Ollama inference requires an explicit opt-in and installed model",
)
def test_real_local_ollama_infers_and_cites_source():
    cfg = ai.config()
    assert cfg.get("provider") == "ollama", "Live test must use local Ollama, never a remote BYOAI provider"
    assert cfg.get("configured"), "Set DOTPOL_AI_MODEL to a locally installed Ollama model"
    listed = asyncio.run(ai.probe_local_model())
    assert listed["ready"], f"Configured local model not ready: {listed['status']}"

    evidence = [{
        "source_id": "a" * 32, "source_name": "synthetic-report.txt",
        "sha256": "b" * 64, "line": 1,
        "excerpt": "The fictional public research project recorded 73 percent turnout in 2024.",
    }]
    answer, cited, model_id = asyncio.run(ai.synthesize(
        "In what year did the fictional project record turnout? Cite the line.",
        evidence,
    ))
    assert answer.strip() and "[1]" in answer
    assert cited == evidence
    assert model_id == f"ollama:{cfg['model']}"
    # Citation syntax and numeric support are checked by ai.synthesize.
    # This confirms a real model response, NOT independent semantic accuracy.
