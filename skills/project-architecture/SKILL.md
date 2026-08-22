---
name: project-architecture
description: Use this skill when designing a clean project architecture from requirements — analyzing needs, proposing folder/module structure, responsibilities, dependencies, and key architecture decisions. Triggers on requests to design, structure, scaffold, or evaluate architecture for a new or existing project.
---

# Project Architecture

Helps an AI agent design a clean, scalable, and maintainable project architecture from natural-language requirements.

## Purpose

Translate ambiguous requirements into a concrete architecture: folder layout, module boundaries, responsibilities, dependencies, data flows, and documented trade-offs. Prevents over-engineering while ensuring the design can scale.

## When to Use

- User asks to design, scaffold, or structure a new project, service, or feature
- User wants an architecture review or refactoring plan for an existing codebase
- User describes requirements and asks "how should I organize this?"
- User needs ADRs (Architecture Decision Records) or a technical design document
- Keywords: `architecture`, `project structure`, `scaffold`, `design system`, `module layout`, `tech stack`

## Workflow

### 1. Clarify requirements

- Extract explicit requirements from the user prompt
- List implied requirements (auth, persistence, scaling, observability) and confirm which are in scope
- Identify constraints: team size, timeline, deployment target, existing tech, compliance
- If ambiguous, ask at most 2-3 focused questions — then propose and proceed

### 2. Analyze domain and boundaries

- Identify core domain entities and bounded contexts
- Distinguish core complexity (domain logic) from supporting concerns (auth, logging, email, payments)
- Map actors (users, services, external APIs) and their interactions

### 3. Choose an architectural style

Select the simplest style that fits:

- **Monolith** (modular) — small team, early stage, few bounded contexts
- **Modular monolith** — medium complexity, want clear boundaries without distributed overhead
- **Microservices / service-oriented** — independently deployable, distinct scaling/ownership needs
- **Event-driven / hexagonal / clean** — when portability, testability, or async flows are primary

Justify the choice in one paragraph: why this, not the alternatives.

### 4. Define modules, responsibilities, and dependencies

For each module/service, specify:

- **Responsibility**: single, crisp sentence
- **Owns**: data, domain entities, or external integration it exclusively controls
- **Depends on**: explicit dependencies (direction matters — enforce acyclic graph)
- **Exposes**: public interface (REST, gRPC, events, library API)

Visualize with a simple dependency diagram (Mermaid `graph TD` or ASCII).

### 5. Propose folder and file structure

- Provide a tree covering the top 2-3 levels (don't list every file)
- Align folders to modules from step 4; avoid `utils`/`helpers` catch-alls without scope
- Show where cross-cutting concerns live (`config/`, `middleware/`, `observability/`)
- Note build/test/config files at the root

Example:

```
my-app/
├── cmd/server/        # entrypoint
├── internal/
│   ├── auth/          # auth domain
│   ├── billing/
│   └── platform/db/
├── api/openapi.yaml
├── web/
└── deploy/
```

### 6. Specify data and integration design

- Data model: key tables/collections and relationships (high-level, not full DDL)
- State and consistency: transactional vs. eventual, where and why
- External integrations: third-party APIs, queues, storage — with failure modes
- Configuration and secrets: env/secret management approach

### 7. Document decisions and trade-offs (ADRs)

- For each significant decision, write a mini-ADR: **Context → Decision → Consequences → Alternatives considered**
- Call out risks and deferred decisions explicitly ("Defer sharding until >10M rows; current vertical scale suffices")
- Note what is intentionally *not* built (YAGNI)

## Instructions

- **Start simple, evolve deliberately.** Prefer modular monolith over microservices unless requirements demand distribution.
- **Enforce boundaries.** Each module owns its data; cross-module access goes through the public interface, not shared tables.
- **Keep dependencies acyclic.** If a cycle appears, introduce an abstraction or event.
- **Separate domain from infrastructure.** Business logic should not import web frameworks or DB drivers directly (use ports/interfaces).
- **Minimize abstractions.** Create an interface only when there are ≥2 implementations or a test seam is needed.
- **Validate against requirements.** Before finalizing, walk through each requirement and show which module satisfies it.

## Constraints

- Do NOT over-engineer: no extra services, queues, or caches without a stated need
- Do NOT propose a folder structure without first clarifying domain boundaries
- Do NOT produce a vague "scalable architecture" without concrete module responsibilities
- Do NOT ignore constraints the user stated (team size, existing stack, deployment target)
- Do NOT embed secrets or environment-specific values in the architecture doc

## Examples

### Example 1 — New SaaS project

> **User**: "Design the architecture for a habit-tracker SaaS with teams, reminders, and a mobile app."

**Agent actions**:
1. Clarifies: auth scope (email+OAuth?), reminder delivery (push/email?), team size
2. Chooses modular monolith (small team, single deploy unit, clear domains)
3. Defines modules: `auth`, `habits`, `teams`, `notifications`, `platform`
4. Proposes folder tree under `internal/` + `api/` + `mobile/`
5. Notes ADRs: "Postgres over Mongo for relational habits→teams", "Defer event bus; direct calls suffice at current scale"

### Example 2 — Review existing project

> **User**: "Review the architecture in this repo — is `src/utils` getting out of hand?"

**Agent actions**:
1. Scans `src/` tree, counts files per folder, identifies `utils` as grab-bag (auth helpers, date helpers, API clients)
2. Proposes split: `auth/tokens.ts`, `time/format.ts`, `api/client.ts`; deletes empty `utils/`
3. Maps dependencies, flags a cycle `users ↔ teams`, suggests `membership` module as intermediary

### Example 3 — ADR for a single decision

> **User**: "Should we use WebSockets or SSE for live updates?"

**Agent delivers**:

```
ADR-003: Live updates via SSE
Context: Dashboard needs 1-way server→client updates, ~5 events/min, corporate proxies
Decision: SSE over WebSockets (simpler, auto-reconnect, works over HTTP/2)
Consequences: No client→server push over same channel (use REST); need EventSource polyfill for older clients
Alternatives: WebSockets (overkill for unidirectional), polling (higher latency)
```

## References

- Related skills: `documentation` (to capture ADRs), `code-review` (to evaluate against architecture)
- Template for ADR: keep each ADR ≤ 10 lines in the design doc
