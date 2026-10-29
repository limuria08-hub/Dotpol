# ADR-0004: Five execution phases, donor isolation, and recursive teams

- **Status:** Accepted planning direction (implementation/licences unverified)
- **Date:** 2026-10-29
- **Owner:** Dotpol product/architecture maintainers
- **Related:** ADR-0001, ADR-0002, ADR-0003; MASTER_PLAN.md; ROADMAP.md

## Context

LiOS.Pol must cover the full political-intelligence vision without repeated planning changes or duplicate repo imports. The old thirteen 0–12 technical milestones made team execution look more fragmented than intended. Collaboration must support administrator → delegated supervisors → nested mobile teams. Many donor projects have complete overlapping backends or copyleft/asset licensing considerations.

## Constraints

- Zero-cost core, local-first personal mode, open-source reuse, no paid key required.
- One capability owner, one canonical political ontology, source provenance, auditable deterministic calculations.
- Preserve original technical milestones/tests as supporting work packages; no deletion of scope.
- No individual inferred voter political preferences, household-targeted persuasion or invented official live booth feeds.

## Options considered

1. Continue treating milestones 0–12 as standalone phases: preserves labels but makes orchestration and user prioritization unwieldy.
2. Introduce five top-level execution phases while retaining 0–12 as explicit detailed milestones: clear ownership, no lost requirements, no parallel plans. **Selected.**
3. Bulk-fork and merge every promising donor: duplicates state, licences and infrastructure; rejected.
4. Embed libraries and connect optional services behind stable Dotpol contracts, forking only for necessary modifications: **selected**.

## Decision

Exactly five execution phases:

- **P1:** Foundation, political data/AI, cited research (former 0–3).
- **P2:** Elections, GIS, statistics, psephology, surveys and verified pre-election field pilot (former 4–6).
- **P3:** Scenario simulation, policy, legislation, manifestos, governance, media and advanced research (former 7–9).
- **P4:** Recursive organization teams, mobile/field workflows, aggregate election-day operational command centre (former 10, reuses fieldops from 6).
- **P5:** Durable monitoring, plugin/service integrations, tests, security, local/share deployment and release (former 11–12).

Keep ADR-0002 stack locked. Do not import alternative large backends without a replacement ADR. Use embedded libraries first, optional API services second; Docker Compose is the default service profile, K3s optional only when justified.

P4 uses canonical Organization/Team/TeamMembership/RoleGrant/Delegation/ProjectAccess and existing Task/FieldUpdate/Incident/Alert/SyncReceipt, with permission-aware recursion. Fieldops owns operations semantics, platform/auth owns identity, warroom composes read models. Unknown future extensions must go through DOMAIN_MODEL review.

New researched candidates (Casbin, Centrifugo, Indian election adapters, DoWhy, OpenFisca, Polis, Decidim, Quarto, IndicTrans2, etc.) are **candidate/reference/optional**, not selected dependencies or installed code. Exact licences and component-level rights must pass before adoption.

## Consequences

Positive: one orchestrated plan, predictable code ownership, reuse without multiplying services, end-to-end shared state. Trade-offs: integration adapters still require engineering; 3-day target can only deliver a bounded working preview, not the entire full-feature release.

## Migration impact

Update README, MASTER_PLAN, ROADMAP, ARCHITECTURE, DOMAIN_MODEL, CAPABILITY_REGISTRY, AGENTS, donor matrix, machine-readable capability/donor metadata and release acceptance references. Old Phase 0–12 references in archived/supporting specifications remain valid as **legacy milestones** mapped to P1–P5.

## Duplication impact

No second chat backend, map workspace, election DB, standalone voter CRM, duplicate forms authoring runtime, independent field-task store, or independent model gateway.

## Verification

- Confirm five execution phases map all thirteen former milestones and every capability.
- Confirm each new candidate is marked unintegrated, unpinned, licence unverified and optional as appropriate.
- Test same dataset chat→workbench→map→artifact; 1 admin/3 coordinators/10 members with nested sub-team and unauthorized access denial; offline retries result in one observation.
- Security/privacy/licence/local install gates are required before any feature is called complete.
