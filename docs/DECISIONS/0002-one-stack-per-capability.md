# ADR-0002: Single selected integration engine per capability

- **Status:** Proposed — not accepted / not implemented
- **Date:** 2026-10-15
- **Drivers:** User preference for speed, no alternatives per job, minimal forks, one owner and a 3–7-day first-preview target
- **Linked selection:** [Selected stack](../SINGLE_STACK_SELECTION.md), [machine-readable selection](../../architecture/selected_stack.yml)
- **Supersedes:** No accepted ADR. This proposal must be reconciled with [Blueprint v1.0](../BLUEPRINT.md) and pending ADR-0001 before code changes.

## Context

The existing blueprint has 13 phases and one owner per capability, but the 43-candidate donor research list and architecture descriptions expose several overlapping application-level technologies. Without a narrow selection, independent agents may each build one AI router, chat shell, search/RAG index, map renderer or charting subsystem. Fork count is not an integration metric.

## Proposed decision

- **Primary web UI:** one Next.js/React application, selectively adapting approved Vane source/citation/progress UI components only; Vane's server/tool runtime is not a second platform.
- **Agent + inference:** one PydanticAI tool runtime and one local Ollama server (user-managed/no-key non-AI path).
- **State / analytics / retrieval:** SQLite for authoritative operational metadata, DuckDB solely for analytical SQL, LanceDB OSS solely for full-text/vector/hybrid retrieval. No parallel retrieval index, agent memory store or shadow political ontology.
- **Document ingestion:** Docling and dlt each do only their assigned parsing/ingestion work, introduced after the foundational preview.
- **GIS:** **one top-level map workspace using Kepler.gl embedded components.** Kepler's MapLibre and deck.gl dependencies are internal to the selected map product; do not integrate a second independently owned MapLibre/deck.gl application. GeoPandas remains backend spatial geometry computation. This is an intentional **proposed** change from `docs/ARCHITECTURE.md` section 11 where separate core maps and Kepler Map Lab coexisted, and thus requires acceptance before implementation.
- **Analytical UI:** Perspective only, not a parallel charting framework; Statsmodels classical statistics and PyMC Bayesian forecasts are different mathematical responsibilities.
- **Surveys:** SurveyJS MIT Form Library for web rendering; ODK Collect only for separately scoped offline Android collection, sharing a single Dotpol survey schema. Do not add paid SurveyJS Creator under an open-source assumption.
- **Later domain engines:** BERTopic for topic grouping; Prefect for durable scheduling, Presidio as PII helper and promptfoo for AI evaluation.

## Considerations

1. **Forks:** no new fork required now. Existing `kiranvbiim-coder/Vane` is for selected UI component adaptation if legal/technical reviews pass. Kepler should be embedded as maintained upstream package before deciding whether a fork is justified by actual modifications.
2. **3–7-day path:** only Next.js, FastAPI, SQLite, PydanticAI, Ollama if installed, LanceDB and bounded local document imports. Vane components only if approved/fit. No GIS, analytics workbench, automations or forecasting installed on day one.
3. **MapLibre token/tiles:** Kepler upstream uses MapLibre/deck.gl, but tokenless operation still requires an allowed self-hosted or appropriately licensed basemap. Upstream examples show token-free configurations; do not assume all defaults work without Mapbox credentials.
4. **Retrieval versioning:** record source/evidence IDs in indexed hits; allow text-first FTS without an embedding model. Validate LanceDB import/runtime overhead on the supported OS; if it proves blocking, an ADR must replace—not duplicate—search engine ownership.
5. **Politically specific semantics:** canonical elections/constituencies/policy/source evidence models remain Dotpol-owned, with no extra political data backend. Existing libs handle commodity mechanics.

## Consequences and acceptance

Positive: narrower runtime, fewer maintenance branches, one provider surface per feature, faster integration. Risks: Kepler React/Redux embedding cost; LanceDB installation/embedding complexity; permissive component/asset review; incomplete free form authoring. These require bounded experiments and owners before adoption.

**Conditions for acceptance:**
- [ ] Maintainer signs off the selection and map simplification.
- [ ] Architecture paths/registry and Phase 1 examples align with accepted ADR-0001.
- [ ] Component-level licences (especially Vane, Kepler tiles, ODK) reviewed and pinned.
- [ ] Demonstrate no-network/no-paid-key local research with one retrieval index and stable citations.
- [ ] Later-phase technologies remain uninstalled until used.
- [ ] Recorded acceptance criteria ensure 3–7-day preview is not mislabeled entire OS complete.

**Until these conditions are accepted, this is a proposed plan, not an implementation or released architecture.**
