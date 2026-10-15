# Dotpol Blueprint v1.0 — Independent Planning Audit

**Date:** 2026-10-15  
**Status:** Proposed review findings; not an implementation authorization  
**Baseline:** `main` — `README.md`, `docs/BLUEPRINT.md`, `docs/ROADMAP.md`, architecture/AI/data/domain/donor/licence documents, and the Phase 1 task plan.

## Executive decision

**Keep the current Phase 0–12 dependency order, local-first/₹0-core constraints, one-capability-owner model, PydanticAI v1 choice, and reuse-before-build policy.** Do not add a second framework or initiate donor forks based on this review. The principal weakness is *missing operational specificity*: who owns a contract, what the user can actually accomplish at each milestone, what risk controls must exist before ingesting sensitive data, and what test evidence closes a gate.

Repository inspection at review time found documentation, YAML planning registries, and a Phase 1 plan only; no `apps/`, `services/`, `platform/` implementation, CI workflow, or test suites on `main`. This is **not** a code-completeness claim beyond the inspected branch. Do not count roadmap items as implemented.

## Prioritized gap register

| ID | Priority | Gap / consequence | Proposed change | Owner to designate | Closure evidence |
|---|---|---|---|---|---|
| DP-01 | P0 | `services/api` Phase 1 plan vs `platform/ai,data,provenance` capability owners could produce parallel implementations | Proposed ADR-0001: services hosts API/composition; capability contracts have single canonical owners | Architecture maintainer | Approved ADR + path/import ownership table |
| DP-02 | P0 | No user-centric MVP or usable milestone defines 'value' | `PRODUCT_MVP_AND_ACCEPTANCE.md` with journeys, explicit phase slices and non-goals | Product lead | Reviewed demo scripts and acceptance criteria |
| DP-03 | P0 | Privacy/consent/retention and licensed-data handling under-specified | `DATA_GOVERNANCE.md` with acquisition and data-class gates | Data/privacy reviewer | Source and dataset intake checklist approved |
| DP-04 | P0 | Local gateway, untrusted documents, tools and GitHub CI lack concrete threat models | `SECURITY_AND_AI_ASSURANCE.md` with least privilege, abuse cases and test plan | Security maintainer | Threat model and negative-test inventory signed off |
| DP-05 | P0 | Root licence proposed but unapproved; no licence file | Maintainer decision **before** distributing assimilated code; never assume Apache-2.0 is already adopted | Repository owner | Approved licence decision + root LICENSE in separate change |
| DP-06 | P1 | API contracts, schema migration and code ownership unclear | Contract-first review for every phase, semantic/schema versions, compatibility and migration fixtures | API/data owners | Versioned interface catalog and compatibility tests in implementation phase |
| DP-07 | P1 | Data quality, source freshness and disputed assertions need product-visible states | Observed vs derived vs forecast vs inferred labels, source conflicts and uncertainty | Data/analytics owners | Golden evidence/quality evaluation datasets |
| DP-08 | P1 | Agent permissions and external side-effect approvals unspecified | Classify read/write/network/destructive tools; human approval and auditable events | AI/security owners | Agent abuse/evaluation suite incl. refusal/no-evidence paths |
| DP-09 | P1 | No cross-phase release scorecard or evidence checklist | Introduce measurable entry/exit and no-go rules, record proofs in PRs | Release owner | Phase gate checklist linked to passing CI/results |
| DP-10 | P1 | Political-data governance must handle changing law/permissions by source and jurisdiction | Legal/data review checklist, versioned policies, source terms, privacy review | Legal/privacy reviewer | Recorded decision per source/country/use case |
| DP-11 | P2 | GIS 'free' does not imply free/bulk offline tile hosting | Tile-provider adapter, attribution and offline tile licence checks | GIS owner | Offline/online provider and terms test |
| DP-12 | P2 | No explicit global team/plugin sync threat boundary | Define local-mode threat assumptions first; make remote/team-mode design a later ADR | Architecture/security | Local/team separation documented |
| DP-13 | P2 | Accessibility/localisation and low-resource India workflows lack early usability checks | Design for multilingual text, slow networks/offline, keyboard accessibility and uncertainty display | UX owner | User-journey review + accessibility acceptance notes |
| DP-14 | P2 | Donor status may be mistaken for integration or permission | Record exact upstream commit, components, notices, licence and accept/reject rationale; don't start unused forks | OSS owner | Donor review card per adopted component |

**Priority meanings:** P0 must resolve before Phase 1 implementation or data exposure as relevant; P1 is required by its owning phase; P2 is researched and gated before adoption, not a reason to stall Phase 1.

## Duplication-prevention decisions for collaborators

1. One registered owner per platform capability; `services/api` acts as a transport/composition boundary rather than an independent AI/data/provenance implementation (pending ADR-0001).
2. A domain can define only its political rules and read models; canonical identity, geography, sources, storage, maps, analytics and retrieval have shared owners.
3. An agent is a thin orchestration layer; an agent cannot own a second election calculation, document parser, search provider, persistence layer or forecast engine.
4. Provider/framework substitution requires **measured deficiency + ADR**, not a popularity-based choice.
5. Freeze interfaces at phase entry; parallel agents may develop independent units only after shared schemas and merge contracts are reviewed.
6. Mark items explicitly `proposed`, `approved`, `implemented`, `verified`, or `released`; forks/dependencies/config files are not proof of integration.

## Maintainer decisions needed before implementation

- [ ] **D1** Approve or revise product MVP/journeys; pick initial deployment persona and supported local operating systems.
- [ ] **D2** Accept/modify/reject proposed **ADR-0001** on foundation contract ownership.
- [ ] **D3** Approve project licence (Apache-2.0 is only a recommendation today); establish attribution/NOTICE policy.
- [ ] **D4** Approve privacy and sensitive-data categories, use boundaries, retention/default delete/export posture.
- [ ] **D5** Agree the Phase 1 security baseline and whether optional external AI sharing is disabled until explicit consent.
- [ ] **D6** Name maintainers/reviewers for product, API/architecture, data/privacy, AI evaluation, security, OSS/licensing and release.
- [ ] **D7** Agree canonical milestone evidence: tests, demos, fixtures, source references, licence checks and local/no-key runs.
- [ ] **D8** Decide whether Phase 1 will be reviewed as seven narrow PRs or a small grouped sequence, without weakening its dependency gates.

## Practical sequencing without premature feature work

**M0 — planning accepted:** decisions D1–D7 recorded, licence choice approved, no unresolved P0 architectural contradictions.  
**M1 — foundation:** seven Phase 1 tasks, local no-key run, persistent projects, basic source provenance, evidence-aware tool, web shell, CI.  
**M2 — first research journey:** a real, permissibly sourced local file/document becomes a canonical record and produces citation-addressable research answers; no mandatory web/commercial provider.  
**M3 — analyst validation:** one versioned aggregate election dataset feeds repeatable analytical comparisons and a map, using the same canonical IDs across modules.  
**M4 — specialist verticals:** surveys, forecasts, policy, media and war room begin only against completed platform contracts, with domain-specific acceptance evidence.  
**M5 — public release:** packaging, privacy/security validation, offline use, licences, accessibility, provenance and reproducible cross-platform CI.

The milestones are *evidence-oriented groups*, not a replacement for the 13 roadmap phases.

## Key risks / assumptions to track

| Risk | Mitigation | Trigger for revisit |
|---|---|---|
| Local-first UI still requires hidden network services | CI no-network/no-key smoke test and local default | Any new mandatory endpoint |
| Growing repo acquires duplicate abstractions | Registry + proposed ADR + PR check | New package defines overlapping source/entity/model interfaces |
| 'Public' election/media data improperly reused | Source-level ToS/licence, privacy classification, provenance | Every connector or imported dataset |
| AI emits false legal/political/election claims | Evidence/abstention/calibration tests and visible status labels | Each agent/tool feature |
| Public CI executes untrusted PR content with secrets | Unprivileged fork PR workflows; restricted token | CI redesign or privileged workflow |
| Forecast or survey release implies false precision | Held-out backtests, methodology, suppressed small cells | Each model/estimate release |
| Feature creep makes MVP unattainable | Local research and source-backed vertical slices first | Any proposed Phase 4+ early feature |

## Research and review sources (planning references, not blanket licence approvals)

- NIST AI RMF / GenAI Profile: https://www.nist.gov/itl/ai-risk-management-framework and https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
- NIST Secure Software Development Framework: https://csrc.nist.gov/projects/ssdf
- OWASP LLM/GenAI risk guidance: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- GitHub Actions security for untrusted pull requests: https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target
- MeitY Digital Personal Data Protection Rules 2025 and related commencement material (must recheck applicability/current notifications): https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa
- SurveyJS product licence distinction: https://surveyjs.io/licensing
- OSMF tile policy: https://operations.osmfoundation.org/policies/tiles/

This audit is engineering/product planning, not legal advice. Compliance obligations require jurisdiction-, data-, and feature-specific review before shipment.
