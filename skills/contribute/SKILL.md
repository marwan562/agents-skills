---
name: contribute
description: Use this skill when contributing to any open-source project via an issue or PR link — fixing bugs, implementing features, or continuing PRs across GitHub/GitLab/Gitea and any language, running the full pipeline from repo sync to PR.
---

# Contribute

Orchestrates an end-to-end open-source contribution: from a bare issue/PR link to a maintainer-ready PR, delegating heavy analysis and review work to parallel sub-agents. Nothing here is tied to one project, one host, or one language — the pipeline shape is fixed, everything else is detected fresh each run.

## Purpose

Provide a repeatable, low-interruption contribution workflow that turns a single issue/PR URL into a tested, reviewed, and properly formatted pull request, respecting the target project's own conventions instead of generic defaults.

## When to Use

- User provides an issue or PR URL and wants to work on it: "start this issue", "let's fix", "pick up this ticket", "here's the next one"
- User mentions a `contributions/` directory or asks to contribute to an external repo
- User asks to open a PR against any GitHub, GitLab, or Gitea project
- Keywords: `contribute`, `fix this issue`, `implement this feature`, `pick up`, `PR for`, `good first issue`

## Workflow

### 1. Parse the link

Extract host, owner/repo, and number. Everything downstream reads from what's detected here — don't hardcode to whichever project you saw last.

- GitHub: `github.com/<owner>/<repo>/issues/<n>` or `/pull/<n>`
- GitLab: `gitlab.com/<owner>/<repo>/-/merge_requests/<n>` or `/-/issues/<n>`
- Gitea/Forgejo: similar URL shape — detect via web fetch fallback
- Host determines tooling: GitHub → `gh`, GitLab → `glab`, else `web_fetch`/`web_search`

### 2. Locate and sync the local clone

- Find the repo in this order: (a) path the user just mentioned, (b) `~/contributions/<repo>`, (c) `~/code/contributions/<repo>`, (d) `./contributions/<repo>`, (e) case/dash/underscore-insensitive fuzzy match across those roots. Nothing found → ask once whether to clone into `~/contributions/<repo>` (default) or elsewhere. Don't silently clone.
- `git remote -v` to see actual remote setup (fork workflow usually has `origin` = user's fork, `upstream` = real project). Add `upstream` from parsed owner/repo if missing.
- Detect the real default branch (`main`, `master`, `develop`, ...) — don't assume `main`. `git fetch` the right remote, check out the default branch, pull.
- If there are uncommitted local changes, **stop and ask** rather than stashing.

### 3. Read the issue or PR

- `gh issue view <n> --repo owner/repo --comments` (swap for `gh pr view <n> ... --comments` plus `gh pr diff <n>` when continuing/reviewing an existing PR), or the `glab`/web equivalent.
- Pull out: problem statement, repro steps, acceptance criteria, labels (`bug`/`feature`/`good-first-issue` changes how wide the fix should be), and anything a maintainer already said in comments — a maintainer's clarifying comment outranks the original body.
- If the issue is thin, flag it; the Root-Cause Analyst will need to reproduce it rather than take the description at face value.

### 4. Learn the project's own conventions before touching code

Read whatever exists, in priority order: `CONTRIBUTING.md` / `.github/CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `.github/ISSUE_TEMPLATE/`, `docs/DEVELOPMENT.md`, dev-setup section of root `README.md`, and lint/format/commit configs (`.eslintrc*`, `.editorconfig`, `rustfmt.toml`, `.pre-commit-config.yaml`, `commitlint.config.*`).

See **Ecosystem detection** below for language → build/test/lint command lookup so you're not guessing `npm test` on a Rust repo. This step is never skippable, even for a one-line fix.

**Ecosystem detection (check universal wrappers first):**

1. `Makefile` with `test`/`lint`/`build` target → use `make test`, `make lint`, etc.
2. `justfile` → `just test`, `just lint`
3. `.github/workflows/*.yml` — ground truth for exact CI commands

Fallback per language:

| Signal | Language | Install | Test | Lint/format |
|---|---|---|---|---|
| `package.json` | Node/JS/TS | `npm ci` / `yarn` / `pnpm` (match lockfile) | `npm test` or `scripts.test` | `npm run lint` |
| `Cargo.toml` | Rust | `cargo build` | `cargo test` | `cargo clippy`, `cargo fmt --check` |
| `go.mod` | Go | `go mod download` | `go test ./...` | `go vet ./...` |
| `pyproject.toml` / `requirements.txt` | Python | `pip install -e .` / `poetry install` | `pytest` | `ruff check` |
| `Gemfile` | Ruby | `bundle install` | `bundle exec rspec` | `rubocop` |
| `pom.xml` / `build.gradle` | Java | `mvn install` / `./gradlew build` | `mvn test` / `./gradlew test` | project-specific |
| `mix.exs` | Elixir | `mix deps.get` | `mix test` | `mix format --check-formatted` |

### 5. Create a working branch

Name it per the project's own stated convention if step 4 found one; otherwise `fix/<issue-number>-<short-slug>` or `feat/<issue-number>-<short-slug>`. Branch off the freshly-synced default branch, never off a stale local branch.

### 6. Delegate deep analysis to multi-agents

Once steps 3–4 give real context (not before), run the multi-agent workflow with three roles. Use the shared context block so agents don't re-derive what's already gathered:

```
PROJECT: <owner/repo>
ISSUE/PR: <url> (#<number>)
TYPE: <bug | feature | continuing-pr>
SUMMARY: <2-4 sentence restatement from step 3>
MAINTAINER NOTES: <anything maintainer said>
CONVENTIONS: <bits from CONTRIBUTING.md/configs>
LOCAL PATH: <path to synced clone>
BRANCH: <branch from step 5>
```

**Agent A — Root-Cause Analyst**: Reproduce the bug or pin down the exact functional gap for a feature ask. Trace to specific file(s)/function(s)/line(s). Diagnoses, doesn't fix yet.

**Agent B — Codebase & Convention Researcher**: Identify files the fix will touch, find prior art (similar past PRs/commits), confirm which tests already cover this area, and surface conventions that would be easy to miss.

**Agent C — Senior Maintainer Reviewer** (held back until step 9): Reviews the real diff against this project's own standards — not generic best practice.

### 7. Implement

Using Agent A's root cause and Agent B's research as the spec, make the change. Keep the diff as small as the issue actually requires — note unrelated cleanup separately instead of folding it in.

### 8. Verify locally

Run the project's actual test/lint/build commands from step 4. Add or update a test for the change — a fix with no accompanying test is one of the most common reasons maintainers request changes. Re-run the full suite, not just the new test.

### 9. Maintainer-style review

Send the real diff (not the plan) to the Senior Maintainer Reviewer. Check: correctness, test coverage, style/lint cleanliness, commit hygiene, whether it actually closes the issue as scoped, and anything a maintainer would flag (missing docs, breaking-change risk, edge cases). Loop steps 7 → 9 until it passes or you hit three rounds; if it still isn't converging, bring the disagreement to the user.

### 10. Commit and prepare the PR

- Commit message per the project's own convention (Conventional Commits `fix:` / `feat:` by default).
- **Checkpoint — confirm before pushing.** Show the diff summary and commit message; push to the user's fork only after they say go.
- Draft the PR description filled in with what actually changed, how it was tested, and `Closes #<issue-number>`.
- **Checkpoint — confirm before opening the PR.** Run `gh pr create` only after the user reviews the description.

**PR description template:**

```markdown
## Summary
<1-3 sentences: what this PR does and why>

## Related issue
Closes #<issue-number>

## Changes
- <bullet per meaningful change>

## Testing
- <exact commands run>
- <new test(s) added>

## Checklist
- [ ] Tests added/updated
- [ ] Lint/format passes
- [ ] Docs updated (if user-facing behavior changed)
```

### 11. Hand off

One short summary: what the issue was, what changed, what was tested, and the branch/PR link. Don't re-paste the whole diff.

## Constraints

- Do NOT silently clone — always ask first where to clone
- Do NOT stash uncommitted changes without asking
- Do NOT guess the default branch — detect it
- Do NOT skip learning project conventions — even for one-line fixes
- Do NOT push or open a PR without explicit user confirmation (checkpoints)
- Do NOT assume GitHub when the URL may be GitLab/Gitea — parse the host generically

## Checkpoints (never skip)

- Uncommitted local changes found in step 2 → ask, don't stash
- No local clone found → ask before cloning, confirm the path
- Before `git push`
- Before opening the PR / marking a draft PR ready for review

Everything else — reading files, running agents, running tests, iterating on the diff — proceeds without asking.

## Scaling the agent brief

- **Trivial fix** (typo, one-line logic bug) — merge Analyst and Researcher into one role; light review
- **Cross-cutting or multi-file feature** — add fourth **Docs/Changelog Agent**
- **Continuing someone else's PR** — swap Root-Cause Analyst for **PR State Analyst**: what's already done, what review feedback is still unresolved

Three well-briefed agents beat five thin ones — only add roles the issue actually needs.

## Examples

### Example 1 — Bug fix

> **User**: "Here's the next one: https://github.com/owner/repo/issues/42 — repo's in contributions/"

**Agent**: Parses `owner/repo#42`, finds `~/contributions/repo`, syncs `main`, reads `issue #42` (missing required flag silently exits 0), learns conventions (`errs` package, table-driven tests), creates `fix/42-missing-flag-error`, delegates to three agents, implements fix, runs `go test ./...`, gets reviewer approval, commits `fix: return error when required flag missing`, asks confirmation, pushes, opens PR with `Closes #42`.

### Example 2 — Feature request

> **User**: "Pick up https://github.com/acme/web/issues/101 — feature: add CSV export"

**Agent**: Detects feature type, traces exact gap (no export path), finds prior `JSON export PR #89` as pattern, adds CSV export following same structure, adds test in `export_test.go`, review checks API docs updated, opens PR.

## References

- Ecosystem detection and PR template are inline above — no external reference files needed at publish time
- For the full multi-agent brief template, see the upstream skill source or `skills/multi-agents/SKILL.md` in this repo
