# ADR-0001: Foundation API and canonical capability ownership

- **Status:** Accepted planning architecture — implementation and package import verification pending
- **Date:** 2026-10-15
- **Owners:** Unassigned; architecture maintainer to approve
- **Related capabilities:** AI model gateway, tool registry, source registry, provenance, local persistence, API gateway

## Context

`docs/ARCHITECTURE.md` and `docs/CAPABILITY_REGISTRY.md` assign reusable AI/data/provenance capabilities to `platform/`. The existing Phase 1 implementation plan places `ai/`, `sources/`, `provenance/` and `tools/` under `services/api/dotpol_api/`. Without an explicit distinction, parallel contributors could implement the same capability twice, or later introduce a costly package extraction.

## Constraints

Preserve local-first, ₹0-core, one-owner, modular Python + FastAPI, typed contracts, tests and provenance. Do not add a second API server, storage engine, provider gateway or framework.

## Options considered

**A — Gateway composition and transport only; canonical reusable packages in `platform/` from the outset (recommended).**  
Pros: matches registry, prevents split-brain ownership and enables future workers/server mode. Cons: slight packaging/import setup in Phase 1.  
`services/api`: FastAPI lifecycle/routes, wiring, config and deploy surface.  
`platform/ai`: provider-neutral model adapter and tool contract/orchestration.  
`platform/data`: source registry and storage-independent data contracts.  
`platform/provenance`: evidence/run models and ownership.  
`platform/storage` or explicitly registered data persistence adapter: local SQLite/filesystem implementation after selecting owner.  
`packages/contracts`: versioned cross-language/API schemas where justified, not a second canonical domain model.

**B — Keep implementations in `services/api` initially with explicit canonical ownership and pre-agreed extraction plan.**  
Pros: fastest single-package bootstrap. Cons: more churn as reusable capabilities are consumed by other service/worker entry points. Must prohibit parallel `platform/` implementations.

**C — Have both `services/api` and `platform/` implement them.**  
Rejected: directly violates one capability/one owner.

## Decision

Select **A** as the canonical foundation layout. `services/api` composes the platform capabilities and provides FastAPI interfaces, rather than being a second system of record. No full code scaffold is requested by this ADR. The Phase 1 *file paths* must align with this ownership rule before implementation; do not blindly execute outdated path examples.

## Consequences

- Clean responsibility boundaries reduce duplicate engineering and make tests reusable.
- Project/lifecycle API tests remain owned by the gateway; source/provenance/model tests by their platform module.
- Any data read/write passes through one ownership contract even if the API and local backend run in a single process.
- Commit/PR scopes can be split by capability without competing subsystems.

## Migration impact

There is no production code to migrate on the inspected `main` branch as of this review. Update `docs/superpowers/plans/2026-10-15-dotpol-foundation.md`, `architecture/capabilities.yml`, `docs/CAPABILITY_REGISTRY.md` and import/dependency diagrams together *if and when accepted*. The choice of local-storage adapter owner also needs recording; do not silently add it as a new canonical capability.

## Duplication impact

Prevents `services/api/dotpol_api/ai` vs `platform/ai`, separate source/provenance registries and accidental second gateway/tool registry.

## Verification

- Architecture test/import scan shows domain modules never import provider SDKs and routes do not calculate domain statistics.
- Each capability ID maps to one canonical implementation path.
- One SQLite source registry serves API and agent tooling and survives restart.
- Tests run locally in a no-API-key configuration.
- No parallel packages provide the same canonical entity or tool registry.

**Planning decision accepted; no product code exists and no test, licence or deployed-integration result is implied.**
