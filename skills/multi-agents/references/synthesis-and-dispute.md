# Multi-Agent Synthesis & Dispute Resolution

Protocols for reconciling contradictory sub-agent findings, managing review disputes, and making sound architectural decisions.

---

## 1. Synthesis Methodology

The orchestrating agent is an **active evaluator and integrator**, not a passive copy-paster.

1. **Extraction**: Parse key claims from each agent's structured response.
2. **Empirical Cross-Checking**: Never accept a sub-agent's line citation without verifying that the file and lines actually exist on disk and perform the stated function.
3. **Harmonization**: Combine non-overlapping insights (e.g., Codebase Researcher's file list + Root-Cause Analyst's offending line).
4. **Resolution**: Detect contradictions and resolve using the Dispute Protocol below.

---

## 2. Conflict Matrix & Resolution

| Conflict Type | Scenario | Resolution Protocol |
|---|---|---|
| **Competing Root Causes** | Agent A blames `auth.ts:42` (cache expiry), Agent B blames `session.ts:88` (token hashing) | **Empirical test**: Orchestrator writes or runs a minimal reproduction script. The hypothesis that reproduces the failure under the exact user condition is accepted. |
| **Architectural Disagreements** | Agent A proposes a new abstraction layer; Agent B proposes modifying existing classes | **Occam's Razor & Project Idiom**: Check existing project precedents (from Codebase Researcher). Prefer the minimal diff that aligns with existing code unless requirements explicitly demand a refactor. |
| **Scope Creep vs. Minimalism** | One agent recommends refactoring adjacent legacy utilities while fixing a bug | **Scope Discipline**: Enforce strict isolation. The primary diff must only touch what is necessary. Record cleanup suggestions under "Unfinished / Follow-up" in the final report. |
| **Critic vs. Implementer Deadlock** | Critic rejects the diff citing security/perf, Implementer argues it is negligible | **Maintainer Bar**: The Critic's concern must be addressed unless proven false by an automated test or explicit project convention. |

---

## 3. The Three-Round Iteration Cap

When the Critic / Maintainer Reviewer requests changes on an implementation:

```
Cycle 1: Implement ─────────> Critic Review (Requests Changes)
                                    │
                                    ▼
Cycle 2: Address Feedback ──> Critic Review (Requests Changes)
                                    │
                                    ▼
Cycle 3: Final Re-alignment ─> Critic Review
                                    │
                  ┌─────────────────┴─────────────────┐
                  ▼                                   ▼
             [APPROVED]                          [ESCALATE]
         Proceed to merge/push             Stop. Bring structured
                                           options to the user.
```

- If after 3 rounds the diff does not satisfy the Critic, **STOP**.
- Do not loop infinitely. Infinite loops waste tokens and introduce code churn.
- Escalate to the user using the template below.

---

## 4. Structured Escalation Template

When sub-agents disagree on fundamental architecture or the Critic rejects after 3 cycles, present a concise decision matrix to the user:

```text
### Decision Checkpoint: Architectural Alignment Needed

During multi-agent review, a fundamental trade-off was identified:

- Option A: <Summary of approach, e.g. In-memory session invalidation>
  - Pros: Minimal diff, zero external dependencies, immediate fix.
  - Cons: Does not persist across cluster worker restarts.

- Option B: <Summary of approach, e.g. Shared Redis blacklist>
  - Pros: Fully distributed, survives server reboots.
  - Cons: Requires Redis dependency and configuration updates.

Recommendation: We recommend Option A to keep the PR focused, with Option B tracked as a follow-up feature.

Which approach do you prefer?
```
