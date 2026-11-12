# skills

Agent skills I write and use with Claude Code, Codex, and other agents that support the [Agent Skills](https://agentskills.io) format.

## Skills

| Skill | What it does |
| --- | --- |
| [daily-budget](skills/daily-budget/SKILL.md) | Sweeps Firelands Current's sources for new stories, events and images, drafts the best leads with newsroom, and builds a dated review packet for the editor. |
| [design-taste](skills/design-taste/SKILL.md) | Audits, polishes, or checks web UI so it stops reading as AI-generated: the dated tells registry, the accessibility and typography floor, motion timing, and a two-round screenshot critique. |
| [humanize](skills/humanize/SKILL.md) | Rewrites or audits text so it stops reading as AI-generated, keeping the meaning and the writer's voice. |
| [improve-codebase](skills/improve-codebase/SKILL.md) | Audits a codebase for the improvements most worth making, weighted toward the files git history says change and break most, checks every finding against the code, reports a short ranked list with a "looks bad but is fine" section, and files the findings you pick as GitHub issues ready for issue. Never edits code. |
| [improve-skills](skills/improve-skills/SKILL.md) | Audits agent skills for what makes them misfire, get ignored, or waste context, with a bundled checker for frontmatter, links, invocation settings, and eval prompts. Checks each finding against the files and the skill's git history, gives each skill a keep, improve, merge, or retire verdict, then makes the fixes you pick and has a fresh subagent compare old and new. |
| [issue](skills/issue/SKILL.md) | Picks a GitHub issue, offers a cheaper model when the job is small, does the work in your checkout, reviews it, updates the docs it affected, pauses for you to test it in local dev, then commits the change and the version bump as one `vX.Y.Z` release commit on the default branch, tags it, and pushes. With `--branch` it works in its own worktree instead and ships through a PR, squash-merged as the release commit. Can also work a batch of non-overlapping issues in parallel, each on a subagent with the model and effort its size calls for, and ship them one release at a time. |
| [minor](skills/minor/SKILL.md) | Cuts a minor release: bumps `X.Y.Z` to `X.Y+1.0`, updates the changelog, commits, tags, and pushes. |
| [music-creation](skills/music-creation/SKILL.md) | Writes, revises, and critiques songs, lyrics, melodies, and arrangements, prepares ready-to-paste Suno packages, and can plan an EP or album. |
| [newsroom](skills/newsroom/SKILL.md) | Writes, edits, and checks news stories for Firelands Current in AP style, with house rules, story-type playbooks, and editor flags. |
| [patch](skills/patch/SKILL.md) | Cuts a patch release: bumps `X.Y.Z` to `X.Y.Z+1`, updates the changelog, commits, tags, and pushes. |
| [prospect](skills/prospect/SKILL.md) | Finds one local business in Stone Dragon Media's coverage area, checks its website, Google profile, and Facebook for a problem SDM can fix, writes a link-free first message from Justin with humanize, and sends it by email, contact form, or Facebook only after approval, keeping a record so no one is contacted twice. |
| [seo-audit](skills/seo-audit/SKILL.md) | Audits a site or web project for search problems (crawling, indexing, canonicals, titles, structured data, link previews, JavaScript rendering, AI-crawler access) with a bundled raw-HTML checker, traces each finding to the template that causes it, and fixes it on request. |
| [sprite](skills/sprite/SKILL.md) | Makes pixel-art sprites for Chomp Chomp Panic!: generates each animation with Codex CLI's image tool from a structured prompt and a reference image, then snaps it onto the game's frame grid, palette and outline and writes the strips the Unity importer expects. Needs [Codex CLI](https://github.com/openai/codex) installed and logged in. |
| [title](skills/title/SKILL.md) | Renames the current chat session to match what actually happened in it. |
| [update-docs](skills/update-docs/SKILL.md) | Audits README, AGENTS.md, CLAUDE.md, CHANGELOG, the privacy policy, and other docs against the code and fixes what's wrong or out of date, then finds contradictions, stale records, and docs to consolidate or delete, and proposes structural changes for approval. |

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
    tests/          # optional unit tests for those scripts
    references/     # optional docs the skill loads on demand
    agents/         # optional Codex settings (openai.yaml)
    evals/          # optional test cases for skill-creator or `claude plugin eval`
    SOURCES.md      # optional upstream skills it draws on, pinned to a commit
```

Each skill folder holds all of its own files, so it can be copied anywhere on its own. Some skills call another skill: daily-budget needs newsroom installed too, and prospect needs humanize. Issue runs update-docs on each change before it ships, so install it alongside; without it, issue checks the docs by hand. With `--branch`, when a repo can't squash-merge, it leaves a `/patch` or `/minor` run as your follow-up. Improve-codebase files issues for issue to work, and leaves docs drift to update-docs.

Most skills run only when you invoke them: `disable-model-invocation: true` in the frontmatter does that for Claude Code (`/<name>`), and `agents/openai.yaml` does it for Codex (`$<name>`). Newsroom, humanize, and update-docs are left out, because other skills call them and these settings would block that.

## Credits

Some skills distill what the most-used public skills on the same subject agree on; the rest were checked against them. Each one lists its sources in a `SOURCES.md` in its own folder, with each source pinned to the commit last reviewed and its license. The agent never loads these files.

- [daily-budget](skills/daily-budget/SOURCES.md): eight journalism and news-monitoring skills, for the sources-swept log.
- [design-taste](skills/design-taste/SOURCES.md): nine frontend design skills, with most of the motion guidance from emilkowalski/skills and jakubkrehel/skills.
- [humanize](skills/humanize/SOURCES.md): thirteen anti-AI-writing skills; each rule appears in most of them.
- [improve-codebase](skills/improve-codebase/SOURCES.md): about twenty codebase-improvement skills, led by Matt Pocock's improve-codebase-architecture and codebase-design and shadcn's improve.
- [improve-skills](skills/improve-skills/SOURCES.md): fifteen skill-writing and skill-improvement skills, beyond Anthropic's and OpenAI's skill-creators.
- [issue](skills/issue/SOURCES.md): twelve issue-to-PR skills, led by open-mercato's om-auto-fix-issue (reproduce first) and fandhe-ai's implement-issue (out-of-scope tracking).
- [minor](skills/minor/SOURCES.md) and [patch](skills/patch/SOURCES.md): thirteen release and changelog skills, led by jssblck's tag-release and tobi/qmd's release.
- [music-creation](skills/music-creation/SOURCES.md): four songwriting skill collections, with a map of each rule to the sources behind it (licenses in [NOTICE.md](skills/music-creation/NOTICE.md)).
- [newsroom](skills/newsroom/SOURCES.md): builds on the `newsroom-style` skill in jamditis/claude-skills-journalism (MIT; see [NOTICE.md](skills/newsroom/NOTICE.md)).
- [prospect](skills/prospect/SOURCES.md): nine cold-outreach and prospecting skills, led by coreyhaines31's cold-email and prospecting.
- [seo-audit](skills/seo-audit/SOURCES.md): the most-installed SEO skills, with the fix loop from squirrelscan's audit-website and the "look before you recommend" rule from seo-skill-bench.
- [sprite](skills/sprite/SOURCES.md): adapts The Sprite Wizard's "prompt bible" from r/aigamedev.
- [title](skills/title/SOURCES.md): twelve session- and tab-renaming skills.
- [update-docs](skills/update-docs/SOURCES.md): eight docs-maintenance skills, including Anthropic's claude-md-improver, amelnagdy's docs-guard, and laurigates' docs-sync.
