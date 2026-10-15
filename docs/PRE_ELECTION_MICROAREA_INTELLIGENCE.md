# Pre-Election Microarea Intelligence and Booth Operations — Product Specification

**Date:** 2026-10-15  
**Status:** Phase 0 proposal for maintainer review; **not implemented and not a licence/compliance approval**  
**Related:** [Blueprint](BLUEPRINT.md), [Roadmap](ROADMAP.md), [Domain Model](DOMAIN_MODEL.md), [ADR-0003](DECISIONS/0003-pre-election-microarea-operations.md), [Phase 0 audit PR #1](https://github.com/limuria08-hub/Dotpol/pull/1) and [single-stack donor PR #2](https://github.com/limuria08-hub/Dotpol/pull/2).

## 1. Why this is a core missing workstream

The existing plan has booths/polling stations, aggregate election metrics, Survey Studio, `FieldUpdate`/`Task`/`Incident`, offline interoperability and Phase 10 war room. It **does not yet have an end-to-end specification for work *before polling day***: preparation, booth directory and boundaries, neutral public-service/facilities assessments, authorised field reporting, verifiable microarea observations, offline collection, reviewer workflows, readiness and continuity into polling-day incident operations.

**Product definition:** An election-operations and civic research workspace for lawful, **aggregate geographic** intelligence and authorized staff workflows at polling-station and other appropriately sized *microarea* units. A "microarea" may be a neighbourhood/sector/ward part or public facility catchment; it is **not** a map of individual named electors, households or inferred political preferences.

**Not in scope:** Individual voter political profiles or support/loyalty labels; inferred vote choice; identifiable person/household political persuasion scores or contact-routing; matching electoral rolls to survey answers, phone numbers or private data; lists of who has/has not voted; automated personalized voter persuasion or suppression. No donor, AI agent or supervisor can override this boundary.

## 2. User roles and separation of duties

| Role in Dotpol | Lawful job / permissions | Restrictions |
|---|---|---|
| Project supervisor | Create a project, approved station areas, allocate geographic observation assignments, review issues and manage aggregate dashboards | No default export of personal respondent records; cannot deem unverified updates official |
| Authorized field enumerator | Collect preapproved **site/microarea observations**, nonpartisan facilities checklists and consent-based surveys within assigned area, offline where needed | Cannot import electoral rolls as individual intelligence records or classify named voter preferences |
| Data quality reviewer | Flag missing coverage, duplicate reports, implausible counts, contradictory evidence, source and timestamp problems | Keeps raw observations immutable; records corrections/reviews separately |
| Elections/analyst reader | Read validated public aggregates, dated reports, approved summaries and maps | No respondent-level political information, no home-address/location pins |
| Polling-day observer / incident reporter | Report site conditions, observed queue/accessibility issues, operational incidents via authorized channel | No real-time targeting of voters, unlawful electioneering or impersonation of officials |
| Privacy and compliance reviewer | Approve data classes, collection purpose, form types, suppression, retention/deletion and exports | Has a distinct approval trail and can block unsafe workflows |

**India-specific note:** ECI-appointed **Booth Level Officers (BLOs)** are election personnel and party-appointed **Booth Level Agents (BLAs)** have different functions. Neither role nor polling-agent authorization may be impersonated or inferred from an app account. Dotpol has its **own internal field operator roles**, not ECI appointments. Any election-specific candidate/party activity must comply with jurisdiction, ECI instructions and the Model Code of Conduct.

## 3. First-class capabilities (one owner each)

### A. Station and microarea directory — owned by `domains/constituencies` / `platform/gis`

- Canonical `PollingStation` with official ID, name, accessibility/facility metadata, election and effective boundary/version; separate mapping of microareas to station/ward/constituency.
- Import public/permitted station reference data with source date/licence/provenance; do not silently map home addresses or personal elector-roll rows.
- Coverage view: *sites/microareas mapped*, *sites visited*, *reports received*, *unverified reports*; display denominators and reporting freshness.
- Restrict the minimum mapping unit for display of sensitive survey aggregates; small-area reports must not reveal individual participants.

### B. Pre-election readiness/facilities checks — owned by `domains/fieldops`

- Checklist: public entrance accessibility, ramps, signage, public transport approaches, water/sanitation accessibility, public lighting, facility readiness and verified logistical issues.
- Attach permitted site photographs, timestamp, form version, source/observer role and site coordinates (not respondent home GPS). Flag unverified/permission-restricted photos.
- Keep observed infrastructure condition distinct from predictions, party sentiment or private voter preferences.
- Escalate outstanding site problems using existing `Task`/`Incident` contracts; do not make a second task manager.

### C. Nonpartisan local issue observations — owned by `domains/fieldops` with `platform/surveys`

- Collect coded **public issue categories** as area-level observations (e.g., water access, transport/accessibility, connectivity, infrastructure) and aggregate feedback using approved surveys.
- Recorded observations include observation window, sample basis or site visit count, reviewer, quality and data provenance; label findings as observed/reported, not representative unless methodology supports that claim.
- Never score named voters, households or tiny identifiable cohorts for party affinity, persuasion susceptibility or expected turnout.

### D. Authorized field assignments and QA — owned by `domains/fieldops`

- Assign an operator a *site/microarea work item* with deadline, form type, permitted scope and supervisor.
- States: `draft -> assigned -> in_progress -> submitted -> verified/rejected -> closed`; version all changes, timestamp submission and verification.
- Idempotent submissions; duplicates, stale observations and conflicting reports appear in a review inbox; no silent overwrites.
- Use minimal staff/workforce identification and access permissions; GPS records are about a **site**, not default continuous tracking of people.

### E. Offline collection and synchronization — owned by `platform/surveys`

- **ODK Collect** is the *single chosen offline Android collection runtime* when that phase starts; keep Dotpol's canonical form/observation schemas and audit/provenance contract.
- Use approved ODK form/XLSForm interoperability, collection without connectivity, opt-in/controlled sync to a reviewed endpoint or local import workflow. ODK submission encryption protects finalized forms but does not by itself secure drafts on devices, accounts or exports.
- Provide client-generated submission IDs, form versions, retries, deduplication, conflict review, source-device time plus server-receipt time, and minimal data transfer.
- **Do not assume a free compulsory hosted ODK backend.** A local/private ingestion mechanism is the source of truth; any ODK Central deployment is a separate architecture/licensing/operations decision, not another Dotpol domain engine.

### F. Pre-election analyst overview and reporting — owned by `domains/fieldops` + `apps/web`

- Maps of station **facility status**, assignment/report **coverage**, aggregate verified issues and approved quality indicators.
- Filters by constituency/ward/station/observation period/report type; no individual political trait segments or personally identifying home pins.
- Source badges: `official`, `field_report_unverified`, `field_report_verified`, `derived_aggregate`, `outdated` / `withdrawn`.
- Reports show denominator, period, geography version, known gaps, suppression and sources; support accessible printable preparedness summary and issues brief.
- No "supporters", "persuadables", "likely voter", "household persuasion score" or voter contact priority views.

### G. Link to election-day war room — owned by `domains/warroom` (composition only)

- Reuse station ID/geography, site conditions, approved observer assignments, incidents, and alert acknowledgement records for Phase 10.
- Distinguish **approximate official ECI Voter Turnout App (VTR) figures**, **statutory Form 17C polling-station records where lawfully available**, and **field-provided non-official operational observations**. Never treat all three as the same source or finality.
- Live dashboard displays timestamp, source/authority, granularity, verification, update lag and conflicts; no claim that a nonexistent live per-booth official feed is available.
- Alerts cover missing operational reports, site accessibility incidents, delayed synchronization and disputed statistics—not individual voter mobilization, persuasion or surveillance.
- Election-day permissions/Model Code compliance gates are strict; independent review before any polling-day deployment.

## 4. Canonical contracts — new entities only if not representable by existing model

**Reuse:** `PollingStation`, `AdministrativeArea`, `ElectoralArea`, `BoundaryVersion`, `Survey`, `SurveyResponse` with controls, `TurnoutObservation`, `FieldUpdate`, `Task`, `Incident`, `Alert`, `Evidence`, `Source`, `TransformationRun`, `Briefing`.

**Proposed additions:**

| Entity | Minimum fields / linkages | Reason |
|---|---|---|
| `Microarea` | stable non-personal geographic ID, jurisdiction, polygon/catchment, `boundary_version`, effective dates, permitted source ID | Public operational unit below ward/constituency, never a named-voter/household record |
| `StationFacilityAssessment` | station ID, form version, observation period, facility type/status, attachments/source refs, reporter role, validation state | Typed structured site-readiness checks; retains revisions |
| `FieldAssignment` | assignment ID, operator role ID, site/microarea, approved template, due period, workflow state, reviewer | Authorised work allocation without duplicate task engine; implemented as a `Task` specialization if viable |
| `FieldObservation` | observation ID, site/area ID, category, source, collected and received times, device submission ID, review state | Typed specialization of `FieldUpdate`, not a shadow table if current model suffices |
| `SyncReceipt` | client-generated key, form version, ingestion timestamp, server receipt ID, dedupe/conflict status | Robust offline retries and audit separate from form content |
| `BoothReadinessSnapshot` | aggregate period, station set, source versions, observed coverage, missing/verified/flagged site totals | Derived view; **not** authoritative data source / new polling-station entity |

**Do not introduce** `VoterProfile`, `HouseholdPoliticalPreference`, `VoterContactScore`, `LikelyVoter`, `SupporterTier`, `IndividualTurnoutStatus` or equivalent proxy fields. Disable arbitrary analyst joins that reconstruct these categories.

### Operational event example (conceptual; not a shipped API)

```json
{
  "event_type": "facility_assessment.submitted",
  "event_id": "uuid",
  "site_id": "station-id",
  "form_version": "1",
  "submission_id": "client-generated-uuid",
  "observed_at": "ISO-8601-time-with-zone",
  "received_at": "ISO-8601-time-with-zone",
  "source_id": "registered-field-source",
  "verification": "unverified",
  "data_class": "site_observation"
}
```

The versioned `Source` and evidence attachments remain separately addressable. Every field must pass an approved data dictionary before coding; these are intent sketches, not stable API contracts.

## 5. Use cases and acceptance tests

| ID | User / request | Expected outcome | Gate |
|---|---|---|---|
| U1 | Supervisor imports 100 approved polling stations and public accessibility data | 100 canonical station IDs, duplicate reconciliation, missing geometry indicated | Every imported fact points to allowed source/version |
| U2 | Operator receives an assignment to review signage and accessible entry at 5 sites | Form and due date scoped to those sites; no ability to enumerate named electors | Assignment/state and access audit passes |
| U3 | Field operator records a site readiness assessment without internet | Local draft remains usable, final submission syncs once, retries do not duplicate | Offline, clock skew, media size, dedupe tests |
| U4 | Two reports disagree about ramp accessibility at one station | Dashboard shows conflict and asks reviewer; previous reports remain available | No silent overwrite, provenance and reviewer decision trail |
| U5 | Analyst opens a microarea public-issues summary | Only adequately aggregated, method-labelled issue counts and gaps shown | Small cell/complementary suppression and re-identification tests |
| U6 | Election-day reviewer inspects reported turnout status | ECI approximate, Form17C if authorized, and field observations remain distinct with period and status | No false official source, zero individual 'voted/not voted' rows |
| U7 | Staff member loses device or leaves project | Revoke access; deleted expired service/operational data reconciles to caches and exported access | Retention, access revocation and offline recovery exercise |
| U8 | Supervisor exports a booth preparedness report | Contains station facility state, unresolved issues, period, completeness and verified source trail | No personal respondent data, no political preference fields |

**Quality measures (targets to approve):** valid station-ID match rate; duplicate submission rejection rate; verified report coverage; report freshness lag; offline sync failure/retry rate; conflict resolution time; empty/no-evidence correctness; issue resolution throughput; data deletion/export audit; accessibility of UI. Establish denominators/thresholds from an approved fixture **before** reporting pass/fail.

## 6. Data, legal, privacy and fair-election controls

1. **Boundary:** no processing intended to identify private voting preferences, create named or household-level political profiles or direct individualized political persuasion. Aggregate outputs require a published aggregation/suppression threshold set by privacy reviewers; keep thresholds configurable and prevent repeated filtering from defeating suppression.
2. **Data minimisation:** collect site condition observations and consent-based survey answers for clearly stated lawful purposes. A public electoral roll is **not** authorization to scrape, link it with private contact lists, append political labels or redistribute it.
3. **Separate lawful service records:** if an individual voluntarily reports an accessibility problem and requests follow-up, store only the necessary contact and case in a purpose-limited restricted service-case store; do **not** join it to party/voting analytics or make it part of the common microarea map. Require consent/other lawful basis, notice, deletion/retention and reviewer approval before introducing this function.
4. **Sensitive data:** no respondent names, phone numbers or exact private GPS coordinates in shared map exports; restrict form fields, attachments, free text, audit logs and role visibility.
5. **Source rights:** licensing, ECI terms, publication and permitted-use review for every station map, electoral source, GIS geometry or official turnout update.
6. **Law timelines:** India's DPDP Act/2025 Rules have staggered commencement and corrigenda. Maintain a dated legal review per workflow; **do not label the Act universally in force on 2026-10-15**.
7. **Agent boundaries:** AI may summarize **approved aggregate reports**, suggest logistical checks and flag incomplete evidence. It must not fabricate field updates, assign political stance to individuals or issue unsupervised official/compliance instructions.
8. **Election-day controls:** distinguish app staff, ECI BLO, party BLA and statutory polling agents; follow election-period rules, permitted locations and approved access. No restricted marked-roll digitization, coercion, intimidation or noncompliant canvassing.
9. **Security:** scoped device/form credentials, local encryption as appropriate, prepared safe photo handling, offline device-loss policy, resource caps, audit log integrity, no default surveillance and clear operator opt-out/retention.
10. **Human oversight:** an unverified report never becomes an official record because an LLM says so. Supervisors must be able to correct, mark disputed and withdraw an event with immutable audit history.

## 7. Reuse-first, single stack integration and cost

**Use only existing selected platform capabilities, not a separate voter CRM or new research engine.**

```text
ODK Collect (offline Android site observations, later field phase)
      ↓ secure export / explicitly configured transport + idempotent ingest
Dotpol FastAPI local gateway
      ↓ authorization / validation / dedup / versioning
platform/surveys → domain/fieldops → platform/data + provenance
      ↓ shared station IDs and approved observation read models
apps/web booth preparedness / issue map / supervisor work inbox
      ↓ Phase 10 consumes same read models
domains/warroom → existing task/incident/alert + briefing state
```

- Site and boundary rendering uses the *single GIS integration selected by accepted ADR*; don't add a second booth-map product.
- `platform/analytics` processes aggregate counts/methods; do not create separate field-specific statistics engine.
- `platform/automation` later handles scheduled freshness/escalation when needed; a basic verified queue is enough for an early field pilot.
- Do **not** fork ODK Collect merely to add form templates. Use documented form/export/interop. A fork is justified only by essential Android code modifications, reviewed licence and upstream maintenance plan.
- ₹0 core: a local survey demo must work with local imports/exports and no paid endpoint. Full multi-device real-time shared operations may require a chosen self-hosted sync deployment and should never be represented as a ready feature before architecture/test sign-off.

## 8. Phase alignment (critical to avoid leaving it all for Phase 10)

| Roadmap point | Required addition | Gate |
|---|---|---|
| **Phase 0 (NOW)** | Approve this workstream's boundaries, field roles and one-owner capability; accept/revise ADR-0003 and privacy/data dictionary | No conflicting voter CRM, no individual political-profile data model |
| **Phase 2** | Canonical station/microarea public data and source/boundary versioning | Deterministic import, permissions/terms, dated lineage |
| **Phase 4–5** | Station directory/microarea maps and booth aggregate election overlays | Same canonical station IDs in table/map/election tool |
| **Phase 6** | Authorized pre-election field forms, area issue summaries, site-facilities checklists and ODK offline pilot | U1–U5 on synthetic/public allowed fixtures; privacy/security reviewed |
| **Phase 10** | Real-time site and incident operations, disputed report handling, turnout-source distinctions, supervisor dashboard and alerts | U6–U8, role/permission and real operational evidence tests |
| **Phase 11–12** | Durable alerts, optional syncing at scale, packaging/privacy/security hardening | Reproducible supervised recovery and resilience tests |

**Fast-track constraint:** This module is a high-priority **specification** now, but it does not silently replace the existing **3–7-day research-preview scope**. A runnable field demonstration requires additional collection, synchronization, access-control and privacy reviews. If the product owner changes the first release to prioritize field operations, approve a separate MVP scope decision and exit gates rather than declaring all phases complete.

## 9. Maintainer decisions / unresolved items

- [ ] **D1:** Confirm purpose and scope as neutral aggregate microarea intelligence and lawful operational support, not individual political targeting.
- [ ] **D2:** Confirm field roles and who can use which polling-day data/places in each jurisdiction; distinguish BLO/BLA/polling agents.
- [ ] **D3:** Approve `domains/fieldops` as **one** owner for pre-election field workflows, consumed by `domains/warroom` later (ADR-0003).
- [ ] **D4:** Approve permissible source types, data dictionary, sensitive-data restrictions, min cell suppression and retention/delete policy.
- [ ] **D5:** Approve ODK Collect offline form/transport/security integration and whether self-hosted server/sync is necessary; don't mandate a cloud service.
- [ ] **D6:** Approve aggregation/QA/verification states and exact official-vs-field turnout source handling.
- [ ] **D7:** Select acceptance fixture/datasets and evaluate U1–U8, including failed/offline/conflicted states and privacy attacks.
- [ ] **D8:** Approve which part can enter a first *field-pilot* milestone without implying full election-day deployment.

## 10. Researched external references (checked 2026-10-15)

These links establish **guidance/known behaviours**; none is a connector/API access or reuse permission.

- ECI [Model Code of Conduct](https://www.eci.gov.in/mcc) — polling-day conduct and use/limitations of authorized workers.
- ECI [electoral rolls portal](https://www.eci.gov.in/electoral-roll) and [site Terms](https://www.eci.gov.in/terms-and-conditions) — review allowed uses and boundaries; published roll access is not blanket profiling authority.
- ECI [electoral roll revision FAQ](https://www.eci.gov.in/Documents/Final-ER-FAQ.pdf) — role distinction and revision processes; do not confuse official BLO with party BLA.
- ECI [Voter Turnout FAQ](https://www.eci.gov.in/Documents/Final-VTR-FAQ.pdf) — approximate public VTR reporting and distinct Form 17C statutory polling-station data.
- ODK [Collect introduction](https://docs.getodk.org/collect-intro/), [Using Collect](https://docs.getodk.org/collect-using/), [Encrypted forms](https://docs.getodk.org/encrypted-forms/) — offline field functionality, server submission and encrypted finalization caveats.
- MeitY [DPDP Rules 2025 and corrigenda](https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa) — applicability and staged enforcement must be rechecked for each workflow.

**No application code or third-party donor has been integrated or marked complete by this specification.**
