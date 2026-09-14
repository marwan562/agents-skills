---
name: multi-tenant
description: Use this skill when designing or reviewing secure multi-tenant AI agent platforms — tenant isolation for data, execution, memory, and billing. Triggers on multi-tenant, tenant isolation, RLS, SaaS, sandbox.
---

# Multi-Tenant

> Shared infrastructure, strict tenant isolation — no accidental cross-tenant access.

Designs and reviews secure, production-grade multi-tenant systems for AI agent platforms where tenants share infrastructure but never share data, memory, files, credentials, or execution.

## Purpose

Translate multi-tenant requirements into an end-to-end isolation design: trusted tenant context, enforced authorization, isolated data, sandboxed execution, namespaced stateful services, and per-tenant metering. Prevents the most common SaaS failure — filtering in one layer while leaking through cache, memory, jobs, logs, or sandboxes.

## When to Use

- User asks to design, add, audit, or fix multi-tenancy in a SaaS / agent platform
- User mentions tenants, workspaces, organizations, isolation, data leakage, or cross-tenant access
- User needs tenant-aware auth, Row-Level Security, per-tenant sandboxes, memory, cache, queues, files, secrets, or billing
- User asks "how do we isolate tenants?", "is this tenant-safe?", "review for tenant leaks?"
- Keywords: `multi-tenant`, `tenant isolation`, `tenant_id`, `RLS`, `sandbox`, `SaaS`, `workspace isolation`, `cross-tenant`

Do NOT trigger for single-user CLI tools, single-tenant prototypes with no shared infrastructure, or generic auth without a tenant boundary.

## Workflow

```
[1. Model Context] ──> [2. Enforce Data] ──> [3. Isolate Execution] ──> [4. Namespace State] ──> [5. Meter & Observe] ──> [6. Verify & Ship]
```

### 1. Model identity and establish TenantContext

- Map the ownership hierarchy: `Tenant → Users → Agents → Sessions → Runs → Tools / Files / Memory`.
- Define one canonical `TenantContext` (`tenantId`, `userId`, `role`) resolved server-side from authentication + membership. Never trust a client-supplied `tenant_id` alone.
- List every tenant-owned resource (`agents`, `sessions`, `runs`, `messages`, `memories`, `files`, `credentials`, `usage`, `billing`). Default: every resource gets explicit `tenant_id` — see [data-isolation](references/data-isolation.md).
- If ambiguous, ask at most 2-3 questions (isolation model, enterprise dedicated-tenants?, compliance needs) — then propose and proceed.

### 2. Enforce authorization at the data boundary

- Apply the golden rule on every access: `RESOURCE_ID + TENANT_ID`, never ID alone. Prefer `WHERE id = ? AND tenant_id = ?` over load-then-check.
- Choose a DB strategy deliberately — shared tables (default), separate schemas, or separate databases — per the decision table in [data-isolation](references/data-isolation.md). Add RLS as a second line of defense for sensitive tables.
- Derive tenant from session in list APIs (`GET /agents`, not `GET /tenants/:id/agents/:id` unless hierarchy is public). If a tenant ID appears in the URL, verify membership.
- Default to deny: `authenticated → membership → ownership → role → policy → allow`.

### 3. Isolate agent execution and integrations

- Give each execution its own sandbox (`Tenant → Agent → Sandbox → Container / MicroVM`). Scope filesystem, CPU, memory, network, env vars, lifetime — see [execution-isolation](references/execution-isolation.md).
- Inject only the secrets required for that run; prefer short-lived credentials. Never log, prompt, or trace secret values.
- Scope files (`tenant/{tenantId}/agent/{agentId}/...`), git workspaces (one sandbox, one workspace, one tenant), MCP tools (tenant credentials, per-tool allowlist), and WebSocket subscriptions (verify `session belongs to current tenant` before subscribing).

### 4. Namespace all stateful services

- Apply the pattern `tenant:{tenantId}:<resource>:<id>` to cache keys, memory namespaces (`memory/{tenant}/{agent}/...`), vector filters (`filter = { tenant_id }`), queue payloads, and events — see [stateful-services](references/stateful-services.md).
- Propagate `tenantId` through every background job and retry; workers must re-validate ownership, never blindly trust the payload.
- Treat cache, vector recall, and event streams as leak vectors equal to the database.

### 5. Meter, throttle, and observe per tenant

- Emit usage per `tenant → agent → run` (tokens, tool calls, compute, storage). Enforce quotas (`max_agents`, `max_concurrent_runs`, `max_tokens_per_day`) before expensive work starts.
- Rate-limit at `global → tenant → user → agent → session` levels so one tenant cannot starve others.
- Tag every log, metric, and trace with `tenant_id`; keep audit logs append-only for auth, membership, secret, and billing changes — see [operations](references/operations.md).

### 6. Verify isolation before shipping

- Run the cross-tenant negative matrix in [operations](references/operations.md): A cannot read/update/delete B's agents, sessions, files, memory, cache, events, tools, secrets, or billing — including indirect paths (`session → agent → file → run → memory`).
- Confirm failure paths preserve tenant context (retry, sandbox crash, permission revoked mid-run, tenant deleted mid-run).
- Close with the Definition of Done: independent execution + isolated data/memory/files/credentials/environments + separately measurable usage + enforceable quotas + rejected cross-tenant access + passing tests.

## Instructions

- **Be explicit.** Prefer explicit `tenant_id` ownership, explicit context propagation, and explicit authorization over implicit resolution or global state.
- **Enforce at the boundary.** Push checks to the data-access layer (`WHERE id + tenant_id`), the cache-key builder, the job envelope, and the sandbox launcher — not scattered business logic.
- **Start simple, isolate strongly.** Prefer shared tables + strict filtering + RLS for early SaaS; move to schemas or dedicated runtimes only on concrete enterprise, regulatory, or noisy-neighbor evidence.
- **Keep control plane separate from agent runtime.** Control plane owns tenant, user, agent, session, permissions, quotas, billing. Agent runtime owns reasoning, tools, execution. Do not scatter tenant checks inside the agent loop.
- **Prove it with negative tests.** Every isolation claim needs a Tenant-A-vs-Tenant-B rejection test; unverified isolation is a vulnerability.

## Constraints

- Do NOT trust client-provided `tenant_id`, bare resource IDs, or session IDs as authorization.
- Do NOT write unscoped queries, global cache keys, global memory namespaces, global credentials, or unscoped background jobs.
- Do NOT interpolate tenant values into SQL, shell, or paths — use parameterized queries and validated path joins inside the tenant root.
- Do NOT log, trace, or return secrets, and do NOT expose another tenant's telemetry, billing, or error details.
- Do NOT weaken isolation to simplify implementation, and do NOT ship without cross-tenant negative tests and a security-checklist pass.
- Do NOT embed secrets, real connection strings, or tenant PII in designs or examples.

## Examples

### Example 1 — Add tenancy to an agent API

> **User**: "Make `src/agents/` multi-tenant."

**Agent actions**:

1. Reads `src/agents/*`, `src/db/schema.*`, auth middleware; lists tenant-owned tables missing `tenant_id`.
2. Introduces `TenantContext { tenantId, userId, role }` in middleware; rewrites reads to `WHERE id = $1 AND tenant_id = $2`.
3. Namespaces cache (`tenant:{id}:agent:{id}`), queues (`{ tenantId, agentId, sessionId }`), and vector filters.
4. Adds negative tests: `Tenant A token → GET /agents/<B-id> → 403/empty`; verifies with test run.

### Example 2 — Audit for tenant leaks

> **User**: "Is `internal/memory/` tenant-safe?"

**Agent actions**:

1. Traces `similaritySearch(query)` — flags missing `filter = { tenant_id }` at `internal/memory/store.ts:42`.
2. Checks cache keys (`agent:123` → leak; fix to `tenant:456:agent:123`), logs (missing `tenant_id`), and job payloads.
3. Verdict: `Request changes` — 1 blocking (unfiltered vector recall), 2 important (global cache key, unscoped retry job).

### Example 3 — Isolate execution

> **User**: "Agents run shell + git — isolate tenants."

**Agent actions**:

1. Proposes `Tenant → Agent → Sandbox → Container` with per-run workspace `tenants/{tenantId}/agents/{agentId}/`.
2. Scopes secrets per run, blocks `../` traversal, separates git workspaces, allowlists MCP tools per tenant.
3. Adds lifecycle: provision → run → stream → persist → destroy; no abandoned sandboxes.

## References

- [references/data-isolation.md](references/data-isolation.md) — Ownership model, DB strategies A/B/C, RLS, query patterns.
- [references/execution-isolation.md](references/execution-isolation.md) — Sandboxes, secrets, files, git, MCP tools, WebSockets.
- [references/stateful-services.md](references/stateful-services.md) — Memory/vector, cache, queues, events.
- [references/operations.md](references/operations.md) — Billing, rate limits, quotas, observability, audit, lifecycle, failures, testing matrix, security checklist, rollout order, Definition of Done.
- Companion skills: `project-architecture` (module boundaries), `code-review` (diff audit), `documentation` (ADRs, runbooks).
