# agents-skills

A curated collection of reusable **Agent Skills** for AI coding agents. Production-ready, open-source, and compatible with the [Agent Skills](https://skills.sh) ecosystem and tools like [OpenCode](https://opencode.ai), Claude Code, Antigravity, and others that support the `SKILL.md` specification.

## Why this project exists

AI coding agents work best with focused, reusable instructions. Instead of pasting the same long prompts for architecture design, code review, documentation, or contribution workflows, this repository packages each workflow as an **independent, versioned Skill** that any agent can discover and load.

Goals:
- **Simple** — no build step, no over-engineering. Markdown + convention.
- **Reusable** — each skill is self-contained and works across projects and languages.
- **Discoverable** — published to [skills.sh](https://skills.sh) for one-command install.
- **Contributor-friendly** — clear structure, validated `SKILL.md` files, easy to extend.

## Available Skills

| Skill | Directory | Scope & Purpose |
|---|---|---|
| [**competitive-programming-coach**](skills/competitive-programming-coach/SKILL.md) | [`skills/competitive-programming-coach/`](skills/competitive-programming-coach/) | Socratic coaching & expert solving for LeetCode, Codeforces, AtCoder, and contest algorithms |
| [**project-architecture**](skills/project-architecture/SKILL.md) | [`skills/project-architecture/`](skills/project-architecture/) | Design clean, scalable project architectures and module boundaries from requirements |
| [**code-review**](skills/code-review/SKILL.md) | [`skills/code-review/`](skills/code-review/) | Systematic code review for correctness, security, performance, and maintainability |
| [**documentation**](skills/documentation/SKILL.md) | [`skills/documentation/`](skills/documentation/) | Create and maintain accurate project documentation, changelogs, and API references |
| [**contribution**](skills/contribution/SKILL.md) | [`skills/contribution/`](skills/contribution/) | Guide contributors specifically through *this* repository's (`agents-skills`) workflow |
| [**contribute**](skills/contribute/SKILL.md) | [`skills/contribute/`](skills/contribute/) | Autonomous 12-step open-source contribution pipeline (issue → PR) for *any* repo, host, and language |
| [**multi-agents**](skills/multi-agents/SKILL.md) | [`skills/multi-agents/`](skills/multi-agents/) | Orchestrate complex tasks through parallel sub-agent collaboration (research, implement, review) |

> Each skill lives in its own directory under `skills/` and contains a single `SKILL.md` (and optional `references/` for extensive templates). This makes skills independently installable and versionable.

See [`docs/architecture.md`](docs/architecture.md) for detailed repository design, skill composition, and workflow architecture.

---

## Skill Composition & How Skills Work Together

While every skill functions standalone, higher-level workflow skills coordinate with specialized companion skills for enhanced precision:

```
                            ┌────────────────────────┐
                            │       contribute       │
                            │ (Autonomous Pipeline)  │
                            └───────────┬────────────┘
                                        │
     ┌──────────────────┬───────────────┼───────────────┬──────────────────┐
     ▼                  ▼               ▼               ▼                  ▼
┌──────────────┐ ┌──────────────┐ ┌───────────┐ ┌──────────────┐ ┌────────────────────┐
│ /ego-browser │ │ multi-agents │ │code-review│ │documentation │ │project-architecture│
│(Issue & PR UI│ │(Root-Cause & │ │(Maintainer│ │(Changelog &  │ │(Module Boundary   │
│ Inspection)  │ │ Research)    │ │ Diff Pass)│ │ API Docs)    │ │ Design)            │
└──────────────┘ └──────────────┘ └───────────┘ └──────────────┘ └────────────────────┘
```

- **[`contribute`](skills/contribute/SKILL.md)** delegates deep root-cause reproduction and codebase research to **[`multi-agents`](skills/multi-agents/SKILL.md)** in Step 7.
- It leverages browser tools (`/ego-browser`) in Steps 3–4 to inspect rendered GitHub/GitLab issue sidebars, linked PRs, and maintainer feedback.
- It uses the multi-point checklist from **[`code-review`](skills/code-review/SKILL.md)** for Senior Maintainer diff reviews in Step 10 before opening the PR.
- For doc-heavy changes, it pairs with **[`documentation`](skills/documentation/SKILL.md)**; for large architectural refactors, it pairs with **[`project-architecture`](skills/project-architecture/SKILL.md)**.
- If you are contributing specifically to this skills collection itself, use **[`contribution`](skills/contribution/SKILL.md)**.

---

## Installation

### Via skills.sh (recommended)

Install the entire collection:

```bash
npx skills add marwan562/agents-skills
```

Install a single skill:

```bash
npx skills add marwan562/agents-skills --skill competitive-programming-coach
npx skills add marwan562/agents-skills --skill project-architecture
npx skills add marwan562/agents-skills --skill code-review
npx skills add marwan562/agents-skills --skill documentation
npx skills add marwan562/agents-skills --skill contribution
npx skills add marwan562/agents-skills --skill contribute
npx skills add marwan562/agents-skills --skill multi-agents
```

Browse and install visually at: `https://skills.sh/marwan562/agents-skills`

Alternative registry syntax (if your CLI differs):

```bash
# Generic: clone and reference locally
git clone https://github.com/marwan562/agents-skills.git
```

### Via OpenCode

Add to your `opencode.json`:

```json
{
  "skills": ["marwan562/agents-skills"]
}
```

Or copy a specific `SKILL.md` into your project's `.opencode/skills/` or `~/.config/opencode/skills/`.

### Manual

```bash
git clone https://github.com/marwan562/agents-skills.git
cp -r agents-skills/skills/<skill-name> ./your-project/.skills/
```

## Usage

Skills are loaded automatically by compatible agents when the task matches the skill's `description` in the frontmatter. You can also invoke them explicitly:

**OpenCode / Claude Code / Agent examples:**

```
> Help me solve this Codeforces problem using competitive-programming-coach: https://codeforces.com/problemset/problem/1234/D

> Use the project-architecture skill to design the architecture for a real-time chat app with WebSockets.

> Run code-review on the recent changes in src/auth/

> Use documentation to generate API docs for this codebase.

> I want to contribute to this repo — use the contribution skill.

> Here's the next issue: https://github.com/owner/repo/issues/42 — use contribute

> Use multi-agents to break this refactor into parallel workstreams
```

**When a skill triggers, the agent:**
1. Reads `skills/<name>/SKILL.md` for the workflow
2. Follows the instructions, constraints, and workflow steps
3. Produces output consistent with the skill's specification

## How to create your own skill

```bash
# 1. Scaffold a new skill directory
mkdir -p skills/my-new-skill

# 2. Create SKILL.md with required frontmatter
cat > skills/my-new-skill/SKILL.md << 'EOF'
---
name: my-new-skill
description: One-line description of when this skill should be used
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

# 3. Validate (no secrets, valid frontmatter, correct structure)
# 4. Submit a PR — see CONTRIBUTING.md
```

Full guide: [`CONTRIBUTING.md`](CONTRIBUTING.md) (section: "How to Create a New Skill")

Required `SKILL.md` frontmatter:

```yaml
---
name: my-new-skill        # kebab-case, matches directory name
description: Clear trigger description for the agent
---
```

## Repository Structure

```
/
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── .gitignore
├── skills/
│   ├── competitive-programming-coach/
│   │   └── SKILL.md
│   ├── project-architecture/
│   │   └── SKILL.md
│   ├── code-review/
│   │   └── SKILL.md
│   ├── documentation/
│   │   └── SKILL.md
│   ├── contribution/
│   │   └── SKILL.md
│   ├── contribute/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── ecosystem-detection.md
│   │       ├── multi-agent-brief.md
│   │       └── pr-template.md
│   └── multi-agents/
│       └── SKILL.md
└── docs/
    └── architecture.md
```

## Contributing

We welcome contributions! See [`CONTRIBUTING.md`](CONTRIBUTING.md) for:

- Cloning and local setup
- Skill naming conventions
- `SKILL.md` structure and validation
- Commit and PR rules
- Proposing new skills

Quick start:

```bash
git clone https://github.com/marwan562/agents-skills.git
cd agents-skills
# create your skill under skills/<name>/SKILL.md
```

## License

[MIT](LICENSE) — Copyright (c) 2026 agents-skills contributors
