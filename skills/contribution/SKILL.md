---
name: contribution
description: Use this skill when guiding a contributor through this repository's contribution workflow. It follows CONTRIBUTING.md and repository conventions to help the agent clone, create skills, validate, and submit PRs correctly.
---

# Contribution

Teaches an AI agent how to contribute correctly to *this* repository (`agents-skills`), following its own conventions.

## Purpose

Ensure contributions are consistent, well-structured, and merge-ready by grounding the agent in the repository's actual rules rather than generic GitHub advice. Reduces review churn and keeps the skill catalog coherent.

## When to Use

- User says they want to contribute, add a skill, fix a skill, or open a PR against this repo
- User asks "how do I contribute?", "how do I add a new skill?", "what are the conventions?"
- Agent is about to scaffold a new `skills/<name>/SKILL.md` in this repository
- Before the agent commits, pushes, or opens a PR in this repo

## Workflow

### 1. Orient the contributor and set up the workspace

- Confirm the repo root is `agents-skills` (contains `skills/`, `CONTRIBUTING.md`, `README.md`)
- If cloning fresh:

  ```bash
  git clone https://github.com/marwan562/agents-skills.git
  cd agents-skills
  ```

- For fork workflow, verify remotes:

  ```bash
  git remote -v
  # expect origin -> contributor fork, upstream -> marwan562/agents-skills
  ```

- Ensure working from latest `main`:

  ```bash
  git checkout main
  git fetch upstream  # or origin if no upstream
  git pull --ff-only
  ```

### 2. Read the source of truth

- Open and follow `CONTRIBUTING.md` (the canonical workflow) and `docs/architecture.md` (why the layout is this way)
- Check root `README.md` → Available Skills table for naming collisions
- Inspect `skills/<existing>/SKILL.md` count and style to match tone
- Note commit convention (Conventional Commits) and branch naming (`feat/<skill>`, `fix/<skill>-...`)

### 3. Plan the change

- For **new skill**: propose `kebab-case` name, verify it matches directory, draft `description` (20-300 chars, trigger style: "Use when...")
- For **fix/docs**: identify the minimal diff; note if `README.md` catalog or `docs/architecture.md` also needs an update
- For **large or cross-cutting change**: advise opening an issue first (`Proposal: <skill-name> skill`) before coding — per `CONTRIBUTING.md`

### 4. Scaffold or edit

- New skill:

  ```bash
  mkdir -p skills/my-new-skill
  # Create skills/my-new-skill/SKILL.md with required frontmatter
  ```

- Frontmatter must be at line 1:

  ```yaml
  ---
  name: my-new-skill
  description: Use when you need to do X efficiently
  ---
  ```

- Body sections in order: `Purpose` → `When to Use` → `Workflow` → `Instructions` → `Constraints` → `Examples` (plus optional `References`)
- Keep the skill independent and reusable; no hard dependency on another skill without declaration

### 5. Update catalog and cross-references

- If adding a skill: add a row to `README.md` → Available Skills table

  ```markdown
  | **my-new-skill** | `skills/my-new-skill/` | Short purpose summary |
  ```

- Add installation examples for the new skill:

  ```bash
  npx skills add marwan562/agents-skills --skill my-new-skill
  ```

- Adjust structure diagrams if needed; do not restructure unrelated sections

### 6. Validate locally (never skip)

Run these before committing:

```bash
# 1. Each skill has SKILL.md and name matches directory
for f in skills/*/SKILL.md; do
  dir=$(basename $(dirname "$f"))
  name=$(grep "^name:" "$f" | awk '{print $2}')
  [ "$dir" = "$name" ] && echo "✓ $f" || echo "✗ MISMATCH $f dir=$dir name=$name"
done

# 2. No secrets / tokens in diff
git diff --cached  # review; ensure no .env, keys, tokens

# 3. Frontmatter parses
python3 -c "
import pathlib, yaml
for p in pathlib.Path('skills').glob('*/SKILL.md'):
    data = yaml.safe_load(p.read_text().split('---')[1])
    assert 'name' in data and 'description' in data
    print(f'✓ {p}')
"

# 4. Links resolve
# Click through README links to CONTRIBUTING.md and docs/architecture.md
```

### 7. Commit, push, and open PR

- Create a topic branch from `main`:

  ```bash
  git checkout -b feat/my-new-skill
  ```

- Commit with Conventional Commits:

  ```bash
  git add skills/my-new-skill/SKILL.md README.md
  git commit -m "feat(my-new-skill): add my-new-skill skill"
  ```

- Push and open PR:

  ```bash
  git push -u origin feat/my-new-skill
  gh pr create --title "feat(my-new-skill): add my-new-skill skill" --body "$(cat <<'EOF'
  ## Summary
  Adds `my-new-skill`...

  ## Changes
  - ...

  ## Validation
  - [x] Frontmatter valid
  - [x] No secrets in diff
  - [x] Links checked
  EOF
  )"
  ```

- If `gh` is not authenticated, instruct the user to run `gh auth login` and retry; do not fabricate a PR URL

## Instructions

- **Follow CONTRIBUTING.md first.** If this skill and CONTRIBUTING.md disagree, CONTRIBUTING.md wins — update this skill to match.
- **Keep diffs minimal.** One skill per PR; do not bundle unrelated reformatting.
- **Preserve existing style.** Mirror headings, tone, and table formatting from existing skills.
- **Validate file paths.** Use forward slashes, `skills/<name>/SKILL.md` exactly; do not create `skill/` or `SKILL.MD`.
- **Warn before external actions.** Confirm with the user before `git push` or `gh pr create` — these are public and irreversible.

## Constraints

- Do NOT overwrite `origin` or `upstream` remotes without asking
- Do NOT commit secrets, tokens, `.env`, or private URLs
- Do NOT change `LICENSE` or `.gitignore` unless explicitly requested
- Do NOT create a skill without `name` ≡ directory-name invariant
- Do NOT invent a `CONTRIBUTING.md` workflow that contradicts the actual file in the repo

## Examples

### Example 1 — Contributor wants to add a skill

> **User**: "I want to add a `testing` skill to this repo."

**Agent**:
1. Reads `CONTRIBUTING.md:1-50`, checks `skills/` for collision (`testing` not present)
2. Scaffolds `skills/testing/SKILL.md` with required sections
3. Updates `README.md` Available Skills table
4. Runs validation loop; shows `git diff --stat` and asks confirmation before push

### Example 2 — Quick fix to an existing skill

> **User**: "Fix a typo in the `code-review` skill."

**Agent**:
1. Reads `skills/code-review/SKILL.md:45`, patches typo
2. Validates frontmatter still parses, `name` unchanged
3. Commits as `fix(code-review): correct typo in workflow step 3`
4. Pushes only after confirmation

### Example 3 — Contributor asks how to contribute

> **User**: "How do I contribute here?"

**Agent**:
1. Summarizes `CONTRIBUTING.md`: clone → create `skills/<name>/SKILL.md` → validate → commit (`feat:`) → PR
2. Shows scaffold command and validation checklist
3. Points to `docs/architecture.md` for deeper design rationale

## References

- Canonical workflow: `CONTRIBUTING.md`
- Architecture rationale: `docs/architecture.md`
- Skill spec and install guide: `README.md`
