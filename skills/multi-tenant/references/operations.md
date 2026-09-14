# Operations

Canonical reference for metering, limits, observability, lifecycle, failures, testing, and rollout. Ship only when every gate passes.

## Billing and usage (tenant-scoped)

Track per event: `tenant_id`, `agent_id`, `user_id`, `session_id`, `run_id`, `provider`, `model`, `input/output_tokens`, `execution_time`, `tool_calls`, `compute_usage`.

Never bill from globally aggregated activity without tenant attribution.

## Rate limiting (layered)

```text
Global → Tenant → User → Agent → Session / Run
```

Example: tenant 100 concurrent runs, user 10, agent 5. Prevents one tenant from starving shared infrastructure.

## Quotas

Enforce before expensive work begins:

```text
max_agents, max_concurrent_runs, max_storage, max_tokens_per_day,
max_cpu, max_memory, max_file_size, max_repository_size, max_execution_time
```

## Observability

Tag every log/trace/metric with tenant identity where appropriate:

```json
{ "tenant_id": "tenant_123", "agent_id": "agent_456", "run_id": "run_789", "event": "tool.execution.started" }
```

Never log secrets. Tenants see only their own telemetry.

## Audit logs (append-only where practical)

Record: login, membership/role changes, agent create/delete, secret create/rotate, tool execution, repo/file access, config and billing changes.

```json
{ "tenant_id": "tenant_123", "actor_id": "user_456", "action": "agent.delete", "resource_id": "agent_789", "timestamp": "..." }
```

## Session lifecycle + failure handling

Lifecycle: `CREATE → AUTHENTICATE → AUTHORIZE → PROVISION → RUN → STREAM → PERSIST → CLEANUP`, with sandbox create/destroy bracketing execution.

Design for: tenant deleted mid-run, permission revoked mid-run, sandbox crash, queue retry, timeout, process restart, partial transaction, expired credential, stream disconnect. Retries preserve tenant context.

## Isolation test matrix (minimum)

```text
A cannot read/update/delete B agent
A cannot read B session, files, memory, cache, events, tools, secrets, billing
Indirect paths: A → session → agent → file → run → memory
```

## Security review checklist

```text
[ ] Auth mandatory, membership validated, context server-derived
[ ] Every tenant resource has ownership; every query enforces tenant scope
[ ] Cache/queue/event/WebSocket/vector/memory/file/secret scopes verified
[ ] Sandboxes isolated; tool execution authorized; git workspaces isolated
[ ] Logs clean of secrets; usage/rate-limit/quota/audit enforced
[ ] Cross-tenant tests exist; retry paths preserve tenant context
```

## Rollout order (add to existing systems incrementally)

```text
1. Tenant + membership model → 2. TenantContext → 3. Authz layer
4. Data ownership → 5. Tenant-aware DB → 6. Cache → 7. Queues/events
8. Files → 9. Memory/vector → 10. Execution → 11. Secrets
12. Quotas/limits → 13. Observability → 14. Security tests → 15. Review
```

## Definition of Done

Multiple tenants share the platform AND execute independently AND data/memory/files/credentials/environments are isolated AND usage is separately measurable AND quotas enforceable AND cross-tenant access is rejected AND automated tests prove it.

Invariant: Tenant A must never observe, modify, execute, retrieve, or infer Tenant B's protected resources unless an explicit shared relationship exists.
