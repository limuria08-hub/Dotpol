# Contributing to Dotpol

Dotpol is an open-source, local-first political intelligence platform. Contributors should optimize for reuse, clarity, evidence, and long-term maintainability rather than feature count.

## Before you contribute

Read `AGENTS.md` and the documents under `docs/` before opening implementation work.

The current project phase is architecture-first. Do not begin large feature work unless the relevant capability owner, data contracts, donor strategy, and roadmap prerequisites are already defined.

## Contribution workflow

1. Identify the capability in `docs/CAPABILITY_REGISTRY.md` and `architecture/capabilities.yml`.
2. Confirm the owning module.
3. Check whether the capability already exists.
4. Check `docs/DONOR_MATRIX.md` for reusable OSS.
5. If a new major architectural dependency is needed, propose an ADR before implementation.
6. Keep changes focused and reviewable.
7. Add or update deterministic tests.
8. Add AI evaluation cases where an agent/model behavior changes.
9. Record provenance/lineage behavior where the change consumes evidence or data.
10. Update relevant documentation and donor/licence records.

## Pull-request expectations

A PR should explain:

- problem being solved;
- owning capability/module;
- architecture impact;
- donor/dependency changes;
- licence implications;
- tests/evaluations run;
- local-first behavior;
- migration implications;
- relevant ADR, if any.

## Architecture change rule

Do not replace a core technology or duplicate a subsystem because an alternative framework is fashionable or newly released.

Core architecture changes require evidence that the current design cannot meet a documented requirement, creates unacceptable security/licence/performance risk, or that the replacement provides a meaningful measurable improvement.

Use `docs/DECISIONS/` for Architecture Decision Records.

## Open-source reuse

Dotpol follows a reuse-before-build philosophy.

Permissive projects are preferred, especially MIT, Apache-2.0, BSD-2-Clause and BSD-3-Clause. Other licences require explicit review before adoption.

Do not copy code simply because it is visible on GitHub. Record the exact source and licence before assimilation.

## Local-first requirement

Every core feature should be designed so a user can operate Dotpol on their own machine without mandatory cloud infrastructure.

Optional hosted services and premium AI/search providers are integrations, not requirements.

## Code quality direction

- Prefer typed contracts and small modules.
- Prefer adapters around external projects/providers.
- Keep political domain logic separate from infrastructure.
- Keep agent prompts/orchestration separate from deterministic engines.
- Keep canonical domain entities consistent across modules.
- Avoid premature microservices; start with a modular local architecture.
- Prefer explicit provenance and reproducibility over hidden magic.

## Security and data

Do not commit secrets, real API keys, private political datasets, personally identifying field datasets, or credentials.

Fixtures and demos should use synthetic or clearly public data.

## Scope boundary

Dotpol's AI intelligence should focus on aggregate/geographic/cohort political analysis, surveys, policy, legislation, media, research, operations, forecasting, and decision support. Individual-level political persuasion or inferred-vote targeting is not a target architecture for the AI decision layer.

## Documentation is part of the product

When a contribution changes a capability, architecture decision, donor, data model, AI tool, or roadmap gate, update the relevant repository documentation in the same PR.
