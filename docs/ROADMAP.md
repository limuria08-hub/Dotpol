# LiOS.Pol — Five-Phase Build and Integration Roadmap

**Canonical execution checklist · Updated 2026-10-30 · Implementation status is evidence-based, not inferred.**

**Use this roadmap to assign work.** [Master Plan](MASTER_PLAN.md) defines product and architecture, [execution-plan.yml](../architecture/execution-plan.yml) gives machine-readable gates, [AGENTS.md](../AGENTS.md) defines agent rules, and [donor registry](../architecture/donor-candidates.yml) tracks unapproved OSS candidates. The previous milestones 0–12 are preserved only in [archived technical requirements](archive/LEGACY_MILESTONES_0-12.md). **There are five execution phases, not thirteen.**

## 0. One product, one codebase, reuse full upstream capabilities

**Product repository:** `limuria08-hub/Dotpol`. Maintain one Next.js UI, one FastAPI gateway, one PydanticAI tool/model gateway, one canonical political data model and one evidence/artifact store. Local SQLite stores operational truth; DuckDB calculates analytics; LanceDB indexes retrieval; team PostgreSQL is a later storage adapter.

| Adoption mode | What to do | Examples | Rule |
|---|---|---|---|
| **Use upstream package** | Install and pin library; expose one owned adapter | Next.js, FastAPI, PydanticAI, LanceDB, Docling, DuckDB, Perspective, Kepler, GeoPandas, Statsmodels, SurveyJS, shadcn/Radix, assistant-ui | No source fork for normal use |
| **Use full external service** | Deploy separately and integrate API/auth/event contracts | **required OpenClaw gateway**, ODK Central where needed, user-managed Ollama and optional notification/civic services | No duplicate frontend/backend or databases inside Dotpol |
| **Selective assimilation** | Copy only reviewed modules with copyright notices, test and upstream pin | Existing Vane fork, India-election parsers, selected OPOL routines | Do not bulk-merge the whole donor app |
| **Reference only** | Learn design/contracts, import **no** source code without separate approval | Open Politics HQ, full civic apps and unrelated backend frameworks | Don't introduce competing stacks |

**OpenClaw is REQUIRED for the completed LiOS.Pol product**, not an optional gateway. Reuse the full maintained `openclaw/openclaw` local agent/channel/device/skills system through supported interfaces. Adopt its authenticated WebSocket gateway and CLI rather than copying the complete application. P1 proves gateway lifecycle/readiness and safe contracts; P4 brings authorized team/channel workflows; P5 verifies full integration. OpenClaw does not displace PydanticAI's evidence-grounded political research or Dotpol's canonical records. Do not add any unrelated file-collaboration donor, adapter or runtime.

### Permanent agent lanes and ownership

| Lane | Agent | Owns | Rule |
|---|---|---|---|
| **A** | Platform | API, identity, SQLite/PostgreSQL contracts, data/evidence, sync | Canonical records and API only |
| **B** | AI & research | PydanticAI, tools, LanceDB, model adapters, evals | No second model/agent gateway |
| **C** | Analytics & GIS | DuckDB, Perspective, GeoPandas/Kepler, Statsmodels/PyMC | Deterministic engines own numbers |
| **D** | Political intelligence | ECI/data.gov.in connectors, entities, elections, policy, legislation, media | One canonical domain ontology |
| **E** | UX & field apps | Next.js shell, chat/workbench, mobile, SurveyJS forms, team views | One UI component owner; reuse approved OSS |
| **F** | Integration/QA | donor assessments, CI, licensing, security, performance, releases | Acceptance evidence before "done" |

Agents may work concurrently only after shared contracts have an owning reviewer. **One work package = one scoped PR** where practical. Reuse current P1 [PR #11](https://github.com/limuria08-hub/Dotpol/pull/11); do not scaffold a competing implementation.

## Phase 1 — AI-native foundation, evidence and unified UI
**Epic:** [#6](https://github.com/limuria08-hub/Dotpol/issues/6) · **Former milestones:** 0–3 · **Owners:** A, B, E, F.  
**Goal:** local, source-backed AI research working through a real chat/workbench with persisted artifacts. **Current evidence:** PR #11 is open; component implementation exists on the branch, full acceptance remains unverified.

- [ ] **P1.01 · A/F — Baseline:** review PR #11, reconcile with main, verify build/test, existing code ownership, and explicit architecture/license decisions; do not re-scaffold.
- [ ] **P1.02 · A — Local gateway/storage:** FastAPI, SQLite migrations, projects, source records, stable artifact IDs, backups and restart recovery.
- [ ] **P1.03 · A/D — Evidence/data:** provenance, SHA-256/content hashes, timestamps, source rights, TXT/CSV/JSON import; Docling PDF and document pipeline behind the same owned interface.
- [ ] **P1.04 · B — Retrieval:** LanceDB local full-text **and tested hybrid/vector where available**, project scoping, withdrawal, line/row hashes, no-evidence and rebuild tests. Never advertise hybrid until verified.
- [ ] **P1.05 · B — AI/model gateway:** PydanticAI, optional loopback Ollama with a **real inference** test, optional BYOAI with per-request evidence consent, secrets handling and no-model path.
- [ ] **P1.06 · B/A — Tool contracts:** typed source/search/document tools, tool IDs, permissions, provenance, cancellation/failure modes; no AI calculation or unapproved network/file action.
- [ ] **P1.07 · B/D — Deep research:** search → verify → compare → synthesize → source-linked brief; claim/citation mismatch and hostile-document tests.
- [ ] **P1.08 · E — OSS UI:** shadcn/Radix-style components, assistant-ui custom adapter *only if compatible*, Lucide, responsive single shell and accessible keyboard controls. Vane UI is a nonduplicate, reviewed donor only.
- [ ] **P1.09 · E/A — Artifact continuum:** ask in chat → preview tool output → open same saved Artifact ID in resizable Workbench → revise/export/reopen; no JSON-only user experience.
- [ ] **P1.10 · A/D — Political ID groundwork:** canonical project/source/election/party/constituency/person/jurisdiction IDs and source/version contracts; no premature national dataset import.
- [ ] **P1.11 · A/B/F — Required OpenClaw foundation:** establish the native OpenClaw gateway lifecycle/health contract, local executable/daemon discovery, secure channel-agent adapter, permission requirements and a real local readiness test. Do not add a competing AI gateway or store; P5 completes channels, skills, devices and automation.
- [ ] **P1.12 · F — Exit gate:** clean install and browser E2E, exact citations, provider refusal/consent, no-key/no-network mode, accessibility, source/license notices and verified CI.

**Done when:** fresh checkout on a declared OS imports actual permitted source data, invokes configured local AI, produces verifiable cited output, opens/edits/reopens an artifact, and works in explicit evidence-only mode without a model. Do not call a mocked model test "live inference".

## Phase 2 — Elections, GIS, statistics, psephology and surveys
**Epic:** [#7](https://github.com/limuria08-hub/Dotpol/issues/7) · **Former milestones:** 4–6 · **Owners:** C, D, E (A/B provide contracts).

- [ ] **P2.01 · D — Ingest verified election results:** official ECI/public datasets; validate permitted Indian parser and DataMeet material with source dates, rights and provenance.
- [ ] **P2.02 · D/A — Canonical entities:** Election, Contest, Constituency, BoundaryVersion, Candidate, Party, Alliance, Result and PollingStation linked without duplicate models.
- [ ] **P2.03 · D/C — Reconcile:** delimitation/time-valid boundaries, changed party names, missing data, totals, anomalous records, official/derived/field flags.
- [ ] **P2.04 · C — Deterministic election math:** turnout, vote shares, margins, historical comparisons, descriptive swings; reference fixtures and error bounds.
- [ ] **P2.05 · C/E — Analytical workbench:** DuckDB SQL and FINOS Perspective as the shared table/pivot/chart engine; editable query and sourced exports.
- [ ] **P2.06 · C/E — Map Lab:** **one** Kepler.gl surface, GeoPandas joins and reusable boundary layers; licensed/local basemap handling.
- [ ] **P2.07 · C — Statistical lab:** Statsmodels tests/regression/time series, survey uncertainty and diagnostics; assumptions visible.
- [ ] **P2.08 · C/E — Psephology/Survey Studio:** methods, sample design, weighting, cross-tabs, confidence intervals, SurveyJS Form Library (not paid Creator).
- [ ] **P2.09 · E/A — Field research pilot:** ODK Collect offline or approved interoperable form flow, verified station directory and F1–F5; ODK Central remains optional API service.
- [ ] **P2.10 · B/C/E — AI analyst tools:** natural language → typed election/GIS/statistics/survey tool → reproducible map/table/artifact; model never invents numbers.
- [ ] **P2.11 · F — Exit gate:** one versioned dataset produces matching results across chat, statistical workbench, GIS, saved report and approved F1–F5 field pilot.

**Done when:** the same source/versioned election dataset produces auditable tables, maps, statistical findings and cited AI interpretations, with correct boundary dates and survey limitations.

### P2.01 implementation slice — normalized candidate results (stacked on P1)

**Branch:** `feat/p2-01-election-results-import-20261030`. **Owner:** Agent D + A for source/identity contracts; Agent F for tests. This initial import **does not satisfy full P2.01 official source verification, P2.02 candidate entity resolution, P2.03 delimitation reconciliation or P2.11 exit.** Completion remains unchecked until official datasets/rights and integration acceptance are verified.

1. Import a CSV as an existing P1 project source; original bytes are represented by its canonical source content and SHA-256. To avoid claiming official ECI support, normalize reviewed source columns explicitly to this fixed v1 schema:
   `election,year,constituency,boundary_version,candidate,party,votes,total_valid_votes`.
2. Invoke `POST /api/projects/{project_id}/election-results/import` with `{"source_id":"<existing-project-source-id>"}`. Get import details at `GET /api/projects/{project_id}/election-results/imports/{import_id}`.
3. The importer is local and deterministic. It validates year, numeric votes, unique candidate labels per contest, matching declared denominators and one boundary version per contest; it refuses totals exceeded by supplied candidate votes. A single SQLite transaction writes normalized result rows plus reused P1 election/party/constituency/boundary-version IDs. No model or remote provider runs.
4. Each result row links to the **source file hash, project, import ID and original CSV physical line**. The quality report exposes whether supplied candidate votes cover their *own declared* total. This is **not** official validation, source independence, a winners list, an inference about voter preferences, or proof of constituency boundary equivalence.
5. If a source is withdrawn later, imports retain an explicit withdrawn source status and cannot be used as current verified evidence. An identical source ID cannot be imported twice; revised sources require new source IDs and provenance.
6. Use `PYTHONPATH=platform/src:services/api python -m pytest tests/test_election_results.py -q`. Local fixture: synthetic constituencies and candidates, not real voters or official results.

**Next prerequisite before connecting actual ECI records:** review ECI's official [statistical reports](https://www.eci.gov.in/statistical-reports) and each chosen data resource's usage rights and field semantics, then add a **single mapping adapter** that outputs the normalized CSV. Do not bulk-import open-source election datasets or mark ECI integration verified without source-by-source checks.



## Phase 3 — Policy, legislation, media, governance and advanced simulations
**Epic:** [#8](https://github.com/limuria08-hub/Dotpol/issues/8) · **Former milestones:** 7–9 · **Owners:** D, C, B, E.

- [ ] **P3.01 · D — Legislative sources:** bills, debates, amendments, questions, votes and regulatory timelines from authorized public sources.
- [ ] **P3.02 · D — Governance/policy:** budgets, public programmes, schemes, outcomes, jurisdiction and manifesto/commitment record linking.
- [ ] **P3.03 · D — Political knowledge/quality:** linked entities, event/source reconciliation, versioned assertions, no second graph of truth.
- [ ] **P3.04 · D/B — Media research:** verified public news/RSS data, BERTopic, event/narrative trends, differences among sources and timestamps.
- [ ] **P3.05 · C — Forecast/scenario models:** PyMC and proven statistical methods for aggregate estimates, confidence intervals, calibration, backtesting and sensitivity.
- [ ] **P3.06 · C/D — Causal/policy simulation:** evaluate DoWhy and optional external OpenFisca only after assumptions, local rules, resource and licence audit.
- [ ] **P3.07 · D/A — Civic deliberation:** optional independently deployed Polis/Decidim, via approved API; no mandatory AGPL code embedding.
- [ ] **P3.08 · B/E — Language/reporting:** optional IndicTrans2 model, document/report generation, reproducible research briefs and cited exports.
- [ ] **P3.09 · B/D — AI specialists:** policy, legislation, media, governance, forecasting and report tools reuse P1 gateway, P2 engines and source registry.
- [ ] **P3.10 · F — Exit gate:** a complete public-policy/legislation/media research journey with primary evidence, model assumptions, uncertainty and reproducibility tests.

**Done when:** questions about legislation, governance, public issues or policy impacts produce sourced, dated, calibrated and reproducible analyses, not unsupported forecasts.

## Phase 4 — Nested teams, OpenClaw communications, mobile fieldwork and command centre
**Epic:** [#9](https://github.com/limuria08-hub/Dotpol/issues/9) · **Former milestone:** 10 + approved field continuity from 6 · **Owners:** A, E, B, F.

- [ ] **P4.01 · A — Org/team core:** Organization, Team, Membership, RoleGrant, Delegation, ProjectAccess; recursive subteams with depth/cycle limits and audit logs.
- [ ] **P4.02 · A/F — Secure scoped access:** parent/team/resource rules, invitations, least privilege, revocation, denial tests and data export isolation.
- [ ] **P4.03 · A/B/F — OpenClaw channel authorization:** map paired Telegram/WhatsApp/supported channel accounts to explicitly authorized Dotpol actors; enforce project/team scope on every inbound action and restrict outbound notifications. A shared gateway must not cross untrusted organization boundaries.
- [ ] **P4.04 · A/E — Unified team messaging workflow:** supervisor assigns and verifies operational tasks in Dotpol; approved field notifications and responses traverse OpenClaw and return to the same canonical Task/Incident records with idempotent delivery and audit receipts.
- [ ] **P4.05 · E/A — Mobile teams:** team leader → member assignments, approved check-in, site forms, incidents, task handover, multilingual workflows.
- [ ] **P4.06 · A/E — Offline sync:** ODK Collect/Central interoperability, idempotent receipts, retries, conflict resolution, lost-device/revocation cases.
- [ ] **P4.07 · A/E — Command centre:** site preparedness, timestamped aggregate turnout observations, incident severity/escalation, verified reports; reuse fieldops records and F6–F8.
- [ ] **P4.08 · B/E — AI supervisor copilot:** permission-safe briefings, assignment summaries, duplicate issue flags, shift handovers; no unauthorized actions.
- [ ] **P4.09 · A/F — Optional realtime:** Centrifugo or ntfy *only if required* as delivery transport, never authoritative Task/Incident DB.
- [ ] **P4.10 · F — Exit gate:** 1 admin → 3 supervisors → 10+ workers → nested child team; offline recovery; denied cross-team reads; OpenClaw authorized messaging/field-update journey; station F6–F8.

**Done when:** one organization can securely coordinate delegated mobile teams, share authorized files, reconcile offline observations, and see traceable command-centre summaries.

## Phase 5 — OpenClaw, agents, automations, plugins and release
**Epic:** [#10](https://github.com/limuria08-hub/Dotpol/issues/10) · **Former milestones:** 11–12 · **Owners:** B, A, E, F.

- [ ] **P5.01 · A/B — Agent/plugin manifests:** one versioned registry for DataConnector, AnalysisTool, AIProvider, FieldService, ArtifactProvider and AutomationProvider; permissions/expiry/audits.
- [ ] **P5.02 · B/F — Required OpenClaw runtime:** install/pin and launch maintained OpenClaw gateway as a supported first-class LiOS.Pol component; authenticate, pair nodes, sandbox tools, enforce approval and verify local restart/reconnect. No arbitrary host shell or unreviewed skills enabled.
- [ ] **P5.03 · B/A — Channels and devices:** required authorized Telegram/WhatsApp/supported device integration through OpenClaw; inbound identity mapped to Dotpol role scope; no channel credentials copied into Dotpol client.
- [ ] **P5.04 · B/A — Do not duplicate AI:** OpenClaw transports channel messages and invokes approved Dotpol tools; PydanticAI owns political research orchestration; no second authority for projects, tools, model policy or data.
- [ ] **P5.05 · B/A — Automations:** Prefect for durable approved tasks where needed, scheduled research/monitoring, confirmation gates, retries, cost/resource caps and audit trail.
- [ ] **P5.06 · A/F — Zero-paid deployment profiles:** provide a supported local OpenClaw gateway install/launch and upgrade path as part of LiOS.Pol, plus ODK/notification service profiles where used. Compose is allowed for supported service management, not mandatory paid hosting or K3s.
- [ ] **P5.07 · F — Supply-chain compliance:** exact donor refs/versions, component/model/data licence checks, third-party notices, SBOM, update policy, permissions and security review.
- [ ] **P5.08 · E/F — Cross-device UX:** responsive desktop/tablet/mobile, keyboard, accessibility, export/import, data recovery and documented supported targets.
- [ ] **P5.09 · F — Resilience/security:** AI prompt-injection, remote-consent, unauthorized tool/cross-team access, API exposure, secrets, offline/reconnect, throughput and restore tests.
- [ ] **P5.10 · F — Exit gate:** reproducible local and approved shared deployment, final integrated research→analysis→field→report flows, release artifacts and contributor documentation.

**Done when:** local first-run, optional organization deployment and required OpenClaw channels are independently reproducible, secure, maintained and fully documented.

## Execution protocol and completion gates

1. **Small, reviewable PRs:** one work-package ID, one owning lane, dependencies declared, commit/changeset and test evidence. Do not create extra product forks or blanket import repositories.
2. **Fork-first only for approved donor modifications** under the user-owned GitHub account; preserve upstream, pinned commit and notices. Otherwise use upstream package or isolated service.
3. **Separate planning from implementation:** candidate ≠ installed ≠ adapter integrated ≠ end-to-end tested ≠ released. Never mark tasks done automatically.
4. **Integrate in order of prerequisite contracts:** P1 shared schema/tool/artifact → P2 verified data/analytics → P3 policy/media/models. P4 identity/field contracts may proceed against P1 when stable; P5 service/security investigation may run independently, but release depends on all gates.
5. **One source of truth:** `docs/MASTER_PLAN.md` for product, this file for step checklists, `architecture/execution-plan.yml` for machine gates, five existing phase issues #6–10 for assignments. Historical documents are reference only, never alternate roadmaps.
6. **Protect the local-first core:** OpenClaw provided in the supported local install; no compulsory ODK Central, hosted AI, paid tiles or cloud; explicit consent before transmitting user evidence or connecting external accounts.
7. **Political product boundary:** use authorized aggregate research/operations, documented survey data and lawful source access; do not build inferred individual political preferences, persuasion targeting, electoral-roll enrichment or fictional official live booth feeds.
8. **Phase exit evidence:** demonstrate a complete user journey, reproducible tests, accurate source/model metadata, security/permission checks, exact dependency licences, and independent install results.

### Immediate execution queue

1. **Finish/review existing [P1 PR #11](https://github.com/limuria08-hub/Dotpol/pull/11),** confirm CI and real model/browser/search integration. No competing P1 branch.
2. **Agent E:** work from [UI issue #12](https://github.com/limuria08-hub/Dotpol/issues/12) against P1 application contracts. No full frontend reset.
3. **A/D:** finalize service contract stubs and political IDs; integrate OpenClaw locally with security gates; **do not** create any file-service integration.
4. **F:** review licences, CI, source evidence, runtime constraints, and conflicts before any merge.
