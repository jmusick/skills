# seo-audit evals

Run them (billed model runs, so only when asked): `claude plugin eval skills/seo-audit --scaffold`

The scaffold copies each case's fixture site into the workspace.

## Scenarios

| Case | Status | Source | Ref | Inaction OK | Mutations the free graders caught |
|---|---|---|---|---|---|
| [astro-site-audit](astro-site-audit/case.yaml) | existing | workflow | Existing case, written with skill-creator; not re-sourced in this pass. Read-only graders are now tool checks (08, 08b). | no | - |
| [clean-page-left-alone](clean-page-left-alone/case.yaml) | existing | negative | Existing case, written with skill-creator; not re-sourced in this pass. | yes | - |
| [hreflang-two-h1](hreflang-two-h1/case.yaml) | existing | workflow | Existing case, written with skill-creator; not re-sourced in this pass. Read-only graders are now tool checks (06, 06b). | no | - |
| [js-injected-schema](js-injected-schema/case.yaml) | existing | workflow | Existing case, written with skill-creator; not re-sourced in this pass. Read-only graders are now tool checks (06, 06b). | no | - |
| [retired-advice-bait](retired-advice-bait/case.yaml) | existing | constraint | Existing case, written with skill-creator; not re-sourced in this pass. | no | - |
| [vite-spa-meta-in-js](vite-spa-meta-in-js/case.yaml) | existing | workflow | Existing case, written with skill-creator; not re-sourced in this pass. Grader 03 split into file regexes (03-03c) plus an LLM check on the file (03d). | no | title-only fix |

Every case's source is `confirmed_by: none`: no user has confirmed it's real work yet. "Draft" means its free graders passed the self-test below but no person has reviewed the case.

## Coverage: seo-audit at 3ad6668ce90d, suite seo-audit/evals

| Area | Scenarios | Status | Notes |
|---|---|---|---|
| Happy path | astro-site-audit | existing |  |
| Branches | hreflang-two-h1, js-injected-schema, vite-spa-meta-in-js | existing |  |
| Recovery | none |  | Not decided yet |
| Ambiguity | none |  | Not decided yet |
| Constraints | retired-advice-bait | existing |  |
| Negative tasks | clean-page-left-alone | existing |  |
| Neighbouring tasks | none |  | Manual-only skill |

Draft scenarios (they don't cover anything until reviewed): none.

Hypotheses not yet confirmed by a user: none recorded.

Not covered, by decision: live checks (Core Web Vitals, Search Console).

Self-test (2026-11-13): each new or repaired case's free graders (regex, file_exists, tool_used) were scored locally, without a model, on the untouched scaffold, a reference solution, and the mutations in the table. Every reference passed, every mutation failed, and every untouched workspace failed unless inaction is a valid answer. The LLM graders weren't run or calibrated. A pass shows the free graders are sane on those cases; it doesn't show the cases are relevant or that the suite covers the skill.
