# AGENTS.md

This repo holds agent skills in the [Agent Skills](https://agentskills.io) format. There is no build, package manager, or test suite. The files are the product.

CI (`.github/workflows/ci.yml`) calls the shared [jmusick/ci](https://github.com/jmusick/ci) baseline (a secret scan, plus dependency review on pull requests), pinned by commit SHA; Dependabot (`.github/dependabot.yml`) keeps the GitHub Actions pins current. The **CI gate** job is the one check to require.

## Layout

- `skills/<name>/SKILL.md`: one folder per skill. The folder name must match the `name` in the frontmatter. Most skills are this one file. update-docs also has `scripts/doc_links.py` and `references/privacy-policy.md`. No skill has evals or Codex settings.
- `README.md`: the public index. Keep its skills table in sync when you add, rename, or remove a skill, and its options table in sync with every argument, flag, or mode a skill accepts.
- `REFERENCES.md`: the outside sources each skill was built from, one section per skill, with pins to diff from. Credit sources here, not in the skill's folder, and update the section when a skill changes what it takes from them.

## Writing a skill

- Frontmatter needs `name` (lowercase, hyphens) and `description`.
- The description is the only text the agent sees when deciding whether to use a skill. Say what the skill does, then the phrases and situations that should trigger it, in the words users type.
- Every line of `SKILL.md` costs context on every run, so keep only what the model wouldn't do unaided.
- Put a mechanical check the model does unreliably by reading (like resolving links) in `scripts/`, using only the standard library and with a by-hand fallback. Put material only some runs need in `references/`. Point to each from `SKILL.md` and say when to use it.
- Write instructions in the imperative, and explain why a step exists when the reason isn't obvious.
- A skill gets copied or symlinked on its own, so it can't reference files outside its own folder. If it calls another skill by name, say so in the README so people install both.
- No skill sets `disable-model-invocation: true` or ships an `agents/openai.yaml`, so all of them are model-invocable. If you make one manual-only, add both (the `agents/openai.yaml` with `policy: allow_implicit_invocation: false` for Codex), and leave out any skill another skill calls, since these settings also stop one skill from calling another.

## Commits

Use [Conventional Commits](https://www.conventionalcommits.org), with the skill name as the scope: `feat(title): add trigger phrases`, `fix(release): stop on uncommitted changes`, `docs: update the skills table`. The type sets the next version, so pick it by what changes for people using the skill: `feat` for something new (minor), `fix` for a correction (patch), `!` after the type for a breaking change such as a rename or removal (major), and `docs`, `chore`, or `ci` for anything that doesn't change a skill's behavior (no release).

Commit as you go, and cut releases with the `release` skill, which tags `vX.Y.Z` and pushes. There are no version files, so the tags are the version.
