# Dotpol Local Security and AI Assurance Plan

**Status:** Proposed cross-phase security/evaluation controls for Phase 0 review.  
**Owners to designate:** application security, AI evaluations, privacy and release reviewers.  
**Baseline references:** `docs/ARCHITECTURE.md`, `docs/AI_ARCHITECTURE.md`, `docs/DATA_ARCHITECTURE.md`.

## Protected assets, entry points, attackers

Protected assets: local projects/datasets, source/evidence records, model credentials, cached text, exported reports, plugin permissions, software supply chain and any future team-access control.

Potential entry points: public PDFs/HTML/CSV, imported project archives, local API, optional remote search/model providers, file paths, agent tool results, plugins/connectors, GIS assets and external pull requests.

Threat actors include malicious websites/documents embedded as untrusted evidence, prompt-injection authors, compromised packages, unsafe plugins, opportunistic network users, and misconfigured CI. Local operation reduces dependencies, **not** all threats.

## Phase 1 local gateway baseline

- Bind to loopback by default; do not expose the API on the LAN or internet without an explicit independently reviewed deployment mode.
- Restrict CORS/origin/host and protect mutating localhost APIs against cross-site request forgery or cross-origin drive-by requests. Define local session/token strategy before exposing write routes.
- Apply strict paths/workspace sandboxing; reject traversal, symlinks escaping workspace, unsafe archive entries, oversized inputs and malicious filenames.
- Keep keys outside version control; choose OS-appropriate secure storage and explicit retention/redaction behavior. No auth provider or paid service mandatory.
- Avoid shell execution and filesystem/network powers in AI tools by default; disallow arbitrary command execution in v1 research agent.
- Define size, request rate, model token/time and computation limits so local mode cannot accidentally exhaust storage/CPU/GPU.
- Errors/logs must not include credentials, imported private data or entire prompts by default.
- Configured external models/web search are opt-in; fail clearly without keys and label transmission destinations and inputs.
- Persistent state survives restart; migrations, backup/restore and safe delete are tested; absence of an AI model does not block non-AI project tasks.

## AI tool permission contract

Every tool declaration must specify: `tool_id`, capability owner, typed inputs/outputs, data classifications accessed, required file/network permissions, side effects, approval mode, logging/provenance, time/resource budget and test fixtures.

| Class | Examples | Planned policy |
|---|---|---|
| R0 local read | list project sources, query imported dataset | scoped to active workspace; trace results |
| R1 external read | web retrieval, public connector | explicit enabled provider and source terms; validate outbound URLs/SSRF |
| W1 local mutation | import/transform/create note | require user-initiated context and validated path/scope; auditable |
| W2 external/write/destructive | publish, post, message, sync, delete data | explicit per-action human approval, reversible where possible; cannot be silently triggered by documents |

Agents **never** promote instructions found in PDFs, websites, repository files or search snippets to trusted system/operator instructions. A valid model response does not override application authorization. Domain engines, not AI text, perform deterministic calculations.

## AI reliability & adversarial evaluations

Maintain versioned test cases under future `evaluations/` linked to a capability and model/tool version. Test:

1. citation/evidence ID validation, span fidelity and unknown-source abstention;
2. prompt injection embedded in documents/web results asking to ignore instructions, reveal secrets or invoke tools;
3. privileged-tool escalation and destructive network/file operations without approval;
4. private-data leakage into remote providers, logs or generated reports;
5. malicious and contradictory datasets, missing columns, unstable entity matches and outdated sources;
6. model/provider unavailable, timeout, rate limit, and low-resource offline behavior;
7. numeric claims vs deterministic reference calculation and evaluation of forecast intervals;
8. multilingual/translation and date/jurisdiction ambiguity;
9. provenance after transformation, deletion/withdrawal and version changes.

Each AI-facing PR must state measured pass/fail criteria, benchmark dataset provenance and known limitations. Target thresholds are proposed by responsible owners and approved before release; unknown results are marked *not tested*. AI evaluation complements deterministic tests, it cannot replace them.

## CI and OSS supply-chain baseline

- Public fork PR CI runs with least privilege and no production secrets; avoid running untrusted PR code in a privileged `pull_request_target` context.
- Pin major actions and, for sensitive workflows, immutable commits; create dependency lockfiles when tools are introduced.
- Identify third-party licence obligations before assimilation and maintain `THIRD_PARTY_NOTICES.md` once donor code is added.
- Plan vulnerability checks, SBOM generation and signed/verifiable release artifacts in Phase 12; critical dependency alerts should be handled earlier when code appears.
- Require reviewer approval for changes to workflow permissions, deployment, provider credential handling, plugin execution, or sensitive data paths.
- Verify test assertions and artifacts, not just that CI job reported green.

Security engineering references:
- NIST SSDF: https://csrc.nist.gov/projects/ssdf
- OWASP LLM application risks: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- NIST Generative AI Profile: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
- GitHub Actions privileged PR warning: https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target

## Progressive security gates

**Phase 0:** owner, threat model, permission classes, planned test catalog and privacy policy approved.  
**Phase 1:** localhost security, path containment, no-secrets CI, provider opt-in, tested missing-model behavior.  
**Phase 2–3:** untrusted file/parser/source threats, retrieval prompt injection, provenance integrity, SSRF controls.  
**Phase 4–9:** source-dependent analytical privacy, uncertainty, explainability and trusted output labels.  
**Phase 10–11:** actor permissions, remote delivery, data sync, integrations, audit, plugin isolation/approval.  
**Phase 12:** coordinated disclosure/security policy, SBOM/versions, threat-model re-review, accessibility, release and recovery testing.

Do not defer core security until Phase 12 merely because that phase contains overall hardening.
