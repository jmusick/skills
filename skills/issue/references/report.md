# The report

End every run with this report. The **Follow-up** section is required, since it tells the user what's theirs to do; write "None" if nothing is.

```
Shipped #42 - Fix login redirect after password reset
- Size: normal (two files, existing tests to follow); ran on sonnet at medium effort
- Tested by you in local dev; one fix round (the redirect dropped the query string)
- Committed on main after 1 review round as "v1.4.3 - Fix login redirect after password reset" (3f2a9c1), which closed #42
- Released v1.4.3 (patch): tagged 3f2a9c1 and pushed main and the tag; CI runs on the push

Follow-up
- None
```

With `--branch`, name the PR, its review rounds and CI, the merge commit the tag points at, and the worktree and branches cleaned up.

When the run stopped early, lead with that, and make each follow-up concrete: what to do, where, and what to run.

```
Stopped on #61 - Add CSV export (PR #63 open, waiting for review)
- Blocked: main requires an approving review before merge, and GitHub doesn't let a PR's author approve it

Follow-up
- Get PR #63 approved by another maintainer: https://github.com/owner/repo/pull/63 (it already bumps to v1.5.0)
- Then run `/issue 61`: it resumes the PR, merges it as the release commit, and tags it
```
