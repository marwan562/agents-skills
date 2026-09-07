# Multi-Agent Orchestration Protocol

Standardized operational guidelines for dispatching, synchronizing, and managing parallel sub-agent workflows.

---

## 1. Orchestration Lifecycle

Canonical 5-phase flow (matches `SKILL.md` Workflow):

```
[1. Task Analysis & Role Selection] ──> [2. Parallel Orchestration & Dispatch] ──> [3. Adversarial Collaboration & Critique] ──> [4. Synthesis & Dispute Resolution] ──> [5. Verification & Structured Reporting]
```

```
┌────────────────────────────────────────────────────────┐
│          PHASE 1: TASK ANALYSIS & ROLE SELECTION       │
│  - Parse objectives, identify dependencies & risks     │
│  - Select minimal role set from role-catalog.md        │
└───────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────┐
│          PHASE 2: PARALLEL ORCHESTRATION & DISPATCH    │
│  - Assemble immutable Shared Context Block             │
│  - Dispatch independent agents in parallel single turn │
└───────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────┐
│          PHASE 3: ADVERSARIAL COLLABORATION & CRITIQUE │
│  - Hold back Critic/Reviewer until diff/plan exists    │
│  - Challenge with concrete failure modes               │
└───────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────┐
│          PHASE 4: SYNTHESIS & DISPUTE RESOLUTION       │
│  - Collect outputs, reconcile conflicting findings     │
│    per synthesis-and-dispute.md                        │
│  - Iterate (max 3 cycles) or escalate to user          │
└───────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────┐
│          PHASE 5: VERIFICATION & STRUCTURED REPORTING  │
│  - Execute local verification test/build suites        │
│  - Produce concise structured handoff report           │
└────────────────────────────────────────────────────────┘
```

---

## 2. Dispatch Envelopes Across Runtimes

Sub-agent dispatch mechanisms vary across platforms. Adapt only the outer envelope while preserving role prompts and shared context blocks.

### Standard `Task` Tool (OpenCode, Claude Code, Generic Agent Runtimes)
```text
Task(
  subagent_type="general",
  description="Investigate auth failure in src/auth/",
  prompt="""
  ROLE: Root-Cause Analyst
  GOAL: Isolate the root cause of the auth bypass reported in issue #42.
  
  SHARED CONTEXT:
  TASK: Fix session invalidation bypass on password change
  SCOPE: src/auth/**, tests/auth/**
  CONSTRAINTS: TypeScript strict, no new dependencies
  ACCEPTANCE CRITERIA: Session tokens invalidated immediately upon password change
  
  OUTPUT FORMAT: Follow Root-Cause Analyst schema in role-catalog.md
  """
)
```

### Antigravity / Gemini Sub-Agent Runtime
```text
browser_subagent(
  TaskName="Root-Cause Analysis",
  TaskSummary="Isolate the mechanism of session bypass in auth.ts",
  RecordingName="root_cause_analysis",
  Task="""
  ROLE: Root-Cause Analyst
  GOAL: Isolate the root cause of the auth bypass reported in issue #42.

  SHARED CONTEXT:
  TASK: Fix session invalidation bypass on password change
  SCOPE: src/auth/**, tests/auth/**
  CONSTRAINTS: TypeScript strict, no new dependencies
  ACCEPTANCE CRITERIA: Session tokens invalidated immediately upon password change

  OUTPUT FORMAT: Follow Root-Cause Analyst schema in role-catalog.md
  """
)
```

---

## 3. Shared Context Block Specification {#shared-context-block}

Every sub-agent brief MUST include the shared context block verbatim. Never require a sub-agent to guess project roots, constraints, or user intent. This spec is canonical; `SKILL.md` shows only the fast-path shape.

```text
================ SHARED CONTEXT BLOCK ================
TASK: <Verbatim user prompt or issue specification>
SCOPE: <Explicit file paths, directories, or modules in play>
CONSTRAINTS: <Branch rules, lint/format commands, language standards, performance criteria>
GROUNDED EVIDENCE: <Rendered intake findings, stack traces, reproduction inputs>
ACCEPTANCE CRITERIA:
1. <Criterion 1>
2. <Criterion 2>
======================================================
```

Field notes: `SCOPE` and `TARGET SCOPE` are the same slot; `CONSTRAINTS` includes `PROJECT CONVENTIONS` plus runtime limits. Always include `GROUNDED EVIDENCE` when prior intake, repro, or trace output exists.

---

## 4. Parallel Dispatch Mechanics

1. **Single-Turn Parallel Execution**: When dispatching independent sub-agents (e.g. Researcher + Root-Cause Analyst), emit all tool calls in a **single turn** so the runtime executes them concurrently.
2. **Sequential Dependencies**: When Agent B requires the output of Agent A (e.g. Implementer requires Root-Cause Analyst's findings), do NOT dispatch Agent B prematurely.
3. **Holding Back the Critic**: The Devil's Advocate / Maintainer Reviewer must NEVER run on the prompt or idea alone. It must evaluate a concrete artifact: either the formal implementation plan or the actual code diff.

---

## 5. Context Budgeting & Token Management

To avoid context window exhaustion and degraded reasoning across multiple agents:

1. **No Monolithic File Dumps**: Do not paste 1,000-line source files into the sub-agent prompt. Provide exact file paths, line ranges, and concise snippets. Instruct sub-agents to read the necessary files directly using workspace tools.
2. **Structured Compact Outputs**: Require sub-agents to adhere to schemas from `role-catalog.md`. Refuse freeform conversational filler.
3. **Diff-Only Review Passes**: When sending work to the Critic / Reviewer, pass only `git diff` and affected test outputs, not the entire codebase history.
4. **Pruning Between Cycles**: When iterating through review rounds, summarize past review feedback in 2-3 lines rather than appending redundant conversation trees.
