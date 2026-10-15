# Dotpol — Practical Fork Queue and Donor Action Plan

**Prepared:** 2026-10-15  
**Status:** Proposed planning guidance; no code imported, licences approved or integrations run.  
**Master inventory:** [All 43 upstream candidates with direct links](DONOR_RESEARCH_2026-10-15.md)  
**Fast-release scope:** [3–7 day first-preview proposal, PR #3](https://github.com/limuria08-hub/Dotpol/pull/3).  
**Architecture:** [Architecture / acceptance PR #1](https://github.com/limuria08-hub/Dotpol/pull/1) and [Vane donor audit](VANE_MODULE_DECISION_MATRIX.md).

## Answer: what the repository owner needs to fork

**Required new forks for the first 3–7-day *research preview*: NONE.**

We have a [real Vane fork](https://github.com/kiranvbiim-coder/Vane), parent [ItzCrazyKns/Vane](https://github.com/ItzCrazyKns/Vane), observed `master` SHA `348feca3e378fb4157b217724ed508dc707f853f`; it has not been integrated. It is under `kiranvbiim-coder`, whereas the product repo is under `limuria08-hub`. **Do not make a duplicate Vane fork only for vanity.** Decide which account will maintain it.

### Fork queue — prioritized by actual value, not fork count

| Priority | Project | Action | When it becomes genuinely useful | What to retain / not duplicate |
|---|---|---|---|---|
| **0 — exists** | [Vane](https://github.com/ItzCrazyKns/Vane) / [our fork](https://github.com/kiranvbiim-coder/Vane) | **Already forked; stop forking** | Phase 3 and selected UI during first research preview *only after component review* | Reuse source/citation/research progress UI as candidates; do not transplant its Drizzle DB, full Next.js API, provider SDKs or bundled SearXNG into Dotpol |
| **1 — optional next fork** | [Kepler.gl](https://github.com/keplergl/kepler.gl) | **Fork only if we commit to a customized Map Lab** | GIS/analyst phase, not first 7 days | Keep one geospatial renderer/layer stack; adapt advanced analyst experience, do not rebuild all maps |
| **2 — conditional fork** | [OPOL](https://github.com/open-politics/opol) | **Read and select modules first; fork only if edits genuinely needed** | Political ingest/entity/classifier pipeline after data contracts | Its multi-service architecture and older upstream do not replace local Python/SQLite foundation; verify MIT claim and bundled services |
| **3 — conditional fork** | [ODK Collect](https://github.com/getodk/collect) | **Prefer official app/interoperability first; fork for branded/offline Android needs only** | Survey/field phase after explicit mobile-app strategy | Do not rebuild mobile forms; do not introduce ODK Central as a required local-first component |
| **4 — conditional fork** | [OpenElections Core](https://github.com/openelections/openelections-core) | **Reference or fork one parser only when relevant** | Election adapters, especially after evaluating Indian official formats | US-specific logic must not become the Dotpol canonical election ontology |
| **5 — optional UI alternative** | [Vercel AI Chatbot](https://github.com/vercel/chatbot) | **Reference first; fork if chosen as the ONE app template** | Only if Vane UI components prove unsuitable and the host dependencies can be removed | Never run competing main chat applications or duplicate persistence/AI gateway |

These are **candidate owner actions**, not instructions to create forks immediately. **One optional next fork at most:** Kepler.gl if the owner wants to prepare the future GIS workspace and accepts that no integration will occur in the first 7 days.

## What NOT to fork: use the existing upstream product

| Wave | Dependency / runtime candidates | Integration tactic |
|---|---|---|
| Initial local shell and AI | [PydanticAI](https://github.com/pydantic/pydantic-ai), [Ollama](https://github.com/ollama/ollama) or [llama.cpp](https://github.com/ggml-org/llama.cpp), [promptfoo](https://github.com/promptfoo/promptfoo) | Integrate published/upstream package or separately configured local runtime; no second provider gateway; no cloud requirement |
| First data and evidence | [Docling](https://github.com/docling-project/docling), [dlt](https://github.com/dlt-hub/dlt), [Splink](https://github.com/moj-analytical-services/splink), [LanceDB](https://github.com/lancedb/lancedb), [Presidio](https://github.com/data-privacy-stack/presidio) | Single platform data/search APIs; include only as soon as a use case requires it; keep model/component licences separate |
| GIS and analytics | [DuckDB](https://github.com/duckdb/duckdb), [Perspective](https://github.com/perspective-dev/perspective), [MapLibre](https://github.com/maplibre/maplibre-gl-js), [deck.gl](https://github.com/visgl/deck.gl), [GeoPandas](https://github.com/geopandas/geopandas), [H3](https://github.com/uber/h3), [PMTiles](https://github.com/protomaps/PMTiles), [Statsmodels](https://github.com/statsmodels/statsmodels) | Dependencies, not forks. H3 is an existing blueprint dependency beyond the 43-candidate shortlist. GIS phase work is not the initial research preview |
| Later surveys/forecast/media | [SurveyJS Form Library](https://github.com/surveyjs/survey-library), [XLSForm pyxform](https://github.com/XLSForm/pyxform), [PyMC](https://github.com/pymc-devs/pymc), [BERTopic](https://github.com/MaartenGr/BERTopic), [Prefect](https://github.com/PrefectHQ/prefect) | Keep owned typed adapters; default to upstream releases/interop |

## Legal and architecture red flags

- **Do not fork into the permissive core without a specific legal decision:** [OpenFisca](https://github.com/openfisca/openfisca-core), [RSSHub](https://github.com/DIYgod/RSSHub), [KoBo KPI](https://github.com/kobotoolbox/kpi) (AGPL); [Open WebUI](https://github.com/open-webui/open-webui) (current special licence/branding terms); Vane's bundled [SearXNG](https://github.com/searxng/searxng) (AGPL).
- [SurveyJS Form Library](https://github.com/surveyjs/survey-library) and paid Survey Creator are distinct products. Use the free runtime as a dependency only; survey authoring remains Dotpol-owned unless separately licensed.
- A public fork is not licence approval; licence text, transitive dependencies, images, binary artifacts, data assets, model weights and attribution all require concrete review **before** copying/redistribution.
- **Don't add unnecessary backend stacks.** Vane, LibreChat and chatbot templates each contain independent app state/provider/server choices. Reuse components and user-interface ideas behind Dotpol's one platform architecture instead of running three competing apps.

## What the owner should do next (in order)

1. **For the 3–7-day preview:** approve the *scope* in PR #3, settle the proposed foundation ownership and licence in PR #1, and approve the selective donor matrix in PR #2. These are the only planning decisions that unblock safe code integration.
2. Keep the existing [Vane fork](https://github.com/kiranvbiim-coder/Vane) accessible and decide its continuing maintainer. Do not fork Vane a second time.
3. **Optional, not required today:** if committing to a future modified Map Lab, sign in to the desired fork owner account and open [Kepler.gl](https://github.com/keplergl/kepler.gl), press **Fork**, select the GitHub account and create the fork. Provide the resulting repository URL; record parent/ref. Keep Kepler out of first sprint runtime.
4. Do **not** fork OPOL, ODK, OpenElections or a chatbot template until we have reviewed a specific code component needing modification.
5. Only start coding after accepted architecture and contract gates; open small single-owner PRs, verify runtime/test evidence, then mark a donor 'integrated' or 'verified'.

## Fork intake form for the maintainer/agents

On a fork URL reply, capture: `parent_repo`, `fork_repo`, `default_branch`, `observed_upstream_sha`, `fork_maintainer`, `target_Dotpol_capability`, `needed_modules`, `licence_component_review`, `integration_status`, `tests`, `upstream_sync_plan`.

Store planned candidates in `architecture/donor-candidates.yml`; only record **observed** fork flags when GitHub confirms a fork. Use `architecture/donors.lock.yml` for actually approved component refs, licences and future adoption checks.

## Stop and resume rules

**Stop donor discovery** unless a named blocking requirement has no viable candidate. The 43 documented options are already ample; evaluating more repos is likely slower than verifying the first vertical slice. **Resume fork assessment** only at its owner roadmap phase or when a benchmark justifies moving from a dependency to an incompatible fork.

**Current facts:** 43 listed candidates, 1 verified fork (Vane), 0 integrated donor components. No new GitHub fork required to start the first research preview.
