# Dotpol Architecture v1.0

**Status:** Five-phase consolidated planning baseline (2026-10-29); implementation pending. See [Roadmap](ROADMAP.md) and [ADR-0004](DECISIONS/0004-five-phase-execution-and-service-isolation.md).

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

**Python path detail (ADR-0001):** `platform/ai`, `platform/data` and other entries describe logical owners. Implement reusable Python code once under the importable package `platform/src/dotpol_platform/{ai,data,provenance,...}` and install it into the FastAPI service; never import from Python's standard-library name `platform` or create duplicate `dotpol_api/ai` implementations. [Phase 1 file plan](superpowers/plans/2026-10-15-dotpol-foundation.md) is now aligned.

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

## 17. Reusable OSS integration topology and hierarchical teams

**One-time integration contract, not all-at-once installation:** app and gateway expose typed DataConnector, AnalysisTool, AIProvider, FieldService, ArtifactProvider and AutomationProvider contracts. Donors are either embedded libraries, separately operated optional API services, narrowly adapted approved forks, or references. The selected stack (ADR-0002) remains the implementation baseline. There is no second canonical AI/GIS/search/task system.

**Personal/local:** Next.js frontend + FastAPI local gateway; SQLite for operational records; DuckDB for analytical computation; LanceDB for search index; filesystem for assets and backed-up files. No mandatory cloud, Kubernetes, external services or paid keys. Optional Ollama is user-managed. A no-model workflow must work honestly.

**Connected teams:** one shared gateway and PostgreSQL authoritative store behind stable storage contracts; clients may be mobile/offline. Only authorized records sync. Optional ODK Central provides independent field form intake, with ODK submission IDs mapped to Dotpol canonical FieldUpdate/Task/Evidence IDs. Optional real-time transport delivers events but does not own state. Use Compose for optional profiles. K3s only after a measurable deployment need.

**Recursive hierarchy:** one canonical Organization/Team tree with TeamMembership, delegated RoleGrant, ProjectAccess and resource-level visibility. Delegated permissions cannot exceed the issuer's privileges; revocation cascades according to explicit policies. All mutations are auditable. Support admin → supervisor → sub-team → staff. Geographic hierarchy and reporting hierarchy remain independent.

**Artifact continuum:** chat results, interactive map, statistical table, research report and saved library item share a canonical Project, SourceRef, EvidenceRef, Artifact and versioned ToolRun/AnalysisRun context. Chat previews open the exact corresponding workbench artifact, and edits persist both ways.

**Source truth and reporting:** historical official results, field observations and publicly published aggregate turnout are independently labelled with authority, timestamp and verification class. No invented official live booth-level feed. No individual inferred vote/preference tracking.

## 18. External full-service contracts (OpenCloud and OpenClaw)

**Do not merge entire donor applications into the Dotpol codebase.** Running a full open-source service with its own lifecycle is different from embedding a component.

| Service | Canonical ownership | Adapters and responsibilities | Security/failure behavior |
|---|---|---|---|
| **OpenCloud (P4 optional)** | OpenCloud owns file bytes, folders and sharing state. Dotpol owns political Project, SourceRef, EvidenceRef, Artifact and authorized business actions. | Explicit OIDC identity mapping and consented approved file APIs/WebDAV/Graph where supported; version/share scope/import audit. | Treat remote files as untrusted and verify rights on **each** access; deny stale/revoked grants, separate credentials; offline local research continues without OpenCloud. Its AGPL web UI is not copied. |
| **ODK Central (P2/P4 optional)** | ODK owns field form submissions; Dotpol owns Task, FieldUpdate, review and Incident semantics. | Map submission IDs/version/review state into existing canonical entities, idempotently. | Never create duplicate authoritative task/incident stores. Mobile retries must not duplicate records. |
| **OpenClaw (P5 optional)** | OpenClaw owns channel connections, pairing, device/skills sessions; Dotpol owns political model/tools/project permissions and decisions. | Scoped gateway adapter maps authenticated channel sender to Dotpol actor/scope; only approved deterministic/political tools are invoked through PydanticAI-owned policy. | Sandboxed tools and explicit enablement; disable unrestricted host filesystem/shell and untrusted skills. Gateway unavailable must not break local chat/research. Channel messages are untrusted, with disclosure and audit. |
| **Ollama (P1 optional)** | Model inference only. | One local provider adapter under `platform/ai`. | No auto model download, no model startup network access, unavailable-model state explicit. |

**Contract fields** for external calls: `actor_scope`, `project_id`, `service_id`, `tool_id`, `requested_action`, `consent`, `source/evidence ids`, `observed_at`, `received_at`, `remote_ref`, `idempotency_key`, `status`, `audit_id`. Only add fields required by the current workflow; no placeholder parallel domain store.

**Runtime rule:** local mode cannot require OpenCloud/OpenClaw/ODK/paid AI, browser login or Kubernetes. Compose is permitted for opt-in service profiles; K3s only if later needed. Validate platform, network/security and exact licence/model/assets before adopting each service. Preserve the local FastAPI/PydanticAI/SQLite/AI architecture.

## 19. Architecture change control

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
