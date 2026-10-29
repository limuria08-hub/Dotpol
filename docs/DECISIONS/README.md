# Dotpol Architecture Decision Records (ADRs)

Dotpol uses ADRs to prevent repeated architecture churn and undocumented framework changes.

## When an ADR is required

Create an ADR before changing any project-wide decision involving:

- local-first runtime model;
- zero-cost-core guarantee;
- operational/analytical storage strategy;
- canonical political domain model;
- model gateway;
- agent framework;
- retrieval/RAG architecture;
- GIS stack;
- analytical workbench/statistics stack;
- workflow engine;
- major donor classification;
- licensing policy;
- plugin/security model;
- provenance contract;
- deployment architecture.

Small implementation details within an already approved capability normally do not need an ADR.

## File naming

```text
0001-short-decision-title.md
0002-next-decision.md
```

Numbers are sequential and never reused.

## ADR template

```markdown
# ADR-NNNN: Title

- Status: Proposed | Accepted | Superseded | Rejected
- Date: YYYY-MM-DD
- Owners:
- Related capabilities:

## Context

What documented requirement/problem requires a decision?

## Constraints

Local-first, zero-cost, licence, performance, compatibility and roadmap constraints that apply.

## Options considered

### Option A
Pros / cons / licence / migration / operational impact.

### Option B
Pros / cons / licence / migration / operational impact.

## Decision

What is being chosen and why?

## Consequences

Positive and negative consequences.

## Migration impact

Files/modules/data/contracts affected and transition plan.

## Duplication impact

What old/parallel implementation is removed or prevented?

## Verification

Tests/benchmarks/evaluations that will demonstrate the decision works.
```

## Decision standard

A core change should not be accepted merely because a new project is more popular or recently released.

It should demonstrate at least one of:

- current architecture cannot meet a documented requirement;
- current architecture has unacceptable licence/security/reliability risk;
- alternative provides a clear measurable improvement worth migration cost;
- upstream project is abandoned/incompatible and creates a maintenance risk.

Every accepted ADR must update the affected blueprint/capability/donor documents in the same change.

## Current execution structure

- [ADR-0004 — Five-phase execution and optional service isolation](0004-five-phase-execution-and-service-isolation.md) defines the consolidated P1–P5 delivery structure. Old 0–12 numbering survives only as milestone/test references; the selected stack is unchanged unless another ADR explicitly replaces it.
