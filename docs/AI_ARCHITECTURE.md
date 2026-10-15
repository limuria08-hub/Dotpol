# Dotpol AI Architecture v1.0

## 1. Objective

Dotpol is AI-native, but not AI-dependent for deterministic truth. AI should be embedded across research, search, GIS, surveys, policy, forecasting, media and operational workflows while critical calculations and state remain auditable.

## 2. Core rule

```text
AI reasons.
Tools retrieve.
Engines calculate.
Data proves.
Provenance explains.
```

No agent should manufacture a deterministic result that a tool/engine can compute.

## 3. One model gateway

All model access flows through one Dotpol-owned interface.

Supported provider classes should include:

- local models;
- OpenAI-compatible local endpoints;
- Ollama;
- optional MLX/llama.cpp adapters;
- BYOAI commercial providers;
- OpenAI/Anthropic/Google/OpenRouter/others through replaceable adapters.

Domains and agents must not directly import provider SDKs.

LiteLLM OSS is a candidate implementation dependency for multi-provider routing, but Dotpol owns the interface.

## 4. Local-first model policy

A valid configuration must support local-only AI.

Suggested workload routing:

### Local models first where adequate

- classification;
- extraction;
- tagging;
- simple summarisation;
- query routing;
- document metadata;
- structured cleanup;
- local private-data workflows.

### Optional stronger BYOAI models

- difficult multi-source reasoning;
- complex research synthesis;
- sophisticated report drafting;
- hard tool-planning tasks.

Users choose providers and bear their own optional API costs.

## 5. Agent framework

V1 uses one agent framework: **PydanticAI**, unless an ADR changes the decision.

Do not add LangGraph/CrewAI/AutoGen/etc. to production simply to experiment.

If a specific stateful orchestration requirement cannot be met cleanly, document it and evaluate alternatives through an ADR.

## 6. Agent family

Expected specialist agents:

- Research Agent;
- Election Agent;
- Survey/Psephology Agent;
- GIS Agent;
- Statistics Agent;
- Forecast Agent;
- Scenario Agent;
- Policy Agent;
- Legislative Agent;
- Media/Narrative Agent;
- Field Operations Agent;
- Data Quality Agent;
- Report Agent;
- War Room Agent.

These are configurations over shared tools/platform services, not independent software stacks.

## 7. Tool architecture

Agents access capability-owned tools such as:

- `SearchTool`;
- `DocumentSearchTool`;
- `DatasetQueryTool`;
- `MapQueryTool`;
- `StatisticsTool`;
- `SurveyAnalysisTool`;
- `ElectionAnalysisTool`;
- `ForecastTool`;
- `ScenarioTool`;
- `PolicySearchTool`;
- `LegislationTool`;
- `MediaAnalysisTool`;
- `ReportTool`.

Names are conceptual until implementation plans define exact interfaces.

Tools call domain/platform engines. They do not hide duplicate logic in prompts.

## 8. Example execution

User asks:

> Compare two constituencies, explain the swing, and simulate a 3-point turnout change.

Correct flow:

```text
Election Agent
 -> resolve constituencies
 -> ElectionAnalysisTool
 -> deterministic swing/turnout calculations
 -> ScenarioTool
 -> simulation engine
 -> provenance bundle
 -> agent synthesises explanation
```

Incorrect flow:

```text
Prompt model to estimate swing and scenario result from prose.
```

## 9. Retrieval

V1 starts with hybrid retrieval:

- structured query/filtering;
- local full-text retrieval;
- semantic/vector retrieval;
- reranking;
- canonical entity/evidence links.

Do not ship multiple graph-RAG frameworks in parallel.

LightRAG and GraphRAG remain evaluation/reference donors until benchmark results justify one.

## 10. Generative search

Dotpol search should combine, depending on the request:

- local project data;
- documents;
- structured political datasets;
- connected official sources;
- optional public web search;
- optional user-selected commercial search provider.

Vane is a donor/reference for generative-search patterns, but Dotpol owns search-provider abstractions and result/provenance contracts.

## 11. Structured output

Agents should prefer typed/validated structured outputs for:

- entity extraction;
- tool calls;
- classifications;
- analytical requests;
- workflow plans;
- report sections with evidence references;
- alerts.

Free-form text is appropriate for explanation, not core state.

## 12. Memory

Agent memory must distinguish:

- conversation state;
- project knowledge;
- canonical political entities;
- user-supplied data;
- durable workflow state.

Do not make chat history the canonical database.

## 13. Provenance

Agent outputs should retain links to tool runs and evidence.

For important generated claims, store where practical:

- source/evidence IDs;
- tool run IDs;
- model/provider/model version;
- prompt/template version where material;
- generation timestamp;
- structured result IDs;
- confidence/uncertainty inherited from engines.

## 14. Evaluations

AI capabilities require evaluation suites under `evaluations/`.

Evaluation categories should include:

- citation/evidence correctness;
- tool selection;
- refusal to fabricate missing data;
- structured-output validity;
- entity-resolution quality;
- extraction precision/recall where measurable;
- research completeness;
- local-model compatibility;
- prompt-injection/tool-security cases;
- cost/token metrics for optional remote providers.

`promptfoo` is a candidate evaluation dependency, but exact tooling can be introduced with the phase that owns evaluation infrastructure.

## 15. Hallucination policy

When required data is unavailable:

- state the gap;
- show what sources were checked when possible;
- do not substitute invented numbers;
- allow the user to connect/import data;
- distinguish observed, derived, forecast and inferred values.

## 16. Political intelligence boundary

The AI layer should support deep aggregate/geographic/cohort political intelligence, public-actor research, policy analysis, surveys, forecasting, media analysis and operational support.

Individual-level political persuasion or inferred private voting preference targeting is not an objective for the AI decision layer.

### Pre-election field intelligence rules (proposed ADR-0003)

The Field Operations and War Room agents may describe authorized **site conditions**, missing assignment coverage, facility accessibility issues, verified **aggregate** geographic summaries, source conflicts and dated public turnout observations. AI does not create an authoritative field/turnout fact, infer a named person's political preference, synthesize a voter contact score, track individual voted/not-voted status, or recommend individualized political targeting. Reviewer approval, data provenance, role limits and aggregate suppression apply equally to automated reports and human-accessible tools.

See [pre-election field specification](PRE_ELECTION_MICROAREA_INTELLIGENCE.md) and [ownership ADR](DECISIONS/0003-pre-election-microarea-operations.md).

## 17. Automation

Long-running or scheduled intelligence should use workflow infrastructure rather than keeping an agent conversation alive.

Example:

```text
Schedule/event
 -> workflow
 -> connectors/search
 -> deterministic/AI tools
 -> result/provenance
 -> briefing/alert
```

Prefect is the v1 preferred durable-workflow dependency when this phase begins.

## 18. Provider portability test

A domain/agent feature fails architecture review if it cannot be reasonably tested with a local/open provider because provider-specific assumptions leaked through the model gateway.

Provider-specific optional features may exist, but the core capability must degrade gracefully.
