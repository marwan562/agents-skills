# Issue Intake Protocol (steps 3-4) - BLOCKING

Read this file in full BEFORE opening the issue/PR URL. No branch, no code edit,
no `/multi-agents` brief until the intake artifact at the bottom of this file exists.

Why this gate exists: issue authors put decisive evidence outside plain text -
annotated screenshots, drag-dropped images, GIF/video, log pastes, repro repos,
CodeSandbox/StackBlitz links, live demos, sibling-repo references. A `gh issue view`
or `web_fetch` dump silently drops most of that. The rendered page inside
`ego-browser` is the record of truth; the CLI is only a structured complement.

## 1. Invoke ego-browser (required, every run)

Load the `ego-browser` skill the way this environment does it (slash-command,
Skill tool, or `ego-browser nodejs` heredoc per its SKILL.md). Adapt only the
invocation format to the real interface - never the content bar below.

```bash
ego-browser nodejs <<'EOF'
const task = await useOrCreateTaskSpace('contribute-issue-<number>')
cliLog('task space id: ' + task.id)
await openOrReuseTab('<issue-or-pr-url>', { wait: true, timeout: 30 })
cliLog(await snapshotText())
EOF
```

Keep reusing the SAME task space for the issue page, every candidate PR page,
and every external link in this intake. Do not open a new space per link.
Close scratch tabs as you go; keep the issue tab until step 4 is done.
`completeTaskSpace` runs only when the whole contribution is handed off, not
after intake.

If the skill is missing, the CLI errors, login blocks a private repo, or the
page will not render: STOP. Report the exact error and what unblocks it, and
wait. Do not continue on a CLI-only read.

## 2. Full-thread capture checklist

- [ ] Wait for load (`waitForLoad` / `waitForNetworkIdle` where needed), then
  `snapshotText()` with default full-page scope.
- [ ] Scroll and expand until everything is visible: "show more", "load more",
  collapsed comments, resolved/hidden review threads, activity timeline. Re-run
  `snapshotText()` after each expansion round. The last snapshot must contain the
  bottom of the thread (comment box / footer), proving you reached the end.
- [ ] Record: title, body (verbatim for the brief), labels, milestone, state
  (open/closed/merged/draft), assignees, author, reactions/priority signals,
  and every maintainer/contributor comment with author + date. A maintainer's
  later clarification outranks the original body - quote it verbatim.
- [ ] Record the "linked pull requests" / development sidebar and every inline
  `Fixes #N` / `Closes #N` / cross-repo reference (`org/repo#N`, full URLs).
  These are step 4's input.
- [ ] Complement (not replacement) via CLI: `gh issue view` / `gh pr view` /
  `glab` for `--json state,labels,assignees,timeline` where awkward in DOM.
  On conflict, the rendered page wins for content; the CLI wins for raw state.

## 3. Visual assets - open every one, describe what it proves

Authors attach evidence as rendered media, not prose. An unread image is an
incomplete read.

- [ ] Inventory ALL of it: inline screenshots, drag-dropped images, attachments,
  GIF, video, pasted rich tables/code images. Enumerate from `snapshotText()`
  (`url=...` / `loc=...`) plus one `js(...)` image/attachment sweep where the
  snapshot is ambiguous.
- [ ] Open EACH asset at full resolution in the same task space (follow its link,
  click the thumbnail, or `browserFetch` its URL) and `captureScreenshot()` where
  it matters. Read text inside images (error messages, stack traces, version
  strings) character-exact - transcribe short strings verbatim.
- [ ] For each asset write one line: filename/position, type (screenshot/photo/
  GIF/video/log-image), and what it proves (actual vs. expected UI, exact error,
  repro state). Example: `shot-2 (body img 3): Settings modal shows blank list
  after reload, console in shot reads "TypeError: undefined map", matches repro
  step 2`.
- [ ] If an asset fails to load, note it as UNREADABLE with the URL - never skip
  silently. If the body says "see video" and there is no playable media, flag the
  gap for step 7 (Analyst reproduces rather than assumes).

## 4. External URLs - follow every one, summarize what loaded

- [ ] Inventory every outbound link in body + comments: repro repo/branch/commit,
  gist/paste, CodeSandbox/StackBlitz/CodePen, live demo/deploy preview, docs page,
  video (YouTube/Loom), sibling issue/PR (same or other org repo).
- [ ] Open EACH in the same task space (`openOrReuseTab`, `gotoAndWait` for
  in-tab navigation), `snapshotText()` it, and record: what it is, whether it
  still loads, and the one fact it contributes (repro steps, config, failing
  version, expected output). One line each. Mark dead/expired links as DEAD with
  date checked.
- [ ] For repro repos/gists: record default branch, the file/entry point that
  reproduces, and the exact command if given. Do NOT clone it yet - that decision
  belongs to step 7. For videos: watch far enough to capture the failing moment;
  timestamp it.
- [ ] Sibling-repo references get the same treatment as candidate PRs in step 4:
  open rendered, read status + review history, not title alone.

## 5. Related-work pass (step 4, same task space)

- [ ] Open every candidate linked PR/MR from the sidebar and every reference found
  above. Record number, repo, state (open/merged/closed/draft), CI/review state,
  and in one line why it does or does not resolve this issue.
- [ ] For a stale/rejected attempt: quote the maintainer rejection reason verbatim.
  It goes straight into the step 7 brief so the new attempt does not repeat it.
- [ ] Apply the branch rules in SKILL.md step 4 (merged-closes-it / open-covers-it /
  stale-rejected / nothing-found). The "already solved" verdict must cite rendered
  pages, not search-result titles.

## 6. Intake artifact (required output - paste into step 7 brief)

Produce this block before leaving intake. Steps 6-7 consume it verbatim:

```text
INTAKE - <issue-or-pr-url> (rendered via ego-browser, <date>)
TITLE: <verbatim>
STATE/LABELS: <open/closed + labels + assignees>
THREAD: <N comments read to footer; maintainer direction quoted verbatim>
PROBLEM: <1-3 sentences: symptom, repro, acceptance bar>
VISUALS (<n> found, <n> opened):
- <asset 1: what it shows, key transcribed text>
- <asset 2: ...>
- (or: NONE - no images/video in body or comments)
EXTERNAL LINKS (<n> found, <n> opened):
- <url 1: what it is, loads Y/N, one fact it contributes>
- (or: NONE)
RELATED WORK: <linked PRs with state + one-line verdict each; rejected reason quoted>
GAPS: <what is still unknown; what Agent A must reproduce vs. take at face value>
```

Keep the whole artifact short and factual. Verbatim quotes for maintainer
direction and error strings; one-line summaries for everything else.

## 7. Stop conditions (do not work around these)

- ego-browser unavailable / page unrenders / auth wall -> stop, report, wait.
- Visuals or repro link unreadable and material to the bug -> mark UNREADABLE/DEAD,
  flag in GAPS, and if the issue is uninterpretable without it, ask the user
  before burning step 7 cycles on a guess.
- Never mark intake done after `gh issue view` alone, after the first viewport
  without scrolling, or with unopened images/links still on the list.
