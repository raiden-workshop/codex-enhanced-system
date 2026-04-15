# Codex Global Memory

This is the app-wide memory system for Codex.

- Shared guides live in `instructions/company/`, `instructions/user/`, and `instructions/local/`.
- Each workspace gets its own memory node under `workspaces/<workspace-key>/`.
- `workspaces/index.json` maps normalized workspace paths to workspace keys.
- Workspace nodes contain:
  - `instructions/repo/GUIDE.md`
  - `candidates/`
  - `memories/`
  - `runtime/`
  - `dream/`
  - `config.json`
  - `registry.json`
- `runs/` stores temporary worker-run artifacts.
- `global/` stores cross-workspace memory, conflict items, and global runtime context.
