# Stateful Services

Canonical reference for memory, cache, queues, and events. Most cross-tenant leaks happen here, not in the primary database.

## Agent memory (tenant-scoped)

Never use a global namespace (`memory/*`). Prefer:

```text
memory/{tenant_id}/{agent_id}/...
```

Vector stores MUST carry and filter on tenant metadata:

```json
{ "tenant_id": "tenant_123", "agent_id": "agent_456" }
```

Bad: `similaritySearch(query)`. Good: `similaritySearch(query, filter = { tenant_id: currentTenant })`.

## Caching

Every cache key for tenant data encodes the tenant:

Bad: `agent:123`. Good: `tenant:456:agent:123`.

```text
tenant:{tenantId}:session:{sessionId}
tenant:{tenantId}:memory:{memoryId}
tenant:{tenantId}:usage:{date}
```

## Queues and background jobs

Jobs carry full context; workers re-validate ownership:

Bad: `{ "agentId": "agent_123" }`.
Good: `{ "tenantId": "tenant_456", "agentId": "agent_123", "sessionId": "session_789" }`.

Every retry preserves and re-validates tenant context. A retry must never execute under the wrong tenant.

## Events

Include tenant context on every event:

```json
{
  "event": "agent.run.completed",
  "tenantId": "tenant_123",
  "agentId": "agent_456",
  "runId": "run_789"
}
```

Never publish tenant-sensitive events to an uncontrolled global stream without filtering and authorization.
