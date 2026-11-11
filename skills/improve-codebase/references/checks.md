# What to look for

Work through the sections that fit the scope. Each section lists what to flag, what usually isn't a problem, and tools that help. A tool's output is a lead: open the code before it becomes a finding.

Run a listed tool only if it's already installed or in the project's dependencies. For the `npx` ones, write `npx --no <tool>`, which refuses to download a package the project doesn't have.

## Severity

- **Critical:** the code is wrong or unsafe now, or nothing can be verified. A hardcoded live credential, an injection path, data loss, no working test or build command on a project that ships.
- **High:** it keeps costing time or bugs in code that changes often. Logic duplicated across a hotspot so fixes keep missing a copy, a god file in the busiest area, swallowed errors on a critical path, a high-churn path with no tests.
- **Medium:** a real cost in code that changes sometimes. A pass-through layer, inconsistent ways of doing one thing, loose types at a boundary, an unused dependency.
- **Low:** a small, contained cleanup. A dead helper, one magic value, a stale flag.

## 1. Verification baseline

Check this first. Every other fix depends on it.

- Flag: no test command, a red test suite or build on the default branch, a linter or typechecker that's configured but not run in CI, tests that are skipped or quarantined with no reason, CI that doesn't run on pull requests.
- Usually fine: a small script or prototype repo with no tests, when its README says so. Report it as a question, not a defect.

## 2. Structure

- **Pass-through layers.** Classes or modules whose methods mostly forward to something else; "Manager", "Helper", "Service", "Utils" names with thin bodies; an interface nearly as big as its implementation. Apply the deletion test.
- **Scattered concepts.** Understanding or changing one concept means touching many small files. Propose merging them into one module that owns the concept.
- **Leaky abstractions.** Public types that expose internal representation; callers forced to sequence calls (`startX()` then `finishX()` instead of `x()`); methods that exist only for tests.
- **Logic in the wrong layer.** Business rules in views or handlers, UI state in models, feature checks sprinkled through shared code, the same config read from several places.
- **Special-case growth.** One-off flags, nullable modes, and `if` branches bolted onto a busy function. Often a missing type or a missing separate path.
- **Size.** Files over roughly 500 lines or functions over roughly 80 are worth a look, not automatically a finding. Ask whether they hold more than one concept. Generated files, data tables, and test fixtures are fine.
- **Cycles.** Circular imports between modules.
- Tools: `npx madge --circular src` (JS/TS), `pydeps --show-cycles` (Python), `go vet ./...`.

## 3. Duplication and consistency

- Flag: the same logic in three or more places; copy-paste with small variations (the variation is usually a missing parameter); several ways to do one thing (two HTTP clients, three date helpers, four error types for one failure); a new helper written next to an existing one that does the same job.
- Usually fine: two similar blocks that change for different reasons; duplicated test setup that keeps each test readable.

## 4. Dead code

- Flag: unused code and dependencies, feature flags that are always on or off, compatibility shims and fallbacks with no remaining caller.
- Before calling something dead, search for dynamic uses: string-based lookups, reflection, plugin registries, framework conventions (routes, migrations, entry points named in config), public API a library exports for others.
- Tools: `npx knip` (JS/TS), `vulture` (Python), `cargo machete` or `cargo udeps` (Rust), `staticcheck` (Go), `npx depcheck`.

## 5. Types and contracts

- Flag: `any`, `as` casts, `# type: ignore`, `@ts-ignore`, and untyped dicts at module boundaries; optional parameters or fields that hide a real invariant; silent fallbacks that paper over an unclear contract; input from users, files, or the network used without validation.
- Usually fine: a cast at a well-marked interop edge with a comment saying why.
- Tools: `tsc --noEmit`, `mypy`, `pyright`.

## 6. Errors and resilience

- Flag: errors swallowed where the caller needed to know, inconsistent error shapes from one module, outbound calls with no timeout, unbounded retries, unclosed resources.
- Usually fine: a broad catch at the top of a process that logs and exits, or a deliberate best-effort path with a comment saying so.

## 7. Tests

- Flag: frequently changed or fixed code with no tests, tests that assert on implementation details, tests that can't run without network or secrets.
- Don't chase a coverage number. Tie each finding to code that changes or breaks.
- Tools: the project's own coverage command, if it has one.

## 8. Dependencies and config

- Flag: known vulnerabilities, dependencies nothing uses, two libraries doing one job, a major version far behind on a package that still gets security fixes only on newer lines, environment variables read in code but not documented, defaults that differ between environments without a reason.
- Report a major upgrade as its own issue with what breaks, not as a quick fix.
- Tools: `npm audit` / `pnpm audit`, `pip-audit`, `cargo audit`, `govulncheck`, `npx depcheck`.

## 9. Performance

Only with evidence that the code is on a hot path (a request handler, a loop over user data, a render path).

- Flag: N+1 queries, blocking I/O in async code, unbounded caches.
- Don't flag: micro-optimizations, or anything you can't connect to a path that runs often.

## 10. Security hygiene

A quick pass, not a security review. For a full one, point the user at `/security-review`.

- Flag: hardcoded secrets (cite the location and kind, never the value), SQL or shell built by string concatenation with outside input, missing authorization checks on a route that has them elsewhere, `*` CORS on an authenticated API, homemade crypto.
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
