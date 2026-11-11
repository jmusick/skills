# Follow-ups

Read this for `/prospect follow-up`.

List the records due for one, oldest first:

```bash
python <this skill's directory>/scripts/outreach.py due <outreach folder>
```

It lists `status: sent` records whose first contact was seven or more days ago. Show any it lists under `unreadable_first_contact` too, since their dates need fixing by hand. For each one Justin picks:

1. Ask whether they replied. If the channel was email, offer to search his Gmail for a reply first. Never assume no reply.
2. If there was no reply, draft one short follow-up on the same channel (about 40–80 words). Refer back to the first note in a sentence, add one useful detail, and repeat the opt-out line. A follow-up may include one link to stonedragonmedia.com or a relevant portfolio page, since the business has now heard from Justin once.
3. Humanize it, check it with `check_message.py <file> --channel <channel> --follow-up` (40–80 words, one link allowed), get approval as in step 6 of SKILL.md, send it as in step 7, and set `status: followed-up` with a History line.

Send one follow-up at most. After that the business has heard twice, and a third unanswered message is pestering.
