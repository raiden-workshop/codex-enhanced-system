# Codex Enhanced System

This repository consolidates the three Codex support systems into one place:

- `knowledge-base` has been split out to the standalone repo at `/Users/wz/project/knowledge-base`
- `memory-system/` for global memory refresh and governance
- `method-forge/` for implementation workflows, orchestration, and autonomous execution

The intended priority order is:

1. Codex App native behavior and built-in automation boundaries
2. This repository's root guidance
3. The subworkspace guidance inside each system

Keep the shared coding principles aligned across the guides and templates: think before coding, simplicity first, surgical changes, and goal-driven verification.

Use the subdirectory that matches the task. If a task spans systems, keep the work in this repo and follow the narrowest applicable instructions first. If the task is about the knowledge base itself, switch to `/Users/wz/project/knowledge-base`; it is no longer a live subdirectory workflow inside this repo.

## Native-first compatibility map

This repository is a method and governance layer on top of Codex App, not a second implementation of Codex App itself.

When native Codex capabilities overlap with local workflows, treat Codex App as the source of truth and let this repository fill only the missing method layer.

### Codex App native owns

- multi-agent and subagent execution
- worktree isolation
- diff review, built-in Git actions, commit/push/PR flows
- automations, including thread automations and heartbeat-style wakeups
- plugin installation, app integrations, MCP distribution, and skill loading
- Computer Use
- built-in image generation
- native memories under `~/.codex/memories/`

### `codex-enhanced-system` owns

- `method-forge` request intake, `spec -> plan -> tasks -> verify`, and explicit quality gates
- `method-forge` autonomous run-state, resume rules, and loop guards on top of native automations
- `memory-system` governance, refresh, scope separation, and promotion rules for `~/.codex/memory/`
- repo-local and user-local skills that encode reusable workflows more explicitly than the native surface

### Memory boundary

- Keep mandatory repo and team rules in `AGENTS.md` or checked-in docs.
- Treat `~/.codex/memory/` as the governed long-term memory layer managed by this repository's memory system.
- Treat native memories in `~/.codex/memories/` as the default owner for personal preferences, common corrections, and convenience recall.
- Keep `~/.codex/memory/` focused on governed project facts, reusable references, open loops, and promotion/audit flow.
- When native memories are enabled, disable `memory-system` `user` and `feedback` capture to avoid duplicate recording.
- Do not duplicate the same repo rule or project fact across both memory systems unless you are intentionally maintaining a compatibility bridge.

## Install

Start here: [INSTALL.md](INSTALL.md)

The one-command bootstrap installs the `method-forge` skills into `"$CODEX_HOME/skills"` without touching existing Codex memory data.
