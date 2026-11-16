---
name: release
description: Cuts a release of the current repo, working out the semver bump (major, minor, or patch) from the Conventional Commits since the last tag, then tags and pushes. When no commit calls for a new version, it still pushes the branch, without a tag. Use when the user types /release or asks to cut, ship, tag, or publish a release or new version. Don't use it unasked, since it pushes.
---
Cut the next version from the commits since the last tag. Running the skill is the go-ahead to commit, tag, and push, so don't confirm along the way, except for a major bump. If the repo's AGENTS.md or CLAUDE.md has a release section, follow it where it differs from these steps.

## 1. Survey

Run `git fetch origin --tags` first. Origin's tags are the record of what's been released, and local tags can lag behind them.

Stop and tell the user, before changing anything, if:
- HEAD is detached, or a merge, rebase, or cherry-pick is in progress.
- The branch is behind its upstream. Don't pull, rebase, or merge to catch up: how to reconcile is the user's call.
- There are uncommitted changes. Offer to commit them first as Conventional Commits, so the release holds only typed, committed work.

Find the latest `vX.Y.Z` tag and list the commits since it (`git log <tag>..HEAD`). With no commits since it, say there's nothing to release and stop.

## 2. Pick the bump

Take the bump from the highest-ranking commit: `!` after the type or a `BREAKING CHANGE:` footer is major, `feat` is minor, `fix` or `perf` is patch. Commits that aren't Conventional (older free-form subjects, merged PR titles) still count: read their diffs and rank them by what changed for users. Fixes and tweaks are a patch, something users couldn't do before is a minor, and anything that breaks existing use (a removed or renamed feature, changed behavior people rely on) is a major.

- **Major:** confirm with the user first. A new major, or 1.0.0 from 0.x, is their call.
- **Nothing but other types** (`chore`, `docs`, `ci`, ...): there's no version to cut. Still push the branch, with no tag and the push rules in step 5, so the pending commits go out. Report that nothing needed a release and what was pushed, and stop.

Then stop and ask if:
- `vX.Y.Z`, or any newer release tag, is already on origin. Tagging it again would put two releases under one number.
- A version file is ahead of the latest tag (say `package.json` at 1.5.0 with v1.4.0 the latest tag). A bump was probably made and never tagged, so the right release may be that version.

## 3. Update the version files

Update every file that holds the current version: `package.json`, `pyproject.toml`, `Cargo.toml`, `*.csproj` or `Directory.Build.props`, `VERSION`, plugin and extension manifests, and so on.

- Skip `node_modules/`, `vendor/`, `dist/`, `build/`, `evals/`, and `fixtures/`. Dependencies and test projects carry versions that aren't this one.
- Leave files that are versioned on their own (a separately released extension, say), and mention them in the report.
- **npm:** `npm version X.Y.Z --no-git-tag-version`, which also bumps `package-lock.json`. Then check `git diff package.json` and restore any reformatted lines, since only the version should change. Without npm, edit the lockfile's top-level `version` and `packages[""].version` by hand.
- **Unity:** `bundleVersion` in `ProjectSettings/ProjectSettings.asset`. Leave the generated `Assembly-CSharp*.csproj` files alone.

## 4. Update the changelog

If there's no changelog, don't create one: the tags carry the version. If there is one:
- Match its format exactly: heading style, today's date, categories.
- If it has an `Unreleased` section, turn that into this version's section instead of writing a second one for the same changes, and leave a fresh, empty `Unreleased` above it.
- Write for readers, from the breaking, `feat`, and `fix` commits. Say what changed for them rather than pasting commit subjects, and leave out what they can't see (refactors, CI, tests, chores).

## 5. Check, commit, tag, push

Run the project's checks (test, lint, build: whatever AGENTS.md or CLAUDE.md, `package.json` scripts, or a Makefile name) after the bump, since it can touch a lockfile they read. If one fails, stop and report it rather than tag a release that fails its own checks.

Commit the version files and changelog as `chore(release): vX.Y.Z`. If nothing needed updating, skip the commit and tag the current one.

Tag `vX.Y.Z` in the style of the existing tags: lightweight (`git tag vX.Y.Z`), or annotated with the release commit's subject as the message (`git tag -a vX.Y.Z -m "chore(release): vX.Y.Z"`). `git cat-file -t <latest tag>` prints `tag` for an annotated one and `commit` for a lightweight one.

Push the branch, then the tag (`git push origin <branch>`, then `git push origin vX.Y.Z`). Add `-u` if the branch has no upstream yet.
- If a push is rejected, stop and tell the user. Don't force-push, rebase, or merge.
- With no remote, keep the commit and tag local and say nothing was pushed.
- If a sandbox blocks the network, ask for permission rather than report success.

## 6. Report

Give the new version, the commits that set the bump, the files updated (and any left alone), and what was pushed.
