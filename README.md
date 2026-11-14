# skills

Agent skills I write and use with Claude Code, Codex, and other agents that support the [Agent Skills](https://agentskills.io) format.

## Skills

| Skill | What it does |
| --- | --- |
| [commit](skills/commit/SKILL.md) | Commits the current work with [Conventional Commits](https://www.conventionalcommits.org) messages. |
| [issue](skills/issue/SKILL.md) | Picks an issue from GitHub Issues and works it. |
| [release](skills/release/SKILL.md) | Cuts a release: works out the version bump from the Conventional Commits since the last tag, then tags and pushes. |
| [title](skills/title/SKILL.md) | Renames the session to match what was actually done in it. |
| [update-docs](skills/update-docs/SKILL.md) | Reviews docs like README.md and AGENTS.md and updates them to match the project. |

## Install

With the [skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add jmusick/skills
```

Or install one by hand by copying (or symlinking) its folder into your agent's skills directory:

```bash
cp -r skills/release ~/.claude/skills/
```

Claude Code reads `~/.claude/skills/`, Codex reads `~/.codex/skills/`.

## Layout

```
skills/
  <skill-name>/
    SKILL.md        # frontmatter (name, description) + instructions
```

Each skill is one self-contained folder, so it can be copied anywhere on its own. None of them depends on another skill, and none turns off model invocation, so your agent can pick any of them up from plain English as well as from `/<name>` (Claude Code) or `$<name>` (Codex).

`commit` and `release` are meant as a pair: commit each piece of work as you go, then run `release` when you want to ship what's built up. Each works on its own too, since `release` reads any Conventional Commits history.
