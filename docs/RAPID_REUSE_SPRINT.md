# Dotpol Rapid Reuse Sprint — 3–7-Day First Working Release

**Selected technology authority:** [Master Plan](MASTER_PLAN.md) and [selected stack](SINGLE_STACK_SELECTION.md). This sprint is the first preview subset, not permission to install later-phase dependencies.

**Date:** 2026-10-15  
**Status:** Proposed time-boxed execution plan; **no implementation authorized by this document**.  
**Target:** The **first runnable, local-first research MVP**, not all 13 roadmap phases.  
**Source of truth:** [Master Plan](MASTER_PLAN.md); supporting implementation detail: [Blueprint](BLUEPRINT.md), [Roadmap](ROADMAP.md), and [Phase 1 plan](superpowers/plans/2026-10-15-dotpol-foundation.md).  
**Approved planning ADRs:** [foundation ownership](DECISIONS/0001-foundation-module-ownership.md) and [single stack](DECISIONS/0002-one-stack-per-capability.md). Source/licence/CI checks still required.

## Product outcome and honest scope

**Day-3 checkpoint:** Demonstrate Dotpol running on **one supported local development OS**: web workspace; local FastAPI gateway; create/reopen project; model gateway can connect to an installed local Ollama-compatible model or explicitly show an unavailable-model state; a bounded research-tool flow produces observable events. A fake citation is not acceptable. Components must pass the tests actually present, not only appear in a mock-up.

**Day-7 stretch goal:** A newcomer can use documented steps to run it locally, import at least TXT plus CSV/JSON (using available permissive parsers/stdlib where suitable), see sources and source records, search/query those sources, obtain a response with verifiable document-line or dataset-row citations **when model is available**, save/export a brief, close and reopen the project without loss. Without an installed model, import/query/source inspection still works and UI clearly states AI is unavailable. A Docling PDF path is a **stretch** and can be cut without falsely claiming PDF is supported.

**Explicitly NOT done in 3–7 days:** full nationwide election ETL, complex GIS/Kepler, psephology, probabilistic forecasts, policy/legislation ingestion across jurisdictions, real-time media collection, campaign field operations/war room, validated 14-agent suite, international connectors, cross-platform distribution and enterprise deployment. These remain Phases 4–12; a demo cannot be advertised as completion.

This is an engineering sprint *target*, **not a promised delivery date**; feasibility depends on available maintainers, local dev/test environment, model download, upstream compatibility, credentials, approvals and CI. If one developer alone must integrate and certify every component, plan longer. At the end, label completed work by actual verified evidence.

## Time-boxed critical path (7 calendar-day target, if work is authorized immediately)

| Window | Minimal workstream | Single capability owner | Reuse first | Exit evidence |
|---|---|---|---|---|
| **Day 1** | Resolve only blocking Phase 0 decisions; establish repo contracts, local gateway, health check, run instructions and CI skeleton | architecture + `services/api` | FastAPI, Pydantic, GitHub Actions | One fresh local start; loopback, health, CI smoke; no API key |
| **Day 2** | SQLite project lifecycle; filesystem source registry + evidence IDs; first local import and non-AI inspection | `platform/data` + `platform/provenance` | SQLite stdlib, typed contracts; format parsers already available | Create/import/reopen without loss; stable ids; negative path tests |
| **Day 3** | Next.js research shell + AI gateway/tool invocation; local Ollama adapter path; user-visible missing-model behavior | `apps/web` + `platform/ai` | Next.js, PydanticAI, Ollama (user-managed); Vane **UI modules only after rights/security review** | Working integrated vertical demo; stream/events; no invented citations |
| **Day 4** | Indexed local TXT/CSV/JSON retrieval, exact row/line source linkage; minimal evidence registry | `platform/search` + documents/data | LanceDB OSS full-text index with stable evidence IDs; bounded lightweight format parsers | Known-answer and unknown-answer fixtures; no-network tests |
| **Day 5** | Research agent ties retrieval to source evidence; answer/brief export, abstention and model-failure paths | `platform/search`, `platform/ai`, `platform/provenance` | PydanticAI tools + existing document/research UX | Fake/withdrawn/missing citation rejected; export matches evidence |
| **Day 6** | Security, privacy, docs, integration regression; optional PDF import if Docling fits without destabilizing scope | security + data + docs | Existing scanners/test libraries; Docling optional | SSRF/path/prompt-injection fixtures; CI/local no-key passes |
| **Day 7** | Fix blockers, clean fresh-start demo, licence/attribution inventory, tag first working preview **only if gates pass** | release owner | Existing packaging, CI artifacts | Independent reviewer reproduces on one OS; no known P0 blocker |

**3-day fast path:** Days 1–3 are the runnable spine and honest demo. **7-day path:** Days 4–7 add trustworthy local source-backed research. Dates are target windows, not guaranteed time estimates.

## Reuse choices made for speed

| Capability | Fastest approach | Why we choose it | Avoid now |
|---|---|---|---|
| UI | Next.js/React + existing accessible components; selectively adapt Vane source/citation/progress UI after approval | One app; avoid building chart/chat scaffolding from zero | embedding complete Vane app and its separate backend |
| API | FastAPI local gateway, same process for first release | Existing ecosystem and planned architecture | microservices or second Next.js API as canonical backend |
| Storage | SQLite + filesystem, explicit source/evidence identifiers | no external DB deployment | Postgres, second Drizzle data model, premature DuckDB unless CSV size demands it |
| Agent/runtime | one PydanticAI typed-tool runner | already chosen and extensible | LangGraph/CrewAI/parallel Vane agent runtime |
| Model | local Ollama runtime *if already installed*; no-model non-AI mode otherwise | one local provider, zero mandatory cloud cost | automatic heavy model downloads or another inference runtime |
| Retrieval | LanceDB OSS full-text search with exact source/row/line IDs; enable vectors only when available | one search index handles both keyword and semantic retrieval | additional RAG/vector/full-text engines, mandatory web search/SearXNG |
| Documents | basic TXT/CSV/JSON first; Docling behind future adapter | reliably proves citation architecture | full Office/PDF parsing on critical path |
| Donors | use the [selected stack](SINGLE_STACK_SELECTION.md); Vane only for approved source/citation/progress UI | one choice per capability, minimal forks | copying 43 repos or installing competing app backends |

Donor review is **not** an integration blocker if an unapproved Vane component can be replaced by an existing permissive UI primitive. No unverified donor code crosses into product. Cross-phase major architectural changes still require an accepted ADR.

## Parallelization without duplication

Run at most three **contract-compatible** implementation lanes after the Day-1 interface decision:

- **Platform:** FastAPI + SQLite workspace/source registry + provenance; **one** set of canonical IDs.
- **Web/UI:** Next.js shell and typed source/research components; mock contract for early work but production demo uses the real API.
- **AI/research:** PydanticAI provider/tool skeleton and research workflow behind the approved API; cannot define a second source registry or search engine.

Only the responsible owner can change a shared contract; obtain reviewers before parallel work. Freeze `Project`, `SourceRecord`, `EvidenceRef`, `SearchHit`, `ToolRun` and research event schemas as minimum typed interfaces. Make PRs small; do not merge mock-only or frontend-only green CI as product progress.

## Hard-stop gates

1. **No licence decision:** no donor assimilation/release claiming an open-source licence. The proposed Apache-2.0 root licence is not yet approved.
2. **Unresolved architecture ownership:** decide where the canonical AI/data/provenance code lives, then update old Phase-1 example paths before coding. See PR #1 / ADR-0001 proposal.
3. **No source fidelity:** never ship a model answer represented as evidence-backed without verified, valid source/span IDs. Show unavailable/partial states rather than fabricate.
4. **No secure local API path:** loopback-only by default, no arbitrary file reads, safe mutating route/origin/session design, secrets never committed/logged.
5. **Paid service required:** fails ₹0 core. A user-provided local model is optional to non-AI use; don't require hosted LLM, hosted search, map tiles or Postgres.
6. **No reproducible tests:** cannot label verified/released. Record actual CI result, local startup command, test fixtures, environment and limitations.
7. **Unreviewed external network activity:** any web search, provider upload, browser automation or sync must be opt-in, scoped and tested.

## Cut list if schedule is slipping

In order, defer: animations/widgets; multi-provider AI; web search integration; Vane sidecar; auto PDF OCR/complex Docling formats; semantic vectors; charts/maps; fancy export templates; all Phase 4+ features. **Never cut provenance, local persistence, basic input validation, licence gate or end-to-end demo tests.** If necessary, release a smaller *verified* preview rather than an unverified full-feature claim.

## Decision and evidence checklist

- [ ] Maintainer approves scope: '7-day research preview' rather than 'complete political-intelligence OS'.
- [ ] Confirm development OS, model availability, people/reviewers, CI permissions and actual working-hours capacity.
- [ ] Accept/revise architecture ownership proposal + licence decision (PR #1).
- [ ] Approve exact 3–5 donor/dependency shortlist per sprint, no wholesale Vane backend ([donor review](VANE_MODULE_DECISION_MATRIX.md)).
- [ ] Create scoped implementation PRs, one per capability lane with complete acceptance checks.
- [ ] Record actual days and blockers; do not infer a completion percentage from added files/merges.
- [ ] Independently run demo, tests and data-backup/reopen flow before announcing preview.

## Acceptance walk-through (must pass to call the preview done)

1. Fresh checkout: follow local install command; start web and API without a paid account.
2. Create a workspace, import a small public/synthetic TXT or CSV and view source ID, origin and checksum.
3. Restart services and recover workspace/source records.
4. Search a known phrase or tabular row and click through to exact supporting source text.
5. With a configured local model, request a summary; see only citations that resolve to imported evidence. Without a model, see clear unavailability with no fabricated answer.
6. Ask about missing facts; system abstains or flags no evidence.
7. Export a small saved work product with citations and source metadata.
8. Run CI/local tests, including invalid file path, private-source boundaries and hostile prompt in document; record pass/fail, not assumptions.

**Recommendation:** speed comes from excluding most planned phases from first release, not from bypassing licence, provenance, security or canonical ownership. Count reused functionality only after it works in Dotpol. Preserve all 13 phases as longer-term roadmap.
