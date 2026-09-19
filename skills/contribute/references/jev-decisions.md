# Jev Review Gates (optional, steps 4 / 7 / 10)

Use this when you want calibrated quality scores instead of a chatty
"looks good". Jev never writes the fix. A generator still writes it,
tests still prove it. Jev only scores the supplied state; ordinary code
(you, the agent) enforces the thresholds below.

If no Jev key is available, skip this file entirely and run steps 4, 7, 10
as written in `SKILL.md`. Nothing here is blocking without a key.

## 1. Setup (once per machine, never in the repo)

Keys live in the environment only. Never paste one into a skill file, a log,
a commit, or a PR body.

```bash
export JEV_API_KEY="your-key"  # from the TypeSafe console
```

macOS GUI apps may not inherit shell exports. Make the key visible before
starting the agent:

```bash
launchctl setenv JEV_API_KEY "$JEV_API_KEY"
test -n "$(launchctl getenv JEV_API_KEY)" && echo "JEV_API_KEY is configured"
```

OpenCode MCP (`~/.config/opencode/opencode.json`):

```json
{
  "mcp": {
    "servers": {
      "jev-review": {
        "type": "local",
        "command": ["node", "/absolute/path/to/jev-review/dist/server.js"],
        "environment": {
          "JEV_API_KEY": "{env:JEV_API_KEY}"
        }
      }
    }
  }
}
```

If the MCP host does not inherit the parent env, front it with a wrapper
that pulls from `launchctl` at spawn time and point `command` at the wrapper
instead. Verify with `opencode mcp list` — `jev-review` must show connected.

## 2. Call shape (`jev_review` MCP tool)

```json
{
  "task": "Issue scope + acceptance criteria, one paragraph",
  "diff": "Focused git diff for this step",
  "files": [
    { "path": "src/example.ts", "content": "Only surrounding code needed to judge the change" }
  ],
  "repositoryContext": "Conventions, invariants, exact test commands + results",
  "previousEvaluation": {}
}
```

Send `task` + current `diff` on most calls. Add `files` only when surrounding
behavior is needed. Put test outcomes in `repositoryContext`. On a follow-up
call, pass the prior response unchanged as `previousEvaluation` and send the
current implementation — never the stale pre-fix diff. Keep task scope stable
so deltas stay comparable.

Never send secrets, credentials, `.env` content, vendored code, or unrelated
repository content. If Jev reports its input limit was exceeded, shrink the
context or split into coherent review slices.

## 3. Gate A - step 4, duplicate / prior-art check

State: issue title + body + candidate PR summary + rejection reason if any.
`repositoryContext`: what the browser intake proved (linked-PR sidebar,
review history, visuals).

Ask Jev to score `correctness` and `reliability` of the "adopt vs. proceed"
read. Enforce step 4's existing branches regardless: `proceed` continues,
`adopt` reviews the existing PR instead, `stop` reports resolved. On low
confidence, do the browser re-read yourself instead of trusting the gate.

## 4. Gate B - step 7, analysis readiness

State: intake artifact + root-cause draft + files the fix will touch.

Enforce: implement (step 8) only when `correctness >= 7` with confidence
`>= 0.6` and no high-severity correctness issue pointing at a vague root
cause. Otherwise loop the Analyst/Researcher roles once more, then escalate
to the user rather than coding on a guess.

## 5. Gate C - step 10, merge gate (runs before the reviewer loop)

State: issue scope + full `git diff` + exact test/lint commands and results.

Enforce (thresholds you may tighten per repo, never loosen silently):

- Targeted weak metrics (correctness, reliability, security, tests) improved
  or held, with no new high-severity issue and no regression on another
  important dimension: hand to the Senior Maintainer Reviewer role.
- Gate says revise (concrete defect with location): fix exactly that,
  re-run tests, re-ask once with `previousEvaluation`.
- Low confidence (`< 0.6`) or still failing after the step-10 three-round
  loop: stop and bring it to the user. Never push to "fix later".

The reviewer role and the three-round cap still apply on every path. Scores
are evidence, not objectives: never chase a score with speculative
architecture, needless abstraction, meaningless tests, or scope expansion.

## 6. Learning loop (how "he learns")

Jev's weights do not update from your runs. What improves is your gate:
thresholds, task wording, and which cases you auto-advance. Log every gate
to an untracked file outside the repo and review it:

```bash
# append-only, one JSON object per line, never committed:
~/.cache/contribute/jev-decisions.jsonl
# fields: date, repo, issue, gate, task, scores, confidence,
#         action_taken, outcome (merged / reverted / CI red)
```

Monthly, or after any revert: re-read the low-confidence and wrong calls,
then change one thing — a threshold value or one task sentence — and note it
in the log. That history is the learning. If reverts cluster under
confidence `< 0.75`, raise the bar to `0.75`.
