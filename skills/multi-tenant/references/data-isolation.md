# Data Isolation

Canonical reference for tenant ownership, database strategies, and query enforcement. Read this before touching any tenant-owned table.

## Ownership model

Every tenant-owned resource MUST have an unambiguous tenant boundary — directly via `tenant_id`, or via an enforced relationship.

Tenant-owned (default): `users/memberships`, `organizations`, `agents`, `sessions`, `runs`, `messages`, `memories`, `files`, `projects`, `tools`, `credentials`, `api_keys`, `usage`, `billing`.

Prefer explicit `tenant_id` even when derivable (e.g. `sessions` has both `agent_id` and `tenant_id`) — safer authz, indexing, auditing, query planning.

```sql
agents   (id, tenant_id, name, created_at)
sessions (id, tenant_id, agent_id, created_at)
```

## Strategy decision table

| Model | Shape | Use when | Cost |
|---|---|---|---|
| A — Shared DB, shared tables (default) | rows carry `tenant_id` | early SaaS, low ops overhead | low |
| B — Separate schemas | `tenant_a.*`, `tenant_b.*` | stronger logical separation | medium |
| C — Separate databases | `DB_A`, `DB_B` | enterprise / regulatory / dedicated | high |

Do not adopt B/C without a concrete requirement. Hybrid is common: shared for standard tenants, dedicated runtime/DB for enterprise.

## Query rules

All tenant-scoped access follows `RESOURCE_ID + TENANT_ID`:

```sql
-- read
SELECT * FROM sessions WHERE id = $1 AND tenant_id = $2;
-- list
SELECT * FROM agents WHERE tenant_id = $1 ORDER BY created_at DESC;
-- update
UPDATE agents SET name = $1 WHERE id = $2 AND tenant_id = $3;
-- delete
DELETE FROM agents WHERE id = $1 AND tenant_id = $2;
```

Never `findAgent(id)` then authorize afterward. Enforce as close to the data layer as practical.

## Row-Level Security (Postgres)

Use RLS as a second line of defense, not a replacement for app authz:

- Enable RLS on tenant tables; policy `USING (tenant_id = current_setting('app.tenant_id')::text)`.
- Set `app.tenant_id` per transaction from trusted `TenantContext`.
- Audit bypass roles; `FORCE ROW LEVEL SECURITY` where appropriate; test that service/migration roles cannot leak.

## TenantContext

```ts
type TenantContext = {
  tenantId: string
  userId: string
  role: string
}
```

Resolution order: `Request → Authentication → User Identity → Tenant Membership → TenantContext → Authorization → Business Logic`. If the API receives a tenant identifier, verify the principal belongs to it. Default = DENY.

## API design

Prefer deriving tenant from auth context:

```http
GET /agents
POST /agents
GET /agents/:id
POST /agents/:id/runs
```

Avoid `GET /tenants/:tenantId/agents/:agentId` unless hierarchy is public. If `tenantId` is in the URL, authorize it.
