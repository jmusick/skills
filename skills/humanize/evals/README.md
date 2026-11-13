# humanize evals

Run them (billed model runs, so only when asked): `claude plugin eval skills/humanize`

No scaffold or tool grants. Model-invocable, so the routing cases use plain English, and their `Skill` graders are with-only trigger indicators.

## Scenarios

| Case | Status | Source | Ref | Inaction OK | Mutations the free graders caught |
|---|---|---|---|---|---|
| [clean-text-left-alone](clean-text-left-alone/case.yaml) | existing | negative | Existing case, written with skill-creator; not re-sourced in this pass. | yes | - |
| [detect-mode-flags-only](detect-mode-flags-only/case.yaml) | existing | workflow | Existing case, written with skill-creator; not re-sourced in this pass. | no | - |
| [rewrite-keeps-every-fact](rewrite-keeps-every-fact/case.yaml) | existing | workflow | Existing case, written with skill-creator; not re-sourced in this pass. | no | - |
| [triggers-without-slash](triggers-without-slash/case.yaml) | draft | workflow (routing) | description triggers ("sounds like ChatGPT") | no | skill doesn't fire |
| [ap-news-edit-skips-humanize](ap-news-edit-skips-humanize/case.yaml) | draft | neighbouring | description: "Not for AP-style news edits (use newsroom)" | no | skill fires |

Every case's source is `confirmed_by: none`: no user has confirmed it's real work yet. "Draft" means its free graders passed the self-test below but no person has reviewed the case.

## Coverage: humanize at 3ad6668ce90d, suite humanize/evals

| Area | Scenarios | Status | Notes |
|---|---|---|---|
| Happy path | rewrite-keeps-every-fact | existing |  |
| Branches | detect-mode-flags-only | existing | File mode (edit a file in place) isn't tested |
| Recovery | none |  | Not applicable |
| Ambiguity | none |  | Not decided yet |
| Constraints | rewrite-keeps-every-fact | existing | no added facts |
| Negative tasks | clean-text-left-alone | existing |  |
| Neighbouring tasks | ap-news-edit-skips-humanize | draft | Plain proofreading isn't tested |

Draft scenarios (they don't cover anything until reviewed): triggers-without-slash, ap-news-edit-skips-humanize.

Hypotheses not yet confirmed by a user: triggers-without-slash and ap-news-edit-skips-humanize, from the description.

Not covered, by decision: being called by prospect (tested from prospect's drafts-email-from-saved-pages).

Self-test (2026-11-13): each new or repaired case's free graders (regex, file_exists, tool_used) were scored locally, without a model, on the untouched scaffold, a reference solution, and the mutations in the table. Every reference passed, every mutation failed, and every untouched workspace failed unless inaction is a valid answer. The LLM graders weren't run or calibrated. A pass shows the free graders are sane on those cases; it doesn't show the cases are relevant or that the suite covers the skill.
