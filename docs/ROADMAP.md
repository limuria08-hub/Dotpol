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
- Kepler Map Lab donor evaluation/assimilation.

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

- field tasks/updates/incidents;
- offline collection/sync interoperability;
- aggregate turnout and operational monitoring;
- maps and escalation workflows;
- controller/war-room workspace;
- alert acknowledgement/state;
- War Room Agent;
- after-action/post-election learning.

**Rule:** war room consumes shared election/GIS/survey/media engines; it does not rebuild them.

**Exit gate:** live operational information can be combined with existing intelligence while preserving source/time/verification states.

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

## Phase quality-gate addendum (proposed for Phase 0 review, 2026-10-15)

This addendum **does not renumber, reorder, or mark complete** any phase. It defines evidence needed to keep the existing dependency order from becoming duplicate implementation work. See [planning audit](PLAN_AUDIT_2026-10-15.md), [MVP acceptance plan](PRODUCT_MVP_AND_ACCEPTANCE.md), [data governance](DATA_GOVERNANCE.md) and [security/AI assurance](SECURITY_AND_AI_ASSURANCE.md).

### Phase 0 (before implementation)

- [ ] Identify owner and reviewer for every Phase 1 capability and its API/data contract; resolve [proposed ADR-0001](DECISIONS/0001-foundation-module-ownership.md) before generating conflicting Python package paths.
- [ ] Approve or revise initial MVP persona and user journeys J1–J4; explicitly distinguish Phase 1 foundation from usable end-to-end research MVP.
- [ ] Approve project licence and decide root LICENSE/third-party attribution approach; keep all proposed donor licences unverified until checked at exact version/component.
- [ ] Approve data-classification/intake policy, local gateway threat model, agent permission classes and CI security expectations.
- [ ] Assign an accountable reviewer for architecture, AI evaluation, data/privacy, security/licensing, UX and release acceptance; agree what test reports and demos count as evidence.
- [ ] Ensure the Phase 1 task plan is compatible with approved owners, schemas and no-network/zero-cost assumptions.

### Cross-phase planning gates (apply at entry, review, exit)

1. **Capability owner:** one registered owner and import path; no competing model gateway, vector store, engine, data registry or parser.
2. **Contracts:** typed schemas, canonical identifiers, units, temporal and geographic references, errors, source/evidence links; backward-compatibility and migration strategy.
3. **Security:** classify exposed data and tool effects, review trust boundaries, include negative tests and restricted defaults. Local first does not mean unsecured localhost.
4. **AI:** source-linked and no-evidence behavior evaluated; deterministic reference engine owns calculations; approval required for external/destructive side effects.
5. **Reproducibility:** version data, model, transform, tool and boundary, with documented methodology and input/outputs; output states observed/derived/forecast/inferred.
6. **OSS/legal:** pin and verify donor version/component and terms; observe map tile, data, model-weight and form-editor licences.
7. **User value:** demonstrate phase-specific journey with real/synthetic clearly labeled fixtures; accessible and understandable errors/uncertainty.
8. **Verification:** link passing tests/CI, local/no-key launch when applicable, evidence for unfinished cases. Mark 'specified', 'approved', 'implemented', 'verified', 'released' separately.

### Specific additional exit checks

- **Phase 1:** loopback/local API protection and path-validation tests; missing-model/startup behavior; source IDs cannot be invented; workspace reopens after restart; baseline public PR CI runs unprivileged.
- **Phase 2:** source/licence/personal-data classification, canonical identity merge/conflict fixtures, imported raw→staging→canonical lineage and schema-version validation.
- **Phase 3:** source span/row citation fidelity; explicit no-evidence abstention; privacy-filtered local retrieval and document prompt-injection tests.
- **Phase 4–5:** boundary-version comparability warnings; shared dataset drives table/chart/map; reference tests for margins, turnout, swing and missing results.
- **Phase 6–7:** documented sampling/weighting/quality, publication suppression, model calibration/backtests and provenance-linked uncertainty.
- **Phase 8–9:** time/version-sensitive legislative and media claims; contradictory sources and observed-versus-inferred labels.
- **Phase 10–11:** auditable field event/alert state; delegated tool approvals, least privilege, secure sync/plugin boundaries and no default unsanctioned publishing.
- **Phase 12:** practical installer, restore, export/erase where lawful, dependency SBOM/licence notices, tested recovery and supported-OS matrix.

**Non-goal:** do not turn this into a mandate to add all planned packages before their phase. Security, licence and privacy review begins early; heavyweight mechanisms are introduced when required.
