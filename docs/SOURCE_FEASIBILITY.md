# India-first Official Data Connector Feasibility Matrix

**Status:** Research shortlist / planning only (2026-10-15). No connector, dataset, API credential, scraping permission or reuse licence has been approved or integrated.

**Purpose:** Avoid teams separately building election, legislative, census and policy fetchers without the canonical `platform/data` ingestion/source contracts. The same sources may serve research, policy, election, GIS and forecasts through a **single** source registry.

## Candidates and sequencing

| Candidate | Official source and example | Phase | Suitable first experiment | Unverified gates |
|---|---|---:|---|---|
| ECI statistical reports | https://www.eci.gov.in/statistical-reports | 2 + 5 | Manual download/parse one published aggregate constituency election report (PDF/XLSX), register source version and totals | Reuse/redistribution rights, stable URLs, format drift, final/amended status and electorate vs votes |
| Government Open Data Platform (OGD India) | https://data.gov.in/ and https://data.gov.in/Godl | 2 | Import one officially licensed structured dataset with source attribution | Dataset-specific attribution, API/auth terms, availability, schema and update cadence |
| Census India tables | https://censusindia.gov.in/census.website/en/data | 2 + 4 | Import published aggregate tables and align to named administrative areas | Historical boundary changes, table years, statistical suppression and permitted use |
| India Code (Ministry of Law and Justice) | https://indiacode.gov.in | 2 + 8 | Ingest one official document with dated version and paragraph citation spans | Official status, copyright/reuse/API terms, amendment/vigency/version resolution |
| Digital Sansad — Parliament | https://sansad.in/ls/dashboard and https://sansad.in/ls/questions/questions-and-answers | 2 + 8 | Link a published question/answer to its chamber/session/date/ministry and source span | Access/redistribution terms, query interfaces, updated proceedings, status distinctions |

**Keep optional and later:** policy-budget joins, regional/state legislative websites, archival PDFs, machine-translated records and public media/news connectors. These have substantially different permissions, quality and schema profiles; do not create a generic scraper and claim they are solved.

## First connector feasibility checklist (no automation yet)

1. Identify **one** canonical capability owner and source type. Confirm `docs/CAPABILITY_REGISTRY.md` and `architecture/capabilities.yml`.
2. Confirm the exact publisher/URL, access and reuse licence, attribution, API/ToS, robots/rate limits, and whether local caching and exports are allowed. Do not assume public means unrestricted.
3. Select a small, freely usable fixture; record source publication date, retrieved date, checksum, time/geographic scope, schema and data class.
4. Define minimal raw -> validated staging -> canonical entity mapping without modifying the raw source.
5. Check primary keys, amendments, duplicated identifiers, boundary/election-year versions, missing/non-standard values and exact data totals.
6. Produce a source/evidence record with transformations and a deterministically reproducible result. Distinguish **official observed** vs **derived** vs **forecast**.
7. Measure document extraction/structured parse fidelity with known-good and known-bad examples. Mark errors/conflicts and abstain from invalid claims.
8. Document offline/reopen behavior, licensing constraints for redistributed fixtures and future connector-update plan.
9. Only after independent data/privacy and technical review, propose a reusable adapter behind platform ingestion contracts.
10. Record the eventual donor/dependency selection and pinned version only if third-party code is actually adopted.

## Pilot acceptance by milestone

**Phase 2 pilot:** One approved source of each selected *data shape* (tabular and document) is imported with provenance, schema, validation failures and local reopening. Source organization alone is not a successful connector.

**Phase 3 use:** Local search answers cite an actual record/span from the same pilot with no fabricated references.

**Phase 4/5 use:** Published aggregate election data can be loaded with versioned geographical IDs and compared using independent deterministic reference calculations.

**Phase 8 use:** Official bills/schemes/questions can be linked into a dated public-policy evidence timeline without collapsing proposal, enactment, implementation and commentary into the same state.

## Risk notes

- Election Commission of India publishes official statistical reports in downloadable formats, but those should still be checked for terms/version and actual structured consistency before redistribution.
- OGD India publishes a Government Open Data License; check its terms **and** each actual resource/owner. The site currently presents a sandbox environment notice on its home page: confirm production endpoints before treating that instance as dependable.
- Census time-series may be incompatible across administrative or electoral boundary versions without documented crosswalks.
- Parliamentary records and legislation evolve; retain past snapshots/versions, publication times and contradictory/withdrawn metadata.
- Do not scrape electoral rolls, merge personal political preferences, or bulk acquire individual records under the cover of this aggregate public-data plan.

## Source review links (checked 2026-10-15)

- ECI published statistical reports: https://www.eci.gov.in/statistical-reports
- OGD India portal and Government Open Data License: https://data.gov.in/ and https://data.gov.in/Godl
- Census India: https://censusindia.gov.in/census.website/en/data
- India Code: https://indiacode.gov.in
- Digital Sansad: https://sansad.in/ls/dashboard
