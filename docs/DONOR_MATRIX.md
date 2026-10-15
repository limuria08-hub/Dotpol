# Dotpol Open-Source Donor Matrix v1.0

## 1. Purpose

Dotpol should aggressively reuse strong open-source engineering while avoiding duplicate frameworks, licence surprises and unnecessary long-term forks.

This matrix classifies candidates as:

- **FORK/DONOR** — maintain a fork/mirror or selectively assimilate because substantial modification is expected.
- **DEPENDENCY** — use upstream through a Dotpol-owned interface; do not fork initially.
- **REFERENCE** — study architecture/UX/algorithms, but do not make it a required runtime component.
- **DOTPOL-OWNED** — capability is core political/domain value and should be implemented in Dotpol.

**Licence rule:** the licence below is a planning signal, not final legal approval. Before code assimilation, pin the exact upstream commit/tag and verify the exact licence plus relevant subcomponent/model licences.

## 2. Priority donor candidates

| Project | Repository | Class | Expected role | Planning licence signal | Decision |
|---|---|---|---|---|---|
| Open Politics / OPOL | `open-politics/opol` | FORK/DONOR + REFERENCE | political ingestion, classification, entity/geocoding/domain patterns | MIT at project level; bundled services need separate review | serious political-domain donor, do not wholesale-copy full stack |
| Vane | `ItzCrazyKns/Vane` — verified fork `kiranvbiim-coder/Vane` | FORK/DONOR (fork created; not integrated) | generative search/research patterns | MIT root only; component review pending | evaluate scoped UI/search modules behind Dotpol Search; avoid bundling SearXNG/second API; [review](DONOR_EVAL_VANE.md) |
| Kepler.gl | `keplergl/kepler.gl` | FORK/DONOR when Phase 4 begins | advanced GIS Map Lab | MIT | core maps use MapLibre/deck.gl; Kepler is advanced analyst workspace |
| Vercel AI Chatbot | `vercel/chatbot` | REFERENCE/DONOR | streaming chat, tool UI, artifact interaction patterns | verify exact repository version | do not make Dotpol product architecture depend on template |
| LibreChat | `LibreChat-AI/LibreChat` | REFERENCE | chat/agent/MCP/file UX patterns | MIT | reference rich AI workspace behavior; avoid parallel app foundation |

## 3. Core dependencies

| Project | Repository | Class | Role | Planning licence signal | Notes |
|---|---|---|---|---|---|
| FastAPI | `fastapi/fastapi` | DEPENDENCY | local gateway/API | permissive | Python backend foundation |
| DuckDB | `duckdb/duckdb` | DEPENDENCY | embedded analytics | MIT | local analytical engine |
| LanceDB | `lancedb/lancedb` | DEPENDENCY candidate | embedded vector retrieval | Apache-2.0 planning signal | keep behind adapter; verify when adopted |
| dlt | `dlt-hub/dlt` | DEPENDENCY | ingestion | Apache-2.0 planning signal | one primary ingestion framework |
| Docling | `docling-project/docling` | DEPENDENCY | document extraction | MIT planning signal | models/subdependencies need their own review |
| MapLibre GL JS | `maplibre/maplibre-gl-js` | DEPENDENCY | map renderer | BSD-3-Clause planning signal | no mandatory proprietary map provider |
| deck.gl | `visgl/deck.gl` | DEPENDENCY | large geospatial layers | MIT planning signal | core GIS visualization |
| H3 | `uber/h3` | DEPENDENCY | spatial indexing | Apache-2.0 planning signal | use official upstream |
| FINOS Perspective | `perspective-dev/perspective` | DEPENDENCY | analytical grid/pivot/workbench | Apache-2.0 planning signal | terminal-grade interactive analytics |
| Statsmodels | `statsmodels/statsmodels` | DEPENDENCY | statistics/econometrics | BSD planning signal | deterministic statistics |
| PyMC | `pymc-devs/pymc` | DEPENDENCY | Bayesian modelling | Apache-2.0 planning signal | introduce in forecasting/psephology phase |
| PydanticAI | `pydantic/pydantic-ai` | DEPENDENCY | v1 agent runtime | MIT planning signal | one agent framework in v1 |
| LiteLLM | `BerriAI/litellm` | DEPENDENCY candidate | provider routing | MIT core; enterprise areas separate | only permissive OSS portions; Dotpol owns gateway interface |
| Prefect | `PrefectHQ/prefect` | DEPENDENCY | durable workflows | Apache-2.0 planning signal | add only when automation phase requires it |
| SurveyJS Form Library | `surveyjs/survey-library` | DEPENDENCY/FORK candidate | web form runtime | MIT planning signal | visual Survey Creator is separate/commercial; Dotpol builds its own studio |
| ODK | `getodk/collect`, `getodk/central` | INTEROP/REFERENCE | offline field collection/sync | verify exact component licences | integrate before rebuilding offline field stack |

## 4. Experimental/reference candidates

| Project | Class | Use |
|---|---|---|
| Microsoft GraphRAG | REFERENCE/EXPERIMENT | graph/entity retrieval ideas; not a second production RAG in v1 |
| LightRAG | REFERENCE/EXPERIMENT | graph-enhanced RAG evaluation |
| Apache Superset | REFERENCE | BI/dashboard patterns; too large to become core workbench initially |
| Meltano | REFERENCE/FALLBACK | connector ecosystem if dlt cannot satisfy a documented requirement |
| OpenRefine | REFERENCE | data-cleaning/entity-reconciliation UX and workflows |
| BERTopic | DEPENDENCY candidate later | topic/narrative clustering when media phase begins |
| promptfoo | DEPENDENCY candidate | AI evaluation when evaluation infrastructure begins |
| Langfuse | OPTIONAL/REFERENCE | self-hosted tracing/evaluation patterns; avoid mandatory runtime dependency |

## 5. Projects to keep outside the permissive core unless an ADR approves otherwise

This list is not a judgement on project quality. It protects Dotpol's local-first/permissive/zero-cost architecture.

### SearXNG

Useful self-hosted search metasearch software, but AGPL implications require deliberate architectural/legal treatment. Do not vendor into permissive Dotpol core by default. External/user-hosted integration can be supported through `SearchProvider`.

### n8n

Useful workflow product, but its licence model is not the default fit for embedding as Dotpol's core automation engine. Use Prefect/open Python workflows instead unless an ADR changes this.

### Dify / other source-available AI platforms

Study concepts where useful; do not make them foundational without explicit licence/architecture review.

### Airbyte

Strong connector ecosystem but licence/operational complexity is unnecessary for the initial local-first core. Prefer dlt and add specific adapters.

### Hosted-only services

Pinecone, mandatory Mapbox/Google Maps billing, hosted-only auth/databases or mandatory commercial search APIs cannot be required core dependencies.

## 6. What Dotpol should own

Open-source donors should not replace Dotpol's domain innovation.

**DOTPOL-OWNED:**

- canonical political ontology/data contracts;
- entity resolution rules for political domain data;
- political source/evidence/provenance semantics;
- election intelligence workflows;
- constituency intelligence;
- psephology workflows;
- political GIS semantics/layers;
- forecast specifications/calibration/backtesting;
- scenario/simulation workflows;
- policy/legislative/governance intelligence;
- manifesto promise tracking semantics;
- media/narrative political intelligence;
- political agent toolsets;
- war-room intelligence;
- aggregate/geographic political digital-twin models;
- evidence-backed political work products.

## 7. Donor assimilation process

Before assimilating code:

1. Name the capability being solved.
2. Confirm no existing Dotpol owner already solves it.
3. Compare at least the meaningful OSS candidates.
4. Verify exact repository and upstream commit/tag.
5. Verify licence and relevant subcomponent licences.
6. Decide fork vs dependency vs reference.
7. Define a Dotpol-owned interface around the capability.
8. Import only the modules/code actually needed where practical.
9. Preserve required copyright/licence notices.
10. Add tests for the Dotpol interface.
11. Add local-first verification.
12. Record the upstream version in `architecture/donors.lock.yml`.
13. Document how upstream updates will be reviewed.

## 8. Fork policy

Fork only when at least one of these is true:

- Dotpol needs substantial upstream-incompatible changes;
- the donor is being transformed into a Dotpol-specific workspace;
- upstream release cadence creates unacceptable integration risk and we need a controlled patch line;
- selective assimilation is safer through a maintained mirror.

Otherwise use a dependency.

## 9. Upstream sync policy

Never auto-merge upstream into a heavily modified fork.

For each fork:

- track upstream repository;
- pin upstream base commit/tag;
- periodically review release/security changes;
- cherry-pick/rebase intentionally;
- run Dotpol tests/evaluations before accepting updates;
- update donor lock metadata.

## 10. Current high-level decision

Do not fork everything immediately.

Phase 0/1 should establish Dotpol's interfaces first. Donor forks should be created/assimilated when the capability's roadmap phase begins, so we do not maintain unused forks or prematurely inherit their architecture.

## 11. Second-pass donor research and coverage audit — 2026-10-15

**Verified fork status:** Vane is forked under [`kiranvbiim-coder/Vane`](https://github.com/kiranvbiim-coder/Vane) as of 2026-10-15, with upstream and fork `master` at the same observed commit `348feca3e378fb4157b217724ed508dc707f853f`. See [Vane evaluation](DONOR_EVAL_VANE.md). This does *not* imply a component licence clearance or Dotpol integration.



This matrix remains the *architecture-level classification*. See the expanded **[43-candidate research register](DONOR_RESEARCH_2026-10-15.md)** and **[reuse/fork playbook](OSS_REUSE_AND_FORK_POLICY.md)**, backed by the machine-readable **`architecture/donor-candidates.yml`** inventory.

The user's aspirational **90% commodity functionality reuse** target is accepted as a *direction*, not proven code coverage. Track acceptance-tested third-party functionality separately from original political domain models and from the mere existence of forks.

**New donors/alternatives recommended for evaluation (not adopted):**

- Political ingestion/ontology: OpenElections, OpenStates, Popolo data standard (reference only), Splink vs dedupe for entity resolution.
- Local data/analytics: GeoPandas, PMTiles, Tippecanoe, Apache ECharts, OpenRefine/Datasette reference interfaces.
- Surveys/field: XLSForm/pyxform plus ODK Collect/Central interoperability instead of creating another offline mobile stack.
- Narrative/media: BERTopic; RSSHub is AGPL, so external interoperability only until reviewed.
- Model and privacy tooling: Ollama/llama.cpp optional local runtimes, promptfoo evaluations, OpenTelemetry and Presidio privacy helpers.
- Policy impact: OpenFisca is AGPL and should remain external/reference until a written licence and architecture decision.

**New risk findings:** OPOL's latest observed GitHub push was 2025-05-06 (low maintenance signal), while Vane and Kepler are active in 2026. Vane advertises MIT but bundles SearXNG, which is AGPL; evaluate exact modules instead of whole-stack assimilation. Open WebUI's newer branding clause makes it unsuitable as an unreviewed permissive-core donor. SurveyJS Form Library remains distinct from commercial Survey Creator. Every repo's code, model weights, map tiles, datasets, services and dependencies have independent rights.

**Canonical upstream URL maintenance:** LibreChat's current upstream is `LibreChat-AI/LibreChat`; FINOS Perspective's current upstream is `perspective-dev/perspective`. Name changes do not approve new versions or mark adoption complete.

**Fork policy retained:** prefer upstream dependencies/adapters; do not create all possible forks upfront. Propose Vane as the first targeted review/fork candidate, Kepler in Phase 4 only if custom modifications are required, and OPOL only after a scoped module/licence audit. Forking a repo is not integrating it.

No roadmap phase or donor was marked complete through this research.

### Vane concrete module outcomes (source screening only)

The [2026-10-15 Vane module-level matrix](VANE_MODULE_DECISION_MATRIX.md) makes narrower donor decisions: **A candidates** for selected UI/progress/citation components, **B references** for classifier/research heuristics, **C optional external** SearXNG/Vane API adapters, and **D excluded as-is** duplicate database/model/tool runtimes, insecure browser scraper and bundled Docker stack. No integration, full dependency review or security testing has occurred. The fork remains under `kiranvbiim-coder/Vane`.
