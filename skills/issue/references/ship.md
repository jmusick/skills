# Shipping: steps 8 to 11

Read this after the user's go at step 7 (or after review with `--no-test`). These steps bump the version in the PR, open it, merge it as the release commit, and tag it.

## 8. Bump the version on the PR branch

The bump goes in the PR so the squash merge is the release commit. Don't run `/patch` or `/minor`: they commit, tag, and push the branch they run on, making a second commit.

First bring the branch up to date, even if the rest of this step is skipped. The test pause can last hours, and if someone released meanwhile, a bump from the old base would disagree with the new tags:

```bash
git -C <worktree> fetch origin --tags
git -C <worktree> merge --no-edit origin/<default>
```

Never rebase or force-push. Where the merge conflicts on version lines or the changelog, keep `<default>`'s side of those lines, since the bump below redoes them; in a lockfile, keep the branch's dependency changes too, or regenerate it with the package manager. If the merge brought anything in, rerun the checks. If it needed more than mechanical conflict resolution, show the user the result and ask for a fresh go.

Skip the rest of this step, the release subject in step 10, and step 11 (merging as a plain squash with GitHub's default subject) if:
- `--no-ship` or `--no-merge` was passed. With `--no-merge` the user merges later, so a bump could go stale; the follow-up is `/issue N`, which resumes the PR and ships it as one release commit.
- `has_release_tags` is false. Ask before creating the repo's first tag.

Choose the bump:
- **Patch:** bug fixes, docs, chores, and tweaks that add nothing new for users.
- **Minor:** anything a user can now do that they couldn't before.
- **Breaking:** stop and ask; that's the user's call.

```bash
cd <worktree> && python <this skill's directory>/scripts/version_info.py <patch|minor>
```

It prints current and next version, `next_tag`, `tag_style`, version files with `in_lockstep` and an `update` hint, and the changelog path. Stop and ask if `versions_disagree` or `next_tag_exists_locally` is true. Then, in the worktree:
- Update every version file with `in_lockstep` true per its `update` hint. For `package.json`, run `npm version <X.Y.Z> --no-git-tag-version` (it updates the lockfile too) and check that only version lines changed. Leave independently versioned files alone and mention them in the report.
- If there's a changelog, add a section at the top in its exact format, with today's date, written for readers. Don't create one.
- Follow any release steps in the repo's AGENTS.md / CLAUDE.md.

Commit as `Bump version to X.Y.Z` (the squash hides this subject) and rerun checks if the bump touched something they read, such as a lockfile. With no version files and no changelog, there's nothing to commit; the subject and tag carry the version.

Write down the version, tag, and a release summary: imperative, capitalized, under about 60 characters, no trailing period, e.g. `Reset hCaptcha after a failed contact-form send`.

## 9. Open the PR and wait for CI

```bash
git -C <worktree> push -u origin <branch>
gh pr create --base <default> --head <branch> --title "<imperative title>" --body-file <file>
```

If the PR already exists (resuming), push to it and update its body (`gh pr edit <pr> --body-file <file>`) instead of creating one. If it's a draft, mark it ready (`gh pr ready <pr>`) once CI passes, since a draft can't be merged.

The body has `Closes #N`, a short summary, how you verified it (including the user's local-dev test, or that `--no-test` skipped it), the size with the model and effort used, and `Releases vX.Y.Z (patch)` or similar. Follow the user's or repo's attribution rules. Write the body file in a temp directory and delete it after.

Wait: `gh pr checks <pr> --watch --fail-fast`. CI often outlasts a foreground shell call's timeout, so run it in the background where your agent can and wait for it to finish; otherwise rerun it until nothing is pending. If it reports no checks but `.github/workflows/` exists, wait about 15 seconds and retry before concluding there's no CI. On failure, read `gh run view <run-id> --log-failed`, fix, and push. Stop after two attempts.

With `--no-merge`, stop here, remove only the worktree (`git worktree remove <worktree path>`, after stopping any dev server), and report. Keep the local and remote branch: the open PR needs them.

## 10. Merge as the release commit

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

If squash isn't allowed, use the first of `merge_methods` without the release subject, and put running `/patch` or `/minor` on `<default>` in the follow-up: it commits on the branch it runs on, and this run doesn't switch the user's checkout. Don't delete the branch yet (step 12 does). Never pass `--admin` or bypass a failing check. If the PR needs an approving review, it has to come from someone other than its author, and the PR was opened from the user's account: take the failure path and name getting that review as the follow-up.

Confirm the issue closed (`gh issue view N --json state`); if not, close it with a comment linking the PR.

## 11. Tag the release

Tag the squash-merge commit by its SHA, from the worktree, so nothing switches or pulls in the user's checkout. Nothing is pushed to `<default>`, so branch protection doesn't interfere.

```bash
sha=$(gh pr view <pr> --json mergeCommit --jq .mergeCommit.oid)
git -C <worktree> fetch origin
cd <worktree> && python <this skill's directory>/scripts/version_info.py --verify X.Y.Z --ref "$sha"   # ready_to_tag must be true
git -C <worktree> tag -a vX.Y.Z "$sha" -m "vX.Y.Z - <Summary>"  # lightweight `git tag vX.Y.Z "$sha"` if tag_style is lightweight
git -C <worktree> push origin vX.Y.Z
```

If `ready_to_tag` is false, don't tag; report its `problems` with the fix as the follow-up. If the push is rejected, keep the local tag and put `git push origin vX.Y.Z` in the follow-up.

Then go back to step 12 in SKILL.md to clean up.
