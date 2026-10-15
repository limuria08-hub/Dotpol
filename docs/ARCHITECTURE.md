# Dotpol Architecture v1.0

**Status:** Consolidated planning baseline; implementation pending.

## 1. Architectural objective

Dotpol must provide a local-first political-intelligence platform that is free to build and can run in a valid ₹0 configuration, while preserving a clean path to collaborative/server deployments later.

The architecture therefore separates:

- application shells;
- a local gateway/API;
- reusable platform capabilities;
- political domain logic;
- deterministic analytical/statistical engines;
- AI agents/orchestration;
- connectors;
- storage/runtime adapters.

## 2. Top-level repository target

```text
Dotpol/
├── apps/
│   ├── web/
│   ├── field/
│   └── admin/
├── services/
│   ├── api/
│   └── workers/
├── platform/
│   ├── ai/
│   ├── search/
│   ├── data/
│   ├── provenance/
│   ├── analytics/
│   ├── gis/
│   ├── documents/
│   ├── surveys/
│   ├── automation/
│   └── auth/
├── domains/
│   ├── elections/
│   ├── constituencies/
│   ├── psephology/
│   ├── forecasting/
│   ├── simulation/
│   ├── policy/
│   ├── legislation/
│   ├── governance/
│   ├── manifestos/
│   ├── media/
│   ├── research/
│   ├── fieldops/        # proposed pre-election site/microarea operations
│   └── warroom/
├── agents/
├── connectors/
│   ├── india/
│   └── global/
├── packages/
│   ├── ui/
│   ├── domain/
│   ├── contracts/
│   └── sdk/
├── evaluations/
├── tests/
├── infra/
└── docs/
```

Create directories when their roadmap phase begins; do not scaffold empty architecture merely for appearance.

## 3. Runtime topology

### Personal/local mode

```text
Browser/Desktop Shell
       │
       ▼
Dotpol Web UI
       │
       ▼
Dotpol Local Gateway (FastAPI)
       │
       ├── Tool registry
       ├── Agent runtime
       ├── Plugin/connector registry
       ├── Workflow runtime
       ├── Search/RAG
       ├── Domain services
       └── Provenance
       │
       ├── SQLite        operational state
       ├── DuckDB        analytics
       ├── Parquet       datasets
       ├── Vector store  semantic retrieval
       └── Filesystem    documents/assets
```

No internet connection is required for purely local datasets/models/workflows.

### Team/server mode later

```text
Multiple clients
     │
Shared Dotpol Gateway
     │
PostgreSQL + shared storage + worker pool
```

Team mode must preserve the same logical contracts used in local mode.

## 4. Application layer

Applications render workflows and call platform/domain APIs. They must not own political engines.

### `apps/web`

Primary analyst/research terminal. Expected workspaces include chat, search, research, maps, analytics, elections, surveys, forecasts, policy, media, library and war room.

### `apps/field`

Field/mobile interface when required. Offline workflows should reuse established offline collection patterns/interoperability rather than creating a separate political backend.

### `apps/admin`

Local/team administration, data sources, models, plugins, permissions and diagnostics.

## 5. Local gateway

The local gateway is the control plane for a Dotpol installation.

Responsibilities:

- API contracts;
- session/workspace state;
- model routing;
- agent/tool invocation;
- connectors;
- workflows;
- capability registry;
- provenance;
- local runtime health;
- permissions in team mode.

The gateway must not become a monolithic god object. Capabilities remain modular behind typed interfaces.

## 6. Platform ownership

### AI

One model gateway. Domains and agents do not call providers directly.

### Search

Unified local/internal/web search interfaces. Provider-specific implementations remain adapters.

### Data

Source registry, ingestion contracts, validation, dataset/version metadata, storage adapters.

### Provenance

Cross-cutting result lineage and evidence graph.

### Analytics

DuckDB/Perspective/statistical-engine integration and reproducible analytical runs.

### GIS

Canonical geographic operations, boundaries, spatial indexes, map-layer contracts and rendering adapters.

### Documents

Document parsing/chunking/metadata/evidence extraction.

### Surveys

Shared questionnaire/response contracts and collection adapters; psephology remains domain logic.

### Automation

Durable workflows, schedules and event-triggered execution.

### Auth

Local identity/settings first; RBAC/team identity added without forcing hosted auth.

## 7. Domain layer

Domains contain political semantics and rules, not commodity infrastructure.

Examples:

- `domains/elections` owns election contests/results/swing/turnout domain operations;
- `domains/psephology` owns weighting, poll aggregation and survey-analysis workflows;
- `domains/forecasting` owns forecast specifications/runs/calibration/backtesting;
- `domains/policy` and `domains/legislation` own policy/legislative semantics;
- `domains/media` owns narrative/event intelligence semantics;
- `domains/fieldops` owns pre-election station facilities, microarea aggregate reporting, and verified authorized field workflows behind shared `Task`, `FieldUpdate` and survey contracts (per [ADR-0003](DECISIONS/0003-pre-election-microarea-operations.md));
- `domains/warroom` composes validated fieldops/election/GIS/survey intelligence, including appropriate polling-day source distinctions, without reimplementing field collection or underlying engines.

## 8. Agent layer

Agents are orchestrators over tools and domain/platform interfaces.

Agents must be thin relative to domain engines. Prompts should not encode deterministic business logic that belongs in code.

A typical path:

```text
User request
  -> Agent
  -> Tool contract
  -> Domain/platform engine
  -> Data
  -> Result + provenance
  -> Agent explanation/work product
```

## 9. Storage architecture

### SQLite

Use for local operational metadata such as workspaces, sessions, settings, registry metadata, tasks and lightweight canonical records where suitable.

### DuckDB

Use for analytical querying of election/survey/media/policy datasets and local columnar workflows.

### Parquet

Use as portable analytical dataset storage/interchange when appropriate.

### Embedded vector store

Use behind `VectorStore`-style Dotpol contracts. LanceDB is the current preferred candidate, not a hard-coded cross-project dependency.

### Filesystem

Documents, attachments, map assets, exports, caches and local work products.

### PostgreSQL

Reserved for shared/team mode or use cases that exceed embedded/local requirements. Do not require it for first-run personal mode.

## 10. AI architecture boundary

One Dotpol model interface supports:

- local Ollama-compatible models;
- MLX/llama.cpp paths where integrated;
- BYOAI APIs;
- optional OpenAI/Anthropic/Google/OpenRouter/etc. adapters.

No domain can import a provider SDK directly without going through the platform adapter.

## 11. GIS architecture

One GIS experience (ADR-0002):

```text
Canonical station/boundary + GIS layer contracts
        ↓
GeoPandas backend spatial calculations
        ↓
Kepler.gl embedded in the Dotpol web app
```

MapLibre/deck.gl remain Kepler's internal dependencies, **not separate Dotpol map applications**. Kepler never owns canonical geographic IDs or source versions. Local/offline basemap terms must be reviewed.

## 12. Analytics architecture

```text
Dataset
  ↓
DuckDB
  ↓
Domain/statistical engine
  ↓
Perspective views
  ↓
AI tool explanation
```

Statsmodels/PyMC provide mathematical machinery; domain modules define political model specifications.

## 13. Search/retrieval architecture

Start simple and measurable:

```text
Structured filters/search
 + full-text retrieval
 + semantic retrieval
 + reranking
 + entity/evidence relationships
 = Dotpol hybrid retrieval
```

Do not introduce multiple graph-RAG engines until evaluations show the need.

## 14. Plugin/connector architecture

Connectors/plugins must expose explicit manifests and capabilities.

Potential contribution types:

- data source;
- parser;
- search provider;
- model provider;
- tool;
- workflow;
- map layer;
- UI extension;
- export/work-product adapter.

External plugins must not bypass licence/security/provider controls.

## 15. Security architecture direction

- secrets remain local by default;
- API keys are never committed;
- connectors get least-privilege credentials;
- local services bind safely by default;
- shared/team mode introduces explicit auth/RBAC;
- imported files/data are treated as untrusted inputs;
- tool invocation needs permissions and auditability;
- plugin execution receives a security review before broad enablement.

## 16. Performance direction

Prefer embedded/vectorized/columnar local execution before introducing distributed infrastructure.

Scale-up path:

```text
embedded local -> stronger local machine -> shared server -> workers/distributed components
```

Do not start at the final scale.

## 17. Architecture change control

An ADR is mandatory before changing:

- local-first storage model;
- primary agent framework;
- AI gateway abstraction;
- core GIS stack;
- core analytics stack;
- workflow system;
- canonical domain ontology;
- provenance contract;
- donor/fork strategy with project-wide consequences.

See `docs/DECISIONS/README.md`.
