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

Use the subdirectory that matches the task. If the task is about the knowledge base itself, switch to `/Users/wz/project/knowledge-base`; it is no longer a live subdirectory workflow inside this repo.

## Install

Start here: [INSTALL.md](INSTALL.md)

The one-command bootstrap installs the `method-forge` skills into `"$CODEX_HOME/skills"` without touching existing Codex memory data.
