# Branch mode (`--branch`)

Read this before step 1 when the run uses `--branch`, works a batch, resumes a PR, or passes `--no-merge`. The issue is worked in its own worktree and ships through a PR: the squash merge carries the change and the version bump under the release subject `vX.Y.Z - <Summary>`, and the release tag points at it. Every step in SKILL.md applies except where this file changes it.

The run never switches the user's branch or touches their uncommitted work; all work happens in the worktree, and the only change to their checkout is step 10's fast-forward of `<default>`. So skip step 1's checkout checks: a dirty checkout is fine, and the user can keep working in it during the run.

If `required_approvals` is above 0, tell the user up front that the run will open the PR and then stop for someone else's review, since GitHub doesn't let a PR's author approve it, and carry on. If it's null, the branch is protected but its review rule couldn't be read; say merge may need a review. With `--no-test`, put this in the report instead.

## Step 3: Size it and claim it

Size it as step 3 says, then claim it so nobody else takes it:

```bash
gh issue edit N --add-assignee @me
gh issue view N --json assignees --jq '[.assignees[].login]'
gh issue comment N --body "Working on this now. A PR will follow."
```

If the assignees show someone besides you, another run or person took it between the survey and now: unassign yourself and pick again without commenting.

## Step 4: Set up a branch and worktree

```bash
git fetch origin
git worktree add ../<repo>-issue-N -b issue-N-<short-slug> origin/<default>
```

Use a three- or four-word slug from the title, such as `issue-42-fix-login-redirect`. Branching from `origin/<default>` keeps you independent of the user's local branch. If the path is taken by an earlier run's worktree, check `git worktree list`: reuse it if it's on an `issue-N-*` branch with nothing unpushed, otherwise pick another path and mention the old one in the report.

Take the worktree's absolute path from `git worktree list` and use it for every edit, command, and cleanup. Don't build it by hand: the session's working directory is still the user's checkout, so a relative path or bare `git` lands there, and on Windows `/tmp`-style paths don't match native ones.

A fresh worktree has no dependencies and none of the checkout's gitignored config, and step 5's checks need both. Install dependencies, and copy the gitignored config the checks and app need (such as `.env`) from the user's checkout. Never commit those files; tell the user which you copied.

## Steps 5 to 7: in the worktree

Do steps 5 to 7 in the worktree, with these changes:
- **Step 5:** commit the change with a short imperative subject that mentions #N.
- **Step 6:** read the diff with `git -C <worktree> diff origin/<default>...HEAD`, and give `/code-review` the branch as its target, e.g. `/code-review medium issue-42-fix-login-redirect`; without one it reviews the user's checkout. Tell `/update-docs` to work in `<worktree path>` (with `git -C <worktree>`) and to check only docs this branch's diff could have made wrong. Commit each round's fixes, and doc edits as `Update docs for #N`.
- **Step 7:** start the app from the worktree, on another port if the default is taken (often by the user's own server), and give the worktree path. Commit each fix round. Say plainly that nothing is pushed and their go releases it. On **Discard**, remove the worktree and delete the local branch instead of stashing. If an earlier run pushed this work (resuming), also close its PR (`gh pr close <pr> --delete-branch`), so the next `/issue N` doesn't resume it.

## Step 8: Bump the version on the PR branch

The bump goes in the PR so the squash merge is the release commit. Don't run `/patch` or `/minor`: they commit, tag, and push the branch they run on, making a second commit.

First bring the branch up to date, even if the rest of this step is skipped. The test pause can last hours, and if someone released meanwhile, a bump from the old base would disagree with the new tags:

```bash
git -C <worktree> fetch origin --tags
git -C <worktree> merge --no-edit origin/<default>
```

Never rebase or force-push. Where the merge conflicts on version lines or the changelog, keep `<default>`'s side of those lines, since the bump redoes them; in a lockfile, keep the branch's dependency changes too, or regenerate it with the package manager. If the merge brought anything in, rerun the checks. If it needed more than mechanical conflict resolution, show the user the result and ask for a fresh go.

Then continue step 8 after its fast-forward, running `version_info.py` from the worktree (`cd <worktree> && python ...`). Where it skips the version parts of step 9, here that means the release subject in 9b and all of 9c: merge as a plain squash with GitHub's default subject. Skip them for `--no-merge` too: the user merges later, so a bump could go stale; the follow-up is `/issue N`, which resumes the PR and ships it as one release commit.

Commit as `Bump version to X.Y.Z` (the squash hides this subject). With no version files and no changelog, there's nothing to commit; the subject and tag carry the version.

## Step 9: Ship through the PR

This replaces step 9.

### 9a. Open the PR and wait for CI

```bash
git -C <worktree> push -u origin <branch>
gh pr create --base <default> --head <branch> --title "<imperative title>" --body-file <file>
```

If the PR already exists (resuming), push to it and update its body (`gh pr edit <pr> --body-file <file>`) instead of creating one. If it's a draft, mark it ready (`gh pr ready <pr>`) once CI passes, since a draft can't be merged.

The body has `Closes #N`, a short summary, how you verified it (including the user's local-dev test, or that `--no-test` skipped it), the size with the model and effort used, and `Releases vX.Y.Z (patch)` or similar. Follow the user's or repo's attribution rules. Write the body file in a temp directory and delete it after.

Wait: `gh pr checks <pr> --watch --fail-fast`. CI often outlasts a foreground shell call's timeout, so run it in the background where your agent can and wait for it to finish; otherwise rerun it until nothing is pending. If it reports no checks but `.github/workflows/` exists, wait about 15 seconds and retry before concluding there's no CI. On failure, read `gh run view <run-id> --log-failed`, fix, and push. Stop after two attempts.

With `--no-merge`, stop here, remove only the worktree (`git worktree remove <worktree path>`, after stopping any dev server), and report. Keep the local and remote branch: the open PR needs them.

### 9b. Merge as the release commit

Confirm nobody released while CI ran:

```bash
git -C <worktree> fetch origin --tags
cd <worktree> && python <this skill's directory>/scripts/version_info.py --verify X.Y.Z --ref origin/<default>
```

If `ready_to_merge` is false (`problems` says why), redo step 8 from the merge, resolving its version-line conflicts as step 8 says, with the new version. Push, update the PR body's `Releases vX.Y.Z` line (`gh pr edit <pr> --body-file <file>`), and wait for CI again.

Squash-merge, pinning the head commit (`git -C <worktree> rev-parse HEAD`) so you merge exactly what was reviewed and tested:

```bash
gh pr merge <pr> --squash --match-head-commit <head sha> \
  --subject "vX.Y.Z - <Summary>" --body-file <file>
```

The body file (temp directory, deleted after) has a few sentences on the release and anything a future reader needs (checks passed, migrations), then `Closes #N via PR #<pr>.` No `Co-Authored-By`, "Generated with", or other AI attribution, whatever the attribution reminder says for PRs. `--body-file` also stops GitHub appending the squashed subjects.

If squash isn't allowed, use the first of `merge_methods` without the release subject, and put running `/patch` or `/minor` on `<default>` in the follow-up: it commits on the branch it runs on, and this run doesn't switch the user's checkout. Don't delete the branch yet (step 10 does). Never pass `--admin` or bypass a failing check. If the PR needs an approving review, it has to come from someone other than its author, and the PR was opened from the user's account: take the failure path and name getting that review as the follow-up.

Confirm the issue closed (`gh issue view N --json state`); if not, close it with a comment linking the PR.

### 9c. Tag the release

Tag the squash-merge commit by its SHA, from the worktree, so nothing switches or pulls in the user's checkout. Nothing is pushed to `<default>`, so branch protection doesn't interfere.

```bash
sha=$(gh pr view <pr> --json mergeCommit --jq .mergeCommit.oid)
git -C <worktree> fetch origin
cd <worktree> && python <this skill's directory>/scripts/version_info.py --verify X.Y.Z --ref "$sha"   # ready_to_tag must be true
git -C <worktree> tag -a vX.Y.Z "$sha" -m "vX.Y.Z - <Summary>"  # lightweight `git tag vX.Y.Z "$sha"` if tag_style is lightweight
git -C <worktree> push origin vX.Y.Z
```

If `ready_to_tag` is false, don't tag; report its `problems` with the fix as the follow-up. If the push is rejected, keep the local tag and put `git push origin vX.Y.Z` in the follow-up.

Don't wait for a deploy the merge starts, even to confirm it went live; mention it in the report, and the user can ask for a check later.

## Step 10: Clean up

Remove only what this run created. Stop any dev server first; a running process can hold files and block worktree removal, especially on Windows.

```bash
git worktree remove <worktree path>
git branch -D <branch>                   # -D because a squash merge leaves it looking unmerged
git push origin --delete <branch>        # skip if the repo auto-deleted it
git fetch --prune
```

Remove the worktree only once everything in it is pushed. Otherwise leave it and give its path in the report.

To bring the user's local `<default>` up to date, run `git fetch origin <default>:<default>` if their checkout isn't on `<default>` (git refuses to update a branch that is checked out, so this form can't be used when it is). If it is, run `git merge --ff-only origin/<default>` in the user's checkout, which leaves uncommitted files alone and refuses rather than overwrite them. If either refuses because their copy diverged or their changes conflict, leave it to them and say so in the report.
