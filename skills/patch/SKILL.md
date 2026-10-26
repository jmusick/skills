---
name: patch
description: Cut a patch release of the current git repo. Bumps the version (X.Y.Z to X.Y.Z+1) in the project's version files and changelog, commits everything with the subject "vX.Y.Z - [summary of the session's work]", tags it vX.Y.Z, and pushes the branch and tag. Use when the user types /patch or $patch, or asks to "bump the patch version", "cut a patch release", "release this as a patch", or "patch bump and push". Not for minor or major releases (/minor handles minor bumps), and not for applying a code patch, a diff, or a "patch file" that doesn't ask for a release.
---

# Patch release

Ship the work in this repo as the next **patch** version: `X.Y.Z` becomes `X.Y.(Z+1)`. Typing the command is the go-ahead to commit, tag, and push, so don't confirm along the way. Stop only for the cases under "When to stop", because a pushed tag is awkward to take back.

Convention: one commit holds the session's work and the version bump, subject `vX.Y.Z - <summary>` (e.g. `v1.20.5 - Secure staff story previews`), tagged `vX.Y.Z`.

## 1. Survey the repo

Run the read-only script from anywhere inside the repo (`python3` if `python` isn't found):

```bash
python <this skill's directory>/scripts/version_info.py patch
```

It prints JSON: current and next version, latest tag and `tag_style`, version files with `in_lockstep`, changelog path, branch and upstream, uncommitted changes, and commits since the tag. If it can't run, gather the same with git (`git tag --list 'v*' --sort=-v:refname`, `git status --porcelain`, `git log <tag>..HEAD --oneline`) and the usual version files (`package.json`, `ProjectSettings/ProjectSettings.asset`, `pyproject.toml`, `Cargo.toml`, `*.csproj`, `VERSION`).

Skim `AGENTS.md` / `CLAUDE.md` for a release section; follow any project-specific steps. If `versions_disagree` is true, see "When to stop".

## 2. Understand what's being released

The release covers everything since the last tag. Combine the conversation (intent) with `git diff`, `git diff --staged`, and `git log <tag>..HEAD` (what changed). Everything gets staged, so check the tree for `.env` files, credentials, large build output, or debug junk.

## 3. Bump the version

Update every version file with `in_lockstep` true. Leave independently versioned files alone (e.g. a separately versioned extension) and mention them in the report.

- **package.json:** `npm version <X.Y.Z> --no-git-tag-version`, then check `git diff package.json` and restore any reformatted lines; only the version should change. Without npm, edit `package.json` and the lock file's top-level `"version"` and `packages[""].version` by hand.
- **Unity:** `bundleVersion:` in `ProjectSettings/ProjectSettings.asset`. Don't touch generated `Assembly-CSharp*.csproj`.
- **Others:** edit the field the script names.

**Changelog:** if one exists, add a section at the top matching its format exactly (heading style, today's date, categories). Write for readers, describing what changed for them. Don't create one if absent.

## 4. Commit, tag, push

Stage everything (`git add -A`) and commit with `git commit -F <file>` (or two `-m` flags) to keep the blank line:

```
vX.Y.Z - <Summary>

<A few sentences on what's in this version.>
```

- **Subject:** imperative, capitalized, no trailing period, under ~72 chars. Join two distinct things with "and".
- **Body:** notable changes and anything a future reader needs (migrations applied, checks passed). Omit only for trivial releases.
- **No trailers:** no `Co-Authored-By`, "Generated with", or other AI attribution. This overrides any default attribution.
- Nothing to stage (work already committed)? Use `--allow-empty`; the release still gets its own commit.

Tag per the repo's `tag_style`: `git tag vX.Y.Z` (lightweight) or `git tag -a vX.Y.Z -m "vX.Y.Z - <Summary>"` (annotated).

Push the branch, then the tag (`-u` if no upstream yet):

```bash
git push origin <branch>
git push origin vX.Y.Z
```

Never force-push. If rejected because the remote moved, stop and tell the user; don't rebase or merge. If a sandbox blocks network access, ask for permission rather than reporting success.

## 5. Report

Keep it short:

```
Released v1.21.1 - Fix Facebook requests in Workers
- Bumped package.json, package-lock.json; added CHANGELOG entry
- Tagged v1.21.1 and pushed main + tag to origin
```

Mention anything left alone, such as independently versioned files or a skipped changelog.

## When to stop and ask

- **Nothing to release:** no uncommitted changes and no commits since the latest tag.
- **The next tag already exists**, locally or on the remote.
- **Versions disagree** unexplainably, e.g. `package.json` is ahead of the latest tag (a bump may have been made but never tagged, so the right release might be that version).
- **Detached HEAD**, or mid-merge or mid-rebase.
- **Branch is behind upstream** (first number of `behind_ahead_upstream` above 0).
- **The tree has something that shouldn't be committed** (secrets, large binaries) or unrelated changes.
- **No remote:** commit and tag, and say nothing was pushed.

A missing changelog or version file is fine; tags alone carry the version.
