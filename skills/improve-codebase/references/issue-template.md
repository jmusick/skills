# Issue template

Write every issue for someone who hasn't seen this conversation, this audit, or the other issues. `/issue` will refuse an issue with no clear done state, and `/wave` uses the files in scope to keep parallel issues from colliding, so both sections are required.

## Title

An imperative sentence that names the change and where it lands: "Merge the UserRepository pass-through methods into find and save", "Add tests pinning invoice rounding before the tax refactor". Not "Tech debt in users" or "Improve code quality".

## Body

```markdown
## Problem

<What's wrong, in two or three sentences, with the evidence: `path:line` for each location and a short excerpt (under ~15 lines) of the current code.>

## Why it matters

<The cost this code pays now: how often it changes or breaks (from git history), fixes that had to be repeated, a test that can't be written, a bug it caused. Severity: Critical | High | Medium | Low.>

## Proposed change

<The direction, not the full code: what goes away, what merges, where logic moves, what the new interface looks like if there is one. Name the existing helper or pattern to reuse, with its path. Mention the smaller alternative if one was considered.>

## Files in scope

- `path/one`
- `path/two`

Out of scope: <things that look related but must not change, such as a public API, a schema, or a neighboring module>.

## Done when

- [ ] <A checkable result: "`grep -r legacyParse src` finds nothing", "`UserRepository` exposes only `find` and `save`">
- [ ] `<test command>` passes
- [ ] `<lint / typecheck command>` passes

## Keeping behavior the same

<How to prove nothing changed: the existing tests that cover this code, or the tests to add first. If this issue depends on a tests issue, say so here and below.>

## Notes

- Depends on #N <if any>
- Risk: <what could go wrong>
- Stop and ask on the issue if <the condition that would make the proposed change wrong, e.g. "a caller outside this repo uses the old method">.

Found by /improve-codebase at <short commit SHA>.
```

## Rules

- Leave out sections that truly don't apply (a deletion has no new interface), but never leave out Files in scope or Done when.
- Never paste a secret, even partly. Cite its location and kind.
- Quote no more code than the reader needs to recognize the spot.
- For a tests-first issue, Done when lists the new tests and says they pass against the current, unchanged code.
