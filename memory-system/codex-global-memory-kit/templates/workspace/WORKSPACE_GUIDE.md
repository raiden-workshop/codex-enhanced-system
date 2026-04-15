# Workspace Guide

This workspace is connected to the Codex App global memory system.

Conventions:

- Global memory root is `~/.codex/memory/`
- The workspace memory node will be created under `~/.codex/memory/workspaces/` on first refresh
- Before complex work, read shared guides first, then the workspace memory node if it already exists
- After meaningful work, run:
  - `python3 ~/.codex/scripts/refresh_memory.py --workspace-root "__WORKSPACE_ROOT__"`
