# The failure path

Read this when an issue can't be finished. Leave the work where the user can pick it up:

- **A PR exists:** comment with what's done, what's blocking, and the next step, and leave the issue assigned. `/issue N` resumes it later. Mark it draft (`gh pr ready <pr> --undo`) unless the only blocker is a missing review: a draft tells reviewers it isn't ready, so leave that one ready for review.
- **Commits but no PR:** push, open a draft PR so the work is visible, and comment on it as above.
- **Nothing pushed** (nothing written yet, or the user discarded it): unassign yourself (`gh issue edit N --remove-assignee @me`) and comment with what you learned and what's needed. End the comment with the line `<!-- agent-waiting-for-reply -->`: it's invisible on GitHub, and the survey skips the issue until someone replies, so `/loop /issue` doesn't retry it every round. Remove the worktree and delete the local branch; nothing on them is worth keeping.
- Otherwise clean up the worktree as in step 12 once everything is pushed, and keep the branch.
- **Merged but not tagged:** say so first in the report, with the merge SHA and the exact `git tag` and `git push` commands from step 11.

Then write the report (step 13), leading with where it stopped.
