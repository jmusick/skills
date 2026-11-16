# Issue template

Write every issue for someone who hasn't seen this conversation, this audit, or the other issues: `/issue` works it cold.

## Title

An imperative sentence that names the change and where it lands: "Merge the UserRepository pass-through methods into find and save", "Add tests pinning invoice rounding before the tax refactor". Not "Tech debt in users" or "Improve code quality".

## Body

```markdown
## Before you start

Found by /improve-codebase at `<short commit SHA>`. Run `git diff --stat <short commit SHA>..HEAD -- <each path in Files in scope>`. If a file in scope has changed, compare it with the excerpts under Problem. If they no longer match, stop and comment on this issue rather than adapting the plan.

## Problem

<What's wrong, in two or three sentences, with the evidence: `path:line` for each location and a short excerpt (under ~15 lines) of the current code.>

## Why it matters

<The cost this code pays now: how often it changes or breaks (from git history), fixes that had to be repeated, a test that can't be written, a bug it caused. Severity: Critical | High | Medium | Low.>

## Proposed change

<The direction, not the full code: what goes away, what merges, where logic moves, what the new interface looks like if there is one. Name the existing helper or pattern to reuse, with its path, and one file that already does this the way the repo wants, to match. Mention the smaller alternative if one was considered.>

## Files in scope

- `path/one`
- `path/two`

Out of scope: <things that look related but must not change, such as a public API, a schema, or a neighboring module>.

## Done when

- [ ] <A checkable result: "`grep -r legacyParse src` finds nothing", "`UserRepository` exposes only `find` and `save`">
- [ ] `<test command>` passes
- [ ] `<lint / typecheck command>` passes

## Keeping behavior the same

<How to prove nothing changed: the existing tests that cover this code, or the tests to add first, and an existing test file to model new tests on. "Nothing" includes the errors callers see, the order of side effects, and public names, not just return values. If this issue depends on a tests issue, say so here and below.>

## Notes

- Depends on #N <if any; one line per issue, in this exact wording, because `/issue` reads it and waits until #N is closed>
- Risk: <what could go wrong>

## Stop and ask

Comment on this issue instead of improvising if:

- the change needs a file outside Files in scope;
- <the assumption this proposal rests on turns out false, e.g. "a caller outside this repo uses the old method">.
```

## Rules

- Leave out sections that truly don't apply (a deletion has no new interface), but never leave out Before you start, Files in scope (`/issue`'s batch mode uses it to keep parallel issues from colliding), Done when (`/issue` refuses an issue without a clear done state), or Stop and ask.
- For a Low-confidence finding, file an investigation: title it "Investigate whether …", make Proposed change what to check and where, and make Done when "the finding is confirmed and a fix issue is filed, or ruled out with the reason in a comment". Leave out Keeping behavior the same.
- Quote no more code than the reader needs to recognize the spot.
- For a tests-first issue, Done when lists the new tests and says they pass against the current, unchanged code. If writing them turns up a bug, they pin the current behavior anyway and the bug gets its own issue, because callers may depend on it.
- For a merge or deepening, say in Keeping behavior the same how the new module gets tested, by what it depends on: in-process code is tested directly through its interface; a dependency with a local stand-in (an in-memory database, a temp folder) uses the stand-in; a remote or third-party service goes behind an interface with a fake for tests. Old unit tests on the merged pieces are deleted once tests at the new interface cover them; don't keep both layers.
