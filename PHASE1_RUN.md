# Dotpol Phase 1 — runnable local research foundation

**Implementation scope:** local projects, TXT/CSV/JSON imports, SHA-256 source lineage, exact line-level retrieval, AI-native cited research with a configured model, artifact persistence, no-key mode, a Next.js workspace and safety tests. The shared model gateway uses PydanticAI and supports local Ollama or explicitly configured HTTPS BYOAI. A real model has not been exercised in this environment. This is **not** full political ETL, LanceDB hybrid indexing, advanced GIS or organization login. See the [five-phase roadmap](docs/ROADMAP.md).

## Requirements

Python 3.11+, Node 22+, no paid keys, no Docker required.

## Start API

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
PYTHONPATH=platform/src:services/api uvicorn app:app --host 127.0.0.1 --port 8765
```

Local state is stored in `~/.dotpol/dotpol.sqlite3`; set `DOTPOL_DATA_DIR` to choose a different folder. No automatic network requests occur to AI providers on startup. Model availability is checked only when you explicitly click **Check local model** (which contacts the localhost Ollama `/api/tags` endpoint and does not run inference). To activate AI synthesis, install/run [Ollama](https://github.com/ollama/ollama) locally, pull a compatible model and configure it explicitly:

```bash
export DOTPOL_AI_PROVIDER=ollama
export DOTPOL_AI_MODEL=<your-installed-model-name>
export DOTPOL_OLLAMA_URL=http://127.0.0.1:11434
```

PydanticAI uses Ollama's local OpenAI-compatible API at `/v1`. The configured model is invoked only when you submit a research question whose source evidence exists. `GET /api/ai/status` reports **configuration**, not actual runtime readiness. No model download is performed automatically.

Optional BYOAI (explicitly user-supplied, not required) uses `DOTPOL_AI_PROVIDER=openai-compatible`, `DOTPOL_AI_API_BASE=https://provider.example/v1`, `DOTPOL_AI_MODEL`, and `DOTPOL_AI_API_KEY`. Only a user-configured HTTPS endpoint is accepted. **Configuring BYOAI is not authorization to send project data**: each remote research request requires checking the one-request consent box in the UI, or supplying `allow_remote_evidence: true` to the API explicitly. A denied request returns `remote-consent-required` without contacting the external provider. The consent is not saved for future requests. Do not configure BYOAI for sensitive projects without a valid data-sharing basis. Keys are never returned to the browser. A model with no retrieved project evidence is not invoked.

No model? The workspace continues to import, inspect and return source excerpts without labeling them as AI generation.

## Start web

```bash
cd apps/web
npm install
npm run dev
```

Open `http://127.0.0.1:3000` or `http://localhost:3000`. Create a project, import a source and ask about a phrase inside it. Open a saved artifact, inspect line/source hash, edit its text and save a new revision under the same artifact ID, review revision history, or export JSON. Human edits retain original evidence references but are explicitly labelled as human-authored; unchanged citations do not prove new claims. Files are sent only to the local FastAPI process. Maximum input size is 1 MiB per file for this preview. Do not expose the service beyond localhost; no organization authentication is implemented.

## Test

```bash
python -m pytest -q
cd apps/web && npm run build
```

The browser build requires dependencies to have been installed; not yet verified locally because npm dependencies are unavailable here. CI will attempt the build in GitHub Actions.

## P1 checklist status

- **Implemented, locally tested:** SQLite persistence, import validation, scoped source records, SHA-256 lineage, exact-evidence citation checks, deterministic retrieval, no-evidence state, source withdrawal, API origin/host/mutation checks.
- **Implemented, not yet browser-tested:** Next.js research workspace, file import, saved artifacts, same-ID editing with revision history and JSON export.
- **Implemented with mocked AI service tests (live model not verified):** PydanticAI local Ollama and opt-in HTTPS BYOAI adapter, source-grounded AI synthesis path, citation validation, model metadata and persistence, no-model fallback.
- **Not implemented:** LanceDB hybrid retrieval, Docling PDF parsing, organization login, independent OS release and comprehensive security review. A live model run and browser build remain verification gates. Do not mark P1 verified or released.

## Artifact editing and revision safety (P1.09)

Artifacts retain a stable ID in chat, saved research and the workbench. The local API supports:
- `GET /api/projects/{project_id}/artifacts/{artifact_id}/revisions` — original answer plus dated human revisions.
- `POST /api/projects/{project_id}/artifacts/{artifact_id}/revisions` — `{"answer":"...","expected_revision":1}` with the required `X-Dotpol-Local: 1` header.

A matching revision increments the version without changing the artifact ID, original source references, generation method or model provenance. A stale edit returns **409 revision-conflict**; invalid text/versions return 422, and cross-project artifact references return 404. Old SQLite databases are migrated in place and legacy artifacts backfilled as revision 1. This is single-user localhost editing, **not** multiuser permissions, a semantic citation checker or an externally audited collaborative editor. A user must re-check evidence after modifying content. Python API/migration regression tests cover this behavior; real-browser E2E acceptance is still outstanding.

## Trust boundaries

Data and citations are linked to original text but source correctness is not guaranteed. Source excerpts are **not** AI analyses. Projects are only isolated logically in personal local mode; they are not access-controlled user accounts. Never expose this preview as an internet-facing or multiuser service. Do not upload private elector information or infer individual political preferences.

## P1 current verification ledger (2026-10-30)

- Local backend verification: `PYTHONPATH=platform/src:services/api pytest -q` — **11 passed** (including external model per-request consent, local-only model probe, and provider endpoint guards).
- Browser: not built here. `npm install --offline` returned `ENOTCACHED` for dependencies. GitHub CI is the required next build verification.
- Real Ollama inference: **not verified**; explicit probe verifies only that the configured model is listed, not that it produces a correct answer.
- Trust: PydanticAI prompt citations are validated for existing IDs, lines and hashes, **not** semantically fact-checked claim by claim; review is required for high-stakes claims.
- Auth, paid-free local AI availability, comprehensive hybrid retrieval, document/OCR import and full Phase 1 security remain open acceptance gates.

## Optional LanceDB keyword index (next P1 retrieval integration)

The normal local-only retrieval path uses verified project source lines. To enable the selected LanceDB full-text engine, install `python -m pip install -e '.[test,search]'` and set `DOTPOL_SEARCH_ENGINE=auto` (default) or `lancedb`. Index data is derived under `DOTPOL_DATA_DIR/search-index/<project>`; SQLite remains canonical. A missing or failed index is reported as a degraded literal scan, never falsely as indexed retrieval. Every index hit is checked against current source bytes, project ID, line number, SHA-256 and active/withdrawn state. This provides **keyword FTS**, not semantic embeddings or hybrid vector retrieval yet. Run `pytest tests/test_search_index.py -q` with the optional package installed to verify real index rebuild and withdrawal.
