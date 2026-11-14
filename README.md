# skills

Agent skills I write and use with Claude Code, Codex, and other agents that support the [Agent Skills](https://agentskills.io) format.

## Skills

| Skill | What it does |
| --- | --- |
| [issue](skills/issue/SKILL.md) | Picks an issue from GitHub Issues and works it. |
| [minor](skills/minor/SKILL.md) | Cuts a minor release: bumps `X.Y.Z` to `X.Y+1.0`, then commits and pushes. |
| [patch](skills/patch/SKILL.md) | Cuts a patch release: bumps `X.Y.Z` to `X.Y.Z+1`, then commits and pushes. |
| [title](skills/title/SKILL.md) | Renames the session to match what was actually done in it. |
| [update-docs](skills/update-docs/SKILL.md) | Reviews docs like README.md and AGENTS.md and updates them to match the project. |

## Install

With the [skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add jmusick/skills
```

Or install one by hand by copying (or symlinking) its folder into your agent's skills directory:

```bash
cp -r skills/patch ~/.claude/skills/
```

Claude Code reads `~/.claude/skills/`, Codex reads `~/.codex/skills/`.

## Layout

```
skills/
  <skill-name>/
    SKILL.md        # frontmatter (name, description) + instructions
```

Each skill is one self-contained folder, so it can be copied anywhere on its own. None of them depends on another skill, and none turns off model invocation, so your agent can pick any of them up from plain English as well as from `/<name>` (Claude Code) or `$<name>` (Codex).
