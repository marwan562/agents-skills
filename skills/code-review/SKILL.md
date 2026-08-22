---
name: code-review
description: Use this skill when reviewing code for correctness, security, maintainability, performance, testing, and clean code. Triggers on requests to review, audit, critique, or assess code, PRs, or diffs.
---

# Code Review

Provides a systematic, repeatable code-review workflow that balances thoroughness with actionability.

## Purpose

Help an AI agent produce high-quality code reviews that catch defects, surface risks, and improve maintainability — without nitpicking or over-flagging. The output should be prioritized, justified, and easy for the author to act on.

## When to Use

- User asks to review code, a file, a directory, or a PR diff
- User requests an audit, critique, or assessment of implementation quality
- User pastes a snippet and asks "is this good?", "any issues?", "can you review?"
- CI or pre-merge checks need a checklist-based review
- Keywords: `review`, `audit`, `critique`, `assess`, `PR review`, `code quality`

## Workflow

### 1. Scope and context

- Identify what is under review: commit range, PR diff, file list, or full module
- Read surrounding context (neighboring files, tests, configs) to understand intent — do not review in isolation
- Note stated goals, linked issue/ticket, and any project conventions (`CONTRIBUTING.md`, linters, `.editorconfig`)

### 2. Correctness

Check that the code does what it claims:

- Logic errors, off-by-one, null/undefined handling, error paths, edge cases
- API contracts: request/response shapes, status codes, error codes
- Concurrency and async correctness (races, deadlocks, unawaited promises)
- Data invariants and state transitions

### 3. Security

Scan for common vulnerabilities, proportional to the code's exposure:

- Injection (SQL, XSS, command, template), auth/authz bypass, IDOR
- Secrets in code/logs, insecure randomness, weak crypto, unsafe deserialization
- Mass assignment, SSRF, path traversal, open redirects
- Dependency risks (known CVEs if a lockfile changed)
- If nothing security-relevant is in scope, explicitly say "No security-relevant changes in this scope" rather than inventing issues

### 4. Maintainability and clean code

- Naming clarity, single responsibility, function/module length, duplication
- Abstraction appropriateness (no premature abstraction, no leaky abstraction)
- Public API surface: is it minimal and hard to misuse?
- Comments: explain *why*, not *what*; remove stale or misleading comments
- Consistency with project style (naming, error handling, patterns)

### 5. Performance

- Obvious hot-path issues: N+1 queries, unbounded loops, missing pagination, large allocations
- Complexity regressions (e.g., O(n) → O(n²) on a large collection)
- I/O: redundant network calls, missing caching where appropriate, blocking I/O on event loop
- Only flag measurable concerns; avoid micro-optimizations without evidence

### 6. Testing

- Is the change covered by tests? Would you trust this without manual QA?
- Test quality: asserts behavior, not implementation; covers edge cases and failure paths
- Missing tests for bug fixes (should include a regression test)
- Over-mocked or flaky tests

### 7. Synthesize and prioritize

Produce findings grouped by severity:

- **🔴 Blocking** — must fix before merge (incorrectness, security, data loss)
- **🟡 Important** — should fix (maintainability debt, missing tests, performance risk)
- **🟢 Suggestion** — optional/nit (style, minor naming, alternative approach)

For each finding, include:

- **Location**: `file_path:line_number`
- **Issue**: one sentence
- **Why it matters**: impact if not fixed
- **Suggested fix**: concrete code or direction (diff hunk when helpful)

Close with a **verdict**: `Approve` / `Approve with comments` / `Request changes` and a 2-3 line summary.

## Instructions

- **Be specific and evidence-based.** Every finding must cite a location and explain the risk. Never emit vague "consider improving quality" without a concrete pointer.
- **Limit noise.** If there are >15 findings, show the top 10 and summarize the rest as "Additional nits: ...". Respect the author's time.
- **Acknowledge good code.** Call out one thing done well when warranted — it reinforces patterns and balances tone.
- **Follow project conventions first.** House style outranks generic preference. Cite the config or doc that supports a style comment.
- **Don't rewrite the PR.** Suggest the smallest fix that resolves the issue; offer a larger refactor only as an optional follow-up.
- **Use non-judgmental tone.** "This branch does not handle..." not "You forgot to handle..."

## Constraints

- Do NOT hallucinate files or lines — only reference artifacts you actually read
- Do NOT flag security issues without a plausible attack path in this codebase
- Do NOT demand tests for trivial config/doc-only changes unless they affect behavior
- Do NOT suggest adding dependencies without noting the trade-off
- Do NOT provide a review without an explicit verdict (Approve / Approve with comments / Request changes)

## Examples

### Example 1 — PR review

> **User**: "Review the diff in `src/auth/login.ts` from this PR."

**Agent**:

1. Reads `src/auth/login.ts:1-120`, `src/auth/login.test.ts`, and `CONTRIBUTING.md`
2. Produces:

```
Verdict: Request changes

🔴 Blocking
- src/auth/login.ts:42 — `password` logged in plaintext via `console.log`.
  Risk: credential leak in logs. Fix: remove log or log `***`.

🟡 Important
- src/auth/login.ts:78 — Missing rate-limit check before `verify()`.
  Risk: brute-force. Fix: call `rateLimiter.check(ip)` first.

🟢 Suggestion
- src/auth/login.ts:91 — Variable `tmp` is vague; rename `pendingSession`.
```

### Example 2 — Security-focused audit

> **User**: "Audit `api/search.ts` for security."

**Agent**:

1. Reads `api/search.ts:1-80`, checks for `req.query` usage
2. Flags: `api/search.ts:34 — String-interpolated SQL: \`SELECT ... WHERE q='${q}'\`. Use parameterized query \`db.query('SELECT ... WHERE q=$1', [q])\`` with severity 🔴 Blocking
3. Notes "No authz check needed here — endpoint is public by design" to show reasoning

### Example 3 — Whole-module review

> **User**: "Can you review `internal/billing/` for maintainability?"

**Agent**:

1. Lists files, measures per-file length, spots duplication between `invoice.ts` and `receipt.ts`
2. Recommends extracting shared `Money` value object, notes function `calculate()` at 90 lines should be split
3. Verdict: `Approve with comments` — no blocking issues, but debt will compound if not addressed

## References

- Complements `project-architecture` (review the architecture) and `documentation` (note missing docs flagged during review)
