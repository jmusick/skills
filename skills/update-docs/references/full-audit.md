# Full audit steps

Read this on a full run. A run limited to named files or to what a diff could have made wrong skips it.

## 2. See what changed since the docs were last touched

For each doc, find its last commit and what changed in the repo after it:

```bash
git log -1 --format='%h %as' -- README.md
git log --oneline --stat <that-hash>..HEAD
git status --short
```

This points you at likely drift (new folders, renamed scripts, removed features) and at docs nobody has touched in a long time. It doesn't replace step 3, because some docs were wrong from the day they were written.


## 4. Check dated records and agent notes

Never rewrite what a dated record says, even where the code has moved on. It records what was decided or found at the time, and "fixing" it to match today's code falsifies that record.

Instead, work out each record's status from commits, the code, and newer records: still open, done, superseded, or abandoned.

- **Done or superseded but still worth keeping as history:** add one status line under the title, e.g. `> Status: superseded by docs/adr/0007-queue.md (2026-10-31)` or `> Status: done in v0.7.0`. Update an existing `Status:` line instead of adding a second.
- **No longer worth keeping:** propose deleting it (step 8). Examples: a plan whose work shipped and is recorded in the changelog or an ADR, an audit whose findings were all fixed, a scratch file with nothing in it a reader still needs.
- **Still open:** leave it.

Agent notes are lists of work, so check them like one. Propose removing items the code or history shows are done, and propose deleting a notes file whose content is all done or stale.

If a living doc cites a dated record as current ("see the 2024 audit for our auth setup") and the record is stale, that's a living-doc problem; fix the citation.


## 6. Review organization

Look for:

- **Docs no longer needed:** about a removed feature, superseded by another doc, an empty stub, or a finished record or notes file (step 4). Give the reason and the evidence for each.
- **Duplication:** the same content in two places that will drift apart. Propose keeping it in one and linking from the other. Keep the copy where a reader would look first, or the one more docs already link to. AGENTS.md may restate a few rules agents must see without following a link; that's fine.
- **Misplaced content:** long reference material in the README that belongs in `docs/`; how-to-run steps buried in a design doc; human-only background in AGENTS.md, which loads into every agent session and should hold only what an agent can't learn from the code.
- **Shape:** one doc covering unrelated topics (propose splitting it), or several tiny docs on one topic (propose merging them).
- **Findability:** docs nothing links to, a `docs/` folder with many files and no index, a README that never points to `docs/`.

If the docs as a whole are scattered, duplicated, or hard to navigate, also propose a target layout: a short tree of what lives where and what moves or merges to get there. Don't propose one for its own sake. A small repo with a good README and a changelog is already organized.


## 9. Apply what's approved

Do only the numbers the user approved.

- Move tracked files with `git mv` so history follows them; untracked files with a plain move.
- When merging, keep everything from the source that isn't already in the target, then delete the source.
- After any move, merge, or delete, search the repo for links and mentions of the old path and fix them, including in AGENTS.md and code comments that point at docs.
- Report what you applied, in the same format. Still nothing committed.
