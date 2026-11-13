# music-creation evals

Run them (billed model runs, so only when asked): `claude plugin eval skills/music-creation`

No scaffold or tool grants. Prompt-only cases; the outcome rests on the LLM graders, which haven't been calibrated.

## Scenarios

| Case | Status | Source | Ref | Inaction OK | Mutations the free graders caught |
|---|---|---|---|---|---|
| [critique-only-keeps-voice](critique-only-keeps-voice/case.yaml) | draft | workflow | SKILL.md Deliver ("A critique-only request gets critique") | no | rewrites the lyrics |
| [second-verse-only](second-verse-only/case.yaml) | draft | workflow | SKILL.md "Match the size of the answer" and the invented-detail rule | no | returns the whole song |
| [suno-package-keeps-lyrics](suno-package-keeps-lyrics/case.yaml) | draft | workflow | references/suno.md (separate pasteable fields; supplied lyrics stay as written) | no | rewrites a lyric line, claims to have generated the track |
| [instrumental-plan-no-lyrics](instrumental-plan-no-lyrics/case.yaml) | draft | workflow | SKILL.md Deliver (an instrumental gets a musical plan) | no | adds lyrics |

Every case's source is `confirmed_by: none`: no user has confirmed it's real work yet. "Draft" means its free graders passed the self-test below but no person has reviewed the case.

## Coverage: music-creation at 3ad6668ce90d, suite music-creation/evals

| Area | Scenarios | Status | Notes |
|---|---|---|---|
| Happy path | suno-package-keeps-lyrics | draft |  |
| Branches | critique-only-keeps-voice, second-verse-only, instrumental-plan-no-lyrics | draft | EP/album planning (albums.md) isn't tested |
| Recovery | none |  | Suno generation problems (a mispronounced name) aren't tested |
| Ambiguity | none |  | A thin concept (offer directions or ask one question) isn't tested |
| Constraints | suno-package-keeps-lyrics, critique-only-keeps-voice | draft | the writer's words stay theirs; no claims of hearing or rendering |
| Negative tasks | none |  | "Already strong, stop" isn't tested |
| Neighbouring tasks | none |  | Manual-only skill |

Draft scenarios (they don't cover anything until reviewed): critique-only-keeps-voice, second-verse-only, suno-package-keeps-lyrics, instrumental-plan-no-lyrics.

Hypotheses not yet confirmed by a user: all four, from SKILL.md and references.

Not covered, by decision: melody and harmony claims checked against notation.

Self-test (2026-11-13): each new or repaired case's free graders (regex, file_exists, tool_used) were scored locally, without a model, on the untouched scaffold, a reference solution, and the mutations in the table. Every reference passed, every mutation failed, and every untouched workspace failed unless inaction is a valid answer. The LLM graders weren't run or calibrated. A pass shows the free graders are sane on those cases; it doesn't show the cases are relevant or that the suite covers the skill.
