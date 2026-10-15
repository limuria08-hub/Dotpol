# Dotpol OSS Reuse, Fork and Integration Playbook

**Current implementation choice:** [one canonical stack](SINGLE_STACK_SELECTION.md) and [selected_stack.yml](../architecture/selected_stack.yml). Candidate comparisons below are research, not authorization for multiple engines.

**Status:** Proposed architecture/engineering review (2026-10-15); planning only.  
**Companions:** `docs/DONOR_RESEARCH_2026-10-15.md`, `architecture/donor-candidates.yml`, `docs/DONOR_MATRIX.md`, `architecture/donors.lock.yml`.

## Purpose and 90% reuse ambition

Aim to **reuse around 90% of commodity functionality** where licensing, maintenance, deployment and architecture fit allow. This is an **ambition, not a verified metric or quota to justify unsafe copying**. Original work will remain necessary for Dotpol's canonical political ontology, evidence/provenance, jurisdiction-specific contracts, reproducible methodology, integrations, trustworthy domain engines and specialized user journeys.

**Prefer existing upstream code whenever viable.** Reuse can be:
1. **Native dependency**: use existing maintained library through a Dotpol-owned interface.
2. **Local interoperability / sidecar / user's own tool**: communicate over documented files/APIs; keep licensed or heavyweight runtime outside permissive Dotpol core.
3. **Selective assimilation**: copy only scoped permissive modules after code-level review, notice preservation and acceptance tests.
4. **Maintained fork**: own incompatible modifications to a donor with named maintainer, updates, CI and clearly scoped work.
5. **Reference**: learn interface, tests or algorithms; write necessary Dotpol-owned domain glue, not clone competing application architecture.

Use the first appropriate category in that order. Adding a framework to skip a few hundred lines of glue is not always lower total cost.

## Adoption decision flow

```text
Need / accepted user journey
 -> existing capability ID and owner?
 -> existing Dotpol implementation? extend it
 -> exact OSS candidate(s) and licence/component screen
 -> does an upstream dependency solve it? use wrapper
 -> does documented local interface solve it? interoperate
 -> is substantial modification unavoidable? selective donor/fork with ADR as needed
 -> else build the smallest original Dotpol business-specific glue
 -> tests + provenance + local/no-key checks + security + notices
 -> approve + integrate + verify + mark released when shipped
```

### Pre-adoption scorecard (record evidence, don't invent score)

A reviewer should evaluate:
- functional fit to the **accepted user journey** (required vs nice-to-have);
- API stability / change history, maintainer activity and security advisories;
- actual source and transitive licence compatibility, plus model/data/tile rights;
- ability to work offline, locally and at ₹0 mandatory software/API cost;
- dependencies introduced (other DBs, search services, cloud services, runtimes);
- provider/identity/schema isolation: one capability, one owner;
- compute/memory/storage and supported OS footprint;
- isolation/security, input validation, remote telemetry and data access;
- accessibility and internationalisation requirements;
- upstream upgrade and future fork-maintenance effort;
- tests, benchmarks, citations/provenance and verified output differences.

**Blockers:** unclear/unreviewed embedded licence; mandatory paid cloud/API; new competing data/agent/search stack; unsafe client-side access to privileged files; private data routed externally without explicit approval; unresolvable deployment prerequisites; lost source/provenance lineage.

### Fork approval contract

Before creating a **maintained** fork, document:

```text
capability_id:
upstream_repo:
upstream_tag_or_sha:
upstream_root_and_subcomponent_licences:
reason dependency / adapter is insufficient:
files/modules to reuse/change:
Dotpol single capability owner:
destination_account/repo:
target branch strategy:
notice/third-party rights:
local-mode and no-network test:
security/data review:
integration seam (input/output contracts):
maintenance owner / upstream sync plan:
size budget / runtime impact:
estimated acceptance test / evaluator:
ADR reference if architectural:
```

Forks must be created under approved owner `limuria08-hub` **only if the maintainer has authority**. The fork is not integration evidence. Do not fork all 43 candidates. Keep upstream branch tracked, pin base SHA, preserve notices, use targeted cherry-picks and run Dotpol's integration tests on updates.

## 90% target: measurable evaluation

Define a **commodity capability coverage** metric once there is code and approved scope:

`reused_verified_weight / all_verified_commodity_capability_weight`

Where the weights are estimated by product/engineering owners **before** adoption and correspond to one independently testable commodity acceptance capability (parsing, mapping, charting, form runtime, etc.). Count it as reused only if an actual third-party dependency/interop/adapted module passes Dotpol's acceptance suite. Do **not** count merely forked code, documentation, downloaded repositories or copied lines that cannot run.

Track separately:
- `reuse_coverage`: accepted commodity work fulfilled primarily by upstream functionality;
- `adaptation_effort`: Dotpol-maintained code, security, tests and notices for wrapping it;
- `fork_maintenance_burden`: open patches and upstream update lag;
- `original_domain_value`: political schemas, rules and workflows owned by Dotpol;
- `duplicate_engine_count`: must be zero in production.

Do not use a LOC-only percentage, because generated/vendor code inflates it and may conceal duplicate systems. Revisit the 90% target if it damages licence compliance, privacy, local-first performance or correctness.

## Recommended waves (phase-aligned, no premature installation)

| Wave | Phases | Candidate focus | What counts as success |
|---|---|---|---|
| F0 planning | 0 | source audit, donor shortlist, licence/ADR, canonical paths | reviewed decisions, candidates not integrated |
| F1 local spine | 1 | FastAPI, PydanticAI, optional Ollama/llama.cpp, promptfoo | one gateway/agent/test path; no-key and no-web boot |
| F2 data/research | 2–3 | dlt, Docling, Splink, LanceDB, OPOL patterns, Vane evaluated modules | one source-aware imported document/dataset and correct citation |
| F3 geo/analysis/elections | 4–5 | DuckDB, Perspective, MapLibre, deck.gl, H3, GeoPandas, PMTiles, Kepler, OpenElections references | canonical election dataset drives one testable map/chart/metric |
| F4 verticals | 6–9 | SurveyJS, XLSForm/ODK, Statsmodels, PyMC, BERTopic, official policy connectors | governed, validated vertical flows without duplicate engines |
| F5 coordination/release | 10–12 | Prefect, privacy/security/observability tools, connector SDK | reliable audited local product and optional team mode |

## Priority evaluation PRs — not code integrations

1. `donor-eval: PydanticAI vs local provider seam` — use existing chosen framework, confirm one AI model/tool interface and valid no-key start.
2. `donor-eval: Docling/dlt input contract` — compare bounded import of approved public/sample records and parser output formats.
3. `donor-eval: Vane search components and AGPL boundary` — map concrete permissive modules vs bundled SearXNG dependencies and cost of extraction.
4. `donor-eval: OPOL module audit` — find valuable political entity/ingestion modules; assess stale upstream and runtime fit; avoid wholesale import.
5. `donor-eval: Splink vs dedupe` — use same synthetic/matched fixtures; choose one if relevant.
6. `donor-eval: Kepler Map Lab` — delay until approved Phase 4 contracts; compare embedding, theming, data APIs and local tile access.

These are comparison/planning proposals; they do not authorize installing dependencies in the foundation.

## Existing verified fork status (2026-10-15)

One targeted donor fork **already exists**: [kiranvbiim-coder/Vane](https://github.com/kiranvbiim-coder/Vane), from [ItzCrazyKns/Vane](https://github.com/ItzCrazyKns/Vane). Fork and upstream `master` SHAs both observed as `348feca3e378fb4157b217724ed508dc707f853f`. It was created under `kiranvbiim-coder`, **not** the `limuria08-hub` Dotpol owner. The fork is not yet integrated or component-licence approved. See [Vane evaluation](DONOR_EVAL_VANE.md) and [source-level adoption matrix](VANE_MODULE_DECISION_MATRIX.md).

Do **not** create a duplicate Vane fork until maintainers decide to move ownership or maintain a deliberately separate fork. Use the existing fork for source review without changing its code. The GitHub connector used here can update GitHub issues/PRs/docs but does not expose a new-repository fork action.

## GitHub forking: user action when approved

The current connected GitHub operations can read repositories and create branches/files/issues/PRs in Dotpol, but **do not provide a repository-fork action**. A repository owner can create a fork from their own GitHub UI:

1. Sign in to GitHub as `limuria08-hub`.
2. Open an *approved future* donor upstream, e.g. https://github.com/keplergl/kepler.gl when that phase arrives. Vane is already forked; do not repeat it.
3. Select **Fork**, choose the explicitly approved fork owner, and retain link to upstream; create the fork.
4. Share the new fork URL with collaborators; record exact upstream SHA, licence and reason in the acceptance record *before* any assimilation.
5. Fork Kepler only when Phase 4 modifications have been approved. Don't fork OPOL merely because a repo exists.

Optional GitHub CLI for **future** approved donors: `gh repo fork <upstream-owner>/<repository> --clone=false` (replace placeholders). Confirm authentication and destination first. **Do not rerun this for Vane**. No access tokens need to be sent through chat.

## Donor acceptance status model

- `candidate`: identified, metadata only.
- `screened`: upstream + dependency licences, maintenance and fit reviewed.
- `approved`: exact ref, security/architecture and owner formally accepted.
- `forked`: optional GitHub copy exists; may still be unused.
- `integrated`: actual Dotpol code uses the approved module/adapter.
- `verified`: compatibility, no-cloud/local, legal attribution, negative tests and end-to-end evidence pass.
- `released`: included in a documented supported product version.

A candidate/fork never jumps straight to verified/released. A fork's status is orthogonal to integration: it may be forked but not integrated.

## Repository bookkeeping

- **Research pool:** `architecture/donor-candidates.yml`.
- **Technical and legal acceptance:** reviewed PR plus module acceptance card.
- **Adoption lock:** `architecture/donors.lock.yml` exact refs and licence verification states, updated **only** with true outcomes.
- **Licence obligations:** `THIRD_PARTY_NOTICES.md` after actual code assimilation; root `LICENSE` after maintainer decision.
- **Capability ownership:** `architecture/capabilities.yml` and `docs/CAPABILITY_REGISTRY.md` remain the one-owner source of truth.
- **Any architectural change:** ADR under `docs/DECISIONS/`.

**No new code or forks are created by this document.** 
