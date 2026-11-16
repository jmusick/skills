---
name: title
description: Renames the current chat session so its title says what was actually done, not just what the first message asked. Use when the user types /title or $title, asks to rename, retitle, or fix the title of this chat, session, conversation, or thread, or says its title is wrong, stale, or out of date. Not for writing titles of other things (posts, documents, PRs, commits, headlines), and don't use it unasked at the end of other work.
---

# Title

Chats drift. A session that opens with "fix the login button" can end up as a rewrite of the auth middleware, while the auto-generated title still says "Fix login button". Look back over the whole conversation and rename the session to match what was really done, so the user can find it later in a sidebar of fifty others.

This is quick housekeeping. Don't redo or re-verify any of the work, and don't write a summary. Read, decide, rename, report.

## 1. Read what came with the command

- An exact title (`/title Stripe webhook retry fix`): use it as written, without rewording or recasing it, and skip to step 4. The user chose those words.
- Other text (`/title focus on the deploy fix`, `/title shorter`): guidance on emphasis or form. Follow it in step 3.
- Nothing: decide the title yourself.

## 2. Check the current title

In the Claude desktop app, call `mcp__ccd_session_mgmt__get_session` with `session_id: "self"`. The session tools are often deferred; if so, load the pair in one call with `ToolSearch` and the query `select:mcp__ccd_session_mgmt__get_session,mcp__ccd_session_mgmt__set_session_title`.

Elsewhere (the Claude Code CLI, Codex, other agents) there's usually no way to read the title, so skip this step.

If the current title already fits the session, say so and leave it alone. Renaming for the sake of it only makes the sidebar harder to scan. The exception is an explicit request for a different or shorter title.

## 3. Decide the title

Read from the first message to now. If earlier turns were compacted, the summary counts as the record of the beginning; it's often the only place the original intent survives. Skip meta turns when weighing topics: this `/title` call, greetings, thanks, and small wording tweaks say nothing about what the session was for.

Work out three things:

- **Where it ended up.** What was built, fixed, decided, or learned by the end. This weighs most, because it's what the user will search for, and the opening request is often the part that turned out wrong.
- **The main thread vs. detours.** A ten-minute tangent about a lint error doesn't belong in the title of a database migration. Weigh topics by how much of the session they took and how much they mattered to the result.
- **Concrete anchors.** The project, feature, library, file, or the bug's symptom. Specific nouns are what make a title findable: "Migrate billing tables to Postgres 16" beats "Database work".

Then write it:

- Lead with the outcome or subject, not the conversation: "Fix race condition in upload queue", not "Chat about upload issues" or "Helping with a bug".
- 3 to 8 words, under about 60 characters, because sidebars cut long titles off.
- Sentence case, no trailing period, no quotes or emoji.
- Use the language the conversation was held in, even if the code or this skill is in another.
- If the session centered on one issue, PR, or ticket, include its number ("Fix #42 login redirect loop"). It's often the first thing the user searches for.
- Two genuinely separate threads can be joined: "Add CSV export + fix date parsing". With more, name the one that took most of the session and mattered most to the result.
- If the work ended unfinished, name what was being worked on and don't claim it was done. "Debugging flaky Playwright login test" is honest; "Fix flaky Playwright login test" isn't if it still fails.
- Keep secrets out: no tokens, passwords, API keys, private hostnames, client names under NDA, or personal contact details. Titles show in sidebars, on shared screens, and on synced devices, so a pasted credential that mattered to the work still stays out of the title.

| Started as | Actually became | Title |
| --- | --- | --- |
| "why is my build slow" | Found and removed a circular import, then set up a Vite cache | Fix circular import slowing Vite build |
| "help me write a cover letter" | Cover letter, then a full resume rework for a PM role | Resume and cover letter for PM role |
| "login test keeps failing" | Ruled out timeouts, still flaky when the session ended | Debugging flaky Playwright login test |
| "can you look at issue 118" | Traced the bug to a stale cache key and fixed it | Fix #118 stale cache key in search |
| "redis or memcached?" | Compared both, chose Redis for session storage | Choose Redis for session storage |
| "what does VACUUM do" | Explained why it was blocking writes on a big table | Why Postgres VACUUM blocks writes |

### Sessions that don't fit the pattern

- **Barely started.** If little has happened beyond the first request, title it by that request, stated plainly. Don't invent an outcome.
- **Questions and research, no code.** Name the subject or the answer, not the act of asking: "Why Postgres VACUUM blocks writes", not "Question about Postgres".
- **A decision.** Name the choice made, or the choice still open ("Redis vs Memcached for sessions") if none was.
- **Asked again after a rename.** The user didn't like the last title. Take any guidance they gave, and otherwise try a different angle (a different anchor or a shorter form) rather than a near-copy of the one they rejected.

## 4. Rename and report

If you have a tool that renames the current session, use it. In the Claude desktop app that's `mcp__ccd_session_mgmt__set_session_title` with `session_id: "self"` and the new title. If the user set the current title by hand, the app may ask them to approve the change; that's expected, so let it happen rather than working around it. Other agents may have their own rename tool, so look for one before falling back.

Rename only this session. Session tools can often reach other sessions too, but the user asked about this chat, and an unexpected rename elsewhere makes those sessions harder to find, not easier.

Then reply in one line:

> Renamed: **Old title** → **New title**

Add a short clause on why only when the change isn't self-explanatory, such as "the session moved from the login bug to the auth middleware rewrite". If you couldn't read the old title, show only the new one.

If there's no rename tool, you can't change the title yourself, so don't say or imply that you did. Give the title in a form that's easy to copy and say where to set it:

> Suggested title: `Fix circular import slowing Vite build`

- Claude Code CLI: run `/rename Fix circular import slowing Vite build`.
- Codex app: rename the thread from its entry in the sidebar.
- Anything else: use its rename option for the chat or thread.

Keep the reply to that. The user asked for a title, not a recap of the session.
