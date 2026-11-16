# What to look for

Work through the sections that fit the scope. Each section lists what to flag, what usually isn't a problem, and tools that help.

Run a listed tool only if it's already installed or in the project's dependencies. Write the `npx` ones as `npx --no <tool>`: plain `npx` downloads and runs a package the project doesn't have, which is installing unvetted code.

## Severity

- **Critical:** the code is wrong or unsafe now, or nothing can be verified. A hardcoded live credential, an injection path, data loss, no working test or build command on a project that ships.
- **High:** it keeps costing time or bugs in code that changes often. Logic duplicated across a hotspot so fixes keep missing a copy, a god file in the busiest area, swallowed errors on a critical path, a high-churn path with no tests.
- **Medium:** a real cost in code that changes sometimes. A pass-through layer, inconsistent ways of doing one thing, loose types at a boundary, an unused dependency.
- **Low:** a small, contained cleanup. A dead helper, one magic value, a stale flag.

## Confidence

Severity says how much a finding costs; confidence says how sure you are it's real. Set it after you open the code yourself (SKILL.md step 4).

- **High:** you read the code and the cost is certain from what's in the repo.
- **Medium:** a strong signal that rests on something you couldn't confirm, such as a caller outside the repo, runtime config, or how often a path runs.
- **Low:** a smell worth a look. It gets filed as an investigation, not a fix (see `issue-template.md`).

A finding you can only infer, with no line that shows the cost, stays Medium severity or below.

## 1. Verification baseline

Check this first. Every other fix depends on it.

- Flag: no test command, a red test suite or build on the default branch, a linter or typechecker that's configured but not run in CI, tests that are skipped or quarantined with no reason, CI that doesn't run on pull requests, and no AGENTS.md, CLAUDE.md, or CONTRIBUTING that names the build and test commands, since the agent working each filed issue has to find them.
- Usually fine: a small script or prototype repo with no tests, when its README says so. Report it as a question, not a defect.

## 2. Structure

- **Pass-through layers.** Classes or modules whose methods mostly forward to something else; "Manager", "Helper", "Service", "Utils" names with thin bodies; an interface nearly as big as its implementation. Apply the deletion test.
- **Scattered concepts.** Understanding or changing one concept means touching many small files. Propose merging them into one module that owns the concept.
- **Leaky abstractions.** Public types that expose internal representation; callers forced to sequence calls (`startX()` then `finishX()` instead of `x()`); methods that exist only for tests.
- **Logic in the wrong layer.** Business rules in views or handlers, UI state in models, feature checks sprinkled through shared code, the same config read from several places.
- **Avoided modules.** Busy code working around a module that rarely changes: wrappers or adapters around it, logic copied out of it instead of changed in it, comments warning not to touch it (`grep -rniE "don'?t (touch|change|modify)|do not (touch|change|modify)|workaround"`). Its low churn comes from fear, not health. The module is the finding, and the evidence is the workarounds in the busy files, with `path:line`, plus its commit count from `hotspots.py`.
- **Special-case growth.** One-off flags, nullable modes, and `if` branches bolted onto a busy function. Often a missing type or a missing separate path.
- **Size.** Files over roughly 500 lines or functions over roughly 80 are worth a look, not automatically a finding. Ask whether they hold more than one concept. Generated files, data tables, and test fixtures are fine.
- **Cycles.** Circular imports between modules.
- Tools: `npx --no madge --circular src` or `npx --no fallow architecture --cycles` (JS/TS), `pydeps --show-cycles` (Python), `go vet ./...`.

## 3. Duplication and consistency

- Flag: the same logic in three or more places; copy-paste with small variations (the variation is usually a missing parameter); several ways to do one thing (two HTTP clients, three date helpers, four error types for one failure); a new helper written next to an existing one that does the same job.
- **Hand-rolled machinery.** A home-made parser, date or path helper, retry loop, CLI argument parser, or HTTP wrapper doing what the standard library or a dependency already in the manifest does ("vanilla reimplementation"). Name what would replace it and what would be deleted. A small owned version of a tiny job, or one that's deliberate for security or speed, is fine.
- **The repo's own rules.** Code that breaks a rule AGENTS.md, CONTRIBUTING, or a design doc states about the code (every command has a test, errors go through one helper, handlers split past a size). The evidence is the rule plus the line that breaks it.
- Usually fine: two similar blocks that change for different reasons; duplicated test setup that keeps each test readable.

## 4. Dead code

- Flag: unused code and dependencies, feature flags that are always on or off, compatibility shims and fallbacks with no remaining caller, commented-out blocks with no note saying why they're kept.
- Agent-written code piles up its own kind: options and modes no user asked for, "extensible" mechanisms nothing extends, retry and fallback paths nobody can explain, and long files that read like a log of one request after another. Ask whether a user would notice if it disappeared.
- Before calling something dead, search for dynamic uses: string-based lookups, reflection, plugin registries, framework conventions (routes, migrations, entry points named in config), public API a library exports for others.
- Tools: `npx --no knip` or `npx --no fallow dead-code` (JS/TS), `vulture` (Python), `cargo machete` or `cargo udeps` (Rust), `staticcheck` (Go), `npx --no depcheck`.

## 5. Types and contracts

- Flag: `any`, `as` casts, `# type: ignore`, `@ts-ignore`, and untyped dicts at module boundaries; optional parameters or fields that hide a real invariant; silent fallbacks that paper over an unclear contract; guards against states the code can't reach ("phantom bugs"), which hide the real contract instead of protecting it; input from users, files, or the network used without validation.
- Usually fine: a cast at a well-marked interop edge with a comment saying why.
- Tools: `tsc --noEmit`, `mypy`, `pyright`.

## 6. Correctness and errors

Bugs you can show by reading the code in scope, not a bug hunt across the repo. Diffs belong to `/code-review`.

- Flag errors: errors swallowed where the caller needed to know, inconsistent error shapes from one module, outbound calls with no timeout, unbounded retries, unclosed resources, failures on a critical path that leave no log or error report, and nested catches that return null or a default so a failure looks like success ("defensive programming theatre").
- Flag correctness: an async result that's never awaited or checked; check-then-act on shared state; several writes that must land together with no transaction; a retried operation (webhook, queue job) that isn't idempotent; a `switch` or enum `default` that silently does nothing; a non-null assertion on a value that can be null; off-by-one or empty-collection cases.
- Flag things declared but never wired up: a config option nothing reads, a CLI flag that does nothing, a registry or `switch` that handles four of five types. Users get quietly wrong or missing output.
- Usually fine: a broad catch at the top of a process that logs and exits, or a deliberate best-effort path with a comment saying so.

## 7. Tests

- Flag: frequently changed or fixed code with no tests, tests that assert on implementation details, tests that can't run without network or secrets.
- Don't chase a coverage number. Tie each finding to code that changes or breaks.
- Tools: the project's own coverage command, if it has one.

## 8. Dependencies and config

- Flag: critical or high advisories in code that runs or ships (not every line `npm audit` prints), dependencies nothing uses, two libraries doing one job, a major version far behind on a package that still gets security fixes only on newer lines, environment variables read in code but not documented, defaults that differ between environments without a reason.
- Report a major upgrade as its own issue with what breaks, not as a quick fix.
- Tools: `npm audit` / `pnpm audit`, `pip-audit`, `cargo audit`, `govulncheck`, `npx --no depcheck`.

## 9. Performance

Only with evidence that the code is on a hot path (a request handler, a loop over user data, a render path).

- Flag: N+1 queries, blocking I/O in async code, unbounded caches, queries or list endpoints with no limit or pagination.
- Don't flag: micro-optimizations, or anything you can't connect to a path that runs often.

## 10. Security hygiene

A quick pass, not a security review. For a full one, point the user at `/security-review`.

- Flag: hardcoded secrets, SQL or shell built by string concatenation with outside input, missing authorization checks on a route that has them elsewhere, `*` CORS on an authenticated API, homemade crypto.
- Usually fine: test fixtures with obviously fake keys, a local-dev default documented as such.

## 11. Docs

Leave this to `/update-docs`. If the README's setup steps don't work or the docs contradict the code, report it as one finding that recommends running `/update-docs`, instead of one issue per doc.

## Don't recommend

These come up in generic advice and aren't findings without evidence from this repo:

- A rewrite, a new framework, or a new language.
- Microservices, a plugin system, dependency injection everywhere, or a design pattern by name, with no current pain it removes.
- Splitting files into many smaller ones by line count alone.
- Comments or docstrings everywhere.
- A coverage percentage target.
- Renames across the codebase for taste.
- Formatting or style nits. If formatting is inconsistent, the finding is "add the formatter to CI", once.

## Finding format

Every candidate finding, from a subagent or your own pass, comes back in this shape, so findings merge and vet the same way:

```markdown
### <Short imperative title>

- Evidence: `path:line`, one sentence on what's there. Repeat for the 2–5 strongest locations; add "and ~N similar" if it's wider.
- Cost: what this code pays now (churn, repeated fixes, a test that can't be written, a bug).
- Severity: Critical | High | Medium | Low
- Confidence: High | Medium | Low
- Effort: S | M | L, for the fix including its tests.
- Decided?: any decision record, explaining comment, or suppression with a reason you found nearby, or "none found".
- Fix sketch: one to three sentences, enough to judge the effort.
```
