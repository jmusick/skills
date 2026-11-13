---
name: minor
description: Cut a minor release (X.Y.Z to X.Y+1.0) of the current git repo, committed as "vX.Y.Z - Summary", tagged, and pushed.
disable-model-invocation: true
---

# Minor release

Ship the work in this repo as the next **minor** version: `X.Y.Z` becomes `X.(Y+1).0`. Typing the command is the go-ahead to commit, tag, and push, so don't confirm along the way. Stop only for the cases under "When to stop and ask", because a pushed tag is awkward to take back.

Convention: one commit holds the session's work and the version bump, subject `vX.Y.Z - <summary>` (e.g. `v1.21.0 - Add an advertising inquiry form`), tagged `vX.Y.Z`.

## 1. Survey the repo

Fetch first, so the survey compares against what's on the remote now, then run the read-only script from anywhere inside the repo (`python3` if `python` isn't found):

```bash
git fetch origin --tags
python <this skill's directory>/scripts/version_info.py minor
```

It prints JSON: current and next version, latest tag and `tag_style`, whether origin already has the next tag or a newer one, version files with `in_lockstep`, changelog path and whether it has an `Unreleased` section, branch and upstream, uncommitted changes, and commits since the tag. If it can't run, gather the same from git and the project's version files.

Skim `AGENTS.md` / `CLAUDE.md` for a release section; follow any project-specific steps. If `versions_disagree` is true, see "When to stop and ask".

## 2. Understand what's being released

The release covers everything since the last tag. Combine the conversation (intent) with `git diff`, `git diff --staged`, and `git log <tag>..HEAD` (what changed). Everything gets staged, so check the tree for `.env` files, credentials, large build output, or debug junk.

Check that the work fits the bump. A patch is fixes and tweaks that add nothing new for users, a minor adds something users couldn't do before, and anything that breaks existing use (a removed or renamed feature, changed behavior people rely on) is a major. If it breaks something, stop and ask: a major bump is the user's call. If it otherwise fits a different bump than this one, say which and ask once, since the version number tells users what to expect.

## 3. Bump the version

Update every version file with `in_lockstep` true, as its `update` hint says. After `npm version`, check `git diff package.json` and restore any reformatted lines; only the version should change. Leave independently versioned files alone (e.g. a separately versioned extension) and mention them in the report.

**Changelog:** if one exists, add a section at the top matching its format exactly (heading style, today's date, categories). If it has an `Unreleased` section (`changelog_has_unreleased`), turn that into this version's section instead of writing a second one for the same changes, and leave a fresh empty `Unreleased` above it. Write for readers, describing what changed for them, and leave out what they can't see (refactors, CI, tests). Don't create one if absent.

## 4. Check, commit, tag, push

Run the repo's checks (test, lint, build: whatever AGENTS.md / CLAUDE.md, `package.json` scripts, or a Makefile name) after the bump, since it can touch a lockfile they read. If one fails, stop and report it rather than tag a release that fails its own checks. With no checks, skip this.

Stage everything (`git add -A`) and commit with `git commit -F <file>` (or two `-m` flags) to keep the blank line:

```
vX.Y.Z - <Summary>

<A few sentences on what's in this version.>
```

- **Subject:** imperative, capitalized, no trailing period, under ~72 chars.
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
Released v1.22.0 - Add an advertising inquiry form
- Bumped package.json, package-lock.json; added CHANGELOG entry
- Tagged v1.22.0 and pushed main + tag to origin
```

Mention anything left alone, such as independently versioned files or a skipped changelog.

## When to stop and ask

- **Nothing to release:** no uncommitted changes and no commits since the latest tag.
- **The next tag already exists**, locally or on the remote (`next_tag_exists_on_origin`, or anything in `origin_tags_at_or_above_next`).
- **Versions disagree** unexplainably, e.g. `package.json` is ahead of the latest tag (a bump may have been made but never tagged, so the right release might be that version).
- **Detached HEAD**, or mid-merge or mid-rebase.
- **Branch is behind upstream** (first number of `behind_ahead_upstream` above 0).
- **Checks fail**, or **the work breaks existing use** (see step 2).
- **The tree has something that shouldn't be committed** (secrets, large binaries) or unrelated changes.
- **No remote:** commit and tag, and say nothing was pushed.

A missing changelog or version file is fine; tags alone carry the version.
