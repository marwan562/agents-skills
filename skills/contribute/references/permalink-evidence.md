# Permalink Evidence

Use a commit-pinned permalink every time you point at code in public text:
issue bodies, review comments, PR descriptions, and follow-up replies.
A bare `path:line` on the default branch drifts as the file changes.
A permalink does not.

## When to use it

- Citing the root cause in a new issue body.
- Quoting the exact lines a review finding refers to.
- Pointing at prior art or a stale attempt in step 4.
- Any `file:line` that a maintainer must open to verify your claim.

Internal reasoning and subagent briefs can keep bare `path:line`.
Anything a human clicks must be a permalink.

## How to build one (GitHub)

1. Open the file on the default branch.
2. Click the first line number, shift-click the last one to select the range.
3. Press `y`. GitHub rewrites the URL to the exact commit SHA.
4. Copy the result. It looks like this:

```
https://github.com/<owner>/<repo>/blob/<40-char-sha>/path/to/file.go#L291-L305
```

GitLab: open the file, select the range, use the link icon to copy a
commit-pinned URL (`/-/blob/<sha>/...#L291-305`).
Gitea: same flow, copy the URL after selecting the range and pinning
to the commit.

## Snippet format

Paste the link, then quote the lines in a fenced block so the claim
reads without a click. Name the language for highlighting.
Keep the first comment line as the source of truth:

````markdown
https://github.com/<owner>/<repo>/blob/<sha>/pkg/registry/core/pod/storage/eviction.go#L291-L305

```go
// pkg/registry/core/pod/storage/eviction.go (L291-L305, master @ <short-sha>)
deleteOptions := originalDeleteOptions
```
````

Quote the source verbatim, even if a comment inside it trips a
prose rule. The Voice Gate scans your prose, not quoted upstream code.
Never paraphrase the quoted lines. If the range is wrong, rebuild the
link instead of editing the quote.

## Rules

- One permalink per claim. Link the smallest range that proves it.
- Never link `master`, `main`, or `HEAD` in public text. Always a SHA.
- Verify the SHA exists (`gh api repos/<owner>/<repo>/commits/<sha>`)
  before posting. A dead link is worse than no link.
- Keep prose around the link short per `human-voice.md`. The link
  carries the evidence, so the sentence only needs the conclusion.
