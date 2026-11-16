# Branch mode

Read this before step 1 of SKILL.md when the run uses `--branch`, a batch, or an unattended run whose checkout fails step 1's checks. Step numbers refer to SKILL.md.

The run never switches the user's branch or touches their checkout, so skip step 1's checkout checks (2 to 4).
- **Claim it** after sizing: `gh issue edit N --add-assignee @me`, then check the assignees. If someone else is also there, they took it meanwhile, so unassign yourself and pick again. Otherwise comment "Working on this now. A PR will follow."
- **Worktree:** `git fetch origin`, then `git worktree add ../<repo>-issue-N -b issue-N-<short-slug> origin/<default>`. Take its absolute path from `git worktree list` and use it for every edit and command, because the session still sits in the user's checkout and Windows paths don't match `/tmp` style. Install dependencies and copy the gitignored config the checks and app need (such as `.env`) from the user's checkout. Never commit those files, and say which you copied.
- **Review:** diff with `git -C <worktree> diff origin/<default>...HEAD` and give `/code-review` the branch as its target. Run `/update-docs` in the worktree. Test from the worktree, on another port if the user's server holds the default one.
- **Ship:** commit with the commit skill from the worktree, push with `-u`, and open the PR with `gh pr create`. Use the commit subject as the PR title, because a squash merge turns it into the commit release reads. Put `Closes #N`, a short summary, and how it was verified in the body. Wait on `gh pr checks <pr> --watch` in the background; on failure, read `gh run view <id> --log-failed`, fix, and push, at most twice. Don't merge: the user reviews and merges, then runs release from the default branch.
- **Clean up:** stop your dev server first (a running process can block removal on Windows), then `git worktree remove <path>`. Keep the branch, since the PR needs it.
