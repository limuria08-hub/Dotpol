# ADR-0003 — One pre-election field-operations owner

**Status:** Accepted planning scope · **Date:** 2026-10-15 · **Implementation owner:** `domains/fieldops`

## Problem

The original blueprint covered booths, surveys and election-day war room but did not specify pre-election site readiness, authorized field assignments, offline report verification or continuity into live operations. Treating this solely as a Phase 10 feature would leave the essential earlier field workflow missing.

## Decision

- **`domains/fieldops`** owns pre-election site/microarea assessments, assigned work and verified field-observation semantics, using canonical `Task` and `FieldUpdate`.
- **`domains/warroom`** composes the **same** records into election-day incidents, aggregate monitoring and alerts. No second task store, map system, voter CRM or survey backend.
- `platform/surveys`: versioned forms and **ODK Collect** offline interoperability.
- `platform/gis`: canonical stations, areas and boundary versions.
- `platform/data`/`provenance`/`auth`: source lineage, verification, retention and permissions.
- Proposed derived/specialized records are reviewed under [Domain Model](../DOMAIN_MODEL.md), not added as an independent ontology.

## Delivery

- **Phase 0:** approve data limits and owner.
- **Phases 2, 4, 5:** station identifiers, permitted geographic data and maps.
- **Phase 6:** facility checklist and offline verified field pilot.
- **Phase 10:** same event/incident records in the election-day command center.
- **Phases 11–12:** alerts, resilience, audit and release.

**Limits:** site observations and lawful aggregated local reports; no inferred individual political preferences, electoral-roll targeting, named voter/household political profiles or individual voted/not-voted records. Staff project roles are not equivalent to official ECI appointments.

## Verification

Pass tests **F1–F8** in the [field specification](../PRE_ELECTION_MICROAREA_INTELLIGENCE.md), including offline retry, conflicts, role isolation, aggregate suppression and distinct official/field turnout source states. No implementation is marked complete until tested.

**Dependencies:** use accepted planning [ADR-0001](0001-foundation-module-ownership.md) and [ADR-0002](0002-one-stack-per-capability.md). Compliance, source permission, role grants and F1–F8 tests remain implementation gates.
