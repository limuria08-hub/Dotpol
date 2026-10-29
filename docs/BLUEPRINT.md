# Dotpol Blueprint v1.0

**Status:** Consolidated planning baseline — implementation, licences and component pins pending  
**Purpose:** Product scope and engineering constitution; **the five-phase execution schedule is in [MASTER_PLAN](MASTER_PLAN.md) / [ROADMAP](ROADMAP.md)**. Historical phases 0–12 mentioned here are detailed milestones mapped to P1–P5, not additional execution phases.  
**Change policy:** Major changes require an ADR under `docs/DECISIONS/`.

## Five-phase implementation structure (2026-10-29)

P1 foundation/research (former 0–3); P2 election/GIS/statistics/surveys + field pilot (4–6); P3 simulation/policy/media (7–9); P4 nested teams/command centre (10 and continuation of 6); P5 automations/release (11–12). Scope below remains intact. No donor is installed or licence-approved just because it is listed. See [ADR-0004](DECISIONS/0004-five-phase-execution-and-service-isolation.md).

## 1. Mission

Dotpol is an open-source, AI-native political intelligence operating system designed to make advanced political research, analysis and operational intelligence accessible without requiring an expensive proprietary consulting/technology stack.

Dotpol should combine the capabilities usually fragmented across research platforms, psephology teams, GIS tools, survey systems, policy/legislative trackers, media-monitoring products, election analysis software and war-room workflows.

The product should remain local-first and have a valid ₹0 operating configuration.

## 2. Product thesis

Political intelligence is currently fragmented across many tools and specialist teams. Dotpol should provide one coherent intelligence layer where users can:

- discover information;
- connect and ingest data;
- research deeply with citations;
- explore political entities and relationships;
- map political and socio-economic geography;
- analyse elections and surveys;
- run statistical models;
- forecast and simulate scenarios;
- monitor legislation, policy, governance and manifestos;
- understand media, narratives and issues;
- coordinate field and war-room operations;
- automate monitoring and briefing workflows;
- produce evidence-backed reports and work products.

Chat is one interface, not the product architecture. Search, maps, analytical tables, timelines, networks, dashboards, work products, alerts, automations and domain workspaces are equally important interaction surfaces.

## 3. Product scope

### 3.1 Intelligence workspace

- conversational political copilot;
- generative search;
- deep research;
- projects/workspaces;
- library and source collections;
- saved research/work products;
- citations and provenance;
- watchlists and monitors;
- reusable analytical views.

### 3.2 Election intelligence

- election history;
- constituencies and boundaries;
- candidates/parties/alliances;
- vote share, margin and turnout;
- swing analysis;
- geographic election analysis;
- booth/ward/constituency aggregate analytics;
- comparative elections;
- opponent/party performance analysis;
- election briefs;
- election agents/tools.

### 3.3 Surveys and psephology

- survey/questionnaire authoring;
- sampling plans;
- enumerator/field workflows;
- web and offline collection interoperability;
- weighting;
- cross-tabs;
- response-quality diagnostics;
- margins of error/uncertainty;
- poll aggregation;
- longitudinal polling;
- geographic estimates;
- psephology workbench;
- survey/psephology agent.

### 3.4 GIS and spatial intelligence

- auto-mapping;
- boundary management/versioning;
- constituencies, wards and polling geography;
- demographic and socio-economic layers;
- infrastructure/assets;
- H3/spatial indexing;
- clustering and hotspots;
- issue/event maps;
- survey/election overlays;
- choropleths, points, arcs, heatmaps and time-aware layers;
- advanced Map Lab;
- GIS agent/tooling.

### 3.5 Statistical and analytical workbench

- filtering/grouping/pivoting;
- descriptive statistics;
- correlations;
- regression;
- time-series analysis;
- segmentation/clustering;
- weighting and survey statistics;
- hypothesis/effect analysis where appropriate;
- uncertainty intervals;
- reproducible analytical runs;
- charts/tables/exports;
- AI-assisted analysis over deterministic engines.

### 3.6 Forecasting and simulation

- vote-share forecasting;
- turnout scenarios;
- seat projections;
- swing scenarios;
- Monte Carlo simulation;
- Bayesian models;
- uncertainty/calibration;
- backtesting;
- scenario comparison;
- aggregate/geographic political digital twins;
- model registry and evaluation.

### 3.7 Policy, legislation and governance

- bills and amendments;
- debates and speeches;
- questions and committees;
- acts/regulations/rules;
- policy documents;
- scheme/program monitoring;
- budget/program links;
- manifesto promises;
- promise-to-policy-to-implementation tracking;
- governance outcomes where reliable data exists;
- policy impact/research workflows;
- policy/legislative agents.

### 3.8 Media and narrative intelligence

- news/RSS/public digital ingestion;
- entity extraction;
- issue/topic detection;
- narrative clustering;
- stance/sentiment where methodologically appropriate;
- event timelines;
- media-source comparison;
- narrative change detection;
- public misinformation/claim verification workflows;
- media/narrative agent.

### 3.9 Field operations and war room

- field tasks;
- offline-capable data collection interoperability;
- incidents;
- aggregate turnout/operational updates;
- geographic operational views;
- escalations;
- controller/war-room dashboards;
- team coordination;
- briefing and summaries;
- operational alerting;
- post-event/election learning.

### 3.9A Pre-election booth and microarea field operations

- Canonical polling stations, time-valid aggregate microareas and facilities/accessibility assessments.
- Authorized site assignments, offline field forms, review, conflict resolution and sourced issue summaries.
- Preparedness dashboard for coverage, incomplete work, verified site conditions and incidents.
- Phase 10 war room consumes **the same** station IDs, `Task`, `FieldUpdate`, `Incident` and alert data.
- One owner: `domains/fieldops`. No separate voter CRM, inferred individual political preferences or voter-level tracking.

See [Master Plan](MASTER_PLAN.md), [field contracts](PRE_ELECTION_MICROAREA_INTELLIGENCE.md) and [ADR-0003](DECISIONS/0003-pre-election-microarea-operations.md).

### 3.10 Open platform

- connectors;
- plugins;
- APIs/SDK;
- MCP/tool interfaces where useful;
- scheduled automation;
- local model support;
- BYOAI;
- BYO data;
- exportable work products.

## 4. Non-goals for v1 architecture

- mandatory cloud/SaaS operation;
- mandatory commercial LLM/search/map provider;
- premature microservices;
- multiple competing agent frameworks;
- multiple parallel RAG architectures;
- generic social-network scraping without a documented legal/data route;
- duplicating mature open-source infrastructure solely to own more code;
- LLM-generated election/statistical numbers without deterministic engines;
- individual-level political persuasion/inferred-vote targeting as an AI decision objective.

## 5. Governing engineering principles

### 5.1 Free-to-build

Development should use open-source tooling and free public-repository CI wherever practical.

### 5.2 Local-first

The canonical first installation is a local machine. Team/server deployment is an expansion of the same architecture, not a separate rewrite.

### 5.3 ₹0 core mode

A user should be able to run core Dotpol using local storage, public/local data and local/open models without a mandatory recurring software/API bill.

### 5.4 Reuse before build

Commodity infrastructure should come from strong OSS when possible. Dotpol engineering effort should concentrate on political ontology, data contracts, political engines, analytical workflows, agents and decision intelligence.

### 5.5 One capability owner

Shared platform capabilities are implemented once and reused by domains.

### 5.6 One canonical domain model

The same political entity is reused across elections, surveys, GIS, policy, media and war-room modules.

### 5.7 AI reasons, engines calculate

LLMs orchestrate tools and explain results. Deterministic calculation remains in deterministic/statistical engines.

### 5.8 Provenance by construction

Evidence lineage, transforms, model/tool versions and uncertainty are first-class platform data.

### 5.9 Adapters over lock-in

External AI/search/map/storage providers sit behind Dotpol-owned interfaces.

### 5.10 Change by evidence

Core architecture changes only when documented requirements or measurable risk/benefit justify them.

## 6. Architecture layers

```text
┌─────────────────────────────────────────────┐
│ Applications                                │
│ Web | Field | Admin | future desktop shell  │
└──────────────────────┬──────────────────────┘
                       │
┌──────────────────────▼──────────────────────┐
│ Dotpol Local Gateway / API                  │
│ FastAPI | sessions | tools | plugins        │
└──────────────────────┬──────────────────────┘
                       │
┌──────────────────────▼──────────────────────┐
│ Platform capabilities                       │
│ AI | Search | Data | Provenance | GIS       │
│ Analytics | Documents | Surveys | Workflow  │
└──────────────────────┬──────────────────────┘
                       │
┌──────────────────────▼──────────────────────┐
│ Political domains                           │
│ Elections | Psephology | Forecasting       │
│ Policy | Legislation | Governance | Media  │
│ Research | War Room | Simulation           │
└──────────────────────┬──────────────────────┘
                       │
┌──────────────────────▼──────────────────────┐
│ Agent layer                                 │
│ Research | Election | GIS | Stats | Survey  │
│ Forecast | Policy | Media | War Room        │
└──────────────────────┬──────────────────────┘
                       │
┌──────────────────────▼──────────────────────┐
│ Work products and decisions                 │
│ Briefs | reports | maps | forecasts | alerts│
└─────────────────────────────────────────────┘
```

## 7. Local-first runtime

Default personal mode:

- SQLite for operational metadata/state;
- DuckDB for analytical queries;
- Parquet for portable analytical datasets;
- filesystem for documents/attachments;
- embedded local vector store through an adapter (LanceDB preferred candidate);
- local AI through Ollama/MLX/llama.cpp-compatible paths where supported;
- BYOAI as optional provider configuration.

Future team mode may replace/augment local state with PostgreSQL/shared storage while preserving platform contracts.

## 8. v1 technology direction

- Frontend: React + Next.js.
- UI system: accessible component system; shadcn/ui patterns are acceptable.
- AI streaming/tool UI: use framework utilities/pattern donors, not a mandatory hosted platform.
- Backend/local gateway: Python + FastAPI.
- Agent framework: PydanticAI in v1.
- AI provider abstraction: one Dotpol gateway built on PydanticAI; local Ollama as runtime, no second routing layer.
- Workflow orchestration: Prefect when durable workflows are needed.
- Ingestion: dlt.
- Document processing: Docling.
- GIS map experience: one Kepler.gl embedded workspace (its MapLibre/deck.gl dependencies are internal); GeoPandas handles backend spatial operations.
- Analytics UI: FINOS Perspective.
- Statistics: Statsmodels.
- Bayesian/forecasting: PyMC.
- Tables, pivots and charts: FINOS Perspective (one shared analytics interface).
- Surveys: Dotpol Survey Studio + SurveyJS Form Library where appropriate + ODK interoperability.

A technology listed here is not automatically installed at repository initialization. Add it when the roadmap phase that owns it begins.

## 9. OSS assimilation strategy

All external projects fall into four classes:

1. **Fork donor** — Dotpol expects substantial modifications or selective assimilation.
2. **Dependency** — upstream project is used through a stable interface.
3. **Reference** — architecture/UX is studied without becoming a core runtime dependency.
4. **Dotpol-owned** — political/domain capability built in this repository.

Major current research candidates:

- Open Politics / OPOL — political data/intelligence domain donor/reference;
- Vane — generative-search donor;
- Kepler.gl — selected single GIS workbench when Phase 4 begins;
- Vercel AI Chatbot / LibreChat — chat/tool UX reference donors, not product foundations;
- FINOS Perspective — analytics dependency;
- Docling — document dependency;
- dlt — ingestion dependency;
- GeoPandas — backend spatial operations; Kepler's internal map dependencies are not separate Dotpol integrations;
- Statsmodels/PyMC — statistical dependencies;
- PydanticAI — agent dependency;
- ODK — field/offline interoperability/donor reference;
- SurveyJS Form Library — form runtime candidate.

See `docs/DONOR_MATRIX.md` for current classifications and gates.

## 10. Domain model strategy

Dotpol uses a shared political ontology spanning:

- geography/jurisdictions/boundaries;
- people/parties/organisations/offices/memberships;
- elections/contests/results/candidates;
- surveys/questions/aggregate responses/weighting runs;
- forecasts/scenarios/models/runs;
- policies/bills/amendments/votes/debates/speeches;
- manifestos/promises/schemes/budgets;
- media items/narratives/issues/events;
- datasets/documents/sources/evidence;
- operational incidents/tasks/updates.

Domain modules may define views/read models but must not create competing canonical entities.

## 11. Political knowledge layer

Do not begin by deploying multiple complex graph-RAG systems.

Start with:

- canonical entities and identifiers;
- explicit relationships;
- structured search;
- local full-text retrieval;
- semantic retrieval;
- reranking;
- evidence associations.

Graph-augmented retrieval can be introduced later if evaluations prove a material improvement.

## 12. AI design

One AI model gateway serves all domains and agents.

Agents are specialized orchestrators over shared tools:

- Research Agent;
- Election Agent;
- Survey/Psephology Agent;
- GIS Agent;
- Statistics Agent;
- Forecast Agent;
- Scenario Agent;
- Policy Agent;
- Legislative Agent;
- Media/Narrative Agent;
- Field Operations Agent;
- Data Quality Agent;
- Report Agent;
- War Room Agent.

Agents never own canonical data or deterministic engines.

## 13. Data strategy

Priority order:

1. user-provided local data;
2. official structured/open data;
3. documented public APIs/feeds;
4. openly licensed datasets;
5. web retrieval/search when needed;
6. commercial providers only as optional plugins.

India-first connectors should eventually cover official election, parliament/legislature, law/regulation, government open-data, census/statistics and related public sources where technically and legally available.

International enrichment can include open structured political and event datasets where appropriate.

## 14. Provenance contract

Important derived results should be able to record:

- output/result ID;
- source/evidence IDs;
- dataset version/hash;
- boundary/geography version;
- transform/run ID;
- tool/engine version;
- model/version where applicable;
- parameters;
- retrieved/generated timestamp;
- confidence/uncertainty where applicable;
- actor/agent/workflow that produced the output.

Provenance is shared platform functionality.

## 15. Anti-duplication workflow

Before creating code:

```text
Requirement
  ↓
Capability registry
  ↓
Existing owner?
  ├─ yes -> extend it
  └─ no
       ↓
    OSS search
       ↓
Suitable permissive donor?
  ├─ yes -> adapt behind Dotpol interface
  └─ no  -> build smallest Dotpol capability
       ↓
Tests + provenance + docs
```

No subsystem may bypass this process for convenience.

## 16. Roadmap principle

Dotpol is built as a spine first, capabilities second.

Order:

0. Blueprint/architecture freeze.
1. Local platform foundation.
2. Political data fabric and ontology.
3. Search/research/provenance.
4. GIS and analytical terminal.
5. Election intelligence.
6. Surveys and psephology.
7. Forecasting and simulation.
8. Policy/legislation/governance/manifestos.
9. Media/narrative intelligence.
10. Field operations and war room.
11. Automation/open platform.
12. Hardening/release engineering.

Later phases must not be implemented in a way that bypasses missing prerequisite data contracts or engines.

See `docs/ROADMAP.md` for gates.

## 17. Collaboration model

Every substantial capability needs:

- owner/module;
- typed interface/data contract;
- donor decision;
- licence check;
- tests;
- AI evaluations where relevant;
- provenance behavior;
- roadmap phase;
- documentation.

Architecture debates are settled through ADRs, not repeated redesigns in unrelated PRs.

## 18. Definition of Dotpol's unique value

Open source should solve as much commodity infrastructure as possible:

- UI primitives;
- maps/renderers;
- analytical grids;
- databases;
- vector search;
- document parsing;
- model routing;
- offline survey foundations;
- workflow execution;
- statistical libraries.

Dotpol should concentrate original work on:

- political ontology and data contracts;
- political knowledge layer;
- election intelligence;
- psephology workflows;
- political GIS semantics;
- forecasting/calibration/backtesting;
- scenario engines;
- policy/legislative/governance intelligence;
- manifesto intelligence;
- narrative/event intelligence;
- political agents and toolsets;
- provenance and reproducibility;
- aggregate political digital twins;
- war-room and decision-intelligence workflows.

## 19. Blueprint freeze rule

Blueprint v1.0 is the working architecture until evidence justifies a change.

A change must answer:

1. What documented requirement cannot the current architecture meet?
2. What alternatives were evaluated?
3. What measurable improvement/risk reduction does the change deliver?
4. What duplication/migration does it create?
5. Does it preserve local-first and zero-cost-core guarantees?
6. What licences are introduced?

If these questions cannot be answered, do not change the architecture.
