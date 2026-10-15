# Dotpol Open-Source and Zero-Cost-Core Policy v1.0

## 1. Purpose

Dotpol is an open-source project and should remain free to build and capable of running locally without mandatory paid services.

This policy is architectural. It does not replace project-specific legal review when required.

## 2. Proposed Dotpol project licence

**Current recommendation:** Apache License 2.0 for Dotpol-authored code.

A root `LICENSE` should be added only after maintainers explicitly approve the project licence decision.

Reasons for the Apache-2.0 recommendation include broad commercial/open-source usability, an explicit patent grant, and standard NOTICE/attribution mechanisms.

## 3. Preferred dependency licences

Prefer:

- Apache-2.0;
- MIT;
- BSD-2-Clause;
- BSD-3-Clause;
- similarly permissive licences after review.

Other licences are not automatically prohibited, but they require explicit architecture/licence review before becoming part of Dotpol core.

## 4. Component-level review

Never assume a permissive top-level repository means every included component/model/service has the same licence.

Before adoption:

- pin exact repository and version/commit;
- inspect root licence;
- inspect subdirectory/component licences;
- inspect model/data licences where relevant;
- inspect bundled services;
- inspect attribution/NOTICE obligations;
- record decision in donor registry.

## 5. Zero-cost core rule

Core Dotpol must not require:

- a paid LLM API;
- paid cloud database;
- paid vector database;
- paid map provider;
- paid search provider;
- paid authentication service;
- paid workflow platform;
- paid analytics/BI product;
- mandatory commercial data vendor.

Optional paid integrations are allowed only when a free/local path remains available or the feature is clearly optional.

## 6. AI providers

Dotpol must support local/open models as a first-class path.

Commercial AI APIs are BYOAI integrations. Dotpol must not carry the user's provider inference bill as a core architectural requirement.

Provider-specific features should remain behind adapters.

## 7. Search providers

Core search must work over local/indexed/connected data without a commercial web-search API.

Web search providers such as commercial search APIs may be optional plugins/adapters.

Copyleft or source-available search systems may be supported as separately deployed/user-managed integrations only after reviewing architectural/licence consequences.

## 8. Maps

Core mapping must not require Mapbox/Google Maps billing.

Use open renderer/data-provider abstractions and permit:

- open/public tile providers where terms permit;
- self-hosted/offline tiles;
- user-configured tile providers;
- local GeoJSON/GeoParquet/tile packages.

## 9. Surveys/field tools

Do not assume all products from one vendor/project use one licence.

For example, when using an open form runtime, separately verify visual designer/creator licensing. Dotpol should own its survey-authoring UX if doing so avoids a mandatory commercial component.

## 10. Source-available software

Source visibility is not equivalent to open-source/permissive licensing.

Do not vendor or embed source-available/commercially restricted software into Dotpol core merely because its code is on GitHub.

## 11. Copyleft software

Copyleft software can be excellent and useful, but adoption into Dotpol core must be deliberate.

Questions to resolve before adoption:

- linking/derivative-work implications;
- network-use obligations where applicable;
- distribution requirements;
- compatibility with Dotpol's chosen project licence;
- whether external interoperability is cleaner than embedding.

## 12. Donor code attribution

For assimilated donor code:

- retain required copyright notices;
- retain required licence text;
- record source repository and commit/tag;
- document modified files where practical;
- maintain `THIRD_PARTY_NOTICES.md` once code assimilation begins.

## 13. Data licensing

Open-source code does not grant permission to redistribute arbitrary datasets.

Each connector/dataset should record:

- source;
- terms/licence;
- redistribution permissions;
- attribution requirements;
- update date/version;
- access restrictions.

User-supplied datasets remain governed by the user's rights/obligations.

## 14. Model licensing

Local/open model weights have their own licences/acceptable-use terms.

Dotpol should not bundle model weights by default unless redistribution and intended use are clearly permitted.

Model adapters can allow users to install/configure models separately.

## 15. CI enforcement target

Later hardening phases should add:

- dependency licence inventory;
- SBOM generation;
- prohibited-licence checks;
- third-party notice generation/review;
- dependency lock/pin strategy;
- security/dependency updates.

## 16. Cost classification

Every new external service/dependency proposal should record:

```text
software licence cost:
hosting requirement:
API/inference cost:
storage/bandwidth cost:
free/local alternative:
mandatory or optional:
```

A core capability proposal without a viable zero-cost/local path requires explicit maintainer approval and an ADR.
