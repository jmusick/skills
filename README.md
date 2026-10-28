# skills

Agent skills I write and use with Claude Code, Codex, and other agents that support the [Agent Skills](https://agentskills.io) format.

## Skills

| Skill | What it does |
| --- | --- |
| [daily-budget](skills/daily-budget/SKILL.md) | Sweeps Firelands Current's sources for new stories, events and images, drafts the best leads with newsroom, and builds a dated review packet for the editor. |
| [design-taste](skills/design-taste/SKILL.md) | Audits, polishes, or checks web UI so it stops reading as AI-generated: the dated tells registry, the accessibility and typography floor, motion timing, and a two-round screenshot critique. |
| [humanize](skills/humanize/SKILL.md) | Rewrites or audits text so it stops reading as AI-generated, keeping the meaning and the writer's voice. |
| [issue](skills/issue/SKILL.md) | Picks a GitHub issue, offers a cheaper model when the job is small, does the work in its own worktree, reviews it, updates the docs it affected, pauses for you to test it in local dev, bumps the version in the PR, squash-merges it as one `vX.Y.Z` release commit, tags it, cleans up its branches, and retitles the chat. |
| [minor](skills/minor/SKILL.md) | Cuts a minor release: bumps `X.Y.Z` to `X.Y+1.0`, updates the changelog, commits, tags, and pushes. |
| [music-creation](skills/music-creation/SKILL.md) | Writes, revises, and critiques songs, lyrics, melodies, and arrangements, prepares ready-to-paste Suno packages, and can plan an EP or album. |
| [newsroom](skills/newsroom/SKILL.md) | Writes, edits, and checks news stories for Firelands Current in AP style, with house rules, story-type playbooks, and editor flags. |
| [patch](skills/patch/SKILL.md) | Cuts a patch release: bumps `X.Y.Z` to `X.Y.Z+1`, updates the changelog, commits, tags, and pushes. |
| [sprite](skills/sprite/SKILL.md) | Makes pixel-art sprites for Chomp Chomp Panic!: generates each animation with Codex CLI's image tool from a structured prompt and a reference image, then snaps it onto the game's frame grid, palette and outline and writes the strips the Unity importer expects. Needs [Codex CLI](https://github.com/openai/codex) installed and logged in. |
| [title](skills/title/SKILL.md) | Renames the current chat session to match what actually happened in it. |
| [update-docs](skills/update-docs/SKILL.md) | Audits README, AGENTS.md, CLAUDE.md, CHANGELOG, the privacy policy, and other docs against the code and fixes what's wrong or out of date. |
| [wave](skills/wave/SKILL.md) | Picks a wave of non-overlapping GitHub issues, hands each to a subagent on the model and effort its size calls for, reviews every diff and updates the docs it affected, ships each issue one at a time as its own squash-merged, tagged `vX.Y.Z` release, and retitles the chat. |

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
    evals/          # optional test cases for skill-creator or `claude plugin eval`
```

Each skill folder holds all of its own files, so it can be copied anywhere on its own. Some skills call another skill: daily-budget needs newsroom installed too. Issue and wave run update-docs on each change before it ships and title at the end of the run, so install those alongside them; without them, issue and wave check the docs by hand and leave the chat's title alone. They also fall back to patch and minor when a repo can't squash-merge or the user merges a PR themselves.

## Credits

Some skills distill what the most-used public skills on the same subject agree on. These notes live here rather than in each `SKILL.md`, because an agent loads `SKILL.md` into its context and gets nothing from them.

- **humanize:** the consensus of ten anti-AI-writing skills: blader/humanizer, stop-slop, no-ai-slop, Cursor's unslop, avoid-ai-writing, sepia, academic-humanizer, antislop, theclaymethod/unslop, and anti-ai-slop-writing. Each rule appears in most of them.
- **design-taste:** what Anthropic's frontend-design, Leonxlnx/taste-skill, pbakaus/impeccable, Vercel's web-interface-guidelines, ui-ux-pro-max, emilkowalski/skills, jakubkrehel/skills, Google's stitch taste-design, and ConardLi's web-design-engineer agree on. Most of the motion guidance comes from emilkowalski/skills and jakubkrehel/skills.
- **update-docs:** draws on Anthropic's claude-md-improver, getsentry's agents-md, amelnagdy's docs-guard (checking each doc statement as a claim), giuseppe-trisciuoglio's docs-updater, ruchernchong's sync-docs, iliaal's md-docs, tartinerlabs' update-project, and laurigates' docs-sync (catalog and count drift).
- **music-creation:** what four songwriting skill collections agree on: [bitwize-music-studio/claude-ai-music-skills](https://github.com/bitwize-music-studio/claude-ai-music-skills) (CC0), jtydhr88's [music-composition-skills](https://github.com/jtydhr88/music-composition-skills) and [lyric-writing-skills](https://github.com/jtydhr88/lyric-writing-skills), and melodic-software's [songwriting plugin](https://github.com/melodic-software/claude-code-plugins/tree/main/plugins/songwriting) (MIT; see [NOTICE.md](skills/music-creation/NOTICE.md)). [source-synthesis.md](skills/music-creation/references/source-synthesis.md) maps each rule to the sources behind it.
- **sprite:** the prompt structure (a logical pixel grid with an exact nearest-neighbor enlargement, a ranked detail budget, and the AI-cliché blocklist with its "don't make it plain" guard) adapts The Sprite Wizard's "prompt bible" from r/aigamedev, whose own pipeline runs generated art through their [Sprite Grid](https://thespritewizard.itch.io/sprite-grid) processor the way `sprite_clean.py` does here.
- **newsroom:** builds on the `newsroom-style` skill in [jamditis/claude-skills-journalism](https://github.com/jamditis/claude-skills-journalism) (MIT; see [NOTICE.md](skills/newsroom/NOTICE.md)), keeping the rules that most published newsroom skills agree on, with Firelands Current's own rules on top.
