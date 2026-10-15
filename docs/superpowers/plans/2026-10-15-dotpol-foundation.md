# Dotpol Phase 1 Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the smallest runnable local-first Dotpol spine: web shell, local FastAPI gateway, embedded project storage, provenance/source registries, one AI provider interface, tool registry, and a minimal evidence-aware agent path.

**Architecture:** The web application talks only to the local FastAPI gateway. The gateway owns provider/tool orchestration and exposes platform contracts; SQLite/filesystem provide local state. Domain-specific election/GIS/policy features are intentionally excluded from Phase 1 so later modules build on stable shared interfaces rather than duplicating infrastructure.

**Tech Stack:** React/Next.js, Python/FastAPI, SQLite, Pydantic/PydanticAI, local filesystem, pytest, frontend test tooling selected by the web scaffold, GitHub Actions for public-repo CI.

**Spec:** `docs/BLUEPRINT.md`

## Global Constraints

- Core Dotpol must run locally without mandatory cloud services.
- A ₹0 core operating configuration must remain valid.
- Domains/agents must not call model providers directly; one Dotpol model interface owns provider access.
- Do not add election, GIS, forecasting, policy, survey or war-room implementations in Phase 1.
- Do not add a second agent framework or RAG framework.
- All important tool results must be capable of carrying provenance/source references.
- Secrets/API keys must stay outside committed files.
- New architectural dependencies require donor/licence review and, when project-wide, an ADR.

## Review Focus

- Starting Dotpol with no internet/API key should still launch and expose local health/project operations.
- Missing or invalid optional provider configuration should fail clearly without corrupting local project state.
- Reopening a local project after process restart should preserve its metadata/source records.
- Tool/agent outputs must distinguish missing evidence from generated text and never invent source IDs.
- Paths/project names/user-provided metadata must be validated so local workspace operations cannot escape the configured Dotpol data directory.

---

## Planned file structure

```text
apps/
└── web/
    ├── app/
    ├── components/
    ├── lib/api/
    └── tests/

services/
└── api/
    ├── dotpol_api/
    │   ├── main.py
    │   ├── config.py
    │   ├── projects/
    │   ├── sources/
    │   ├── provenance/
    │   ├── ai/
    │   └── tools/
    └── tests/

packages/
└── contracts/
    └── README.md

infra/
└── dev/

.github/
└── workflows/
    └── ci.yml
```

Exact generated framework files may differ, but the ownership boundaries above must remain.

### Task 1: Create the local API skeleton and configuration contract

**Files:**
- Create: `services/api/dotpol_api/main.py`
- Create: `services/api/dotpol_api/config.py`
- Create: `services/api/tests/test_health.py`
- Create: `services/api/pyproject.toml`

**Interfaces:**
- Produces: `create_app() -> FastAPI`
- Produces: `DotpolSettings` with local data directory and optional provider configuration.
- Produces: `GET /health` returning stable service/version/local-mode status.

- [ ] **Step 1: Write failing health/config tests**

Test that `create_app()` exposes `/health`, that no API key is required to start, and that the default runtime reports local mode.

- [ ] **Step 2: Run the focused tests and confirm failure**

Run: `pytest services/api/tests/test_health.py -v`

Expected: FAIL because API/settings are not implemented.

- [ ] **Step 3: Implement minimal FastAPI app and typed settings**

Keep configuration environment/file driven; do not introduce hosted config/auth services.

- [ ] **Step 4: Run tests**

Run: `pytest services/api/tests/test_health.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add services/api
git commit -m "feat: add local Dotpol API foundation"
```

### Task 2: Implement safe local project/workspace persistence

**Files:**
- Create: `services/api/dotpol_api/projects/models.py`
- Create: `services/api/dotpol_api/projects/repository.py`
- Create: `services/api/dotpol_api/projects/routes.py`
- Create: `services/api/dotpol_api/storage/sqlite.py`
- Create: `services/api/tests/test_projects.py`

**Interfaces:**
- Produces: `Project` typed model with ID, name, created/updated timestamps and local workspace path reference.
- Produces: `ProjectRepository.create/list/get` methods.
- Produces: project CRUD API sufficient for create/list/get in Phase 1.

- [ ] **Step 1: Write tests for create/list/reopen/path validation**

Assertions must include persistence across a newly constructed repository instance and rejection of project names/paths that could escape the configured Dotpol data directory.

- [ ] **Step 2: Verify tests fail**

Run: `pytest services/api/tests/test_projects.py -v`

- [ ] **Step 3: Implement SQLite-backed local repository and workspace creation**

Use one local SQLite operational store; do not add PostgreSQL/Supabase.

- [ ] **Step 4: Run project tests and whole API suite**

Run: `pytest services/api/tests -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add services/api/dotpol_api/projects services/api/dotpol_api/storage services/api/tests/test_projects.py
git commit -m "feat: add local project persistence"
```

### Task 3: Add source registry and provenance primitives

**Files:**
- Create: `services/api/dotpol_api/sources/models.py`
- Create: `services/api/dotpol_api/sources/repository.py`
- Create: `services/api/dotpol_api/provenance/models.py`
- Create: `services/api/dotpol_api/provenance/repository.py`
- Create: `services/api/tests/test_sources_provenance.py`

**Interfaces:**
- Produces: `SourceRecord` with stable ID, source type, title/location, optional licence metadata, imported/retrieved timestamp and checksum/version fields where present.
- Produces: `EvidenceRef` and `ToolRunRecord` primitives that later results can reference.
- Consumes: Task 2 SQLite storage utilities.

- [ ] **Step 1: Write tests for source persistence and valid evidence references**

Include a test that fabricated/unknown source IDs cannot be silently attached as valid evidence.

- [ ] **Step 2: Run and confirm failure**

Run: `pytest services/api/tests/test_sources_provenance.py -v`

- [ ] **Step 3: Implement minimal source/provenance repositories**

Keep contracts intentionally small but extensible toward `docs/DATA_ARCHITECTURE.md`.

- [ ] **Step 4: Run API tests**

Run: `pytest services/api/tests -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add services/api/dotpol_api/sources services/api/dotpol_api/provenance services/api/tests/test_sources_provenance.py
git commit -m "feat: add source and provenance registries"
```

### Task 4: Implement one Dotpol AI model interface with local-first behavior

**Files:**
- Create: `services/api/dotpol_api/ai/models.py`
- Create: `services/api/dotpol_api/ai/provider.py`
- Create: `services/api/dotpol_api/ai/providers/local.py`
- Create: `services/api/dotpol_api/ai/providers/optional_remote.py`
- Create: `services/api/tests/test_ai_gateway.py`

**Interfaces:**
- Produces: provider-neutral request/response contracts.
- Produces: `ModelProvider` protocol/interface.
- Produces: local provider adapter contract that can be configured without remote credentials.
- Optional remote adapter must fail with a clear configuration error when no key/config exists.

- [ ] **Step 1: Write provider portability/config tests**

Test startup without remote credentials, local-provider selection and explicit remote-provider configuration failure.

- [ ] **Step 2: Verify failure**

Run: `pytest services/api/tests/test_ai_gateway.py -v`

- [ ] **Step 3: Implement provider-neutral gateway**

Do not expose provider SDK types outside the adapter package.

- [ ] **Step 4: Run tests**

Run: `pytest services/api/tests -v`

- [ ] **Step 5: Commit**

```bash
git add services/api/dotpol_api/ai services/api/tests/test_ai_gateway.py
git commit -m "feat: add provider-neutral AI gateway"
```

### Task 5: Add typed tool registry and minimal evidence-aware agent path

**Files:**
- Create: `services/api/dotpol_api/tools/models.py`
- Create: `services/api/dotpol_api/tools/registry.py`
- Create: `services/api/dotpol_api/ai/agent.py`
- Create: `services/api/dotpol_api/tools/source_lookup.py`
- Create: `services/api/tests/test_tools_agent.py`

**Interfaces:**
- Consumes: Tasks 3 and 4 source/provenance/model contracts.
- Produces: typed tool registration/invocation contract.
- Produces: one minimal agent that can invoke a deterministic source lookup tool and return an answer/result with evidence references.

- [ ] **Step 1: Write tests proving tools—not prompts—produce source-backed data**

Include a no-evidence case that returns an explicit missing-evidence state rather than an invented citation.

- [ ] **Step 2: Verify tests fail**

Run: `pytest services/api/tests/test_tools_agent.py -v`

- [ ] **Step 3: Implement tool registry and PydanticAI-based minimal agent orchestration**

Do not add additional agent frameworks.

- [ ] **Step 4: Run tests**

Run: `pytest services/api/tests -v`

- [ ] **Step 5: Commit**

```bash
git add services/api/dotpol_api/tools services/api/dotpol_api/ai/agent.py services/api/tests/test_tools_agent.py
git commit -m "feat: add evidence-aware tool and agent runtime"
```

### Task 6: Create the Dotpol web shell against gateway contracts

**Files:**
- Create: `apps/web/` using the selected Next.js scaffold.
- Create: `apps/web/lib/api/client.ts`
- Create: `apps/web/app/page.tsx`
- Create: `apps/web/app/projects/` minimal project experience.
- Create: frontend tests appropriate to the scaffold.

**Interfaces:**
- Consumes: `GET /health` and project API from Tasks 1–2.
- Produces: local-first app shell showing service health and create/list/open project flow.

- [ ] **Step 1: Add failing frontend tests for local gateway/project flow**

Do not hard-code a Vercel/Supabase/backend service.

- [ ] **Step 2: Run frontend tests and confirm failure**

Use the package-manager/test command chosen by the scaffold and record it in `apps/web/README.md`.

- [ ] **Step 3: Implement minimal UI shell and typed API client**

Navigation may expose future sections as disabled/planned labels, but do not create fake feature implementations.

- [ ] **Step 4: Run frontend tests/build**

Expected: PASS/build succeeds without commercial-service credentials.

- [ ] **Step 5: Commit**

```bash
git add apps/web
git commit -m "feat: add local Dotpol web shell"
```

### Task 7: Add public-repository CI and local developer verification

**Files:**
- Create: `.github/workflows/ci.yml`
- Create: `infra/dev/README.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: backend/frontend test/build commands from Tasks 1–6.
- Produces: reproducible CI for standard public GitHub runners and documented local commands.

- [ ] **Step 1: Define CI checks for backend and frontend**

Start with Linux for fast validation; add Windows/macOS matrix jobs only when platform-specific runtime/packaging paths exist so CI is useful rather than decorative.

- [ ] **Step 2: Run all commands locally**

Backend expected: `pytest services/api/tests -v` PASS.  
Frontend expected: test/build commands documented by scaffold PASS.

- [ ] **Step 3: Add CI workflow and developer instructions**

No paid external services or secrets should be necessary for the baseline CI path.

- [ ] **Step 4: Verify the workflow syntax and push branch/PR**

The first successful Actions run becomes Phase 1 baseline evidence.

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/ci.yml infra/dev/README.md README.md
git commit -m "ci: add free public-repo validation"
```

## Phase 1 completion gate

Phase 1 is complete only when all are true:

- Dotpol launches locally without paid-service credentials.
- Local project state survives restart.
- Source/provenance primitives exist.
- AI provider access is behind one Dotpol interface.
- At least one local-model-compatible path exists or is cleanly adapter-ready without forcing a remote provider.
- One evidence-aware tool/agent path works without fabricating citations.
- Web shell uses the local gateway.
- Baseline tests pass.
- Public-repo CI passes.
- No Phase 2+ domain capability has been prematurely duplicated into the foundation.

## Execution note

Implement Phase 1 only after maintainers review Blueprint v1.0. Prefer subagent-driven implementation with review gates because storage, AI, provenance and frontend contracts become dependencies for nearly every later phase.

## Planning review overlay — 2026-10-15 (proposed; not implementation)

**Stop before Task 1 until Phase 0 review is accepted.** The task checkboxes above remain authoritative and unchecked. The proposed [ADR-0001](../../DECISIONS/0001-foundation-module-ownership.md) is intentionally not accepted; it may change the *file placement* of sources, provenance, AI and tools from `services/api` to registered `platform/` owners. Do not create both implementations. (The relative ADR link should resolve from this plan's directory as `../../DECISIONS/0001-foundation-module-ownership.md`.)

### Preconditions

- [ ] Maintainers accept/revise the [plan audit](../../PLAN_AUDIT_2026-10-15.md) and select initial [MVP journey](../../PRODUCT_MVP_AND_ACCEPTANCE.md).
- [ ] Resolve [ADR-0001](../../DECISIONS/0001-foundation-module-ownership.md) and adjust path examples/tests before assigning parallel agents; designate single canonical implementation owner for local persistence/source/provenance/model/tool contracts.
- [ ] Approve root project licence decision and establish legal/OSS review process.
- [ ] Review [data governance](../../DATA_GOVERNANCE.md), [security/AI assurance](../../SECURITY_AND_AI_ASSURANCE.md) and local-model/no-provider fallback behavior.
- [ ] Record API contract cards for health, projects, sources, evidence, provider and tool invocation; designate cross-language schema/semver policy as needed.

### Extra failure tests required in implementation, by task

- **Task 1:** loopback binding by default, disallowed CORS/origins/host headers, no-key boot, sensible resource limits and non-leaky errors; localhost write routes require an approved anti-CSRF/local-auth strategy.
- **Task 2:** path traversal/symlink escape, malformed names, reopening/migrations, backup/restore plan and forbidden destructive path operations.
- **Task 3:** unknown/withdrawn source and evidence IDs rejected; source classification and version/attribution metadata preserved.
- **Task 4:** credentials never required or logged for local startup; remote provider disabled unless configured by user; clear offline/unavailable errors; no private data silently sent remotely.
- **Task 5:** untrusted source prompt injection, no-evidence abstention, typed tool allowlists, no unsolicited network/write/destructive effect and bounded execution.
- **Task 6:** no mock production data presented as genuine; error/loading/absence states; keyboard accessibility, local gateway safety and clear model offline status.
- **Task 7:** fork PRs have restricted tokens and no privileged execution of untrusted code; CI reports backend/frontend tests and no-secret/no-key path; dependency licences reviewed before adoption.

### Completion evidence record

For each task link: PR; capability ID/owner; typed contract; donor/legal review if applicable; command and actual test result; negative security test; offline/local result; relevant provenance/evaluation; acceptance demo. A merged PR without verification is **implemented**, not **verified**. No future domain phase should start merely to make the UI appear complete.
