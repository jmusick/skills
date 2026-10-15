---
name: title
description: Renames the current chat session so its title reflects what actually happened in the conversation, not just the opening request. Use whenever the user types /title or $title, or asks to rename, retitle, or re-name "this chat", "this session", or "this conversation", or says the session's title is wrong, stale, or outdated. Do not use for writing titles of other things (blog posts, documents, PRs, commits, headlines).
---

# Title

Chats drift. A session that opens with "fix the login button" can end up as a rewrite of the auth middleware, and the auto-generated title still says "Fix login button". This skill looks back over the whole conversation and renames the session to match what was really done, so the user can find it later in their sidebar.

This is a quick housekeeping task. Don't redo or re-verify any of the work, and don't write a long summary. Read, decide, rename, report.

## Steps

### 1. Review the whole conversation

Go through the conversation from the first message to now. If earlier parts were compacted into a summary, treat that summary as the record of the beginning of the chat; it is often the only place the original intent survives.

Work out:
- **Where it ended up.** What was built, fixed, decided, or learned by the end. This carries the most weight, because it's what the user will be looking for when they search for this chat later.
- **The main thread vs. detours.** A ten-minute tangent about a lint error doesn't belong in the title of a session about migrating a database. Weight topics by how much of the session they took up and how much they mattered to the result.
- **Concrete anchors.** Project names, feature names, the tool or library involved, the bug's symptom. Specific nouns make a title findable.

If the user passed text with the command (e.g. `/title focus on the deploy fix`), treat it as guidance on emphasis. If they gave an exact title (e.g. `/title Stripe webhook retry fix`), use it as written.

### 2. Check the current title

Find out what the session is called now, using whatever your environment offers:

- **Claude desktop app (Claude Code tab):** call `mcp__ccd_session_mgmt__get_session` with `session_id: "self"`. These session tools are often deferred; if so, load them first with `ToolSearch` using `select:mcp__ccd_session_mgmt__get_session,mcp__ccd_session_mgmt__set_session_title`.
- **Anywhere else (Codex, the plain `claude` CLI, other agents):** there is usually no tool for reading the title. Skip this check and move on.

If you can see the current title and it already describes the session well, say so and leave it alone. Renaming for the sake of it isn't helpful.

### 3. Write the new title

Aim for something the user would recognize at a glance in a list of fifty sessions:

- **3 to 8 words, under about 60 characters.** Sidebars truncate long titles.
- **Lead with the outcome or subject**, not the conversation. "Fix race condition in upload queue", not "Chat about upload issues" or "Helping with a bug".
- **Be specific.** "Migrate billing tables to Postgres 16" beats "Database work".
- **Sentence case, no trailing period, no quotes or emoji.**
- **Two genuinely separate threads?** Join them: "Add CSV export + fix date parsing". If there are more than two, name the one that mattered most.
- **If the chat ended unfinished**, name what was being worked on; don't claim it was completed. "Debugging flaky Playwright login test" is honest; "Fix flaky Playwright login test" isn't, if it's still flaky.

Examples:

| Started as | Actually became | Good title |
|---|---|---|
| "why is my build slow" | Found and removed a circular import, then set up a Vite cache | Fix circular import slowing Vite build |
| "help me write a cover letter" | Cover letter, then reworked the whole resume for a PM role | Resume and cover letter for PM role |
| "create a skill called title" | Built and tested a session-renaming skill | Create /title session-rename skill |

### 4. Rename and report

**If you have a tool that renames the current session, use it.** In the Claude desktop app, that's `mcp__ccd_session_mgmt__set_session_title` with `session_id: "self"` and the new title. If the user set the current title by hand, the app may ask them to approve the change. That's expected; let it happen. Other agents may expose their own rename tool; look for one before falling back.

Then reply in one or two lines, showing the change:

> Renamed: **Old title** → **New title**

Add a short clause on why only if the change isn't self-explanatory (e.g. "the session moved from the login bug to the auth middleware rewrite").

**If no rename tool is available** (Codex, the plain `claude` CLI, and most other agents), you can't change the title yourself. Give the user the title in a form that's easy to copy, and tell them where to apply it:

> Suggested title: `Fix circular import slowing Vite build`

- **Claude Code CLI:** run `/rename <title>`.
- **Codex app:** rename the thread from its entry in the sidebar.
- **Other tools:** use their rename option for the chat or thread.

Keep it to that. Don't pretend the rename happened.
