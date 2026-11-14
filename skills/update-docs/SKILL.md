---
name: update-docs
description: Checks a repo's docs (README, AGENTS.md, CLAUDE.md, CONTRIBUTING, docs/ guides) against the code and fixes what's no longer true. Use when the user types /update-docs or asks to update, sync, audit, or check the docs, or asks whether the README is still accurate. Not for writing new docs, or for changelog entries and version bumps, which release does.
---
Make the docs true about the code as it is now. Edit docs only, not code.

1. Read AGENTS.md and CLAUDE.md first: their doc rules (like "keep the README table in sync") are claims to check too. If CLAUDE.md only imports AGENTS.md, edit AGENTS.md.
2. Check each statement in a doc against the repo: paths, commands and flags, versions, config keys, links, examples, and catalogs both ways (nothing listed that's gone, nothing on disk that's missing).
3. Leave alone dated records (ADRs, plans, audits, past changelog entries), which were true when written; files that are the product, like SKILL.md bodies and prompt files; generated docs; and the CHANGELOG and version numbers, which release maintains.
4. Make the smallest edit that makes each doc true, in its own voice. Flag what you can't verify instead of guessing. Ask before deleting, moving, or merging files.
5. If the user or a calling skill limits the run (for example, to docs a diff touched), check only those.
6. Don't commit. Report what changed and what you flagged, and offer to commit it as `docs:`, which doesn't trigger a release.
