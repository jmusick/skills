# skills

Agent skills I write and use with Claude Code, Codex, and other agents that support the [Agent Skills](https://agentskills.io) format.

## Skills

| Skill | What it does |
| --- | --- |
| [daily-budget](skills/daily-budget/SKILL.md) | Sweeps Firelands Current's sources for new stories, events and images, drafts the best leads with newsroom, and builds a dated review packet for the editor. |
| [design-taste](skills/design-taste/SKILL.md) | Audits, polishes, or checks web UI so it stops reading as AI-generated: the dated tells registry, the accessibility and typography floor, motion timing, and a two-round screenshot critique. |
| [humanize](skills/humanize/SKILL.md) | Rewrites or audits text so it stops reading as AI-generated, keeping the meaning and the writer's voice. |
| [improve-codebase](skills/improve-codebase/SKILL.md) | Audits a codebase for the improvements most worth making, weighted toward the files git history says change and break most, checks every finding against the code, reports a short ranked list with a "looks bad but is fine" section, and files the findings you pick as GitHub issues ready for issue or wave. Never edits code. |
| [improve-skills](skills/improve-skills/SKILL.md) | Audits agent skills for what makes them misfire, get ignored, or waste context, with a bundled checker for frontmatter, links, invocation settings, and eval prompts. Checks each finding against the files and the skill's git history, gives each skill a keep, improve, merge, or retire verdict, then makes the fixes you pick and has a fresh subagent compare old and new. |
| [issue](skills/issue/SKILL.md) | Picks a GitHub issue, offers a cheaper model when the job is small, does the work in its own worktree, reviews it, updates the docs it affected, pauses for you to test it in local dev, bumps the version in the PR, squash-merges it as one `vX.Y.Z` release commit, tags it, cleans up its branches, and retitles the chat. |
| [minor](skills/minor/SKILL.md) | Cuts a minor release: bumps `X.Y.Z` to `X.Y+1.0`, updates the changelog, commits, tags, and pushes. |
| [music-creation](skills/music-creation/SKILL.md) | Writes, revises, and critiques songs, lyrics, melodies, and arrangements, prepares ready-to-paste Suno packages, and can plan an EP or album. |
| [newsroom](skills/newsroom/SKILL.md) | Writes, edits, and checks news stories for Firelands Current in AP style, with house rules, story-type playbooks, and editor flags. |
| [patch](skills/patch/SKILL.md) | Cuts a patch release: bumps `X.Y.Z` to `X.Y.Z+1`, updates the changelog, commits, tags, and pushes. |
| [seo-audit](skills/seo-audit/SKILL.md) | Audits a site or web project for search problems (crawling, indexing, canonicals, titles, structured data, link previews, JavaScript rendering, AI-crawler access) with a bundled raw-HTML checker, traces each finding to the template that causes it, and fixes it on request. |
| [sprite](skills/sprite/SKILL.md) | Makes pixel-art sprites for Chomp Chomp Panic!: generates each animation with Codex CLI's image tool from a structured prompt and a reference image, then snaps it onto the game's frame grid, palette and outline and writes the strips the Unity importer expects. Needs [Codex CLI](https://github.com/openai/codex) installed and logged in. |
| [title](skills/title/SKILL.md) | Renames the current chat session to match what actually happened in it. |
| [update-docs](skills/update-docs/SKILL.md) | Audits README, AGENTS.md, CLAUDE.md, CHANGELOG, the privacy policy, and other docs against the code and fixes what's wrong or out of date, then finds contradictions, stale records, and docs to consolidate or delete, and proposes structural changes for approval. |
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
    agents/         # optional Codex settings (openai.yaml)
    evals/          # optional test cases for skill-creator or `claude plugin eval`
```

Each skill folder holds all of its own files, so it can be copied anywhere on its own. Some skills call another skill: daily-budget needs newsroom installed too. Issue and wave run update-docs on each change before it ships and title at the end of the run, so install those alongside them; without them, issue and wave check the docs by hand and leave the chat's title alone. They also fall back to patch and minor when a repo can't squash-merge or the user merges a PR themselves. Improve-codebase files issues for issue and wave to work, and leaves docs drift to update-docs.

Most skills run only when you invoke them: `disable-model-invocation: true` in the frontmatter does that for Claude Code (`/<name>`), and `agents/openai.yaml` does it for Codex (`$<name>`). Newsroom, update-docs, title, patch, and minor are left out, because other skills call them and these settings would block that.

## Credits

Some skills distill what the most-used public skills on the same subject agree on. These notes live here rather than in each `SKILL.md`, because an agent loads `SKILL.md` into its context and gets nothing from them.

- **humanize:** the consensus of ten anti-AI-writing skills: blader/humanizer, stop-slop, no-ai-slop, Cursor's unslop, avoid-ai-writing, sepia, academic-humanizer, antislop, theclaymethod/unslop, and anti-ai-slop-writing. Each rule appears in most of them.
- **design-taste:** what Anthropic's frontend-design, Leonxlnx/taste-skill, pbakaus/impeccable, Vercel's web-interface-guidelines, ui-ux-pro-max, emilkowalski/skills, jakubkrehel/skills, Google's stitch taste-design, and ConardLi's web-design-engineer agree on. Most of the motion guidance comes from emilkowalski/skills and jakubkrehel/skills.
- **update-docs:** draws on Anthropic's claude-md-improver, getsentry's agents-md, amelnagdy's docs-guard (checking each doc statement as a claim), giuseppe-trisciuoglio's docs-updater, ruchernchong's sync-docs, iliaal's md-docs, tartinerlabs' update-project, and laurigates' docs-sync (catalog and count drift).
- **improve-codebase:** what about twenty codebase-improvement skills agree on, led by Matt Pocock's improve-codebase-architecture and codebase-design (the deletion test, deep modules, git-history hotspots) and shadcn's improve (vetting subagent findings, self-contained plans). Also: ksimback's tech-debt-audit (the required "looks bad but is actually fine" section), max4c's improve-codebase, tomzx's improve-codebase, Cursor's thermo-nuclear-code-quality-review and deslop, Anthropic's knowledge-work-plugins tech-debt, juliusbrussee/caveman's safe-refactor, chrisallenlane's refactor, jnsahaj's zero-tech-debt, and wondelai's remove-technical-debt.
- **improve-skills:** what fifteen skill-writing and skill-improvement skills agree on, beyond Anthropic's and OpenAI's skill-creators: mattpocock's writing-for-agents (context pointers, no-ops, positive phrasing over bans), obra/superpowers' writing-skills (baseline first, and matching the form of a fix to the failure), dotnet's improve-skill-quality (classify the failure before editing, retirement as a valid outcome), Warp's skill-doctor (change only what would have prevented a real failure), alchaincyf's darwin-skill (paired before/after judging), Trail of Bits' skill-improver (don't weaken a guarantee to close a finding), affaan-m/ecc's skill-stocktake (keep, improve, merge, retire verdicts), softaworks' skill-judge (knowledge delta), Grafana's skill-authoring, mcollina's skill-optimizer, sanyuan0704's skill-review, daymade's skill-reviewer, tradermonty's dual-axis-skill-reviewer, Expo's skill-eval, and dboeckli's skill-best-practices.
- **music-creation:** what four songwriting skill collections agree on: [bitwize-music-studio/claude-ai-music-skills](https://github.com/bitwize-music-studio/claude-ai-music-skills) (CC0), jtydhr88's [music-composition-skills](https://github.com/jtydhr88/music-composition-skills) and [lyric-writing-skills](https://github.com/jtydhr88/lyric-writing-skills), and melodic-software's [songwriting plugin](https://github.com/melodic-software/claude-code-plugins/tree/main/plugins/songwriting) (MIT; see [NOTICE.md](skills/music-creation/NOTICE.md)). [source-synthesis.md](skills/music-creation/references/source-synthesis.md) maps each rule to the sources behind it.
- **seo-audit:** what the most-installed SEO skills agree on: coreyhaines31/marketingskills' seo-audit, addyosmani/web-quality-skills' seo, AgriciDaniel/claude-seo, firecrawl's seo-audit, resciencelab/opc-skills' seo-geo, zubair-trabzada/geo-seo-claude, Anthropic's knowledge-work-plugins seo-audit, affaan-m/ecc's seo, sanity-io's seo-aeo-best-practices, aaron-he-zhu's technical-seo-checker, and Bhanunamikaze/Agentic-SEO-Skill, with the fix loop from squirrelscan's audit-website. Where they disagree, the skill follows Google's current documentation. The "look before you recommend" rule comes from [seo-skill-bench](https://github.com/aleclindz/seo-skill-bench), where skills lost the most points for "fixing" things that were already fine.
- **sprite:** the prompt structure (a logical pixel grid with an exact nearest-neighbor enlargement, a ranked detail budget, and the AI-cliché blocklist with its "don't make it plain" guard) adapts The Sprite Wizard's "prompt bible" from r/aigamedev, whose own pipeline runs generated art through their [Sprite Grid](https://thespritewizard.itch.io/sprite-grid) processor the way `sprite_clean.py` does here.
- **newsroom:** builds on the `newsroom-style` skill in [jamditis/claude-skills-journalism](https://github.com/jamditis/claude-skills-journalism) (MIT; see [NOTICE.md](skills/newsroom/NOTICE.md)), keeping the rules that most published newsroom skills agree on, with Firelands Current's own rules on top.
