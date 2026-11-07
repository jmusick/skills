# AGENTS.md

This repo holds agent skills in the [Agent Skills](https://agentskills.io) format. There is no build, no package manager, and no test suite beyond the eval cases some skills carry. The files are the product.

## Layout

- `skills/<name>/SKILL.md`: one folder per skill. The folder name must match the `name` in the frontmatter.
- `skills/<name>/scripts/`: optional helper scripts the skill tells the agent to run.
- `skills/<name>/references/`: optional extra docs the skill loads only when needed.
- `skills/<name>/agents/openai.yaml`: Codex-only settings. Here it just turns off implicit invocation.
- `skills/<name>/evals/`: optional eval cases, one folder per case (`prompt.md`, `case.yaml`, `graders/`), in the layout skill-creator writes and `claude plugin eval` runs. They're real, billed model runs, so run them only when asked: `claude plugin eval skills/<name>`. When you change a skill that has evals, update any grader the change makes wrong. A case can also carry `files/`, a fixture project that its `scaffold_script` (`place-files.sh`) copies into the sandbox. Nothing installs those fixtures, so Dependabot alerts and PRs on their `package.json` files don't affect anyone using the skills.
- `README.md`: the public index. Keep its skills table in sync when you add, rename, or remove a skill.

## Writing a skill

- Frontmatter needs `name` (lowercase, hyphens) and `description`. The description is what the agent sees when deciding whether to use the skill. Say what the skill does, list the phrases and situations that should trigger it, and say what it is *not* for, so it doesn't fire on near misses.
- Keep `SKILL.md` short enough to read in one pass (under ~500 lines). Move long reference material into `references/` and link to it.
- Write instructions in the imperative, and explain why a step exists when the reason isn't obvious. Agents follow rules better when they know what the rule protects.
- A skill gets copied or symlinked on its own, so it can't reference files outside its own folder. It can call another skill by name (daily-budget uses newsroom); say so in the README so people install both.
- Skills run only when the user invokes them: add `disable-model-invocation: true` to the frontmatter for Claude Code, and an `agents/openai.yaml` with `policy: allow_implicit_invocation: false` for Codex. The exception is a skill another skill calls (newsroom, update-docs, title, patch, minor): leave it model-invocable, because these settings also stop one skill from calling another. If a skill starts calling one that has them, remove both from the one being called. Eval prompts for a flagged skill must start with `/<name>`, since the agent won't pick it up from plain English.

## Shared code

`skills/minor/scripts/version_info.py`, `skills/patch/scripts/version_info.py`, `skills/issue/scripts/version_info.py` and `skills/wave/scripts/version_info.py` are intentionally identical copies, because a skill can't read files from another skill's folder. So are `skills/issue/scripts/issue_survey.py` and `skills/wave/scripts/issue_survey.py`. If you change one copy, make the same change in the others.

`skills/patch/SKILL.md` and `skills/minor/SKILL.md` are twins too: they differ only in the name, description, bump rule, and example releases. Keep everything else the same in both.

## Scripts

- Scripts should run with only the Python standard library (or plain shell) so they work wherever the skill is installed.
- Skills invoke them as `python` with a `python3` fallback, so keep them compatible with both names on Windows, macOS, and Linux.

## Commits

Use short imperative subjects, e.g. `Add title skill` or `humanize: tighten the hedging rules`.
