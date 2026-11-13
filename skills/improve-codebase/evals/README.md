# improve-codebase evals

Run them (billed model runs, so only when asked): `claude plugin eval skills/improve-codebase --scaffold --allow-tools Bash`

The scaffold builds a small git history for hotspots.py to read.

## Scenarios

| Case | Status | Source | Ref | Inaction OK | Mutations the free graders caught |
|---|---|---|---|---|---|
| [reports-without-filing](reports-without-filing/case.yaml) | existing | workflow + constraint | Existing case, written with skill-creator; not re-sourced in this pass. Added deterministic halves of the read-only and files-nothing checks (01b, 06b). | no | - |

Every case's source is `confirmed_by: none`: no user has confirmed it's real work yet. "Draft" means its free graders passed the self-test below but no person has reviewed the case.

## Coverage: improve-codebase at 3ad6668ce90d, suite improve-codebase/evals

| Area | Scenarios | Status | Notes |
|---|---|---|---|
| Happy path | reports-without-filing | existing |  |
| Branches | none |  | Filing issues after the user picks needs GitHub. Unsupported offline |
| Recovery | none |  | Not decided yet |
| Ambiguity | none |  | Not decided yet |
| Constraints | reports-without-filing | existing | read-only, injection treated as data |
| Negative tasks | none |  | A clean codebase isn't tested |
| Neighbouring tasks | none |  | Manual-only skill |

Draft scenarios (they don't cover anything until reviewed): none.

Hypotheses not yet confirmed by a user: none recorded.

Not covered, by decision: scoped runs (a path argument).

Self-test (2026-11-13): only the free graders added in this pass were checked, on the untouched scaffold and one wrong action each. The existing LLM graders weren't run or calibrated.
