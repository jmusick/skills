---
name: title
description: Renames the current chat session so its title reflects what actually happened in the conversation, not just the opening request.
disable-model-invocation: true
---

# Title

Chats drift, and the auto-generated title only reflects the opening request. Rename the session to match what was really done, so the user can find it later in their sidebar. This is quick housekeeping: don't redo or re-verify any work.

If the command came with an exact title (`/title Stripe webhook retry fix`), use it as written and skip step 2. Other text (`/title focus on the deploy fix`) is guidance on emphasis.

## 1. Check the current title

In the Claude desktop app, call `mcp__ccd_session_mgmt__get_session` with `session_id: "self"`. Elsewhere there's usually no way to read the title; skip this step.

## 2. Decide the title

Read from the first message to now. A compacted summary counts as the record of the beginning; it's often the only place the original intent survives. Skip meta turns: this `/title` call, greetings, and small wording tweaks say nothing about what the session was for.

- Name where it ended up (what was built, fixed, decided, or learned), since that's what the user will search for: "Fix race condition in upload queue", not "Chat about upload issues". A chat that started as "why is my build slow" and ended with a circular import removed becomes "Fix circular import slowing Vite build".
- If the work ended unfinished, don't claim it was done: "Debugging flaky Playwright login test", not "Fix ...".
- Use specific nouns (project, feature, tool, the bug's symptom), plus the issue, PR, or ticket number if the session centered on one ("Fix #42 login redirect").
- Two separate threads can be joined ("Add CSV export + fix date parsing"). With more, name the one that took most of the session and mattered most to the result.
- 3 to 8 words, under about 60 characters, because sidebars truncate. Sentence case, no trailing period, quotes, or emoji, in the language the conversation was held in.
- Keep secrets out: no tokens, passwords, client names under NDA, or personal contact details. Titles show in sidebars, shared screens, and synced devices.

If the current title already fits, say so and stop.

## 3. Rename and report

If you have a tool that renames the current session, use it: in the Claude desktop app, `mcp__ccd_session_mgmt__set_session_title` with `session_id: "self"`. Then reply in one line, adding a short clause on why only if the change isn't self-explanatory:

> Renamed: **Old title** → **New title**

If there's no rename tool, don't pretend the rename happened. Give the title in a form that's easy to copy (`Suggested title: \`...\``) and say where to apply it: `/rename <title>` in the Claude Code CLI, or the sidebar's rename option in the Codex app and other tools.
