# Dotpol Product MVP and Acceptance Plan

**Status:** Proposed for Phase 0 maintainer review; not an architecture replacement.  
**Canonical context:** `docs/BLUEPRINT.md` and `docs/ROADMAP.md`.

## Intended users and first useful jobs

1. **Independent researcher / policy analyst:** imports official reports and data, asks traceable questions, saves evidence-backed briefs.
2. **Election/constituency analyst:** imports official aggregate results, compares elections with reproducible metrics, overlays versioned boundaries and publishes uncertainty-aware maps.
3. **Survey methodologist:** designs lawful instruments, processes appropriately protected samples, publishes weighted aggregate estimates and methodology.
4. **Public-policy / legislative analyst:** traces a promise, bill, speech or scheme across sources and time.

All four are eventual personas. **Select only the first as the initial MVP persona** unless maintainers change the priority. A chat UI alone is not an MVP.

## Smallest compelling end-to-end journeys

### J1 — local evidence-backed research (MVP; Phases 1–3)

**Given:** a fresh offline-capable installation and an appropriately licensed local PDF/CSV dataset.  
**When:** the user creates a project, imports a document/dataset, searches it and asks an evidence question.  
**Then:** the app can show indexed source, exact cited span/row where supported, retrieval method, uncertainty or missing-evidence result, and a saved/exportable work product. With no model installed, the app still imports/lists/filters and explains which optional AI action cannot run.

**Acceptance:** project survives restart; offline path works without paid API keys; no fabricated citations; source version and retrieval time are available; imported data remains within selected workspace.

### J2 — reproducible constituency comparison (post-MVP; Phases 2, 4, 5)

**Given:** a lawful official aggregate election dataset and compatible dated constituency boundary versions.  
**When:** user selects two elections/constituencies and compares vote share, margins, turnout, swing and maps.  
**Then:** the same IDs and source versions flow through table/map/brief; the deterministic engine produces figures; comparability warnings appear if delimitation or missing data affects results.

**Acceptance:** independent reference calculations match, missing data is explicit, boundary-version lineage is recorded, and exports reproduce metrics.

### J3 — survey-to-aggregate insight (later; Phase 6)

**Given:** lawful survey responses with a documented sampling and privacy basis.  
**When:** user validates, weights and aggregates the survey.  
**Then:** outputs include target population, sample, weights, design effects where relevant, uncertainty, suppression and reproducible run metadata.

**Acceptance:** explicit privacy controls; no default publication of small cells or respondent-level political preferences; method and tool versions saved.

### J4 — policy promise evidence trail (later; Phase 8)

**Given:** a manifesto claim and relevant official law/scheme/budget records.  
**When:** user traces claim status.  
**Then:** observed documents and dated evidence-backed assessments remain separate, contradictory evidence is visible and the user can export an auditable report.

**Acceptance:** source/authority/time are visible; no ungrounded claim presented as a resolved fact.

## MVP scope discipline

**MVP includes:** local gateway, project state, source/document/file import, evidence-linked search over local content, one research journey, basic saved brief, tests and public CI. Aim to *prove vertical integration* rather than maximize features.

**MVP excludes:** mandatory cloud accounts, live election-day monitoring, AI-automated external messaging, targeting individuals by inferred politics, team RBAC/sync, full advanced GIS studio, forecasts and complex agent swarms. These remain later roadmap work, not discarded product goals.

The Phase 1 deliverable is explicitly a *foundation milestone*, not the whole MVP. J1 becomes end-to-end only after Phase 2 ingestion and Phase 3 retrieval are usable.

## Interface and ownership review required before parallelization

Each phase must record a short `contract card` covering:

- capability ID + canonical code owner + intended import path;
- typed request/response shapes and validation, source and evidence semantics;
- stable canonical IDs, timestamp/timezone, units, locale, boundary version if relevant;
- model/provider-independent tool input/output, errors and absent-evidence states;
- API/schema version and change/migration policy;
- read/write authority, user approval and side effects;
- local/no-network behavior and failure modes;
- deterministic tests, fixtures and AI evaluation cases;
- donor version/licence/NOTICE record where needed.

Avoid hard-coded Python/TypeScript domain types owned separately by the UI and API: implement shared versioned schemas or generation only *after* an approved contract decision. Never create duplicate canonical entities for convenience.

## Phase-quality scorecard: required evidence, not guessed progress %

| Dimension | Minimum proof |
|---|---|
| Product value | Recorded user journey, working demo and failure-case demo |
| Functionality | Tested contracts and integration/smoke tests linked from PR |
| Data quality | Known-good/known-bad fixtures; official/source IDs and lineage |
| AI credibility | No-evidence abstention, citation validation, tool correctness, model compatibility |
| Security/privacy | Negative tests; scoped permissions; data classification; no secret leakage |
| Portability/cost | Local-first path tested without paid credentials; offline scenario where applicable |
| OSS compliance | Actual component licence/notice checks, provenance of reused code |
| Operability | Launch instructions, failure diagnostics, backup/reopen/restore behavior |
| UX | Accessible keyboard navigation and understandable uncertainty labels |

For each metric record a baseline, test dataset, method, owner and target **before** claiming a pass. Do not invent targets or mark 'passing' without actual runs. One missing blocking dimension means the milestone is not verified.

## Release labels

- `specified`: spec and owner exist;
- `approved`: maintainers accept requirements and contracts;
- `implemented`: code exists behind the contract;
- `verified`: tests/evaluations and local demo produce evidence;
- `released`: packaging and documentation available to actual users.

Each workstream issue/PR must use exactly one state and link artifacts proving transitions. Do not count documentation, donor forks or unchecked task lists as code delivery.

## Parallel work and review protocol

- Freeze reviewed contracts before assigning parallel implementation.
- Separate API contract, storage adapter, provider adapter, UX and domain calculations into non-overlapping PRs with owners.
- Require architecture review for overlapping capability IDs, new persistence engines, and new providers/frameworks.
- Make small migration-compatible PRs; use draft PRs for unapproved architectural choices.
- Branch protection/required reviews should be configured by repository administrators before implementation (ChatGPT collaborator does not have admin permissions).
- Record explicit owner/sign-off for security, dataset/licence handling and AI evaluation.

## India-first, internationally extensible

Prioritize connectors to authoritative public election, legislation, policy and geography sources where permissions allow. Never bake English-only names, India-only electoral hierarchy, single election system, assumed boundary stability, or fixed timezone into core entity contracts. Localized rendering and jurisdiction-specific adapters belong outside canonical IDs. Separate published official returns from estimates and operational observations.
