---
name: contribute
description: Use this skill to contribute via GitHub/GitLab/Gitea issue/PR links (fixing bugs, implementing features). Triggers on "start this issue", "pick up this ticket", contributions dir, or open-PR requests. Uses ego-browser intake and multi-agents review before push.
---

# Contribute

> You've got a link. This skill takes it from there.

Orchestrates an end-to-end open-source contribution: from a bare issue or pull request link all the
way to an opened PR, with no manual gates in between once the work itself checks out.
It reads the issue like a maintainer would. Then it fixes it, tests it, and opens a PR you don't have to babysit.
Delegates rendered issue/PR intake to browser intake (rendered read via `/ego-browser` preferred, browser subagent fallback per `references/issue-intake.md`)
and deep analysis/review to `/multi-agents`. Nothing here is tied to one project,
one host, or one language - the pipeline shape is fixed, everything else is detected
fresh each run.

## Purpose

Help you earn trust with a PR that is easy to merge.

Give it an issue link. It sends back a small fix with a test and proof. It pings you only when it must.

That's the bar. Small diff. Real proof. Kind tone.

### Act with full ownership

A trusted human contributor doesn't pitch a plan and wait for a nod before opening their
editor - they read the issue, understand the codebase, and get to work, looping in a
maintainer only when something is genuinely ambiguous or high-stakes. Once steps 1-5 have
given you that same footing, hold yourself to the same standard. The checkpoints later in
this skill are the *complete* list of moments worth a pause - routine calls a competent
contributor makes independently (which test file to extend, whether a helper deserves its
own file, commit styling) are yours to make, not questions to surface. Put the reasoning in
the commit and PR description, where it actually benefits reviewers.
The same standard applies to everything posted publicly: see `references/human-voice.md`
before writing any comment, issue text, or PR content. No public text gets pushed or posted
until its Rule 6 self-check passes. Write in plain B2 English, casual and short, like a senior
engineer who fixed one thing. Never in high-formal, buzzword-laden, em-dash-filled prose.

Maintainers are busy volunteers. They merge work they can read fast.

Keep the diff small. Show what you ran and that it passed. Credit prior tries. Keep it short so they can say yes fast.

## When to Use

- User shares an issue or pull request URL from GitHub, GitLab, Gitea, etc., paired with intent to work on it ("start this issue", "let's fix", "pick up this ticket", "here's the next one")
- User mentions a local `contributions/` directory or asks to begin an open-source task
- User requests opening a bug fix or feature PR against an external upstream repository
- User wants an end-to-end autonomous contributor pipeline that doesn't halt for routine micro-decisions

### What "done" looks like from the user's side

Just this:

> "Here's the next one: `<issue-or-pr-url>`. Repo's in contributions/."

That's a complete invocation. The skill infers the rest, checks whether the ground has
already been covered by someone else, and - once it's confident the work is solid - pushes
and opens the PR itself. It only interrupts you at the explicit checkpoints listed below.

## Inputs

- **Required:** one URL to an issue or PR. Parse it generically - host, owner/org, repo
  name, number - rather than assuming GitHub. GitHub -> use `gh` for structured
  fields. GitLab -> use `glab` for structured fields. Anything else -> detect via
  browser intake (preferred) or `web_fetch`/`web_search` against the web UI.
  Host detection never changes the intake rule. Read the issue body and comments rendered
  in browser intake per `references/issue-intake.md`, on every host.
- **Inferred when not stated:**
  - *Local repo path* - check in this order: (a) a path the user just mentioned, (b)
    `~/contributions/<repo>`, (c) `~/code/contributions/<repo>`, (d) `./contributions/<repo>`
    in the current workspace, (e) a case/dash/underscore-insensitive fuzzy match across
    those roots. Nothing found -> ask once whether to clone into `~/contributions/<repo>`
    (default) or elsewhere. Don't silently clone - it's the one setup step worth a
    question.
  - *Issue vs. PR* - tell from the URL shape (`/issues/` vs `/pull/` or `/merge_requests/`)
    or from fetched metadata.
  - *Agent roles for step 7* - default to the three-role brief below; only scale up for
    genuinely large issues (see "Scaling the agent brief").

## External skills this depends on

**Blocking-required - the pipeline stops without this:**

- **Browser intake** (steps 3-4, blocking gate via `/ego-browser` preferred, browser subagent fallback) - the ONLY accepted way to read the
  issue/PR. Open the live rendered page as a maintainer would see it and capture:
  (a) title, body, labels, assignees, state, reactions/priority signals;
  (b) the FULL comment thread including collapsed/hidden comments, review threads,
  and the "linked pull requests" sidebar;
  (c) every visual asset - screenshots, attached images, video/GIF, pasted rich
  media - viewed at full resolution, with what each one actually shows written down;
  (d) every external URL in body/comments (repro repos, CodeSandbox/StackBlitz,
  live demos, docs, videos, sibling-repo issues/PRs) - followed and summarized;
  (e) cross-references into sibling repos in the same org.
  Follow the exact protocol in `references/issue-intake.md` and produce its intake
  artifact before touching code. `gh issue view` / `glab` / `web_fetch` supply
  structured fields (state, timeline, assignees) as a complement - they NEVER replace
  the rendered read, because linked-PR sidebars, reactions, images, and external
  repro content do not come through cleanly as text.
  - Attempt a rendered read first, every run: `/ego-browser` preferred, browser subagent / Playwright fallback per `references/issue-intake.md`.
    CLI-only is permitted only as a logged exception after a failed rendered attempt, with the intake artifact recording the attempted method, the exact error, and an explicit `VISUALS: UNVERIFIED` flag. Never infer `VISUALS: NONE` from CLI text alone.
  - If no browser tool can launch, or the page fails to load and no fallback renders it:
    STOP. Tell the user plainly what failed and what resolves it (e.g. install/enable the skill, log in for a
    private repo, paste the exact error), and wait. A `gh`-only read is not an
    acceptable substitute for this gate.
  - Opencode / generic agents: invoke it the way this environment loads skills
    (slash-command, Skill tool, or `ego-browser nodejs` heredoc per its SKILL.md).
    Adapt only the invocation format, never the content bar: full thread + visuals
    + external links, every run.

**Required with graceful solo fallback:**

- **`/multi-agents`** (steps 7 and 10) - runs the three-role analysis/review brief. See
  `references/multi-agent-brief.md` for the exact shape to hand it. If it isn't installed,
  or there's no subagent-spawning tool at all in this environment, don't let the pipeline
  stall waiting for it - read the brief yourself and work through the three roles in order
  (Root-Cause Analyst, then Codebase & Convention Researcher, then - held back until step
  10 - Senior Maintainer Reviewer) inside your own reasoning instead. You lose the
  independence of a separate pass doing it this way, so be honest in the reviewer role
  rather than rubber-stamping your own work - reread that role's "OUTPUT EXPECTED" in the
  brief and hold your diff to it as if someone else had written it.

If the call shape either skill actually expects (flags, JSON, a fixed slot count) differs
from what's described here, adapt the *format* to match its real interface but keep the
content and roles intact. If you're ever unsure how one wants to be invoked, ask the user
to paste its SKILL.md once rather than guessing.

**Optional companions - reach for these when the situation calls for it, not as a checklist
to run through every time:**

- **`code-review`** - lends its correctness/security/maintainability/performance/testing
  checklist to the Senior Maintainer Reviewer role in step 10, so the review has real
  structure behind it instead of a vague "looks fine."
- **`jev-decisions`** (`references/jev-decisions.md`) - optional `jev_review`
  MCP gate for steps 4, 7, and 10. Scalar scores + confidence with
  `previousEvaluation` deltas instead of a chatty "looks good". Never writes
  code, never replaces tests. Skipped entirely when `JEV_API_KEY` is not
  configured.
- **`documentation`** - for a change that touches public APIs, config, or commands, keeps
  README/CHANGELOG/API docs in sync with the diff instead of leaving them stale.
- **`project-architecture`** - for a cross-cutting or large-feature issue, works out module
  boundaries before step 8 instead of improvising structure mid-implementation.

## Workflow

### 1. Parse the link
Extract host, owner, repo, and number. Everything downstream reads from what's detected
here - don't hardcode to whichever project you saw last.

### 2. Locate and sync the local clone
- Find the repo using the inference order above.
- `git remote -v` to see the actual remote setup (a fork workflow usually has `origin` =
  the user's fork, `upstream` = the real project). Add `upstream` from the parsed
  owner/repo if the fix needs to sync against it and it's missing.
- If `origin` isn't something you'll actually be able to push to later - it points at the
  upstream project itself rather than a fork, and you don't have write access - don't wait
  until step 11 to find that out. Fork it now (`gh repo fork` / `glab repo fork`, run with
  no arguments from inside the clone): both rename the existing `origin` to `upstream` and
  add the new fork as `origin` automatically, so there's somewhere to push when the time
  comes.
- Detect the real default branch (`main`, `master`, `develop`, ...) - don't assume `main`.
  `git fetch` the right remote, check out the default branch, pull.
- If there are uncommitted local changes, **stop and ask** rather than stashing: that work may matter to the user. Alternatively, work in an isolated `git worktree` (`git worktree add -b fix/<issue> ../<repo>-worktrees/fix-<issue> <default-branch>`) so work proceeds immediately in a clean directory without touching the user's uncommitted files.

### 3. Read the issue or PR (BLOCKING - browser intake only)
Run this inside browser intake per `references/issue-intake.md` (`/ego-browser` preferred, browser subagent fallback). Do not start it via
`gh issue view` alone, and do not treat the first screen as the whole read.

1. Open the exact URL the user shared in a dedicated browser task space
   (e.g. `contribute-issue-<number>`). Wait for load, capture `snapshotText()`,
   and scroll/expand until the full thread is visible - including collapsed,
   "show more", "load more", and resolved review threads.
2. Capture structured state as a complement (`gh`/`glab`: state, labels,
   assignees, timeline), but the rendered read is the record of truth. A
   maintainer's clarifying comment outranks the original issue body.
3. Inventory and OPEN every visual asset: screenshots, drag-dropped images,
   attachments, GIF/video. View each at full resolution (follow its link or
   screenshot it), and write down what it proves - error text, broken UI state,
   expected vs. actual - not just "has screenshot". An unread image is an
   incomplete read.
4. Inventory and FOLLOW every external URL in the body and comments - repro repo,
   branch, commit, CodeSandbox/StackBlitz/CodePen, live demo, docs page, video,
   log paste, sibling issue/PR. Open each in the same task space, note what it
   contains and whether it still loads. Mark dead links as dead; never silently
   ignore them.
5. Pull out the problem statement, repro steps, acceptance criteria, and how
   labels change scope (bug vs. feature vs. good-first-issue). Quote maintainer
   direction verbatim for the step 7 brief.
6. Write the intake artifact (title, thread summary, visual inventory, external-link
   inventory, related-work leads) exactly as `references/issue-intake.md` defines.
   Steps 4, 6, and 7 MUST NOT start until it exists. If the issue body is thin
   after all of this, say so explicitly - Agent A in step 7 reproduces from the
   visuals/repro link rather than the text.

### 4. Check for related work and duplicates (still inside browser intake)
Before writing anything, find out if this ground has already been covered, using
the rendered context from step 3 - not title search alone:
- Look at the "linked pull requests" sidebar from step 3 for anything already tied to this
  issue.
- Search the issue/PR body and comments for references to other issues or PRs - including
  ones in **sibling repos** in the same org (a monorepo-adjacent project like
  `sveltejs/svelte` + `sveltejs/kit` cross-references constantly; don't assume the fix
  lives only in the repo the issue was filed against).
- Use browser intake to open any candidate PR(s) you find and read their actual status and
  review history, not just their title. Follow cross-repo references in the browser
  too - a fix that started in a sibling repo reads differently in rendered review
  comments than in a timeline API dump.
- Branch on what you find:
  - **Already merged and it closes this issue** - stop, tell the user it looks resolved
    already (with the link), and check whether the original issue should have been closed
    or whether some part of it is still open.
  - **An open PR already addresses it well** - don't open a competing one. Summarize its
    approach to the user and ask whether to review/improve that PR instead, or move to a
    different issue.
  - **A stale or explicitly rejected prior attempt** - use browser intake to read *why* it
    stalled or was rejected (maintainer review comments are the ground truth here), and
    carry that reasoning into the brief in step 7 so the new attempt doesn't repeat it.
  - **Nothing found** - proceed normally.
- **Optional Jev gate:** if a Jev key is configured, run Gate A from
  `references/jev-decisions.md` on the candidate-PR evidence. It advises only;
  the branches above still decide.

### 5. Learn the project's own conventions before touching code
Read whatever exists, in priority order: `CONTRIBUTING.md` / `.github/CONTRIBUTING.md`,
`CODE_OF_CONDUCT.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `.github/ISSUE_TEMPLATE/`,
`docs/DEVELOPMENT.md`, the dev-setup section of the root `README.md`, and lint/format/commit
configs (`.eslintrc*`, `.editorconfig`, `rustfmt.toml`, `.pre-commit-config.yaml`,
`commitlint.config.*`). See `references/ecosystem-detection.md` for the language ->
build/test/lint command lookup so you're not guessing `npm test` on a Rust repo. This step
is never skippable, even for a one-line fix - it's what stops a good fix from getting
bounced for a style nit instead of the actual code.

### 6. Create a working branch
Name it per the project's own stated convention if step 5 turned one up; otherwise
`fix/<issue-number>-<short-slug>` or `feat/<issue-number>-<short-slug>`. Branch off the
freshly-synced default branch from step 2, never off a stale local branch.

### 7. Delegate deep analysis to /multi-agents
Once steps 3-5 give real context (not before - a vague brief produces vague agent output),
run `/multi-agents` with a three-role brief (or work the same brief solo, wearing each hat
in turn - see "External skills this depends on" above - if it isn't available). The brief's
Shared Context Block MUST include the step 3 intake artifact verbatim - thread quotes,
visual-asset findings, and external-link findings - plus step 4 and step 5 context, so
subagents never re-derive or silently drop what the browser already proved. Read
`references/multi-agent-brief.md` before your first call - it has the full template,
including where the step 4 findings go, and a worked example so the roles come out sharp
instead of generic. In short, the default roles:

1. **Root-Cause Analyst** - isolates the defect and creates a minimal failing reproduction test case or script (Red state). Diagnoses and proves the failure mechanics down to specific files and line numbers; does not write the final application fix yet.
2. **Codebase & Convention Researcher** - deep-searches the repo for the files the fix will touch, prior art (similar past PRs/commits), the conventions gathered in step 5, and the exact test harness where the reproduction test belongs.
3. **Senior Maintainer Reviewer** - held back until step 10; reviews a real diff, not the issue. Simulates a maintainer of *this specific project*, applying the same correctness/security/maintainability/performance/testing lens as the `code-review` skill (use it directly if it's available) against the actual stated standards from step 5, rather than generic best practice.

Hand each agent the issue/PR content from step 3, the related-work findings from step 4 (especially any rejected prior approach to avoid repeating), and the conventions from step 5 directly: they shouldn't have to re-fetch what's already gathered.
- **Optional Jev gate:** if a Jev key is configured, run Gate B from `references/jev-decisions.md` on the analysis. Implement only when it passes; otherwise loop the roles once, then escalate instead of coding on a guess.

### 8. Implement (Red-Green-Refactor)
Using Agent A's reproduction test and Agent B's codebase research as the spec:
- **Red:** Run the reproduction test case to verify it fails cleanly on untouched code for the exact reported reason.
- **Green:** Implement the minimal fix to satisfy the test and make the suite pass. Keep the diff as small as the issue actually requires: note unrelated cleanup opportunities separately instead of folding them in. Act like a senior earning trust, not a beginner proving range: one issue, one minimal fix, existing patterns reused.
- **Refactor:** Clean up internal structure, adhere to local idioms, and ensure no regressions without expanding scope.

Commit while you work per `references/commit-discipline.md`, not once at the end. Each finished slice (fix plus its test, docs that belong to that slice) becomes a local commit right after its slice checks pass. Group related files together. If the whole fix is one idea in one or two files, keep it as one commit. Do not split one logical fix into micro-commits to look busy.

### 9. Verify locally
Run the project's actual test/lint/build commands (from step 5 /
`references/ecosystem-detection.md`), never assumed generic ones. Add or update a test for
the change - a fix with no accompanying test is one of the most common reasons maintainers
request changes. Verify each slice before its local commit per
`references/commit-discipline.md` section 4 (`git status --short`, staged diff review,
slice tests and lint, no secrets, identity check). Re-run the full suite, not just the new
test, before step 11, to catch regressions.

### 10. Maintainer-style review
Send the real diff (not the plan) to the Senior Maintainer Reviewer role from step 7. Have
it check, against this project's own conventions: correctness, test coverage, style/lint
cleanliness, commit hygiene per `references/commit-discipline.md` (one logical change per
commit, fix travels with its test, no unrelated cleanup folded in), whether it actually
closes the issue as scoped, and anything a
maintainer would flag (missing docs, breaking-change risk, unhandled edge cases). Every
finding that points at code must cite a commit-pinned permalink per
`references/permalink-evidence.md`, never a bare `path:line` on the default branch.
Loop
steps 8 -> 10 until it passes or you hit three rounds; if it still isn't converging, stop
and bring the disagreement to the user instead of pushing something unresolved. Each
review round that changes code becomes a new local commit on the same branch, never a
silent amend, so the maintainer can see what moved since their last look.
- **Optional Jev gate:** if a Jev key is configured, run Gate C from
  `references/jev-decisions.md` on the diff + test results BEFORE the reviewer
  loop. `approve` goes to the reviewer; `revise` fixes and re-asks once;
  `escalate` or low confidence stops. The reviewer role and the three-round cap
  still apply on every path.

### 11. Commit, push, and open the PR - automatically, but never past the Voice Gate

This step has a hard gate inside it. The push is automatic once the gate passes;
it never skips the gate to stay automatic.

- **11.0 Read the voice rules first.** Before drafting anything public, read
`references/human-voice.md` in full and pull this repo's own last 5 to 6 merged
PR titles and bodies (`gh pr list --state merged --limit 10` or the
browser-intake equivalent). Your title, body, and any comments must match their
length, casing, and issue-link style. Generic templates lose to repo reality
every time.
- **11.1 Draft small.** Pick the template from `references/pr-template.md` by diff
size: tiny (1 to 2 sentences, no headers), small (3 to 6 sentences, no headers
unless the repo template forces them), medium (repo headers only). Never more
bullet lines than changed lines. When the text points at code, use a commit-pinned
permalink plus a short verbatim snippet per `references/permalink-evidence.md`.
Write in B2 casual English with at least one
contraction in anything over 2 sentences. Zero em dashes or en dashes as pauses,
zero bare `--` pauses in prose. Backticked flags like `--config` are
fine; English pauses are not.
- **11.2 Commit per `references/commit-discipline.md`.** Message per the project's own convention
(Conventional Commits - `fix: ...` / `feat: ...` - by default, unless step 5 turned up
something else). One logical change per commit, related files grouped: fix travels with
its test, docs travel with the behavior they describe. Single commit stays when the whole
fix is one idea; split into 2 to 3 commits only when parts deserve separate review.
Keep the subject to one thing, short, same casing as merged PRs. Never squash distinct
ideas into one commit to save time, never split one fix into micro-commits.
- **11.3 Run the Voice Gate self-check** from `references/human-voice.md` Rule 6
literally (banned-word grep, banned-phrase grep, dash grep, plus the eye checklist:
one-thing title, length matches diff, contraction present, proof line with real
command and result, `Closes #N` once for PR descriptions (skipped for replies and
comments unless closing an issue), no headers/checklists/emoji unless the repo
template demands them). Rewrite until every check passes. A failing draft does not
get pushed "and fixed later".
- **11.4 Confirm the git identity and signing first.** Check `git config --get user.name` /
`git config --get user.email` in this clone. It must resolve to the actual person
submitting the contribution, not a default identity a coding-agent install may have
set globally. If `git config --get commit.gpgsign` is enabled, preserve commit signing
cleanly without bypassing. If identity isn't clearly a real person's identity, stop and
ask rather than guessing or silently overwriting it.
- **11.5 Never add a "Co-authored-by," "Generated by," or similar signature crediting an AI tool
to the commit or PR body unless the project's own CONTRIBUTING.md or PR template
explicitly asks for that disclosure. If it does ask, answer it honestly - don't leave the
field blank or mark it false to get past a policy written specifically to catch that.
Absent an explicit ask, the commit should just read as the submitting contributor's own
work, because the review, testing, and judgment behind it were theirs.
- **11.6 Push and open the PR only after 11.0 to 11.3 pass.** Once step 10 passes and
the Voice Gate passes, push the local commit stack to the user's fork (the one confirmed
or created back in step 2) and open the PR without waiting for a further go-ahead - that's
what end-to-end automation means here. Push every local commit as is; do not squash and
do not force-push during review unless the maintainer explicitly asks. Draft the PR description from `references/pr-template.md`, filled
in with what actually changed, how it was tested, `Closes #<issue-number>` (or whatever
phrasing this project's own template used in step 5), and a mention of any stale/rejected
prior attempt from step 4 if one existed. The same gate covers every follow-up push and
every review reply or issue comment: re-run the self-check on the new text before posting.
If the gate still fails after three rewrites, stop and bring the draft to the user
instead of pushing it anyway.
- If `gh`/`glab` isn't authenticated, or the push fails for any other reason, say so
plainly and tell the user what to run (`gh auth login`, etc.) - never report a PR as
opened when it wasn't. This is the one place a fabricated link would actually mislead
someone, so treat it as a hard rule rather than a judgment call.
- The two exceptions that still stop and ask instead of proceeding: step 4 found an
existing PR that already resolves this (see step 4's branches), step 10 never
converged after three rounds, or the Voice Gate in 11.3 still fails after three
rewrites. A rejected voice draft never gets pushed to "fix later".

### 12. Hand off
Give CI a few minutes and check it once (`gh pr checks --watch` or the platform
equivalent) before calling this done - not to babysit it through days of human review, but
because a red build from something the local run in step 9 couldn't catch (a CI-only lint
rule, an OS or version you don't have locally) is worth one honest look, and one new
follow-up commit on the same branch if the fix is quick, rather than leaving the user to
discover it later. Never amend an already pushed commit to hide the fix. If it's
still red after that look, or just slow to start, don't loop on it - note the status in
the summary and move on.

One short summary: what the issue was, what changed, what was tested, and the branch/PR
link. Don't re-paste the whole diff - the user just watched it happen.

## Constraints

These keep your PR mergeable. They guard review time, not just code.

- **Do NOT proceed without rendered issue intake** (`references/issue-intake.md`). Attempt a rendered read first, every run. A raw CLI dump is a complement, never a substitute.
- **Do NOT bypass the Human Voice Gate** (`references/human-voice.md`). Zero banned AI buzzwords, zero em dashes, zero en dashes as prose pauses, and zero speculative fluff.
- **Do NOT interrupt the user for routine decisions.** File naming, helper extraction, and test placement are your responsibility. Pause ONLY at the explicit checkpoints.
- **Do NOT open competing PRs** if step 4 finds an existing active or merged PR that resolves the problem.
- **Do NOT cite a bare `path:line` on the default branch in public text** (`references/permalink-evidence.md`). Pin it to a commit SHA and quote the lines verbatim, after verifying the SHA exists.
- **Do NOT push unverified code.** Always execute the project's actual build, lint, and test suites (`references/ecosystem-detection.md`) before pushing. Verify each local commit per `references/commit-discipline.md` section 4.
- **Do NOT dump unrelated work into one commit or split one fix into micro-commits** (`references/commit-discipline.md`). One logical change per commit, committed while you work. Single commit stays for tiny fixes.
- **Do NOT amend or force-push after publishing.** Review-round and CI fixes are new commits on the same branch. Squash only when the maintainer explicitly asks.
- **Do NOT add AI disclosure signatures** ("Co-authored-by: AI", "Generated by...") unless the target repository's `CONTRIBUTING.md` or PR template explicitly mandates it.
- **Do NOT guess git author identity.** Always verify `git config user.name` and `user.email` represent the authentic contributor before committing.
- **Do NOT touch or stash uncommitted changes** in the user's local clone without explicit confirmation.
- **Done means:** tests and lint pass locally, one new or updated test covers the fix, commit stack follows `references/commit-discipline.md` (related work grouped, each commit verified), Voice Gate Rule 6 passes, PR links `Closes #N` once, CI gets one check in step 12.

## Checkpoints (the only points that stop and ask)

Pre-flight safety gates:

- Uncommitted local changes found in step 2 -> ask, don't stash.
- No local clone found -> ask before cloning, and confirm the path.
- Git identity in step 11 isn't clearly the real submitter -> ask, don't guess.

Integrity gates (auto-retry 3x, ask only on failure):

- Browser intake gate fails (no browser tool, page won't render, auth wall, visuals or external repro link unreadable) -> stop and resolve before any code work.
  Never silently downgrade to a gh-only read to stay moving.
- Voice Gate in step 11 still fails after three rewrites -> stop and show the draft to the
  user instead of pushing it anyway.

Stop-work gates:

- Step 4 finds an existing merged/strong-open PR that already resolves the issue -> stop
  and tell the user instead of opening a competing one.
- Step 10's review doesn't converge after three rounds -> stop and flag instead of pushing
  anyway.

Everything else - reading files, running `/multi-agents`,
running tests, iterating on the diff, committing, pushing, and opening the PR - proceeds
straight through without asking, by design. The browser intake gate and the Voice
Gate are part of "straight through": they run every time, they just don't ask, they
complete (intake artifact exists / voice self-check passes) before moving on.

## Scaling the agent brief
The three-role default fits most single-issue contributions. Adjust only when the issue
genuinely calls for it:
- **Trivial fix** (typo, one-line logic bug, clear repro) - merge Analyst and Researcher
  into one role; go straight to a light review.
- **Cross-cutting or multi-file feature** - add a fourth **Docs/Changelog Agent** (or hand
  this to the `documentation` skill directly) so README/CHANGELOG/API-doc updates aren't
  an afterthought.
- **Continuing someone else's PR** (not a fresh issue) - swap Root-Cause Analyst for a
  **PR State Analyst**: what's already done, what review feedback is still unresolved.
- **A stale/rejected prior attempt turned up in step 4** - give the Root-Cause Analyst that
  attempt's rejection reasoning up front so the new pass doesn't re-propose the same thing.

Three well-briefed agents beat five thin ones - only add roles the issue actually needs.

## Works with any project, any language
Nothing above is specific to any one repo, host, or language. Step 1 detects the host,
step 5 detects the project's conventions, and `references/ecosystem-detection.md` detects
the toolchain. Step 4's sibling-repo awareness means it also isn't limited to looking in
just the one repo the issue happened to be filed in. The pipeline shape is the only fixed
part; everything else is discovered fresh on every run.

## Examples

### Example 1 - Straightforward fix, no checkpoints hit
> "Here's the next one: `https://github.com/expressjs/express/issues/1234`. Repo's in
> contributions/."

1. Parses the URL; finds `~/contributions/express` already cloned with `origin` = fork,
   `upstream` = expressjs/express; syncs `main`.
2. Runs the blocking intake in browser intake - full thread, linked-PR sidebar empty,
   one attached screenshot opened at full size confirming the null-route stack, no
   external repro link; writes the intake artifact. A maintainer comment points at
   the null check in `lib/router/route.js`; no prior attempts.
3. Checks `CONTRIBUTING.md` and the lint config, branches `fix/1234-route-null-check`.
4. Runs the three-role brief: Root-Cause Analyst lands on `route.js:38`, Researcher points
   at the existing test pattern in `test/Route.js`.
5. Implements the guard, adds a test, runs the suite and linter, sends the diff through the
   Reviewer role - approved on the first pass.
6. Commits the fix plus its test as one local commit (single idea, so no split),
   pushes to the fork, opens the PR from the template, watches CI turn green, and
   hands off with a three-line summary and the PR link.

Every decision here, from branch name to commit message, was already answered by the
brief and the project's own conventions - nothing needed a check-in.

### Example 2 - Duplicate work found, checkpoint hit
> "Pick up `https://gitlab.com/some-org/some-app/-/issues/88`."

1. Locates and syncs the clone, opens the issue.
2. Step 4 turns up an open, approved MR (`!142`) that already closes it, just awaiting
   merge.
3. Stops: "Issue #88 already has an approved, unmerged MR (!142) that closes it - want me
   to review/improve that one instead, or move to a different issue?"

Opening a second PR here would hand the maintainer two competing fixes to reconcile - this
is exactly what the checkpoint exists for, not a failure of nerve elsewhere in the pipeline.

### Example 3 - Thin issue, /multi-agents unavailable, agent adapts
> "start this issue: `https://github.com/foo/cli-tool/issues/9` - contributions/"

1. The issue is one line - "crashes on --verbose" - no repro, no comments. The
   blocking intake still runs in browser intake: full thread scrolled to footer,
   `VISUALS: NONE - verified rendered`, external links NONE - recorded in the intake artifact as gaps.
2. `/multi-agents` isn't installed here. Rather than stalling, works the brief solo:
   reproduces the crash first (Analyst hat), traces it to an unguarded `.split()` on
   undefined output, then switches to the Researcher hat to find the existing
   flag-parsing tests.
3. Implements the fix and a regression test, runs the suite.
4. Reviews its own diff wearing the Reviewer hat as if it were someone else's PR, catches
   that `--verbose --json` together still crashes, and fixes that too before moving on.
5. Opens the PR, noting that the original issue was thin and the repro was reconstructed
   from the stack trace, so a maintainer can sanity-check the interpretation.

Adapting to what's actually available beats stalling to ask the user to install something
they may not know they're missing.

## Reference files

- `references/commit-discipline.md` - commit-while-you-work protocol for steps 8-11:
  one logical change per commit, when one commit is enough versus 2 to 3, staging and
  message format, no amend or force-push after publishing. Read before the first code change.
- `references/issue-intake.md` - BLOCKING intake protocol for steps 3-4: how to drive
  browser intake (task space, full-thread scroll, visual-asset handling, external-URL
  handling), the intake artifact shape, and the stop-conditions. Read before opening
  the issue URL. No intake artifact, no code.
- `references/human-voice.md` - BLOCKING for *any* public-facing text (issue comment,
  PR description, merge request comment, review reply, status update). Read it before
  drafting, match this repo's own merged PRs, write in B2 casual English, and run its
  Rule 6 self-check until it passes. Do not push or post while it fails. This is what
  keeps the contribution from being closed on sight as generated text.
- `references/multi-agent-brief.md` - exact brief template + worked example for step 7,
  including where step 4's related-work findings go.
- `references/ecosystem-detection.md` - language/build-tool detection and command lookup
  for steps 5 and 9.
- `references/jev-decisions.md` - optional Jev calibrated gates for steps 4, 7, 10:
  typed questions, thresholds, provider priority, and the decision-log learning loop.
- `references/pr-template.md` - PR description template for step 11.
- `references/permalink-evidence.md` - commit-pinned permalink protocol for every
  code citation in public text (steps 10-11): how to build the link, the snippet
  format, and the SHA check. Bare `path:line` drifts; permalinks do not.
