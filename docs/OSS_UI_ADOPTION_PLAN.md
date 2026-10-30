# LiOS.Pol — Open-source UI assimilation plan

**Status:** Canonical adoption guidance. PR #11 now contains an initial pinned Radix/Tailwind UI-02 subset, Lucide and resizable panels; remaining components are not implied installed.  
**Date:** 2026-10-30  
**Owner:** `apps/web` + `packages/ui`; API/AI remain owned by `services/api` and `platform/ai`.  
**Related:** [Five-phase plan](ROADMAP.md), [AI-native contract](AI_NATIVE_CAPABILITY_CONTRACT.md), [donor matrix](DONOR_MATRIX.md), [P1 foundation PR #11](https://github.com/limuria08-hub/Dotpol/pull/11).

## Decision and measurable goal

**Reuse existing, permissively licensed UI components rather than hand-coding navigation, dialogs, AI threads, split panes, charts and editing.** Maintain **one LiOS.Pol frontend**: Next.js + React. All research, GIS, statistics, policy and field team screens share the same shell, token scheme, command model and project/artifact state. Components never become a second backend, auth store, political ontology or AI provider gateway.

**One UI owner per job** (other tools remain *candidates* until installed, tested, version-pinned and licence-cleared):

| UI concern | Primary choice | Repository | Mode | Boundaries |
|---|---|---|---|---|
| Design system, menus, dialogs, input, accessible navigation | **shadcn/ui** with **Radix** primitives, Tailwind CSS | `shadcn-ui/ui`, `radix-ui/primitives` | selectively add source components | Do not create an unversioned wholesale component dump or mix Base UI and Radix flavors |
| AI chat messages, conversation tool-renderers and composer | **assistant-ui** | `assistant-ui/assistant-ui` | dependency / optional targeted components | Use **custom REST/LocalRuntime or external store adapter** to Dotpol's existing FastAPI; no Assistant Cloud, new model API, competing thread database or separate AI backend |
| Research chat ↔ workbench resizing | **react-resizable-panels** | `bvaughn/react-resizable-panels` | dependency | One split-panel system; maintain keyboard controls and persist panel preference locally |
| Icons | **Lucide** | `lucide-icons/lucide` | dependency | Consistent icon system; preserve necessary ISC/Feather notices |
| Research report editing | **Lexical** | `facebook/lexical` | candidate dependency in P1 after basic workbench works | Persist canonical versioned Dotpol Artifact state; editor internal state is NOT the canonical political document DB |
| Team hierarchy, event relationships, optional workflow graphs | **React Flow** | `xyflow/xyflow` | candidate dependency for P3/P4 | Visualize authorized records only; do not treat graph UI nodes as canonical memberships/tasks |
| Large analytical tables, pivot charts | **FINOS Perspective** | `perspective-dev/perspective` | already selected for P2 | Canonical analytical grid; don't install TanStack Table as second analyst engine unless needed for ordinary app-list UI |
| GIS/AutoMap | **Kepler.gl** | `keplergl/kepler.gl` | already selected for P2 | Only Map Lab renderer; MapLibre/deck.gl are transitive, no second map owner; offline basemap/provider rights independently checked |
| Survey forms | **SurveyJS Form Library** | `surveyjs/survey-library` | already selected for P2 | Free MIT form runtime only; commercial Survey Creator excluded |
| Citation/progress patterns | **Existing Vane fork** | `kiranvbiim-coder/Vane` | selectively adapt as already planned | Do not import Vane chat thread renderer alongside assistant-ui; no Vane backend, bundled SearXNG or duplicate data/state |

**Design continuity:** one premium restrained dark terminal visual system, accessible focus/contrast, compact layout, no gratuitous helper labels; neutral typography and restrained accent colors. Tokens rather than repeated per-page CSS. Optimize **UX, DX and AX** without breaking tested user journeys.

## Product shell

```text
LiOS.Pol [Projects / Chats / Research / Elections / Map / Surveys / Teams / Library]
├── AI conversation (assistant-ui, same research/backend tool contracts)
│   ├── source-grounded answers and previews of tool results
│   ├── citations, source state, model status, remote consent
│   └── open/save/revise artifact actions
├── Resizable workbench (react-resizable-panels)
│   ├── editable research report (Lexical, when ready)
│   ├── verified analytical table/chart (Perspective)
│   ├── verified GIS map layer (Kepler)
│   ├── surveys (SurveyJS)
│   └── scoped organizational graph (React Flow)
└── shared project/source/artifact state (FastAPI + SQLite local / PG shared)
```

### Non-negotiable interaction

- Ask in chat → tool returns **real canonical Artifact ID** → preview in conversation → **Open in Workbench** → revise/export → reopen SAME artifact in conversation or Library.
- Changing from research to elections/maps/teams must not reset the user's project, provenance or permission scope.
- AI output is grounded in source IDs and deterministic tool results. UI must explicitly distinguish model not configured, evidence-only extract, failed external service and actual generated answer.
- External BYOAI evidence transmission remains one-request consent. UI controls may not grant provider permissions beyond backend policy.
- On narrow viewports, stack panes or use sheets; no overlap, stuck horizontal overflow or inaccessible controls.

## Agent-ready UI implementation sequence

| ID | Phase | Owner | Concrete change | Acceptance |
|---|---|---|---|---|
| UI-01 | P1 | E web | Capture PR #11 baseline and add visual/accessibility regression fixture before migrating | Current create/import/ask/reopen flows intact; repeatable test |
| UI-02 | P1 | E web | Configure shadcn/ui **Radix flavor**, tokens, Tailwind, Lucide, reusable sidebar/dialog/input/button | No duplicated component styles; keyboard + screen reader labels |
| UI-03 | P1 | E + B | Proof-of-integration for assistant-ui custom adapter over **existing** `/api/projects/{id}/research` | No frontend direct LLM calls; citations, local/no-model/remote-consent states preserved; no extra backend |
| UI-04 | P1 | E web | Resizable chat/workbench layout, true linked artifact ID, saved panel state and responsive fallback | Click result → real saved artifact; reopen/revise without split state |
| UI-05 | P1 | E + F | Component tests, browser E2E, mobile/narrow display, accessibility checks, lockfile/security review | CI passes; no regression of P1 tests; licence notices committed |
| UI-06 | P1/P3 | E web | Lexical report editing behind Artifact storage and version contract | Reload/edit/export retains evidence, history and citations |
| UI-07 | P2 | C + E | Perspective data workspace, Kepler map, SurveyJS form rendering | Same verified dataset/query and source IDs reused across surfaces |
| UI-08 | P3/P4 | D + E | React Flow for authorized entity/team graphs | Uses canonical relationships, respects project/team scopes, read-only by default |
| UI-09 | P5 | E + F | Complete component audit, responsive UX, keyboard accessibility and high-density performance | Production acceptance and release evidence |

**Parallelism:** Only Agent E owns shell/component code. B owns AI tool contracts, C analytics/map data, D political domain data, F QA/CI. Agents may work on separate components only against a frozen shared UI/API contract.

## Adoption and fork policy

1. **Do not fork** shadcn/ui, Radix, assistant-ui, resizable panels, Lucide, Lexical, React Flow, Perspective, Kepler or SurveyJS merely to consume them. Install upstream packages or explicitly add shadcn source components.
2. Before adoption: pin package versions and lockfile, verify exact licence of used code and its bundled assets, check React 19/Next 15 compatibility, run an integration test, check local/no-network behavior.
3. **assistant-ui is a candidate UI renderer**, not an architecture replacement; validate PydanticAI/FastAPI adapter first. If this fails, retain the existing simple controlled chat UI without a second agent framework.
4. Existing Vane fork stays a candidate for source/citation/progress patterns only. Choose ONE renderer for each message/thread, table, GIS map, form and graph type.
5. No external hosted persistence, proprietary component service, commercial SurveyJS Creator, paid map tiles or mandatory SaaS.
6. Review upstream design examples for accessibility and licensing; do not copy proprietary screenshots/brand assets.

## Verification matrix

| Journey | Pass criteria |
|---|---|
| Create/open project | No lost data or broken navigation on desktop/mobile |
| Import source | Hash/source/permission labels shown correctly |
| AI answer | Actual backend model invocation or truthful no-model state; evidence links resolve |
| Remote AI | Request-specific user consent required; declined request sends no evidence |
| Chat to artifact | Same saved `artifact_id` in chat, workbench and Library |
| Report edit | Versioned content persists after restart; source references still valid |
| Specialized workspaces | No extra database/gateway or duplicate map/chart/form ownership |
| Keyboard/a11y | Focus visible, dialogs accessible, split controls operable, labels readable |
| Zero-cost local | No mandatory telemetry, external render/data fetch, paid account or CDN |

**Verified-in-code checkpoint (PR #11):** UI-01 browser fixtures, UI-04
canonical artifact split view, and a **partial UI-02** Radix/shadcn-style control
subset are implemented on the branch, alongside Lucide and a Tailwind v4
PostCSS theme. UI-05 includes a committed npm lockfile, `npm ci`, provenance
dialog focus/keyboard browser checks and a direct dependency notice ledger.
UI-03 now has a **real assistant-ui@0.15.32 ExternalStoreRuntime**
adapter backed solely by saved Dotpol Artifact IDs and the existing FastAPI
`/research` route. The reversible UI switch keeps the verified classic view
as fallback. Browser acceptance exercises sending, source-linked artifact
reopening, reload, remote-consent refusal and cross-project isolation;
no Assistant Cloud or second thread DB/LLM gateway is installed. Full
component parity, manual accessibility, transitive licence/security review
and release signoff remain outstanding. The existing FastAPI/PydanticAI data
contract and mandatory OpenClaw readiness are unaffected.

**UI-06 integration checkpoint:** PR #11 now includes pinned
`lexical@0.52.0` / `@lexical/react@0.52.0` PlainText and History
plugins within the existing workbench. The existing SQLite Artifact
answer/revision/evidence/JSON-export contract is untouched. Browser tests
verify actual edit/reopen/export and UTF-8 limits. This intentionally
**does not claim rich-text persistence or a separate Lexical document
store**. Manual accessibility and broader release checks remain open.

**Status:** This is a UI reuse blueprint. Do NOT mark these components integrated by adding them to a candidate list. Actual implementation and tests must be visible in separate PRs.
