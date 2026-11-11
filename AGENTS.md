# AGENTS.md

This repo holds agent skills in the [Agent Skills](https://agentskills.io) format. There is no build or package manager. The only tests are the eval cases some skills carry and unit tests for the issue skill's scripts. The files are the product.

CI (`.github/workflows/ci.yml`) calls the shared [jmusick/ci](https://github.com/jmusick/ci) baseline (a secret scan, plus dependency review on pull requests), pinned by commit SHA; Dependabot (`.github/dependabot.yml`) proposes new releases and keeps the pins current. The **CI gate** job is the one check to require.

## Layout

- `skills/<name>/SKILL.md`: one folder per skill. The folder name must match the `name` in the frontmatter.
- `skills/<name>/scripts/`: optional helper scripts the skill tells the agent to run.
- `skills/<name>/tests/`: optional standard-library unit tests for the skill's scripts. They test the scripts' own logic (not the projects the skills work on) and run offline. Run them only when you change those scripts: `python -m unittest discover -s skills/<name>/tests`.
- `skills/<name>/references/`: optional extra docs the skill loads only when needed.
- `skills/<name>/agents/openai.yaml`: Codex-only settings. Here it just turns off implicit invocation.
- `skills/<name>/evals/`: optional eval cases, one folder per case (`prompt.md`, `case.yaml`, `graders/`), in the layout skill-creator writes and `claude plugin eval` runs. They're real, billed model runs, so run them only when asked: `claude plugin eval skills/<name>`. When you change a skill that has evals, update any grader the change makes wrong. A case can also carry `files/`, a fixture project that its `scaffold_script` (`place-files.sh`) copies into the sandbox. Nothing installs those fixtures, so Dependabot alerts and PRs on their `package.json` files don't affect anyone using the skills.
- `README.md`: the public index. Keep its skills table in sync when you add, rename, or remove a skill.

## Writing a skill

Draft new skills with skill-creator and review existing ones with `/improve-skills`. Where their defaults differ from the rules below, these rules win.

- Frontmatter needs `name` (lowercase, hyphens) and `description`.
- For a model-invocable skill, the description is the only text the agent sees when deciding whether to use it. Say what the skill does, then the phrases and situations that should trigger it, in the words users type, key use case first (long skill lists get their descriptions cut). Agents tend to undertrigger, so name every distinct case, but don't repeat one case in synonyms. Say what it is *not* for only where a near miss or a sibling skill competes for the same words.
- For a manual-only skill (see below), the agent never sees the description, so one sentence on what the skill does is enough.
- Every line of `SKILL.md` costs context on every run, so keep only what the model wouldn't do unaided: no definitions, generic advice, or restated repo facts. Stay under ~500 lines, and move material only some runs need into `references/`, linked at the step that needs it.
- Write instructions in the imperative, and explain why a step exists when the reason isn't obvious. A rule with its reason generalizes; an all-caps MUST gets over-applied or argued away.
- A skill gets copied or symlinked on its own, so it can't reference files outside its own folder. It can call another skill by name (daily-budget uses newsroom, prospect uses humanize); say so in the README so people install both.
- Skills run only when the user invokes them: add `disable-model-invocation: true` to the frontmatter for Claude Code, and an `agents/openai.yaml` with `policy: allow_implicit_invocation: false` for Codex. The exception is a skill another skill calls (newsroom, humanize, update-docs): leave it model-invocable, because these settings also stop one skill from calling another. If a skill starts calling one that has them, remove both from the one being called. Eval prompts for a flagged skill must start with `/<name>`, since the agent won't pick it up from plain English.

## Shared code

`skills/minor/scripts/version_info.py`, `skills/patch/scripts/version_info.py` and `skills/issue/scripts/version_info.py` are intentionally identical copies, because a skill can't read files from another skill's folder. If you change one copy, make the same change in the others.

The `<!-- agent-waiting-for-reply -->` marker in `skills/issue/references/failure.md` must match `WAITING_MARKER` in `skills/issue/scripts/issue_survey.py`. Change them together.

`skills/patch/SKILL.md` and `skills/minor/SKILL.md` are twins too: they differ only in the name, description, bump rule, and example releases. Keep everything else the same in both.

Steps 8 and 9 of `skills/issue/SKILL.md` do the same release as `/patch` and `/minor` (bump, one `vX.Y.Z - Summary` commit, tag, push) inline, because those two are manual-only and calling them would mean dropping that guard. When you change how `/patch` or `/minor` bumps, writes the commit, or tags, make the matching change there.

## Scripts

- Scripts should run with only the Python standard library (or plain shell) so they work wherever the skill is installed.
- Skills invoke them as `python` with a `python3` fallback, so keep them compatible with both names on Windows, macOS, and Linux.

## Commits

Use short imperative subjects, e.g. `Add title skill` or `humanize: tighten the hedging rules`.
