# Autonomous Heartbeat Prompt

Keep each cycle focused on the smallest safe next step, and stop only when the task is actually blocked, completed, or waiting on a human.

Use this prompt only when a Codex native heartbeat automation has been explicitly requested or an existing autonomous run is being resumed for a `method-forge` task.

```text
You are continuing an active autonomous task in <workspace>.

Default engine:
- Always use `method-forge-execute` as the inner workflow engine unless `runtime/run-state.md` says the task is `completed`, `blocked`, or `waiting-human`.

At the start of each cycle:
1. Read `docs/specs/<change-id>/runtime/run-state.md`.
2. Read `docs/specs/<change-id>/package-index.md`.
3. Read the current phase document referenced by `current_step` or `next_action`.
4. Enforce `loop-guard-rules.md` before doing any new work.

Execution rules:
- Continue automatically when the task is still safely actionable.
- Do not ask the user to restate "use method-forge" again.
- Use `method-forge-execute` to normalize rough inputs, continue the correct workflow phase, and complete implementation/verify when context is sufficient.
- Do not stop just because one micro-slice passed `verify`; if the next safe slice inside the same user goal is already known, keep the run `running` and continue on the next cycle.
- If progress is made, update `run-state.md`, `package-index.md`, and write a new cycle report under `runtime/reports/`.
- If no safe progress can be made, set status to `blocked`, `waiting-human`, or `waiting-external` with a concrete `stop_reason`.
- Set status to `completed` only when the top-level task is actually finished, not when a single sub-slice happens to complete.

Loop guard:
- Max step retries: 3
- Max same error repeats: 2
- Max no-progress cycles: 2
- Max total cycles per task: 12

Never:
- Bypass `verify`
- Directly write long-term memory
- Rebuild a second automation platform
- Ignore repeated identical errors and keep retrying
```
