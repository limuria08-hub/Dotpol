# Dotpol Data Architecture v1.0

## 1. Goals

Dotpol data architecture must be:

- local-first;
- portable;
- reproducible;
- source-aware;
- versioned;
- evidence/provenance friendly;
- capable of scaling to team/server mode without rewriting political domain logic.

## 2. Default local storage

### SQLite — operational state

Use for lightweight local application metadata such as:

- projects/workspaces;
- conversations/session metadata;
- source registry;
- connector configuration metadata;
- capability/plugin registry;
- tasks/alerts;
- local user/settings;
- provenance indexes where appropriate.

### DuckDB — analytical engine

Use for:

- election datasets;
- survey data/cross-tabs;
- media/event analytical tables;
- policy/governance datasets;
- transformations over Parquet/CSV/JSON;
- ad hoc analytical queries;
- reproducible analytical views.

### Parquet — portable analytical storage

Preferred for large typed/tabular local datasets and snapshots.

### Filesystem — documents/assets

Use for:

- PDFs and documents;
- attachments;
- exports;
- GeoJSON/GeoParquet/PMTiles/MBTiles and related map assets;
- model artifacts where appropriate;
- caches that can be safely regenerated.

### Embedded vector store

Semantic retrieval must sit behind a Dotpol adapter. LanceDB is the preferred current candidate because an embedded/local mode fits the architecture. The rest of Dotpol must not depend on LanceDB-specific APIs directly.

## 3. Team/server expansion

PostgreSQL and shared object/file storage may be introduced for shared/team deployments. Domain and platform contracts should allow local adapters to be replaced by server adapters without changing domain semantics.

Do not require PostgreSQL for first-run personal mode.

## 4. Data layers

```text
Raw Source
   ↓
Source Snapshot / Import
   ↓
Validated Staging
   ↓
Canonical Entities + Datasets
   ↓
Derived Analytical Tables
   ↓
Model/Transformation Runs
   ↓
Results / Work Products
```

Never erase raw/source lineage when producing canonical or derived data.

## 5. Source registry

Every external/internal source should track, where relevant:

- source ID;
- source type;
- title/name;
- URL/location;
- publisher/owner;
- licence/access terms;
- jurisdiction;
- retrieval/import time;
- connector/version;
- checksum/hash;
- update cadence;
- reliability/authority metadata where methodologically justified.

## 6. Dataset registry

Every analytical dataset should support:

- dataset ID;
- schema/version;
- source IDs;
- creation/import timestamp;
- time coverage;
- geography coverage;
- licence/access classification;
- checksum or immutable version reference;
- transform lineage;
- quality diagnostics;
- sensitivity/privacy classification where applicable.

## 7. Ingestion

`dlt` is the v1 primary ingestion framework candidate. It should be wrapped by Dotpol connector contracts rather than exposed as the domain API.

Connector responsibilities:

- authentication/provider configuration;
- source discovery;
- incremental sync where available;
- schema mapping;
- source snapshot metadata;
- raw/staging write;
- validation;
- error/retry behavior;
- provenance registration.

Do not install a second ingestion framework until a documented connector requirement cannot reasonably be satisfied.

## 8. Connector priority

1. User files/local databases.
2. Official structured/open sources.
3. Documented public APIs/feeds.
4. Openly licensed datasets.
5. Web search/retrieval.
6. Optional commercial providers.

India-first connector families should eventually include official election, legislative/parliamentary, law/regulatory, open-government-data, census/statistical and related public sources where available.

## 9. Data contracts

Each canonical dataset/entity contract should define:

- required fields;
- optional fields;
- identifiers;
- units;
- enumerations;
- null semantics;
- geographic reference;
- temporal reference;
- source/provenance reference;
- validation rules.

Use typed schemas. A connector maps source-specific data into these contracts; domains do not consume arbitrary provider-specific structures directly.

## 10. Geography/boundaries

Boundary data must be versioned separately from geography identity.

Analytical outputs using boundaries must store the boundary version/reference. Supported import targets should eventually include GeoJSON, GeoParquet, common shapefile conversions and tile packages where appropriate.

## 11. Documents

Docling is the preferred document-processing dependency for supported formats.

Document pipeline:

```text
Document/file
 -> source registration
 -> parsing
 -> structural extraction
 -> chunks/spans
 -> metadata/entities
 -> local index/vector representation
 -> evidence-addressable retrieval
```

Generated answers should cite addressable evidence, not only the parent filename.

## 12. Provenance model

Derived output should be able to link to:

- source/evidence IDs;
- dataset version/hash;
- query/filter specification;
- transformation run;
- engine/tool version;
- model definition/run;
- parameters;
- boundary version;
- timestamps;
- code/version where relevant.

## 13. Deterministic run registry

Statistical, forecasting, simulation and transformation outputs should be reproducible through run records.

A run record should include:

- run ID;
- input dataset versions;
- code/model version;
- configuration/parameters;
- random seed where applicable;
- started/completed timestamps;
- outputs;
- diagnostics/errors;
- environment/version metadata where necessary.

## 14. Data quality

Data-quality checks should cover:

- schema validity;
- duplicates;
- impossible ranges;
- missing critical fields;
- inconsistent totals;
- broken geographic references;
- stale versions;
- source conflicts;
- unexpected category drift;
- survey response-quality diagnostics.

AI can assist in detection/explanation, but deterministic validations remain explicit.

## 15. Search and retrieval

V1 retrieval should combine:

- structured filters;
- full-text search;
- semantic/vector retrieval;
- reranking;
- canonical entity links;
- evidence references.

Graph-RAG frameworks are experimental/reference until evaluation proves enough value to justify added complexity.

## 16. Portability

A local Dotpol project should be exportable/importable without depending on a hosted account.

Long-term project-package design should include:

- project metadata;
- source registry;
- local datasets/snapshots as allowed;
- documents as allowed;
- analytical configurations;
- run metadata;
- work products;
- provenance.

## 17. Sensitive/private data

Do not commit private datasets to the public repository.

Local/private datasets should remain on the user's machine by default. Any future team sync must have explicit permissions, encryption/transport controls and access auditing.

Individual-level political preference inference is not a target for the AI decision layer. Analytical models should emphasize aggregate geography, survey cohorts and appropriately governed operational data.

### Proposed pre-election microarea/field-data rules (ADR-0003)

Station/microarea mapping is an **aggregate/public-site geography** problem, not authorization for named-voter or household targeting. Field assignments, site conditions, source-vetted public issues and verified operational status should reuse canonical `PollingStation/BoundaryVersion/Source/FieldUpdate/Task` and record site coordinates, not people/home GPS. Sensitive survey answers and opt-in accessibility service contact requests require a separate documented purpose, access and retention; they may not be joined into political profiles. Offline uploads need idempotent receipts and collected/received timestamps, verified audit trails, source licensing and suppression to prevent tiny-area re-identification. Distinguish official approximate turnout feeds, lawfully obtained statutory Form 17C records and nonofficial observer observations. See [field specification](PRE_ELECTION_MICROAREA_INTELLIGENCE.md).
