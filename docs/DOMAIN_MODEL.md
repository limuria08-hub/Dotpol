# Dotpol Canonical Political Domain Model v1.0

## 1. Purpose

Dotpol must use one shared political ontology across elections, surveys, GIS, policy, media, forecasting and war-room workflows.

This document defines the canonical concepts. Domain modules may create read models/views, but they must not invent competing canonical entities.

## 2. Identity rules

Every canonical entity should support:

- stable internal Dotpol ID;
- source-specific external IDs where available;
- source/evidence links;
- creation/update timestamps;
- aliases/names where relevant;
- jurisdiction/geography where relevant;
- provenance/version metadata.

Entity resolution must distinguish between:

- source records;
- canonical entities;
- aliases/identifiers;
- assertions/evidence.

Do not silently merge uncertain identities.

## 3. Geography and jurisdiction

Canonical concepts:

### Jurisdiction

Political/legal administrative authority such as country, state or other formal jurisdiction.

### AdministrativeArea

District, municipality, ward, panchayat or other administrative geography.

### ElectoralArea

Parliamentary/assembly/local electoral geography.

### Constituency

Canonical electoral constituency with identifier, jurisdiction, type and time-valid boundary references.

### PollingStation

Polling/booth geography or station metadata where public/lawful data is available.

### Microarea (proposed, ADR-0003)

Public/appropriately aggregated geographic reporting unit for polling-site facilities, logistical coverage and general issue observations. Has a stable non-personal ID, geographic version, effective dates and authoritative/source link; it is **not** a household, voter-profile or private home-location entity. Do not finalize as a canonical entity until the extension rule and ADR review pass.

### BoundaryVersion

Versioned geometry linked to an area and effective date range. Boundary history matters because delimitation changes analytical comparability.

### SpatialFeature

Generic geospatial feature for infrastructure, assets, events or imported user layers.

## 4. Political actors

### Person

Politician, candidate, office holder, public actor or other political person represented from appropriate sources.

### Party

Political party or formal electoral party entity.

### Alliance

Time-bounded alliance/coalition relationship among parties or organisations.

### Organisation

Government body, committee, civil-society organisation, institution, media organisation, think tank or other organisation relevant to political intelligence.

### Office

Political/public office.

### Membership

Time-bounded relation among person, party/organisation, office and role.

### Candidacy

A person's candidacy in a specific election contest with party/alliance status and source evidence.

## 5. Elections

### Election

Election event with jurisdiction, election type, dates and source metadata.

### Contest

Election contest for a specific electoral area/seat.

### CandidateResult

Votes/percentage/rank/outcome for a candidate in a contest.

### PartyResult

Derived/official party-level result for a contest or aggregation.

### TurnoutObservation

Official or operational aggregate turnout observation tied to geography/time/source.

### ElectionMetricRun

Reproducible calculated metric such as swing, margin or comparative result. Store formula/version/inputs rather than only final values.

## 6. Surveys and psephology

### Survey

Survey/poll/research study with field dates, sponsor/owner, methodology and geography.

### Questionnaire

Versioned survey instrument.

### Question

Canonical question/instrument item.

### ResponseRecord

Raw or privacy-appropriate collected response record where permitted.

### AggregateResponse

Aggregated response by approved analytical dimensions.

### SampleDefinition

Target population, sampling frame/design and allocation.

### WeightingSpecification

Weighting dimensions/targets/method.

### WeightingRun

Reproducible weighting execution with inputs, parameters and diagnostics.

### PollEstimate

Derived estimate with uncertainty, methodology and provenance.

## 7. Forecasting and simulation

### ModelDefinition

Versioned model specification with purpose, features/inputs and implementation reference.

### ModelRun

Concrete execution with dataset versions, parameters, code/model version and outputs.

### Forecast

Forecast result for a defined target/geography/time with uncertainty.

### Scenario

User/system-defined hypothetical assumptions.

### SimulationRun

Execution of a scenario/model including random seed where relevant and output distributions.

### CalibrationRecord

Calibration/backtesting metrics comparing previous predictions with observed outcomes.

## 8. Policy, legislation and governance

### Policy

Policy proposal/decision/program represented as a political-policy object.

### LegislativeDocument

Bill, amendment, act, ordinance, rule, regulation or other formal legislative/legal document.

### Bill

Legislative proposal with sponsors, status, versions and related proceedings.

### Amendment

Amendment linked to a legislative document.

### VoteEvent

Recorded legislative vote/division tied to participants/options where data supports it.

### Debate

Parliamentary/assembly/committee debate event.

### Speech

Speech/intervention/transcript segment linked to person/event/source.

### QuestionEvent

Parliamentary/legislative question and response.

### Committee

Legislative/government committee and membership/work products.

### GovernmentScheme

Public program/scheme with ministry/department, geography, dates and evidence.

### BudgetProgram

Budget/expenditure/program record linked to policy/scheme where evidence supports the relation.

## 9. Manifestos and promises

### Manifesto

Party/candidate manifesto or formal promise document.

### Promise

Structured manifesto commitment/assertion with evidence location.

### PromiseStatusAssertion

Time-stamped evidence-backed assessment of promise status. Keep assessments separate from the promise itself.

## 10. Media, issues and narratives

### MediaItem

Article, broadcast transcript, public post, press release or other media/public content with source/time/author/publisher.

### Issue

Canonical political/public-policy issue/topic.

### Narrative

Evidence-backed cluster/frame/theme inferred from media/public content. Narrative assignments must retain model/method provenance.

### Claim

Specific factual/public claim extracted for verification or tracking.

### Event

Political/public event linked to actors, places, issues and evidence.

### Mention

Evidence-level association among media/document content and entities/issues.

### SentimentOrStanceObservation

Model/manual-derived observation with method/model, target, confidence and source scope. Never treat inferred sentiment as ground truth without method context.

## 11. Research and evidence

### Source

External/internal origin such as website, agency, database, user file or publication.

### Dataset

Versioned dataset with schema, ownership/source and licence/access metadata.

### Document

Document/file/web content ingested into Dotpol.

### Evidence

Addressable support for a claim/result, e.g. document span, source record or dataset slice.

### ResearchProject

Workspace/project context for research and analytical work.

### WorkProduct

Brief, report, memo, dashboard snapshot, map, table, forecast pack or other deliverable.

### Citation

Structured relation from generated/derived content to evidence/source.

## 12. Operations

### Incident

Operational incident/event with geography/time/category/status/evidence.

### Task

Assigned operational/research task with owner/status/deadline/context.

### FieldUpdate

Field-provided operational observation. Must retain source/author/time/location/verification state.

### Alert

Generated rule/model/workflow alert with evidence and acknowledgement state.

### Briefing

Time-bounded synthesized intelligence package linked to underlying results/evidence.

### Proposed pre-election operational extensions (ADR-0003)

Reuse `PollingStation`, `Task`, `FieldUpdate`, `Incident`, `Source` and `Evidence`. Proposed specializations: `StationFacilityAssessment` (site inspection); `FieldAssignment` (Task); `FieldObservation` (FieldUpdate); `SyncReceipt` (idempotent offline import); `BoothReadinessSnapshot` (derived, not authoritative). No personal voter political preference entities. See [field contracts](PRE_ELECTION_MICROAREA_INTELLIGENCE.md).

## 13. Provenance and execution

### TransformationRun

Deterministic data transform execution.

### ToolRun

Invocation of a Dotpol tool with inputs/outputs/version.

### AgentRun

Agent orchestration run linked to model/tool runs.

### WorkflowRun

Automation/workflow execution.

### Assertion

Evidence-backed statement about an entity/result when confidence/source semantics matter.

## 14. Relationship examples

```text
Person --member_of--> Party
Person --holds--> Office
Person --candidate_in--> Contest
Contest --for--> Constituency
Contest --part_of--> Election
CandidateResult --result_for--> Candidacy
Survey --covers--> Geography
PollEstimate --derived_from--> Survey/WeightingRun
Forecast --targets--> Contest/Party/Constituency
Bill --concerns--> Issue
Speech --made_by--> Person
Speech --part_of--> Debate
Promise --from--> Manifesto
Promise --concerns--> Issue/Policy
MediaItem --mentions--> Person/Party/Issue/Event
Narrative --supported_by--> MediaItem/Evidence
Incident --located_in--> Geography
WorkProduct --cites--> Evidence
```

## 15. Temporal rule

Political data is highly time-dependent. Memberships, boundaries, party alliances, candidacies, office holding, policies and promises should use effective time ranges when relevant.

Never overwrite historical state merely because a current state changed.

## 16. Geometry rule

Geography identity and geometry versions are separate concepts. A constituency can persist as a conceptual unit while its boundary changes; analytical runs must record the boundary version used.

## 17. Privacy/individual data boundary

Person-level data should be limited to legitimate public/person/entity research or lawful operational records. Dotpol's AI decision layer is not designed to infer or target named individuals by private political preference.

Forecasts, segmentation and campaign/political intelligence should prioritize aggregate geography, public political actors, survey cohorts and appropriately governed operational data.

## 18. Extension rule

Before adding a new canonical entity:

1. Prove the concept cannot be represented as an existing entity + relationship/assertion.
2. Identify at least two workflows that need the entity, unless the domain requirement is intrinsically atomic.
3. Define identifiers, temporal semantics and provenance.
4. Update this document and the capability/data contracts through an ADR if the change is architecture-significant.


## Proposed hierarchical collaboration extension (2026-10-29; ADR-0004)

Do not create a second CRM or duplicate task database. The hierarchical team feature extends authorized operations:

- `Organization`: account/workspace owner with membership and security settings.
- `Team`: stable ID, `organization_id`, optional `parent_team_id`, explicit membership/role policy and lifecycle state. A geographic unit is a reference, not a hierarchy substitute.
- `TeamMembership`: user/team role association, effective dates and explicit invite/approval history.
- `RoleGrant` / `Delegation`: allowed action, resource scope, issuer, expiry and revocation state; child-team admins cannot grant more than they possess.
- `ProjectAccess`: resource/project-level visibility separate from merely belonging to an ancestor team.
- `TeamEvent`: immutable timestamped membership, assignment, escalation and permission-change event; audit links to existing Source/Evidence/ToolRun where needed.
- Existing `Task`, `FieldUpdate`, `Incident`, `Alert` and `SyncReceipt` continue to be canonical. Do not clone them into `warroom` or an external field service.

**Security invariants:** prevent team cycles; configure nesting/membership limits; deny by default; authorization is checked server-side for every read/export, aggregated view and synchronization; revoked devices and cross-team leaks are negative tests. Offline submissions have idempotency keys, observed/received timestamps, conflict status and supervisor review. Stage these definitions behind the existing domain-model extension process; names are proposed, not migrated data tables.
