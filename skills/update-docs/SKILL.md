---
name: update-docs
description: Audit a repo's documentation against the code as it is now and fix what's wrong or out of date. Covers README.md, AGENTS.md, CLAUDE.md, CONTRIBUTING.md, docs/, CHANGELOG.md, and any privacy policy. Checks paths, commands, versions, catalog tables, links, and stated rules against the repo, adds missing user-facing changes to the changelog's Unreleased section, and flags privacy-policy claims the code contradicts. Use when the user types /update-docs or $update-docs, or asks to update, refresh, sync, audit, or check the docs, README, AGENTS.md, or CLAUDE.md; asks whether the docs are still accurate or current; or wants the docs caught up after a batch of changes. Not for writing new docs for a feature from scratch, code comments or docstrings, cutting a release or bumping versions (use /patch or /minor), or editing documents outside the repo.
---

# Update docs

Make the repo's docs tell the truth about the code as it is now. Edit docs only, never code, and don't commit; the user reviews the diff. If the user says "audit" or "check only", report findings without editing.

## 1. Find the docs

```bash
git ls-files '*.md' '*.mdx' '*.rst' '*.txt' | grep -viE 'node_modules|vendor|fixtures?/'
git ls-files | grep -iE 'privacy|terms'
```

In scope: files that describe the project to people or agents (README, AGENTS.md, CLAUDE.md, CONTRIBUTING, SECURITY, `docs/`, nested READMEs, CHANGELOG, the privacy policy wherever it lives, including an HTML page or app route).

Out of scope: files that *are* the product or its content (prompt files, skill bodies, blog posts, templates, test fixtures), LICENSE and third-party notices, and generated docs (edit the source they're built from instead). If the user named specific files, do just those.

Read AGENTS.md / CLAUDE.md first. They may set doc rules (e.g. "keep the README table in sync"), and those rules are claims to check too.

## 2. See what changed since the docs were last touched

For each doc, find its last commit and what changed in the repo after it:

```bash
git log -1 --format=%h -- README.md
git log --oneline --stat <that-hash>..HEAD
git status --short
```

This points you at likely drift (new folders, renamed scripts, removed features). It doesn't replace step 3, because some docs were wrong from the day they were written.

## 3. Check every claim against the repo

Treat each statement a doc makes as a claim and verify it by reading the code or running a read-only command. Don't trust memory of how a tool "usually" works.

- **Paths and names:** every file, folder, script, and module mentioned exists at that path.
- **Commands:** install, build, test, and run commands exist (`package.json` scripts, Makefile, CI workflows, `pyproject.toml`) and use the right flags and package manager.
- **Versions and requirements:** runtime versions, dependencies, and supported platforms match the manifests and CI.
- **Catalogs and counts:** tables or lists of skills, commands, endpoints, packages, or env vars match what's on disk, both ways: nothing listed that's gone, nothing on disk that's missing. Descriptions match the source (frontmatter, help text, docstrings).
- **Config:** env vars, config keys, and defaults match the code that reads them.
- **Links:** relative links and anchors resolve. Don't fetch external links unless the user asks.
- **Examples:** code samples use functions, options, and output formats that still exist.
- **Stated rules:** checkable claims hold ("these two files are identical", "scripts use only the standard library", "no build step").
- **Gaps:** a user-facing feature, command, or top-level folder that no doc mentions where a reader would look for it.

## 4. Fix it

- Make the smallest edit that makes the doc true. Keep its voice, structure, and formatting; this is a correctness pass, not a rewrite.
- If you can't verify something, leave it and flag it. A guess written into docs is worse than a gap, because readers trust it.
- Remove docs for things that no longer exist instead of hedging them.
- Keep AGENTS.md and CLAUDE.md short. They load into every agent session, so they should hold only what an agent can't learn by reading the code: commands, conventions, gotchas. If CLAUDE.md just imports AGENTS.md (`@AGENTS.md`), edit AGENTS.md.

### CHANGELOG

- Leave released entries alone; they record what shipped.
- Add user-facing changes since the latest release tag (`git describe --tags --abbrev=0`) that aren't listed yet, under the existing `Unreleased` section, in the file's own format and categories. Create an `Unreleased` section only if the file follows Keep a Changelog or already used one.
- Write for users: what changed for them, not which files moved. Skip internal refactors.
- Don't bump versions or date a new release. That's /patch or /minor.
- If there's no changelog, don't create one.

### Privacy policy

A privacy policy is a promise to users, so check it against what the code actually does: analytics and tracking SDKs, cookies and local storage, third-party APIs that receive user data, form fields and accounts, logging, error reporting, retention, and the contact address.

- **Fix directly:** factual lists the code settles, e.g. naming a third-party service the code now sends data to, or removing one it no longer uses. Update the "last updated" date only when the content changes.
- **Flag, don't edit:** anything that changes a commitment (what's collected, sold, shared, or kept, and for how long) or that you can't confirm from the code. Show the evidence (file:line) and suggest wording. The user, and possibly a lawyer, decides.

## 5. Report

```
Updated docs
- README.md: added update-docs to the skills table; fixed install path
- AGENTS.md: removed the step for build.sh (deleted in 3f2a1c9)
- CHANGELOG.md: added 2 entries under Unreleased

Needs your call
- PRIVACY.md says no third parties receive data, but src/analytics.ts:12 sends page views to Plausible
- docs/deploy.md: couldn't verify the staging URL

Checked, no changes: CONTRIBUTING.md, docs/api.md
```

List every doc you checked so the user knows what was covered. Nothing is committed; say so.
