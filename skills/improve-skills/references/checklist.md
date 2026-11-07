# Skill review checklist

Apply every section to every skill under review. The checker covers the spec's mechanical rules (frontmatter limits, size, links, nesting, contents lists, unreferenced files), so this list covers what it can't judge.

Contents: 1. Routing · 2. Knowledge delta · 3. Structure · 4. Instructions · 5. Form matches the failure · 6. Scripts · 7. Evals · 8. Across skills · Severity · Often fine

## 1. Routing

Find out first how the skill is invoked, because it decides what the description is for.

**Model-invocable skills** (no `disable-model-invocation: true`). The description is the only text the agent sees when choosing a skill, so it decides whether the skill ever runs.

- It says what the skill does and when to use it, key use case first, in the words users actually type: symptoms, file types, error text, the phrases people use for the task. A description in the author's vocabulary misses requests in the user's, and agents shorten long skill lists by cutting descriptions from the end.
- One trigger per distinct case. Synonyms for the same case are one case written twice: collapse them and spend the characters on cases that are actually different.
- It doesn't summarize the workflow. An agent that reads a summary of the steps tends to follow the summary instead of loading the skill.
- Sibling skills that compete for the same words each claim their own words and exclude the other's, on both sides.
- No exclusion blocks a case the skill exists for. Read each "not for" clause against the skill's own workflow.
- Near the length limit, drop text that repeats the body before you drop triggers.

**Manual-only skills** (`disable-model-invocation: true`, and `allow_implicit_invocation: false` in `agents/openai.yaml` for Codex). The agent never sees the description, so it only has to tell a person scanning a menu what the skill does. Trigger lists here cost nothing at runtime, but they're text to maintain; follow the house rules on whether to keep them.

**The invocation choice itself.** A skill should be model-invocable only when the agent needs to reach it on its own or another skill calls it, because every model-invocable description sits in context on every turn. A skill that another skill calls has to stay model-invocable, since the manual-only setting also stops one skill from calling another. Claude Code and Codex should agree; the checker flags a mismatch.

## 2. Knowledge delta

A skill is worth what it adds to what the model already does. Test every paragraph: would the model do this without being told? If so, it's a no-op that spends context and dilutes the lines that matter. Delete the whole sentence rather than trimming it.

- Typical no-ops: definitions of standard terms, tutorials for common tools, generic advice ("handle errors", "be thorough", "write clean code").
- Restating the environment (`package.json` scripts, config values, `--help` output) is a cache that goes stale. Keep what can't be looked up: unwritten conventions, the reason behind a choice, the gotcha nothing documents.
- One meaning, one place. A rule stated twice gets edited in one place and goes out of date in the other.
- Wrong facts are the most damaging defect a skill can have, because the agent trusts them. Check load-bearing commands, flags, API names, versions and URLs against the tool (`--help`, the docs) when you can, and say which ones you couldn't check.

## 3. Structure

- SKILL.md holds what every run needs. Material only some runs need goes in `references/`, behind a pointer at the point of need that names its condition: "Before filing, read the issue template in references." A list of references at the bottom, with no condition, is a pointer that rarely fires. Split a long SKILL.md the same way: by branch, or by sequence.
- Rules about one concept sit together under one heading. Scattered rules get applied piecemeal.
- Another skill is called by name, never by path, since skills get copied or symlinked on their own.

## 4. Instructions

- Each step ends on a checkable completion criterion. "Every changed model accounted for" gets thorough work; "understand the models" invites stopping early.
- The final output has a contract: its parts, in order. Scale it to the input: a full report template on a small input loses to a direct answer.
- Steps that fail in practice (tool missing, command errors, empty result) say what to do instead.
- There's a stop condition, including the no-op case: input that's already right is left alone, and the skill says so. Check that the fix doesn't over-correct into answering less than the model would unaided.
- Non-obvious rules carry their reason. A rule with its why generalizes to cases the author didn't list; a bare MUST gets negotiated away or over-applied.
- Inputs are marked required only when a person has to supply them. Anything the agent can find, it should be told to find.
- Reporting is honest about what ran: "didn't run", "failed" and "passed" are different results, and success claims cite the run.
- Freedom matches fragility. Fragile or exact operations get a script or an exact command; judgment calls get principles. A rule a script could enforce belongs in a script.
- Outward-facing or hard-to-reverse actions (publishing, sending, pushing, deleting) wait for the user's confirmation.

## 5. Form matches the failure

Before recommending wording, name the failure it fixes. The form that fixes one kind of failure makes another worse.

| Failure | Fix with | Not with |
| --- | --- | --- |
| The agent skips a rule it knows, under pressure (time, sunk cost, "just this once") | A hard rule, its reason, and the specific excuses it must not accept | Soft guidance ("prefer", "consider") |
| The output has the wrong shape (bloated, buried verdict, restated input) | A positive recipe: what the output is, its parts in order | A list of prohibitions |
| The output leaves out a required element | A required slot in the template the agent fills in | A reminder in nearby prose |
| The right behavior depends on a condition | A conditional on something observable ("if the repo has a CHANGELOG, ...") | A rule plus exemption clauses |

Naming a banned behavior makes it more available, so state the target behavior instead. A prohibition earns its place as a hard guardrail that can't be phrased positively, and even then it goes next to the positive target. "Don't X unless it matters" reopens the negotiation; write the exception as its own conditional. A skill with no list of anti-patterns isn't defective for that alone.

## 6. Scripts

- Invoked through its interpreter (`python scripts/x.py`), not by bare path. Packaging can strip the executable bit.
- Changes nothing unless the skill says it does.

## 7. Evals

When the skill has eval cases:

- Each prompt invokes the skill the way a user would. For a manual-only skill that means starting with `/<name>`, since the agent won't pick it up from plain English.
- Graders check what the skill promises, including its output shape and its no-op case.
- A case the model would pass without the skill tests nothing. Say so if you can tell.

## 8. Across skills

When reviewing several skills together:

- Two skills that fire on the same words or do the same job: merge them, or partition them with the real distinction and exclusions on both sides.
- A skill that repeats AGENTS.md or CLAUDE.md: keep the content in one place.
- Retirement is a valid verdict for a skill nothing calls, the user doesn't use, or whose job the model does as well unaided. Polishing it forever costs more.
- Files the house rules say must stay identical: diff them. For twin SKILL.md files, check they differ only where the rules allow.
- Names in cross-references match the skills that actually exist.

## Severity

- **High:** the skill misfires (doesn't trigger, or triggers on the wrong tasks), states a wrong fact or command, links to a missing file its workflow needs, or takes an outward-facing action without confirmation.
- **Medium:** a step the agent is likely to skip or misread, no failure path on a common step, no output contract, or a section of more than ~30 lines the model already knows.
- **Low:** wording, small duplication, organization.

## Often fine

Raise these only with a concrete cost. Otherwise they go on the "looks odd but is fine" list:

- A long SKILL.md where every line is needed on every run.
- No anti-pattern list.
- MUST or "never" on a hard guardrail that carries its reason.
- A trigger list on a manual-only skill, when the house rules ask for one.
- A description near the length limit where every phrase is a distinct trigger.
- A file not linked from SKILL.md that's meant for people (credits, notices, source notes).
- A backticked path that names a file in the user's project, not the skill's folder.
- A placeholder link inside a template or example.
