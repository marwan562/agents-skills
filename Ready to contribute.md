---
title: Ready to contribute
tags:
  - opensource
  - contribute
  - todo
created: 2026-08-24
status: ready
priority: high
---

# Ready to contribute

> **Verified:** 2026-08-24 via `gh search issues --repo <repo> --state open --no-assignee` + `gh issue view <url> --json assignees,comments,labels`
> **Filter:** `no assignee` • `state:open` • `<3 comments` • no `pr-opened` label • no linked PR • no "I will work on it" comment
> **Total scanned:** 9 repos × 100+ unassigned open issues each
> **How to use:** Check `- [x]` when you claim an issue. Run `/contribute <URL>` to start the pipeline.

## 🔥 Top 5 — Start Here (highest impact, truly free)

- [ ] [immich#30933 — Stale untracked integrity report can delete now-tracked original file](https://github.com/immich-app/immich/issues/30933) `immich` | comments:0 | labels:`—` | **CRITICAL data loss** — stale `untracked_file` report deletes file after it becomes asset's original. Delete path not re-validated. ` #ready #bug`
- [ ] [helm#32565 — Regression v4.2.0: `helm template` adds blank line before each `---`](https://github.com/helm/helm/issues/32565) `helm` | comments:1 | **clear regress**, stdout adds extra newline per doc, not `--output-dir` ` #ready #bug`
- [ ] [immich#30914 — ML text encoder UnicodeDecodeError on non-ASCII tokenizer_config.json](https://github.com/immich-app/immich/issues/30914) `immich` | comments:1 | `machine-learning/immich_ml/models/clip/textual.py:61` → `Path.open()` without `encoding="utf-8"` ` #ready #bug #good-first`
- [ ] [kubernetes#141353 — ValidateWebhookService arg order swapped (name, namespace)](https://github.com/kubernetes/kubernetes/issues/141353) `kubernetes` | comments:2 | `kind/bug needs-triage` — causes mislabeled validation errors ` #ready #bug`
- [ ] [immich#30824 — Failed DB backup leaks pg_dump conn holding AccessShareLock](https://github.com/immich-app/immich/issues/30824) `immich` | comments:0 | `DatabaseBackupService` spawns `pg_dump` before opening output file, `ENOENT` leak = `idle in transaction` forever ` #ready #bug`

## 🟩 Immich — Best repo for contributors (0–1 comments, well-described)

- [ ] [immich#30933 — Stale untracked can delete original — data loss](https://github.com/immich-app/immich/issues/30933) | 2026-08-23 | comments:0
- [ ] [immich#30949 — Archived photo remains in timeline & Photo Viewer nav](https://github.com/immich-app/immich/issues/30949) | 2026-08-23 | comments:0 | Web timeline not refreshed after archive ` #ui`
- [ ] [immich#30935 — Duplicate videos not surfacing](https://github.com/immich-app/immich/issues/30935) | 2026-08-23 | comments:0
- [ ] [immich#30914 — ML UnicodeDecodeError (see Top 5)](https://github.com/immich-app/immich/issues/30914) | 2026-08-21 | comments:1
- [ ] [immich#30857 — iOS stale token from deleted session overwrites live token](https://github.com/immich-app/immich/issues/30857) | 2026-08-19 | comments:0 ` #mobile`
- [ ] [immich#30824 — pg_dump leak (see Top 5)](https://github.com/immich-app/immich/issues/30824) | 2026-08-17 | comments:0
- [ ] [immich#30829 — Photospheres from Microsoft ICE shown as 2D](https://github.com/immich-app/immich/issues/30829) | 2026-08-17 | comments:0
- [ ] [immich#30931 — Closing mobile app kills api worker `read ECONNRESET`](https://github.com/immich-app/immich/issues/30931) | 2026-08-22 | comments:1
- [ ] [immich#30911 — Timeline keyboard scrolling stops after asset open/back](https://github.com/immich-app/immich/issues/30911) | 2026-08-21 | comments:0

## ⛵ Helm

- [ ] [helm#32565 — helm template blank line regress (Top 5)](https://github.com/helm/helm/issues/32565) | 2026-08-21 | comments:1
- [ ] [helm#32546 — `helm pull --verify` fails when repo name ≠ chart name](https://github.com/helm/helm/issues/32546) | 2026-08-15 | comments:1
- [ ] [helm#32541 — helm plugin install fails on OCI Image Index tag](https://github.com/helm/helm/issues/32541) | 2026-08-14 | comments:0
- [ ] [helm#32539 — helm pull returns arbitrary chart on OCI Image Index](https://github.com/helm/helm/issues/32539) | 2026-08-14 | comments:1
- [ ] [helm#32532 — Concurrent goroutine dependency builds race on tmpcharts-<pid>](https://github.com/helm/helm/issues/32532) | 2026-08-12 | comments:0
- [ ] [helm#32559 — Add Helm design philosophy to AGENTS.md](https://github.com/helm/helm/issues/32559) | 2026-08-18 | comments:0 ` #docs`

> ⚠️ `helm#32567 provenance multi-block armored keyrings` **EXCLUDED** — 2 people already claimed in comments. Has `help wanted` but contested.

## ☸️ Kubernetes

- [ ] [kubernetes#141353 — ValidateWebhookService arg order swapped (Top 5)](https://github.com/kubernetes/kubernetes/issues/141353) | 2026-08-13 | `kind/bug needs-sig needs-triage` | comments:2
- [ ] [kubernetes#141339 — PodTopologySpread empty `{}` labelSelector is no-op](https://github.com/kubernetes/kubernetes/issues/141339) | 2026-08-12 | `kind/bug sig/scheduling needs-triage` | comments:2 | `pkg/scheduler/framework/plugins/podtopologyspread/common.go` `countPodsMatchSelector`
- [ ] [kubernetes#141513 — macOS client releases not signed](https://github.com/kubernetes/kubernetes/issues/141513) | 2026-08-21 | `kind/feature needs-sig needs-triage` | comments:2
- [ ] [kubernetes#141498 — Remove dependency to pkg/controller/volume/persistentvolume/testing](https://github.com/kubernetes/kubernetes/issues/141498) | 2026-08-20 | `sig/scheduling needs-triage` | comments:2
- [ ] [kubernetes#141367 — ValidatingAdmissionPolicy can deny while CRD params sync after restart](https://github.com/kubernetes/kubernetes/issues/141367) | 2026-08-14 | `kind/bug sig/api-machinery needs-triage` | comments:1

## 📊 Prometheus

- [ ] [prometheus#19395 — scrape: response body copied 2nd time on large target](https://github.com/prometheus/prometheus/issues/19395) | 2026-08-12 | comments:1 ` #perf`
- [ ] [prometheus#19397 — tsdb: avoid retaining unbounded OOO record buffers in bytesPool](https://github.com/prometheus/prometheus/issues/19397) | 2026-08-12 | comments:2
- [ ] [prometheus#19206 — promql/parser incorrect pos for duration/0](https://github.com/prometheus/prometheus/issues/19206) | 2026-07-15 | comments:1 | `// FIXME: this position looks wrong.` in `promql/parser/parse_test.go`
- [ ] [prometheus#19426 — promtool no tool to find inconsistent classic histograms in TSDB](https://github.com/prometheus/prometheus/issues/19426) | 2026-08-15 | comments:1
- [ ] [prometheus#19273 — docs: clamp_max/min NaN behaviour not documented](https://github.com/prometheus/prometheus/issues/19273) | 2026-07-27 | comments:0 ` #docs`
- [ ] [prometheus#19345 — Promtool recording rule block generation should support 24hr blocks](https://github.com/prometheus/prometheus/issues/19345) | 2026-08-06 | comments:2

> ⚠️ `prometheus#19445 deadlock stripeSeries` **EXCLUDED** — 2 open PRs `#19448` `#19460` already fix it.

## 🦀 Tauri

- [ ] [tauri#15910 — Android AAB compiles first Rust target twice](https://github.com/tauri-apps/tauri/issues/15910) | 2026-08-23 | comments:0
- [ ] [tauri#15909 — [feat] Expose whether menu event came from accelerator](https://github.com/tauri-apps/tauri/issues/15909) | 2026-08-23 | comments:0 ` #feat`
- [ ] [tauri#15903 — get_focused_window always None, is_focused true for many](https://github.com/tauri-apps/tauri/issues/15903) | 2026-08-21 | `type:bug status:needs triage` | comments:0
- [ ] [tauri#15905 — CEF: enumerateDevices shows redacted device list](https://github.com/tauri-apps/tauri/issues/15905) | 2026-08-21 | `type:bug scope:cef` | comments:0
- [ ] [tauri#15872 — on_new_window never fires for target=_blank (Win/WebView2)](https://github.com/tauri-apps/tauri/issues/15872) | 2026-08-13 | `type:bug status:needs triage` | comments:1
- [ ] [tauri#15892 — RUSTSEC-2026-0258: h2 unbounded empty DATA frames](https://github.com/tauri-apps/tauri/issues/15892) | 2026-08-19 | comments:0 ` #security`

## 🟣 Supabase

- [ ] [supabase#49426 — Preview branches don't preserve object privileges](https://github.com/supabase/supabase/issues/49426) | 2026-08-22 | `branching external-issue` | comments:0
- [ ] [supabase#49310 — Branching webhook 401s cross-project Edge Function](https://github.com/supabase/supabase/issues/49310) | 2026-08-20 | `bug branching external-issue` | comments:1
- [ ] [supabase#49437 — Next.js SSR not loading on MacOS](https://github.com/supabase/supabase/issues/49437) | 2026-08-23 | `bug awaiting-details` | comments:1
- [ ] [supabase#49106 — RLS INSERT rejects provably-matching auth.uid()](https://github.com/supabase/supabase/issues/49106) | 2026-08-14 | `bug awaiting-details` | comments:1
- [ ] [supabase#49185 — Update MessageBird verification Docs](https://github.com/supabase/supabase/issues/49185) | 2026-08-18 | `documentation external-issue` | comments:1 ` #docs`
- [ ] [supabase#49230 — Rewriting file same name not updating with upsert:true](https://github.com/supabase/supabase/issues/49230) | 2026-08-19 | `bug storage` | comments:1

> ⚠️ 7 Supabase issues with `pr-opened` label excluded (someone already opened PR, e.g. #49435, #49427, #49338, #49142).

## 🔷 Appwrite

- [ ] [appwrite#13311 — live.com rewritten to outlook.com can't be changed](https://github.com/appwrite/appwrite/issues/13311) | 2026-08-22 | comments:0
- [ ] [appwrite#13308 — OAuth Missing redirect URL](https://github.com/appwrite/appwrite/issues/13308) | 2026-08-21 | comments:0
- [ ] [appwrite#13291 — Presence upsert invisible for console-session](https://github.com/appwrite/appwrite/issues/13291) | 2026-08-20 | comments:0 ` #bug`
- [ ] [appwrite#13264 — Sites static runtime crash-loop helpers/server.sh: No such file](https://github.com/appwrite/appwrite/issues/13264) | 2026-08-18 | comments:0
- [ ] [appwrite#13084 — MongoDB adapter _uid misses collation → COLLSCAN](https://github.com/appwrite/appwrite/issues/13084) | 2026-08-03 | comments:1 ` #perf`
- [ ] [appwrite#13100 — Refactor v2 DB metadata schema to async worker](https://github.com/appwrite/appwrite/issues/13100) | 2026-08-04 | comments:2 ` #refactor`

## ✈️ Airbyte

- [ ] [airbyte#84884 — source-s3 bare hostname vs https prefix botocore rejects](https://github.com/airbytehq/airbyte/issues/84884) | 2026-08-18 | `type/bug needs-triage` | comments:3
- [ ] [airbyte#84400 — source-snowflake incremental drops rows in sub-microsecond rounding gap #82705](https://github.com/airbytehq/airbyte/issues/84400) | 2026-08-14 | comments:2
- [ ] [airbyte#84453 — Orchestrator Resource Settings not applied to MySQL CDC](https://github.com/airbytehq/airbyte/issues/84453) | 2026-08-17 | `type/bug area/platform` | comments:3
- [ ] [airbyte#84351 — Build tooling should validate base image has `airbyte` user](https://github.com/airbytehq/airbyte/issues/84351) | 2026-08-13 | comments:2
- [ ] [airbyte#84403 — Support brotli compression in Azure Blob source](https://github.com/airbytehq/airbyte/issues/84403) | 2026-08-14 | comments:2 ` #feat`

## 💻 VS Code — Use with caution

> Most `no-assignee` results are `testplan-item` (internal QA) or `info-needed`. Prefer `good first issue` label.

- [ ] [vscode#229280 — setting to wrap absolute path Copy Path with quotes](https://github.com/microsoft/vscode/issues/229280) | `good first issue` candidate | comments:—
- [ ] [vscode#199953 — Aux window should change cursor in dropping area](https://github.com/microsoft/vscode/issues/199953) | comments:—
- [ ] [vscode#252667 — Update GitHub Issue Notebooks due to query breaking change](https://github.com/microsoft/vscode/issues/252667) | comments:—

## 🌱 Good First Issue — Also unassigned (easy entry)

- [ ] [immich#28832 — Prefer null over empty strings](https://github.com/immich-app/immich/issues/28832) `good first issue` | comments:5
- [ ] [immich#28709 — "already in..." toast misleading](https://github.com/immich-app/immich/issues/28709) `good first issue 📱mobile` | comments:5
- [ ] [helm#30787 — Display OCI annotations in helm show chart](https://github.com/helm/helm/issues/30787) `help wanted good first issue` | comments:5
- [ ] [airbyte#52676 — update sentry client in airbyte-ci](https://github.com/airbytehq/airbyte/issues/52676) `good first issue` | comments:—
- [ ] [supabase#6435 — Allow newlines in SMS OTP template](https://github.com/supabase/supabase/issues/6435) `enhancement good first issue` | comments:—
- [ ] [kubernetes#132195 — API can streamline: assume same key for EnvVarSource](https://github.com/kubernetes/kubernetes/issues/132195) `kind/feature` | comments:—

---

## 📋 Workflow

1. Pick one unchecked item above
2. Comment on GitHub: `I'd like to work on this`
3. Run in this vault: `/contribute https://github.com/<owner>/<repo>/issues/<number>`
4. The universal pipeline will: `parse link → sync clone → read issue via gh → check prior PRs → learn conventions → multi-agents → implement → code-review → push → PR`

## 🔍 Re-run search anytime

```bash
gh search issues --repo immich-app/immich --state open --no-assignee --limit 30 --json number,title,url,commentsCount
gh search issues --repo helm/helm --state open --no-assignee --limit 10 --json number,title,url,labels
gh search issues --repo kubernetes/kubernetes --state open --no-assignee --label "help wanted" --limit 10
```

---
*Generated by `agents-skills` unified /contribute workflow — 2026-08-24* • *Vault: `Documents/Obsidian Vault/Ready to contribute.md`*
