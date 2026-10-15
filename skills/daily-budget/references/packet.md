# The review packet

Everything for one day lives in `<library>/editorial/<YYYY-MM-DD>/`:

```
review.md                       what the editor reads
research.json                   the same content, structured for import
drafts/<key>.md                 newsroom output for each story (headlines, story, notes, flags)
images/                         cleared image files, original bytes
evidence/existing-content.json  baseline snapshot from start_day.py
evidence/...                    saved copies of the source pages, PDFs and images you relied on
```

Write every file as UTF-8. On Windows, a default-encoding write turns en dashes and curly quotes into garbage like `â€“`, and `check_packet.py` will reject it.

## research.json

Keep the field names exactly as below. A later import step reads this file, and the field names match the database columns.

```json
{
  "date": "2026-10-14",
  "scope": "Research and review drafts only; no database writes, uploads, publication or messages",
  "compared_against": { "articles": 64, "events": 70 },
  "stories": [
    {
      "key": "bash",
      "slug": "the-bash-norwalk-2027-lineup-tickets-october-2026",
      "status": "ready",
      "section": "community",
      "community": "Norwalk",
      "headline": "Tim McGraw, Riley Green to headline The Bash in Norwalk next summer",
      "summary": "Under 160 characters. Search results and social cards show this.",
      "body": "Markdown, with the primary source linked inline.",
      "source_urls": ["https://..."],
      "image": {
        "status": "cleared",
        "file": "tim-mcgraw-2012.jpg",
        "source_url": "https://commons.wikimedia.org/wiki/File:...",
        "license": "Public domain",
        "license_url": "https://...",
        "credit": "U.S. Navy photo / Wikimedia Commons",
        "caption": "Tim McGraw performs in 2012. File photo.",
        "alt": "Tim McGraw sings into a microphone on an outdoor stage.",
        "placement": "lead",
        "notes": "Shows the performer, not this festival."
      },
      "notes": "What the editor should know: discrepancies, what's unconfirmed, follow-up reporting."
    }
  ],
  "events": [
    {
      "key": "hike",
      "slug": "creek-bend-creatures-night-hike-october-16-2026",
      "status": "ready",
      "title": "Creatures of the Night Hike",
      "summary": "One plain sentence.",
      "description": "The practical details: what, who it's for, registration, accessibility, weather.",
      "category": "outdoors",
      "starts_on": "2026-10-16",
      "start_time": "19:30",
      "ends_on": null,
      "end_time": "21:00",
      "hours_note": "",
      "venue": "Creek Bend Farm — Wilson Nature Center",
      "address": "720 S. Main St., Lindsey",
      "community": "Lindsey",
      "organizer": "Sandusky County Park District",
      "organizer_url": "https://www.lovemyparks.com/",
      "cost": "Free; registration required by Oct. 16",
      "source_url": "https://reservations.lovemyparks.com/programs/6048/",
      "image": { "status": "none" },
      "notes": "Organizer marks it not wheelchair accessible."
    }
  ],
  "updates": [
    {
      "slug": "sandusky-homecoming-parade-october-14-2026",
      "change": "Add the route and the Camp Street closure.",
      "proposed_copy": "Replacement paragraph(s), ready to paste.",
      "source_url": "https://x.com/cityofsandusky/status/..."
    }
  ],
  "featured": ["bash"],
  "held_leads": [
    { "topic": "Teen cooking kit pickup", "source_url": "https://...", "missing": "Pickup hours and location" }
  ],
  "new_sources": [
    { "name": "Sandusky County Park District", "url": "https://www.lovemyparks.com/", "logged_in_news_sources": true }
  ]
}
```

Field rules:

- `key`: short, unique in the packet, and the name of the story's draft file.
- `slug`: lowercase words joined by hyphens, 120 characters or fewer, and new to the site. Existing stories put the place, the topic and the month or date in the slug: `perkins-doerzbach-demolition-appeal-hearing-october-27-2026`.
- `status`: `ready` (verified, no gaps), `needs-check` (worth running once the listed gap is filled), or `hold`.
- `section`: one of the keys in `SECTIONS` in the repo's `src/lib/news.ts`. Event `category`: one of the keys in `CATEGORIES` in `src/lib/events.ts`.
- Times are 24-hour `HH:MM`, in Eastern time. Use `null` when the source doesn't give one; never fill in a guess.
- `image.status`: `cleared`, `library` (reuse an existing library image; give `media_id`), `permission-needed` (give `contact`), `shoot` (a photo the editor could take; say when and where), or `none`. See `images.md`.
- `featured`: new story keys with a usable lead photo, best first. The editor has asked for new photo stories to replace older featured stories each day.
- `updates`: changes to stories or events that are already published. They're often more urgent than new stories.

## review.md

The editor makes decisions from this file, so put decisions first and evidence after. Follow this outline, and leave out any section that's empty.

```markdown
# Oct. 14, 2026 story and event leads

One paragraph: what you compared against (counts), how many stories, events and
updates you're proposing, and that nothing has been imported or published.

## First action: <update or time-sensitive item>          (only if there is one)

## Best new stories

| Priority | Proposed story | Why use it today | Readiness and image |
| --- | --- | --- | --- |
| 1 | [Headline](drafts/key.md) | Deadline, reach, section need | Sources checked; image status |

A short paragraph per story on what's verified, what isn't, and the trap to avoid.

## Featured

Which new stories should replace the current featured stories, and why.

## Potential calendar additions

| Event | Date and time | Place | Cost, registration and remaining checks |

## Image opportunities

Cleared images with credit and license; permission requests drafted (not sent) with
the contact; photos the editor could take today or tomorrow.

## Useful new sources

| Source | Leads supplied | How to use it |

## Held leads and source checks

What you looked at that didn't make it, and why. This is tomorrow's starting list.
```

Write dates in the editor's style (`Oct. 14`, `Wednesday`), link every source, and keep it scannable. The editor should be able to approve the package in a few minutes.
