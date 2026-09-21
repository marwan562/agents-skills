# Jev Calibrated Gates (optional, steps 4 / 7 / 10)

Use this when you want calibrated quality scores instead of a chatty
"looks good". Jev never writes the fix. A generator still writes it,
tests still prove it. Jev only scores the supplied state; ordinary code
(you, the agent) enforces the thresholds below.

If no Jev key or MCP server is available, skip this file entirely and run
steps 4, 7, 10 as written in `SKILL.md`. Nothing here is blocking without a key.

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

MCP Configuration (e.g. `opencode.json` or Antigravity MCP settings):

```json
{
  "mcp": {
    "servers": {
      "jev": {
        "type": "local",
        "command": ["node", "/path/to/jev/dist/server.js"],
        "environment": {
          "JEV_API_KEY": "{env:JEV_API_KEY}"
        }
      }
    }
  }
}
```

Verify with MCP tool list: the `jev` server provides `jev_check`, `jev_score`,
`jev_ask`, `jev_triage`, `jev_classify`, and `jev_models`.

## 2. Real Tool Contracts (`jev` MCP server)

Jev provides calibrated probability and scoring tools rather than free-form chat:

- **`jev_check`**: Evaluates a binary proposition (0.0 to 1.0 probability) with
  explicit verdict (`yes`, `no`, or `uncertain`).
- **`jev_score`**: Rates state along an ordered scale of defined levels, returning
  probability-weighted score, confidence, and recommended action (`act`, `review`, `abstain`).
- **`jev_ask`**: Evaluates multiple typed questions (`check`, `score`, `classify`) in
  a single forward pass over the same state for maximum speed.

Never send credentials, `.env` content, secrets, or huge vendored files. Keep the state focused.

## 3. Gate A: Step 4 Duplicate and Prior-Art Check (`jev_check`)

State: Issue title + body + candidate PR summary and maintainer review comments.

Call `jev_check`:

```json
{
  "question": "Does this candidate pull request or prior attempt completely resolve the open issue?",
  "state": "Issue: <summary>\nCandidate PR: <url, status, review summary, rejection reason if any>",
  "yes_means": "The issue is already resolved by this candidate PR or merge request",
  "no_means": "The issue remains open, unaddressed, or the candidate PR was rejected/stalled",
  "yes_at_or_above": 0.7,
  "no_at_or_below": 0.3
}
```

Enforce the branches in `SKILL.md` step 4:
- `verdict == "yes"`: Stop, tell the user with link, do not open competing PR.
- `verdict == "no"`: Proceed with fresh implementation.
- `verdict == "uncertain"`: Do the rendered browser read yourself to disambiguate.

## 4. Gate B: Step 7 Analysis Readiness (`jev_score`)

State: Browser intake artifact + Root-Cause Analyst reproduction steps + affected file paths.

Call `jev_score`:

```json
{
  "question": "How thoroughly has the root cause been isolated with reproducible evidence down to exact code locations?",
  "state": "Intake Artifact:\n<intake artifact>\n\nRoot Cause Analysis:\n<analyst output>\n\nTarget Files:\n<candidate files>",
  "levels": [
    "Vague guess or symptom description without exact code location or reproduction",
    "Plausible subsystem identified but specific offending lines remain unverified",
    "Exact file, line range, failure mechanics, and minimal reproduction test case isolated"
  ],
  "act_above": 0.8,
  "review_above": 0.5
}
```

Enforce:
- Proceed to Step 8 (Implement) only when `action == "act"` (or score >= 2.0 with high confidence).
- If `action == "review"` or `"abstain"`: Loop the Analyst and Researcher roles once more to pin down the reproduction test before touching application code. If still uncertain, escalate to the user.

## 5. Gate C: Step 10 Merge Gate (`jev_ask`)

Runs on the diff and test verification output before the Senior Maintainer review loop.
Use `jev_ask` to batch all verification questions in one single forward pass:

```json
{
  "state": "Issue Context:\n<issue scope>\n\nProposed Diff:\n<git diff>\n\nTest Verification:\n<command run + pass output>",
  "questions": [
    {
      "id": "correctness_check",
      "type": "check",
      "question": "Does the diff completely resolve the issue without introducing regressions?",
      "yes_means": "The diff fixes the defect and tests confirm behavior",
      "no_means": "The fix is incomplete, breaks existing invariants, or lacks test coverage"
    },
    {
      "id": "readiness_score",
      "type": "score",
      "question": "How ready is this diff for senior maintainer review without requiring revision?",
      "levels": [
        "Unready: failing tests, extraneous diff hunks, or unhandled edge cases",
        "Functional but rough: needs test expansion or style/convention cleanup",
        "Merge ready: minimal diff, accompanies test, passes all suites, matches repo conventions"
      ]
    }
  ],
  "act_above": 0.8
}
```

Enforce:
- `correctness_check` verdict is `yes` AND `readiness_score` is high: Hand to Senior Maintainer Reviewer role in Step 10.
- `correctness_check` verdict is `no`: Fix the concrete failure, re-run tests locally, re-check.
- Low confidence or failure after three loops: Stop and bring the disagreement to the user. Never push unverified code.

## 6. Learning Loop

Jev model weights do not update from your runs. What improves is your gate:
thresholds, question wording, and which cases you advance automatically.
Log every gate call to an untracked local file outside the repository:

```bash
# append-only, one JSON object per line, never committed:
~/.cache/contribute/jev-decisions.jsonl
# fields: date, repo, issue, gate, question, verdict, confidence,
#         action_taken, outcome (merged / rejected / CI status)
```

Periodically review the log. If reverts cluster under confidence < 0.75, raise the `act_above` threshold to 0.80. That history is the learning.
