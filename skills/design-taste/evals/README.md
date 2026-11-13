# design-taste evals

Run them (billed model runs, so only when asked): `claude plugin eval skills/design-taste --scaffold --allow-tools Bash`

Lint_tells.py runs through Bash. No browser is available in a run, so the screenshot steps can't run and the graders expect them marked not verified.

## Scenarios

| Case | Status | Source | Ref | Inaction OK | Mutations the free graders caught |
|---|---|---|---|---|---|
| [audit-flags-without-editing](audit-flags-without-editing/case.yaml) | draft | workflow | SKILL.md Modes (audit), hard rules 2 and 5, Report | no | fixes during the audit, findings without file:line |
| [polish-keeps-brief](polish-keeps-brief/case.yaml) | draft | workflow + constraint | SKILL.md hard rules 1-3 and the quality floor | no | zoom still disabled, no focus style, brand color changed, new invented proof, image without alt, div button kept, product facts lost, lint skipped |

Every case's source is `confirmed_by: none`: no user has confirmed it's real work yet. "Draft" means its free graders passed the self-test below but no person has reviewed the case.

## Coverage: design-taste at 3ad6668ce90d, suite design-taste/evals

| Area | Scenarios | Status | Notes |
|---|---|---|---|
| Happy path | polish-keeps-brief | draft |  |
| Branches | audit-flags-without-editing | draft | Build mode and references/direction.md aren't tested |
| Recovery | none |  | Not decided yet |
| Ambiguity | none |  | Not decided yet |
| Constraints | polish-keeps-brief | draft | the brief wins; no invented proof |
| Negative tasks | none |  | A page that needs nothing ("say so and stop") isn't tested |
| Neighbouring tasks | none |  | Manual-only skill |

Draft scenarios (they don't cover anything until reviewed): audit-flags-without-editing, polish-keeps-brief.

Hypotheses not yet confirmed by a user: both, from SKILL.md.

Not covered, by decision: the screenshot critique loop and motion rules: they need a browser in the run.

Self-test (2026-11-13): each new or repaired case's free graders (regex, file_exists, tool_used) were scored locally, without a model, on the untouched scaffold, a reference solution, and the mutations in the table. Every reference passed, every mutation failed, and every untouched workspace failed unless inaction is a valid answer. The LLM graders weren't run or calibrated. A pass shows the free graders are sane on those cases; it doesn't show the cases are relevant or that the suite covers the skill.
