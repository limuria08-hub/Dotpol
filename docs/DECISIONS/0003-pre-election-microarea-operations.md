# ADR-0003: Add one pre-election microarea and field operations domain

- **Status:** Proposed (not accepted; Blueprint remains frozen for Phase 0 review)
- **Date:** 2026-10-15
- **Owners:** Maintainer to appoint; proposed `domains/fieldops` (domain), `platform/surveys` (collection), `domains/warroom` (consumer)
- **Related capabilities:** `field-operations-intelligence`, `constituency-intelligence`, `election-intelligence`, `offline-field-interoperability`, `warroom-intelligence`
- **Primary specification:** [Pre-election Microarea Intelligence and Booth Operations](../PRE_ELECTION_MICROAREA_INTELLIGENCE.md)

## Context

The current Blueprint and Phase 10 roadmap specify polling stations, surveys and election-day war room but omit explicit **pre-election** microarea/site assessment workflows, staff permissioning, field-report QA, offline sync semantics and how all of those feed the war room without a second backend. The user identified this as a critical product gap.

## Constraints

- Local-first and valid ₹0 core; one capability owner and canonical entity IDs.
- Strict separation of public station geography, aggregate survey/site observations, personal service requests, and restricted/private electoral data.
- No identifiable or household-level inferred political preference records, voter persuasion/turnout scores, electoral-roll enrichment, named-person voter tracking, or targeted political outreach.
- Compliance with applicable election rules, data permissions, privacy requirements and polling-day operator roles, reviewed by jurisdiction/date.
- Shared GIS, Task/Incident/Alert, Source/Evidence, ODK and Survey contracts; no separate voter CRM, GIS backend or event processor.
- Phase 10 must **consume** verified operations capabilities, not reimplement pre-election fieldwork.

## Options considered

### A — Add `domains/fieldops` as single domain owner and phase-aligned vertical slices (RECOMMENDED)

Pros: explicit accountability for pre-election work, reuse of shared infrastructure, gradual Phase 2–6 preparation, straightforward Phase 10 consumption, prevents separate booth CRM. Cons: needs new field observation/assignment specialization, validation and device-offline permissions; careful small-area privacy rules.

### B — Put every pre-election field feature in `domains/warroom` in Phase 10

Pros: fewer module names. Cons: too late for pre-election preparation, mixes station-readiness collection with election-day incident response, creates shortcuts/duplication and no audited early validation. Not recommended.

### C — Integrate a complete third-party voter CRM/household profiling application

Not selected: conflicts with singular platform ownership and introduces serious personal political-preference targeting, licence/security and data permissions risks; not needed for neutral aggregate site operations.

## Proposed decision

Select **A**: `domains/fieldops` owns pre-election observation and operator task semantics, starting as **specification**. `platform/surveys` owns generic questionnaires and ODK Android offline interoperability. `platform/gis` owns canonical station/microarea geometry and display contracts. `platform/data` and `platform/provenance` own source/raw data lineage, `platform/auth` owns permissions, `platform/automation` later owns scheduled work. `domains/warroom` aggregates validated `FieldUpdate/Task/Incident/Alert/TurnoutObservation` and existing election/GIS/survey data for live read models.

Use single elected map stack once approved separately under ADR-0002; this ADR does **not** choose or replace a GIS renderer.

## Domain and release effects

- Canonical `PollingStation`, `BoundaryVersion`, `FieldUpdate`, `Task`, `Incident`, `Alert` remain unmodified system-of-record concepts.
- Add a **proposed** `Microarea` geographical aggregate unit, `StationFacilityAssessment`, `SyncReceipt`, and task/field-update specializations **only if needed** after the canonical entity extension review. No individual named-voter/household political entity.
- Introduce typed, source/versioned fields for `observed_at`, `received_at`, `verified_at`, geographic boundary version, form version, collecting role, report conflict and status.
- Stage in Phase 2 station data, Phases 4–5 mapping, Phase 6 offline pre-election field forms/QA, Phase 10 live ops, Phase 11 durable alerts and Phase 12 hardened deployments.
- A separate field pilot may be demonstrated earlier only with synthetic/permissibly sourced site data, test-only operators, no private voter targeting, explicit acceptance gate and clear limitations. The seven-day research MVP remains a distinct first-release target.

## Duplication prevention

No new backend, map renderer, task queue, notification engine, survey framework, identity-matching engine, data warehouse or AI gateway. Field agents should **not** own source of truth for polling station identities, raw elections data, contact records or survey methodology.

## Privacy and election-operations safety

- Role-scoped site observation and staffing, documented consent and retention where personal data is collected; no default home/individual geolocation or individual voted/not-voted records.
- Distinguish ECI BLO, political BLA, legally accredited polling agent, Dotpol project enumerator and site supervisor; application access never confers an official role.
- No LLM-generated or unverified reports represented as official records. Data reconciliation and evidentiary confidence states required.
- ECI approximate VTR, Form 17C statutory data when lawfully available, and field operational observations are three distinct provenance/quality categories.

## Verification / acceptance

1. Approved roles, data dictionary, sources, and licence/jurisdiction legal review.
2. Synthetic station/microarea import and stable boundary identifiers; duplicate detection.
3. Offline site checklist submitted once after multiple retries; audit/clock-skew tests.
4. Supervisor conflict resolution preserves both raw observations and explanation.
5. Small-cell suppression/re-identification, access and deletion tests.
6. One shared event model consumed by a pre-election preparedness dashboard and Phase 10 war-room view, without second field schema.
7. ECI source/record state clearly differentiated from operator estimates.
8. Full tests and PR reviewer sign-off before status moves from planned to implemented/verified.

## Migrations / related documents

This planning PR updates `docs/BLUEPRINT.md`, `docs/ROADMAP.md`, `docs/DOMAIN_MODEL.md`, `docs/CAPABILITY_REGISTRY.md`, `architecture/capabilities.yml`, `docs/ARCHITECTURE.md` and `docs/AI_ARCHITECTURE.md` with **explicit proposed scope**. Other draft ADRs in PR #1 and PR #2 are not accepted by this change; their code-ownership/map choices must be reconciled before implementation.

**This ADR is a proposal, not approval to collect identifiable electoral data or implement individual voter targeting.**
