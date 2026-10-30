# Dotpol — Master Product & Delivery Plan

**Updated:** 2026-10-30 · **Status:** Five-phase canonical execution plan · **Implementation:** P1 application work is in open PR #11; phases remain unverified until acceptance tests pass

This is the **single short entry point** for planning and execution. Detailed requirements remain in the linked blueprint, contracts and ADRs; they should not be recopied into new plans. Changes to frozen architecture require an accepted ADR.

## 1. Product

**LiOS.Pol (Dotpol repository) is a local-first, AI-native political-intelligence, public-policy and election-operations platform.** It replaces disconnected notebooks, spreadsheets and apps with one workspace for research, public election data, mapping, surveys, authorized field operations, evidence-backed analysis and live operational coordination.

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

### Full-repository reuse without a second product

Use the full capabilities of an external repo **through its supported APIs** where that is safer/faster than copying its application. This is our reuse policy, not a plan to merge many independent backends. [Detailed steps and agent owners](ROADMAP.md).

| Full OSS service | Intended phase | Responsibility | Integration boundary |
|---|---|---|---|
| **ODK Collect / Central** | P2 field pilot and P4 rollout | Offline field forms/submission workflows | Optional independent service with IDs mapped to canonical Dotpol records |
| **OpenClaw** [upstream gateway](https://github.com/openclaw/openclaw) | P1 integration contract, P4 authorized field/team channels, P5 full acceptance | **Required full gateway integration**: channel messaging (Telegram/WhatsApp), skills, approved device nodes, automation and operation feedback | Install/run maintained OpenClaw with local control plane. Version pin, pairing, sandbox and permission contract required; Dotpol's PydanticAI, political records and UI remain canonical. **Not optional for a complete release.** |
| **Ollama** | P1 optional | Local model inference | User-managed loopback provider; no bundled model/cloud requirement |

**OpenClaw is the only mandatory full external open-source runtime in this integration plan.** The inspected OpenClaw root is MIT; exact release, channel/plugin licences, gateway security, device pairing and local model/resource costs must be audited. It must be available as part of the supported install, not offered as a later optional extra. No extra file-service platform is in scope.

**Not duplicates:** SQLite stores authoritative operational records; DuckDB calculates over analytical datasets; LanceDB indexes searchable content. Each has a different job. No second chat backend, search engine, map app, survey runtime or field database.

**Fork plan:** [Vane is already forked](https://github.com/kiranvbiim-coder/Vane). **No further forks are required now.** Use upstream packages for the other selections; fork only if a reviewed modification truly cannot be made through published APIs. Finalize versions and exact component/asset licences when implementing. See [selected stack](SINGLE_STACK_SELECTION.md), [machine-readable owner list](../architecture/selected_stack.yml) and the [donor audit](DONOR_RESEARCH_2026-10-15.md) for supporting decisions.

## 3. Five-phase execution plan (the ONLY top-level phases)

The previous milestones numbered 0–12 remain **technical work packages and acceptance criteria**, not 13 competing execution phases. Their numbering is preserved in older specifications and ADRs for traceability. [Five-phase roadmap](ROADMAP.md) contains the integrated checklist and phase gates.

| Execution phase | Includes former milestones | Scope | Exit evidence |
|---|---|---|---|
| **P1 — Foundation, AI and evidence-backed research** | 0, 1, 2, 3 | Architecture decisions, Next.js/FastAPI, local projects, authentication baseline, political ontology, ingestion, documents, local AI/BYOAI, retrieval, citations and saved artifacts | Clean local install; user imports public/synthetic data, asks a sourced question and reopens the project; works without paid services |
| **P2 — Political data, election analytics, GIS and surveys** | 4, 5, 6 | Kepler/GeoPandas, DuckDB/Perspective, Statsmodels, versioned constituency and polling-site geometry, historical results, sampling, weighting, SurveyJS and ODK offline field pilot | One traceable dataset drives map, table, statistical analysis, survey and F1–F5 field pilot |
| **P3 — Policy, media and advanced intelligence** | 7, 8, 9 | Reproducible simulation and calibration, public policy, governance, manifestos, legislation, media, narrative/event analysis and cited publications | Verified research workflows with source/version/uncertainty, no invented results |
| **P4 — Hierarchical teams, secure OpenClaw communications and election operations** | 10; operational continuation of 6 | Authorized OpenClaw team/channel integration; recursive admin/supervisor/sub-team hierarchy, scoped permissions, mobile tasks/reports, sync, incident verification, aggregate authorized turnout observations and command centre | 1 admin → 3 coordinators → 10+ scoped staff scenario; offline retries, revocation, incident escalation and F6–F8 accepted |
| **P5 — Required OpenClaw, automations, security and release** | 11, 12 | Required sandboxed OpenClaw gateway, channel/device flows, monitoring, plugin manifests, opt-in isolated services, security, backups, tests, licence inventory, performance and docs | Independently reproducible local and optional shared-mode installs; supported release gates pass |

**Scope invariant:** All political research, elections, psephology, GIS, statistics, policy, legislation, manifestos, public participation (optional), media, simulations, reporting, multilingual tooling, and hierarchical field operations remain in the complete vision. No individual inferred political-preference or persuasion targeting.

**Three-day integration sprint:** a *target for P1 vertical slice plus one narrow P2 election-data/table/map spike if ready*, **not** full completion of five phases. A demonstrated fork or a dashboard mock is not a working product.

**Parallel lanes after typed contracts are agreed:** (A) core/auth/data/provenance, (B) research/AI and artifacts, (C) GIS/analytics/political domain, (D) field teams, (E) release/evaluation. Only the owning lane edits a shared capability.

### Approved reuse and isolation principle

- **Embed** libraries through one Dotpol-owned interface (DuckDB, Kepler.gl, GeoPandas, Perspective, Statsmodels, SurveyJS Form Library).
- **Connect** optional independent services through APIs (user-managed Ollama, ODK Central if necessary, future notification/participation tools). Use Docker Compose initially; K3s only for installations that need an orchestrator.
- **Selectively adapt** donor code only after exact version/component licences and compatibility tests (Vane UI already forked; OPOL and Indian election parsers are candidates only).
- **Reference** full external products rather than wholesale merge competing applications (Open Politics HQ, OpenStates/Popolo, Decidim/Polis/Ushahidi).
- Do not create unused forks, extra retrieval systems, duplicate election/field schemas, parallel databases for authoritative records, or competing chat/agent/GIS engines.

### Hierarchical collaboration model

One organisation may contain arbitrary-depth parent/child teams, subject to configured depth/size limits. Administrators delegate only powers they hold; leaders can create permitted child teams. All users and mobile clients use the **same** canonical Project, Team, Membership, RoleGrant, Task, FieldUpdate, Incident, Evidence and event schemas. Reports roll up according to scope; sensitive records do not become visible simply because a team is an ancestor. Authoritative team mode uses PostgreSQL behind the same storage contracts used by local SQLite. Sync must be idempotent, offline-capable, time-stamped, reviewed and revocable. An optional real-time event transport cannot become the source of truth.

### Donor gating

The selected base stack remains [ADR-0002](DECISIONS/0002-one-stack-per-capability.md). Newly researched projects belong in [donor candidates](../architecture/donor-candidates.yml), **not** in the adopted dependencies until a scoped ADR, exact commit, full component/model/data-licence review, performance evidence and end-to-end acceptance. See [ADR-0004](DECISIONS/0004-five-phase-execution-and-service-isolation.md).

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

**First three days are an ambitious integration-sprint target for a verified research preview, not the entire platform.** Start with Next.js, FastAPI, SQLite, PydanticAI/Ollama, one retrieval index, import/search/citations and a saved project. Add only the Vane UI modules that pass review. No fake proof of completion.

**Next vertical slice (P2 field pilot):** canonical station directory → supervisor assignment → one ODK offline facility form → verified status map → incident carryover. This is the first test of the **core field idea**; scale only after offline/security/privacy and role tests pass.

**Later:** P2–P5 add elections, GIS, surveys, forecasting, policy/media, authorized team collaboration, command centre and required OpenClaw-based communications and automations behind the same data/contracts.

**Do not defer:** evidence IDs, access rules, provenance, no-network mode, sync idempotency and reproducible tests. **Do defer:** decorative features, extra donors, alternative frameworks, unused engines and unrelated forks.

## 6. Definition of done and immediate actions

A capability is **done** only when its code is integrated, tests pass, local install works, source/licence records exist and a real end-to-end use case passes. Documentation or a GitHub fork is **not** implementation.

1. Follow accepted planning decisions [ADR-0001](DECISIONS/0001-foundation-module-ownership.md), [ADR-0002](DECISIONS/0002-one-stack-per-capability.md) and [ADR-0003](DECISIONS/0003-pre-election-microarea-operations.md); exact licenses, source permissions and component versions require review before code import.
2. Work from the [five-phase agent checklist](ROADMAP.md), [machine-readable execution gates](../architecture/execution-plan.yml) and [MVP acceptance journeys](PRODUCT_MVP_AND_ACCEPTANCE.md); do not restart P1 PR #11. The older [rapid reuse sprint](RAPID_REUSE_SPRINT.md) is historical guidance, not a parallel master plan.
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
