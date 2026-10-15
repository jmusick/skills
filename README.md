# skills

Agent skills I write and use with Claude Code, Codex, and other agents that support the [Agent Skills](https://agentskills.io) format.

## Skills

| Skill | What it does |
| --- | --- |
| [humanize](skills/humanize/SKILL.md) | Rewrites or audits text so it stops reading as AI-generated, keeping the meaning and the writer's voice. |
| [minor](skills/minor/SKILL.md) | Cuts a minor release: bumps `X.Y.Z` to `X.Y+1.0`, updates the changelog, commits, tags, and pushes. |
| [newsroom](skills/newsroom/SKILL.md) | Writes, edits, and checks news stories for Firelands Current in AP style, with house rules, story-type playbooks, and editor flags. |
| [patch](skills/patch/SKILL.md) | Cuts a patch release: bumps `X.Y.Z` to `X.Y.Z+1`, updates the changelog, commits, tags, and pushes. |
| [title](skills/title/SKILL.md) | Renames the current chat session to match what actually happened in it. |

## Install

With the [skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add jmusick/skills
```

Or install one by hand by copying (or symlinking) its folder into your agent's skills directory:

```bash
cp -r skills/humanize ~/.claude/skills/
```

Claude Code reads `~/.claude/skills/`, Codex reads `~/.codex/skills/`.

## Layout

```
skills/
  <skill-name>/
    SKILL.md        # frontmatter (name, description) + instructions
    scripts/        # optional helper scripts the skill runs
    references/     # optional docs the skill loads on demand
```

Each skill folder is self-contained so it can be copied anywhere on its own.
