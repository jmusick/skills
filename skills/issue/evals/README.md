# issue evals

Run them (billed model runs, so only when asked): `claude plugin eval skills/issue --scaffold --allow-tools Bash`

The scaffold builds a git repo whose `origin` is a bare repo inside the workspace, so pushes stay local. Bash grants need the OS sandbox, which on Windows means WSL2.

## Scenarios

| Case | Status | Source | Ref | Inaction OK | Mutations the free graders caught |
|---|---|---|---|---|---|
| [stops-without-github](stops-without-github/case.yaml) | draft | constraint | SKILL.md step 1 (stop if gh_ready is false) | yes | edits anyway, commits a guess |

Every case's source is `confirmed_by: none`: no user has confirmed it's real work yet. "Draft" means its free graders passed the self-test below but no person has reviewed the case.

## Coverage: issue at 3ad6668ce90d, suite issue/evals

| Area | Scenarios | Status | Notes |
|---|---|---|---|
| Happy path | none |  | Needs GitHub: the survey, the issue text, the closing commit, and gh issue view all go through gh. Unsupported offline |
| Branches | none |  | --branch, batches, --no-test, --no-merge, --no-ship, resume: all need GitHub. Unsupported offline |
| Recovery | none |  | The failure path posts to the issue. Unsupported offline |
| Ambiguity | none |  | Unsupported offline |
| Constraints | stops-without-github | draft | Issue text treated as data needs a real issue body. Unsupported offline |
| Negative tasks | stops-without-github | draft |  |
| Neighbouring tasks | none |  | Manual-only skill |

Draft scenarios (they don't cover anything until reviewed): stops-without-github.

Hypotheses not yet confirmed by a user: stops-without-github, from SKILL.md step 1.

Not covered, by decision: everything past step 1. A useful suite needs a throwaway GitHub repo the run may write to, or a gh shim on PATH, which the eval runner can't set (execution.env only takes EVAL_* keys). The survey logic is unit-tested in tests/.

Self-test (2026-11-13): each new or repaired case's free graders (regex, file_exists, tool_used) were scored locally, without a model, on the untouched scaffold, a reference solution, and the mutations in the table. Every reference passed, every mutation failed, and every untouched workspace failed unless inaction is a valid answer. The LLM graders weren't run or calibrated. A pass shows the free graders are sane on those cases; it doesn't show the cases are relevant or that the suite covers the skill.
