# Pull Request Description Templates (pick by diff size)

Used in **Step 11** of the `contribute` pipeline. Small diff = small text.
Default to the smallest template that fits. Headers only when this repo's own
`PULL_REQUEST_TEMPLATE.md` (found in step 5) forces them. Never more bullet
lines than changed lines. B2 casual English, one contraction minimum in
anything over 2 sentences, zero em dashes.

Before filling any of these, read `references/human-voice.md` and this repo's
last 5 to 6 merged PRs, then match their length, casing, and issue-link style.

---

## Tiny: typo, docs fix, 1 to 5 lines (use this most)

No headers. No list. No checklist.

```markdown
<title: one thing, e.g. "fix: error when a required flag is missing instead of exiting 0">

<body, 1 to 2 sentences>
`--config ''` slipped through because the parser only checked presence,
not empty. It doesn't error, it just exits 0. Fixed with a check next
to the existing ones.

Closes #241
```

## Small: one bug fix, one or two files

No headers unless the repo template forces them. 3 to 6 sentences:
what broke, what you picked, proof.

```markdown
<title: one thing, under ~60 chars>

Running without --config used to exit 0 with no output. Now it prints
a usage error and returns 1, same as --help already says it should.
I went with an early check in cmd/root.go so the rest of the flow stays as is.
Tested with `go test ./cmd/...`, all pass. I've added one table case in
cmd/root_test.go for the empty-string case.

Closes #241
```

## Medium: feature or multi-file fix

Plain paragraphs. Use the repo's own headers only if its template has them,
and fill them with sentences, not a tour of every file.

```markdown
<title: one thing>

<why, 2 to 3 sentences>
Users hit X when they do Y. It happens because Z. I picked approach A over B
because <one concrete reason>.

<proof, 1 to 2 sentences>
Ran `<exact test command>`, all pass. Added <where the new test lives> covering
<the new behavior>. Doesn't cover <known limit> yet, happy to follow up.

Closes #<issue-number>
```

If step 4 found a stale or rejected prior attempt, add one line:
`Tried a different cut in #<old-pr>, this one <what changed> per <maintainer>'s note.`

---

## Title rules (all sizes)

- One thing only. If it needs "and", split the PR.
- Match merged PRs: Conventional Commits (`fix: ...`) only when the repo
  actually uses it, otherwise plain sentence.
- Under ~60 chars. Lowercase after the colon. No period at the end.
- Bad: "feat: Add comprehensive support for X with enhanced Y and improved Z"
- Good: "fix: error when a required flag is missing instead of exiting 0"

## Voice Gate reminder (internal, never posted)

Run `references/human-voice.md` Rule 6 on the title + body before pushing:
no em/en dashes, no bare `--` pauses, no banned words, no chatbot closers,
length matches the diff, proof line present, `Closes #N` once. Rewrite until
it passes. Three failed rewrites means stop and show the draft to the user.

## Reference files

- `references/multi-agent-brief.md` - exact brief template + worked example for step 7,
  including where step 4's related-work findings go.
- `references/ecosystem-detection.md` - language/build-tool detection and command lookup
  for steps 5 and 9.
- `references/pr-template.md` - PR description template for step 11.
- `references/human-voice.md` - BLOCKING voice rules and Rule 6 self-check for
  all public text. Read it before drafting any title, body, or comment.