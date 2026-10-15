# Vane Module-Level Adoption Decision Matrix — Dotpol

**Review date:** 2026-10-15  
**Scope:** Source inspection and planning, **no implementation**.  
**Fork:** [kiranvbiim-coder/Vane](https://github.com/kiranvbiim-coder/Vane) (`master`, exact inspected tree `348feca3e378fb4157b217724ed508dc707f853f`); confirmed upstream [ItzCrazyKns/Vane](https://github.com/ItzCrazyKns/Vane) was at the same HEAD during this review.  
**Status:** Technical screening completed for named files; legal/transitive dependency review, reproducible execution tests, maintainers' approval and import decisions **open**.

This complements [fork verification](DONOR_EVAL_VANE.md), [Dotpol donor policy](OSS_REUSE_AND_FORK_POLICY.md), [capability ownership](CAPABILITY_REGISTRY.md), and the pending [Phase 0 audit](PLAN_AUDIT_2026-10-15.md) on another PR. An upstream MIT root licence is **not** blanket clearance for model weights, dependencies, bundled SearXNG, images, data or every module.

## Adoption statuses and criteria

- **A — selective code adaptation:** a specific MIT-eligible TypeScript/React module can be modified and embedded behind Dotpol-owned typed APIs with attribution, after exact licence/security review.
- **B — logic/UX reference:** copy the proven workflow idea, *not* its standalone server, provider or storage machinery; original Dotpol glue will be necessary.
- **C — optional external interoperability:** use the independently installed Vane service through a tightly constrained API adapter, optional and replaceable; do not pretend its output is verified Dotpol evidence.
- **D — exclude:** do not bring into Dotpol core because it duplicates an owner, undermines provenance/local security, or requires incompatible runtime/rights.
- **Deferred:** phase/feature not ready; no code transfer now.

**Screening verdict is not integration approval.** A means *candidate*, not code copied. The next approved phase can create a narrow experiment PR if licensing gates pass.

## Source-level evaluation

All source links are pinned to the **inspected fork commit**. Column 'candidate' concerns the *component*, not a blanket judgement on Vane.

| Vane source / mechanism | Function actually seen | Dotpol owner | Verdict | Explicit adoption boundary |
|---|---|---|---|---|
| [`MessageSources.tsx`](https://github.com/kiranvbiim-coder/Vane/blob/348feca3e378fb4157b217724ed508dc707f853f/src/components/MessageSources.tsx) | Card grid/modal for cited sources; file/web treatments | `apps/web` + `platform/provenance` | **A** | Adapt component to accept validated `SourceView` DTO with `source_id`, `evidence_id`, safe `href`, version and claim-link state; remove remote favicon by default; handle file links internally |
| [`Citation.tsx`](https://github.com/kiranvbiim-coder/Vane/blob/348feca3e378fb4157b217724ed508dc707f853f/src/components/MessageRenderer/Citation.tsx) | Small clickable inline citation | `apps/web` | **A** | Typed validated internal evidence link or safely allowlisted external URL; accessible label, `rel`, no user-supplied arbitrary schemes |
| [`AssistantSteps.tsx`](https://github.com/kiranvbiim-coder/Vane/blob/348feca3e378fb4157b217724ed508dc707f853f/src/components/AssistantSteps.tsx) | Collapsible search/read/research progress | `apps/web` | **A** | Use Dotpol's versioned `ResearchEvent` schema and public step descriptions; replace private/reasoning text with safe summaries |
| [`src/lib/agents/search/classifier.ts`](https://github.com/kiranvbiim-coder/Vane/blob/348feca3e378fb4157b217724ed508dc707f853f/src/lib/agents/search/classifier.ts) | Zod classifies skip, personal/academic/discussion, widget choice, stand-alone query | `platform/search` | **B** | Borrow intent categories but create owned, provider-neutral validated search policy; model classification never grants private/network permissions |
| [`src/lib/agents/search/researcher/index.ts`](https://github.com/kiranvbiim-coder/Vane/blob/348feca3e378fb4157b217724ed508dc707f853f/src/lib/agents/search/researcher/index.ts) | Speed/balanced/quality budgets of 2/6/25 iterations; tool stream; source dedup; updates UI | `platform/search` | **B** | Reuse budget/step UX pattern, not TypeScript runner, mutable source merging or separate agent framework; deterministic source IDs and ordered tool results required |
| [`src/lib/agents/search/researcher/actions/registry.ts`](https://github.com/kiranvbiim-coder/Vane/blob/348feca3e378fb4157b217724ed508dc707f853f/src/lib/agents/search/researcher/actions/registry.ts) | Dynamic action registry and `Promise.all` execution | `platform/ai` | **D** | Dotpol has one typed tool registry; current parallel result push ordering is nondeterministic; execution must return `call_id` mapping |
| [`src/lib/agents/search/researcher/actions/search/baseSearch.ts`](https://github.com/kiranvbiim-coder/Vane/blob/348feca3e378fb4157b217724ed508dc707f853f/src/lib/agents/search/researcher/actions/search/baseSearch.ts) | Multi-query search, similarity ranking, snippet vs full page by mode | `platform/search` | **B** | Benchmark ranking modes against fixtures; do not import current fallback `similarity:1`, unscoped embedding calls or unverified source merging |
| [`webSearch.ts`, `academicSearch.ts`, `socialSearch.ts`](https://github.com/kiranvbiim-coder/Vane/tree/348feca3e378fb4157b217724ed508dc707f853f/src/lib/agents/search/researcher/actions/search) | Specialized SearXNG engine/query wrappers | `platform/search` | **B/C** | Map to a single `SearchProvider` config; source-specific availability depends on user's provider and terms; research cannot require SearXNG |
| [`src/lib/searxng.ts`](https://github.com/kiranvbiim-coder/Vane/blob/348feca3e378fb4157b217724ed508dc707f853f/src/lib/searxng.ts) | SearXNG JSON client with query, category, engine, language and 10s abort | `platform/search` | **C** | Optionally interoperate with *user-managed* SearXNG via validated endpoint and timeouts, after license review; do not bundle the AGPL engine as permissive Dotpol core |
| [`src/lib/scraper.ts`](https://github.com/kiranvbiim-coder/Vane/blob/348feca3e378fb4157b217724ed508dc707f853f/src/lib/scraper.ts) | Playwright Chromium + JSDOM/Readability page extraction; launches with disabled Chromium sandbox | `platform/search` / `platform/documents` | **D (as-is)** | URL/SSRF, redirect/IP/DNS validation, browser sandbox, robots/terms, untrusted-HTML limits and audit mandatory; prefer a reviewed shared extraction adapter |
| [`src/lib/agents/search/researcher/actions/scrapeURL.ts`](https://github.com/kiranvbiim-coder/Vane/blob/348feca3e378fb4157b217724ed508dc707f853f/src/lib/agents/search/researcher/actions/scrapeURL.ts) | Agent can issue `urls: string[]`, capped to 3, then scrape and LLM-extract chunks | `platform/search` | **D (as-is)** | No URL-scheme/IP policy enforcement in this module; prompt instructions are not tool authorization; typed network read permissions required |
| [`src/lib/agents/search/researcher/actions/uploadsSearch.ts`](https://github.com/kiranvbiim-coder/Vane/blob/348feca3e378fb4157b217724ed508dc707f853f/src/lib/agents/search/researcher/actions/uploadsSearch.ts) | Search embedded uploaded chunks; URL-based merge | `platform/search` | **B** | Dotpol source/evidence IDs + chunk/span version; never concatenate unversioned snippets into one evidence record |
| [`src/lib/uploads/manager.ts`](https://github.com/kiranvbiim-coder/Vane/blob/348feca3e378fb4157b217724ed508dc707f853f/src/lib/uploads/manager.ts) | Parse PDF/DOCX/TXT, embed chunks and persist filesystem JSON index | `platform/documents` / `platform/data` | **D (as-is)** | Docling and canonical source registry already selected, avoid duplicate parser, JSON file DB and store; useful MIME/format test fixtures only |
| [`src/lib/uploads/store.ts`](https://github.com/kiranvbiim-coder/Vane/blob/348feca3e378fb4157b217724ed508dc707f853f/src/lib/uploads/store.ts) | In-memory embedding similarity and rank merger | `platform/search` | **B** | Benchmark retrieval approaches; has no persisted span/page-level provenance, and result hashing includes full score object, raising rank-fusion consistency concern |
| [`src/app/api/search/route.ts`](https://github.com/kiranvbiim-coder/Vane/blob/348feca3e378fb4157b217724ed508dc707f853f/src/app/api/search/route.ts) | POST endpoint accepts query/models, returns answer + sources or streamed events | `services/api` via `platform/search` | **C (optional)** | Evaluate as optional sidecar `ExternalAnswerProvider`, **not canonical verified retrieval**; endpoint needs validation, result/source verification, failure/time budget |
| [`src/app/api/chat/route.ts`](https://github.com/kiranvbiim-coder/Vane/blob/348feca3e378fb4157b217724ed508dc707f853f/src/app/api/chat/route.ts) | Next.js chat endpoint with own model registry, chat store, streaming | `services/api` | **D** | Duplicate FastAPI gateway, provider model gateway, SQLite schema and session handling |
| [`src/lib/models/registry.ts`](https://github.com/kiranvbiim-coder/Vane/blob/348feca3e378fb4157b217724ed508dc707f853f/src/lib/models/registry.ts) | Multiple provider adapters, config and model choices | `platform/ai` | **D** | Do not create second model registry; logging provider config may expose secret values—review future third-party integration safety |
| [`src/lib/db/schema.ts`](https://github.com/kiranvbiim-coder/Vane/blob/348feca3e378fb4157b217724ed508dc707f853f/src/lib/db/schema.ts) | Local Drizzle/SQLite chats/messages | `platform/data` | **D** | Dotpol canonical project/source/persistence contracts own the records |
| [`src/lib/prompts/search/writer.ts`](https://github.com/kiranvbiim-coder/Vane/blob/348feca3e378fb4157b217724ed508dc707f853f/src/lib/prompts/search/writer.ts) | Prompt requests bracketed numeric citations from numbered context | `platform/provenance` / `platform/ai` | **B** | Prompt is not sufficient evidence validation. Enforce source IDs, spans, quote checks, no-evidence, provenance before rendering |
| [`src/lib/agents/search/widgets/`](https://github.com/kiranvbiim-coder/Vane/tree/348feca3e378fb4157b217724ed508dc707f853f/src/lib/agents/search/widgets) | Weather/stock/calculator helper widgets | UI/shared engines | **Deferred** | Avoid mixing generic widgets with political research MVP unless user journey needs them |
| [`Dockerfile`, `Dockerfile.slim`](https://github.com/kiranvbiim-coder/Vane/tree/348feca3e378fb4157b217724ed508dc707f853f) | Default distribution bundles SearXNG; slim uses external instance | packaging | **D (bundled)** | No mandatory Docker/SearXNG/runtime in Dotpol local-first core; optional external sidecar needs user-managed setup, rights and resource validation |

## Actual code risks and required tests (do not mark 'fixed')

| ID | Priority | Code evidence and consequence | Required Dotpol design/test |
|---|---|---|---|
| V-01 | P0 | `ActionRegistry.executeAll()` uses `Promise.all` and `results.push(output)` on completion, but `researcher/index.ts` associates `actionResults[i]` with `finalToolCalls[i]`; order may differ. | Return ordered `Promise.all(map => output)` or keyed `call_id`; concurrent completion fixture verifies correct associations |
| V-02 | P0 | `writer.ts` asks for `[number]` cites, `api.ts/index.ts` interpolate raw `<result index=... title=...>` content; no evidence-ID binding in observed answer path. | Resolve immutable `SourceRecord/EvidenceRef` before prompt, validate generated citation IDs and spans; fail closed on hallucinated/withdrawn refs and injection |
| V-03 | P0 | `scraper.ts` launches Chromium with `--no-sandbox`, passes URL directly to `page.goto`; `scrapeURL.ts` accepts model-proposed arbitrary `z.string()` URLs. | SSRF/private subnet and localhost rejection, DNS+redirect checks, protocol allowlist, sandboxed worker, browser/time/bytes cap, human-approved network tool policy |
| V-04 | P0 | `src/lib/models/registry.ts` error branch logs serialized `p.config`, which may include credentials. | No raw provider-config logging; structured redaction and test sentinel keys against logs |
| V-05 | P1 | `uploads/manager.ts` stores separate extracted chunks/embeddings as local JSON, `uploads/store.ts` uses `file_id://` not stable evidence span/page IDs. | Use Docling + shared registry; store source checksum, doc/page/row span and model versions; reopen/withdrawal tests |
| V-06 | P1 | `uploads/store.ts` hashes `{chunk,score}` for rank aggregation, so identical chunks with query-dependent scores can be treated as different hashes. | Key by stable `chunk_id`; deterministic reciprocal-rank-fusion fixture and benchmark |
| V-07 | P1 | `baseSearch.ts` falls back to all results `similarity:1` on embedding failure; `researcher/index.ts` merges snippets from duplicate URL into mutable content. | Explicit retrieval-degraded state and source-span-aware dedup with stable IDs; benchmark score/rank consistency |
| V-08 | P1 | `MessageSources.tsx` modal treats file references inconsistently and loads Google favicon URLs for generic source URLs; `AssistantSteps.tsx` uses `new URL(url)` without guard. | No third-party favicon loads by default; internally resolved file IDs; safe URL parsing/link schemes and accessibility tests |
| V-09 | P1 | `src/app/api/search/route.ts` casts JSON to TS interface rather than runtime schema and starts an unawaited agent call. | At Dotpol sidecar boundary parse/validate payload, propagate errors/cancellation and enforce provider budgets |
| V-10 | P1 | `getWriterPrompt()` adds raw searched content and instructions to generated system prompt. Untrusted result content can ask agent to ignore role boundaries. | Retrieval is untrusted data, explicit data/instruction separation and injected-source prompt tests |
| V-11 | P2 | Search modes fix iteration caps 2/6/25 but not end-to-end explicit time/token/network cost budgets. | Configure per-run time/tokens/search depth/remote calls; user-visible cost/provider notices |
| V-12 | P2 | No test script in inspected Vane `package.json` and no runtime benchmark executed for this review. | Treat all findings as static code review; require actual reproducible tests before claiming adoption |

**These are static findings, not confirmed exploitable vulnerabilities.** A reviewer should reproduce potential failures with safe test fixtures and account for upstream updates before recording a security advisory or adopting patches.

## Dotpol contracts to agree before any code transfer

```text
SearchRequest {
  query, workspace_id, allowed_sources, language?, mode,
  allow_network, provider_id?, max_results, deadline_ms
}
SearchHit {
  id, source_id, evidence_ref?, url?, title, snippet,
  published_at?, retrieved_at, content_hash?, publisher?,
  access_and_licence_state, confidence_state
}
ResearchEvent {
  run_id, seq, kind[queued|searching|reading|citing|completed|error],
  public_summary, source_ids?, timestamp
}
ResearchResult {
  run_id, answer_text, citations[{claim_span,evidence_id,source_id}],
  hits[], completion_state[complete|partial|no_evidence|provider_unavailable],
  provenance_id, model_and_tool_versions?, usage?
}
```

These are **conceptual fields**: define language-neutral versioned schema after architecture ADR/ownership decision; do not treat the text above as stable released API.

### Crucial boundary: provider vs verified evidence

- If Vane is optionally run as a sidecar, its `/api/search` returns generated answer plus source URL/snippets. Such output is untrusted *third-party research content*, not a Dotpol canonical `EvidenceRef`. Reconcile, snapshot/validate source addresses, dedup and explicitly mark unverified before inclusion in a Dotpol evidence-backed report.
- A `SearchProvider` should yield *retrieval hits*, not a second canonical conversational agent. A separate `ExternalAnswerProvider` interface is justified only after accepted capability registry/ADR review and observable need.
- Local workspace query and local document research must work with no Vane process, no SearXNG, no cloud API and no commercial token.

## Decision-ready phased plan

| Sequence | Phase | Scope | Owner | PR artifact / acceptance evidence |
|---|---|---|---|---|
| **V0 — now** | 0 | Confirm fork location, module verdicts, exact licences and external backend terms; resolve contracts | Product + architecture + OSS/legal | Accepted decision record, pinned component path/commit and licence inventory |
| **V1 — after foundation** | 1–3 | Reuse/adapt `Citation`, `MessageSources`, `AssistantSteps` against mock *typed Dotpol events* | `apps/web` | Accessibility/safe-link/no-network tests, attribution |
| **V2** | 2–3 | Implement **one** `SearchProvider` abstraction with local lookup first, optionally external SearXNG provider | `platform/search` | Local no-network test, fake provider, citation/span contract validation |
| **V3** | 3 | Benchmark Vane search classification, ranking and research flow against Dotpol grounded fixtures | `platform/search` + `evaluations` | Retrieval precision, latency, cited answer validation, prompt injection and no-source abstention |
| **V4 — optional** | 3+ | Test user-managed Vane `/api/search` as optional `ExternalAnswerProvider` sidecar *if distinct value is proven* | API integration review | Isolated opt-in provider, source reconciliation, abort/time budgets, no duplicate canonical state |
| **V5** | 3+ | Integrate only chosen donor modules, notices, update plan, tested hashes | relevant single owner | Explicit adoption PR; actual integration/eval reports |

## Exact acceptance matrix before adopting any TypeScript component

- Source path + exact fork/upstream SHA + MIT copyright notice.
- Third-party library/asset and transitive-dependency licence & version inventory.
- Screenshots/interaction tests on Dotpol design system and mobile/desktop accessibility.
- Empty/missing/invalid source ID, hostile link scheme, local uploaded file, conflicting source and no-network cases.
- No remote favicon or model/data transmission except explicit opt-in.
- Preserved `source_id/evidence_id` through streaming, caching, exports and restarts.
- Quantitative comparison against non-donor implementation/adapter effort and ongoing patch burden.
- Link to actual local CI logs and end-to-end acceptance proof.

## Concluding recommendation

**Reuse Vane primarily for ready-made UI components and bounded search interaction ideas**, not as the whole Dotpol research runtime. **Do not copy the existing scraper, tool dispatcher, evidence management, upload index, model gateway, database or whole Docker stack.** Consider optional Vane/SearXNG interoperability if it wins an objective benchmark. This preserves the ~90% *commodity* reuse ambition through well-maintained OSS dependencies and narrowly adapted donors rather than duplicated frameworks.

**Nothing in this report marks a component legally approved or functionally integrated.**
