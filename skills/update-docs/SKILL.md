---
name: update-docs
description: "Audit and tidy a repo's docs: fix what no longer matches the code, then propose deleting, merging, or moving stale, duplicated, or misplaced docs. Not for writing new docs, code comments, de-AI'ing prose (use humanize), or releases (use /patch or /minor)."
---

# Update docs

Make the repo's docs tell the truth about the code as it is now, and keep them organized so people and agents can find what they need. Edit docs only, never code, and don't commit; the user reviews the diff.

Two kinds of change, two levels of authority:

- **Apply directly:** fixes inside a file. Wrong facts, broken links, formatting, consistent terms, status notes on dated records, changelog entries.
- **Propose, then wait:** anything that changes which files exist or where content lives. Deleting, moving, merging, splitting, archiving, adding an index. The user approves these by number (step 8). A diff shows an edit line by line, but a deleted or merged file is hard to review that way, and moves break links in places the diff doesn't show.

If the user says "audit" or "check only", apply nothing and report both lists.

If the user or a calling skill limits the run to named files or to docs a diff could have made wrong (issue does this), do steps 1, 3, 5 and 7 for those docs only and skip the organization review. Don't stop to ask for approval; list any structural ideas under "Noticed, not done" so the caller can pass them on.

On a full run, steps 2, 4, 6 and 9 are in [references/full-audit.md](references/full-audit.md): read it before step 2, and do those steps at their numbers below.

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

## 5. Find contradictions

Compare docs that cover the same ground: setup steps in README vs CONTRIBUTING, rules in AGENTS.md vs CONTRIBUTING, versions, defaults, and names for the same thing.

- **The code settles it:** fix the doc that's wrong (step 7).
- **The code can't settle it** (a policy, a process, an intent): don't pick a side. Put both claims, with file:line, under "Needs your call".

A dated record disagreeing with a living doc isn't a contradiction; the record is history. Mark its status instead (step 4).

## 7. Apply the small fixes

Skip in audit mode. Make the smallest edit that makes each doc true and readable.

- Keep each doc's voice, structure, and wording. This is a correctness and consistency pass, not a rewrite.
- If you can't verify something, leave it and flag it. A guess written into docs is worse than a gap, because readers trust it.
- Remove docs for things that no longer exist instead of hedging them.
- Keep AGENTS.md and CLAUDE.md short: commands, conventions, gotchas. If CLAUDE.md just imports AGENTS.md (`@AGENTS.md`), edit AGENTS.md.

### Formatting and consistency

Follow the repo's existing conventions (bullet style, heading case, line wrapping) over your own preferences. Use one term for one thing across all docs, the one the code uses.

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

Noticed, not done (limited runs only)
- docs/setup-old.md looks superseded by the README, but this run covers only the diff

Checked, no changes: SECURITY.md, docs/api.md, docs/adr/0001-0006

Light check only: docs/guides/*.md (README, AGENTS.md and setup guides got the full check)
```

Leave out an empty section. Nothing is committed; say so. If there are no proposals, the run ends here.

