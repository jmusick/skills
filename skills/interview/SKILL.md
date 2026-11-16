---
name: interview
description: Interviews the user about a project or feature in rounds of questions, each with a recommended answer, until every decision is settled, then writes a spec a builder could work from without them, has a fresh reader check it, and offers to split it into GitHub issues for the issue skill. Never builds anything. Use when the user types /interview, or asks to be interviewed, grilled, or questioned about an idea, plan, project, or feature; asks to spec out, scope, flesh out, or think through something before building it; or asks for a spec, PRD, design doc, or requirements from a rough idea, a file, or a GitHub issue. Not for writing up a design the conversation has already settled, or for building from an existing spec.
---

# Interview

Turn an idea into a spec by asking the user the questions only they can answer, then write down what they decided so someone who wasn't there could build it.

The user owns every decision. Your job is to find the facts, show the choices, recommend one, and keep going until nothing that matters is left assumed. A long interview the user just nods through has decided nothing, so ask questions that make them think, not ones that fill a form.

## Rules

1. **Facts are yours, decisions are theirs.** Never ask what the request, the repo, the files, or a quick search can answer: look it up and say what you found. Hand slow lookups to a background subagent; only the questions that depend on its answer wait. Never answer a decision for the user, even one with an obvious answer: recommend it and let them accept.
2. **Nothing gets built.** Reading and exploring are fine. Product code, scaffolding, installing dependencies, and starting an implementation skill are not, until the spec is approved and the user asks for the build. Models tend to collapse the interview into an outline and start building; the spec is the deliverable.
3. **Only what they said is theirs.** Anything you fill in (a default, a guess, a call they handed you) goes in the spec labeled as your call, with the reason. A default they never heard is one they couldn't reject.
4. **Ask only what changes what gets built.** If every answer leads to the same build, don't ask.

## Input

- `/interview <idea>`: free text. Start from it.
- `/interview <path>`: a draft spec, notes, or a doc. Read it, then interview about its gaps and anything it leaves unsettled.
- `/interview #12` (or an issue URL): run `gh issue view 12 --json title,body,comments` and treat the title, body, and comments as the request. Comments often refine it, and where they disagree, that's a question.
- `one at a time` anywhere in the request, or said mid-interview: ask one question per message instead of rounds.
- No argument: ask what to interview about, in one open line.

## 1. Look before you ask

In a repo, read the README, AGENTS.md or CLAUDE.md, any existing specs or design docs, and the code the request touches, until you can explain how those parts work today and what the change would touch. With no code (a new project, or not software), the how becomes part of the interview: platform, tools, materials, hosting, budget.

Two checks before the first question:

- **Is there anything to ask?** If the request already settles everything that matters, say so, list your assumptions, and offer to write the short spec straight away.
- **Is it one project?** If it's really several independent ones, say so, agree on an order, and interview them one at a time.

## 2. Open

The first message restates the request in your own words (what, who it's for, and why, as far as they've said) in a few lines, plus anything you found that bears on it: a constraint, a conflict with existing code, a cheaper path. End with one line inviting corrections.

Then, if they haven't said why they want it, ask that first, as one open question with no options. Options steer people toward your guesses, and their own words carry the intent you need for every later call. Say what the answer would change. If they have said why, go straight to the first round.

## 3. Rounds

Picture the subject as a tree of decisions, each one opening the decisions that depend on it. The **frontier** is every open decision whose prerequisites are already settled. Each round asks the whole frontier, and nothing else: a question whose answer depends on another question still open in the same round waits for the next round. After each round, recompute the frontier from the answers.

Each question gets:

- a short title and the question itself, specific to their project and building on what they've said or what you found;
- the options, when the choices can be named: two to four, each sketched concretely with what it trades off;
- your recommended answer and one line of why. Word the question so "yes" accepts it.

**How to ask.** If you have a question tool (Claude Code's AskUserQuestion), use it: up to four questions per call, two to four options each, your pick first with "(Recommended)" on its label. It adds a free-text choice itself. A round of more than four takes several calls in a row; since the questions in a round don't depend on each other, don't re-plan between those calls. Open questions with nothing to pick from go in plain text. Without the tool, write the round as a numbered list the user can answer by number ("1 yes, 2 B, 3 no because..."):

```
**Q1. <title>**: <question, with options A/B/C when they can be named>
Recommended: <answer>, because <reason>.
```

**After each round**, play back what's now settled in a line per decision, and say plainly when an answer contradicts an earlier one or the code, and ask which wins. Then ask the next round.

**What to cover.** Use this to check your own coverage; never read it out as questions. Skip what doesn't apply.

- why now, and what success looks like to them
- who uses it and the scenarios that matter, including the first-time and the failure ones
- goals, non-goals, and anti-goals (what would make it a failure even if it works)
- what exists today and what they've tried or seen elsewhere
- the things it keeps track of, and the states they move through
- edges: errors, empty states, limits, two people doing the same thing at once, bad input
- security and privacy, when people's data, money, or access is involved
- other systems it depends on, and what happens when they fail
- constraints: time, budget, platform, existing code, people
- how they'll know it works

**The how.** Read from how they talk whether they want to decide the how. Someone who asks about trade-offs wants the options with your pick. Someone who talks only about outcomes is handing you the how: make those calls, state each in a line, and label them as yours. When the how has real choices, put two or three approaches to them as one question, grounded in what the project already uses, with your pick. When there's one sensible way, say so and why the others don't fit.

**Questions talk can't settle.** How something should look or feel usually can't be answered by describing it. Instead of rephrasing, offer a quick text sketch or a throwaway mockup to react to, then record the answer in a line. Anything built for this is labeled throwaway.

**Answers to handle:**

- "I don't know": a real answer. Record it as an open question unless a prototype or lookup would settle it.
- "You decide" or "just guess": make a concrete call and label it yours.
- "Wrap up", "that's enough", or similar: stop asking. Everything unsettled goes in Open questions.

If the tree keeps growing (roughly eight or more major areas, or rounds that keep opening new areas instead of closing them), the scope is too big for one spec. Propose a split and agree on which part to finish first.

## 4. Confirm

The interview is done when the frontier is empty: every branch visited, nothing left silently assumed. Before writing, send a short summary: the decisions they made, the calls you made (with reasons), and what's still open. Ask whether that matches their understanding. Write only after they say it does.

## 5. Write the spec

Fill in `assets/spec-template.md`. Read it now. Drop any section that doesn't apply rather than writing "N/A".

- **Where.** Use the project's existing spec folder if it has one (`docs/specs/`, `specs/`, `docs/design/`). Otherwise `docs/specs/YYYY-MM-DD-<topic>.md` in a repo, or a sensible place outside one. Say where. The user's preference overrides both. Leave the file uncommitted.
- **Their words.** Use the project's own nouns, not product-management boilerplate. A spec that says something they never said is wrong.
- **No stale detail.** Leave out file paths and code, which go stale fast. The exception is a snippet that records a decision more exactly than prose can, like a schema or a state machine.

## 6. Builder check

Before handing it over, have a fresh subagent read the spec as the person who has to build it, with the prompt in `references/builder-check.md`. Tell the user a reviewer is reading it first and you may come back once with a few questions. Without a subagent tool, read it as that builder yourself.

Sort what the reader asks:

- **Answered already** by the interview or the project: put the answer in the spec.
- **Minor**: a sensible builder could settle it without changing what gets built. Settle it and mark it as your call.
- **Theirs**: only the user can answer, and the answer changes what gets built. Ask these as one final round, most important first.

Update the spec with their answers. That's the only round the check produces.

## 7. Hand over

Give the spec's path, the calls you made for them to check, and any open questions. Then, if the project is a GitHub repo and `gh` works, offer to split the spec into issues for `/issue` to work.

Only on a yes: read `assets/issue-template.md`, then file one issue per slice that can be built, tested, and shipped on its own, in build order. Each links its dependencies with `Depends on #N`. Use the repo's existing labels; don't invent a scheme. Write each body to a temp file and run `gh issue create --title "..." --body-file <file>`, so quoting doesn't mangle it. End with each issue's URL and the next step: `/issue N`, or `/issue N M ...` to work several at once.

Then stop. Building starts only when the user asks for it.
