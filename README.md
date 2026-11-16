# skills

Agent skills I write and use with Claude Code, Codex, and other agents that support the [Agent Skills](https://agentskills.io) format.

## Skills

| Skill | What it does |
| --- | --- |
| [commit](skills/commit/SKILL.md) | Commits the current work with [Conventional Commits](https://www.conventionalcommits.org) messages. |
| [daily-news](skills/daily-news/SKILL.md) | Runs [Firelands Current](https://firelandscurrent.com)'s daily news budget: sweeps the paper's sources, verifies and drafts the best stories, and writes a review packet for the editor. Built for that paper's repo and its `packet.mjs` publishing tool. Needs `newsroom`. |
| [humanize](skills/humanize/SKILL.md) | Rewrites or audits text so it stops reading as AI-generated, keeping its meaning, facts, and voice. Built on Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). |
| [issue](skills/issue/SKILL.md) | Picks an open GitHub issue, works it, reviews it, pauses for you to test it, and commits the change so the issue closes when it's released. It can also work on its own branch with a PR, on several issues in parallel, or unattended. Needs `commit`; uses `update-docs` and Claude Code's `/code-review` when present. |
| [newsroom](skills/newsroom/SKILL.md) | Writes, edits, and checks news stories and headlines in AP style, following your publication's house style when the project has one, with story-type playbooks and editor flags. |
| [release](skills/release/SKILL.md) | Cuts a release: works out the version bump from the Conventional Commits since the last tag, then tags and pushes. When nothing calls for a version, it still pushes the pending commits. |
| [title](skills/title/SKILL.md) | Renames the session to match what was actually done in it. |
| [update-docs](skills/update-docs/SKILL.md) | Checks docs like README.md and AGENTS.md against the code, fixes what's no longer true, and proposes cleanups for stale or duplicated docs. |

## Options

Each skill runs with no options. These change what it does. Type them after the command (`/` in Claude Code, `$` in Codex), or say them in plain English. `release` has no options.

| Skill | Option | What it does |
| --- | --- | --- |
| commit | `/commit <files>` | Commits only the named files and leaves the rest uncommitted. |
| daily-news | `--unattended` | Runs without stopping to ask, then imports the packet into local dev, syncs it to production and queues the Facebook posts. Anything that would need a decision is held for the editor instead. |
| daily-news | `--date YYYY-MM-DD` | Builds the packet for that day instead of today. |
| humanize | "audit", "scan", "flag only", or "is this AI?" | Lists each AI-writing pattern it finds, with a fix, without rewriting. It never guesses who wrote the text. |
| humanize | a file path | Edits the prose in that file in place, leaving code, commands, and frontmatter alone. |
| issue | `/issue 42` | Works issue 42, or resumes it if an earlier run left your PR open. With no number, it picks the most important open issue it can finish. |
| issue | `/issue 12 15 18` | Works those issues in parallel, one subagent per issue in its own worktree. |
| issue | `--batch [N]` | Picks a batch of up to N issues (default 4) and works them in parallel. |
| issue | `--branch` | Works in its own worktree on a new branch and opens a PR, leaving your checkout alone. You review and merge it. |
| issue | `--no-test` | Runs unattended: skips the local-dev test pause and every other stop to ask. Pairs with `/loop /issue --no-test` for a backlog. |
| newsroom | "edit" | Revises your draft instead of writing a new one, and says what changed. |
| newsroom | "check", "AP check", "review", or "flag only" | Lists problems as editor flags, each with a fix, without rewriting. |
| title | `/title <title>` | Uses that exact title as written. |
| title | `/title <guidance>` | Picks the title itself, following the guidance (`shorter`, `focus on the deploy fix`). |
| update-docs | `/update-docs <files>` | Checks only the named docs and skips the organization review. |

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
    scripts/        # optional: code the skill runs
    references/     # optional: docs the skill reads only when it needs them
    assets/         # optional: templates the skill fills in
```

Most skills are a single `SKILL.md`. Some carry helper scripts for checks that are easy to get wrong by reading. They need Python 3 (standard library only), and each skill does the check by hand without it.

- `release`: `scripts/next_version.py` runs the pre-release checks and sorts the commits since the last tag by the bump each calls for.
- `update-docs`: `scripts/doc_links.py` checks links and anchors, plus a privacy-policy checklist it reads only when a repo has one.

Each skill is one self-contained folder, so it can be copied anywhere on its own. The sources a skill was built from are credited in [REFERENCES.md](REFERENCES.md) rather than in the skill's folder. Two skills depend on another: `issue` commits through `commit`, and `daily-news` writes its stories with `newsroom`, so install each pair together. `issue` also runs `update-docs` and Claude Code's built-in `/code-review` when they're installed, and checks by hand when they're not. None turns off model invocation, so your agent can pick any of them up from plain English as well as from `/<name>` (Claude Code) or `$<name>` (Codex).

`commit` and `release` are meant as a pair: commit each piece of work as you go, then run `release` when you want to ship what's built up. Each works on its own too, since `release` reads any Conventional Commits history.
