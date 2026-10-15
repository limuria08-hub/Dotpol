# Dotpol Capability Registry v1.0

This registry prevents duplicate implementations. Every shared capability has exactly one owner.

Before adding code, contributors must check this registry and `architecture/capabilities.yml`.

## Platform capabilities

| Capability | Owner | Consumers | v1 direction |
|---|---|---|---|
| AI model gateway | `platform/ai` | all agents/domains | local models + BYOAI; one provider abstraction |
| Agent runtime | `platform/ai` | all agents | PydanticAI v1 |
| Tool registry | `platform/ai` | agents | shared typed tool contracts |
| Search | `platform/search` | research, elections, policy, media | hybrid local/internal/web provider abstraction |
| Semantic retrieval | `platform/search` | research/documents/agents | embedded vector adapter; no parallel RAG stacks |
| Data ingestion | `platform/data` | all connectors/domains | dlt-backed connector abstraction |
| Source registry | `platform/data` | all | canonical source/licence/version metadata |
| Dataset registry | `platform/data` | analytics/domains | versioned datasets/contracts |
| Provenance | `platform/provenance` | all | evidence, run, transform and model lineage |
| Documents | `platform/documents` | research/policy/media | Docling-backed parsing/evidence spans |
| GIS/map workspace | `platform/gis` | elections/surveys/policy/fieldops/warroom/analysts | One Kepler.gl map UI (its renderer dependencies are internal), GeoPandas backend spatial operations; one canonical geography owner |
| Analytics query engine | `platform/analytics` | all analytical domains | DuckDB |
| Analytical workbench | `platform/analytics` | analysts/domains | FINOS Perspective |
| Statistics runtime | `platform/analytics` | psephology/forecasting/research | Statsmodels/shared deterministic interface |
| Bayesian modelling | `platform/analytics` | forecasting/psephology | PyMC |
| Charts | `packages/ui` / analytics | apps/domains | one shared chart abstraction |
| Survey instrument runtime | `platform/surveys` | psephology/field | Dotpol contracts + SurveyJS form candidate |
| Offline field interoperability | `platform/surveys` | field/psephology/warroom | ODK-compatible integration first |
| Workflow automation | `platform/automation` | monitors/agents/connectors | Prefect when required |
| Auth/local identity | `platform/auth` | apps/gateway | local-first; shared RBAC later |
| Plugin/connector registry | platform/gateway | integrations | explicit manifests and capability permissions |

## Political domain capabilities

| Capability | Owner | Depends on | Notes |
|---|---|---|---|
| Political ontology | `packages/domain` + domain governance | data/provenance | canonical entities/relations |
| Constituency intelligence | `domains/constituencies` | GIS, elections, data | one canonical constituency entity |
| Election intelligence | `domains/elections` | data, GIS, analytics | results, turnout, swing, comparisons |
| Psephology | `domains/psephology` | surveys, analytics | weighting, cross-tabs, poll estimates |
| Forecasting | `domains/forecasting` | elections, psephology, analytics | models, uncertainty, calibration |
| Scenario simulation | `domains/simulation` | forecasting/analytics | reproducible assumptions/runs |
| Policy intelligence | `domains/policy` | documents/search/data | policy objects/impact/research |
| Legislative intelligence | `domains/legislation` | documents/search/data | bills, debates, votes, questions |
| Governance intelligence | `domains/governance` | data/policy | schemes/programs/outcomes |
| Manifesto intelligence | `domains/manifestos` | documents/policy | promises/status assertions |
| Media/narrative intelligence | `domains/media` | search/data/AI | topics, narratives, events, stance observations |
| Research workflows | `domains/research` | search/documents/analytics | evidence-backed research/work products |
| Pre-election field operations | `domains/fieldops` | constituencies, GIS, survey forms, Task/FieldUpdate, provenance | area/site readiness, supervised field assignments, verified aggregates and offline sync; no voter political profiles; [workstream](PRE_ELECTION_MICROAREA_INTELLIGENCE.md) |
| War-room intelligence | `domains/warroom` | fieldops + other domains + automation | composition/monitoring of same station, incident and aggregate data; not duplicate engines |

## Agent ownership

Agents live under `agents/` but consume the owners above. They do not own data/engines.

| Agent | Primary tools/capabilities |
|---|---|
| Research Agent | search, documents, datasets, citations |
| Election Agent | elections, GIS, analytics |
| Survey/Psephology Agent | surveys, psephology, statistics |
| GIS Agent | GIS/map layers/spatial queries |
| Statistics Agent | analytics/statistics |
| Forecast Agent | forecasting/model registry |
| Scenario Agent | simulation/forecasting |
| Policy Agent | policy/search/documents |
| Legislative Agent | legislation/documents/search |
| Media Agent | media/search/data |
| Field Operations Agent | authorized station/microarea observations, Task/FieldUpdate, review and aggregate reporting; no voter-level political inference |
| Data Quality Agent | data validations/diagnostics |
| Report Agent | work products + citations/provenance |
| War Room Agent | cross-domain monitoring/tools |

## Duplication examples that are prohibited

- `domains/elections/search.py` implementing another web search engine.
- `domains/policy/llm.py` calling a provider directly.
- a separate GIS database/schema for surveys when canonical geography exists.
- separate PDF parsers under policy, media and research.
- forecasting formulas embedded only in prompts.
- a war-room-specific election model duplicating `domains/elections`.
- a second vector database introduced by one agent.
- a second workflow framework for one connector.
- a separate voter/household political CRM, or booth-agent database with its own authoritative station IDs, overlapping `domains/fieldops`.
- using individual electoral-roll/private survey linkage to create political persuasion or inferred-vote scores.

## Capability proposal template

Before a new capability is approved, record:

```text
name:
problem:
owner:
consumers:
existing Dotpol capability checked:
OSS candidates checked:
donor/dependency/reference/build decision:
licence:
local-first behavior:
input/output contracts:
provenance requirements:
roadmap phase:
ADR required?:
```

## Change rule

If ownership changes or two capabilities overlap, resolve the conflict before implementation. Update this registry and `architecture/capabilities.yml` in the same change.
