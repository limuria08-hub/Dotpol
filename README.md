# Dotpol

**Dotpol is an open-source, AI-native political intelligence operating system.**

Its goal is to bring research, elections, psephology, GIS, surveys, forecasting, public policy, legislative intelligence, media/narrative analysis, field operations, and war-room workflows into one local-first intelligence platform.

## Phase 1 implementation (AI-native research foundation)

An initial Next.js + FastAPI + SQLite political research workspace and PydanticAI model gateway are under implementation and **must be independently validated before being called complete**. Local source imports, exact citations and saved artifacts work in non-model mode; configured local Ollama or explicit BYOAI activates cited synthesis. Read [local run guide](PHASE1_RUN.md) and [AI-native capability contract](docs/AI_NATIVE_CAPABILITY_CONTRACT.md). Other domain agents remain phased plans, not implemented endpoints.

## Start here

**[Dotpol Master Plan](docs/MASTER_PLAN.md)** — the single concise product and delivery plan. It now defines **five execution phases**, preserving former milestones 0–12 as detailed acceptance work packages; it also covers the selected stack, research, political data, pre-election field intelligence, nested teams, election-day operations and release gates. Detailed specifications below are supporting reference, not competing plans.

## Project status

**Five-phase planning baseline accepted for documentation — implementation not verified.**

Dotpol has a consolidated [master plan](docs/MASTER_PLAN.md) and selected stack; implementation and verification remain ahead. The repository should not accumulate duplicate implementations, competing frameworks, or frequently changing architectural choices.

Major architecture changes require an Architecture Decision Record (ADR) under `docs/DECISIONS/`.

## Core principles

1. **Free to build.** Core development must use free/open-source tooling and public-repository CI wherever practical.
2. **Local-first.** A valid Dotpol installation must run on a user's own machine without mandatory cloud infrastructure.
3. **₹0 core operating mode.** Core functionality must not require a paid SaaS product, paid database, paid map provider, paid search provider, or paid AI API.
4. **BYOAI + local AI.** Local models are first-class; commercial models are optional user-configured providers.
5. **Reuse before build.** Search for suitable permissive open-source capabilities before writing commodity infrastructure.
6. **Fork only when modification is substantial.** Prefer dependencies or adapters when upstream software already does the job.
7. **One capability, one owner.** Shared capabilities such as GIS, search, AI routing, analytics, documents, and provenance are implemented once and reused by every domain.
8. **One canonical political domain model.** A constituency, party, election, bill, survey, or policy has one canonical representation across the platform.
9. **AI reasons; engines calculate.** Deterministic results must come from tools/models/data engines, not model improvisation.
10. **Provenance from day one.** Important claims, charts, statistics, forecasts, and generated work products must be traceable to evidence, transforms, and models.
11. **Open architecture.** No mandatory Vercel, Supabase, AWS, Mapbox, Pinecone, OpenAI, Anthropic, or similar hosted dependency.
12. **Change by evidence, not novelty.** Do not replace architecture because a new repository or framework looks interesting.

## Local-first target architecture

```text
Dotpol UI
   │
   ▼
Dotpol Local Gateway / API
   │
   ├── AI + Agents
   ├── Search + Research
   ├── Political Data Fabric
   ├── Documents
   ├── GIS
   ├── Analytics + Statistics
   ├── Surveys
   ├── Forecasting + Simulation
   ├── Policy + Legislative Intelligence
   ├── Media + Narrative Intelligence
   ├── Field Operations
   ├── Automation
   └── Provenance

Local storage by default:
SQLite + DuckDB + Parquet + local vector store + filesystem

Optional team/server mode later:
PostgreSQL + shared object storage + central gateway
```

## Five-phase delivery

| Execution phase | Scope |
|---|---|
| **P1** | Foundation, AI, evidence-backed research and canonical data |
| **P2** | Election intelligence, GIS, statistics, psephology and field pilot |
| **P3** | Advanced simulation, policy, legislation, governance and media |
| **P4** | Recursive teams, mobile collaboration and live command centre |
| **P5** | Automations, optional OSS services, quality, security and release |

The three-day sprint targets a **vertical research-and-analytics demo**, not a completed five-phase product. Preserve the existing selected stack and the no-duplication rules. Read [ROADMAP](docs/ROADMAP.md) and [ADR-0004](docs/DECISIONS/0004-five-phase-execution-and-service-isolation.md).

## Documentation map

Start here:

- [`docs/BLUEPRINT.md`](docs/BLUEPRINT.md) — master product and engineering blueprint.
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — system boundaries and technical architecture.
- [`docs/DOMAIN_MODEL.md`](docs/DOMAIN_MODEL.md) — canonical political concepts and entity rules.
- [`docs/DATA_ARCHITECTURE.md`](docs/DATA_ARCHITECTURE.md) — local storage, ingestion, data contracts, lineage and provenance.
- [`docs/AI_ARCHITECTURE.md`](docs/AI_ARCHITECTURE.md) — models, agents, tools and deterministic-engine rules.
- [`docs/CAPABILITY_REGISTRY.md`](docs/CAPABILITY_REGISTRY.md) — capability ownership and anti-duplication map.
- [`docs/DONOR_MATRIX.md`](docs/DONOR_MATRIX.md) — fork/dependency/reference/build decisions for open-source donors.
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — phased delivery order and gates.
- [`docs/LICENSE_POLICY.md`](docs/LICENSE_POLICY.md) — OSS and zero-cost-core dependency policy.
- [`AGENTS.md`](AGENTS.md) — mandatory instructions for coding agents and contributors.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — collaborator workflow.

Machine-readable architecture controls:

- `architecture/capabilities.yml`
- `architecture/donors.lock.yml`

## Product scope

Dotpol is broader than an election app or voter CRM. Its long-term scope includes:

- political generative search and deep research;
- election history and constituency intelligence;
- survey research and psephology;
- statistical and analytical workbench;
- GIS and auto-mapping;
- forecasting and scenario simulation;
- political digital twins at aggregate/geographic levels;
- policy, legislation, regulation and governance intelligence;
- manifesto and promise tracking;
- media, news, issue and narrative intelligence;
- field and election-day operations;
- war-room monitoring and coordination;
- autonomous/scheduled political-intelligence workflows;
- reports, briefs, dashboards and evidence-backed work products;
- plugins, connectors and APIs.

## Reuse strategy

Dotpol should assimilate proven open-source capabilities rather than rebuild commodity infrastructure. Current donor candidates include projects in political data, generative search, GIS, analytical workbenches, documents, surveys, local AI, ingestion, workflow orchestration and statistical computing. See [`docs/DONOR_MATRIX.md`](docs/DONOR_MATRIX.md).

A donor is not adopted merely because the parent repository has a permissive licence. **Every embedded component and transitive dependency must pass component-level licence and architecture review before integration.**

## Development rule

Before implementing a capability:

```text
Requirement
   ↓
Check capability registry
   ↓
Already exists? ── yes ──► extend existing owner
   │
   no
   ↓
Search existing OSS
   ↓
Suitable permissive donor? ── yes ──► reuse/adapt/integrate
   │
   no
   ↓
Build the smallest Dotpol-owned implementation
   ↓
Tests + provenance + documentation
```

## Current phase

**P1: Foundation and architecture consolidation (implementation requires actual tests).**

Before major implementation, approve any remaining architecture/licence gates, verify contracts and create small independently tested integration PRs. Historic milestone numbers elsewhere in specs refer to work packages mapped in ROADMAP.md, not additional phases.

---

Dotpol is intended to make sophisticated political intelligence substantially more accessible by combining open-source infrastructure with an original political domain model, analytical engines, AI agents and evidence-backed workflows.
