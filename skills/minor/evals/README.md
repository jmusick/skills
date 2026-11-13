# minor evals

Run them (billed model runs, so only when asked): `claude plugin eval skills/minor --scaffold --allow-tools Bash`

The scaffold builds a git repo whose `origin` is a bare repo inside the workspace, so pushes stay local. Bash grants need the OS sandbox, which on Windows means WSL2. The fixture's checks are `npm test` (`node --test`), so Node must be installed.

## Scenarios

| Case | Status | Source | Ref | Inaction OK | Mutations the free graders caught |
|---|---|---|---|---|---|
| [release-feature-npm](release-feature-npm/case.yaml) | draft | workflow | SKILL.md steps 1-5, step 3's package.json reformat check | no | npm reformat kept, lockfile missed, changelog created, lightweight tag, tests skipped, force push |
| [stop-when-work-breaks-use](stop-when-work-breaks-use/case.yaml) | draft | constraint | SKILL.md step 2 (breaking change is a major) | yes | releases anyway |
| [stop-when-behind-upstream](stop-when-behind-upstream/case.yaml) | draft | constraint | SKILL.md "When to stop and ask" (branch behind upstream) | yes | releases anyway, pulls to catch up, discards the uncommitted work |

Every case's source is `confirmed_by: none`: no user has confirmed it's real work yet. "Draft" means its free graders passed the self-test below but no person has reviewed the case.

## Coverage: minor at 3ad6668ce90d, suite minor/evals

| Area | Scenarios | Status | Notes |
|---|---|---|---|
| Happy path | release-feature-npm | draft |  |
| Branches | release-feature-npm | draft | npm, annotated tags, no changelog; Python and changelogs are covered in patch's suite |
| Recovery | none |  | A failing check after the bump isn't tested |
| Ambiguity | stop-when-work-breaks-use | draft |  |
| Constraints | stop-when-behind-upstream, release-feature-npm | draft | no pull/rebase/merge, no force push |
| Negative tasks | none |  | Nothing to release isn't tested |
| Neighbouring tasks | none |  | Manual-only skill |

Draft scenarios (they don't cover anything until reviewed): release-feature-npm, stop-when-work-breaks-use, stop-when-behind-upstream.

Hypotheses not yet confirmed by a user: all three: written from SKILL.md, not from a reported run.

Not covered, by decision: the same stop cases as patch; SKILL.md is a twin, so each suite tests some of them.

Self-test (2026-11-13): each new or repaired case's free graders (regex, file_exists, tool_used) were scored locally, without a model, on the untouched scaffold, a reference solution, and the mutations in the table. Every reference passed, every mutation failed, and every untouched workspace failed unless inaction is a valid answer. The LLM graders weren't run or calibrated. A pass shows the free graders are sane on those cases; it doesn't show the cases are relevant or that the suite covers the skill.
