# Dotpol Phase 1 — runnable local research foundation

**Implementation scope:** local projects, TXT/CSV/JSON imports, SHA-256 source lineage, exact line-level keyword matching, evidence-backed *extractive* research artifacts, no-key mode, a Next.js workspace, health and safety tests. This is **not** yet AI model generation, full political ETL, LanceDB hybrid indexing, advanced GIS, or organization login. See the [five-phase roadmap](docs/ROADMAP.md).

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

Local state is stored in `~/.dotpol/dotpol.sqlite3`; set `DOTPOL_DATA_DIR` to choose a different folder. No automatic network requests occur to AI providers; the model-status endpoint reports that generation is not yet enabled.

## Start web

```bash
cd apps/web
npm install
npm run dev
```

Open `http://127.0.0.1:3000` or `http://localhost:3000`. Create a project, import a source and ask about a phrase inside it. Open a saved artifact, inspect line/source hash and export JSON. Files are sent only to the local FastAPI process. Maximum input size is 1 MiB per file for this preview. Do not expose the service beyond localhost; no organization authentication is implemented.

## Test

```bash
python -m pytest -q
cd apps/web && npm run build
```

The browser build requires dependencies to have been installed; no build was run in an isolated environment without npm access. CI attempts the build on GitHub-hosted runners.

## P1 checklist status

- **Implemented, locally tested:** SQLite persistence, import validation, scoped source records, SHA-256 lineage, exact-evidence citation checks, deterministic retrieval, no-evidence state, source withdrawal, API origin/host/mutation checks.
- **Implemented, not yet browser-tested:** Next.js research workspace, file import, saved artifacts and JSON export.
- **Not implemented:** model generation with PydanticAI/Ollama, LanceDB hybrid retrieval, Docling PDF parsing, full BYOAI, user accounts, independent OS release and comprehensive security review. Do not mark P1 verified or released.

## Trust boundaries

Data and citations are linked to original text but source correctness is not guaranteed. Source excerpts are **not** AI analyses. Projects are only isolated logically in personal local mode; they are not access-controlled user accounts. Never expose this preview as an internet-facing or multiuser service. Do not upload private elector information or infer individual political preferences.
