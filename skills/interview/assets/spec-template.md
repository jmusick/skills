# {Title: what this is, in the project's words}

{YYYY-MM-DD} · Draft · Written from an interview with the user

## Problem and why

{The problem, from the point of view of the people who have it. Why it matters, and why now. A builder who reads only this section should know what a good result is for.}

## Goals

- {What it must achieve. Make each one checkable: "a member can vote from their phone in under a minute", not "easy voting".}

**Non-goals**

- {What it deliberately won't do, in this version or at all. The things the user turned down are often the most useful lines in the spec.}

**Anti-goals**

- {What would make it a failure even if it technically works.}

## Users and scenarios

{Who uses it. Then the scenarios that matter, most important first. Each one is a slice that could be built and shown on its own.}

### {Scenario title} (priority 1)

{One or two sentences on what happens and why it matters.}

- **Given** {starting state}, **when** {action}, **then** {result}.
- **Given** {...}, **when** {...}, **then** {...}.

### {Scenario title} (priority 2)

{...}

## Decisions

| # | Decision | Why | Decided by |
| --- | --- | --- | --- |
| D1 | {What was decided} | {The reason given, or the trade-off that settled it} | user |
| D2 | {A call made for the user} | {The reason} | agent |

{"user" means the user chose it in the interview. "agent" means the interviewer made the call (a default, or a choice the user handed over), so check those first.}

## Approaches considered

{Only when the how had real choices. The two or three approaches weighed, what each trades off, which was picked, and why the others lost.}

## Constraints

- {Time, budget, platform, existing code or systems, people, legal. What the builder can't change.}

## Edge cases and failures

- {Errors, empty states, limits, concurrent use, bad input, a dependency being down: what should happen in each.}

## Open questions

- {What is still undecided, who can settle it, and what it blocks. Write "None" only if nothing is open.}

## Left to the builder

- {What the user doesn't mind either way, so the builder can decide without asking.}
