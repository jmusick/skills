---
name: prospect
description: Find one local business in Stone Dragon Media's coverage area, match it to the SDM service that would help it most, and send Justin Musick's first outreach message by email, contact form, or Facebook after he approves it.
disable-model-invocation: true
---

# Prospect

Find one local business that Stone Dragon Media can actually help, show Justin why, and send a first message he'd be glad to have his name on. Quality beats volume. A badly aimed pitch from a local agency gets remembered around town, so one well-researched message is worth more than ten generic ones.

`references/sdm.md` holds what SDM sells, where it works, and the facts about Justin the message can use. Read it at the start of every run.

## Modes

- **New** (default): `/prospect`, optionally with a town, an industry, or a named business ("/prospect Huron restaurants", "/prospect Maple Street Bakery"). Runs steps 1–7.
- **Follow-up**: `/prospect follow-up`. Read [references/follow-up.md](references/follow-up.md) and follow it.
- **Update**: the user reports a reply, a no, or an opt-out ("Maple Street said no thanks"). Update that business's record and stop.

If the user asks for several businesses, run the loop once per business, each with its own approval.

## The outreach folder

Records live in `C:\Users\JD\projects\stone-dragon-media\Outreach\` unless the user names another folder. Create it on first use.

- `sender.md`: Justin's details for signatures and forms: name, title, phone, the email address to send from (always stonedragonmedia@gmail.com), a mailing address for emails (see step 5), and which Facebook identity to message from. On a first run, or when a field the message needs is missing, ask for it once and save it. Don't guess any of it.
- One file per business, `<town>-<business-slug>.md`, created the moment a business is ruled in or out. Format:

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
follow_up: null
---

## Why this business
The evidence from step 3, with the URL or place each fact came from.

## Message
The exact text that was sent, with the subject line if it was an email.

## History
- 2026-11-10: sent by email from stonedragonmedia@gmail.com
```

Passed-over businesses get a short file with `status: passed` and one line on why, so later runs don't research them again.

## 1. Check the record before anything else

The record check is a script, because a business may be filed under a different name (an LLC, an owner's name) and only its website, phone, or Page gives it away. Before you research any candidate, run:

```bash
python <this skill's directory>/scripts/outreach.py match <outreach folder> --name "<name>" --website <url> --phone "<phone>" --facebook <page url>
```

Pass whichever of those you have (use `python3` if `python` isn't found). Each match lists the fields it matched on; a `similar name` match alone is a lead to compare by eye, not proof. Skip any business that already has a record, whatever its status. The one exception is when the user names a business that has a record: show them the record and ask what they want to do.

## 2. Find candidates

When the user gave no town, pick one from the coverage list in `references/sdm.md`, favoring in-person towns with the fewest records (`outreach.py towns <outreach folder>` counts them) so the outreach spreads across the area. Then gather five to eight candidates with web search, Google Maps, and Facebook: local, independently owned businesses that sell to the public or to other local businesses.

**Facebook as a lead source.** Facebook turns up the strongest kind of candidate: a business whose only presence online is a Facebook Page. Use Justin's signed-in Chrome, and read only:
- Search Facebook Pages for the town and a category (`facebook.com/search/pages/?q=<category> <town>`), and look through the town's public community and buy-local groups for businesses that people name.
- Search a few times, at a normal person's pace. Don't scroll the feed to build lists, and don't collect anything beyond a business's name and its Page. Meta's terms restrict automated collection, and this is Justin's personal account.
- Don't like, follow, join, comment, react, or message anyone while researching. Those are public actions he didn't approve.
- Use only what the business itself published. Never use a resident's post (a complaint, a review, a "can anyone recommend…") in a pitch, and never tell the business where you found it.
- Nextdoor is off limits for research as well as for contact. Its terms prohibit commercial prospecting, and a pitch built from neighbors' posts reads like surveillance.

Leave out, without researching further:
- chains, franchises, and national brands, which buy marketing centrally
- web designers, marketing agencies, and IT shops (competitors)
- government offices, schools, and churches, unless the user asks for them
- businesses that look closed: marked "permanently closed," a dead phone, no activity anywhere in over a year
- SDM's current clients, and anyone Firelands Current is covering in an active news story (see "Firelands Current" below)

## 3. Look at each candidate's online presence

Use the signals in `references/signals.md`: check the website, the Google Business Profile, and the Facebook Page, and note what's missing, broken, or outdated. Facebook shows a login wall to signed-out browsers, so check the Page, and whether one exists at all, in Justin's signed-in Chrome. Search Facebook Pages for the business name before writing "no Facebook Page." Click every link on the Google profile too: a Website button that leads to a dead or unrelated page is easy to miss and costs the business customers. Check every problem yourself before writing it down. Load the site on a phone-width viewport before saying it isn't mobile-friendly, and open the page before calling a link broken. The message will name one of these problems to the owner, and getting it wrong costs the whole pitch.

Pick the candidate with the clearest problem SDM fixes and a contact channel you can actually use. Between close candidates, prefer an owner who is visibly engaged: recent reviews with the owner's replies, recent posts, updated hours. An engaged owner reads messages and is more likely to act on one. If none of them has a real problem, say so, write `passed` records, and offer another town or industry. Don't stretch a weak case.

## 4. Choose the service and the channel

**Service.** Choose the single SDM service that fixes the most important problem you found, using the mapping in `references/signals.md`. The message can mention SDM's other services in one sentence, but it pitches one thing. A message that offers everything says nothing about this business.

**Channel.** Use the first one that exists, in this order:
1. An email address the business publishes itself (its website, Facebook About, Google profile).
2. The contact form on its own website.
3. Facebook Message to its Page.
4. Another channel the business publishes for inquiries, such as an Instagram DM or a LinkedIn company page.

Use only addresses the business published, and note in the record where it published the one you use and the date you saw it, so the source is on file if anyone asks how Justin got it. Don't guess `info@` addresses or pull them from email-finder sites and data brokers: a guessed address bounces or reaches the wrong person, and buying or scraping lists is what makes outreach spam. Never use Nextdoor, Yelp messaging or "Request a Quote," Google review replies, or comments on posts. Those platforms ban solicitation, and a public pitch on someone's page reads badly to their customers. If the only channel is the phone, write the record, give Justin the number and a two-line talking point, and stop.

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

Keep the body (everything above the sign-off) to 75–125 words for emails and forms and 60–100 for Facebook. Owners read these on a phone between customers, and a long message reads like a form letter. A Facebook message shows only its first line or two in the inbox preview. Give the phone number once, in the sign-off, not in the body too. For an email, write a short, plain subject line (two to six words) that names the business or the topic, like "Maple Street Bakery's website." Never write a fake "Re:" or a misleading subject, which CAN-SPAM also prohibits.

**No links in a first message.** That means no URLs, no bare domains (email apps turn `stonedragonmedia.com` into a link), no email address written into the body, and no signature block that adds them. A link from a stranger looks like phishing and gets filtered. The business can reply or call. The phone number is fine.

Don't invent a connection or experience: no "I've been a customer for years," "a friend recommended you," or "I drove past your shop" unless Justin told you so in this conversation. Don't promise results or quote prices; SDM's pricing depends on scope.

Then, in this order:
1. Run the **humanize** skill on the draft in Rewrite mode, and tell it to keep every fact, the opt-out line, the signature, and the no-links rule.
2. Save the humanized message (with `Subject: ...` as the first line for an email) to a scratch file and run `python <this skill's directory>/scripts/check_message.py <file> --channel email|form|facebook`. It counts the body words and flags links, bare domains, email addresses, a phone number in the body, a missing sign-off, and a bad subject line. Drafts run long and estimates run short, which is why the count is a script.
3. Fix every issue it lists, confirm its warnings by eye, and check yourself that humanize kept every fact. Rerun until it passes. Report its word count in step 6.

## 6. Get Justin's approval

Show Justin, in this order:
- the business, town, and a one-line reason it was chosen
- the evidence, with where each fact came from
- the service being pitched
- the channel and the exact destination (the address, form URL, or Page)
- for a form, every field and the value that will go in it
- the final message, exactly as it will be sent, with its body word count

Write the record with `status: drafted` and the full message (subject, body, and sign-off) under `## Message`, since a follow-up run quotes it from there. Then ask: send it, edit it, or pass on this business. Send nothing until he says yes to this message. His name is on it, and a sent message can't be taken back. An edit means showing the revised message and asking again.

## 7. Send it and record it

Use Justin's real browser, where he's signed in (Claude in Chrome, or the browser your agent has that uses his sign-ins), and read that browser's skill first if your agent has one. `references/channels.md` covers each channel's steps and traps. Most important:

- **Email** always goes from stonedragonmedia@gmail.com. Chrome may be signed in to several Google accounts, so confirm the From address is that one before sending, not whichever account Gmail opens first. Replies need to land in SDM's inbox. Remove any signature Gmail adds automatically if it contains links.
- **Contact forms**: fill in only the fields shown in step 6. If the form has a CAPTCHA or "I'm not a robot" check, stop and ask Justin to complete and submit it himself. Don't try to get around it.
- **Facebook**: send from the identity in `sender.md`.

After sending, confirm it went: Gmail's "Message sent," the form's thank-you page, the message appearing in the Facebook thread. Then update the record: `status: sent`, the date, the channel, the final text, and a History line. If sending failed, say so, keep `status: drafted`, and record what happened.

End by telling Justin what was sent, where, and when a follow-up would be due (seven days out).

## Firelands Current

SDM owns Firelands Current, a local news site. Advertising in it may be mentioned in one clause when the business sells to local customers and the paper's readers are its market: "We also run Firelands Current, the local news site, if you ever want to reach readers in the area." Keep the newsroom and sales separate, because the paper's credibility depends on readers believing coverage can't be bought:
- Never mention a story the paper ran or might run about the business, and never suggest that advertising affects coverage.
- Don't pitch a business the paper is covering in an active news story. Check firelandscurrent.com for its name before you choose it.
- Don't use anything learned through the newsroom (tips, sources, interviews) in a pitch.
