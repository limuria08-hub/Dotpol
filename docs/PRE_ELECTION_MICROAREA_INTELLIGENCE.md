# Pre-Election Field Operations — Technical Requirements

**Status:** Proposed and unimplemented · **Canonical plan:** [Five-phase Master Plan](MASTER_PLAN.md) · **Ownership:** [ADR-0003](DECISIONS/0003-pre-election-microarea-operations.md). Historical Phase 2/4/5/6/10/11/12 mentions below are **legacy milestones**: field pilot is P2, command centre P4, hardening P5.

## Scope and ownership

One unified **pre-election field → election-day operations** workflow for permitted polling-site/microarea geography, facilities, authorized staff assignments, offline observations, reviewer validation, aggregated reporting and incidents.

- `domains/fieldops`: site visits, site status, assigned work, report verification and operational issue classifications.
- `domains/warroom`: consumes the same approved station IDs and field records for live command-center status.
- `platform/gis`, `platform/surveys`, `platform/data`, `platform/provenance`, `platform/auth`: each retains its own existing capability. No dedicated voter CRM, second survey/form platform, GIS engine or task database.
- Not a named-elector/household political preference map, voter-contact/persuasion score, electoral-roll enrichment system or individual voted/not-voted tracker. An internal deployment still requires permission, retention and audit controls.

## Approved roles and actions

| Role | Actions |
|---|---|
| Supervisor | Import approved stations, assign facility visits, review reports, manage unresolved incidents |
| Field operator | Report site conditions through scoped forms, including offline submission |
| Data reviewer | Verify/dispute records, flag missing or conflicting observations, preserve audit history |
| Analyst | View safe aggregate site conditions, source/period-labelled summaries and preparedness maps |
| Election-day operator | Observe authorized site incidents and report non-official operating status |
| Privacy administrator | Approve form fields, access roles, minimum aggregation, retention and exports |

Dotpol staff roles do not imply ECI authorization: **Booth Level Officer (BLO)**, **Booth Level Agent (BLA)** and statutory polling agents have distinct roles and legal permissions.

## Minimum records

Reuse canonical `PollingStation`, `BoundaryVersion`, `Task`, `FieldUpdate`, `Incident`, `Alert`, `TurnoutObservation`, `Source` and `Evidence` first.

| Proposed extension | Required attributes | Rule |
|---|---|---|
| `Microarea` | non-personal area ID, geometry, boundary effective dates, parent area, source | Maps public/aggregate units, never private homes |
| `StationFacilityAssessment` | station ID, observed_at, form version, facilities/accessibility codes, report/evidence IDs, verification status | Preserve revisions and reporter/source |
| `FieldAssignment` | existing Task ID, station/microarea, operator role, authorized form, deadline, review state | Implement as Task specialization, not shadow task database |
| `FieldObservation` | existing FieldUpdate ID, type, area/site, observed/received timestamps, form/source, review state | Implement as FieldUpdate specialization |
| `SyncReceipt` | client submission UUID, payload hash, form version, received_at, dedup/conflict state | Retrying a form cannot produce new record |
| `BoothReadinessSnapshot` | derived counts of visited/missing/verified/disputed sites, period and provenance | Derived view only; never override raw data |

No extension becomes canonical without the domain-model extension review and ADR acceptance. No personally identifying respondent or vote-preference fields in general field events.

## End-to-end flow

```text
Approved PollingStation/Microarea records
  → authorized Task + published versioned facility/site form
  → ODK Collect offline report
  → local controlled import/sync + SyncReceipt deduplication
  → reviewer verification / dispute / correction
  → source-backed coverage and facilities map
  → P4 command-centre shared incidents, alerts, briefing (former milestone 10)
```

**Offline sync conditions:** scope credentials by project/site/form, never assume full-time internet; distinguish `observed_at` from `received_at`; preserve raw records, handle clock drift and conflicting submissions; respect device-loss and local-draft protection. ODK submission encryption alone does not secure all device data. No mandatory paid server.

**UI conditions:** show reporting coverage **with denominator**, observation period, timestamp, site boundary version and source/verification state. Do not show misleading percentages when reports are missing. Public-issues survey aggregates need approved minimum cell sizes, complementary suppression and visible sampling limitations; site facility reports can be site-specific where lawful and non-identifying.

**Polling-day source states:** show public approximate official turnout updates, lawful Form 17C records and operator-reported counts as **separate** series. Each needs source, authority, date/time, reporting granularity and final/approximate/disputed status. Do not imply an official live booth feed where none is verified.

## Acceptance fixtures — exact eight cases

| ID | Test |
|---|---|
| F1 | Import authorized stations; reconcile IDs/duplicates and time-valid boundaries |
| F2 | Supervisor assigns five facilities/accessibility inspections; operator sees only their own |
| F3 | Offline submission plus three retries produces one stored observation and one receipt |
| F4 | Contradictory site reports remain visible; reviewer records evidence and resolution |
| F5 | Map verified site conditions; restrict identifiable/small-cell survey aggregates |
| F6 | Election-day incident references same station and field-report IDs as pre-election phase |
| F7 | Official approximate VTR, statutory Form 17C if permitted, and field reports have distinct statuses |
| F8 | Export date-stamped preparedness/incident brief with missing, unresolved, disputed and sourced findings |

**Negative tests:** invalid station ID, invented official source, file/URL permission violation, wrong-role access, repeated-sync corruption, lost-device revocation, revoked evidence, inaccurate sampling denominator, suppression bypass, unauthorized voter-level political fields.

## Phases and exit gates

- **0:** sign off one field owner, operator role rules, permitted data classes and ADR.
- **2:** import source-linked station references and legal geography.
- **4–5:** map valid station IDs, public facilities and allowed election aggregates.
- **6:** **field pilot** completes F1–F5 with approved synthetic/public fixtures.
- **10:** **operational command center** completes F6–F8, timed/conflicted updates, reviewer state and audit.
- **11–12:** durable alerts, recovery, privacy/security and release checks.

## References for source/legal review

- [ECI Model Code of Conduct](https://www.eci.gov.in/mcc)
- [ECI electoral roll information](https://www.eci.gov.in/electoral-roll) — read source-use terms before importing data.
- [ECI voter-turnout guidance](https://www.eci.gov.in/Documents/Final-VTR-FAQ.pdf) — verify current official vs Form 17C terminology and permitted records before deploy.
- [ODK Collect](https://docs.getodk.org/collect-intro/) and [encrypted forms](https://docs.getodk.org/encrypted-forms/) — offline semantics and device-data caveats.
- [MeitY DPDP Rules](https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa) — review applicable commencement and obligations per deployment date.

**Status:** Requirements only; no live official feeds, synchronizing server, form deployment, permission audit or user application have been implemented.
