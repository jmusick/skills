---
name: update-docs
description: "Audit and tidy a repo's docs. Checks each doc against the code and fixes what's wrong or out of date, then reviews organization: contradictions between docs, docs no longer needed, duplicates to consolidate, misplaced content, and inconsistent formatting. Covers README, AGENTS.md, CLAUDE.md, CONTRIBUTING, docs/, CHANGELOG, privacy policies, dated records (audits, ADRs, plans), and agent notes (TODO.md, memory-bank/). Use when the user types /update-docs or $update-docs, or asks to update, refresh, sync, audit, check, clean up, tidy, organize, or consolidate the docs, README, AGENTS.md, or CLAUDE.md; asks whether the docs are still accurate or needed; or wants the docs caught up after a batch of changes, even if they just say the docs are a mess or old plans and audits are piling up. Not for writing new docs from scratch, code comments or docstrings, de-AI'ing prose (use humanize), releases or version bumps (use /patch or /minor), or documents outside the repo."
---

# Update docs

Make the repo's docs tell the truth about the code as it is now, and keep them organized so people and agents can find what they need. Edit docs only, never code, and don't commit; the user reviews the diff.

Two kinds of change, two levels of authority:

- **Apply directly:** fixes inside a file. Wrong facts, broken links, formatting, consistent terms, status notes on dated records, changelog entries.
- **Propose, then wait:** anything that changes which files exist or where content lives. Deleting, moving, merging, splitting, archiving, adding an index. The user approves these by number (step 8). A diff shows an edit line by line, but a deleted or merged file is hard to review that way, and moves break links in places the diff doesn't show.

If the user says "audit" or "check only", apply nothing and report both lists.

If the user or a calling skill limits the run to named files or to docs a diff could have made wrong (issue does this), do steps 3, 5 and 7 for those docs only and skip the organization review. Don't stop to ask for approval; list any structural ideas under "Noticed, not done" so the caller can pass them on.

## 1. Find and sort the docs

```bash
git ls-files --cached --others --exclude-standard -- '*.md' '*.mdx' '*.rst' '*.adoc' '*.txt' | grep -viE 'node_modules|vendor|fixtures?/'
git ls-files --cached --others --exclude-standard | grep -iE 'privacy|terms|(^|/)(docs?|wiki)/|^\.github/'
git ls-files --others --exclude-standard
```

The last command shows which files are untracked. Mark those: they have no git history, so deleting one loses it for good.

Sort each doc into one kind. The kind decides what "fixing" it means.

- **Living docs** describe the project as it is now and must be true now: README, AGENTS.md, CLAUDE.md, CONTRIBUTING, SECURITY, guides in `docs/`, nested READMEs, `.github/` issue and PR templates, HTML docs pages, the privacy policy wherever it lives (including an app route).
- **Dated records** were true when written and stay that way: audits, ADRs and decision logs, plans, specs, RFCs, postmortems, review notes, migration notes. Tells: a date in the name or heading, a `Status:` line, a folder like `adr/`, `decisions/`, `audits/`, or `plans/`, or text describing work to do rather than how things are. Some specs and design docs are kept current instead; if `git log` shows one edited alongside the code it describes, treat it as a living doc.
- **Agent notes** are working files that pile up: `PLAN.md`, `TODO.md`, `NOTES.md`, scratch files, `memory-bank/`, notes under `.claude/`. Settings, commands, agents, and skills under `.claude/` are config, not docs; leave them alone.
- **CHANGELOG** has its own rules (step 7).

Out of scope: files that *are* the product or its content (prompt files, skill bodies, blog posts, templates, test fixtures), LICENSE and third-party notices, and generated docs (edit the source they're built from instead).

Read AGENTS.md / CLAUDE.md first. They may set doc rules (e.g. "keep the README table in sync"), and those rules are claims to check too.

With more than a few dozen docs, checking every claim in every file won't fit one pass. Check the docs readers hit first (README, AGENTS.md, getting-started and setup guides) fully, use step 2 to target the rest, and say in the report which docs got only a light check. If you can spawn subagents, you can split the claim checks by folder, but make the edits yourself so terms and fixes stay consistent across docs.

## 2. See what changed since the docs were last touched

For each doc, find its last commit and what changed in the repo after it:

```bash
git log -1 --format='%h %as' -- README.md
git log --oneline --stat <that-hash>..HEAD
git status --short
```

This points you at likely drift (new folders, renamed scripts, removed features) and at docs nobody has touched in a long time. It doesn't replace step 3, because some docs were wrong from the day they were written.

## 3. Check living docs against the repo

Treat each statement a living doc makes as a claim and verify it by reading the code or running a read-only command. Don't trust memory of how a tool "usually" works.

- **Paths and names:** every file, folder, script, and module mentioned exists at that path.
- **Commands:** install, build, test, and run commands exist (`package.json` scripts, Makefile, CI workflows, `pyproject.toml`) and use the right flags and package manager.
- **Versions and requirements:** runtime versions, dependencies, and supported platforms match the manifests and CI.
- **Catalogs and counts:** tables or lists of skills, commands, endpoints, packages, or env vars match what's on disk, both ways: nothing listed that's gone, nothing on disk that's missing. Descriptions match the source (frontmatter, help text, docstrings).
- **Config:** env vars, config keys, and defaults match the code that reads them.
- **Links:** relative links and anchors resolve. Don't fetch external links unless the user asks.
- **Examples:** code samples use functions, options, and output formats that still exist.
- **Stated rules:** checkable claims hold ("these two files are identical", "scripts use only the standard library", "no build step").
- **Gaps:** a user-facing feature, command, or top-level folder that no doc mentions where a reader would look for it.

## 4. Check dated records and agent notes

Never rewrite what a dated record says, even where the code has moved on. It records what was decided or found at the time, and "fixing" it to match today's code falsifies that record.

Instead, work out each record's status from commits, the code, and newer records: still open, done, superseded, or abandoned.

- **Done or superseded but still worth keeping as history:** add one status line under the title, e.g. `> Status: superseded by docs/adr/0007-queue.md (2026-10-31)` or `> Status: done in v0.7.0`. Update an existing `Status:` line instead of adding a second.
- **No longer worth keeping:** propose deleting it (step 8). Examples: a plan whose work shipped and is recorded in the changelog or an ADR, an audit whose findings were all fixed, a scratch file with nothing in it a reader still needs.
- **Still open:** leave it.

Agent notes are lists of work, so check them like one. Propose removing items the code or history shows are done, and propose deleting a notes file whose content is all done or stale.

If a living doc cites a dated record as current ("see the 2024 audit for our auth setup") and the record is stale, that's a living-doc problem; fix the citation.

## 5. Find contradictions

Compare docs that cover the same ground: setup steps in README vs CONTRIBUTING, rules in AGENTS.md vs CONTRIBUTING, versions, defaults, and names for the same thing.

- **The code settles it:** fix the doc that's wrong (step 7).
- **The code can't settle it** (a policy, a process, an intent): don't pick a side. Put both claims, with file:line, under "Needs your call".

A dated record disagreeing with a living doc isn't a contradiction; the record is history. Mark its status instead (step 4).

## 6. Review organization

Look for:

- **Docs no longer needed:** about a removed feature, superseded by another doc, an empty stub, or a finished record or notes file (step 4). Give the reason and the evidence for each.
- **Duplication:** the same content in two places that will drift apart. Propose keeping it in one and linking from the other. Keep the copy where a reader would look first, or the one more docs already link to. AGENTS.md may restate a few rules agents must see without following a link; that's fine.
- **Misplaced content:** long reference material in the README that belongs in `docs/`; how-to-run steps buried in a design doc; human-only background in AGENTS.md, which loads into every agent session and should hold only what an agent can't learn from the code.
- **Shape:** one doc covering unrelated topics (propose splitting it), or several tiny docs on one topic (propose merging them).
- **Findability:** docs nothing links to, a `docs/` folder with many files and no index, a README that never points to `docs/`.

If the docs as a whole are scattered, duplicated, or hard to navigate, also propose a target layout: a short tree of what lives where and what moves or merges to get there. Don't propose one for its own sake. A small repo with a good README and a changelog is already organized.

## 7. Apply the small fixes

Skip in audit mode. Make the smallest edit that makes each doc true and readable.

- Keep each doc's voice, structure, and wording. This is a correctness and consistency pass, not a rewrite.
- If you can't verify something, leave it and flag it. A guess written into docs is worse than a gap, because readers trust it.
- Remove docs for things that no longer exist instead of hedging them.
- Keep AGENTS.md and CLAUDE.md short: commands, conventions, gotchas. If CLAUDE.md just imports AGENTS.md (`@AGENTS.md`), edit AGENTS.md.

### Formatting and consistency

Follow the repo's existing conventions (bullet style, heading case, line wrapping) over your own preferences.

- One H1 per doc, and no skipped heading levels.
- Lists and tables that render; code fences with a language.
- One term for one thing across all docs. Use the one the code uses.
- Put what a reader needs first (what it is, how to install and run it) ahead of background and history.
- Break up a wall of text with headings, or with a list where the content really is steps or items.

Don't reword sentences beyond that. If the user wants the prose itself tightened or de-AI'd, that's the humanize skill.

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

## 8. Report and propose

Report what you fixed, what needs the user's call, and the numbered structural proposals, then stop and wait. List every doc you checked so the user knows what was covered.

```
Updated docs
- README.md: added update-docs to the skills table; fixed install path
- AGENTS.md: removed the step for build.sh (deleted in 3f2a1c9)
- docs/plans/queue-rewrite.md: marked done in v0.7.0
- docs/*.md: fixed heading levels; "workspace" → "project" to match the CLI
- CHANGELOG.md: added 2 entries under Unreleased

Needs your call
- CONTRIBUTING.md:14 says PRs need two reviews; AGENTS.md:31 says one
- PRIVACY.md says no third parties receive data, but src/analytics.ts:12 sends page views to Plausible

Proposed changes (reply with the numbers to apply, "all", or "none")
1. Delete docs/setup-old.md: superseded by the README's Install section, nothing links to it
2. Merge docs/env.md into docs/config.md: same env var table in both, already drifting
3. Delete NOTES.md (untracked, can't be recovered): every item is done
4. Add docs/README.md as an index: 11 docs, nothing links to 6 of them

Checked, no changes: SECURITY.md, docs/api.md, docs/adr/0001-0006
```

Leave out an empty section. Nothing is committed; say so. If there are no proposals, the run ends here.

## 9. Apply what's approved

Do only the numbers the user approved.

- Move tracked files with `git mv` so history follows them; untracked files with a plain move.
- When merging, keep everything from the source that isn't already in the target, then delete the source.
- After any move, merge, or delete, search the repo for links and mentions of the old path and fix them, including in AGENTS.md and code comments that point at docs.
- Report what you applied, in the same format. Still nothing committed.
