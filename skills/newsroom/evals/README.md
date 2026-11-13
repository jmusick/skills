# newsroom evals

Run them (billed model runs, so only when asked): `claude plugin eval skills/newsroom`

No scaffold or tool grants. Model-invocable, so the routing case uses plain English and its `Skill` grader is a with-only trigger indicator.

## Scenarios

| Case | Status | Source | Ref | Inaction OK | Mutations the free graders caught |
|---|---|---|---|---|---|
| [check-mode-flags-only](check-mode-flags-only/case.yaml) | existing | workflow | Existing case, written with skill-creator; not re-sourced in this pass. | no | - |
| [meeting-notes-no-invented-names](meeting-notes-no-invented-names/case.yaml) | existing | workflow | Existing case, written with skill-creator; not re-sourced in this pass. | no | - |
| [notes-trigger-without-slash](notes-trigger-without-slash/case.yaml) | draft | workflow (routing) | description triggers ("turning notes ... into stories") | no | skill doesn't fire |

Every case's source is `confirmed_by: none`: no user has confirmed it's real work yet. "Draft" means its free graders passed the self-test below but no person has reviewed the case.

## Coverage: newsroom at 3ad6668ce90d, suite newsroom/evals

| Area | Scenarios | Status | Notes |
|---|---|---|---|
| Happy path | meeting-notes-no-invented-names | existing |  |
| Branches | check-mode-flags-only | existing | Obituaries, features, and headline-only requests aren't tested |
| Recovery | none |  | Not applicable |
| Ambiguity | none |  | Not decided yet |
| Constraints | meeting-notes-no-invented-names, notes-trigger-without-slash | draft | no invented names or facts |
| Negative tasks | none |  | Opinion columns and press releases written for an organization (the "Not for" list) aren't tested |
| Neighbouring tasks | none |  | De-AI requests (humanize) aren't tested from this side |

Draft scenarios (they don't cover anything until reviewed): notes-trigger-without-slash.

Hypotheses not yet confirmed by a user: notes-trigger-without-slash, from the description.

Not covered, by decision: being called by daily-budget (needs a live sweep).

Self-test (2026-11-13): each new or repaired case's free graders (regex, file_exists, tool_used) were scored locally, without a model, on the untouched scaffold, a reference solution, and the mutations in the table. Every reference passed, every mutation failed, and every untouched workspace failed unless inaction is a valid answer. The LLM graders weren't run or calibrated. A pass shows the free graders are sane on those cases; it doesn't show the cases are relevant or that the suite covers the skill.
