# Dotpol Phase 1 — Foundation Implementation Checklist

**Status:** Planning baseline; **all tasks below unimplemented**  
**Source of truth:** [Master Plan](../../MASTER_PLAN.md) · [Sprint](../../RAPID_REUSE_SPRINT.md) · [ADR-0001](../../DECISIONS/0001-foundation-module-ownership.md)

## One physical implementation layout

```text
apps/web/                                  Next.js user interface
services/api/dotpol_api/                  FastAPI endpoints, wiring, local config
services/api/tests/                       API integration tests
platform/src/dotpol_platform/ai/          PydanticAI runtime, typed tools, Ollama adapter
platform/src/dotpol_platform/data/        SQLite project/source records and import contracts
platform/src/dotpol_platform/provenance/  source/evidence/run lineage and validation
platform/src/dotpol_platform/search/      phase-3 search index adapter (NOT built in phase 1)
platform/tests/                           reusable capability tests
packages/contracts/                       versioned shared API payload schemas if needed
.github/workflows/ci.yml                  Python/web test and safe build checks
```

`platform/*` in the capability registry names the **logical owner**. Use the Python **import namespace `dotpol_platform`** and a properly configured editable package sourced from `platform/src`; **never use `import platform.ai`**, which collides with Python's `platform` standard-library module. The API imports these registered packages; it does not implement competing `dotpol_api/ai`, `dotpol_api/sources`, `dotpol_api/provenance` or `dotpol_api/tools` repositories.

One FastAPI process and one SQLite source of truth for local mode. Avoid a second model provider/router, search framework, GIS engine or PostgreSQL in Phase 1.

## Tasks (small independent PRs)

| ID | Owner | Implement | Acceptance |
|---|---|---|---|
| P1-1 | `services/api` | FastAPI app, loopback defaults, `GET /health`, local settings | Starts with no cloud credentials; rejects unsafe origins/host settings |
| P1-2 | `platform/data` | Local SQLite project store, filesystem paths and migrations | Create/list/open/reopen project; reject traversal/symlink escapes; recover after restart |
| P1-3 | `platform/data` + `platform/provenance` | Source IDs, import metadata, hash, evidence references, run record | Unknown/withdrawn sources cannot be represented as verified evidence |
| P1-4 | `platform/ai` | PydanticAI provider-neutral tool gateway, Ollama adapter, unavailable-model state | No-provider start, no secret logging, no default external request |
| P1-5 | `platform/ai` | One typed tool registry; read-only source lookup | Tool output includes valid source IDs and an explicit no-evidence state |
| P1-6 | `apps/web` | Next.js local shell, project workspace and API client | End-to-end create/reopen UI, loading/error states, keyboard access |
| P1-7 | CI/release owner | Python/web CI, run instructions, local integration fixture | Fresh local install + tests on one declared OS; zero paid credentials |

**Task order:** P1-1 → P1-2/P1-3 → P1-4/P1-5 → P1-6/P1-7. Parallelize web and platform only against agreed typed contract fixtures; don't duplicate API- or platform-owned schemas.

## Minimum schemas

`Project`, `SourceRecord`, `EvidenceRef`, `ToolRun`, `ProviderStatus`, `ResearchEvent`. Specify stable IDs, content checksum, timestamp with timezone, provenance/source state and validation. `services/api` owns HTTP serializers; reusable platform modules own domain behaviour. Design public versions before code.

## Mandatory negative tests

- Local API rejects origin/CSRF/file traversal attacks; no private data is leaked to external services by default.
- Project survives restart, directory rename/path validation, malformed input and failed transaction.
- A fabricated or withdrawn source reference cannot become a valid citation.
- Missing local model returns a clear state and does not prevent project/file operations.
- Untrusted document prompt instructions cannot invoke network/write tools; no tool permission escalation.
- Sensitive config values never enter trace/log output.
- CI evaluates untrusted public PR code without write tokens/secrets; licence and dependency gates recorded.

## Done means

Passing API + platform + web tests, reproducible local start, actual no-network/no-key smoke, valid source IDs, and reviewer-verified evidence of persistence. A draft plan, a fork or a green documentation check is **not** product progress.

**Later phases only:** Docling document import, LanceDB hybrid retrieval, elections, GIS, statistics, forecasts, field/survey flows and live war-room operations. Refer to [Master Plan](../../MASTER_PLAN.md) and [field contract](../../PRE_ELECTION_MICROAREA_INTELLIGENCE.md), not extra foundation implementations.
