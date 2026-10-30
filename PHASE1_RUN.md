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


### Explicit OpenClaw baseline security audit (P1.11)

The Phase 1 research shell has a **Security audit** control beneath the OpenClaw gateway check. Only a user click triggers the local FastAPI endpoint:

```bash
curl -X POST -H 'X-Dotpol-Local: 1' http://127.0.0.1:8765/api/openclaw/audit
```

The backend executes **`openclaw security audit --json`** (ordinary read-only mode, **never** `--fix`, `--deep`, or `--token`). It requires the installed local OpenClaw binary, never starts OpenClaw, and never saves or returns raw findings, channel identities, credentials, local file paths or stderr. The response contains only nonnegative `critical_count`, `warning_count`, `info_count`, `suppressed_count`, `audit_performed`, `review_required`, and a fixed status/detail. Invalid outputs, timeouts, nonzero exit codes, or missing install fail closed. A suppressed finding always requires review even when active warning counts are zero.

**A clean basic audit does not certify secure operation.** OpenClaw's trust model is one trusted operator/group per gateway. A production OpenClaw integration still requires authenticated/personalized channel access, paired devices, effective tool sandboxing, exact plugin permissions, deep/live audit, and real end-to-end channel tests. This feature is not a finished P4/P5 gateway integration.

Backend tests: `pytest tests/test_openclaw_audit.py -q`. Browser tests: `cd apps/web && npm run test:e2e` (requires the local API/web and Playwright). CI remains the authoritative production build verification after this change.

## P1.11 — Required OpenClaw Gateway foundation (2026-10-30)

**Product decision:** OpenClaw is a **required component of a complete LiOS.Pol release**, not an optional service. OpenCloud is not part of this product. The five-phase canonical plan assigns readiness/contracts to P1, authorized team/channel integration to P4, and full gateway, skills, devices, automations, lifecycle and security acceptance to P5.

The existing FastAPI local gateway exposes a **read-only** status endpoint:

```bash
curl --fail http://127.0.0.1:8765/api/openclaw/status
```

It discovers the installed OpenClaw CLI and executes the documented `openclaw health --json --timeout 2500` command with no shell, bounded timeout, and no auto-install, model download, gateway startup, or access to channel content. The response is a sanitized `required_for_release` / `ready` / `status` / `detail` summary; the raw CLI payload, stderr, credentials and channel identities are never returned.

- `not-installed` means a **required release dependency has not been installed** (not that the feature is optional).
- `unreachable`, `starting`, `unhealthy` or `invalid-response` mean the gateway is not verified ready.
- `gateway-healthy` confirms a successful health RPC **only**. It does not certify secure channel pairing, device policy, tool permissions, skills, runtime supervision or production readiness.
- The read-only probe does not replace PydanticAI's evidence-grounded political research tool chain. OpenClaw retains ownership of its own gateway, channel/device pairing and skills.
- OpenClaw's upstream security guide recommends **one trust boundary per gateway**; use distinct gateway instances/credentials for mutually untrusted organizations. Do not expose full operator tokens to browser clients.

The Next.js shell now includes a compact **OpenClaw · Required** status control. The user explicitly clicks **Check gateway** to query this local API; the browser never contacts the OpenClaw gateway directly and does not receive operator credentials. Playwright covers the initial not-checked state, not-installed and healthy results, failed calls, and response-secret omission. A green UI test does not certify actual installed channel/device readiness.

Automated tests mock the OpenClaw CLI and cover missing installation, startup, errors, timeouts, sanitized health, and rejected remote origins. **Real installed gateway integration remains pending** until live local test and P4/P5 acceptance. Avoid claiming complete OpenClaw integration based solely on this status endpoint.



## P1.05/P1.07 — Explicit real-model verification and grounded synthesis screening

The **existing** PydanticAI gateway now screens every nonempty model-answer sentence for a valid project-retrieved bracketed citation. Each numeric token and directly quoted string in that sentence must occur in the **cited** source excerpts; wrong-source references, missing citations, fabricated numbers/years or fabricated exact quotations return HTTP 422 and **no AI artifact is saved**. The canonical SQLite store continues to independently verify project-scoped source IDs, line numbers, exact excerpts, active status and hashes. New synthetic regression tests cover plausible-looking fabricated statistics and adversarial source instructions; these are **mocked model tests**, not real inference.

**Important limitation:** this rule is a deterministic safety screen, **not semantic entailment or independent fact-checking**. It cannot establish that interpretations, inferred causation, named-entity claims or paraphrases are correct merely because citation IDs and numeric tokens match. The strict sentence-level citation requirement may reject otherwise acceptable model prose; this is deliberate fail-closed preview behavior. Human reviewers must verify material political claims against primary sources.

### Opt-in real local Ollama smoke test (not yet verified)

This test is **skipped in ordinary CI** and does not install a model or contact a hosted provider. Explicitly install/start Ollama and pull a compatible local model first, then run from the repository root:

```bash
DOTPOL_LIVE_OLLAMA_TEST=1 DOTPOL_AI_PROVIDER=ollama DOTPOL_AI_MODEL='<your-installed-model>' python -m pytest tests/test_live_ollama_inference.py -q -rs
```

A successful run must list the configured model, actually invoke PydanticAI against the loopback Ollama API, and return a generated answer with valid saved-evidence references. Because the model response is nondeterministic, a rejected uncited/unfounded answer makes this acceptance test fail rather than silently switching to extractive mode. A real local-model pass has **not** been observed in the GitHub-hosted checks; do not mark the P1.05 live inference gate complete.


## P1.08/UI-04 — Resizable conversation and canonical workbench

The current **single Next.js application** uses the exact direct dependencies
`react-resizable-panels@2.1.9` (MIT) and `lucide-react@0.469.0` (ISC, Feather
attribution for applicable icon designs). See `apps/web/THIRD_PARTY_NOTICES.md`
for the dependency ledger, source links and unclosed licence checks.

A question submitted to the **existing** FastAPI `/api/projects/{id}/research`
route creates one canonical SQLite Artifact. The conversation renders the persisted
question/answer preview and **Open in workbench** opens that same ID. On desktop
the conversation and artifact are resizable using a keyboard-operable handle;
panel sizing is saved locally by `react-resizable-panels`. On narrow screens
the same content stacks without creating a second editor or research store.
Edits continue to use the original `PATCH` revision endpoint, source provenance,
conflict protection and JSON export. The existing OpenClaw status remains separate
and read-only; the UI does not copy gateway tokens or channel data.

External BYOAI evidence consent is **consumed at submission time**, even if the
provider request fails, and is cleared when editing the question or switching
research modes/projects. Browser acceptance covers these privacy cases without
contacting a real external model. A failed request never silently grants the next
request permission.

**Unfinished:** shadcn/Radix token adoption, assistant-ui custom REST adapter
(only if compatible), Lexical editing, complete screen-reader/manual WCAG audit,
full npm lockfile, package licence/SBOM review and real Ollama acceptance.
Nothing about panel rendering certifies those unimplemented integrations.

### Authenticated OpenClaw RPC bridge (P1.11)

The next acceptance level after health/audit is the **actual OpenClaw WebSocket control plane**. LiOS.Pol does **not** implement a second WebSocket handshake or duplicate the OpenClaw identity/pairing store. The backend delegates connection authentication to the installed upstream OpenClaw CLI and calls only a fixed **read-only** `status` RPC:

```bash
# Run an installed, configured and paired OpenClaw Gateway first.
openclaw gateway call status --params '{"includeChannelSummary":false}' --json --timeout 4000

# Ask the local Dotpol API to verify the same authenticated RPC:
curl -X POST -H 'X-Dotpol-Local: 1' http://127.0.0.1:8765/api/openclaw/rpc-check
```

The Dotpol endpoint runs a bounded subprocess with **no shell, no token/password arguments, no arbitrary method/parameters, and no auto-start**. OpenClaw's maintained CLI chooses the configured Gateway and handles its normal device credentials, scopes and authenticated WebSocket protocol. The original RPC payload (which may contain session, channel, identity or host details) stays server-side and is **never returned**. Only `rpc_verified`, `status`, `required_for_release` and a fixed explanatory string are returned. Invalid replies, missing installation, CLI failures or timeouts fail closed.

```bash
# Real local integration evidence (opt-in, skipped by default CI):
DOTPOL_LIVE_OPENCLAW_TEST=1 PYTHONPATH=platform/src:services/api \
  pytest tests/test_live_openclaw_rpc.py -q

# Default mock-based regression suite:
PYTHONPATH=platform/src:services/api pytest tests/test_openclaw_rpc.py -q
```

The LiOS.Pol sidebar has a user-triggered **Verify connection** control alongside **Check gateway** and **Security audit**. It requests only `POST /api/openclaw/rpc-check` and displays the sanitized success/failure summary. No authenticated RPC is attempted automatically when the UI loads. The browser never receives the raw Gateway status document, operator token, session identities, channel metadata or CLI stderr. Browser regression checks cover the opt-in action, absent gateway, successful RPC, transport errors and dropped credential fields. `rpc-connected` confirms only the CLI-authenticated read-only status operation, **not** authorization for OpenClaw agent tool calls.

A passing **real** RPC test demonstrates the installed OpenClaw CLI can complete an authenticated status request with its configured gateway. It does **not** grant per-organization role isolation, approve OpenClaw tools, establish channel pairing, demonstrate device commands, or prove a secure production deployment. Those remain P4/P5 gates. In particular, the CLI's identity may be an **operator credential**; do not forward user-submitted method names or data to the CLI and do not expose its credentials to the browser.



## P1.08/UI-02 — Shared Radix/Tailwind controls with reproducible install

The existing Next.js shell now uses a **small project-owned shadcn-style
component layer** rather than adding a second UI application. Tailwind CSS v4
runs through a local PostCSS plugin. Radix `react-slot`, `react-label`,
and `react-dialog` back accessible Button, Label and source-provenance
controls; Input is a local shared React component. The project, file-import,
research and workbench flows still use the **same FastAPI/SQLite artifact and
source IDs**. The source-provenance dialog displays the original canonical
source ID, complete SHA-256, origin and status and closes via Escape with
keyboard focus restored. No cloud assets, UI data store, new model service or
hosted component provider are introduced.

**Reproducible web dependency workflow:**

```bash
cd apps/web
npm ci --no-audit --no-fund
npm run build
# With local API + web running, Chromium installed:
npm run test:e2e
```

The checked-in `apps/web/package-lock.json` is generated from the successful
Node 22 GitHub Actions install; both web and Chromium CI jobs use `npm ci`
rather than floating npm installs. This pins the resolved dependency graph,
but it does **not** replace a full transitive licence, SBOM or vulnerability
audit. See `apps/web/THIRD_PARTY_NOTICES.md` for the installed subset and
upstream licence references.

**UI-03 boundary:** assistant-ui remains an **uninstalled candidate** until
its external/local REST runtime is validated against the **existing**
`POST /api/projects/{id}/research` contract. No Assistant Cloud,
unreviewed model calls or duplicate thread database will be introduced.
The current conversation already previews saved artifacts with their exact
canonical IDs; this is the working fallback, not evidence that assistant-ui
has been assimilated. Retain no-model, request-scoped remote consent and
required OpenClaw controls during any future renderer evaluation.

**Still open:** complete Radix/shadcn navigational coverage, manual WCAG
screen-reader/keyboard audits, assistant-ui compatibility, real local Ollama
and installed OpenClaw integration. A passing browser fixture verifies the
specified journey only.
