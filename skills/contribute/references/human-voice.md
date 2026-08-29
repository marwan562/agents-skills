# Writing like the person who actually did the work

A maintainer who rejects a PR for reading as AI-generated usually isn't wrong about what
generated it - they're reacting to a real, learnable pattern. This file is what to avoid
and, more usefully, what to do instead: match the specific project's own voice rather than
aiming at a generic "sound human" target.

## Why this matters more than it seems like it should

"Comprehensive" in a PR title is a known joke in maintainer circles for a reason: it's one
of a small set of words that shows up constantly in generated text and almost never in
a PR someone wrote about their own two-line fix. Once a maintainer has seen the pattern a
few times, they stop reading for content and just close on sight - which means the code
quality underneath stops mattering. This file exists to keep that from ever being the
reason a contribution gets closed.

## Words and phrases that read as generated, regardless of context

Avoid these outright, or replace with the plainer word in parentheses:

comprehensive, robust, seamless(ly), leverage (use), utilize (use), delve into (look at),
streamline(d), enhance(d) (improve), ensure(s) that, in order to (to), a myriad of / a
plethora of / numerous / various, "this PR aims to", "I've made the following changes",
"please let me know if you have any questions or feedback", "feel free to", "note that",
"it's worth noting that", "furthermore" / "moreover" / "additionally" as a sentence opener,
"not only X but also Y".

Also avoid: an em dash used for dramatic pause where a comma or period would do, and
stacking three adjectives before a noun ("a comprehensive, robust, and scalable solution").

## Structural patterns that read as generated

- **A title trying to summarize everything.** "feat: Add comprehensive support for X with
  enhanced Y and improved Z" is three PRs pretending to be one title. A human title names
  the one thing that changed: "fix: error on missing --config instead of silent exit".
- **Full headers (`## Summary` / `## Changes` / `## Testing` / `## Checklist`) applied to
  every PR regardless of size.** Nobody writes four headers for a one-line fix. Use
  headers only when the project's own PR template has them - and even then, fill them with
  plain sentences, not more sub-bullets than the diff has lines.
- **A parallel bullet list where every line opens with the same past-tense verb** (Added,
  Fixed, Improved, Updated, Enhanced) - restates the diff instead of explaining the part
  the diff can't show: why.
- **Zero contractions, zero informality, ever.** Real engineers write "doesn't", "it's",
  "here's" in PR text. All-formal-register text with perfect grammar throughout a whole
  description is itself a tell.
- **An upbeat, generic closing line** - "Let me know if you have any questions!" on a PR
  nobody asked to be walked through.
- **Emoji as section decoration** (✨ 🚀 ✅ 🎉) in a plain bugfix PR.

## The one technique that actually works: read the room first

Before writing a title, description, or comment, pull this exact repo's own recent merged
PRs - `gh pr list --state merged --limit 10` (or the `/ego-browser` equivalent) - and
actually read five or six of them. Match:

- **Length.** Most real PRs for a small fix are one to three sentences. Match that instead
  of defaulting to a template that wants five sections.
  Terse repos want two sentences and a benchmark number, not a runthrough of "the following
  files were changed."
- **Casing and format convention.** Does this project actually use Conventional Commits, or
  do maintainers just write plain sentences as titles? Follow what's already there, not a
  generic style guide.
- **What they explain vs. what they leave to the diff.** Most human PR text explains *why*
  and *what it looked like from the outside* (a repro, a symptom, a decision) and trusts the
  reviewer to read the diff for *what* changed line by line.
- **How they reference the issue.** Some repos say "Closes #123", some just say "fixes the
  crash from #123", some don't reference it explicitly in prose at all because it's linked
  automatically. Match what's actually there.

This single step - reading five real examples from the same repo - does more than any
list of banned words, because "human-sounding" isn't one register; it's whatever that
project's actual contributors already sound like.

## Before / after

**Title**
- Generated: "fix: Implement comprehensive validation for missing required CLI flags with
  enhanced error handling"
- Human: "fix: error instead of silently exiting when a required flag is missing"

**Description (a small fix)**
- Generated:
  ```
  ## Summary
  This PR implements a comprehensive fix for the CLI's flag validation logic, ensuring
  robust error handling when required flags are omitted.

  ## Changes
  - Added validation check for required flags
  - Enhanced error messaging
  - Improved test coverage

  ## Testing
  - Ran the full test suite
  - Added new unit tests

  ## Checklist
  - [x] Tests added
  - [x] Lint passes
  - [x] Documentation updated
  ```
- Human:
  ```
  Running the CLI without --config used to just exit 0 with no output instead of erroring.
  This makes it print a usage error and return a non-zero exit code, matching what --help
  already documents. Added a table-driven case alongside the existing ones in
  cmd/root_test.go.

  Closes #241
  ```

**Issue comment**
- Generated: "Thanks for reporting this! I've conducted a comprehensive investigation and
  successfully identified the root cause of this issue."
- Human: "Reproduced it - the flag parser only checks that a value was passed, not that
  it's non-empty, so `--config ''` slips through. Working on a fix."

## What not to compromise on for the sake of sounding casual

Tone is the only thing being adjusted here. Keep every one of these exactly as rigorous as
before:
- Accuracy about what was actually tested and how.
- A real reference to the issue/PR number.
- Calling out a known limitation or partial fix instead of implying full coverage.
- Crediting a prior attempt (per the contribute skill's step 4) if one exists - a
  maintainer who remembers it will notice either way.

Sounding like a person means writing plainly and specifically about real work, not writing
less carefully.