# Dotpol Roadmap v1.0

This roadmap is dependency-ordered. Later phases should not bypass missing foundations simply to create visible features.

## Phase 0 — Blueprint and architecture freeze

**Goal:** establish a stable development constitution before product code.

Deliverables:

- master blueprint;
- architecture boundaries;
- canonical political domain model;
- local-first data architecture;
- AI architecture;
- capability ownership registry;
- donor/reuse matrix;
- licence policy;
- ADR process;
- collaborator/agent instructions;
- implementation plan for Phase 1.

**Exit gate:** collaborators can answer where a new capability belongs, which owner implements it, what data contracts it uses, whether OSS is reused, and what architectural changes require ADRs.

## Phase 1 — Local platform foundation

**Goal:** create the minimal runnable Dotpol spine.

Deliverables:

- web app shell;
- local FastAPI gateway;
- local project/workspace lifecycle;
- SQLite operational storage adapter;
- filesystem workspace layout;
- source registry skeleton;
- provenance/event/run identifiers;
- single model gateway;
- local model adapter path;
- BYOAI provider contract;
- PydanticAI agent runtime skeleton;
- tool registry;
- local configuration/secrets strategy;
- health/diagnostics endpoint;
- baseline tests and CI.

**Do not add:** election models, Kepler, PyMC, policy trackers, war room, multiple RAG frameworks.

**Exit gate:** user can launch Dotpol locally, create/open a project, configure a local or optional external model, invoke a simple evidence-aware tool through the gateway, and close/reopen without data loss.

## Phase 2 — Political data fabric and ontology

**Goal:** create trustworthy ingestion, document and canonical political entity foundations.

Deliverables:

- dlt-backed connector contract;
- source/dataset registries;
- schema validation;
- import for CSV/JSON/Parquet and common local files;
- Docling document pipeline;
- canonical entity identifiers;
- geography/jurisdiction primitives;
- source/versioned polling-station directory and proposed privacy-safe Microarea boundaries for subsequent pre-election site reporting;
- political actors/election/policy/media base entities;
- provenance links from source records to canonical entities;
- initial official/public-source connector pilots;
- OPOL donor evaluation and selective assimilation report.

**Exit gate:** imported source data can be transformed into versioned canonical entities/datasets with reproducible lineage.

## Phase 3 — Search, research and retrieval

**Goal:** make local/user/public information searchable and researchable with evidence.

Deliverables:

- structured search;
- full-text search;
- embedded semantic retrieval adapter;
- hybrid ranking/reranking;
- Vane donor evaluation/assimilation;
- optional web search provider abstraction;
- citations/evidence spans;
- research projects/library;
- Research Agent;
- evidence-backed brief/work-product prototype;
- retrieval evaluation suite;
- benchmark of LightRAG/GraphRAG only if needed.

**Exit gate:** user can ask a research question over local documents/datasets and receive a source-linked answer; web search is optional, not mandatory.

## Phase 4 — GIS and analytical terminal

**Goal:** provide professional map and analytical workbenches.

Deliverables:

- canonical boundary/geometry contracts;
- MapLibre integration;
- deck.gl layers;
- H3 spatial indexing;
- map-layer registry;
- DuckDB analytical datasets/views;
- FINOS Perspective workbench;
- shared chart layer;
- Statsmodels integration;
- reproducible analytical runs;
- GIS Agent and Statistics Agent tools;
- Kepler Map Lab donor evaluation/assimilation;
- canonical station/microarea public-site layers, with site and boundary versions (no private household/voter-level political maps).

**Exit gate:** same canonical dataset can be filtered/pivoted/charted/mapped without duplicating its domain representation.

## Phase 5 — Election and constituency intelligence

**Goal:** make elections a first-class Dotpol domain.

Deliverables:

- election/contest/candidacy/result contracts;
- historical election import adapters;
- constituency workspace;
- margins, vote share, turnout and swing engines;
- election comparison workflows;
- geographic election layers;
- polling-station reference IDs reused by approved public aggregate election analyses and the proposed pre-election field preparedness workspace;
- constituency briefs;
- Election Agent;
- deterministic tests for election calculations;
- data-quality checks for election totals/identifiers.

**Exit gate:** election metrics are reproducible, mapped, source-linked and callable as tools by AI.

## Phase 6 — Surveys and psephology

**Goal:** provide end-to-end survey analysis without rebuilding proven offline collection infrastructure.

Deliverables:

- Dotpol Survey Studio schema/editor MVP;
- SurveyJS form runtime where appropriate;
- ODK interoperability/export/import pilot;
- sample definitions;
- weighting specifications/runs;
- cross-tabs;
- margins/uncertainty diagnostics;
- poll estimates and aggregation;
- survey quality checks;
- Survey/Psephology Agent.

**Exit gate:** a survey can be defined, collected/imported, weighted and analysed reproducibly with methodology/provenance attached.

### Pre-election field operations — Phase 6 proposed addition

`domains/fieldops` reuses station geography, `Task`, `FieldUpdate`, SurveyJS/ODK collection and evidence contracts. Scope: authorized station assessments, offline idempotent submissions, human review and verified aggregate issue maps. Phase 10 consumes the same operations records; no second booth CRM or individual political preference profiling.

**Exit:** pass F1–F5 in the [field specification](PRE_ELECTION_MICROAREA_INTELLIGENCE.md) with permitted/synthetic data. See [Master Plan](MASTER_PLAN.md).

## Phase 7 — Forecasting, simulation and aggregate digital twin

**Goal:** turn historical/survey data into calibrated probabilistic scenarios.

Deliverables:

- model definition/registry;
- forecast run contract;
- PyMC integration where suitable;
- Monte Carlo engine;
- turnout/swing scenario engine;
- vote/seat forecasts;
- uncertainty intervals;
- calibration/backtesting;
- scenario comparison;
- aggregate/geographic digital-twin primitives;
- Forecast and Scenario Agents.

**Exit gate:** every forecast is tied to a model version, data version, parameters, uncertainty and backtest/calibration metadata.

## Phase 8 — Policy, legislation, governance and manifestos

**Goal:** connect political competition to policy/governance intelligence.

Deliverables:

- bills/amendments/debates/questions/votes;
- policy/scheme/program entities;
- manifesto/promise entities;
- official-source India connector pilots;
- policy/legislation search/workspaces;
- promise-status evidence assertions;
- timelines and actor/issue relationships;
- Policy and Legislative Agents;
- policy research work products.

**Exit gate:** users can trace a public promise/issue through documents, legislative/policy activity and evidence-backed status assertions where data allows.

## Phase 9 — Media, event and narrative intelligence

**Goal:** create evidence-backed narrative/event monitoring.

Deliverables:

- news/RSS/public-source connectors;
- MediaItem/Event/Issue pipeline;
- entity mentions;
- topic clustering;
- narrative clustering/versioning;
- source comparison;
- stance/sentiment observations with method provenance;
- event timelines;
- Media Agent;
- monitoring evaluation.

**Exit gate:** narrative/issue outputs link back to concrete source items and method/model versions.

## Phase 10 — Field operations and war room

**Goal:** compose existing intelligence into operational monitoring and coordination.

Deliverables:

- field tasks/updates/incidents, consuming **the same `domains/fieldops` records and site IDs** established in the pre-election field pilot;
- offline collection/sync interoperability with idempotent receipts, clock/source time, dispute review and role permissions;
- aggregate turnout and operational monitoring, distinguishing official approximate VTR, statutory Form 17C when legally available, and non-official field observations;
- maps and escalation workflows;
- controller/war-room workspace;
- alert acknowledgement/state;
- War Room Agent;
- after-action/post-election learning.

**Rule:** war room consumes shared fieldops/election/GIS/survey/media engines; it does not rebuild them. No individual political-preference/voter tracking or voter-level persuasion functionality.

**Exit gate:** live operational information can be combined with existing intelligence while preserving source/time/verification states, with station incidents, discrepancy review, safe aggregated reporting and access-controlled alerts tested end-to-end. See [pre-election handoff requirements](PRE_ELECTION_MICROAREA_INTELLIGENCE.md).

## Phase 11 — Automation, plugins and open platform

**Goal:** make Dotpol extensible and proactive.

Deliverables:

- Prefect-backed durable workflows where needed;
- schedules/triggers;
- monitoring agents;
- plugin manifests;
- connector SDK;
- tool/plugin permissions;
- optional MCP integration;
- alert/delivery adapters;
- external API/SDK stabilization.

**Exit gate:** a contributor can add an approved connector/tool without editing unrelated core modules.

## Phase 12 — Hardening and release engineering

**Goal:** make Dotpol reliable for broad OSS use.

Deliverables:

- cross-platform install/packaging;
- one-command/local onboarding target;
- Windows/macOS/Linux CI;
- migration/version strategy;
- performance benchmarks;
- security review;
- SBOM/dependency inventory;
- automated licence checks;
- backup/export/import;
- reproducibility tests;
- documentation site/user guides;
- accessibility review;
- release process.

## Cross-phase gates

Every phase must preserve:

- local-first operation;
- zero-cost-core path;
- one capability/owner;
- canonical domain model;
- deterministic calculations;
- provenance;
- component-level licence review;
- tests/evaluations;
- documented architecture changes through ADRs.

## Parallel work rule

Parallel tasks are encouraged only when they do not create competing implementations or require unstable interfaces from unfinished prerequisite phases.

A visible UI is not considered progress if it bypasses the canonical data/model/tool architecture.
