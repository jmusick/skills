---
name: prospect
description: Find one local business in Stone Dragon Media's coverage area, match it to the SDM service that would help it most, and send Justin Musick's first outreach message by email, contact form, or Facebook after he approves it.
disable-model-invocation: true
---

# Prospect

Find one local business that Stone Dragon Media can actually help, show Justin why, and send a first message he'd be glad to have his name on. Quality beats volume. A badly aimed pitch from a local agency gets remembered around town, so one well-researched message is worth more than ten generic ones.

## Modes

- **New** (default): `/prospect`, optionally with a town, an industry, or a named business ("/prospect Huron restaurants", "/prospect Maple Street Bakery"). Read `references/sdm.md` (what SDM sells, where it works, and the facts about Justin a message can use), then run steps 1–7.
- **Follow-up**: `/prospect follow-up`. Read `references/sdm.md` and [references/follow-up.md](references/follow-up.md), and follow the latter.
- **Update**: the user reports a reply, a no, or an opt-out ("Maple Street said no thanks"). Find the record with `outreach.py match` (step 2), update its status and History, and stop.

If the user asks for several businesses, run the loop once per business, each with its own approval.

## The outreach folder

Records live in `C:\Users\JD\projects\stone-dragon-media\Outreach\` unless the user names another folder. Create it on first use. Run the scripts as `python <this skill's directory>/scripts/<script>`, or with `python3` if `python` isn't found.

- `sender.md`: Justin's details for signatures and forms: name, title, phone, the email address to send from (always stonedragonmedia@gmail.com), a mailing address for emails (see step 5), and which Facebook identity to message from. On a first run, or when a field the message needs is missing, ask for it once and save it. Don't guess any of it.
- One file per business, `<town>-<business-slug>.md`:

```markdown
---
business: Maple Street Bakery
town: Huron
website: maplestreetbakery.com
facebook: facebook.com/maplestreetbakery
email: hello@maplestreetbakery.com
phone: (419) 555-0100
status: sent   # passed | drafted | sent | replied | declined | do-not-contact | followed-up
channel: email
service: Design & Development (website redesign)
first_contact: 2026-11-10
---

## Why this business
The evidence from step 3, with the URL or place each fact came from.

## Message
The exact text that was sent, with the subject line if it was an email.

## History
- 2026-11-10: sent by email from stonedragonmedia@gmail.com
```

A business you checked in step 3 and passed on gets a short file with `status: passed` and one line on why, so later runs don't check it again. Businesses left out in step 1 (chains, competitors, closed) get no file, since ruling them out again takes seconds.

## 1. Find candidates

A named business is the only candidate; go to step 2. Otherwise, when the user gave no town, pick one from the coverage list in `references/sdm.md`, favoring in-person towns with the fewest records (`outreach.py towns <outreach folder>` counts them) so the outreach spreads across the area.

Gather five to eight candidates with web search, Google Maps, and Facebook: local, independently owned businesses that sell to the public or to other local businesses. Note what each listing already shows (no website, a dead or for-sale domain, a published email, the last Facebook post); that's enough to rank them in step 3 without opening every site.

**Facebook** turns up the strongest candidates: businesses whose only presence online is a Page. In Justin's signed-in Chrome, search Pages for the town and a category (`facebook.com/search/pages/?q=<category> <town>`) and look through the town's public community and buy-local groups for businesses people name. Then:
- Search a few times, at a normal person's pace, and collect only names and Pages. Meta's terms restrict automated collection, and this is Justin's personal account.
- Don't like, follow, join, comment, react, or message anyone, here or when sending. Those are public actions he didn't approve.
- Stay off Nextdoor entirely: its terms prohibit commercial prospecting, and a pitch built from neighbors' posts reads like surveillance.

Leave out, without researching further:
- chains, franchises, and national brands, which buy marketing centrally
- web designers, marketing agencies, and IT shops (competitors)
- government offices, schools, and churches, unless the user asks for them
- businesses that look closed: marked "permanently closed," a dead phone, no activity anywhere in over a year
- SDM's current clients

## 2. Check the records

A business may be filed under another name (an LLC, an owner's name) that only its website, phone, or Page gives away, so a script does the check. Check all the candidates in one call, as a JSON list in a file or on stdin (`-`):

```bash
python <this skill's directory>/scripts/outreach.py match <outreach folder> --batch - <<'EOF'
[{"name": "Maple Street Bakery", "website": "maplestreetbakery.com", "phone": "(419) 555-0100", "facebook": "facebook.com/maplestreetbakery"}]
EOF
```

For one business, the flags `--name`, `--website`, `--phone`, `--facebook`, and `--email` work too. Each match lists the fields it matched on; a `similar name` match alone is a lead to compare by eye, not proof. Drop any candidate that already has a record, whatever its status. When the user named the business and it has a record, show them the record and ask what they want to do.

## 3. Check the strongest candidates

Rank the candidates by the costliest problem their listings hint at, then check them one at a time, strongest first, against `references/signals.md`. Stop at the first with a confirmed problem SDM fixes and a channel you can use (step 4); checking all eight costs an hour for the same answer. Between two that hold up, prefer the visibly engaged owner (replies to reviews, recent posts, updated hours), who reads messages.

Read pages as text (a fetch or the browser's page-text tool) rather than screenshots, which are slower and costlier. Use Justin's signed-in Chrome for Facebook, which walls off signed-out browsers (search Pages for the name before writing "no Facebook Page"), and for the phone-width check. Click every link on the Google profile: a Website button leading to a dead or unrelated page is easy to miss. The message names one of these problems to the owner, and getting it wrong costs the whole pitch, so every problem has to be one you saw yourself on this run.

If none of them has a real problem, say so, write `passed` records for the ones you checked, and offer another town or industry. Don't stretch a weak case.

## 4. Choose the service and the channel

Search firelandscurrent.com for the business's name first. If the paper is covering it in an active news story, pass on it (see "Firelands Current" below).

**Service.** Choose the single SDM service that fixes the most important problem you found, using the mapping in `references/signals.md`. The message can mention SDM's other services in one sentence, but it pitches one thing. A message that offers everything says nothing about this business.

**Channel.** Use the first one that exists, in this order:
1. An email address the business publishes itself (its website, Facebook About, Google profile).
2. The contact form on its own website.
3. Facebook Message to its Page.
4. Another channel the business publishes for inquiries, such as an Instagram DM or a LinkedIn company page.

Use only addresses the business published, and note in the record where and when you saw the one you use, so the source is on file if anyone asks. Don't guess `info@` addresses or use email finders and data brokers: guesses bounce or reach the wrong person, and scraped lists are what make outreach spam. Never use Nextdoor, Yelp messaging or "Request a Quote," Google review replies or Business chat, public posts or comments, or a text to the business's phone. Those platforms ban solicitation, and a public pitch reads badly to the business's customers. If the only channel is the phone, write the record, give Justin the number and a two-line talking point, and stop.

## 5. Write the message

Write it to the owner, as Justin, in his own plain voice: a local business owner writing to another one. Follow `references/sdm.md` for which facts about Justin and SDM you can use.

The message, in this order:
1. A greeting by name if the business's own site or Page names the owner, otherwise to the business ("Hi Maple Street Bakery team").
2. Who Justin is, in one sentence: founder of Stone Dragon Media, a web design and digital strategy company in Sandusky (adjust "in Sandusky" to "nearby" or "here in the area" for other towns).
3. The specific thing you noticed and what it likely costs them, in a sentence or two. Describe it as an observation, not a verdict, and never insult their work: "When I opened your site on my phone, the menu ran off the screen" rather than "Your website is outdated."
4. What SDM would do about it, concretely.
5. One sentence on what else SDM does, and only if it fits, a short mention of advertising in Firelands Current (see below).
6. One low-pressure ask, by default an offer to send a few notes on what he found ("Want me to send them over?"). A yes is easy to give and shows real interest; a call can come after. Offer a free conversation instead only when the problem needs talking through. Don't offer both: two asks split the reply. Invite a reply on this same channel.
7. An opt-out line in plain words, such as "If this isn't useful, just let me know and I won't reach out again."
8. Sign-off: Justin Musick, Founder, Stone Dragon Media, and his phone number. Emails also carry the mailing address from `sender.md`, because U.S. law (CAN-SPAM) requires a valid postal address in commercial email. A P.O. box or registered mailbox is fine.

Keep the body (everything above the sign-off) to 75–125 words for emails and forms and 60–100 for Facebook, whose inbox preview shows only the first line or two. Owners read these on a phone between customers, and a long message reads like a form letter. Give the phone number once, in the sign-off. For an email, write a plain subject line of two to six words that names the business or the topic, like "Maple Street Bakery's website." Never write a fake "Re:" or a misleading subject, which CAN-SPAM also prohibits.

**No links in a first message**: no URLs, no bare domains (email apps turn `stonedragonmedia.com` into a link), and no email address in the body or signature. A link from a stranger looks like phishing and gets filtered. The business can reply or call.

Build the pitch only from what you saw yourself and what the business published. Never use a customer's review or a resident's post (a complaint, a "can anyone recommend…") in a first message or a follow-up, and never tell the business where you found it: quoting their customers back at them reads like surveillance.

Don't invent a connection or experience: no "I've been a customer for years," "a friend recommended you," or "I drove past your shop" unless Justin told you so in this conversation. Don't promise results or quote prices; SDM's pricing depends on scope.

Then, in this order:
1. Run the **humanize** skill on the draft in Rewrite mode, and tell it to keep every fact, the opt-out line, the signature, and the no-links rule.
2. Only then write the record, with `status: drafted` and the humanized message (subject, body, and sign-off) under `## Message`, `Subject: ...` first for an email. Humanize changes the length, so a check run before it is wasted. A follow-up run quotes the message from here.
3. Run `check_message.py <record file>`. It reads the message and channel from the record, counts the body words (drafts run long and estimates run short), and flags links, a phone number in the body, a missing sign-off, and a bad subject line.
4. Fix every issue it lists in the record, confirm its warnings by eye, and check that humanize kept every fact. Rerun until it passes.

## 6. Get Justin's approval

Show Justin, in this order:
- the business, town, and a one-line reason it was chosen
- the evidence, with where each fact came from
- the service being pitched
- the channel and the exact destination (the address, form URL, or Page)
- for a form, every field and the value that will go in it
- the final message, exactly as it will be sent, with its body word count from the check

Then ask: send it, edit it, or pass on this business. Send nothing until he says yes to this message. His name is on it, and a sent message can't be taken back. An edit means updating the record, rerunning the check, and asking again.

## 7. Send it and record it

Use Justin's real browser, where he's signed in (Claude in Chrome, or the browser your agent has that uses his sign-ins), read that browser's skill first if your agent has one, and follow the channel's section of `references/channels.md`. Above all: email goes from stonedragonmedia@gmail.com, not whichever Google account Gmail opens first, so replies land in SDM's inbox; and if a form has a CAPTCHA, stop and let Justin complete and submit it himself.

After sending, confirm it went: Gmail's "Message sent," the form's thank-you page, the message appearing in the Facebook thread. Then update the record: `status: sent`, `first_contact`, the final text, and a History line. If sending failed, say so, keep `status: drafted`, and record what happened.

End by telling Justin what was sent, where, and when a follow-up would be due (seven days out).

## Firelands Current

SDM owns Firelands Current, a local news site. Advertising in it may be mentioned in one clause when the business sells to local customers and the paper's readers are its market: "We also run Firelands Current, the local news site, if you ever want to reach readers in the area." Keep the newsroom and sales separate, because the paper's credibility depends on readers believing coverage can't be bought:
- Never mention a story the paper ran or might run about the business, and never suggest that advertising affects coverage.
- Don't pitch a business the paper is covering in an active news story (step 4 checks).
- Don't use anything learned through the newsroom (tips, sources, interviews) in a pitch.
