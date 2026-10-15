# skills

Agent skills I write and use with Claude Code, Codex, and other agents that support the [Agent Skills](https://agentskills.io) format.

## Skills

| Skill | What it does |
| --- | --- |
| [daily-budget](skills/daily-budget/SKILL.md) | Sweeps Firelands Current's sources for new stories, events and images, drafts the best leads with newsroom, and builds a dated review packet for the editor. |
| [design-taste](skills/design-taste/SKILL.md) | Audits, polishes, or checks web UI so it stops reading as AI-generated: the dated tells registry, the accessibility and typography floor, motion timing, and a two-round screenshot critique. |
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

## Credits

Some skills distill what the most-used public skills on the same subject agree on. These notes live here rather than in each `SKILL.md`, because an agent loads `SKILL.md` into its context and gets nothing from them.

- **humanize:** the consensus of ten anti-AI-writing skills: blader/humanizer, stop-slop, no-ai-slop, Cursor's unslop, avoid-ai-writing, sepia, academic-humanizer, antislop, theclaymethod/unslop, and anti-ai-slop-writing. Each rule appears in most of them.
- **design-taste:** what Anthropic's frontend-design, Leonxlnx/taste-skill, pbakaus/impeccable, Vercel's web-interface-guidelines, ui-ux-pro-max, emilkowalski/skills, jakubkrehel/skills, Google's stitch taste-design, and ConardLi's web-design-engineer agree on. Most of the motion guidance comes from emilkowalski/skills and jakubkrehel/skills.
- **newsroom:** builds on the `newsroom-style` skill in [jamditis/claude-skills-journalism](https://github.com/jamditis/claude-skills-journalism) (MIT; see [NOTICE.md](skills/newsroom/NOTICE.md)), keeping the rules that most published newsroom skills agree on, with Firelands Current's own rules on top.
