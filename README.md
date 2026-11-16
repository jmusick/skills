# skills

Agent skills I write and use with Claude Code, Codex, and other agents that support the [Agent Skills](https://agentskills.io) format.

## Skills

| Skill | What it does |
| --- | --- |
| [commit](skills/commit/SKILL.md) | Commits the current work with [Conventional Commits](https://www.conventionalcommits.org) messages. |
| [daily-news](skills/daily-news/SKILL.md) | Runs [Firelands Current](https://firelandscurrent.com)'s daily news budget: sweeps the paper's sources, verifies and drafts the best stories, and writes a review packet for the editor. Built for that paper's repo and its `packet.mjs` publishing tool. Needs `newsroom`. |
| [design-taste](skills/design-taste/SKILL.md) | Audits, polishes, or builds web UI so it stops reading as AI-generated: a dated registry of generated-design tells, an accessibility and typography floor, motion timing, and a two-round screenshot critique. Uses Anthropic's `frontend-design` to set direction for new pages when it's installed. |
| [humanize](skills/humanize/SKILL.md) | Rewrites or audits text so it stops reading as AI-generated, keeping its meaning, facts, and voice. Built on Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). |
| [improve-codebase](skills/improve-codebase/SKILL.md) | Audits a codebase for the improvements most worth making, weighted toward the files git history says change and break most while still checking old, rarely changed code for risk, checks every finding against the code, reports a short ranked list with a "looks bad but is fine" section, and files the findings you pick as GitHub issues ready for `issue`. Each run can leave a record of what it covered, so later runs start where it stopped. Never edits code. |
| [improve-skills](skills/improve-skills/SKILL.md) | Audits agent skills for what makes them misfire, get ignored, or waste context, with a bundled checker for frontmatter, links, and invocation settings. Checks each finding against the files and the skill's git history, gives each skill a keep, improve, merge, or retire verdict, then makes the fixes you pick. |
| [interview](skills/interview/SKILL.md) | Interviews you about a project or feature in rounds of questions, each with its recommended answer, until every decision is settled, then writes a spec someone who wasn't there could build from. A fresh reader checks the spec before you get it, and it offers to split the spec into GitHub issues for `issue`. Never builds anything. |
| [issue](skills/issue/SKILL.md) | Picks an open GitHub issue, works it, reviews it, pauses for you to test it, and commits the change so the issue closes when it's released. It can also work on its own branch with a PR, on several issues in parallel, or unattended. Needs `commit`; uses `update-docs` and Claude Code's `/code-review` when present. |
| [job-search](skills/job-search/SKILL.md) | Finds jobs that fit Justin on LinkedIn, Indeed, and Sandusky-area employers' sites, checks each against the employer's own posting and his resume, and shows the best three with the fit, gaps, and warning signs. For the ones he picks, it prepares a resume, a cover letter, and screening answers for him to submit himself, then tracks status and quiet applications. Needs `humanize`. |
| [music-creation](skills/music-creation/SKILL.md) | Writes, revises, and critiques songs, lyrics, melodies, and arrangements, prepares ready-to-paste Suno packages, and can plan an EP or album. |
| [newsroom](skills/newsroom/SKILL.md) | Writes, edits, and checks news stories and headlines in AP style, following your publication's house style when the project has one, with story-type playbooks and editor flags. |
| [prospect](skills/prospect/SKILL.md) | Finds one local business in Stone Dragon Media's coverage area, checks its website, Google profile, and Facebook for a problem SDM can fix, writes a link-free first message from Justin, and sends it by email, contact form, or Facebook only after approval, keeping a record so no one is contacted twice. Needs `humanize` and Claude in Chrome. |
| [release](skills/release/SKILL.md) | Cuts a release: works out the version bump from the Conventional Commits since the last tag, then tags and pushes. When nothing calls for a version, it still pushes the pending commits. |
| [seo-audit](skills/seo-audit/SKILL.md) | Audits a site or web project for search problems (crawling, indexing, canonicals, titles, structured data, link previews, JavaScript rendering, AI-crawler access) with a bundled raw-HTML checker, traces each finding to the template that causes it, and fixes it on request. |
| [sprite](skills/sprite/SKILL.md) | Makes pixel-art sprites for Chomp Chomp Panic!: generates each animation with Codex CLI's image tool from a structured prompt and a reference image, then snaps it onto the game's frame grid, palette, and outline and writes the strips the Unity importer expects. Needs [Codex CLI](https://github.com/openai/codex) installed and logged in. |
| [title](skills/title/SKILL.md) | Renames the session to match what was actually done in it. |
| [update-docs](skills/update-docs/SKILL.md) | Checks docs like README.md and AGENTS.md against the code, fixes what's no longer true, and proposes cleanups for stale or duplicated docs. |

## Options

Each skill runs with no options. These change what it does. Type them after the command (`/` in Claude Code, `$` in Codex), or say them in plain English. `music-creation`, `release`, and `sprite` have no options.

| Skill | Option | What it does |
| --- | --- | --- |
| commit | `/commit <files>` | Commits only the named files and leaves the rest uncommitted. |
| daily-news | `--unattended` | Runs without stopping to ask, then imports the packet into local dev, syncs it to production and queues the Facebook posts. Anything that would need a decision is held for the editor instead. |
| daily-news | `--date YYYY-MM-DD` | Builds the packet for that day instead of today. |
| design-taste | "audit", "review", "flag only", or "does this look AI?" | Reports findings with file and line, and changes nothing. The default when pointed at existing UI. |
| design-taste | "polish" or "fix" | Fixes in place with the smallest changes that clear the findings, keeping the project's components, tokens, and identity. |
| design-taste | "build" or "redesign" | Sets a direction for a new page or screen first, then builds to the floor and runs the critique. |
| humanize | "audit", "scan", "flag only", or "is this AI?" | Lists each AI-writing pattern it finds, with a fix, without rewriting. It never guesses who wrote the text. |
| humanize | a file path | Edits the prose in that file in place, leaving code, commands, and frontmatter alone. |
| improve-codebase | `/improve-codebase <path>` | Audits one directory or package instead of the whole repo. |
| improve-codebase | `/improve-codebase <focus>` | Audits one area: `baseline`, `architecture`, `duplication`, `dead-code`, `types`, `correctness` (or `errors`), `tests`, `deps`, `performance`, or `security`. Combines with a path. |
| improve-codebase | `quick` | Checks only the top 10 hotspots, reports only High-confidence findings, and skips the cold-file pass and the second-opinion check. |
| improve-skills | `/improve-skills <name or path> ...` | Reviews only the named skills or folders. |
| improve-skills | `quick` | Runs only the scripted checks, routing, and structure review. |
| improve-skills | `eval` | Also runs the changed skills' evals, where a repo has them. They're billed model runs, so they're off by default. |
| interview | `/interview <idea>` | Interviews you about that idea. |
| interview | `/interview <path>` | Reads a draft spec, notes, or doc, and interviews you about what it leaves unsettled. |
| interview | `/interview #12` | Interviews you about GitHub issue 12, reading its comments too. |
| interview | "one at a time" | Asks one question per message instead of a round at a time. |
| issue | `/issue 42` | Works issue 42, or resumes it if an earlier run left your PR open. With no number, it picks the most important open issue it can finish. |
| issue | `/issue 12 15 18` | Works those issues in parallel, one subagent per issue in its own worktree. |
| issue | `--batch [N]` | Picks a batch of up to N issues (default 4) and works them in parallel. |
| issue | `--branch` | Works in its own worktree on a new branch and opens a PR, leaving your checkout alone. You review and merge it. |
| issue | `--no-test` | Runs unattended: skips the local-dev test pause and every other stop to ask. Pairs with `/loop /issue --no-test` for a backlog. |
| job-search | `/job-search <focus>` | Narrows the search to a role, `local`, or a named employer. `local` adds the area employers' career pages. |
| job-search | `/job-search draft <job>` | Prepares the application for one job (a record, URL, or company name). |
| job-search | `/job-search status` | Lists where each application stands and which have gone quiet. |
| newsroom | "edit" | Revises your draft instead of writing a new one, and says what changed. |
| newsroom | "check", "AP check", "review", or "flag only" | Lists problems as editor flags, each with a fix, without rewriting. |
| prospect | `/prospect <town, industry, or business>` | Narrows the search to that town or industry, or researches the named business. |
| prospect | `/prospect follow-up` | Sends the follow-ups that are due instead of a new first message. |
| seo-audit | "fix" | Fixes each finding at the template or config that causes it, rebuilds, and reruns the checker. Without it, it reports and changes nothing. |
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

Some skills are a single `SKILL.md`. Some carry helper scripts for checks that are easy to get wrong by reading, or reference files read only on the runs that need them. They need Python 3 (standard library only), and each skill does the check by hand without it.

- `daily-news`: `scripts/open_packet.py` opens the day's packet folder and snapshots the site, `scripts/check_packet.py` checks the finished packet against the skill's rules, and `assets/review-template.md` is the editor's review layout.
- `design-taste`: `scripts/lint_tells.py` flags quality-floor misses and the mechanical tells in front-end source. The tells registry, the full floor, the motion rules, and build-mode direction live in `references/`, read when a step calls for them.
- `humanize`: `scripts/scan.py` counts the listed AI words, stock phrases, dashes, and sentence-length spread, with line numbers.
- `improve-codebase`: `scripts/hotspots.py` ranks files by how often git history says they change and break, and lists the large files that rarely change so they still get checked for risk. The audit checklist and the issue template live in `references/`.
- `improve-skills`: `scripts/check_skills.py` runs the mechanical checks on skills (frontmatter, links, invocation settings). The review checklist lives in `references/`.
- `interview`: no scripts. `assets/spec-template.md` is the spec's layout, `assets/issue-template.md` is the issue layout used when you ask for issues, and `references/builder-check.md` is the prompt for the fresh reader that checks the spec.
- `issue`: `scripts/candidates.py` applies the skip rules to the open issues and ranks the rest. Branch and batch mode live in `references/`, read only on those runs.
- `job-search`: `scripts/jobs.py` finds postings already seen, lists applications gone quiet, and names new records. Drafting an application lives in `references/materials.md`.
- `music-creation`: no scripts. Lyrics, composition, Suno, and album planning each live in `references/`, read only when the task needs them.
- `newsroom`: `scripts/ap_lint.py` flags weekdays that don't match their dates and the mechanical AP slips (months, times, numerals, abbreviations, loaded words).
- `prospect`: `scripts/outreach.py` finds existing records and lists follow-ups due, and `scripts/check_message.py` checks a drafted message's length, links, sign-off, and subject. SDM's services, channels, signals, and follow-ups live in `references/`.
- `release`: `scripts/next_version.py` runs the pre-release checks and sorts the commits since the last tag by the bump each calls for.
- `seo-audit`: `scripts/seo_check.py` checks pages for crawl, index, and on-page problems from their raw HTML. The full checks, and where each framework builds the page head, live in `references/`.
- `sprite`: `scripts/make_prompt.py` writes the image prompts from a brief, `scripts/codex_image.py` generates each sheet with Codex CLI, and `scripts/sprite_clean.py` turns it into game-ready strips. These scripts are the pipeline, so `sprite` has no by-hand fallback. The game's sizes, the prompting rules, and the build spec live in `references/`.
- `update-docs`: `scripts/doc_links.py` checks links and anchors, plus a privacy-policy checklist it reads only when a repo has one.

Each skill is one self-contained folder, so it can be copied anywhere on its own. The sources a skill was built from are credited in [REFERENCES.md](REFERENCES.md) rather than in the skill's folder. Some skills depend on another: `issue` commits through `commit`, `daily-news` writes its stories with `newsroom`, and `prospect` and `job-search` run their drafts through `humanize`, so install each pair together. `improve-codebase` and `interview` file issues for `issue` to work, and `improve-codebase` leaves docs drift to `update-docs`. `issue` also runs `update-docs` and Claude Code's built-in `/code-review` when they're installed, and checks by hand when they're not, and `design-taste` lets Anthropic's `frontend-design` set the direction for new pages when it's installed. None turns off model invocation, so your agent can pick any of them up from plain English as well as from `/<name>` (Claude Code) or `$<name>` (Codex).

`commit` and `release` are meant as a pair: commit each piece of work as you go, then run `release` when you want to ship what's built up. Each works on its own too, since `release` reads any Conventional Commits history.
