---
name: update-docs
description: Checks a repo's docs (README, AGENTS.md, CLAUDE.md, CONTRIBUTING, docs/ guides, privacy policy, agent notes like TODO.md) against the code, fixes what's no longer true, and proposes deleting, merging, or moving docs that are stale, duplicated, or misplaced. Use when the user types /update-docs or asks to update, sync, audit, check, clean up, tidy, or organize the docs, asks whether the README is still accurate, or says the docs are a mess or have piled up. Not for writing new docs, de-AI'ing prose (humanize does that), or changelog entries and version bumps, which release does.
---
Make the repo's docs true about the code as it is now, and keep them organized so people and agents can find what they need. Edit docs only, not code.

Two kinds of change, two levels of authority:

- **Apply directly:** fixes inside a file, like wrong facts, broken links, terms, and finished items in agent notes.
- **Propose, then wait:** anything that changes which files exist or where content lives: deleting, moving, merging, splitting, or adding an index. The user approves these by number. A diff shows an edit line by line, but a deleted or merged file is hard to review that way, and a move breaks links the diff doesn't show.

If the user or a calling skill limits the run (to named files, or to docs a diff could have made wrong), check only those docs and skip the organization review. Don't stop for approval: list any structural ideas under "Noticed, not done" so the caller can pass them on.

## 1. Read the rules and sort the docs

Read AGENTS.md and CLAUDE.md first. Their doc rules (like "keep the README table in sync") are claims to check too. If CLAUDE.md only imports AGENTS.md, edit AGENTS.md.

Sort each doc into one kind, because the kind decides what fixing it means:

- **Living docs** describe the project as it is now and must be true now: README, AGENTS.md, CLAUDE.md, CONTRIBUTING, SECURITY, guides in `docs/`, nested READMEs, `.github/` templates, the privacy policy wherever it lives (an app route counts).
- **Dated records** were true when written: ADRs, plans, specs, audits, postmortems, past changelog entries. Tells are a date in the name, a `Status:` line, or a folder like `adr/` or `plans/`. Leave them alone, because rewriting one to match today's code falsifies the record. A spec that `git log` shows being edited alongside its code is kept current, so treat it as living.
- **Agent notes** are working files that pile up: `TODO.md`, `PLAN.md`, `NOTES.md`, scratch files, `memory-bank/`, notes under `.claude/`. Settings, commands, agents, and skills under `.claude/` are config, not docs.
- **Out of scope:** files that are the product (SKILL.md bodies, prompt files, templates, test fixtures), LICENSE and third-party notices, generated docs (fix their source instead), and the CHANGELOG and version numbers, which release maintains.

## 2. Check living docs against the repo

Treat each statement as a claim and verify it by reading the code or running a read-only command. Don't trust memory of how a tool usually works.

- **Paths and names:** every file, folder, script, and module mentioned exists at that path.
- **Commands:** install, build, test, and run commands exist (package scripts, Makefile, CI workflows) with the right flags and package manager.
- **Versions and requirements:** runtimes, dependencies, and platforms match the manifests and CI.
- **Catalogs and counts:** tables of skills, commands, endpoints, or env vars match what's on disk both ways, nothing listed that's gone and nothing on disk that's missing, and their descriptions match the source (frontmatter, help text).
- **Config:** env vars, keys, and defaults match the code that reads them.
- **Links:** relative links and anchors resolve. Run this skill's script from the repo root, `python <this skill's folder>/scripts/doc_links.py`, adding the doc paths on a limited run. It lists broken links and anchors (including wrong-case paths that work on Windows and macOS but break on GitHub), and on a full run, docs nothing links to. Rebuilding GitHub's heading slugs by eye is error-prone, so trust the script over reading. Without Python, open each target. Don't fetch external links unless asked.
- **Examples:** code samples use functions, options, and output that still exist.
- **Stated rules:** checkable claims hold ("no build step", "standard library only").
- **Gaps:** a user-facing feature, command, or top-level folder no doc mentions where a reader would look for it.

## 3. Find contradictions

Compare docs that cover the same ground: setup in README vs CONTRIBUTING, rules in AGENTS.md vs CONTRIBUTING, versions, defaults, and names for the same thing. When the code settles it, fix the doc that's wrong. When it can't (a policy, a process, an intent), don't pick a side: list both claims with file:line under "Needs your call".

## 4. Check agent notes

Agent notes are lists of work, so check each item against the code and history. Remove items that are done. Propose deleting a notes file whose content is all done or stale.

## 5. Check the privacy policy

If the repo has a privacy policy, read `references/privacy-policy.md` and follow it. It lists where tracking, third-party services, and stored data show up in code, so the check doesn't rest on remembering every SDK. Fix the factual lists the code settles; flag any change to a commitment (what's collected, shared, sold, or kept) for the user.

## 6. Review organization

Skip this on a limited run. Look for:

- **Docs no longer needed:** about a removed feature, superseded by another doc, an empty stub, or a finished notes file. Give the reason and the evidence.
- **Duplication:** the same content in two places that will drift apart. Keep it where a reader looks first, or where more docs already link, and link from the other. AGENTS.md may restate a few rules agents must see without following a link.
- **Misplaced content:** long reference material in the README that belongs in `docs/`, run steps buried in a design doc, or human-only background in AGENTS.md, which loads into every agent session and should hold only what an agent can't learn from the code.
- **Shape:** one doc covering unrelated topics (split it), or several tiny docs on one topic (merge them).
- **Findability:** docs nothing links to (the script's second list; code may still load one, so check with `--to` before calling it unused), a `docs/` folder with many files and no index, a README that never points to `docs/`.

If the docs as a whole are scattered, also propose a target layout: a short tree of what lives where. Don't propose one for its own sake; a small repo with a good README is already organized.

## 7. Apply the fixes

Make the smallest edit that makes each doc true, and keep its voice, structure, and wording. This is a correctness pass, not a rewrite; if the user wants the prose tightened, that's humanize.

- Flag what you can't verify instead of guessing. A guess written into docs is worse than a gap, because readers trust it.
- Remove docs for things that no longer exist instead of hedging them.
- Follow the repo's conventions (bullet style, heading case, wrapping), and use one term for one thing across all docs, the one the code uses.

## 8. Report and propose

Don't commit. Report what changed, what needs the user's call, and the numbered proposals, then stop and wait. List every doc checked so the user knows what was covered, and leave out empty sections.

```
Updated docs
- README.md: added update-docs to the skills table; fixed the install path
- AGENTS.md: removed the step for build.sh (deleted in 3f2a1c9)
- TODO.md: removed 3 items that shipped

Needs your call
- CONTRIBUTING.md:14 says PRs need two reviews; AGENTS.md:31 says one
- PRIVACY.md says no third parties get data, but src/analytics.ts:12 sends page views to Plausible

Proposed changes (reply with the numbers to apply, "all", or "none")
1. Delete docs/setup-old.md: superseded by the README's Install section, nothing links to it
2. Merge docs/env.md into docs/config.md: same env var table in both, already drifting
3. Delete NOTES.md (untracked, so it can't be recovered): every item is done

Noticed, not done (limited runs only)
- docs/setup-old.md looks superseded by the README, but this run covers only the diff

Checked, no changes: SECURITY.md, docs/api.md
```

Mark untracked files in a proposal, since deleting one loses it for good. If there are no proposals, offer to commit the edits as `docs:`, which doesn't trigger a release, and stop.

## 9. Apply what's approved

Do only the numbers the user approved.

- Move tracked files with `git mv` so history follows them.
- When merging, keep everything from the source that isn't already in the target, then delete the source.
- After any move, merge, or delete, run `doc_links.py --to <old path>` to list links and mentions of the old path anywhere in the repo, including AGENTS.md and code comments, and fix each one. Then rerun it with no arguments to confirm nothing is broken.
- Report what you applied in the same format, and offer to commit it all as `docs:`.
