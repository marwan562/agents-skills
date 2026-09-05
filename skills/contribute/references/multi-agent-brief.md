# Multi-Agent Brief Template

This reference document defines the multi-agent delegation brief template and role specializations used in **Step 7** and **Step 10** of the `contribute` workflow.

---

## Delegation Overview

When delegating deep investigation to `/multi-agents`, provide a structured, high-context brief so sub-agents work in parallel without duplicating effort or hallucinating context.

```
                  ┌──────────────────────────────┐
                  │      contribute Pipeline     │
                  │   (Steps 1-5 Context Gathering)
                  └──────────────┬───────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 ▼                               ▼
       ┌───────────────────┐           ┌───────────────────┐
       │ Role 1: Analyst   │           │ Role 2: Researcher│
       │ (Root Cause/Repro)│           │ (Codebase/Convens)│
       └─────────┬─────────┘           └─────────┬─────────┘
                 │                               │
                 └───────────────┬───────────────┘
                                 ▼
                  ┌──────────────────────────────┐
                  │       Step 8: Implement      │
                  │       Step 9: Local Test     │
                  └──────────────┬───────────────┘
                                 ▼
                  ┌──────────────────────────────┐
                  │ Role 3: Senior Maintainer    │
                  │ (Step 10 Diff Review Loop)   │
                  └──────────────────────────────┘
```

---

## Standard Three-Role Template

### Shared Context Block (Provide to All Agents)
```text
ISSUE/PR URL: <URL>
ISSUE TITLE: <Title>
ISSUE DESCRIPTION & COMMENTS:
<Verbatim description and key maintainer comment quotes>

INTAKE - RENDERED EVIDENCE (From steps 3-4 via ego-browser, paste verbatim):
<VISUALS inventory: each screenshot/image/video + what it proves, key text transcribed>
<EXTERNAL LINKS inventory: each repro/demo/docs/video/sibling-ref URL + loads Y/N + one fact>
<GAPS: what is unknown, what must be reproduced vs. taken at face value>

RELATED WORK & PRIOR ART (From Step 4):
<Candidate PRs, sibling repo issues, or rejected prior attempts with reasons>

DETECTED PROJECT CONVENTIONS (From Step 5):
- Branch Convention: <e.g., fix/123-short-slug>
- Test Command: <e.g., cargo test / pytest / npm test>
- Lint Command: <e.g., cargo clippy / ruff check / eslint>
- Commit Style: <e.g., Conventional Commits (fix:, feat:)>
- Code Style Rules: <Key guidelines from CONTRIBUTING.md / style guides>
```

---

### Role 1: Root-Cause Analyst
- **Goal:** Reproduce the defect or precisely isolate the functional gap for a feature request.
- **Scope:** Trace the execution path to the exact offending lines of code.
- **Constraints:** Diagnose only; do not write the final fix yet.
- **Prompt:**
  ```text
  ROLE: Root-Cause Analyst
  GOAL: Trace the exact root cause of issue #<issue-number> down to specific files and line numbers.
  CONTEXT:
  <Shared Context Block>
  OUTPUT EXPECTED:
  1. Reproduction steps / Root-cause explanation.
  2. Offending file paths and line number ranges (file:line).
  3. Failure mechanics: why does the current code fail or behave unexpectedly?
  ```

---

### Role 2: Codebase & Convention Researcher
- **Goal:** Deep-search the target repository for related files, prior art, relevant test files, and local idioms.
- **Scope:** Identify all files that need modification and the test harness to extend.
- **Constraints:** Focus on codebase patterns, existing tests, and maintainer standards.
- **Prompt:**
  ```text
  ROLE: Codebase & Convention Researcher
  GOAL: Find all files that must be touched, identify relevant existing tests, and extract project-specific implementation idioms.
  CONTEXT:
  <Shared Context Block>
  OUTPUT EXPECTED:
  1. Files that will need modification or creation.
  2. Existing test files and patterns covering this area.
  3. Precedent / Prior Art: similar PRs or existing helper functions to reuse.
  4. Project-specific idioms or constraints to follow.
  ```

---

### Role 3: Senior Maintainer Reviewer (Held for Step 10)
- **Goal:** Review the actual proposed diff against this project's real maintainer standards and acceptance criteria.
- **Scope:** Correctness, test coverage, edge cases, regression risk, style/lint adherence, commit hygiene.
- **Constraints:** Review the concrete git diff, not the prompt or general idea.
- **Prompt:**
  ```text
  ROLE: Senior Maintainer Reviewer
  GOAL: Act as a core maintainer of this specific repository and review the proposed diff for merge readiness.
  CONTEXT:
  <Shared Context Block>
  PROPOSED DIFF:
  <git diff content>
  OUTPUT EXPECTED:
  - Verdict: [APPROVE | REQUEST_CHANGES]
  - Blocking Issues (if any) with file:line and exact fix required
  - Non-blocking suggestions / nits
  - Verification check: Does this diff completely solve issue #<issue-number> without regression?
  ```

---

## Scaling the Roles

| Scenario | Role Adjustments |
|---|---|
| **Trivial fix** (typo, 1-line logic fix) | Combine Root-Cause Analyst + Researcher into one role; perform light review pass. |
| **Cross-cutting / API feature** | Add a 4th role: **Docs/Changelog Agent** to audit documentation and API reference updates. |
| **Continuing someone else's PR** | Swap Root-Cause Analyst for **PR State Analyst** (analyze what is done vs unresolved review comments). |
| **Prior attempt was rejected** | Supply Root-Cause Analyst with the rejected approach and maintainer rejection reasons up front. |
