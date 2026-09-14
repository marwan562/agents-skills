# Execution Isolation

Canonical reference for sandboxing agent execution and scoping runtime integrations. Agent isolation continues where database isolation stops.

## Sandbox hierarchy

```text
Tenant → Agent → Execution Sandbox → Container / VM / MicroVM
```

A working directory is NOT a security boundary. Control per sandbox: filesystem, CPU, memory, processes, network, env vars, credentials, runtime lifetime.

Lifecycle: `CREATE → AUTHENTICATE → AUTHORIZE → PROVISION → RUN → STREAM → PERSIST → CLEANUP`. Never leave abandoned environments running.

## Secrets

- Scope per tenant, inject per run only what is needed. Prefer short-lived credentials.
- Bad: global env with `ALL_TENANT_API_KEYS`. Good: `Tenant A → { OPENAI_KEY, GITHUB_TOKEN, STRIPE_KEY }` injected per execution.
- Never write secret values into logs, prompts, traces, DB records, error messages, or analytics.

## Files

Tenant-aware roots only:

```text
storage/tenants/{tenantId}/agents/{agentId}/
object key: tenant/{tenantId}/agent/{agentId}/file/{fileId}
```

Validate path joins inside the tenant root. Block `../`, absolute paths, symlink escapes, cross-tenant references.

## Git workspaces

```text
Tenant A → Workspace A → repo A (writable only here)
Tenant B → Workspace B → repo B
```

Prefer one sandbox, one workspace, one tenant context per execution. Never share writable directories across tenants unless explicitly designed.

## MCP / Tools / Plugins

Treat every tool as a privileged capability. Gate before execution:

```text
Who? → Tenant? → Agent? → Permissions? → Tool? → Resource?
```

Tools run with tenant context and tenant credentials — e.g. `github.createIssue(...)` uses the calling tenant's token, never a global one.

## WebSockets and streaming

Tokens, tool calls, logs, terminal output — every socket binds `user + tenant + session`. On subscribe to `session_123`, verify `session_123 belongs to current tenant`. Never use session ID as the sole secret.

## Runtime models

- Shared runtime: cheaper, requires stronger in-runtime isolation.
- Dedicated runtime: stronger isolation, higher cost.
- Hybrid (recommended): shared for standard tenants, dedicated for enterprise.
