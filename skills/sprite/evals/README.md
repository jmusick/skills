# sprite evals

Run them (billed model runs, so only when asked): `claude plugin eval skills/sprite --allow-tools Bash`

Bash, the Codex CLI signed in with network access, and the chomp-chomp-panic checkout at C:/Users/JD/source/chomp-chomp-panic: the cases read the real game repo, so they run only on this machine.

## Scenarios

| Case | Status | Source | Ref | Inaction OK | Mutations the free graders caught |
|---|---|---|---|---|---|
| [redo-cat-walk](redo-cat-walk/case.yaml) | existing | workflow | Existing case, written with skill-creator; not re-sourced in this pass. Added tool checks for writes into the game repo (07b, 07c). | no | - |
| [redo-office-worker](redo-office-worker/case.yaml) | existing | workflow | Existing case, written with skill-creator; not re-sourced in this pass. Added tool checks for writes into the game repo (07b, 07c). | no | - |
| [redo-taxi-side](redo-taxi-side/case.yaml) | existing | workflow | Existing case, written with skill-creator; not re-sourced in this pass. Added tool checks for writes into the game repo (07b, 07c). | no | - |

Every case's source is `confirmed_by: none`: no user has confirmed it's real work yet. "Draft" means its free graders passed the self-test below but no person has reviewed the case.

## Coverage: sprite at 3ad6668ce90d, suite sprite/evals

| Area | Scenarios | Status | Notes |
|---|---|---|---|
| Happy path | redo-cat-walk, redo-office-worker, redo-taxi-side | existing |  |
| Branches | none |  | A new sprite with no existing art isn't tested |
| Recovery | none |  | Codex missing or signed out (stop and say how to install) isn't tested |
| Ambiguity | none |  | Not decided yet |
| Constraints | all three | existing | game repo untouched |
| Negative tasks | none |  | Not decided yet |
| Neighbouring tasks | none |  | Manual-only skill |

Draft scenarios (they don't cover anything until reviewed): none.

Hypotheses not yet confirmed by a user: none recorded.

Not covered, by decision: exact pixel checks: graders 01-05 in each case (strip size, binary alpha, palette, outline color, baseline row) ask an LLM judge to verify pixels it can't count, so a pass there isn't evidence. They need a pixel-check script run on test_output by hand; the eval runner has no code graders.

Self-test (2026-11-13): only the free graders added in this pass were checked, on the untouched scaffold and one wrong action each. The existing LLM graders weren't run or calibrated.
