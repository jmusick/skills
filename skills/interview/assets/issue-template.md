# Issue template

One issue per slice of the spec that can be built, tested, and shipped on its own. Usually that's one scenario, or a scenario plus what it needs. The issue has to make sense to an agent that has the spec but not the interview, so link the spec instead of restating it, and copy only what this slice is judged by.

Title: an imperative phrase saying what the slice delivers, e.g. "Let members vote from the meeting page".

```markdown
## What

{One to three sentences: what this slice delivers and for whom.}

Part of [{spec title}]({spec path, relative to the repo root}), scenario "{scenario title}".

## Done when

- [ ] {Each Given/When/Then from the spec that this slice must satisfy, copied as written.}
- [ ] {Any decision from the spec's Decisions table that this slice puts into effect, with its D number.}

## Not in this issue

- {What a neighboring slice or a later issue covers, so this one doesn't grow.}

Depends on #{N}
```

Leave out the `Depends on` line when the slice depends on nothing.
