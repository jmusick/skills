# Drafting an application

Prepare everything one application needs so Justin can review it and submit it himself. Everything goes in `applications/<company>-<role>/` (the folder name from `jobs.py slug`), and the record moves to `status: drafted`.

## 1. Load the job

Find the record with `jobs.py match`. A URL or company with no record goes through steps 3 and 4 of the search first: check it against the records, find the employer's posting, look for knock-outs, judge the fit, and write the record.

If the record was found more than three days ago, open the employer's posting again: if it has closed, set `status: closed`, tell him, and stop. Then read the record's posting text, `application-answers.md`, and the master resume.

## 2. See what the application asks

Read the application form when it's visible without signing in or starting an application: its questions, which uploads it takes, and whether it has a spot for a cover letter. Don't click Apply on LinkedIn or Indeed to find out (see the rules in SKILL.md), and don't create an account on an employer's site to see the form. Where the form is hidden, prepare for the usual questions (work authorization, sponsorship, years of experience with the posting's main tools, salary, start date, relocation, how he heard about the job) and say the real form may ask more.

**Knock-out check.** Before drafting, look for questions that screen people out automatically: a yes/no on a bachelor's degree, a minimum number of years, willingness to work on-site or relocate, a salary cap. If his true answer could get him rejected, stop and show him the question and his answer. Ask whether to go ahead. Never shade an answer to get past a filter: a false yes on a degree surfaces in the background check.

## 3. The resume

Use the master `resume/justin-musick-resume.pdf` unless the posting stresses something the master buries: a must-have that sits in his second job's last bullet, a skill missing from the summary, a lead or management angle the headline doesn't show. Then tailor, and say what changed and why.

To tailor:
1. Copy `resume/build-resume-docx.py` into the application folder and point its output at `justin-musick-resume-<company>.docx` in that folder.
2. Change only:
   - the headline under his name, when the posting's title says it more plainly
   - the professional summary (2 or 3 short sentences aimed at this role)
   - the order of the skills, so the posting's must-haves come first
   - the order of bullets within a job, and wording that mirrors the posting's terms where his experience truly matches them
3. Leave the rest alone: job titles, employers, dates, and locations stay exactly as they are, every job stays, nothing gets added that the master doesn't say, and it stays at two pages or fewer. Any line he'd struggle to explain in an interview comes out.
4. Build it with a Python that has `python-docx` (ask him before installing it), then export the PDF with LibreOffice: `"C:\Program Files\LibreOffice\program\soffice.exe" --headless --convert-to pdf --outdir <folder> <docx>`. Look at every page before calling it done: a page with one stray line or a heading stranded at the bottom gets fixed.

Upload systems read text, not layout, so keep the master's single column: no tables, text boxes, or images holding content.

## 4. The cover letter

Write one only when the form has a spot for one or the posting asks for it. An unrequested letter on an Easy Apply flow goes unread.

- 250–350 words in three or four paragraphs, one page.
- **Open** with the role and one specific reason this employer: something from the posting or the company's own site, not "I am excited to apply."
- **Middle**: the posting's two or three most important requirements, each matched to real evidence from the resume (a system, a scale, a result). Use his numbers exactly as the resume states them.
- Mention Stone Dragon Media, Firelands Current, Tagstash, or the Hidden Lodge platform when the role values what they show (owning a product end to end, client work, web or CMS work, starting something), in a sentence, not a paragraph.
- **Close** with one plain line asking to talk.
- No "perfect fit", "passionate", "proven track record", "fast-paced", or "I believe I would be a great addition." Write it the way he'd talk.

Run the draft through the **humanize** skill in Rewrite mode, telling it to keep every fact, number, and name. Then check that it did.

Build it from the newest letter in `applications/` (`tebra/build-cover-letter.py` set the style): copy the script into the folder, replace the date, recipient, salutation, and body, and set the output to `justin-musick-cover-letter-<company>.docx`. Export and check the PDF the same way as the resume. Address a named hiring manager only if the posting or company site names one; otherwise "Dear <Company> Hiring Team".

## 5. Screening answers

Write `screening-answers.md` in the folder: each question exactly as the form words it, then the answer to paste or select.

- Take every standard answer from `application-answers.md`: contact details, work authorization, sponsorship, relocation, travel, self-identification, the outside-business disclosure (change the company name in its last sentence), and the approved written answers.
- **Salary**: the midpoint of the posted range, rounded to the nearest $5,000 and never below $80,000. With no range posted, $80,000. State the number and the reason in the file so he can change it.
- **Years with a tool**: count from the resume's dates, and say which jobs the count covers.
- **Degree**: high school diploma, as `application-answers.md` records it. Where a form allows a note, add his years of professional experience, counted from the resume's dates.
- A question the answer bank doesn't cover, or a written answer longer than a sentence: draft it from the resume, run it through humanize, and mark it **new, confirm before using**. When he approves one that will come up again, add it to "Short written answers" in `application-answers.md` with the company and date, so the next form can reuse it.
- A TODO in the answer bank that this form needs: ask him once, then fill it in there.

## 6. Hand it over

Set the record to `status: drafted`, list the files under `## Application`, and add a History line. Then show him:
- the job, and the employer's link to apply
- which resume to upload, with what changed if it was tailored
- the cover letter, if there is one
- every screening answer marked new, and any knock-out question
- the salary answer and its basis
- anything the form may ask that wasn't visible

He submits. When he says it's sent, update the record (Update mode in SKILL.md).
