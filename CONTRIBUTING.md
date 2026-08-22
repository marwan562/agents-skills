# Contributing to agents-skills

Thank you for considering contributing to **agents-skills**! This document explains how to set up the repository, create new skills, and submit high-quality pull requests that align with the Agent Skills ecosystem.

## Code of Conduct

Be respectful, constructive, and collaborative. We aim for a welcoming community for all contributors regardless of experience level.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/marwan562/agents-skills.git
cd agents-skills
```

If you plan to contribute via a fork:

```bash
gh repo fork marwan562/agents-skills --clone
cd agents-skills
git remote add upstream https://github.com/marwan562/agents-skills.git
git fetch upstream
```

### 2. Explore the structure

```
/
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── .gitignore
├── skills/
│   ├── project-architecture/SKILL.md
│   ├── code-review/SKILL.md
│   ├── documentation/SKILL.md
│   ├── contribution/SKILL.md
│   ├── contribute/SKILL.md
│   └── multi-agents/SKILL.md
└── docs/
    └── architecture.md
```

Each skill is **self-contained** in `skills/<skill-name>/SKILL.md`.

### 3. Install / Use the skills locally

#### Via skills.sh (recommended for consumers)

```bash
npx skills add marwan562/agents-skills
# or single skill
npx skills add marwan562/agents-skills --skill code-review
```

#### Local development (for contributors)

Copy a skill into your agent's skills directory or reference directly:

```bash
# OpenCode
cp -r skills/project-architecture ~/.config/opencode/skills/

# Or test via direct path — most agents can load SKILL.md by absolute path
```

No build step is required. Skills are plain Markdown + frontmatter.

## How to Create a New Skill

### Naming conventions

- Use **kebab-case**: `my-new-skill`, `api-design`, `test-generator`
- Name must match the directory name exactly
- Keep names short, descriptive, and generic (no brand-specific terms unless the skill is brand-specific)
- Avoid duplicates — check `skills/` directory first

### Required `SKILL.md` structure

Every `SKILL.md` **must** have:

```markdown
---
name: my-new-skill
description: One sentence describing when the agent should use this skill
---

# My New Skill

## Purpose
What problem this skill solves and why it exists.

## When to Use
Trigger conditions — what user intent or task should activate this skill.

## Workflow
Step-by-step instructions the agent should follow.

## Instructions
Detailed guidance, constraints, best practices.

## Constraints
What the agent must NOT do.

## Examples
Concrete input/output examples showing correct usage.

## References (optional)
Links to related skills or external docs.
```

#### Frontmatter rules (validated on PR)

- `name`: `^[a-z0-9]+(-[a-z0-9]+)*$` — lowercase kebab-case, must equal directory name
- `description`: non-empty, 20-300 characters, starts with action verb or "Use when..."
- Must be valid YAML between `---` delimiters at the very top of the file

#### Content guidelines

- **Purpose**: 2-5 sentences, outcome-oriented
- **When to Use**: bullet list of trigger phrases/tasks
- **Workflow**: numbered steps, each step actionable
- **Constraints**: explicit prohibitions and scope limits
- **Examples**: at least 1, ideally 2-3 (input prompt → expected agent behavior)
- Keep the skill **independent** — no hard dependency on another skill unless explicitly declared
- Prefer **general applicability** over project-specific hacks

### Scaffolding a skill

```bash
mkdir -p skills/my-new-skill
cat > skills/my-new-skill/SKILL.md << 'EOF'
---
name: my-new-skill
description: Use this skill when you need to accomplish X efficiently
---

# My New Skill

## Purpose
...

## When to Use
...

## Workflow
...

## Constraints
...

## Examples
...

EOF
```

## Testing / Validation Before Submitting a PR

Before opening a PR, **validate locally**:

### 1. Structure check

```bash
# Verify each skill has SKILL.md
ls skills/*/SKILL.md

# Verify directory name matches frontmatter name
for f in skills/*/SKILL.md; do
  dir=$(basename $(dirname "$f"))
  front=$(head -n 20 "$f" | grep "^name:" | awk '{print $2}')
  if [ "$dir" != "$front" ]; then
    echo "MISMATCH: $f dir=$dir front=$front"
  fi
done
```

### 2. Frontmatter validation

- Ensure file starts with `---` on line 1
- Ensure YAML parses (no tabs, correct indentation)
- `name` and `description` present and correctly formatted

You can use a quick Python check:

```bash
python3 -c "
import re, pathlib, yaml
for p in pathlib.Path('skills').glob('*/SKILL.md'):
    text = p.read_text()
    assert text.startswith('---'), f'{p} missing frontmatter'
    parts = text.split('---')
    assert len(parts) >= 3, f'{p} invalid frontmatter delimiters'
    data = yaml.safe_load(parts[1])
    assert 'name' in data and 'description' in data, f'{p} missing name/description'
    print(f'✓ {p}: {data[\"name\"]}')
"
```

> If `pyyaml` is not installed: `pip install pyyaml`

### 3. Content quality

- No secrets, API keys, tokens, passwords, or private URLs
- No broken links (check Markdown links)
- Spell-check and grammar-check
- Markdown renders correctly (preview in GitHub)

### 4. Links and references

- Verify all relative links resolve (e.g., `../docs/architecture.md`)
- Verify external links are reachable

## Commit Conventions

We follow **Conventional Commits**:

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

**Types:**

- `feat`: new skill or major feature
- `fix`: bug fix in a skill or docs
- `docs`: documentation-only change
- `refactor`: restructuring without behavior change
- `chore`: tooling, config, maintenance
- `style`: formatting, typos

**Examples:**

```
feat(code-review): add security checklist section
fix(documentation): correct workflow step order
docs: update installation examples in README
feat(skill): add api-design skill
chore: update .gitignore
```

- Use **present tense**, **lowercase** after colon, **no period** at end
- Keep first line ≤ 72 characters
- Sign off commits if required: `git commit -s -m "feat: ..."`

## Pull Request Rules

### Before opening a PR

- [ ] Branch from `main`: `git checkout -b feat/my-new-skill`
- [ ] One skill per PR (unless skills are tightly coupled — justify in description)
- [ ] All validation steps above pass
- [ ] No secrets or private data in diff (`git diff` review)
- [ ] README updated if adding a new skill (Available Skills table)
- [ ] `docs/architecture.md` still accurate

### Branch naming

- `feat/<skill-name>` — new skill
- `fix/<skill-name>-<short-desc>` — fix
- `docs/<desc>` — docs-only change

### PR description template

```markdown
## Summary
One sentence: what this PR does.

## Changes
- Added/changed ...
- Updated ...

## Skill Details (if adding a skill)
- Name: `my-new-skill`
- Purpose: ...
- Trigger: when the user does X

## Validation
- [ ] Frontmatter valid (name matches directory)
- [ ] No secrets in diff
- [ ] Links checked
- [ ] Markdown renders correctly

Closes #<issue-number> (if applicable)
```

### Review process

1. Automated checks (structure, frontmatter) — must pass
2. Maintainer review — feedback within 3-5 days
3. Address comments → push new commits (don't force-push during review)
4. Approval → squash or merge by maintainer

## Code / Documentation Quality Expectations

- **Clear**: short sentences, active voice, concrete steps
- **Accurate**: workflows must be tested against a real agent
- **Minimal**: no over-engineering, no unnecessary sections
- **Consistent**: follow existing skill structure and tone
- **Independent**: skills must work standalone — no cross-file hidden dependencies
- **Portable**: avoid hardcoding paths, hosts, or language-specific assumptions unless the skill is explicitly language-scoped

## How to Propose New Skills

1. **Open an issue first** (recommended for large skills):

   - Title: `Proposal: <skill-name> skill`
   - Body: problem statement, proposed workflow, example usage, why it belongs in this collection vs. standalone

2. **Community discussion**: maintainers will label as `proposal` / `needs-discussion` / `approved`

3. **Build the skill**: scaffold under `skills/<name>/SKILL.md` per guidelines above

4. **Submit PR**: link the proposal issue with `Closes #...`

Alternatively, for small or obvious skills, skip the issue and open a PR directly with a clear description.

## Questions?

- Open an issue with label `question`
- Check existing skills for patterns and examples
- See `docs/architecture.md` for repository design rationale

Thank you for contributing!
