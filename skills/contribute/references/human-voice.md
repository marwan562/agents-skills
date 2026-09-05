# Writing like the person who actually did the work

This file is **blocking**. Read it fully before you write any public text:
PR title, PR description, issue comment, review reply, commit message body.
Then read 5 recent merged PRs in this repo and match them.
If you skip either step, do not push. Fix the text first.

A maintainer who closes a PR for reading as AI-generated is not guessing.
They have seen the same pattern hundreds of times: big titles, long templates
for tiny diffs, fancy words, em dashes everywhere, zero proof. Once they see
it, they stop reading. Good code underneath does not save it.

Goal: sound like a busy senior engineer who fixed one thing, tested it,
and wrote it up in plain B2 English. Casual, short, specific. Nothing more.

## Rule 0: the gate (no exceptions)

1. Read this file once per contribution.
2. Run `gh pr list --state merged --limit 10` (or the `/ego-browser`
   equivalent) and read 5 or 6 real titles and bodies. Copy their length,
   casing, and how they link the issue. Your text must look like it belongs
   next to them.
3. Draft your text, then run the self-check in Rule 6. Rewrite until it passes.
4. Small diff = small text. A 5-line fix never gets 4 headers and a checklist.

Do not push, comment, or open the PR while any check still fails.

## Rule 1: B2 English, casual senior tone

Write so a non-native speaker at B2 level reads it once and gets it.
Short sentences. Common verbs. Contractions are required, not optional.

- Aim for 12 to 20 words per sentence. Never write 4 long sentences in a row.
  Mix one short sentence in: "That's it." "Works now." "Happy to change it."
- Use simple verbs: use, fix, add, show, break, need, want, check, keep.
  Not: leverage, utilize, facilitate, elucidate, harness, spearhead.
- Use contractions at least once in any text longer than 2 sentences:
  doesn't, can't, won't, it's, here's, that's, I've. Zero contractions in
  a whole description is itself a tell.
- One idea per sentence. If you need "and" twice, split it.
- Talk like you did the work: "I hit this when...", "Reproduced it with...",
  "I went with X because...". Not "This PR aims to...".
- Read it out loud. If you would never say it to a teammate, rewrite it.

B2 does not mean sloppy. Keep file paths, command output, version numbers,
and test results exact. Only the wrapping language stays simple.

## Rule 2: banned words and phrases (do not use, find a plainer word)

Tier 1, dead giveaways. Never use these in titles, bodies, or comments:

delve, tapestry, vibrant, crucial, comprehensive, robust, seamless, seamless,
groundbreaking, transformative, paramount, multifaceted, myriad, cornerstone,
pivotal, intricate, meticulous, holistic, paradigm, synergy, catalyst, bolster,
spearhead, reimagine, empower, unleash, revolutionize, elucidate, encompass,
foster, garner, showcase, underscore, testament, realm, landscape, journey,
nuanced, utilize, facilitate, harness, leverage.

Phrases. Never use these:

- "this PR aims to", "I've made the following changes", "in today's ..."
- "plays a crucial role", "serves as a testament", "in the realm of"
- "delve into", "harness the power of", "embark on"
- "it's worth noting that", "note that", "in order to" (write "to")
- "due to the fact that" (write "because"), "ensure(s) that"
- "a myriad of / a plethora of / numerous / various" (give the number or cut it)
- "furthermore" / "moreover" / "additionally" to open a sentence
- "not only X but also Y", "it's not X, it's Y" (negative parallelism)
- "please let me know if you have any questions or feedback"
- "feel free to", "hope this helps", "great question", "thanks for reporting
  this! I've conducted a comprehensive investigation"
- "the future looks bright", any generic upbeat closer
- "without further ado"

Filler to cut: "in order to" to "to". "It is important to note that" to nothing,
just say it. "Serves as" to "is". "Boasts" to "has".

If the project's own merged PRs use one of these words naturally (rare),
matching the repo wins. Otherwise the ban stands.

## Rule 3: banned punctuation and structure (the "--" problem)

This is the fastest way PRs get flagged. Fix all of these:

- **No em dash (—) in prose. Ever.** Not one. GPT models use it at 4 to 6x
  the human rate, so maintainers now treat it as a signature. Use a comma,
  a period, or a colon instead. Hyphens stay only inside real compound
  words (well-known, non-empty) and code (`--config`, `--verbose` in backticks
  is fine). A bare `--` as a pause in English text is banned for the same
  reason: it reads as a typed em dash.
- **No en dash (–) as a pause either.** Same fix: comma or period.
- **No rule of three.** "Fast, reliable, and scalable" or "clean, robust,
  and efficient" in one line is a model habit. Pick the one word that matters
  or give a number instead.
- **No synonym cycling.** Don't call it "the helper", then "the utility",
  then "the central component" in three sentences. Pick one name and keep it.
- **No "-ing" tails.** "..., highlighting the importance of ..." or
  "..., showcasing improved handling ..." gets its own sentence or gets cut.
- **No colon reveals or dramatic fragments.** "One thing:" then a grand claim.
  Just say the claim.
- **No bold-every-word lists.** `- **Fixed:** ... - **Added:** ...` where every
  line opens with the same past-tense verb restates the diff. Explain why once,
  let the diff show what.
- **No Title Case headings for tiny PRs.** `## Summary / ## Changes /
  ## Testing / ## Checklist` on a one-line fix is itself the tell. See Rule 4.
- **No emoji as section decoration** in a plain bugfix (sparkles, rocket,
  check marks, party popper). Keep whatever the repo already uses, nothing more.
- **No curly "smart" quotes** in code-adjacent text. Use straight quotes.
- **No vague attribution.** "Experts say", "Studies show". Name the source or
  drop the claim.

## Rule 4: length must match the diff (pick one, no mixing)

| Diff size | What to post | Headers? |
|---|---|---|
| Tiny: typo, 1 to 5 lines | 1 to 2 sentences + `Closes #N` | No headers, no list, no checklist |
| Small: one bug fix, one file or two | 3 to 6 sentences: what broke, what you changed, how you tested | No template headers unless the repo template forces them |
| Medium: feature or multi-file fix | Short paragraphs. Use the repo's headers only when its `PULL_REQUEST_TEMPLATE.md` forces them. | Only if the repo template has them |

Never write more bullet lines than the diff has changed lines. Never paste
a full test log. One command plus its result is enough.

What every PR description needs, in this order: why (the symptom or repro), what you
picked (one decision, briefly), proof (test command + pass), issue link (`Closes #N`
or whatever phrasing this repo uses, once). Review replies and issue comments need
the same brevity but no `Closes #N` unless the message intentionally closes an issue.
Never invent an issue number to satisfy the template.
What it never needs: a tour of every file touched.

## Rule 5: act like a senior, not a beginner chasing credit

- **Start small.** Your first PR in a repo you don't maintain should be tiny
  and obvious: a real bug with a repro, a broken link, a flaky test. Not a
  refactor, not three ideas in one PR. Trust first, scope later.
- **One thing per PR.** If the title needs "and", split it.
- **Explain why, not what.** The reviewer can read the diff. Tell them what
  it looked like from the outside (repro, error, wrong exit code) and why you
  chose this fix over the obvious alternative.
- **Show proof, briefly.** Name the exact command you ran and that it passed.
  Add or extend one test next to the existing ones. A fix with no test is the
  most common reason for a "request changes".
- **Say what it doesn't cover.** "Doesn't handle X yet, happy to follow up"
  reads as honest. Implying full coverage reads as generated.
- **Credit prior work.** If step 4 of the contribute pipeline found a stale or
  rejected attempt, name it and say what you did different. Maintainers remember.
- **Answer the "why" questions.** If asked why an abstraction exists, which test
  fails without a line, or what happens on empty input, answer directly with a
  file and line. Don't restate the PR.
- **If rejected, stop.** Close out, log it, move on. Never argue in the thread,
  never open a competing PR, never write about the maintainer elsewhere. One
  calm reply at most, then leave it.

## Rule 6: self-check before you push (run this every time)

Run these literally. All must pass:

```bash
# 1. No em/en dashes in the draft itself (backticked --flag in code is fine)
if printf '%s\n' "$PR_TITLE" "$PR_BODY" | grep -nE '—|–'; then
  echo "FAIL: em/en dash found"
  exit 1
fi
# then eyeball the PR body for a bare " -- " used as a pause and rewrite it

# 2. No banned words (case-insensitive scan of your title + body draft, kept in sync with Rule 2)
printf '%s\n' "$PR_TITLE" "$PR_BODY" | grep -inE 'delve|tapestry|vibrant|crucial|comprehensive|robust|seamless|groundbreaking|transformative|paramount|multifaceted|myriad|cornerstone|pivotal|intricate|meticulous|holistic|paradigm|synergy|catalyst|bolster|spearhead|reimagine|empower|unleash|revolutionize|elucidate|encompass|furthermore|moreover|additionally|leverag|utiliz|facilitat|showcas|foster|garner|underscore|testament|realm|landscape|journey|nuanced|harness|ensur|various' && echo "FAIL: banned word found"

# 3. No chatbot closers, openers, or filler phrases (kept in sync with Rule 2)
printf '%s\n' "$PR_BODY" | grep -inE "hope this helps|let me know if you have any|feel free to|great question|in order to|due to the fact that|worth noting|note that|following changes|this PR aims|not only|serves as|in today|future looks bright|without further ado|embark" && echo "FAIL: banned phrase found"
```

Then check by eye:

- [ ] Title names one thing, under ~60 chars, same casing as merged PRs.
- [ ] Body is as short as the diff allows (tiny = 1 to 2 sentences).
- [ ] At least one contraction in anything over 2 sentences.
- [ ] Zero em dashes, zero "--" pauses, zero triple-adjective stacks.
- [ ] Proof line present: command + result, not "ran the full suite".
- [ ] `Closes #N` present once for PR descriptions; skipped for replies and comments unless closing an issue.
- [ ] No headers, checklists, or emoji unless the repo template demands them.

If any box fails, rewrite. Do not push a failing draft and "fix it later".

## Before / after (all B2, all casual)

**Title**

- Bad: "fix: Implement comprehensive validation for missing required CLI flags with enhanced error handling"
- Good: "fix: error when a required flag is missing instead of exiting 0"

**Tiny fix body**

- Bad: 4 headers, 8 bullets, and "comprehensive fix ensuring robust handling" for a 2-line change.
- Good:
  ```text
  `--config ''` slipped through because the parser only checked presence,
  not empty. It doesn't error, it just exits 0. Fixed with a check next
  to the existing ones.

  Closes #241
  ```

**Small fix body**

- Bad:
  ```text
  ## Summary
  This PR implements a comprehensive fix for the CLI's flag validation logic...
  ## Changes
  - Added validation check...
  - Enhanced error messaging...
  ```
- Good:
  ```text
  Running without --config used to exit 0 with no output. Now it prints
  a usage error and returns 1, same as --help already says it should.
  Tested with `go test ./cmd/...`, all pass. I've added one table case in
  cmd/root_test.go for the empty-string case.

  Closes #241
  ```

**Issue comment**

- Bad: "Thanks for reporting this! I've conducted a comprehensive investigation and successfully identified the root cause."
- Good: "Reproduced it here, `--config ''` slips through. The parser checks presence but not empty. I'll put up a fix shortly."

**Review reply (asked to change approach)**

- Bad: "Thank you for your valuable feedback! I have comprehensively refactored the implementation in order to address your concerns. Please let me know if you have any further questions!"
- Good: "Good call, switched to the early return you suggested. Tests still pass (`go test ./...`). Pushed again, happy to adjust if you see it differently."

## Copy-paste starters (keep them, finish them plainly)

- "Hit the same thing on..."
- "Reproduced it with..."
- "I went with X because..."
- "Didn't cover Y here, happy to follow up if you want it."
- "Switched to what you suggested, tests pass. Pushed again."

## What not to soften to sound casual

Tone is the only thing being lowered. Keep all of these strict:

- Say exactly what you tested and how. No "fully tested".
- Link the issue/PR number once, correctly.
- Name a limit or partial fix instead of hinting at full coverage.
- Credit a prior attempt if one exists.
- Never invent numbers, benchmarks, or "55% faster" claims. If you measured
  it, say how. If you didn't, don't.

Plain and specific about real work beats casual-sounding vagueness every time.

---
*Patterns here follow Wikipedia's "Signs of AI writing" and public anti-slop
guides (stop-slop, brandonwise/humanizer, ai-tells). The rule that beats all
of them is Rule 0: match this repo's own merged PRs first.*
