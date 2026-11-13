# daily-budget evals

Run them (billed model runs, so only when asked): `claude plugin eval skills/daily-budget --scaffold --allow-tools Bash`

The scaffold needs Python. It puts a stand-in repo and project library inside the workspace and the prompt names them, so a run never reaches the real firelands-current checkout or library.

## Scenarios

| Case | Status | Source | Ref | Inaction OK | Mutations the free graders caught |
|---|---|---|---|---|---|
| [offline-day-holds-leads](offline-day-holds-leads/case.yaml) | draft | constraint + fixed-failure | SKILL.md steps 1-2, 4, 8-9 and Boundaries; no dated sections in news-sources.md from d18c97f43ac7 | no | logs a dated source section, imports, writes no packet, skips check_packet |

Every case's source is `confirmed_by: none`: no user has confirmed it's real work yet. "Draft" means its free graders passed the self-test below but no person has reviewed the case.

## Coverage: daily-budget at 3ad6668ce90d, suite daily-budget/evals

| Area | Scenarios | Status | Notes |
|---|---|---|---|
| Happy path | none |  | A real sweep needs the live web and a signed-in browser. Unsupported offline |
| Branches | none |  | Updates, events, images, newsroom drafting: need verified leads from live sources. Unsupported offline |
| Recovery | offline-day-holds-leads | draft | no source reachable |
| Ambiguity | none |  | Not decided yet |
| Constraints | offline-day-holds-leads | draft | no import, sync, --remote, or commit; no dated source sections |
| Negative tasks | offline-day-holds-leads | draft | valid output is a packet with no stories |
| Neighbouring tasks | none |  | Manual-only skill |

Draft scenarios (they don't cover anything until reviewed): offline-day-holds-leads.

Hypotheses not yet confirmed by a user: offline-day-holds-leads, from SKILL.md and commit history.

Not covered, by decision: a sweep over saved pages: possible, but news-sources.md would need a local mirror of each source, and the skill would still try the live URLs first.

Self-test (2026-11-13): each new or repaired case's free graders (regex, file_exists, tool_used) were scored locally, without a model, on the untouched scaffold, a reference solution, and the mutations in the table. Every reference passed, every mutation failed, and every untouched workspace failed unless inaction is a valid answer. The LLM graders weren't run or calibrated. A pass shows the free graders are sane on those cases; it doesn't show the cases are relevant or that the suite covers the skill.
