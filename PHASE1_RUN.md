# Dotpol Phase 1 — runnable local research foundation

**Implementation scope:** local projects, TXT/CSV/JSON imports and optional local Docling PDF/DOCX conversion, SHA-256 source lineage, exact line-level retrieval, AI-native cited research with a configured model, artifact persistence, no-key mode, a Next.js workspace and safety tests. The shared model gateway uses PydanticAI and supports local Ollama or explicitly configured HTTPS BYOAI. A real model has not been exercised in this environment. This is **not** full political ETL, LanceDB hybrid indexing, advanced GIS or organization login. See the [five-phase roadmap](docs/ROADMAP.md).

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

Open `http://127.0.0.1:3000` or `http://localhost:3000`. Create a project, import a source and ask about a phrase inside it. Open a saved artifact, inspect its evidence, edit under the same artifact ID, inspect revision history and export JSON. Human edits remain explicitly unverified until their claims are independently reviewed. Files are sent only to the local FastAPI process. Maximum input size is 1 MiB per file for this preview. Do not expose the service beyond localhost; no organization authentication is implemented.

## Test

```bash
python -m pytest -q
cd apps/web && npm run build
```

The browser build requires installed npm dependencies; GitHub Actions independently builds the production app. For a local browser acceptance run, start both the API and web as described above, then:

```bash
cd apps/web
npm install
npx playwright install chromium
npm run test:e2e
```

The CI `browser-e2e` job installs Chromium's OS dependencies, starts the local API and production Next.js application, then tests browser import, evidence-only research, saved revisions/reopen, cross-tab conflicts, no-evidence abstention and keyboard-accessible upload. It does not substitute for testing a real model or public deployment.

## P1 checklist status

- **Implemented, locally tested:** SQLite persistence, import validation, scoped source records, SHA-256 lineage, exact-evidence citation checks, deterministic retrieval, no-evidence state, source withdrawal, API origin/host/mutation checks.
- **Implemented and subject to Chromium acceptance:** Next.js research workspace, source import, saved artifacts with PATCH-based human edits and revision history, JSON export and keyboard-accessible file-picker button.
- **Implemented with mocked AI service tests (live model not verified):** PydanticAI local Ollama and opt-in HTTPS BYOAI adapter, source-grounded AI synthesis path, citation validation, model metadata and persistence, no-model fallback.
- **Not verified/complete:** LanceDB hybrid retrieval, live Docling engine conversion (optional adapter only), organization login, real-model inference, independent OS release and comprehensive security review. Do not mark P1 verified or released.

## Trust boundaries

Data and citations are linked to original text but source correctness is not guaranteed. Source excerpts are **not** AI analyses. Projects are only isolated logically in personal local mode; they are not access-controlled user accounts. Never expose this preview as an internet-facing or multiuser service. Do not upload private elector information or infer individual political preferences.

## P1 current verification ledger (2026-10-30)

- Backend verification: `python -m pytest -q` is executed on every implementation PR by GitHub CI, including request-consent, migration, revision-conflict, document-adapter and source-evidence tests. Use the latest linked PR check for the current result.
- Browser: GitHub CI builds the production Next.js application and runs Playwright/Chromium against the real localhost API. Synthetic-only/no-model browser journeys are distinct from real Ollama inference.
- Real Ollama inference: **not verified**; explicit probe verifies only that the configured model is listed, not that it produces a correct answer.
- Trust: PydanticAI prompt citations are validated for existing IDs, lines and hashes, **not** semantically fact-checked claim by claim; review is required for high-stakes claims.
- Auth, real local AI inference, hybrid retrieval, live Docling extraction/OCR, accessibility audit, dependency locks and full Phase 1 security remain open acceptance gates.

## Optional LanceDB keyword index (next P1 retrieval integration)

The normal local-only retrieval path uses verified project source lines. To enable the selected LanceDB full-text engine, install `python -m pip install -e '.[test,search]'` and set `DOTPOL_SEARCH_ENGINE=auto` (default) or `lancedb`. Index data is derived under `DOTPOL_DATA_DIR/search-index/<project>`; SQLite remains canonical. A missing or failed index is reported as a degraded literal scan, never falsely as indexed retrieval. Every index hit is checked against current source bytes, project ID, line number, SHA-256 and active/withdrawn state. This provides **keyword FTS**, not semantic embeddings or hybrid vector retrieval yet. Run `pytest tests/test_search_index.py -q` with the optional package installed to verify real index rebuild and withdrawal.

## P1.09 Canonical artifact revision contract

- `PATCH /api/projects/{project_id}/artifacts/{artifact_id}` accepts `{"answer":"...","expected_revision":1}` with the required local mutation header.
- `GET /api/projects/{project_id}/artifacts/{artifact_id}/revisions` returns immutable generation/human-edit snapshots. The UI displays history, allows editing and reopening, and retains **the same artifact ID** across revisions.
- Concurrent stale edits receive HTTP 409; a human edit is flagged `user-edited-unverified`. Original source evidence and AI generation metadata are preserved but **do not automatically validate edited claims**. No extra document database or model gateway is created.

## P1.03 Optional Docling document import (2026-10-30)

The existing **one local gateway** additionally accepts PDF/DOCX through
`POST /api/projects/{project_id}/documents` when the optional dependency is installed:

```bash
python -m pip install -e '.[documents]'
```

The existing UI sends an in-memory base64 payload (maximum **1 MiB** original
binary). The gateway uses Docling's `DocumentStream` converter; PDFs use
`NativePdfFormatOption` for **model-free, non-OCR extraction**, avoiding implicit
model downloads. Scanned/image-only PDFs are not supported in this preview.

Document sources preserve **two different hashes**: `file_sha256` for the exact
original uploaded binary and `sha256` for the extracted UTF-8 markdown that
search/citations actually reference. `extraction_method` records the parser.
The DB migration adds nullable metadata columns; older TXT/CSV/JSON sources
retain the same behavior. Import rejects invalid base64, mismatched signatures,
path-like names, empty extracted content and oversized output without saving a
source. Missing Docling returns a truthful 503 rather than an unsupported claim.

**Verification boundary:** automated tests exercise the importer contract through
an in-process Docling stand-in, NOT a live Docling PDF/DOCX conversion. The real
Docling dependency, production Next.js build, real Ollama inference, OCR, hybrid
semantic retrieval and independent clean-install still need verification.
Run `python -m pytest -q` to exercise the P1 core tests. This opt-in parser is
**not** a mandatory service for local AI research.
