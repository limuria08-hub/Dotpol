# Dotpol Donor Research — Historical Candidate Register (Round 2)

**ACTIONABLE SELECTION:** [One canonical technology per capability](SINGLE_STACK_SELECTION.md) and [selected stack manifest](../architecture/selected_stack.yml) supersede the alternatives below for implementation planning. The 43 items are retained for traceable research, **not an instruction to adopt 43 apps**.

**As of:** 2026-10-15. **Status:** candidate evaluation; no production adoption/fork approval.  
**Repo owner:** `limuria08-hub/Dotpol`. **Companion:** [OSS reuse and fork playbook](OSS_REUSE_AND_FORK_POLICY.md) and [current donor matrix](DONOR_MATRIX.md).

## Why this exists

The strategic aspiration is **approximately 90% reuse of commodity engineering**, not 90% blind code copying and not a measured achievement. Reuse can mean existing OSS **dependencies**, interoperable local apps, reference patterns, or selectively modified forks. Dotpol still owns political ontology, evidence semantics, domain contracts, local gateway composition, inference guardrails and vertical workflows.

Scope: 43 candidate entries across political data, knowledge, ingestion, AI, research, analytics, maps, surveys, policy, media and security. The candidates are not a licence clearance, proof of API compatibility, or commitment to run their full stacks.

## Most important findings

1. **OPOL:** distinctive political domain work, but GitHub metadata indicates last push **2025-05-06**, and the multi-service stack does not map directly to Dotpol's embedded/local architecture. Repository README reports MIT, while GitHub top-level SPDX is inconclusive; module and bundled service audits remain mandatory. Prefer architectural/pipeline reference, followed by targeted code review, not an immediate wholesale fork.
2. **Vane:** active on GitHub in 2026 and its root advertises MIT, but its shipped search setup includes SearXNG (AGPL). Reuse only evaluated modules or UX patterns through `SearchProvider`; do not embed an AGPL-dependent bundle into permissive core without legal/ADR review.
3. **Kepler.gl:** well-maintained MIT advanced GIS candidate; reserve its fork for Phase 4 when the Map Lab interface/desired modifications are scoped. Core MapLibre + deck.gl remains distinct from Kepler workspace.
4. **OpenElections / OpenStates / Popolo:** potentially valuable political domain/ingestion/ontology references, but source jurisdictions and stacks differ; never replace Dotpol's cross-country canonical identities with a US-only or old Rails schema.
5. **Splink:** a strong MIT probabilistic record-linkage candidate. Add a *single* data-owned identity-resolution service instead of separate matching code in policy/elections/media.
6. **Perspective:** upstream's canonical repository is `perspective-dev/perspective` (previous references `finos/perspective` may redirect). The dependency can remain FINOS Perspective product.
7. **Data privacy:** Presidio moved to `data-privacy-stack/presidio`, which remains MIT. It can assist but does not solve consent/legal/retention controls.
8. **Major licensing traps:** current Open WebUI licensing includes branding restrictions; OpenFisca and RSSHub report AGPL; SurveyJS Form Library is MIT but Survey Creator/Dashboard/PDF Generator are commercial products; model weights, map tiles and dataset rights are separate from source-code licences.
9. **Fork is not integration.** A reference read, a GitHub fork, a dependency in a lock file, an adapter compiling and an end-to-end verified capability are five different states.

## Candidate inventory

The 'licence signal' reflects GitHub repository metadata and/or upstream documentation **only**; none of these were approved after a pinned component/dependency review. 'Phase' indicates when to examine integration, not when to fork.

| Capability | Candidate upstream | Phase | Initial classification | Licence signal | Fit and caveat |
|---|---|---:|---|---|---|
| political-domain | [`open-politics/opol`](https://github.com/open-politics/opol) | 2 | selective-reference | reported MIT; manifest inconclusive | Stale since 2025-05; multi-service PG/pgvector/SearXNG architecture; study entity/pipeline patterns, never full stack |
| election-ingestion | [`openelections/openelections-core`](https://github.com/openelections/openelections-core) | 5 | reference-or-selective-donor | MIT | US-focused parsers, older packaging; adapt reusable normalized aggregate result patterns only |
| legislation-ingestion | [`openstates/openstates-core`](https://github.com/openstates/openstates-core) | 8 | reference | MIT | US-only Django/data model; borrow API/scraper mapping patterns, no second backend |
| civic-ontology | [`popolo-project/popolo-spec`](https://github.com/popolo-project/popolo-spec) | 2 | standards-reference | spec licence review | Old specification, useful Person/Org/Membership/Vote mapping, not new canonical ontology |
| record-linkage | [`moj-analytical-services/splink`](https://github.com/moj-analytical-services/splink) | 2 | dependency-candidate | MIT | Probabilistic entity matching; avoid merging uncertain political identities; benchmark on synthetic fixtures |
| record-linkage-alt | [`dedupeio/dedupe`](https://github.com/dedupeio/dedupe) | 2 | alternative-reference | MIT | Alternative to Splink; compare, select one method runtime not both by default |
| data-reconciliation | [`OpenRefine/OpenRefine`](https://github.com/OpenRefine/OpenRefine) | 2 | external-tool-or-reference | BSD-3-Clause | Java app; use separately/local or UX reference; do not embed whole cleaning platform |
| research-search | [`ItzCrazyKns/Vane`](https://github.com/ItzCrazyKns/Vane) | 3 | selective-fork-candidate | MIT parent; component review | Strong UX/search patterns; SearXNG inside stack has AGPL impact; no wholesale embed |
| chat-workspace | [`LibreChat-AI/LibreChat`](https://github.com/LibreChat-AI/LibreChat) | 1 | reference | MIT parent; modules vary | Agent/tool/file UX only; do not adopt competing app/server; admin-panel in org is AGPL |
| chat-template | [`vercel/chatbot`](https://github.com/vercel/chatbot) | 1 | reference-or-selective-donor | check exact ref | Chat streaming/artifact patterns; no Vercel hosted coupling |
| chat-alternative | [`open-webui/open-webui`](https://github.com/open-webui/open-webui) | 1 | reference-restricted | custom branding restrictions after v0.6.5 | Avoid embedding current code into permissive Dotpol until explicit legal approval |
| agent-runtime | [`pydantic/pydantic-ai`](https://github.com/pydantic/pydantic-ai) | 1 | dependency | MIT | Single v1 orchestration framework; already selected |
| local-model | [`ollama/ollama`](https://github.com/ollama/ollama) | 1 | optional-runtime | MIT | Optional local inference server, not a required bundled daemon |
| local-inference-alt | [`ggml-org/llama.cpp`](https://github.com/ggml-org/llama.cpp) | 1 | optional-runtime | MIT | Alternative local inference adapter; avoid bundling large models |
| model-routing | [`BerriAI/litellm`](https://github.com/BerriAI/litellm) | 1 | candidate-with-licence-gate | no clear repository SPDX | Use permissive SDK/core only if exact package/component passes review |
| workflow-engine | [`PrefectHQ/prefect`](https://github.com/PrefectHQ/prefect) | 11 | dependency | Apache-2.0 | Durable workflows on demand, not in foundation before necessary |
| ingestion-engine | [`dlt-hub/dlt`](https://github.com/dlt-hub/dlt) | 2 | dependency | Apache-2.0 | One reusable incremental ingestion contract |
| doc-parser | [`docling-project/docling`](https://github.com/docling-project/docling) | 2 | dependency | MIT code; model weights separate | Single document pipeline; separate model licences/weights |
| sql-analytics | [`duckdb/duckdb`](https://github.com/duckdb/duckdb) | 4 | dependency | MIT | Single local analytical query execution owner |
| analyst-table | [`perspective-dev/perspective`](https://github.com/perspective-dev/perspective) | 4 | dependency | Apache-2.0 | FINOS Perspective canonical repo now perspective-dev; plug through analytics UI |
| fast-chart | [`apache/echarts`](https://github.com/apache/echarts) | 4 | dependency-candidate | Apache-2.0 | One chart renderer behind shared chart interface |
| vector-search | [`lancedb/lancedb`](https://github.com/lancedb/lancedb) | 3 | dependency-candidate | Apache-2.0 | Local semantic index behind adapter; avoid second vector store |
| gis-core-renderer | [`maplibre/maplibre-gl-js`](https://github.com/maplibre/maplibre-gl-js) | 4 | dependency | BSD family; component check | GIS base map; tile/data rights separate |
| gis-layer-renderer | [`visgl/deck.gl`](https://github.com/visgl/deck.gl) | 4 | dependency | MIT | Shared geospatial layers, no per-domain map engine |
| gis-lab | [`keplergl/kepler.gl`](https://github.com/keplergl/kepler.gl) | 4 | selective-fork-candidate | MIT | High-value advanced analyst Map Lab; fork when actual modifications scoped |
| geo-frame | [`geopandas/geopandas`](https://github.com/geopandas/geopandas) | 4 | dependency-candidate | BSD-3-Clause | Spatial joins/projections; reuse with core GIS contracts |
| spatial-format | [`protomaps/PMTiles`](https://github.com/protomaps/PMTiles) | 4 | dependency-candidate | BSD-3 code; sample tiles separately licensed | Portable offline tile packages; never assume embedded tile assets redistributable |
| tile-generator | [`felt/tippecanoe`](https://github.com/felt/tippecanoe) | 4 | external-tool-dependency | BSD-2-Clause | Build offline vector tiles when required, not browser embedded |
| geospatial-io | [`OSGeo/gdal`](https://github.com/OSGeo/gdal) | 4 | external-tool-dependency | multi-component; verify | Conversion/reprojection library; ensure binary/distribution review |
| statistics | [`statsmodels/statsmodels`](https://github.com/statsmodels/statsmodels) | 4 | dependency | BSD-3-Clause | Deterministic statistics; do not calculate in LLM prompt |
| bayesian | [`pymc-devs/pymc`](https://github.com/pymc-devs/pymc) | 7 | dependency | repo SPDX unclear; verify exact component | Bayesian forecasts and posterior predictive checking |
| policy-simulation | [`openfisca/openfisca-core`](https://github.com/openfisca/openfisca-core) | 8 | external-or-reference | AGPL-3.0 | Potential laws-as-code; avoid embedding into permissive core |
| survey-forms | [`surveyjs/survey-library`](https://github.com/surveyjs/survey-library) | 6 | dependency | MIT Form Library only | Render forms, Dotpol authors Survey Studio; commercial Survey Creator excluded |
| survey-xlsform | [`XLSForm/pyxform`](https://github.com/XLSForm/pyxform) | 6 | interop-dependency-candidate | BSD-2-Clause | Use XLSForm conversion for ODK interoperability if needed |
| offline-field | [`getodk/collect`](https://github.com/getodk/collect) | 6 | interop-or-fork-later | repo SPDX inconclusive | Android offline workflows; confirm exact module licensing before any fork |
| survey-server | [`getodk/central`](https://github.com/getodk/central) | 6 | optional-external-service | Apache-2.0 | Interoperate; no mandatory separate server |
| survey-server-alt | [`kobotoolbox/kpi`](https://github.com/kobotoolbox/kpi) | 6 | external-only | AGPL-3.0 | Do not embed as permissive Dotpol survey backend |
| media-narratives | [`MaartenGr/BERTopic`](https://github.com/MaartenGr/BERTopic) | 9 | dependency-candidate | MIT | Topic clustering with evaluation/robust multilingual support |
| rss-adapters | [`DIYgod/RSSHub`](https://github.com/DIYgod/RSSHub) | 9 | external-only | AGPL-3.0 | Possible independently hosted/user-managed integration, not vendored core |
| privacy-pii | [`data-privacy-stack/presidio`](https://github.com/data-privacy-stack/presidio) | 2 | dependency-candidate | MIT | Optional PII recognition/redaction (not complete privacy compliance) |
| eval-ai | [`promptfoo/promptfoo`](https://github.com/promptfoo/promptfoo) | 1 | dev-eval-dependency | MIT | Offline/no-key and security regression evals when test infrastructure begins |
| tracing | [`open-telemetry/opentelemetry-python`](https://github.com/open-telemetry/opentelemetry-python) | 1 | dependency-when-needed | Apache-2.0 | Opt-in local instrumentation; no hosted service requirement |
| data-browser | [`simonw/datasette`](https://github.com/simonw/datasette) | 4 | external-or-reference | Apache-2.0 | Lightweight published datasets; avoid second core UI/database layer |

## Preferred by capability (avoid competing duplicate engines)

| Dotpol owner | First choice | Comparison / rule |
|---|---|---|
| `platform/ai` | PydanticAI + provider-owned model gateway | LiteLLM optional after package licence/security review; local Ollama or llama.cpp is a provider, not a second gateway |
| `platform/data` | dlt + Docling + single source registry | evaluate OPOL/OpenElections/OpenStates as adapters/patterns only; **Splink versus dedupe**, not both blindly |
| `platform/search` | unified hybrid search + LanceDB adapter | Vane patterns selectively; SearXNG external/AGPL review only; no parallel RAG framework |
| `platform/gis` | MapLibre + deck.gl + H3 + GeoPandas/PMTiles when needed | Kepler.gl = advanced Map Lab only; GDAL/Tippecanoe external conversion tools |
| `platform/analytics` | DuckDB + Perspective + Statsmodels/PyMC | ECharts chart interface; avoid a second analytics DB or BI stack |
| `platform/surveys` | SurveyJS free Form Library + ODK/XLSForm interoperability | Dotpol-owned survey authoring; no commercial Survey Creator or forced Kobo/ODK server |
| `domains/elections` | Dotpol election rules + open-source parsing patterns | official Indian data and versioned constituency geography need Dotpol adapters |
| `domains/policy` | Dotpol policy models + official data ingest | OpenFisca only optional external/explicit AGPL review |
| `domains/media` | BERTopic as needed + lawful source adapters | RSSHub only external/AGPL review, method-labeled narrative extraction |
| evaluation/privacy | promptfoo, Presidio, OpenTelemetry as bounded dependencies | local-first, test security and licence before adoption |

## Verified Vane fork — 2026-10-15

GitHub verified [kiranvbiim-coder/Vane](https://github.com/kiranvbiim-coder/Vane) as a fork of [ItzCrazyKns/Vane](https://github.com/ItzCrazyKns/Vane), with both observed `master` heads at `348feca3e378fb4157b217724ed508dc707f853f`. Its root MIT licence was read, but SearXNG, transitive modules and model/data terms remain subject to a component-level audit. See [fork assessment](DONOR_EVAL_VANE.md) and [21-entry adoption matrix](VANE_MODULE_DECISION_MATRIX.md).


## Immediate fork decisions (planning stage)

- **Verified existing fork:** `kiranvbiim-coder/Vane` is a true fork of `ItzCrazyKns/Vane` with observed master SHA `348feca3e378fb4157b217724ed508dc707f853f`. No module has been integrated. Avoid duplicate unused forks.
- **First selective assimilation evaluation:** assess the already forked Vane modules. Keep it under its actual owner `kiranvbiim-coder` unless maintainers decide a transfer/duplicate is necessary. See [Vane review](DONOR_EVAL_VANE.md).
- **Second high-value future fork:** `keplergl/kepler.gl` when Phase 4 has an agreed Map Lab contract and real need for divergent patches. Do not fork just to preserve a copy.
- **Conditional political code donor:** `open-politics/opol` only after pinpointing exact files, verifying licence/subcomponents and checking whether its old services are necessary.
- **Dependencies, not forks:** Docling, dlt, DuckDB, PydanticAI, Perspective, Splink, Statsmodels, PyMC, MapLibre, deck.gl, LanceDB, SurveyJS Form Library, BERTopic etc.
- **External/reference/blocked core:** OpenFisca, RSSHub, Kobo KPI, recent Open WebUI and any donor component with unresolved copyleft or proprietary terms.

## Research validation and limitations

Checked GitHub repositories and their reported licences/activity on **2026-10-15**. Source snapshot signals are *not* pinned upstream commits and not package audits; some repositories expose `NOASSERTION` or redirected ownership. **Before integration** record immutable upstream SHA/tag, actual checked root and embedded component licences, full transitive dependency inventory, test coverage, platform/runtime cost, network/offline behavior, and a legal decision when ambiguous.

Source references:
- OPOL https://github.com/open-politics/opol
- Vane https://github.com/ItzCrazyKns/Vane
- FINOS Perspective https://github.com/perspective-dev/perspective
- Presidio transition https://github.com/data-privacy-stack/presidio/blob/main/docs/project_transition.md
- Open WebUI licence https://docs.openwebui.com/license/
- SurveyJS licence https://surveyjs.io/licensing
- PMTiles licence https://github.com/protomaps/PMTiles/blob/main/LICENSE
- Popolo concepts https://www.popoloproject.com/
- OpenStreetMap tiles https://operations.osmfoundation.org/policies/tiles/
- NIST supply chain/SSDF https://csrc.nist.gov/projects/ssdf

**Explicit nonclaim:** this research did not create the GitHub fork; an existing Vane fork was verified. No source code imported, no donor integrated, no donor component legally approved and no '90% reuse' measurement performed by this register.
