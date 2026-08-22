# Architecture

This document explains the architecture of the **agents-skills** repository, why it is organized this way, and how contributors and consumers should work with it.

## Overview

`agents-skills` is a **flat, file-based skills registry**. There is no build step, no runtime, and no code generation. The entire artifact is Markdown + YAML frontmatter, organized by convention so that:

- Agents (OpenCode, Claude Code, etc.) can discover skills deterministically.
- Humans can browse, copy, and contribute without tooling.
- `skills.sh` and similar registries can index the repository automatically.

## Repository Structure

```
/
├── README.md                    # Project entry point, skill catalog, install/usage
├── CONTRIBUTING.md              # Contributor workflow, skill spec, commit/PR rules
├── LICENSE                      # MIT
├── .gitignore                   # Standard OS/editor/build ignores
├── skills/                      # One directory per skill
│   ├── project-architecture/
│   │   └── SKILL.md
│   ├── code-review/
│   │   └── SKILL.md
│   ├── documentation/
│   │   └── SKILL.md
│   ├── contribution/
│   │   └── SKILL.md
│   ├── contribute/
│   │   └── SKILL.md
│   └── multi-agents/
│       └── SKILL.md
└── docs/
    └── architecture.md          # This file
```

### Why this layout?

| Decision | Rationale |
|---|---|
| **One directory per skill** | Enables independent versioning, per-skill `skills add --skill <name>` installs, and isolated PRs (one skill per PR). Avoids merge conflicts in a monolithic file. |
| **Single `SKILL.md` per skill** | Required by the Agent Skills spec. Registry crawlers look for `skills/<name>/SKILL.md` exactly. Additional files would be ignored or create ambiguity. |
| **Top-level `skills/` directory** | Convention adopted by `skills.sh` and OpenCode. Keep the name `skills` — do not rename to `skill` or `agent-skills`. |
| **No code artifacts** | Skills are instructions for LLMs, not executable programs. Adding code would couple the repo to a language/toolchain and violate the "simple and clean" goal. |
| **`docs/` for meta-documentation** | Separates contributor-oriented docs (`CONTRIBUTING.md` at root for GitHub discovery, `architecture.md` under `docs/` for deep dives) from the skill catalog itself. |
| **Root `README.md` as catalog** | Skills.sh renders `README.md` as the marketplace page. The Available Skills table is therefore both the GitHub front page and the registry listing. |

## Why Skills Are Separated into Individual Directories

1. **Discoverability**: Registries scan `skills/*/SKILL.md`. A flat list of directories is trivial to enumerate with `glob("skills/*/SKILL.md")`. A single file would require parsing sections/anchors.

2. **Independent lifecycle**: Each skill has its own purpose, version history, and review scope. Separating files means `git log -- skills/code-review/` shows only relevant changes, and PRs stay focused.

3. **Install granularity**: Users often want one skill, not all. Package managers implement `skills add <repo> --skill <name>` by copying `skills/<name>/`. A monolithic `SKILL.md` cannot support partial installs without extra tooling.

4. **Namespace safety**: Frontmatter `name` must equal the directory name (`kebab-case`). This provides a filesystem-enforced uniqueness guarantee. Two skills cannot silently claim the same name.

5. **Contributor ergonomics**: A contributor adding `api-design` only touches `skills/api-design/SKILL.md` + `README.md` (catalog entry). No need to edit shared files or resolve conflicts in a giant document.

## How Skills Are Discovered

### At runtime (by an agent)

1. Agent reads its configured skill registries (e.g., `npx skills add` installed to `~/.config/opencode/skills/` or project-local `.skills/`).
2. Each `SKILL.md` frontmatter is parsed:
   ```yaml
   ---
   name: code-review
   description: Use when reviewing code for correctness, security, ...
   ---
   ```
3. The `description` becomes the **trigger** — the agent's router compares the user's task ("review this PR", "design architecture") against each skill's description and selects the best match.
4. On match, the agent **loads the full `SKILL.md` body** as instructions and follows its `Workflow`, `Constraints`, and `Examples`.

### At install time (by a human)

- **skills.sh**: User runs `npx skills add marwan562/agents-skills [--skill <name>]`. The CLI clones the repo and copies `skills/<name>/SKILL.md` to the local skills directory.
- **Manual**: `git clone https://github.com/marwan562/agents-skills.git` then copy `skills/<name>/` to the desired location.
- **OpenCode**: Listed in `opencode.json` under `skills` or placed in `.opencode/skills/`.

### Indexing implications for contributors

- Keep `name` and `description` stable — renaming breaks installs.
- Write `description` as a **when-to-use clause** ("Use when...", "Helps the agent..."), not a marketing tagline. The LLM router depends on this phrasing.
- Validate frontmatter on every PR (see `CONTRIBUTING.md`).

## How Contributors Should Extend the Repository

### Adding a new skill

1. Pick a `kebab-case` name, create `skills/<name>/`.
2. Write `skills/<name>/SKILL.md` per `CONTRIBUTING.md` spec.
3. Update `README.md` → Available Skills table + installation examples.
4. Run local validation (frontmatter, links, secrets scan).
5. Open PR with `feat(<name>): ...` commit.

### Modifying an existing skill

- Edit only `skills/<name>/SKILL.md`. Preserve `name` unless intentionally renaming (which is a breaking change — call out in PR).
- Keep changes **backward compatible** where possible: additive workflow steps are safe; removing or reordering steps requires justification.
- Update `README.md` if the skill's purpose/usage changed materially.

### Proposing cross-cutting changes

- If a change affects all skills (e.g., new frontmatter field, new required section), open an **issue first** proposing the convention. Get approval before updating every file.

## How Skills Work with Different AI Coding Agents

The repository is **agent-agnostic** by design:

| Concern | Handling |
|---|---|
| **Instruction format** | `SKILL.md` is plain Markdown. No agent-specific syntax (no Claude-only or OpenCode-only blocks). If an agent requires extra metadata, it reads frontmatter; the body remains portable. |
| **Triggering** | Agents that support `description`-based routing (OpenCode, Claude Code) use frontmatter `description`. Agents without routing can still be prompted manually: "Use the `code-review` skill from `skills/code-review/SKILL.md`". |
| **Workflow steps** | Written as generic imperatives ("Analyze requirements", "Propose folder structure"), not as tool-specific commands. Where tools are mentioned (`git`, `gh`, `grep`), alternatives are noted (`glab`, `web_fetch`). |
| **Constraints** | Scope limits are stated in terms of agent behavior ("Do not over-engineer", "Do not commit without confirmation"), which any agent can obey regardless of tooling. |
| **Examples** | Include both the user prompt and expected agent actions in natural language, not in a single agent's DSL. |

### Compatibility checklist for skill authors

- [ ] No hardcoded agent name in the workflow ("You are Claude..." → avoid; write "You are an AI coding agent...")
- [ ] No dependency on a specific tool unless flagged with fallback (e.g., "`gh` for GitHub, `glab` for GitLab, else `web_fetch`")
- [ ] Works when the skill file is the agent's only context (self-contained): includes purpose, workflow, constraints, examples — no external lookup required to execute

## Non-Goals

- **No runtime code** — Skills never contain executable code beyond documentation examples. The repo is not an npm/pip package.
- **No monolithic skill** — One `SKILL.md` per skill, always. Grouping related workflows ("all testing skills in one file") harms discoverability and install granularity.
- **No over-engineering** — No CI-generated skills, no templating engine, no skill dependency graph. If a skill needs another skill, it declares it in prose ("Delegate to `multi-agents` as described in..."), not via import.

## Future Evolution

Potential extensions that remain compatible with the current architecture:

- **Validation CI**: GitHub Action that lints `skills/*/SKILL.md` frontmatter and checks `name` ≡ directory.
- **Skill versioning**: Optional `version` field in frontmatter (semver) for breaking changes.
- **References**: Subdirectories like `skills/<name>/references/` for lengthy templates (e.g., `contribute` may grow reference files). This pattern is already used in the `contribute` skill's upstream source — adopt it per-skill only when a single `SKILL.md` exceeds ~300 lines.

For now, the repository intentionally stays minimal: **Markdown files + convention + registry**.
