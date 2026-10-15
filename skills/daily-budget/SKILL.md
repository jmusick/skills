---
name: daily-budget
description: Run Firelands Current's daily news budget. Sweeps the paper's sources (agency and organizer sites, official Facebook Pages and X accounts, Google News) for new story leads and calendar events, scouts new sources, checks what's already published, looks for usable images, drafts the best stories with the newsroom skill, and assembles a dated review packet for the editor. Use when the user types /daily-budget or $daily-budget, or asks to find today's stories, find some new stories or leads, check our sources, look for new events to add, or see what's new for Firelands Current, even if they never say "budget." Stops at the review packet. Not for importing, publishing, syncing to production, featuring stories, or queuing Facebook posts; not for writing or editing one story the user already has (use newsroom); and not for site code changes.
---

# Daily budget

A news budget is the day's list of stories. This skill builds Firelands Current's budget: it finds what's new, verifies it, drafts the best of it, and hands the editor a packet they can approve in a few minutes. Accuracy beats volume. Three solid stories are a good day; five unverified ones are a bad one.

The skill **stops at the review packet**. Importing, publishing, featuring and Facebook queuing happen only after the editor says so, because they put words and images in front of readers under the paper's name.

## Setup

Work from the `firelands-current` repository (for example `C:\Users\JD\source\firelands-current`). The project library is beside it at `../../Projects/firelands-current`, or wherever `FIRELANDS_PROJECT_DIR` points.

Read these before you start, every time. They change almost daily.

- `docs/news-sources.md`: coverage area, editorial rules, the source list, and notes on each source's traps. This is the source of truth for **where** to look.
- The "Images" section of `docs/accessible-publishing.md`.
- `references/verification.md` in this skill: the general traps that `news-sources.md` records case by case.

## Workflow

### 1. Open the packet and read the baseline

Run from the repo root (use `python3` if `python` isn't found):

```bash
python <skill-dir>/scripts/start_day.py
```

It creates `editorial/<today>/` in the library, snapshots existing stories, events and media to `evidence/existing-content.json`, and prints a briefing. Read it for:

- **Stories from the last 21 days.** Don't repeat them. An update to one of them is a different thing (step 5).
- **Section balance.** Sections marked thin need stories most. The site wants at least three current stories in each section so every homepage block fills in.
- **Upcoming events**, so you don't list one twice.
- **Media library photos** you could reuse.
- **Style samples.** Match their voice: direct news ledes, short paragraphs, the primary source linked inline, practical details (time, place, cost, registration, accessibility), and explicit attribution.

Then open yesterday's `review.md` (the newest earlier folder in `editorial/`). Its held leads and follow-ups are today's first leads.

### 2. Sweep the sources

Work in this order, and note the date on everything you find:

1. **Follow-ups.** Yesterday's held leads, plus anything new about stories published in the last few days (a route announced, a time changed, a vote taken).
2. **Reliable sources** in `news-sources.md`, newest notes first.
3. **Social.** Use the signed-in browser available to you (Codex's in-app Browser, Claude in Chrome, or the built-in browser) for the official Facebook Pages and X accounts listed in `news-sources.md`, plus Facebook event search. Use Google News's local section for leads. **Read only:** don't post, comment, react, message, follow or join anything. Don't download or reuse images from social posts.
4. **Promising sources** from `news-sources.md` that haven't produced a story yet.

### 3. Scout for new sources

Spend part of the sweep looking for sources the paper doesn't use yet, aimed at the thin sections and at places in the coverage area with no source listed. Try villages, townships, school districts, libraries, parks, chambers, nonprofits, hospitals and venues. Log each useful one in `docs/news-sources.md` under a dated heading like the existing ones (`### Sources checked Oct. 15, 2026`): what it's good for, how to read it, and any trap you hit. This repo file is the one you edit. Don't commit it; the editor does.

### 4. Verify every lead

Apply `references/verification.md` to each lead: the year on the page, the posting versus announcement date, times, prices, access, projections and conflicts between pages. Take facts from the primary source, never from a search summary, another outlet, or a resident's comment. Save a copy of each page you rely on into `evidence/`.

A lead that can't be verified today goes into `held_leads` with what's missing. That's a normal outcome, not a failure.

### 5. Sort and rank

Sort each lead into one of these:

- **Update:** changes an existing story or event. This usually goes first, because a published story that's now wrong is worse than a missing one.
- **Story:** news a reader would want explained, such as a decision, a change in a service, a deadline, an award or a hearing.
- **Event:** a calendar listing. Many leads are only events. Don't pad a calendar item into a story.
- **Hold:** promising but missing something.

Rank stories by urgency (a deadline or event today or tomorrow), how many readers it affects, how thin its section is, and whether there's an image. Aim for three to five stories.

### 6. Find images

Follow `references/images.md`. Images are nice to have, not required: when two stories are otherwise even, choose the one with a picture. Every story gets an `image.status`, even if it's `none`.

### 7. Draft the stories with newsroom

For each chosen story, use the **newsroom** skill (`/newsroom` or `$newsroom`) in Write mode with your verified facts and source links, then run its Check mode on the result. Newsroom covers AP and house style, ledes, attribution and fairness, so follow it rather than restating its rules here. Save its full output (headlines, story, notes, flags) to `drafts/<key>.md`.

Don't invent anything a source doesn't give, including end times, first names, percentages and reactions. A `[NEED: ...]` gap makes the story `needs-check`, not `ready`.

### 8. Write the packet and check it

Write `research.json` and `review.md` as described in `references/packet.md`, as UTF-8. Recommend which new photo stories to feature. Then run:

```bash
python <skill-dir>/scripts/check_packet.py
```

Fix every error. Fix each warning or explain it in `review.md`.

### 9. Stop and report

Reply in a few lines:

- Each proposed story: headline, why today, image status, and its strongest source link.
- Updates to existing coverage, with the urgent ones first.
- How many events, and any that happen today.
- New sources you logged.
- A link to `review.md`.
- That nothing has been imported or published.

Then offer the next steps the editor usually takes: import locally for review at `http://127.0.0.1:4321/news`, or sync to production, queue the Facebook posts and feature the new photo stories. Those follow "Getting a story live" in `docs/news-sources.md` and the repo's `AGENTS.md`, and need the editor's go-ahead in this conversation.

## Boundaries

During a budget run, don't:

- Write to the local or production database, upload to R2, or run any `--remote` command.
- Send email or messages, including image-permission requests. Draft them in `review.md`.
- Act on social accounts beyond reading.
- Commit, push or bump versions. The only repo file you edit is `docs/news-sources.md`.
- Use an image without a verified license or permission.
