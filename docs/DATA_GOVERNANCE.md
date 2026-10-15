# Dotpol Political Data Governance and Source Intake

**Status:** Proposed Phase 0 policy, subject to maintainer and jurisdiction-specific legal review.  
**Owners to designate:** data owner, privacy reviewer, source/licence reviewer.  
**Applies to:** connectors, documents, surveys, election datasets, geospatial layers, public media, model inputs and exports.

## Rule zero

A public URL, public election result, open-source software repository, open map or openly viewable social post is **not** automatically permission to scrape, redistribute, train models on, or process personal data. Record applicable law, source terms, publication rights and intended use *per dataset/component*.

Policy must be evaluated against the law currently in force at the time and place of processing. For India, keep a compliance register for the Digital Personal Data Protection Act, 2023, its 2025 Rules, official commencements/corrections and applicable sectoral laws; do not assert all provisions became enforceable on one date without checking current gazette notices. This is a review trigger, not legal advice.

Reference: https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa

## Data classification required on intake

| Class | Examples | Default controls |
|---|---|---|
| PUBLIC-VERIFIED | permissibly sourced published aggregate election returns, legislation, government releases | store provenance/licence, version, attribution and official-vs-derived status |
| PUBLIC-UNVERIFIED | media posts, secondary tables, disputed assertions | preserve raw item, publisher, time and confidence/dispute state; never label official |
| INTERNAL | workspaces, unreleased research, internal monitoring notes | local-only by default; no remote AI sharing by default |
| PERSONAL | names/contacts or lawful respondent/field records | necessity/purpose review, limited access, retention and deletion controls |
| SENSITIVE-HIGH-RISK | identifiable political attitudes, linked survey/precise location records, protected subjects | disallow or isolate pending specific lawful-purpose and privacy approval; no routine remote-model upload |

Classes are labels for engineering controls and do not replace legal categories. Any unknown class is treated as restricted until reviewed.

## Intake/source record contract — decide before Phase 2

Record for each imported dataset/source:

- `source_id`, publisher/authority, canonical URL/file checksum, source title and connector version;
- source type, collection method, retrieved/official publication time, coverage and update cadence;
- licence, attribution, reproduction/reuse terms, robots/API/ToS restrictions and redistribution permission;
- jurisdiction, personal-data class, intended purpose and legal/permission-review state;
- schema version, external identifiers, units, time and language conventions;
- transformations, derived dataset versions, confidence and known missing/disputed fields;
- ability to remove a source and track dependent outputs.

**Intake gate:** unknown licence or permitted use blocks redistribution/automated assimilation, not basic metadata cataloguing. Preserve uncertainty rather than manufacturing an approval.

## Purpose limitation, storage and export

- Collect only fields necessary for a documented research/analytical purpose. Do not silently join public and private datasets to infer individual political preferences.
- Survey individual records must have explicitly documented collection/use basis, access restrictions and retention; high-risk identifiable political responses are not shipped in sample fixtures.
- Workspace imports are local by default. User-initiated BYOAI exports require a preview of which context would be transmitted, explicit consent/approval and vendor-independent provider routing.
- Specify per-class/default retention and deletion behavior before personal-data ingestion; do **not** pick arbitrary durations in code. Consider deletion propagation to indexes/caches/vector stores and saved work products.
- Support project export/erase at the proper roadmap phase; ensure backups and exports preserve licence restrictions rather than leaking restricted datasets.
- Provenance may need to retain non-identifying tombstones after deletion: keep only fields legally necessary and avoid reconstructing deleted personal content.
- Enforce least privilege when team sync/RBAC eventually arrives. No public upload or shared link for internal/personal records by default.

## Aggregate/statistical publication controls

- Distinguish official returns, raw survey counts, weighted estimates, simulations, derived statistics and agent-generated interpretation.
- Predefine minimum cell-size/suppression and complementary suppression policy for respondent cohorts **before** releases. Escalate re-identification risk from repeated queries, small geographical units or longitudinal joins.
- Record sample frame, response rates, weighting design, missingness, confidence/credible intervals, model versions, boundary versions and validation method where appropriate.
- A model can forecast aggregates or public outcomes; individual-level political persuasion/inferred-vote targeting is out of scope for the AI decision layer.
- Interpret media stance/sentiment as model-derived observations with method and confidence, not private beliefs or fact.

## Political and geographic data versioning

- A constituency's stable identity and geometry version are distinct. Delimitation can invalidate raw time-series comparison; preserve effective dates and boundary crosswalk methodology.
- Record provisional/final/amended results and retrieval timestamp rather than overwrite prior published source versions.
- Avoid a single universal list of administrative/election levels; use jurisdiction-specific schema mappings.
- Maps must display proper attribution and use an authorised tile/data source. OpenStreetMap data availability does not make OpenStreetMap Foundation's public tile servers a free bulk/offline tile service. No bulk prefetch from OSMF tiles; supply local/self-hosted or appropriately licensed offline packages.

OSMF tile policy: https://operations.osmfoundation.org/policies/tiles/

## Source reliability / conflict states

Each claim and analytical output should expose:

1. `observed`, `derived`, `forecast`, `inferred` or `unknown`;
2. source type and evidence span/record;
3. publication/retrieval time and data version;
4. validity and verification states: verified, unverified, disputed, outdated, or withdrawn;
5. uncertainty and method when relevant.

When two sources disagree, retain both and create an explicit reconciliation assertion, not destructive overwrites. When evidence is unavailable, show a missing-evidence state.

## Required phase gates

**Phase 0:** classify data, appoint reviewers, confirm this policy and the India legal-review checklist.  
**Phase 1:** safe local project storage and paths; private/remote provider boundary; delete/export plan; prohibit checked-in private fixtures; source metadata supports classification.  
**Phase 2:** validate intake contracts, source terms and schema quality, duplicate/version handling and sensitive-data handling before connector adoption.  
**Phase 3:** evidence spans, citations, retained provenance, invalid/withdrawn source behavior and privacy-aware retrieval.  
**Phases 4–9:** boundaries, sampling, model methods, fairness, uncertainty, provenance, acceptable dissemination.  
**Phases 10–12:** access controls/audit, sync and disclosure review; retention and compliance tests for release.

## Review checklist for each new dataset or connector

- [ ] Legitimate purpose, data classification, permission/licence and attribution recorded.
- [ ] Personal information minimised; high-risk processing separately reviewed.
- [ ] Raw snapshot, versioned transform and schema validation defined.
- [ ] Geographic/time/identity alignment and source conflict cases tested.
- [ ] Export/reuse/offline map terms compatible with product.
- [ ] Retention/delete expectations and downstream lineage considered.
- [ ] One canonical owner and approved capability ID; no hidden shadow database.
- [ ] Legal/review sign-off documented where appropriate.

No dataset or donor may be described as adopted merely because it appears in a planning registry.
