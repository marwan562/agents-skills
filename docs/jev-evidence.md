# Jev Evidence Template

How to prove Jev speeds up the contribution workflow — with measured numbers,
not adjectives. Jev does not change model inference speed. It shortens the
loop: fewer rewrites, fewer review rounds, fewer CI reds.

## What to measure

Run comparable issues with gates on vs. off and record:

| Metric | Without Jev | With Jev |
|---|---|---|
| Review rounds to mergeable diff | | |
| Wall-clock time, issue to open PR | | |
| CI red on first push (yes/no) | | |
| Reverts within 30 days (yes/no) | | |
| Gate C first-try pass (yes/no) | | |

One honest table from 5-10 issues beats any speedup claim.

## Logging format

Append one JSON object per gate call to an untracked file outside the repo
(never committed):

```bash
~/.cache/contribute/jev-decisions.jsonl
```

Fields per line:

```json
{
  "date": "2026-09-19",
  "repo": "owner/repo",
  "issue": 42,
  "gate": "C",
  "task": "one-line scope",
  "scores": { "correctness": 8.3, "security": 8.0 },
  "confidence": 0.7,
  "action_taken": "approve-to-reviewer | revise-once | escalate",
  "outcome": "merged | reverted | ci-red"
}
```

Monthly, or after any revert: re-read low-confidence and wrong calls, change
one thing (a threshold or one task sentence), note it in the log. If reverts
cluster under confidence `< 0.75`, raise the bar to `0.75`.

## Worked example (real session)

Integrating `jev_review` gates across this collection (`feat/jev-review-all-skills`):

1. Implemented: rewrote `skills/contribute/references/jev-decisions.md`,
   added short gate sections to 6 skills.
2. Validated: `python3 scripts/validate-skills.py` → 7 skills, 0 errors.
3. Baseline via `jev_review`: Duplication 7.6, Changeability 7.9 (low).
4. Fixed: trimmed per-skill blurbs to 3-4 lines each, centralized on one file.
5. Rescored with `previousEvaluation`: Duplication 7.6 → 8.9,
   Changeability 7.9 → 8.6, no regressions, priorities empty. Stopped.

Total: two Jev calls, one focused edit, validator green throughout.

## Demo checklist

- Record: implement → baseline scores → one fix → rescore deltas.
- Show the delta numbers on screen (e.g. `Duplication 7.6 → 8.9`).
- State the setup: `JEV_API_KEY` env, local MCP server, `previousEvaluation` loop.
- Never paste keys, never send secrets as review context.

Full gate protocol: `skills/contribute/references/jev-decisions.md`.
