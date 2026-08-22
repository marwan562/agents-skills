---
name: multi-agents
description: Use this skill when a task benefits from parallel sub-agent collaboration — research, implementation, and review decomposed into specialized roles. Triggers on complex tasks, large refactors, or whenever the user wants multi-agent orchestration, devil's-advocate review, or fast parallel exploration.
---

# Multi-Agents

Orchestrates complex tasks through parallel sub-agent collaboration: analyze, spawn, review, and integrate.

## Purpose

Decompose a task that is too large, risky, or high-stakes for a single pass into parallel, non-overlapping sub-agent roles. Each sub-agent works with a focused brief, then results are synthesized into one coherent output with explicit review before delivery.

## When to Use

- Task has multiple independent workstreams (research, implementation, testing, docs)
- High-risk change where a second perspective catches flaws (security, architecture, data migration)
- User explicitly requests `multi-agents`, `orchestrate`, `parallel agents`, or `research + implement + review`
- Large refactor or cross-cutting feature where a single agent would miss conventions or prior art
- Need to validate reasoning, challenge assumptions, or compare trade-offs before committing
- Keywords: `multi-agent`, `orchestration`, `parallel`, `delegate`, `sub-agent`, `devil's advocate`

## Workflow

### 1. Task analysis

- Parse the task into objectives, constraints, and acceptance criteria
- Classify parts as **independent** (can run in parallel), **sequential** (depends on prior output), or **risky** (needs extra review)
- Determine the minimal set of roles needed — default to three, expand only when justified

### 2. Multi-agent orchestration (required)

Spawn parallel sub-agents with **specific, non-overlapping roles**. Provide each with: goal, context, constraints, and expected output format. Run independent agents in parallel whenever possible.

**Default three-role brief** (adapt to the task):

| Role | Focus | Output |
|---|---|---|
| **Researcher / Root-Cause Analyst** | Reproduce or ground the problem; trace to responsible code/lines; surface prior art | Short root-cause writeup with file:line pointers |
| **Implementer / Codebase Researcher** | Identify files to touch, existing tests/patterns, conventions that apply | List of relevant files/patterns/tests + hidden conventions |
| **Critic / Maintainer Reviewer** | Validate against acceptance criteria and project conventions; devil's-advocate trade-offs | Approval or actionable change list phrased as review comments |

**When to scale:**

- **Trivial task** — collapse Researcher and Implementer into one; keep a light Critic pass
- **Cross-cutting feature** — add **Docs/Changelog** agent
- **Large refactor** — add **Risk/Edge-Case** agent focused on rollback, migration, and failure modes
- **Continuing a PR** — swap Researcher for **PR State Analyst** (what's done, what review feedback remains)

Three well-briefed agents beat five thin ones — only add roles the task actually needs.

### 3. Collaboration and thinking

- Do NOT work alone — use sub-agents to validate your reasoning and propose alternatives
- When you hit a decision point, spawn a sub-agent to independently analyze options and compare trade-offs before you commit
- Use one sub-agent explicitly as **devil's advocate** to review your plan for flaws, edge cases, and missed requirements

### 4. Review and integration

- Collect results from all sub-agents and synthesize into one coherent output
- Resolve contradictions (e.g., Researcher says bug is in `auth.ts:42`, Implementer points at `auth.ts:55` — reconcile by re-reading code)
- Run a final review pass (yourself or a dedicated reviewer sub-agent) against the original acceptance criteria before delivering
- If agents disagree and you cannot reconcile in one synthesis pass, surface the disagreement to the user with options rather than silently picking

### 5. Reporting

When done, report:

- **(a) What was accomplished** — summary of changes/decisions
- **(b) Which sub-agents were used and what each produced** — one line per agent
- **(c) Assumptions made** — what you inferred vs. what was explicit
- **(d) Anything left unfinished and why** — deferred work, open questions, follow-ups

## How to invoke sub-agents

This skill assumes your environment exposes a `task` tool (or equivalent) to spawn sub-agents. Shape the call generically:

```
Task(
  subagent_type="general" | "explore",
  description="<short role label>",
  prompt="""
  ROLE: <role name>
  GOAL: <specific objective>
  CONTEXT: <shared task context, file paths, constraints>
  OUTPUT: <expected format — bullets, diff, file:line list>
  """
)
```

If your platform uses a different tool name (e.g., `spawn_agent`), keep the **role content** identical and adapt only the envelope. The three-role structure and shared context are the contract; the tool name is not.

**Shared context block** (send to every agent, once):

```
TASK: <original task verbatim>
SCOPE: <files/dirs in play>
CONSTRAINTS: <project conventions, style, deadlines>
ACCEPTANCE CRITERIA: <how to know it's done>
```

## Instructions

- **Provide full context to each agent.** Don't make them re-derive what you already know. Paste the shared context block verbatim.
- **Keep roles non-overlapping.** If two agents produce the same work, the decomposition was wrong — refine the brief.
- **Run independent agents in parallel.** Use a single turn with multiple tool calls for the parallel dispatch, then synthesize in the next turn.
- **Preserve the reviewer's independence.** The Critic/Maintainer agent should run **against the real diff or final plan**, not the issue description. Hold it back until there is something concrete to review.
- **Loop at most three rounds.** If the Critic still rejects after three implement→review cycles, escalate to the user instead of iterating indefinitely.

## Constraints

- Do NOT spawn sub-agents without a clear role and expected output — "go help with this" is not a brief
- Do NOT run sub-agents sequentially when they are independent — parallel dispatch saves time
- Do NOT ignore a sub-agent's finding — address or explicitly defer each point
- Do NOT skip the final review pass, even when sub-agents agree
- Do NOT use multi-agents for trivial one-file edits where a single pass is faster — match tooling to task complexity

## Examples

### Example 1 — Complex feature

> **User**: "Add CSV export to `src/export/` — use multi-agents."

**Agent**:
1. Analyzes: independent work — research existing export patterns, implement CSV, update docs
2. Spawns in parallel:
   - Researcher: finds `src/export/json.ts` as prior art, notes table-driven test in `export.test.ts`
   - Risk agent: flags large-file streaming, delimiter escaping, UTF-8 BOM
3. Implements `csv.ts` using Researcher's pattern, handles Risk agent's edge cases
4. Critic reviews the diff, flags missing doc update → agent adds `docs/api.md` entry
5. Reports: what changed, which agents were used, assumptions (comma delimiter default), unfinished (Excel BOM deferred as follow-up)

### Example 2 — Bug fix with devil's advocate

> **User**: "Fix the auth bypass in `src/auth/` — run multi-agents with a devil's advocate."

**Agent**:
1. Spawns Root-Cause Analyst (reproduces bypass, traces to `auth.ts:42`) and Codebase Researcher (finds `auth.test.ts`, `CONTRIBUTING.md` auth conventions) in parallel
2. Implements fix based on both outputs
3. Devil's-advocate reviewer challenges: "Does this break the `guest` role? What about cached sessions?" → agent adds regression tests for both cases
4. Reports with explicit assumption log

### Example 3 — Research-only orchestration

> **User**: "Use multi-agents to explore how `internal/billing/` works before we refactor."

**Agent**:
1. Spawns three explore sub-agents in parallel:
   - Agent A: maps `internal/billing/` files and responsibilities
   - Agent B: traces billing data flow from API → DB
   - Agent C: audits test coverage and flags gaps
2. Synthesizes into a single briefing doc, notes contradictory findings, and recommends next steps

## References

- This skill is designed to be portable across agent platforms — adapt the `Task` tool envelope to your runtime
- Pairs with `contribute` (contribute workflow delegates to this skill in steps 6 and 9) and `code-review` (reviewer role can use that checklist)
