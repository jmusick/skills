# AGENTS.md

Agent skills for the harbor office, one folder per skill under `skills/`.

- Skills run only when someone invokes them: `disable-model-invocation: true` in the frontmatter, plus `agents/openai.yaml` turning off implicit invocation for Codex. A manual-only skill's description is one sentence saying what it does, since no agent reads it.
- The exception is tide-report: buoy-alert calls it, so it stays model-invocable.
- A skill calls another by name, never by path.
