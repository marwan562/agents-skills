# Jev Decision Gates (optional, steps 4 / 7 / 10)

Use this when you want calibrated yes/no + confidence numbers instead of a
chatty "looks good". Jev never writes the fix. A generator still writes it,
tests still prove it. Jev only answers typed questions; ordinary code (you,
the agent) enforces the thresholds below.

If no Jev key is available, skip this file entirely and run steps 4, 7, 10
as written in `SKILL.md`. Nothing here is blocking without a key.

## 1. Setup (once per machine, never in the repo)

Keys live in the environment only. Never paste one into a skill file, a log,
a commit, or a PR body.

```bash
export TYPESAFE_API_KEY="<from console.typesafe.ai>"
# optional fallback, paid credits required for Jev on OpenRouter:
export OPENROUTER_API_KEY="<from openrouter.ai/keys>"
```

Provider priority:

1. **TypeSafe direct (preferred):** `POST https://api.typesafe.ai/v1/systemone`,
   `model: "jev-latest"`. Free signup credits, no card, waitlist-gated.
2. **OpenRouter paid:** `POST https://openrouter.ai/api/v1/chat/completions`,
   `model: "typesafe/jev-1.13"`. Costs `$0.042/1M` input, output free.
   Requires purchased credits. There is no `:free` variant.
3. **Degraded (`openrouter/free`):** advisory only. Force JSON-only output,
   treat the verdict as uncalibrated, and never auto-push on it alone.
   Tests (step 9) plus the reviewer role (step 10) still decide.

## 2. Call shape (TypeSafe)

```json
{
  "state": "<issue text + diff + test results, keep under 32k tokens>",
  "model": "jev-latest",
  "questions": {
    "closes_issue": {
      "type": "noul",
      "instructions": "Does this diff close the issue as scoped?"
    }
  }
}
```

Answers come back under the same keys with probabilities and `confidence`.
`noul` returns `0` (no) to `1` (yes). `choice` returns the winner plus the
full distribution. `score` returns a weighted value plus `legend`.

## 3. Gate A - step 4, duplicate / prior-art check

State: issue title + body + candidate PR summary + rejection reason if any.

```json
{
  "already_resolved": {
    "type": "noul",
    "instructions": "Does the linked PR already resolve this issue?"
  },
  "route": {
    "type": "choice",
    "instructions": "What should the pipeline do?",
    "criteria": {
      "proceed": "No resolving PR found",
      "adopt": "A good open PR exists, review it instead",
      "stop": "Already merged, nothing left to do"
    }
  }
}
```

Enforce: `route=proceed` continues. Anything else follows step 4's existing
branches (stop and tell the user). On `confidence < 0.6`, do the browser
re-read yourself instead of trusting the gate.

## 4. Gate B - step 7, analysis readiness

State: intake artifact + root-cause draft + files the fix will touch.

```json
{
  "reproduced": {
    "type": "noul",
    "instructions": "Is the root cause pinned to specific lines, not guessed?"
  },
  "scope": {
    "type": "choice",
    "instructions": "How big is the fix?",
    "criteria": {
      "single": "One file, surgical change",
      "multi": "Several files, needs design care",
      "unclear": "Root cause still vague, do not implement yet"
    }
  }
}
```

Enforce: implement (step 8) only on `reproduced >= 0.75` and
`scope != unclear`. Otherwise loop the Analyst/Researcher roles once more,
then escalate to the user rather than coding on a guess.

## 5. Gate C - step 10, merge gate (runs before the reviewer loop)

State: issue scope + full `git diff` + exact test/lint commands and results.

```json
{
  "closes_issue": {
    "type": "noul",
    "instructions": "Does this diff fully close the issue as scoped?"
  },
  "risk": {
    "type": "score",
    "instructions": "Breakage risk outside the issue scope?",
    "criteria": ["Low", "Medium", "High"]
  },
  "decision": {
    "type": "choice",
    "instructions": "What should happen to this diff?",
    "criteria": {
      "approve": "Mergeable as is",
      "revise": "Has a concrete defect to fix first",
      "escalate": "Uncertain, needs a human call"
    }
  }
}
```

Enforce (thresholds you may tighten per repo, never loosen silently):

- `decision=approve` AND `closes_issue >= 0.90` AND `risk <= 0.30`:
  hand to the Senior Maintainer Reviewer role for the final pass.
- `decision=revise`: fix exactly what the distribution points at, re-run
  tests, re-ask the gate once.
- `decision=escalate` OR `confidence < 0.6` OR still failing after the
  step-10 three-round loop: stop and bring it to the user. Never push to
  "fix later".

On the degraded free-router path, `approve` only shortens the loop, it never
skips the reviewer role or the Voice Gate in step 11.

## 6. Learning loop (how "he learns")

Jev's weights do not update from your runs. What improves is your gate:
thresholds, criteria wording, and which cases you auto-merge. Log every gate
to an untracked file outside the repo and review it:

```bash
# append-only, one JSON object per line, never committed:
~/.cache/contribute/jev-decisions.jsonl
# fields: date, repo, issue, gate, questions, answers, confidence,
#         action_taken, outcome (merged / reverted / CI red)
```

Monthly, or after any revert: re-read the low-confidence and wrong calls,
then change one thing - a threshold value or one `criteria` sentence - and
note it in the log. That history is the learning. If reverts cluster under
`confidence < 0.75`, raise the bar to `0.75`.
