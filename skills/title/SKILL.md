---
name: title
description: Renames the current chat session so its title reflects what actually happened in the conversation, not just the opening request.
disable-model-invocation: true
---

# Title

Chats drift, and the auto-generated title only reflects the opening request. Rename the session to match what was really done, so the user can find it later in their sidebar. This is quick housekeeping: don't redo or re-verify any work. Read, decide, rename, report.

## 1. Review the whole conversation

Read from the first message to now. A compacted summary counts as the record of the beginning; it's often the only place the original intent survives. Work out:

- **Where it ended up:** what was built, fixed, decided, or learned. This weighs most, because it's what the user will search for.
- **The main thread vs. detours:** weight topics by how much of the session they took and how much they mattered to the result.
- **Concrete anchors:** project, feature, tool, or the bug's symptom. Specific nouns make a title findable.

Skip meta turns when weighing topics: this `/title` call, greetings, and small wording tweaks say nothing about what the session was for.

Text passed with the command (`/title focus on the deploy fix`) is guidance on emphasis. An exact title (`/title Stripe webhook retry fix`) is used as written.

## 2. Check the current title

In the Claude desktop app, call `mcp__ccd_session_mgmt__get_session` with `session_id: "self"`. Elsewhere there's usually no way to read the title; skip this step.

If the current title already fits, say so and leave it alone.

## 3. Write the new title

- 3 to 8 words, under about 60 characters, because sidebars truncate.
- Lead with the outcome or subject, not the conversation: "Fix race condition in upload queue", not "Chat about upload issues".
- Sentence case, no trailing period, quotes, or emoji.
- Write it in the language the conversation was held in.
- If the session centered on one issue, PR, or ticket, include its number ("Fix #42 login redirect"); it's often what the user searches for.
- Keep secrets out: no tokens, passwords, client names under NDA, or personal contact details. Titles show in sidebars, shared screens, and synced devices.
- Two separate threads can be joined ("Add CSV export + fix date parsing"). With more than two, name the one that mattered most.
- If the work ended unfinished, don't claim it was done: "Debugging flaky Playwright login test", not "Fix ...".

For example, a chat that started as "why is my build slow" and ended with a circular import removed becomes "Fix circular import slowing Vite build".

## 4. Rename and report

If you have a tool that renames the current session, use it. In the Claude desktop app that's `mcp__ccd_session_mgmt__set_session_title` with `session_id: "self"`. If the user set the title by hand, the app may ask them to approve; let it. Then reply in one line:

> Renamed: **Old title** → **New title**

Add a short clause on why only if the change isn't self-explanatory.

If there's no rename tool, don't pretend the rename happened. Give the title in a form that's easy to copy (`Suggested title: \`...\``) and say where to apply it: `/rename <title>` in the Claude Code CLI, or the sidebar's rename option in the Codex app and other tools.
