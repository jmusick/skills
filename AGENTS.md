# AGENTS.md

This repo holds agent skills in the [Agent Skills](https://agentskills.io) format. There is no build, package manager, or test suite. The files are the product.

CI (`.github/workflows/ci.yml`) calls the shared [jmusick/ci](https://github.com/jmusick/ci) baseline (a secret scan, plus dependency review on pull requests), pinned by commit SHA; Dependabot (`.github/dependabot.yml`) keeps the GitHub Actions pins current. The **CI gate** job is the one check to require.

## Layout

- `skills/<name>/SKILL.md`: one folder per skill. The folder name must match the `name` in the frontmatter. Each skill is currently this one file, with no scripts, references, evals, or Codex settings.
- `README.md`: the public index. Keep its skills table in sync when you add, rename, or remove a skill.

`skills/patch/SKILL.md` and `skills/minor/SKILL.md` are twins: they differ only in the name, description, and bump rule. Keep everything else the same in both.

## Writing a skill

- Frontmatter needs `name` (lowercase, hyphens) and `description`.
- The description is the only text the agent sees when deciding whether to use a skill. Say what the skill does, then the phrases and situations that should trigger it, in the words users type.
- Every line of `SKILL.md` costs context on every run, so keep only what the model wouldn't do unaided.
- Write instructions in the imperative, and explain why a step exists when the reason isn't obvious.
- A skill gets copied or symlinked on its own, so it can't reference files outside its own folder. If it calls another skill by name, say so in the README so people install both.
- No skill sets `disable-model-invocation: true` or ships an `agents/openai.yaml`, so all of them are model-invocable. If you make one manual-only, add both (the `agents/openai.yaml` with `policy: allow_implicit_invocation: false` for Codex), and leave out any skill another skill calls, since these settings also stop one skill from calling another.

## Commits

Use short imperative subjects, e.g. `Add title skill` or `patch: tighten the bump rule`.
