# Dotpol — One Canonical Technology per Capability

**Date:** 2026-10-15  
**Status:** Selected canonical planning baseline (ADR-0002). **No implementation**; exact version, component licence and integration tests pending.  
**Goal:** ~90% reuse of *commodity capabilities* through maintained upstream code and small adapters, not blind code copying or fork counts.  
**Scope:** One local-first political intelligence product, one owner per capability; no second application stack for a feature. This does not claim all 13 phases can be completed in seven days.

## The rules (mandatory for implementation once approved)

1. **One owning subsystem per job**: agents, local inference, operational records, source extraction, retrieval, analytical SQL, map experience, statistics, surveys, workflows.
2. **Do not fork unless an approved code modification is necessary**. Published packages and app components are faster. A dependency of a selected framework is not an independently managed second Dotpol engine.
3. **Do not install multiple products for the same job**. The historical [43-candidate inventory](DONOR_RESEARCH_2026-10-15.md) is research evidence, **not an implementation shopping list**.
4. **Scope by phase**. The first preview uses only the *first-release* rows. Later-phase selections are roadmap decisions, not instructions to install everything now.
5. **Upstream status is not adoption**. Pin version and module, review licence/transitive assets, preserve notices, measure local/no-key tests and evidence handling, then move from proposed to integrated and verified.
6. Any change to the frozen Blueprint's core GIS, vector retrieval or framework arrangements requires a documented maintainer-approved ADR before code changes. The proposed single-map plan below deliberately removes extra top-level GIS engines; Kepler's internal transitive rendering dependencies remain its implementation details.

## The selected stack — exactly one authoritative choice for each purpose

Each technology has **one exclusive purpose**. A combination is permitted only when components do different jobs. The matrix specifies the one selected integration point.

| Purpose / owner | **Single selected technology** | Integration boundary | First release? | Source |
|---|---|---|---|---|
| Primary web application / `apps/web` | **Next.js** | Own all Dotpol web routing, workspace and pages; one React app | **YES** | https://github.com/vercel/next.js |
| Existing research source/citation/progress UI donor / `apps/web` | **Vane (selected UI modules)** | Adapt `MessageSources`, `Citation`, `AssistantSteps` only *after licence/security review*. Not a second app/API/DB/research-agent runtime | **YES, if cleared** | https://github.com/kiranvbiim-coder/Vane |
| Local API gateway / `services/api` | **FastAPI** | One local HTTP interface; registered platform packages own reusable logic | **YES** | https://github.com/fastapi/fastapi |
| Agent orchestration, typed tools / `platform/ai` | **PydanticAI** | One tool/agent framework and provider-neutral orchestration | **YES** | https://github.com/pydantic/pydantic-ai |
| Local model serving / `platform/ai` | **Ollama** | One opt-in local model runtime; no mandatory cloud, no forced model download | **YES if user installed it** | https://github.com/ollama/ollama |
| Local operational state / `platform/data` | **SQLite** | Workspace, sessions, canonical source metadata, settings, trace records; **not** analytical dataset engine | **YES** | https://sqlite.org/ |
| Batch/official data ingestion / `platform/data` | **dlt** | One pipeline abstraction and incremental source adapters, including official election/policy ingestion later | Phase 2 | https://github.com/dlt-hub/dlt |
| PDF/Office/document parsing / `platform/documents` | **Docling** | One structured extraction path with versioned page/span/source provenance; basic plaintext/CSV handled natively until needed | Phase 2 / preview stretch | https://github.com/docling-project/docling |
| Local retrieval (keyword, vector, hybrid) / `platform/search` | **LanceDB OSS** | **One retrieval index** for both text/BM25 and vector when enabled; separate from SQLite metadata. Store source/evidence IDs in every hit | **YES for evidence search if feasible** | https://github.com/lancedb/lancedb |
| Large tabular/political analytics SQL / `platform/analytics` | **DuckDB** | One analytical calculation/query engine for CSV, Parquet and election/survey aggregates; never duplicate SQLite's metadata owner | Phase 4 | https://github.com/duckdb/duckdb |
| Analyst tables, pivots and charts / `apps/web` + `platform/analytics` | **FINOS Perspective** | Single interactive table/chart workbench; no separately owned chart engine | Phase 4 | https://github.com/perspective-dev/perspective |
| Interactive maps + GIS Map Lab / `platform/gis` + `apps/web` | **Kepler.gl** | Single chosen map UI/workbench; Kepler internally brings MapLibre/deck.gl. **Do not independently integrate parallel map renderers or separate map UIs** | Phase 4 | https://github.com/keplergl/kepler.gl |
| Geospatial geometry/joins / `platform/gis` | **GeoPandas** | Spatial transform/joins and source-aligned boundaries on backend; no frontend map ownership | Phase 4 | https://github.com/geopandas/geopandas |
| Reproducible descriptive/regression statistics / `platform/analytics` | **Statsmodels** | Deterministic classical statistical methods and reference calculations; domain owns election semantics | Phase 4–6 | https://github.com/statsmodels/statsmodels |
| Bayesian forecasts / `domains/forecasting` | **PyMC** | Posterior estimation and simulations only; no second general statistics engine | Phase 7 | https://github.com/pymc-devs/pymc |
| Web survey form rendering and response capture / `platform/surveys` | **SurveyJS Form Library** | MIT form runtime only; survey design/schema/editor policy remains Dotpol-owned. **Do not include commercially licensed Survey Creator** | Phase 6 | https://github.com/surveyjs/survey-library |
| Offline Android field form collection / `apps/field` | **ODK Collect** | External/mobile capture interop once needed; no duplicated web survey authoring engine and no mandatory separate server | Phase 6/10 | https://github.com/getodk/collect |
| Media theme/topic clustering / `domains/media` | **BERTopic** | Analysis on lawfully sourced versioned documents; label outputs as model-derived | Phase 9 | https://github.com/MaartenGr/BERTopic |
| PII redaction support / `platform/data` | **Presidio** | Helper detection/redaction prior to sharing/export; privacy policy and lawful processing are separate governance obligations | Phase 2 | https://github.com/data-privacy-stack/presidio |
| Scheduled jobs/automation / `platform/automation` | **Prefect** | One orchestrator only once durable user-triggered/periodic jobs are required | Phase 11 | https://github.com/PrefectHQ/prefect |
| AI/research evaluation / `evaluations` | **promptfoo** | One regression test harness for unsafe tools, grounded citations and agent injection | Phase 1–3 | https://github.com/promptfoo/promptfoo |

### Why this isn't duplication

- **SQLite vs DuckDB vs LanceDB:** operational records vs columnar data analysis vs retrieval index. Each has a distinct exclusive owner and data lifecycle. Do not store independent authoritative copies of the same canonical political entity in three places.
- **Kepler vs GeoPandas:** one interactive map workbench vs backend spatial calculation. Kepler's MapLibre/deck.gl *transitive* internals **are not separately owned Dotpol integrations**. Verify one embedding path and no mandatory Mapbox key by configuring an appropriately licensed local/self-hosted basemap before accepting this departure from current Blueprint GIS arrangement.
- **Vane vs PydanticAI/LanceDB:** Vane donates *some React presentation components only*. Dotpol does not run Vane's whole researcher, Next.js API routes, SQLite index, LLM gateway or SearXNG as a parallel system.
- **SurveyJS vs ODK Collect:** web-form runtime vs offline Android collection on a **later mobile platform**. Survey question IDs/source and response contracts remain canonical in Dotpol; do not build two different survey-schema editors.
- **Statsmodels vs PyMC:** deterministic descriptive/classical analysis vs specialized Bayesian posterior models; no duplicated 'general forecasting' interface.
- **Policy/election/legislation/war-room:** no dedicated third-party competing core app. Reuse **dlt**, **DuckDB**, **Statsmodels**, **Kepler**, **PydanticAI**, **Prefect** via one shared capability registry; Dotpol owns political rules, entity schema and legally sourced adapters.

## Execution wave lock

### Now — first 3–7-day **research preview**, NOT the whole product

1. Next.js UI + FastAPI local gateway + SQLite project/source state.
2. PydanticAI tool gateway; local Ollama only if installed; truthful missing-model handling.
3. LanceDB *one* local retrieval path (text first; semantic search only when available) with stable source/span/row IDs.
4. Import TXT/CSV/JSON with simple built-in parsers. Use Docling only after import contract and source fidelity work; keep it a preview stretch.
5. Use up to three Vane presentation modules **only after** component notices, safe URL handling, evidence link validation and UI acceptance.
6. Demonstrate a restart-safe imported workspace, correct citation/no-evidence behavior and a saved brief. Security/CI acceptance gates from [rapid preview](https://github.com/limuria08-hub/Dotpol/pull/3) remain non-negotiable.

**Explicitly absent from this sprint:** heavyweight GIS/Kepler, tabular workbench, dlt pipelines, forecasting, surveys, field/mobile, scheduled automations, media models and other later-phase runtime dependencies.

### Later phases — implement selected row *once* when the use case arrives

Phase 2: dlt, Docling, Presidio.  
Phase 4–5: DuckDB, Perspective, Kepler, GeoPandas, Statsmodels.  
Phase 6–7: SurveyJS Form Library, ODK Collect, PyMC.  
Phase 9: BERTopic.  
Phase 11: Prefect.

No blank scaffolds/idle runtimes should be installed for later phases.

## What is deliberately **not** a second stack

Historical research remains in [43-donor register](DONOR_RESEARCH_2026-10-15.md), but **none of the unused candidates are implementation choices**. Their records remain candidate/rejected-by-this-selection until an approved ADR shows a measurable need to change an owner. Do not adopt extra chat frameworks, model routers, inference servers, web search stacks, GIS renderers, chart frameworks, identity matchers, vector databases, survey creators or workflow engines without explicit capability-level replacement.

No new forks required. The Vane fork exists; Kepler **should be used as an upstream dependency first** and forked only if a concrete modification beyond the public component API is unavoidable.

## Before releasing these components

- [x] Consolidated one-per-purpose stack and single Kepler map UI recorded in Blueprint/Architecture (planning only).
- [ ] Resolve [proposed ADR-0001](https://github.com/limuria08-hub/Dotpol/pull/1) about `services/api` and `platform/` owners.
- [ ] Set exact versions/lockfiles and transitive/asset licence reviews *per imported component*. SurveyJS free Form Library is **not** Survey Creator; separate Geo basemap/tile rights.
- [ ] Confirm one supported development OS, local model availability, CPU/GPU and preview acceptance tests. Kepler React/Redux/basemap integration needs its own phase.
- [ ] Record owner for each capability in `architecture/capabilities.yml` and update `docs/ARCHITECTURE.md` only once ADR is accepted.
- [ ] At integration PR time, mark donor in `architecture/donors.lock.yml` with actual pinned SHA and licence approval, never by intention alone.

## References checked

- PydanticAI official Ollama support: https://github.com/pydantic/pydantic-ai/blob/main/docs/models/ollama.md
- LanceDB full-text/semantic/hybrid search: https://docs.lancedb.com/ and https://github.com/lancedb/docs/blob/main/docs/search/full-text-search.mdx
- Kepler documentation says MapLibre GL + deck.gl inside one embedded component: https://github.com/keplergl/kepler.gl
- Kepler token-free MapLibre examples vs older Mapbox-default docs: https://github.com/keplergl/kepler.gl/blob/master/examples/README.md
- SurveyJS licences: https://surveyjs.io/licensing

**This is one selected implementation plan, not proof of technical integration, runnable CI or legal clearance.**
