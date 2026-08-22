---
name: documentation
description: Use this skill when creating or maintaining project documentation — README, API docs, guides, ADRs, or inline docs. The agent should first understand the existing codebase before writing, ensuring docs are accurate and not hallucinated.
---

# Documentation

Guides an AI agent to produce accurate, maintainable documentation by first grounding itself in the actual codebase.

## Purpose

Create documentation that is **true to the code**, easy to navigate, and cheap to keep updated. Avoids the common failure of writing plausible but incorrect docs from memory or assumptions.

## When to Use

- User asks to write, update, or improve docs (`README`, `CONTRIBUTING`, API reference, guides, `docs/` pages)
- User asks to document a module, endpoint, function, or workflow
- User says "explain this codebase" or "onboard me to this repo"
- User requests ADRs, architecture docs, or runbooks
- Keywords: `documentation`, `docs`, `README`, `guide`, `API docs`, `explain`, `onboard`

## Workflow

### 1. Discover before writing

- Inventory the codebase: entry points, top-level folders, package manifests (`package.json`, `go.mod`, `pyproject.toml`, etc.), routing/config files
- Check for existing docs: `README.md`, `docs/`, `CONTRIBUTING.md`, `CHANGELOG.md`, inline comments
- Identify the primary audience: new contributor, end user, operator, or API consumer — scope and tone follow from this
- **Do not write yet.** Grounding first prevents hallucinated endpoints, env vars, or commands.

### 2. Read the source of truth

- For each doc section you plan to write, open the corresponding source file(s) and extract facts:
  - Commands actually in `package.json` scripts / `Makefile` / `justfile`
  - Routes/handlers actually registered, not guessed
  - Env vars actually read (`process.env`, `os.Getenv`, etc.)
  - Dependencies and versions from lockfiles/manifests
- Note any contradictions between existing docs and code — surface them to the user

### 3. Design the doc structure

Choose the minimal set needed; avoid duplicating information:

- **README.md** — what it is, why it matters, quick start, links to deeper docs (keep under ~150 lines; details live in `docs/`)
- **API reference** — endpoints/operations, auth, request/response examples, error codes (derive from OpenAPI/spec or handler code, not memory)
- **Guides / How-tos** — task-oriented ("Deploy to Fly.io", "Add a new skill")
- **Architecture / ADRs** — why the system is shaped this way (link to `docs/architecture.md`)
- **Reference** — configuration, env vars, CLI flags (table format)

Include a table of contents when the doc exceeds ~80 lines.

### 4. Write with accuracy and navigability

- Use **absolute file references** with line numbers where helpful: `` `src/auth/login.ts:42` ``
- Provide **copy-pasteable commands** verified in step 2; never invent flags
- Show **real examples**: actual request/response payloads, not placeholder `foo`/`bar` unless clearly labeled as schematic
- Keep language concise, active, and consistent (present tense for behavior, imperative for instructions)
- Add diagrams (Mermaid) only when they clarify a non-obvious flow

Templates:

**README quick-start**:
```markdown
## Quick Start
\`\`\`bash
git clone <repo>
cd <repo>
npm ci         # verified from package.json:12
npm run dev    # starts http://localhost:3000
\`\`\`
```

**API endpoint**:
```markdown
### POST /api/habits
Auth: Bearer token
Request: { "title": "string", "frequency": "daily|weekly" }
Response 201: { "id": "uuid", "title": "..." }
Errors: 400 validation, 401 unauthorized
```

### 5. Verify and maintain

- Click every link; run every command sequence in a clean checkout when feasible
- Remove or fix stale sections you discovered in step 2
- Leave a maintenance note where docs are likely to drift ("Source: `src/routes.ts:18-45` — update here if routes change")
- If the repo has a docs linter or link checker, run it

## Instructions

- **Never document from memory.** Every command, env var, flag, and endpoint must be traced to a file:line you read.
- **Prefer discovery via tools.** Use glob/grep to inventory files, read to extract facts, bash to verify commands.
- **Minimize duplication.** If `package.json` already declares the dev command, the README should call it out once and point to the file — don't copy-paste a second source of truth.
- **Match the project's voice.** Mirror tone and formatting from existing docs; don't introduce a new style guide mid-repo.
- **Keep diffs focused.** When updating docs, preserve surrounding formatting and TOC; only change what is inaccurate or missing.
- **Flag drift explicitly.** If code and existing docs disagree, say so: "> Note: `README` says `npm start` but `package.json:8` defines `npm run dev` — docs updated to match."

## Constraints

- Do NOT invent APIs, env vars, commands, or file paths not found in the codebase
- Do NOT write documentation before reading relevant source files
- Do NOT duplicate large code blocks into docs when a file reference suffices
- Do NOT use placeholder examples that could be mistaken for real usage without a clear label
- Do NOT over-document: skip internal helpers that are not part of the public surface unless requested

## Examples

### Example 1 — Create a README from scratch

> **User**: "Document this repo — there's no README yet."

**Agent**:
1. Globs `**/*.{json,md,toml,yaml}`, reads `package.json`, `src/index.ts:1-30`, `CONTRIBUTING.md`
2. Drafts `README.md` with: description from `package.json:3`, quick start from `package.json:12-18`, project structure from directory listing
3. Verifies `npm run dev` actually starts the server before committing the example

### Example 2 — Update API docs

> **User**: "Update docs/api.md — we added a new endpoint `POST /teams`."

**Agent**:
1. Reads `src/routes/teams.ts:10-55`, extracts auth, validation, response code
2. Updates `docs/api.md` with the `POST /teams` section using the exact schema from `src/schemas/team.ts:5-20`
3. Runs Markdown link check, confirms no broken anchors

### Example 3 — Fix stale documentation

> **User**: "The README says `yarn start` but we migrated to pnpm."

**Agent**:
1. Reads `README.md:24`, `package.json:10` (`pnpm dev`), `pnpm-lock.yaml` existence
2. Patches `README.md:24` to `pnpm dev`, adds note about `pnpm install` vs `npm ci`
3. Greps for other occurrences of `yarn start` across `docs/` and fixes them in the same pass

## References

- Works alongside `project-architecture` (architecture docs) and `code-review` (flags missing docs)
- For skill docs, see `CONTRIBUTING.md` → "How to Create a New Skill" for `SKILL.md` structure
