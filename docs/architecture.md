# Architecture

This document explains the architecture of the **agents-skills** repository, why it is organized this way, how skills interoperate, and how contributors and consumers should work with it.

## Overview

`agents-skills` is a **flat, file-based skills registry**. There is no build step, no runtime, and no code generation. The entire artifact is Markdown + YAML frontmatter, organized by convention so that:

- Agents (OpenCode, Claude Code, Antigravity, etc.) can discover skills deterministically.
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
    └── architecture.md          # This file
```

### Why this layout?

| Decision | Rationale |
|---|---|
| **One directory per skill** | Enables independent versioning, per-skill `skills add --skill <name>` installs, and isolated PRs (one skill per PR). Avoids merge conflicts in a monolithic file. |
| **Single `SKILL.md` per skill** | Required by the Agent Skills spec. Registry crawlers look for `skills/<name>/SKILL.md` exactly. Additional files would be ignored or create ambiguity. |
| **Modular `references/` subdirectories** | For complex skills like `contribute`, reference templates (briefs, ecosystem matrix, PR templates) live alongside `SKILL.md` in `references/`, keeping the main instruction file clear and maintainable. |
| **Top-level `skills/` directory** | Convention adopted by `skills.sh` and OpenCode. Keep the name `skills` — do not rename to `skill` or `agent-skills`. |
| **No code artifacts** | Skills are instructions for LLMs, not executable programs. Adding code would couple the repo to a language/toolchain and violate the "simple and clean" goal. |
| **`docs/` for meta-documentation** | Separates contributor-oriented docs (`CONTRIBUTING.md` at root for GitHub discovery, `architecture.md` under `docs/` for deep dives) from the skill catalog itself. |
| **Root `README.md` as catalog** | Skills.sh renders `README.md` as the marketplace page. The Available Skills table is therefore both the GitHub front page and the registry listing. |

---

## The Contribution Skills: `contribute` vs `contribution`

This repository includes two distinct skills related to contribution. It is important to understand their different scopes:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             CONTRIBUTION SKILL SCOPES                            │
├────────────────────────────────────────┬─────────────────────────────────────────┤
│    skills/contribution/SKILL.md        │        skills/contribute/SKILL.md       │
│         (Internal Meta-Skill)          │       (Universal OSS Pipeline)          │
├────────────────────────────────────────┼─────────────────────────────────────────┤
│ • Targets THIS repository only         │ • Targets ANY external OSS repository   │
│ • Follows repo CONTRIBUTING.md rules   │ • Works across GitHub, GitLab, Gitea    │
│ • Guides adding/updating skills here   │ • Works across ANY programming language │
│ • Validates SKILL.md frontmatter       │ • Autonomous 12-step issue → PR flow    │
│ • Human-guided interactive workflow    │ • Zero unnecessary interruptions        │
└────────────────────────────────────────┴─────────────────────────────────────────┘
```

1. **[`contribution`](../skills/contribution/SKILL.md)**:
   - Guides contributors and agents on how to add, modify, validate, and document skills **inside the `agents-skills` repository**.
   - Grounded in this repository's [`CONTRIBUTING.md`](../CONTRIBUTING.md) and [`docs/architecture.md`](architecture.md).

2. **[`contribute`](../skills/contribute/SKILL.md)**:
   - A universal, autonomous, end-to-end pipeline that takes an external issue or pull request URL and delivers a tested, maintainer-reviewed PR in **any external repository and any language**.

---

## Deep Dive: The `contribute` Skill Pipeline

The updated `contribute` skill implements an **autonomous 12-step contribution pipeline** designed to run with minimal human intervention. Once invoked with an issue URL, it runs end-to-end and only pauses at four explicit checkpoints.

### The 12-Step Pipeline

```
  [1. Parse Link] ──> [2. Sync Clone] ──> [3. Read Issue/PR (/ego-browser)]
                                                     │
  [6. Branch] <── [5. Detect Conventions] <── [4. Check Prior Art / Sibling PRs]
       │
       ▼
  [7. Delegate to /multi-agents]
       ├── Root-Cause Analyst (reproduce/isolate)
       └── Codebase Researcher (conventions/tests/files)
       │
       ▼
  [8. Implement Diff] ──> [9. Verify Locally] ──> [10. Maintainer Review Loop]
                                                              │ (Senior Reviewer)
                                                              ▼
  [12. Handoff Summary] <── [11. Commit, Push & Open PR (Auto)] ◄── Passes
```

1. **Parse Link**: Extracts host (GitHub, GitLab, Gitea), owner, repo, and issue/PR number.
2. **Locate & Sync Local Clone**: Finds the local clone under `~/contributions/<repo>`, checks remotes (`origin` fork vs `upstream`), pulls the real default branch.
3. **Read Issue or PR**: Uses browser inspection (`/ego-browser`) to capture rendered context (linked PRs sidebar, maintainer priority comments, reactions, issue threads).
4. **Check Related Work & Duplicates**: Checks candidate PRs, sibling repository issues (e.g. `sveltejs/svelte` vs `sveltejs/kit`), and stale/rejected prior attempts.
5. **Learn Project Conventions**: Reads `CONTRIBUTING.md`, style guides, linters, and CI configurations using [`ecosystem-detection.md`](../skills/contribute/references/ecosystem-detection.md).
6. **Create Working Branch**: Uses project branch conventions (e.g. `fix/<issue-number>-<slug>`).
7. **Delegate Analysis to `/multi-agents`**: Dispatches parallel sub-agents using [`multi-agent-brief.md`](../skills/contribute/references/multi-agent-brief.md).
8. **Implement**: Applies the minimal surgical diff.
9. **Verify Locally**: Executes actual project test, lint, and build suites.
10. **Maintainer-Style Review**: Loops diff through Senior Maintainer Reviewer (up to 3 iterations).
11. **Commit, Push, and Open PR**: Formats commit message, pushes to fork, and creates PR using [`pr-template.md`](../skills/contribute/references/pr-template.md).
12. **Handoff**: Summarizes the contribution and returns the PR link.

### The 4 Stopping Checkpoints
The skill only stops and asks the user in 4 specific situations:
1. Uncommitted local changes in the repository clone.
2. No local clone found on disk (confirms cloning location).
3. Step 4 finds an existing merged or high-quality open PR already resolving the issue.
4. Step 10 review loop does not converge after three rounds of changes.

---

## Skill Composition: Companion Skills Required by `contribute`

While each skill is self-contained and independently installable, complex workflows like `contribute` orchestrate specialized sub-skills to achieve modularity without tight code coupling.

```
                            ┌────────────────────────┐
                            │       contribute       │
                            │ (Orchestration Pipeline│
                            └───────────┬────────────┘
                                        │
     ┌──────────────────┬───────────────┼───────────────┬──────────────────┐
     ▼                  ▼               ▼               ▼                  ▼
┌──────────────┐ ┌──────────────┐ ┌───────────┐ ┌──────────────┐ ┌────────────────────┐
│ /ego-browser │ │ multi-agents │ │code-review│ │documentation │ │project-architecture│
│ (Step 3 & 4) │ │ (Step 7 & 10)│ │ (Step 10) │ │ (Doc Updates)│ │(Complex Features)  │
└──────────────┘ └──────────────┘ └───────────┘ └──────────────┘ └────────────────────┘
```

The `contribute` pipeline coordinates with the following companion skills:

### 1. [`multi-agents`](../skills/multi-agents/SKILL.md) (Required for Step 7 & 10)
- **Why it is needed:** Decomposes deep codebase analysis into parallel, specialized sub-agent roles rather than doing a shallow single-pass edit.
- **Roles spawned:**
  - **Root-Cause Analyst**: Reproduces the problem and isolates the exact faulty lines.
  - **Codebase & Convention Researcher**: Gathers relevant files, existing tests, and project patterns.
  - **Senior Maintainer Reviewer**: Holds the maintainer standard during the Step 10 review loop.
- **Reference Brief:** Uses [`skills/contribute/references/multi-agent-brief.md`](../skills/contribute/references/multi-agent-brief.md).

### 2. `/ego-browser` (Required for Steps 3 & 4)
- **Why it is needed:** Allows the agent to inspect the fully rendered web page of the issue/PR. This surfaces critical context that raw API dumps or text fetches miss:
  - "Linked Pull Requests" sidebar indicators
  - Maintainer reactions and upvotes
  - Sibling-repository cross-references across monorepo-adjacent organizations
  - Detailed maintainer feedback on stale/rejected prior PRs
- **Fallback:** If `/ego-browser` is not available, falls back to `gh`/`glab` CLI or `web_fetch`.

### 3. [`code-review`](../skills/code-review/SKILL.md) (Companion for Step 10)
- **Why it is needed:** Supplies the multi-dimensional auditing checklist (Correctness, Security, Maintainability, Performance, Testing) used by the Senior Maintainer Reviewer role to review the diff before opening the PR.

### 4. [`documentation`](../skills/documentation/SKILL.md) (Companion for Step 8/Docs)
- **Why it is needed:** When a contribution introduces or changes public APIs, configuration options, or commands, `documentation` ensures accurate README, changelog, and API doc updates accompany the code diff.

### 5. [`project-architecture`](../skills/project-architecture/SKILL.md) (Companion for Large Features)
- **Why it is needed:** For cross-cutting or large feature issues, `project-architecture` provides clean module boundaries, interface design, and architectural trade-off analysis before implementation starts.

---

## How Skills Are Discovered

### At runtime (by an agent)

1. Agent reads its configured skill registries (e.g., `npx skills add` installed to `~/.config/opencode/skills/` or project-local `.skills/`).
2. Each `SKILL.md` frontmatter is parsed:
   ```yaml
   ---
   name: contribute
   description: Use this skill whenever the user wants to contribute to an open-source project...
   ---
   ```
3. The `description` becomes the **trigger** — the agent's router compares the user's task against each skill's description and selects the best match.
4. On match, the agent **loads the full `SKILL.md` body** as instructions and follows its `Workflow`, `Constraints`, and `Examples`.

### At install time (by a human)

- **skills.sh**: User runs `npx skills add marwan562/agents-skills [--skill <name>]`.
- **Manual**: `git clone https://github.com/marwan562/agents-skills.git` then copy `skills/<name>/` to the desired location.
- **OpenCode**: Listed in `opencode.json` under `skills` or placed in `.opencode/skills/`.

---

## How Contributors Should Extend the Repository

### Adding a new skill

1. Pick a `kebab-case` name, create `skills/<name>/`.
2. Write `skills/<name>/SKILL.md` per [`CONTRIBUTING.md`](../CONTRIBUTING.md) spec.
3. If the skill requires reference files (like templates or command matrices), place them under `skills/<name>/references/`.
4. Update `README.md` → Available Skills table + installation examples.
5. Run local validation (frontmatter, links, secrets scan).
6. Open PR with `feat(<name>): ...` commit.

### Modifying an existing skill

- Edit `skills/<name>/SKILL.md` and related reference files.
- Keep changes **backward compatible** where possible.
- Update `README.md` and `docs/architecture.md` if the skill's purpose or workflow changed.

---

## Non-Goals

- **No runtime code** — Skills never contain executable code beyond documentation examples. The repo is not an npm/pip package.
- **No monolithic skill** — One `SKILL.md` per skill. Grouping related workflows harms discoverability and install granularity.
- **No tight programmatic coupling** — Skills declare relationships in prose and reference templates, maintaining compatibility across all LLM runtimes.
