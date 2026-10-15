# Vane fork — verified source and selective-integration evaluation

**Date:** 2026-10-15  
**Status:** **FORKED / VERIFIED GITHUB PARENT, NOT INTEGRATED, NOT COMPONENT-LICENCE APPROVED**  
**Dotpol capability:** generative-search / research experience under `platform/search`, with `platform/ai` gateway and `platform/provenance` evidence contracts as upstream dependencies.

## GitHub source and fork facts

- Upstream: https://github.com/ItzCrazyKns/Vane
- Actual fork: https://github.com/kiranvbiim-coder/Vane — **not** `limuria08-hub/Vane`; GitHub shows connected collaborator/admin access to the fork.
- GitHub API returned `fork: true`, `parent.full_name: ItzCrazyKns/Vane`, `source.full_name: ItzCrazyKns/Vane`.
- Default branch: `master`. Fork created `2026-10-15T04:46:08Z`.
- **Observed fork HEAD:** `348feca3e378fb4157b217724ed508dc707f853f`.
- **Observed upstream master HEAD:** `348feca3e378fb4157b217724ed508dc707f853f` (equal at time of review; upstream may move).
- Root `LICENSE` reports MIT, copyright 2026 ItzCrazyKns; `package.json` reports version `1.12.2`. **No transitive, bundled-service or per-component licence review has passed yet.**
- No Dotpol application code imported; no dependency added; no tests run or fork customizations made by this evaluation.

**Account boundary:** The fork belongs to `kiranvbiim-coder`, while Dotpol belongs to `limuria08-hub`. Both are connected in the current collaborator context. Keep links and maintenance ownership explicit, rather than assuming a fork already exists in the Dotpol owner's namespace. Do not create a duplicate fork just for naming without an ownership decision.

## What I inspected

- `README.md`: local/cited answering engine, file upload, local Ollama and optional hosted models, speed/balanced/quality search modes; default Docker distribution bundles SearXNG, while slim distribution expects external SearXNG.
- `docs/architecture/WORKING.md`: query classification -> parallel research/widgets -> generated answer; Vane documents model-prompted citation behaviour and POST `/api/search` output with `message` and `sources`.
- `package.json`: Next.js/React frontend, Drizzle + `better-sqlite3`, multiple remote AI SDKs and local Ollama; incompatible with using Vane as Dotpol's single Python FastAPI/provider/data backend without duplicating owners.
- `src/lib/searxng.ts`: direct HTTP adapter to SearXNG JSON API. **The adapter and AGPL SearXNG backend are separate artefacts; don't assume bundling/modification or redistribution is cleared.**
- `src/lib/scraper.ts`: Playwright-based browser ingestion + Mozilla Readability; currently launches Chromium with `--no-sandbox`/`--disable-setuid-sandbox`, follows input URL, and uses web page content. **Do not transplant it without an SSRF/private-network blocklist, sandbox redesign, resource limits and tool-level URL permissions**.
- `src/components/MessageSources.tsx`, `src/components/MessageRenderer/Citation.tsx`, `src/components/AssistantSteps.tsx`: candidate UX locations for citations and multi-step feedback. Paths observed, not code accepted.
- `src/lib/agents/search/` (classifier, researcher, search orchestration, widgets), `src/app/api/search/route.ts`, `src/lib/uploads/`: candidate directories to inspect next; module existence is not evidence of correct results or licensing suitability.

## Recommended selective adoption map

| Vane capability | Candidate path / seam | Dotpol owner | Decision | Reason / gate |
|---|---|---|---|---|
| Search session/steps UX | `src/components/AssistantSteps.tsx` and search-related components | `apps/web` | **Study/adapt** | Preserve typed Dotpol event schema and accessible streaming |
| Citation/source rendering | `src/components/MessageSources.tsx`, `src/components/MessageRenderer/Citation.tsx` | `apps/web` using `platform/provenance` | **Study/adapt selectively** | Validate evidence IDs/spans; do not trust LLM-generated reference tokens |
| Query classification & intent decomposition | `src/lib/agents/search/classifier.ts` and researcher | `platform/search` | **Benchmark/select parts** | Python tools and PydanticAI own orchestration; no duplicate agent framework |
| Web retrieval interface | `src/lib/searxng.ts` | `platform/search` | **Adapter pattern only until approved** | External/user-run SearXNG optional; local search must function without it |
| Page text extraction | `src/lib/scraper.ts` | `platform/search` / `platform/documents` | **Do not copy as-is** | Headless-browser sandbox and SSRF concerns; Docling existing parser owner |
| Provider/model routing | `src/lib/models/` | `platform/ai` | **Do not assimilate** | Would bypass one Dotpol model gateway |
| SQL/chat history | `src/lib/db/` | `platform/data` | **Do not assimilate** | Would create competing canonical/project storage |
| Image/video discovery and generic widgets | `src/app/api/images`, `videos`, `widgets` | shared search/UI | **Defer** | Outside first research MVP; respect provider costs/data licences |
| Complete Vane Docker application | root Dockerfile / bundled SearXNG | n/a | **Do not embed wholesale** | Extra app/API stack and AGPL/bundled component/licence boundary |

## Phase 0/3 acceptance gates

- [x] Verify true GitHub fork and exact origin.
- [x] Record current fork/upstream `master` SHA (observation only; not acceptance pin).
- [x] Identify component directories and initial one-owner integration seams.
- [ ] Maintainer decides fork maintenance owner and whether `kiranvbiim-coder` is permanent fork home.
- [ ] Review exact root and subcomponent licences, dependency SBOM, embedded SearXNG runtime, component notices, model/data licences.
- [ ] Review search agent and citation rendering implementations line by line, benchmark accuracy, avoid duplicating `platform/search` or `platform/ai`.
- [ ] Approve typed `SearchProvider`, `ResearchRun`, `EvidenceRef`, `Citation` contracts with local/offline and no-evidence semantics.
- [ ] Run security evaluation for poisoned search results/HTML prompt injection, unknown citation references, SSRF, provider key leakage and no-network mode.
- [ ] Scope **individual reusable modules**, preserve MIT notices, pin exact assimilation SHA, review upstream changes, and open a separate code PR only after review.
- [ ] Mark `integrated` only when Dotpol code actually consumes the approved donor output; mark `verified` only with passing end-to-end tests/provenance.

## Integration architecture rule

```text
Dotpol Web research UI (may adapt Vane UI patterns)
    -> Dotpol FastAPI local gateway
      -> platform/search SearchProvider + ResearchRun contracts
      -> platform/ai single provider-neutral model gateway
      -> platform/documents parsing/retrieval
      -> platform/provenance verified source/evidence references
    -> typed result and deterministic provenance -> UI citation rendering
```

Vane's own Next.js server, model provider SDKs, Drizzle database and Docker image do **not** become Dotpol's second backend, second canonical database, required metasearch service or source of evidence truth.

## Next action

Keep this as an evaluation document on the donor planning PR. Decide intended fork home and component scope. Then inspect search/research modules and citation rendering and record a component-level import-versus-rewrite (minimal adapter glue) decision. **No implementation authorized by this verification.**
