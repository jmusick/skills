# Resuming an issue

Read this when the survey set `resume`: an earlier run left this issue's PR open (usually as a draft) on its branch. The run continues as `--branch`, so follow [branch.md](branch.md) too.

1. Skip the claim; the issue is already yours. Still size it (step 3).
2. Reuse the worktree if `git worktree list` shows one on that branch. Otherwise `git worktree add <path> <branch>` if the branch exists locally, or `git worktree add <path> -b <branch> origin/<branch>` if not, then set it up as branch.md's step 4 says (absolute path, dependencies, gitignored config).
3. Read the PR's comments and the issue's to learn where it stopped and what blocked it. If the blocker is still open (a decision nobody made, a review nobody gave), ask the user, or with `--no-test` stop and report it.
4. Continue from the first step not yet done: unreviewed work goes to step 6, untested work to step 7, a green PR to step 8 or 9b. Reread the diff either way.
