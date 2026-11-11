# Sizing an issue

Read this at step 3 to pick the model and effort an issue calls for, and to decide whether to stop for a model switch.

| Size | Examples | Claude (model / effort) | Codex (model / effort) |
| --- | --- | --- | --- |
| Trivial | Typo, docs wording, config value, one-line fix | haiku / low | gpt-6-luna / low |
| Small | A bug with an obvious cause in one function, a small change with a pattern to copy | sonnet / low | gpt-6-luna / high |
| Normal | A bug or small feature in one area, a few files, existing tests to follow | sonnet / medium | gpt-6.1-sol / low |
| Large | A feature that spans a few modules, new tests to write, some design choices | opus / high | gpt-6.1-sol / medium |
| Hard | Changes across several modules, new design, concurrency, security, data migrations, a bug with an unclear cause | opus / xhigh | gpt-6.1-sol / high |
| Hardest | Only a Hard issue that clears the bar below | fable / medium | gpt-6-astra / medium |

Hardest has a high bar because the top models cost far more per token. Difficulty alone stops at Hard, and so does going up a size when unsure. Use Hardest only for a Hard issue where one of these holds:
- The user asked for the top model on this issue.
- An earlier attempt at Hard failed, as the issue's comments or a closed PR show.
- A miss couldn't be undone after release, such as a migration that rewrites production data.

Note the size, the reason, and any Hardest condition in the report, and in the PR with `--branch`.

Don't go to `max` or `ultra` by default: they spend far more for the last bit of quality, and Codex's `ultra` spawns its own subagents. If an issue seems to need them, ask the user. On another agent, map the rows onto its small, mid, and top tiers. Model lineups change, so if a listed model isn't offered, use the nearest tier that is. When unsure, go up a size: a too-weak model costs a review round, which costs more.

## The model-fit stop

Compare models by tier, ignoring effort: haiku < sonnet < opus < fable, and gpt-6-luna < gpt-6.1-sol < gpt-6-astra. Stop before starting when this session's model is below the one the size calls for (a too-weak model costs a review round), or two or more tiers above it (opus on a Trivial issue, fable on a Small or Normal one), and tell the user, e.g. "#42 looks trivial (a one-line config fix). Haiku at low effort can handle it. Switch in the model menu (`/model` in the CLI) and say go, or say go to stay." Only the user can switch, and switching now is cheapest because a switch drops the prompt cache. Fold this into any step 2 questions so the run stops once. A model one tier above the size, or an effort level off, isn't worth the pause: note the better fit in the report and go. If the session fits, or if you can't tell, don't stop.
