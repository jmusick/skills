# patch evals

Run them (billed model runs, so only when asked): `claude plugin eval skills/patch --scaffold --allow-tools Bash`

The scaffold builds a git repo whose `origin` is a bare repo inside the workspace, so pushes stay local. Bash grants need the OS sandbox, which on Windows means WSL2. The fixture's checks are `python -m unittest`.

## Scenarios

| Case | Status | Source | Ref | Inaction OK | Mutations the free graders caught |
|---|---|---|---|---|---|
| [release-promotes-unreleased](release-promotes-unreleased/case.yaml) | draft | workflow + fixed-failure | SKILL.md steps 1-5; Unreleased promotion and fetch-first from c64a4e01ae38 | no | duplicate changelog section, AI trailer, tag not pushed, tests skipped, force push |
| [stop-when-next-tag-on-origin](stop-when-next-tag-on-origin/case.yaml) | draft | constraint | SKILL.md "When to stop and ask" (next tag exists); fetch-first from c64a4e01ae38 | yes | releases anyway, tags without pushing |
| [feature-work-asks-about-minor](feature-work-asks-about-minor/case.yaml) | draft | constraint | SKILL.md step 2 (work fits a different bump) | yes | releases anyway, tags without pushing |

Every case's source is `confirmed_by: none`: no user has confirmed it's real work yet. "Draft" means its free graders passed the self-test below but no person has reviewed the case.

## Coverage: patch at 3ad6668ce90d, suite patch/evals

| Area | Scenarios | Status | Notes |
|---|---|---|---|
| Happy path | release-promotes-unreleased | draft |  |
| Branches | release-promotes-unreleased | draft | Python/pyproject and lightweight tags only; npm and annotated tags are covered in minor's suite, which runs the same steps |
| Recovery | none |  | A failing check after the bump (stop and report) isn't tested |
| Ambiguity | feature-work-asks-about-minor | draft |  |
| Constraints | stop-when-next-tag-on-origin, release-promotes-unreleased | draft | no force push, no AI trailer |
| Negative tasks | none |  | Nothing to release (no commits since the tag) isn't tested |
| Neighbouring tasks | none |  | Manual-only skill: it never fires on its own, so routing has nothing to test |

Draft scenarios (they don't cover anything until reviewed): release-promotes-unreleased, stop-when-next-tag-on-origin, feature-work-asks-about-minor.

Hypotheses not yet confirmed by a user: all three: written from SKILL.md and commit history, not from a reported run.

Not covered, by decision: detached HEAD, mid-rebase, versions disagree, no remote, secrets in the tree, a repo-specific release step in AGENTS.md.

Self-test (2026-11-13): each new or repaired case's free graders (regex, file_exists, tool_used) were scored locally, without a model, on the untouched scaffold, a reference solution, and the mutations in the table. Every reference passed, every mutation failed, and every untouched workspace failed unless inaction is a valid answer. The LLM graders weren't run or calibrated. A pass shows the free graders are sane on those cases; it doesn't show the cases are relevant or that the suite covers the skill.
