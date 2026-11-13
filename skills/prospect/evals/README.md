# prospect evals

Run them (billed model runs, so only when asked): `claude plugin eval skills/prospect --scaffold`

Saved pages stand in for the web.

## Scenarios

| Case | Status | Source | Ref | Inaction OK | Mutations the free graders caught |
|---|---|---|---|---|---|
| [drafts-email-from-saved-pages](drafts-email-from-saved-pages/case.yaml) | existing | workflow | Existing case, written with skill-creator; not re-sourced in this pass. | no | - |
| [facebook-when-no-email](facebook-when-no-email/case.yaml) | existing | workflow | Existing case, written with skill-creator; not re-sourced in this pass. | no | - |
| [passes-when-no-real-problem](passes-when-no-real-problem/case.yaml) | existing | negative | Existing case, written with skill-creator; not re-sourced in this pass. Added file checks for the excluded businesses (04b, 04c). | yes | - |
| [skips-business-already-contacted](skips-business-already-contacted/case.yaml) | existing | constraint | Existing case, written with skill-creator; not re-sourced in this pass. Grader 04 is now a file check on Outreach/. | yes | - |

Every case's source is `confirmed_by: none`: no user has confirmed it's real work yet. "Draft" means its free graders passed the self-test below but no person has reviewed the case.

## Coverage: prospect at 3ad6668ce90d, suite prospect/evals

| Area | Scenarios | Status | Notes |
|---|---|---|---|
| Happy path | drafts-email-from-saved-pages | existing |  |
| Branches | facebook-when-no-email | existing | Contact-form channel isn't tested |
| Recovery | none |  | Not decided yet |
| Ambiguity | none |  | Not decided yet |
| Constraints | skips-business-already-contacted | existing | never sends |
| Negative tasks | passes-when-no-real-problem | existing |  |
| Neighbouring tasks | none |  | Manual-only skill |

Draft scenarios (they don't cover anything until reviewed): none.

Hypotheses not yet confirmed by a user: none recorded.

Not covered, by decision: follow-ups on a due date; live research.

Self-test (2026-11-13): only the free graders added in this pass were checked, on the untouched scaffold and one wrong action each. The existing LLM graders weren't run or calibrated.
