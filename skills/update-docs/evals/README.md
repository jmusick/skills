# update-docs evals

Run them (billed model runs, so only when asked): `claude plugin eval skills/update-docs --scaffold --allow-tools Bash`

Model-invocable, so prompts are plain English and the `Skill` graders are with-only trigger indicators.

## Scenarios

| Case | Status | Source | Ref | Inaction OK | Mutations the free graders caught |
|---|---|---|---|---|---|
| [fixes-drift-proposes-delete](fixes-drift-proposes-delete/case.yaml) | draft | workflow | SKILL.md steps 1, 3, 7, 8 and the two levels of authority | no | deletes without approval, changes code to match docs, dates a release, puts the entry under a released version, leaves the README stale, commits |
| [audit-only-applies-nothing](audit-only-applies-nothing/case.yaml) | draft | workflow | SKILL.md "audit" / "check only" rule | yes | applies fixes, edits with sed |
| [scoped-to-diff](scoped-to-diff/case.yaml) | draft | workflow + fixed-failure | SKILL.md limited runs (how issue calls it), from 9587e6d52df2 | no | does a full run instead, reverts the user's change, doesn't fix the README |
| [new-doc-request-skips-skill](new-doc-request-skips-skill/case.yaml) | draft | neighbouring | description: "Not for writing new docs" | no | skill fires, copies the stale README command |

Every case's source is `confirmed_by: none`: no user has confirmed it's real work yet. "Draft" means its free graders passed the self-test below but no person has reviewed the case.

## Coverage: update-docs at 3ad6668ce90d, suite update-docs/evals

| Area | Scenarios | Status | Notes |
|---|---|---|---|
| Happy path | fixes-drift-proposes-delete | draft |  |
| Branches | audit-only-applies-nothing, scoped-to-diff | draft | Privacy policy checks and dated-record status lines (full-audit.md) aren't tested |
| Recovery | none |  | Not decided yet |
| Ambiguity | none |  | Contradictions the code can't settle ("Needs your call") aren't tested |
| Constraints | fixes-drift-proposes-delete, scoped-to-diff | draft | docs only, no commit, no structural change without approval |
| Negative tasks | none |  | An already-accurate repo (report and change nothing) isn't tested |
| Neighbouring tasks | new-doc-request-skips-skill | draft | De-AI'ing prose (humanize) isn't tested |

Draft scenarios (they don't cover anything until reviewed): fixes-drift-proposes-delete, audit-only-applies-nothing, scoped-to-diff, new-doc-request-skips-skill.

Hypotheses not yet confirmed by a user: all four, from SKILL.md.

Not covered, by decision: the second turn, where the user approves numbered proposals: it needs a resumed transcript.

Self-test (2026-11-13): each new or repaired case's free graders (regex, file_exists, tool_used) were scored locally, without a model, on the untouched scaffold, a reference solution, and the mutations in the table. Every reference passed, every mutation failed, and every untouched workspace failed unless inaction is a valid answer. The LLM graders weren't run or calibrated. A pass shows the free graders are sane on those cases; it doesn't show the cases are relevant or that the suite covers the skill.
