---
description: Unified contribution workflow — orchestrates all 6 agents-skills (contribution, contribute, code-review, documentation, multi-agents, project-architecture) for end-to-end contributions
---

You are executing the **unified /contribute workflow** for the `agents-skills` repository. This single command orchestrates **all 6 skills** in `skills/` to take any contribution from idea to merged PR without manual skill switching.

**Skills to orchestrate (all local in `skills/` and globally in `~/.agents/skills/`):**
- `contribution` — repo-specific workflow for THIS repo (CONTRIBUTING.md, skill spec, validation)
- `contribute` — universal 12-step pipeline for ANY repo (issue/PR URL → branch → PR)
- `multi-agents` — parallel decomposition (Root-Cause, Codebase Researcher, Maintainer Reviewer)
- `code-review` — 6-dimension review gate (correctness, security, maintainability, performance, testing)
- `documentation` — accurate README/docs/changelog sync
- `project-architecture` — module boundaries and ADRs for new skills or large refactors

**ARGUMENTS:** `$ARGUMENTS`

## Execution logic

### A. If $ARGUMENTS is empty or is `help`
Ask what to contribute and show:
```
Usage:
  /contribute                         → interactive: ask for task
  /contribute <issue-or-pr-URL>       → run universal contribute pipeline (any repo)
  /contribute add skill <name>        → scaffold new skill in this repo
  /contribute fix <skill> <desc>      → patch existing skill
  /contribute docs                    → sync docs after code change
  /contribute review <path>           → code-review gate before PR
```

### B. Detect target repo
1. If $ARGUMENTS contains a URL with `github.com/`, `gitlab.com/`, or `gitea` and `/issues/` or `/pull/` or `/merge_requests/` → **external contribution** = follow `contribute` pipeline as primary.
2. Else if $ARGUMENTS mentions a skill name, `agents-skills`, or no URL → **internal contribution** to THIS repo (`/Users/marwanhassan/agents-skills`) = follow `contribution` pipeline as primary.
3. If ambiguous, ask once.

### C. Orchestration order (always load skills via the `skill` tool — do not skip)

Execute in this order, loading each skill's SKILL.md before acting on its steps:

**1. Ground in project conventions — `skill({ name: "contribution" })`**
- Load `contribution` skill first when target is THIS repo.
- Read `CONTRIBUTING.md`, `README.md` Available Skills table, `docs/architecture.md`, existing `skills/*/SKILL.md` for style/naming.
- Verify branch naming (`feat/<skill>` / `fix/<skill>-...`) and Conventional Commits.
- If external target, instead load `contribute` skill steps 1-5 (parse link, sync clone, read issue via ego-browser/gh, check prior PRs, learn conventions).

**2. Design before code — `skill({ name: "project-architecture" })` if needed**
- Trigger when: new skill, new module, or refactor touches ≥3 files.
- Otherwise note: "Architecture review skipped — single-file/minimal change" and proceed.
- When triggered: clarify domain boundaries, choose simplest style, define responsibilities/dependencies, propose folder tree.

**3. Decompose with parallel agents — `skill({ name: "multi-agents" })`**
- Required when task is non-trivial (repro, research, implementation, review would each be separate).
- Spawn 3 parallel sub-agents via `task` tool:
  - Root-Cause/Researcher: repro or trace to file:line
  - Codebase Researcher: files to touch, existing tests/patterns, conventions
  - Critic held for step 5 review
- Share full context (task, scope, constraints, acceptance criteria) with each.

**4. Implement — minimal surgical diff**
- Use outputs from steps 1-3 as spec.
- Keep diff minimal; note follow-ups separately.

**5. Review gate — `skill({ name: "code-review" })`**
- Load `code-review` skill. Run 6-dimension check (correctness, security, maintainability, performance, testing, clean code).
- Produce prioritized findings: 🔴 Blocking / 🟡 Important / 🟢 Suggestion with file:line, why, fix.
- Required verdict: Approve / Approve with comments / Request changes. Loop implement→review ≤3 rounds.

**6. Document — `skill({ name: "documentation" })` if docs changed**
- Trigger when: new skill added, README table changed, architecture changed, or user said `docs`.
- Verify every command/env var/endpoint against source file:line; fix stale sections; run link checks.

**7. Validate locally (never skip — from `contribution` workflow)**
```bash
for f in skills/*/SKILL.md; do
  dir=$(basename $(dirname "$f"))
  name=$(grep "^name:" "$f" | awk '{print $2}')
  [ "$dir" = "$name" ] && echo "✓ $f" || echo "✗ MISMATCH $f dir=$dir name=$name"
done

python3 -c "
import pathlib, yaml
for p in pathlib.Path('skills').glob('*/SKILL.md'):
    data = yaml.safe_load(p.read_text().split('---')[1])
    assert 'name' in data and 'description' in data
    print(f'✓ {p}')
"

git diff --stat
```

**8. Commit, push, PR (per CONTRIBUTING.md)**
- Branch from `main`, Conventional Commits `feat(<scope>): ...` or `fix(...): ...`
- Ask confirmation before `git push` / `gh pr create` (irreversible).

## Rules
- Always load the skill file before claiming to follow it — use `skill({ name: "<name>" })`.
- If a skill is not applicable, explicitly say why you skipped it (don't silently omit).
- When `contribute` pipeline is primary (external URL), still run code-review + documentation as steps 10 and 8 respectively per `docs/architecture.md` composition diagram.
- Prefer discovery via `read`, `glob`, `grep` — don't invent paths/commands.

Now execute for: `$ARGUMENTS`
If $ARGUMENTS is empty, ask for the contribution task (new skill name, issue URL, or file to fix) before proceeding.
