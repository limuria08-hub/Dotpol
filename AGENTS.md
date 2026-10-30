# Dotpol Agent Instructions

**Start with [Master Plan](docs/MASTER_PLAN.md) and [Five-phase Roadmap](docs/ROADMAP.md).** There are exactly FIVE execution phases P1–P5; historic milestone labels 0–12 are supporting acceptance work packages only. For field work read [Field Specification](docs/PRE_ELECTION_MICROAREA_INTELLIGENCE.md) and accepted planning [ADR-0003](docs/DECISIONS/0003-pre-election-microarea-operations.md). P2 establishes field records; P4 consumes those same records. Planning is not verified implementation.

These instructions are mandatory for AI coding agents, automation workers, and human collaborators working in this repository.

## 1. Read before changing code

Before implementing anything, read:

1. `README.md`
2. `docs/BLUEPRINT.md`
3. `docs/ARCHITECTURE.md`
4. `docs/DOMAIN_MODEL.md`
5. `docs/DATA_ARCHITECTURE.md`
6. `docs/AI_ARCHITECTURE.md`
7. `docs/CAPABILITY_REGISTRY.md`
8. `docs/DONOR_MATRIX.md`
9. `docs/ROADMAP.md` (five-phase checklist and legacy milestone map)
10. `docs/LICENSE_POLICY.md`
11. `architecture/capabilities.yml`
12. `architecture/donors.lock.yml`
13. `docs/DECISIONS/0004-five-phase-execution-and-service-isolation.md`

If a requested change conflicts with these documents, do not silently invent a new architecture. Create or propose an ADR under `docs/DECISIONS/`.

## Open-source UI reuse contract

- Before editing the Next.js shell, consult [OSS UI Adoption Plan](docs/OSS_UI_ADOPTION_PLAN.md). Use existing permissively licensed components for navigation, panels, forms and AI-thread presentation; **do not** copy complete competing products.
- **Agent E (`apps/web`) is the sole owner of the shared UI shell and design tokens.** Agent B exposes the existing FastAPI/PydanticAI stream/REST contracts, never a parallel frontend AI server.
- UI baseline: shadcn/ui + Radix-flavor accessible components + Lucide; react-resizable-panels for chat/workbench; evaluate assistant-ui custom adapter over current API. Vane is a source/citation UX donor only, not a second chat renderer. Validate versions/licences and React/Next compatibility first.
- Later specialty UI: Perspective for tables, Kepler for GIS, SurveyJS Form Library for surveys; Lexical and React Flow only after justified integration spikes. One component owner per job.
- UI is a view over canonical Project/Artifact/Source/RoleGrant IDs. A chat artifact and full workbench must be *the same persisted object*; no visual-only mock data or parallel stores.
- Ship accessibility/mobile/keyboard and local/no-cloud tests; preserve remote AI consent and no-model behavior while replacing handcrafted UI.

## Five-phase execution contract

- **P1** foundation + evidence-backed research; **P2** elections/GIS/statistics/psephology/field pilot; **P3** policy/media/simulation; **P4** recursive teams/mobile/war room; **P5** automations, optional services and release.
- The first three days are a *bounded demo target*; they do NOT certify five-phase completion. Mark items complete only after tests and integrated user journeys.
- Every PR must state execution phase P1–P5, former milestone if relevant, canonical owner, interfaces, donor classification, licence evidence, tests and user-visible acceptance.
- Build only what a current phase consumes. Register future donor candidates without installing/forking them prematurely.
- Embedded libraries (Kepler, DuckDB, Perspective, GeoPandas, Statsmodels) belong behind ONE Dotpol owner; Ollama, ODK Central, optional notifications/civic systems may be separately run and accessed via typed APIs.
- Docker Compose is the default optional service orchestration path. Do not require Kubernetes or an always-on cloud for personal/local mode. K3s remains a future option.
- P4 recursive teams: parent-child organization records, delegated membership and roles, scoping by project/team and specific resources, revocation, auditable escalation. A parent's membership must not automatically grant access to all confidential child records.
- Mobile updates and notifications never replace the authoritative Task/FieldUpdate/Incident store; submissions use unique IDs, observed and received timestamps, permissions and conflict-safe idempotent sync.
- Agent recommendations must be evidence- and aggregate-grounded; no inferred individual voter political preferences or targeted political persuasion.

## 2. Project constitution

### Local-first

Core Dotpol must run without mandatory cloud services. A local-only installation must remain a supported architecture.

### Zero-cost core

Core functionality must not require paid SaaS, paid databases, paid map platforms, paid vector databases, paid search APIs, or paid LLM APIs.

Optional commercial providers may be supported only through replaceable provider interfaces.

### Reuse before build

Before writing a new subsystem:

1. Search the capability registry.
2. Search existing Dotpol code.
3. Check approved donors/dependencies.
4. Evaluate relevant permissive OSS.
5. Extend or integrate where possible.
6. Build new infrastructure only when no acceptable solution exists.

### One capability, one owner

Do not create duplicate search engines, GIS engines, AI gateways, document parsers, analytics engines, workflow engines, or provenance systems inside domain modules.

Shared capabilities belong to `platform/` and are reused by domains.

### One concept, one canonical entity

Do not create parallel domain representations such as `SurveyConstituency`, `ElectionConstituency`, and `GISConstituency` unless they are explicit view/read models over the canonical `Constituency` entity.

### AI does not invent deterministic results

Agents orchestrate tools. Engines calculate.

For calculations, forecasts, statistics, geospatial transforms, election math, survey weighting, or deterministic state:

```text
Agent -> Tool -> Engine -> Data -> Result -> Provenance -> Explanation
```

Never substitute an LLM estimate for an available deterministic calculation.

### Provenance is mandatory

Important outputs must preserve source IDs, data versions, transformations, model/tool versions, timestamps and uncertainty/confidence when relevant.

## 3. Architecture boundaries

Expected top-level ownership:

- `apps/` — user-facing applications only.
- `platform/` — reusable technical capabilities.
- `domains/` — political domain logic.
- `agents/` — agent definitions and orchestration over tools.
- `connectors/` — external data/source adapters.
- `packages/` — shared packages/contracts/UI.
- `evaluations/` — AI and model evaluation suites.
- `tests/` — deterministic and integration tests.
- `infra/` — packaging/deployment/runtime configuration.
- `docs/` — architecture/specification/decisions.

An application must not own core domain logic.
A domain must not directly integrate model providers.
A domain must not create its own persistence technology when a platform storage contract exists.
An agent must not become a second implementation of a domain engine.

## 4. Locked v1 technology direction

These are architectural defaults, not permission to install everything immediately.

- Frontend: React + Next.js + shadcn/ui-style component system.
- Backend/local gateway: Python + FastAPI.
- Local operational state: SQLite.
- Local analytics: DuckDB.
- Dataset interchange: Parquet/CSV/JSON plus typed contracts.
- Local document/file storage: filesystem.
- Local retrieval: LanceDB OSS for full-text/vector hybrid through one Dotpol-owned search interface.
- Team/server mode later: PostgreSQL and shared storage behind the same contracts.
- AI model access: local models + BYOAI through one Dotpol model gateway.
- Agent framework v1: PydanticAI unless an ADR changes it.
- Workflow orchestration: Prefect when durable workflows are required.
- GIS: **one Kepler.gl map interface** with its internal renderers; GeoPandas handles backend geometry, one canonical GIS owner.
- Analytics UI: FINOS Perspective.
- Statistics: Statsmodels; Bayesian modelling: PyMC.
- Documents: Docling.
- Ingestion: dlt.
- Surveys: Dotpol-owned Survey Studio, SurveyJS Form Library where appropriate, ODK interoperability for robust field/offline collection.

Do not add competing frameworks without an ADR.

## 5. Donor rules

Donors are classified as:

- **fork** — expected substantial modification;
- **dependency** — use upstream through stable interfaces;
- **reference** — study patterns only;
- **Dotpol-owned** — original domain/IP capability.

Never copy code from a donor before checking `docs/DONOR_MATRIX.md`, `architecture/donors.lock.yml`, the donor's exact licence, and any relevant subcomponent licences.

Do not assume a permissive parent repository makes every bundled service permissive.

When assimilating donor code:

1. Record source repository and commit/tag.
2. Record licence.
3. Record files/modules assimilated.
4. Preserve required notices/attribution.
5. Wrap the capability in a Dotpol-owned interface.
6. Add tests proving the interface.
7. Avoid leaking donor-specific assumptions across the rest of Dotpol.

## 6. Change control

Major architectural changes require an ADR when they affect any of:

- primary database/storage strategy;
- agent framework;
- model gateway;
- frontend application architecture;
- GIS engine;
- analytics engine;
- workflow engine;
- canonical domain model;
- provenance model;
- donor classification;
- licensing policy;
- local-first or zero-cost-core guarantees.

An ADR must state context, decision, alternatives, consequences and migration impact.

## 7. Implementation workflow

For each capability:

1. Identify the owning module.
2. Define typed inputs/outputs/contracts.
3. Define deterministic tests first for core logic.
4. Implement the smallest useful slice.
5. Add provenance hooks where the capability consumes evidence/data.
6. Add evaluation cases for AI behavior.
7. Document the capability registry entry.
8. Update donor records if OSS was assimilated.
9. Verify local-only operation where relevant.
10. Commit a coherent, reviewable change.

## 8. Prohibited patterns

Do not:

- call OpenAI/Anthropic/Gemini directly from domain modules;
- require a paid cloud service for a core path;
- add a second agent framework experimentally to production code;
- maintain two canonical databases for the same local state;
- add duplicate election/survey/GIS representations;
- calculate statistics in prompts when a deterministic engine exists;
- hard-code one search provider;
- hard-code one AI provider;
- hard-code one map tile provider;
- silently introduce copyleft/source-available code into permissive core;
- rewrite working infrastructure merely because a new framework appears;
- implement a roadmap phase before its required foundation/data contracts exist.

## 9. Product boundary

Dotpol is a broad political-intelligence platform. Individual modules are not separate products inside the codebase.

Individual-level political persuasion or inferred-vote targeting is not a design objective for the AI decision layer. Forecasting and political intelligence should focus on lawful aggregate, geographic, cohort, survey, policy, media, research and operational intelligence.

## 10. Definition of done

A capability is not done merely because its UI works. It is done when:

- ownership is clear;
- contracts are stable enough for the phase;
- deterministic tests pass;
- AI evaluation exists where applicable;
- provenance is preserved;
- licence obligations are recorded;
- local-first behavior works;
- documentation is updated;
- no duplicate implementation was introduced.
