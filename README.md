# Dotpol

**Dotpol is an open-source, AI-native political intelligence operating system.**

Its goal is to bring research, elections, psephology, GIS, surveys, forecasting, public policy, legislative intelligence, media/narrative analysis, field operations, and war-room workflows into one local-first intelligence platform.

## Proposed pre-election field / booth intelligence workstream

The [Pre-Election Microarea Intelligence and Booth Operations specification](docs/PRE_ELECTION_MICROAREA_INTELLIGENCE.md) and [ADR-0003](docs/DECISIONS/0003-pre-election-microarea-operations.md) propose a single fieldops owner for **polling-site geography, facility readiness, lawful aggregate public issues, authorized field assignments, offline reports and verification**, reused by the existing election-day war room. This is a **Phase 0 proposal**, not implemented or approved individual political-voter profiling. The existing user-level political targeting boundary remains unchanged.

## Project status

**Blueprint v1.0 — architecture freeze before implementation.**

Dotpol is intentionally beginning with documentation and architecture before feature development. The repository should not accumulate duplicate implementations, competing frameworks, or frequently changing architectural choices.

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

**Phase 0: Blueprint and architecture freeze.**

No major feature implementation should begin until the blueprint documents, capability ownership, donor decisions, data contracts and architecture rules have been reviewed by collaborators.

---

Dotpol is intended to make sophisticated political intelligence substantially more accessible by combining open-source infrastructure with an original political domain model, analytical engines, AI agents and evidence-backed workflows.
