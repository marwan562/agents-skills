# Pull Request Description Template

This template is used in **Step 11** of the `contribute` pipeline to automatically compose high-quality, maintainer-friendly PR descriptions.

---

## Template

```markdown
## Summary
<!-- Concise 1-2 sentence description of what problem this PR solves and the high-level approach -->

## Root Cause / Motivation
<!-- Briefly explain why the previous behavior occurred or why this feature is needed -->

## Changes
- <!-- Specific file / module changes -->
- <!-- New helper functions or refactored components -->
- <!-- Added / updated test cases -->

## Testing & Verification
- [x] Local test suite executed and passing (`<test command executed>`)
- [x] Linters and formatters passed (`<lint command executed>`)
- [x] Added unit/regression tests covering the new behavior

## Related Work & Prior Art
<!-- Mention any related issues, sibling PRs, or rejected prior attempts if found in Step 4 -->
- Closes #<issue-number>
```
