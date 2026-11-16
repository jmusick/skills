---
name: daily-news
description: Runs Firelands Current's daily news budget. Sweeps the paper's sources for new stories, events and updates to published stories, verifies them, drafts the best few, and writes a dated review packet (review.md and packet.json) for the editor. With --unattended it also imports the packet into local dev, syncs it to production and queues the Facebook posts. Use when the user types /daily-news, or asks to run the daily news, the news budget or today's story sweep, or to find today's stories for Firelands Current. Don't use it unasked, and never run --unattended unless the user names it.
---
A news budget is the day's list of stories. Find what's new, verify it, draft the best of it, and hand the editor a packet they can approve in a few minutes. Accuracy beats volume: three solid stories are a good day, and five unverified ones are a bad one.

Arguments:
- A bare `/daily-news` stops at the review packet. Nothing reaches the database, the site or Facebook until the editor says so, because it puts words and images in front of readers under the paper's name.
- `--unattended` runs every step without stopping to ask, then takes the packet live. Read **Unattended** before step 1.
- `--date YYYY-MM-DD` builds the packet for another day. Today is the default.

## Setup

Work from the `firelands-current` repository. The project library is at `../../Projects/firelands-current` from it, or wherever `FIRELANDS_PROJECT_DIR` points. Read these every run, because they change almost daily:
- `docs/news-sources.md`: coverage area, editorial rules, the byline account, sections and the source list with each source's traps. It decides **where** to look.
- `docs/editorial-tools.md`: the `packet.json` manifest and the `packet.mjs` modes.
- The "Images" section of `docs/accessible-publishing.md`.

## 1. Open the packet

1. Create `editorial/<date>/` in the library, with `drafts/`, `evidence/` and `images/`. If the folder already has a `packet.json` or `local-import.json`, stop: that day has a run in progress, and the tool won't adopt it.
2. Snapshot the site to `evidence/existing-content.json` with read-only `npx wrangler d1 execute DB --local --json --command "SELECT ..."` queries: `news_articles` (slug, headline, summary, section, community, status, featured, published_at, lead_media_id), `events` (slug, title, category, starts_on, start_time, venue, community, status) and `media` (id, filename, alt, caption, credit, created_at). If there's no local database, run `npm run db:migrate:local` and retry. Everything after this depends on the snapshot.
3. From it, note stories from the last 21 days (don't repeat them), sections with fewer than three current stories (they need stories most), events in the next 30 days (don't list one twice), and the newest library photos. Read three recent stories in full for voice.
4. Open the newest earlier `review.md` in `editorial/`. Its held leads and follow-ups are today's first leads.

## 2. Sweep and scout

Work in this order. Note the date on everything, and log each source you open, with the time and what it turned up, for the "Sources swept" table:
1. **Follow-ups**: yesterday's held leads, and anything new on stories from the last few days (a route announced, a time changed, a vote taken).
2. **Reliable sources** in `news-sources.md`.
3. **Social**: the official Facebook Pages and X accounts it lists, and Facebook event search, in a signed-in browser (the built-in browser, Claude in Chrome or Codex's Browser). Read only: never post, comment, react, message, follow or join, and never reuse images from social posts. If no signed-in browser is available, mark social "not reached" and say so in the report.
4. **Promising sources** that haven't produced a story yet.

Spend part of the sweep looking for new sources for the thin sections and for places in the coverage area with no source: villages, townships, school districts, libraries, parks, chambers, nonprofits, venues. Add each useful one to `news-sources.md` as one entry in the list it belongs to, with what it's good for and any trap, and edit an existing entry in place when a source changes. Don't add dated sections; the file is a reference read every run, not a log. It's the only repo file you edit. Don't commit or push it.

## 3. Verify every lead

Take each fact from the primary source (the agency, organizer or document), never from a search summary, another outlet or a resident's comment. Save a copy of every page, PDF or image you rely on into `evidence/`, since notices disappear and a correction may need them. Check for the traps that have bitten this paper:
- **Year and date.** Confirm the year on the page itself; URLs, titles and promos keep last year's. Report when the news happened, not when it was posted. Check the weekday against the date. Drop anything already over.
- **Times.** A gate or doors time isn't a start time, a calendar window isn't a duration, and a midnight or all-day entry is a placeholder. Never infer an end time.
- **Money and access.** Free admission doesn't make parking or activities free, and a missing price isn't evidence of free. "Starting at" isn't the total. Check availability where tickets are sold.
- **Claims.** Projected jobs aren't filled jobs, a scheduled reopening isn't a confirmed one, and a public notice sets a hearing, not its outcome. Attribute projections and findings to whoever made them.
- **Conflicts.** When two official pages disagree on a fee, age limit or deadline, report both or leave it out. Never pick one.
- **Look-alikes.** Sandusky County isn't the city of Sandusky, Huron the city isn't Huron County, and other states have a Huron too.
- **Images and PDFs.** Read the flyer or press-release image; the details are often only there. Use `pdftotext -layout` on PDFs and read the year printed inside.

A lead you can't verify today goes in the held leads with what's missing. That's a normal outcome, not a failure.

## 4. Sort, rank and find images

Sort each lead as an **update** (it changes a published story or event; usually first, because a published story that's now wrong is worse than a missing one), a **story**, an **event** (a calendar listing; don't pad one into a story), or a **hold**. Rank stories by urgency (a deadline today or tomorrow), how many readers it affects, how thin its section is, and whether it has an image. Aim for three to five.

Images are nice to have, not required; when two stories are otherwise even, pick the one with a picture. Look first in the media library, then a press kit whose terms cover that file, then openly licensed files (Wikimedia Commons, U.S. federal work) whose license you read on the file's own page. Never use an image just because it's public, and never use an AI-generated one. A CC BY-ND image can't be cropped, so it can only be a body figure. When an agency holds the right image, draft a permission request in `review.md` and don't send it. Caption what the photo shows, where and when, and end a file photo with "File photo." so it never implies it shows today's event. Credit the creator, source and license. Write alt text under 300 characters that doesn't repeat the caption.

## 5. Draft

Write each story to `drafts/<key>.md`: three headline options, a summary under 160 characters, the body in Markdown, and notes on what's unconfirmed. Follow the editorial rules in `news-sources.md` and the voice of the stories you read in step 1: a direct news lede, short paragraphs, the primary source linked inline, explicit attribution, and the practical details (time, place, cost, registration, accessibility). Write in the paper's own words, never a reworded version of another outlet's story. Don't invent anything a source doesn't give: a first name, an end time, a percentage, a reaction. Mark each gap `[NEED: ...]`; a story with one is `needs-check`, not `ready`.

## 6. Write the packet

Write every file as UTF-8. On Windows a default-encoding write turns curly quotes and dashes into `â€“`.

**`packet.json`**: the manifest from `editorial-tools.md`, with only `ready` items in it. Set `publish_window.until` to the end of the budget date, the author from `news-sources.md`, and `expect` to the counts you mean, so a dropped story fails loudly. Take section keys from `SECTIONS` in `src/lib/news.ts` and event categories from `CATEGORIES` in `src/lib/events.ts`. Times are 24-hour `HH:MM` Eastern, and `null` when the source gives none. Get update baselines and reused-photo facts from `packet-facts.mjs` rather than computing them. List the featured stories you recommend (new photo stories, best first), with the ones they replace unfeatured. Never put a `[NEED:` marker in it.

**`review.md`**: decisions first, evidence after. Leave out any section that would be empty:
- An opening paragraph: what you compared against (counts), what you propose, and that nothing has been imported or published.
- **First action**: an urgent update or time-sensitive item, with the replacement copy.
- **Best new stories**: a table of priority, headline linked to its draft, why today, and readiness and image status, then a short paragraph per story on what's verified, what isn't and the trap to avoid.
- **Featured**, **Potential calendar additions** (date and time, place, cost and remaining checks), **Image opportunities**, **Useful new sources**.
- **Held leads and source checks**: what didn't make it and why. This is tomorrow's starting list.
- **Sources swept**: every source you opened, with the time and result, including the ones with nothing new and the ones not reached.

Write dates in the editor's style (`Oct. 14`, `Wednesday`) and link every source.

## 7. Report

Reply in a few lines: each proposed story (headline, why today, image status, strongest source), the updates with urgent ones first, how many events and any happening today, new sources logged, a link to `review.md`, and that nothing has been imported or published. Then offer the next steps from **Going live**.

## Going live

On the editor's go-ahead in this conversation, or under `--unattended`, run `node scripts/editorial/packet.mjs --date <date>` with each mode in turn, stopping at the step the editor approved:
1. `--apply-local`. Then start `npm run dev` and run `--verify-http`; the editor reviews at `http://127.0.0.1:4321/news`. Changing copy after the import means restoring the local database and starting over, because the manifest's hash is now frozen.
2. `--prepare --production`, `--publish --production`, `--queue --production`, `--verify --production`, in that order.
3. Write `production-publication.md` in the packet folder and add a short "Production sync completed" note to the top of `review.md`. Stop the dev server you started.

If any mode fails, stop and report its output. Never rerun a mode that writes, edit `packet.json` after the import, use `--ignore-window`, apply migrations, or push to `main`: each of those needs the owner, and the tool's intent files exist so a person inspects a failed write before anyone retries it.

## Unattended

`--unattended` is the owner's go-ahead for **Going live**, given in advance: run steps 1 through 6 without asking, then every mode through `--verify --production`. Hold anything that would need a decision, rather than asking: a `needs-check` story, a conflict between sources, an image whose license you can't confirm, an update you can't verify against the live text. Held items go in `review.md`, not the manifest. If nothing is `ready`, write the packet and stop without importing. Report as in step 7, plus what went live, what was queued for Facebook, and what was held and why.

## Boundaries

Before **Going live**, don't write to the local or production database, upload to R2, or run any `--remote` command. At any point, don't send email or messages (draft them in `review.md`), don't act on social accounts, and don't commit or push.
