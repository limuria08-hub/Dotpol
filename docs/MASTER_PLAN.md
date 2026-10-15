# Dotpol — Master Product & Delivery Plan

**Date:** 2026-10-15 · **Status:** Canonical consolidated planning baseline · **Implementation:** not started

This is the **single short entry point** for planning and execution. Detailed requirements remain in the linked blueprint, contracts and ADRs; they should not be recopied into new plans. Changes to frozen architecture require an accepted ADR.

## 1. Product

**Dotpol is a local-first, internal political-intelligence and election-operations platform.** It replaces disconnected notebooks, spreadsheets and apps with one workspace for research, public election data, mapping, surveys, authorized field operations, evidence-backed analysis and live operational coordination.

**Product rule:** one canonical record and one owning subsystem per capability. Reuse maintained open-source components; write only domain contracts, integration glue and specialist political logic.

**Data boundary:** support lawful, purpose-limited staff/service records, public polling-site information and appropriately aggregated geographic or survey reports. Do not build identifiable voter political-preference profiles, inferred support/turnout scores, electoral-roll enrichment for persuasion or individually targeted political outreach. Internal deployment still needs role-based permissions, source rights, retention and an audit trail.

## 2. Exact technology selection

| One job | Selected technology | One Dotpol owner |
|---|---|---|
| Web application and workspaces | **Next.js**; selectively adapt **Vane** source/citation/progress UI after component review | `apps/web` |
| Local API | **FastAPI** | `services/api` |
| AI agents and tools | **PydanticAI** | `platform/ai` |
| Local model runtime | **Ollama** (no-model mode must still work) | `platform/ai` |
| Projects, assignments, events, source metadata | **SQLite** | `platform/data` |
| Full-text and semantic retrieval | **LanceDB OSS** | `platform/search` |
| Official/public data ingestion | **dlt** | `platform/data` |
| Documents and extraction | **Docling** | `platform/documents` |
| Tabular analytical calculations | **DuckDB** | `platform/analytics` |
| Interactive analytics tables/charts | **Perspective** | `apps/web` |
| One interactive GIS/map workspace | **Kepler.gl** (its internal renderers are not separate Dotpol stacks) | `platform/gis` |
| Spatial joins and geometry | **GeoPandas** | `platform/gis` |
| Statistics | **Statsmodels** | `platform/analytics` |
| Bayesian forecasting | **PyMC** | `domains/forecasting` |
| Web form runtime | **SurveyJS Form Library** (not paid Survey Creator) | `platform/surveys` |
| Offline Android field forms | **ODK Collect** | `platform/surveys` |
| Media topic clustering | **BERTopic** | `domains/media` |
| Personal-data redaction aid | **Presidio** | `platform/data` |
| Durable scheduled work | **Prefect** | `platform/automation` |
| AI regression/security evaluation | **promptfoo** | `evaluations` |

**Not duplicates:** SQLite stores authoritative operational records; DuckDB calculates over analytical datasets; LanceDB indexes searchable content. Each has a different job. No second chat backend, search engine, map app, survey runtime or field database.

**Fork plan:** [Vane is already forked](https://github.com/kiranvbiim-coder/Vane). **No further forks are required now.** Use upstream packages for the other selections; fork only if a reviewed modification truly cannot be made through published APIs. Finalize versions and exact component/asset licences when implementing. See [selected stack](SINGLE_STACK_SELECTION.md), [machine-readable owner list](../architecture/selected_stack.yml) and the [donor audit](DONOR_RESEARCH_2026-10-15.md) for supporting decisions.

## 3. Product workstreams and ownership

| Phase | Deliverable | Exit evidence |
|---|---|---|
| **0 — Decisions** | Approve ownership, core licence, minimal data/evidence contracts and this plan | No contradictory approved architecture |
| **1 — Foundation** | Start web + local API; projects, users/roles, health, model status, CI | New install can create, save and reopen a project |
| **2 — Data** | Source registry, versioned public datasets, polling-station IDs, document imports | Imports can be traced to original source and date |
| **3 — Research** | Search, AI tools, valid citations and saved briefs | User can answer a source-backed query, reject unsupported claims |
| **4 — GIS / analytics** | One map workspace, tables, reproducible calculations, station/microarea geometry | Same data filters and maps without duplicate entities |
| **5 — Elections** | Constituencies, contests, candidates/results, official historical turnout and comparisons | Source-linked deterministic election metrics |
| **6 — Surveys + pre-election field operations** | Forms, approved field assignments, booth/site readiness, offline reports, verified aggregate issue maps | Demonstrate the full field workflow below on allowed test data |
| **7 — Forecasting** | Calibrated models, scenarios, uncertainty and backtesting | Reproducible method/data/version trail |
| **8 — Policy** | Bills, governance, schemes, manifestos and source-linked policy views | Traceable claim-to-document links |
| **9 — Media** | Public-source issue/event collection, topic clustering, monitored reports | Every finding links to sources and methods |
| **10 — Election-day command center** | Live operational status, field incidents, authorized aggregate turnout observations, alerts and supervisor response | Timestamped, verified reports use **the same** records as Phase 6 |
| **11 — Automation** | Scheduled connectors, approvals, monitoring, delivery | Auditable bounded runs and retries |
| **12 — Release** | Tests, permissions, backups, recovery, privacy/licence checks, supported packaging | Independent end-to-end installation and test evidence |

**High-priority integration:** Phase 6 **pre-election field intelligence** is not optional or deferred entirely to Phase 10. Phases 2/4/5 prepare canonical station geography first; Phase 10 builds on the Phase 6 operational records.

## 4. One pre-election-to-polling-day workflow

```text
Approved station/microarea directory
  → supervisor assigns site/field tasks
  → operator completes approved offline form
  → idempotent synchronization / local import
  → reviewer verifies or disputes observation
  → map and preparedness report show sourced area/site aggregates
  → incidents and unresolved tasks continue into election-day command center
```

**Same data model throughout:** `PollingStation`, `BoundaryVersion`, `Microarea` (proposed aggregate unit), `Task`, `FieldUpdate`, `Incident`, `Alert`, `TurnoutObservation`, `Source`, `Evidence` and `SyncReceipt` (proposed). `domains/fieldops` owns assignments and site observations; `domains/warroom` composes them. GIS, forms, provenance and analytics retain their existing single owners.

**Reporting rules:** label information `official`, `field-unverified`, `field-verified`, `derived`, `disputed` or `outdated` with observed/received time. Distinguish **approximate official turnout updates**, **statutory Form 17C records when legitimately available**, and **unofficial field observations**. Never imply a per-booth official live feed exists without a verified permitted source.

**Acceptance use cases:**

| ID | What must work |
|---|---|
| F1 | Import approved station list; reconcile duplicates and boundary versions |
| F2 | Assign site accessibility/facilities inspections with scoped operator roles |
| F3 | Collect offline, retry upload and create exactly one submission |
| F4 | Preserve conflicting observations and the supervisor review trail |
| F5 | Map verified site conditions and sufficiently aggregated local issues; suppress identifying survey slices |
| F6 | Open election-day site status/incident view from the **same** station records |
| F7 | Show official/field turnout numbers with source, timestamp, finality and discrepancies |
| F8 | Export a dated preparedness/incident brief with unresolved issues, gaps and evidence |

**India-specific roles:** Dotpol field operators are not automatically ECI Booth Level Officers, party Booth Level Agents or accredited polling agents. Deployment and data collection must use authorized roles and election-period rules. Sensitive contact/service cases, if approved, stay purpose-limited and separate from political analytics.

## 5. Delivery order

**First 3–7 days target: a verified research preview, not the entire platform.** Start with Next.js, FastAPI, SQLite, PydanticAI/Ollama, one retrieval index, import/search/citations and a saved project. Add only the Vane UI modules that pass review. No fake proof of completion.

**Next vertical slice:** canonical station directory → supervisor assignment → one ODK offline facility form → verified status map → incident carryover. This is the first test of the **core field idea**; scale only after offline/security/privacy and role tests pass.

**Later:** full election, GIS, survey, forecasting, policy/media, live war room and automation phases use the same data/contracts rather than separate apps.

**Do not defer:** evidence IDs, access rules, provenance, no-network mode, sync idempotency and reproducible tests. **Do defer:** decorative features, extra donors, alternative frameworks, unused engines and unrelated forks.

## 6. Definition of done and immediate actions

A capability is **done** only when its code is integrated, tests pass, local install works, source/licence records exist and a real end-to-end use case passes. Documentation or a GitHub fork is **not** implementation.

1. Follow accepted planning decisions [ADR-0001](DECISIONS/0001-foundation-module-ownership.md), [ADR-0002](DECISIONS/0002-one-stack-per-capability.md) and [ADR-0003](DECISIONS/0003-pre-election-microarea-operations.md); exact licenses, source permissions and component versions require review before code import.
2. Use the [3–7-day preview execution checklist](RAPID_REUSE_SPRINT.md) and [MVP acceptance journeys](PRODUCT_MVP_AND_ACCEPTANCE.md); start only the selected first-release components.
3. Prepare lawful [field F1–F8 tests](PRE_ELECTION_MICROAREA_INTELLIGENCE.md) after the foundation and canonical station data exist.
4. Open small coding PRs for foundation, data/research and web, then the field slice; require passing local and CI evidence before marking work complete.

### Documentation ownership

- **This file:** product priorities, selected technologies, phased delivery and completion criteria.
- [Blueprint](BLUEPRINT.md) and [architecture](ARCHITECTURE.md): constraints and accepted structural decisions.
- [Roadmap](ROADMAP.md): detailed phase gates and dependencies.
- [Domain model](DOMAIN_MODEL.md) and [capability registry](CAPABILITY_REGISTRY.md): identifiers, source-of-truth and owners.
- [Field specification](PRE_ELECTION_MICROAREA_INTELLIGENCE.md): concise operational contracts and test cases.
- [ADRs](DECISIONS/README.md): changes requiring approval.
- Other donor/feasibility/audit documents: **supporting evidence only**, not parallel product plans.

**No new product stack, code or feature is implemented by this plan.**
