# Multi-Agent Failure Recovery & Virtual Role Fallback

Protocols for handling sub-agent failures, runtime limitations, and single-agent virtual role execution.

---

## 1. Sub-Agent Failure Modes & Remediation

| Failure Mode | Symptom | Recovery Action |
|---|---|---|
| **Sub-agent Timeout / Crash** | Tool execution exceeds timeout or returns an execution error | 1. Retry once with a simplified, narrower scope.<br>2. If retry fails, absorb the role into the orchestrator and complete the investigation directly. |
| **Hallucinated Files / APIs** | Agent references non-existent file paths, functions, or dependencies | 1. Orchestrator runs a quick file existence check (`view_file` or `ls`).<br>2. Invalidate hallucinated claims immediately.<br>3. Reground the brief with verified file listings. |
| **Circular Review Loop** | Implementer and Critic repeat the same arguments across multiple turns | Enforce the 3-cycle hard limit from `synthesis-and-dispute.md`. Halt iteration and escalate the trade-off to the user. |
| **Empty / Vacuous Output** | Sub-agent returns generic boilerplate without concrete code or file pointers | Reject output. Re-issue brief with explicit requirement: "Must cite specific file:line numbers and provide reproduction evidence." |

---

## 2. Virtual Role Sequencing (Solo Fallback Mode)

When running in an environment that lacks a sub-agent spawning tool (or when tool execution is disabled), **do not abandon multi-agent rigor**. Instead, execute the workflow using **Sequential Virtual Roles**:

The orchestrator explicitly wears each role hat in sequence, maintaining strict intellectual separation between phases.

### Step 1: Root-Cause Analyst Hat
- Focus entirely on understanding the problem.
- Read files, run reproduction tests, trace lines.
- **Mental Rule**: Do NOT write the fix or plan architecture yet. Produce only the root-cause diagnosis.

### Step 2: Codebase & Convention Researcher Hat
- Search the codebase for prior art, related utilities, and conventions.
- Check test fixtures and style configs.
- **Mental Rule**: Discover patterns without modifying code.

### Step 3: Implementation Specialist Hat
- Implement the minimal surgical diff addressing the root cause.
- Follow the patterns discovered by Hat 2.
- Run local tests to verify basic functionality.

### Step 4: Devil's Advocate / Maintainer Critic Hat (Crucial)
- **Hold this hat back until the diff is written.**
- Step back and review your own diff as if an unfamiliar external contributor submitted it.
- Ask:
  - *What breaks if inputs are null, empty, or concurrent?*
  - *Does this introduce a performance regression or security loophole?*
  - *Does it violate any project conventions?*
- Address all findings before presenting the final result to the user.
