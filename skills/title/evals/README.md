# title evals

Run them (billed model runs, so only when asked): `claude plugin eval skills/title`

No scaffold. In an eval run there's no tool that renames the session, so both cases test the documented no-rename-tool branch. drifted-unfinished-chat resumes `history.jsonl`, a hand-written transcript in Claude Code's session format; the eval docs don't define that format, so check the first run for a resume error before trusting its result.

## Scenarios

| Case | Status | Source | Ref | Inaction OK | Mutations the free graders caught |
|---|---|---|---|---|---|
| [drifted-unfinished-chat](drifted-unfinished-chat/case.yaml) | draft | workflow + fixed-failure | SKILL.md step 2 (name where it ended, unfinished work, no secrets); secrets rule from c64a4e01ae38 | no | pretends to rename, leaks the password, gives a bare title |
| [exact-title-given](exact-title-given/case.yaml) | draft | workflow | SKILL.md (exact title given) | no | pretends to rename, rewrites the title |

Every case's source is `confirmed_by: none`: no user has confirmed it's real work yet. "Draft" means its free graders passed the self-test below but no person has reviewed the case.

## Coverage: title at 3ad6668ce90d, suite title/evals

| Area | Scenarios | Status | Notes |
|---|---|---|---|
| Happy path | drifted-unfinished-chat | draft | The desktop-app rename (set_session_title) can't run in an eval |
| Branches | exact-title-given | draft | Guidance text ("/title focus on ...") isn't tested |
| Recovery | none |  | Not applicable |
| Ambiguity | none |  | Two threads joined in one title isn't tested |
| Constraints | drifted-unfinished-chat | draft | no secrets in the title |
| Negative tasks | none |  | Not applicable: the skill always proposes a title |
| Neighbouring tasks | none |  | Manual-only skill |

Draft scenarios (they don't cover anything until reviewed): drifted-unfinished-chat, exact-title-given.

Hypotheses not yet confirmed by a user: both, from SKILL.md.

Not covered, by decision: titles in another language.

Self-test (2026-11-13): each new or repaired case's free graders (regex, file_exists, tool_used) were scored locally, without a model, on the untouched scaffold, a reference solution, and the mutations in the table. Every reference passed, every mutation failed, and every untouched workspace failed unless inaction is a valid answer. The LLM graders weren't run or calibrated. A pass shows the free graders are sane on those cases; it doesn't show the cases are relevant or that the suite covers the skill.
