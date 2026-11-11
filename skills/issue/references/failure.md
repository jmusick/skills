# The failure path

Read this when an issue can't be finished. Leave the work where the user can pick it up:

- **Uncommitted work in the checkout** (the default mode) that's worth keeping: move it to a branch and a draft PR, so the default branch stays clean and `/issue N` can resume it as `--branch`. Undo any version bump first; a later run redoes it from fresh tags.

  ```bash
  git switch -c issue-N-<short-slug>
  git add -A
  git commit -m "<Imperative subject> (#N, unfinished)"
  git push -u origin issue-N-<short-slug>
  gh pr create --draft --base <default> --title "<imperative title>" --body-file <file>
  git switch <default>
  ```

  The body says `Closes #N`, what's done, what's blocking, and the next step. Then comment on the issue as for an existing PR, below.
- **A PR exists:** comment with what's done, what's blocking, and the next step, and leave the issue assigned. `/issue N` resumes it later. Mark it draft (`gh pr ready <pr> --undo`) unless the only blocker is a missing review: a draft tells reviewers it isn't ready, so leave that one ready for review.
- **Commits but no PR** (`--branch`): push, open a draft PR so the work is visible, and comment on it as above.
- **Nothing pushed** (nothing written yet, or the user discarded it): unassign yourself if the run claimed it (`gh issue edit N --remove-assignee @me`) and comment with what you learned and what's needed. End the comment with the line `<!-- agent-waiting-for-reply -->`: it's invisible on GitHub, and the survey skips the issue until someone replies, so `/loop /issue` doesn't retry it every round. With `--branch`, remove the worktree and delete the local branch; nothing on them is worth keeping.
- **Committed and tagged but not pushed** (the default mode): say so first in the report, with the exact push commands from step 9.
- Otherwise, with `--branch`, clean up the worktree as in branch.md's step 10 once everything is pushed, and keep the branch.
- **Merged but not tagged** (`--branch`): say so first in the report, with the merge SHA and the exact `git tag` and `git push` commands from branch.md's step 9c.

Then write the report (step 11), leading with where it stopped.
