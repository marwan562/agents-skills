---
name: multi-agents
description: Use this skill to orchestrate complex tasks through parallel sub-agent collaboration — delegating research, implementation, and devil's-advocate review to specialized roles. Triggers on multi-agent, orchestration, delegate, complex refactors, and high-risk changes.
---

# Multi-Agents

> Work like a staff team, not a single thread — parallel minds, adversarial review, one verified outcome.

Orchestrates complex tasks through parallel sub-agent collaboration: analyze, spawn, review, and integrate.

## Purpose

Decompose complex, high-risk, or multifaceted engineering tasks into focused, non-overlapping sub-agent roles. By executing research and analysis concurrently, enforcing independent adversarial review, and systematically reconciling findings, this skill eliminates blind spots, prevents regression loops, and delivers verified, maintainer-grade outcomes.

## When to Use

- Task has multiple independent workstreams (e.g., simultaneous codebase research, bug reproduction, and prior art search)
- High-risk or breaking changes where a second perspective catches subtle security, architecture, or edge-case flaws
- User explicitly requests `multi-agents`, `orchestrate`, `parallel agents`, `sub-agents`, or `devil's advocate`
- Large refactor or cross-cutting feature where a single agent pass risks missing repository conventions
- Validating reasoning, comparing architectural trade-offs, or exploring alternatives before committing
- When delegated to by `contribute` for root-cause research and diff review

Keywords: `multi-agent`, `orchestration`, `parallel`, `delegate`, `sub-agent`, `devil's advocate`

## Workflow

```
[1. Task Decomposition] ──> [2. Parallel Dispatch] ──> [3. Adversarial Critique] ──> [4. Synthesis & Dispute] ──> [5. Verification & Report]
```

### 1. Task Analysis & Role Selection

- Parse requirements, scope boundaries, and acceptance criteria.
- Classify workstreams:
  - **Independent**: Can execute concurrently in parallel (e.g., root cause investigation + codebase conventions search).
  - **Sequential**: Depends on prior stage output (e.g., implementation depends on root-cause analysis).
  - **Adversarial / High-Risk**: Demands an independent critique pass (e.g., security, edge cases, maintainer review).
- Select the minimal set of roles needed from [`references/role-catalog.md`](references/role-catalog.md). Default to the **Three-Role Brief**:
  1. **Root-Cause Analyst**: Isolates the bug mechanism and responsible code lines.
  2. **Codebase & Convention Researcher**: Maps target files, idiomatic patterns, and existing tests.
  3. **Devil's Advocate / Maintainer Critic**: Held back until diff/plan exists to conduct an adversarial review.

  **When to scale:**
  - **Trivial / single-file** — collapse Analyst + Researcher into one brief; keep a light Critic pass
  - **Cross-cutting feature** — add **Documentation Scribe (#8)** + **QA Specialist (#7)**
  - **Large refactor / migration** — add **Performance Analyst (#6)** + **Security Auditor (#5)**
  - **Continuing a PR** — swap Analyst for **PR State Analyst**: what's done, what review feedback remains

  > Three well-briefed agents beat five thin ones — only add roles the task actually needs.

### 2. Parallel Orchestration & Dispatch

- Formulate an immutable **Shared Context Block** per the canonical spec in [`references/orchestration-protocol.md#shared-context-block`](references/orchestration-protocol.md). Minimal fast-path shape:
  ```text
  TASK: <verbatim task requirements>
  SCOPE: <target directories or files>
  CONSTRAINTS: <language, conventions, performance criteria>
  ACCEPTANCE CRITERIA: <definition of done>
  ```
  Do not redefine fields here; that spec is canonical.
- Dispatch independent sub-agents concurrently in a **single turn** using your environment's sub-agent tool (`Task`, `browser_subagent`, etc.).
- Enforce strict role isolation: provide clear objectives and structured output schemas so sub-agents produce actionable outputs without overlapping. The orchestrator implements; sub-agents analyze, research, and critique unless an Implementation Specialist is explicitly dispatched.

### 3. Adversarial Collaboration & Critique

- Never let an implementation proceed without independent challenge.
- When an implementation plan or code diff is produced, dispatch the **Devil's Advocate / Maintainer Critic** against the concrete diff or artifact.
- Evaluate concrete failure modes: null/undefined states, race conditions, performance bottlenecks, and project style regressions.

### 4. Synthesis & Dispute Resolution

- Aggregate outputs using the methodology in [`references/synthesis-and-dispute.md`](references/synthesis-and-dispute.md).
- Resolve contradictions:
  - For competing root-cause hypotheses, run an empirical test or inspect the specific lines.
  - For architectural disputes, prefer simplicity and adherence to existing project precedents.
- Enforce the **Three-Cycle Hard Limit**: If the Critic still rejects changes after 3 rounds, halt iteration and present structured decision options to the user.

### 5. Verification & Structured Reporting

- Execute local build, lint, and test suites to verify the integrated outcome.
- Optional Jev gate (skipped without `JEV_API_KEY`): send task + diff +
  test results to `jev_review`, rescore after fixes with `previousEvaluation`.
  The Critic verdict and three-cycle cap still decide. Never send secrets.
  Full protocol: [`contribute Jev gates`](../contribute/references/jev-decisions.md).
- Produce a clear, concise handoff report:
  - **(a) What was accomplished**: Summary of changes and decisions.
  - **(b) Sub-agents utilized**: Role names and brief outcome from each.
  - **(c) Verified trade-offs & assumptions**: Key architectural calls made.
  - **(d) Deferred work**: Any secondary cleanups noted for future follow-up.

## How to Invoke Sub-Agents

Adapt the dispatch call to your environment's native sub-agent tool while keeping the prompt contract and shared context intact:

```text
Task(
  subagent_type="general",
  description="<Short Role Label>",
  prompt="""
  ROLE: <Role Name from references/role-catalog.md>
  GOAL: <Specific objective>
  
  SHARED CONTEXT:
  TASK: <Verbatim task requirements>
  SCOPE: <Target directories or files>
  CONSTRAINTS: <Language, conventions, performance criteria>
  ACCEPTANCE CRITERIA: <Definition of done>
  
  OUTPUT FORMAT: <Follow schema defined in references/role-catalog.md>
  """
)
```

For complete runtime envelope specifications (OpenCode, Claude Code, Antigravity/Gemini), see [`references/orchestration-protocol.md`](references/orchestration-protocol.md).

## Instructions

- **Default to rigor:** Parallelize discovery, hold back judgment until there is a diff, and never ship without a critic.
- **Provide complete context up front**: Never force sub-agents to guess repository root, conventions, or constraints. Paste the shared context block into every dispatch.
- **Maintain role separation**: If two agents produce identical work, refine their briefs to eliminate overlap.
- **Dispatch in parallel**: Independent agents must be dispatched concurrently in a single turn, not sequentially.
- **Hold back the critic**: The Critic / Reviewer must evaluate a concrete plan or real code diff, never a vague idea.
- **Budget tokens effectively**: Avoid dumping entire multi-thousand-line files into prompts; pass exact paths and line ranges.

## Constraints

- Do NOT dispatch sub-agents with vague, open-ended instructions ("go investigate this repo").
- Do NOT run independent sub-agents sequentially when parallel dispatch is supported.
- Do NOT ignore findings from specialized agents; explicitly address or document trade-offs.
- Do NOT loop past 3 review cycles. Escalate persistent architectural disagreements to the user.
- Do NOT spawn unnecessary roles for trivial single-file edits where a direct pass is faster and lower-risk.
- Do NOT lose rigor if sub-agent tools are unavailable in the host runtime; execute sequential virtual roles per [`references/failure-recovery.md`](references/failure-recovery.md).

## Examples

### Example 1 — Complex Feature with Parallel Exploration

> **User**: "Add CSV export to `src/export/` — use multi-agents."

1. **Decomposition**: Identifies independent workstreams (research existing exporters vs. risk/streaming analysis).
2. **Parallel Dispatch**:
   - *Codebase Researcher*: Identifies `src/export/json.ts` pattern, notes table-driven tests in `export.test.ts`.
   - *Performance & Risk Analyst*: Identifies memory limits with large datasets, flags delimiter escaping and UTF-8 BOM.
3. **Implementation**: Implements `csv.ts` following `json.ts` idioms, incorporating streaming and escaping guards.
4. **Adversarial Review**: Maintainer Critic reviews the diff, flags missing documentation in `docs/api.md`.
5. **Synthesis & Handoff**: Documentation updated, tests pass, delivered with structured report.

### Example 2 — Bug Fix with Devil's Advocate

> **User**: "Fix the auth bypass in `src/auth/` — run multi-agents with a devil's advocate."

1. **Parallel Dispatch**:
   - *Root-Cause Analyst*: Reproduces bypass, isolates flaw to missing role check in `auth.ts:42`.
   - *Codebase Researcher*: Locates `auth.test.ts` fixture suite and project authentication conventions.
2. **Implementation**: Implements targeted guard in `auth.ts:42`.
3. **Devil's Advocate**: Challenges the diff: "Does this invalidate active guest sessions? What about cached JWTs?"
4. **Refinement**: Implementer adds regression tests confirming guest sessions and token revocation behavior.
5. **Handoff**: Passes test suite, reports verified assumptions.

### Example 3 — Research-Only Fan-Out

> **User**: "Use multi-agents to explore `internal/billing/` before refactor."

1. Dispatches 3x `general` sub-agents in one turn, all with the Shared Context Block:
   - (A) file map and responsibilities, (B) API-to-DB data flow, (C) test coverage audit.
2. Synthesizes into a briefing doc with `CODEBASE RESEARCH` schemas; flags contradiction A vs B via an empirical re-read of the exact lines.
3. Critic verdict: `ESCALATE — billing retry path undocumented, recommend spike before refactor.`

### Example 4 — Single-Agent Virtual Role Fallback

> **User**: "Analyze `internal/billing/` before refactoring." (Environment lacks sub-agent spawning tool)

1. Follows [`references/failure-recovery.md`](references/failure-recovery.md) solo fallback protocol.
2. Wears *Analyst Hat*: Maps module dependencies and database interactions.
3. Wears *Researcher Hat*: Audits test coverage and identifies undocumented coupling.
4. Wears *Critic Hat*: Challenges refactoring assumptions and highlights high-risk migration paths.
5. Synthesizes findings into an architectural brief.

## References

- [`references/role-catalog.md`](references/role-catalog.md) — Comprehensive catalogue of agent role prompts, objectives, and output schemas.
- [`references/orchestration-protocol.md`](references/orchestration-protocol.md) — Parallel dispatch mechanics, shared context blocks, and runtime envelopes.
- [`references/synthesis-and-dispute.md`](references/synthesis-and-dispute.md) — Reconciliation methodology, conflict resolution matrix, and escalation protocol.
- [`references/failure-recovery.md`](references/failure-recovery.md) — Remediation for sub-agent timeouts, hallucinated code, and single-agent virtual role execution.
- Integrates directly with [`skills/contribute`](../contribute/SKILL.md) and [`skills/code-review`](../code-review/SKILL.md).
