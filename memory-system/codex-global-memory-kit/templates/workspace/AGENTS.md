# Workspace Memory Bridge

- This workspace uses the app-wide Codex memory system under `~/.codex/memory`.
- Before substantial work, read:
  - `~/.codex/memory/instructions/company/GUIDE.md`
  - `~/.codex/memory/instructions/user/GUIDE.md`
  - `~/.codex/memory/instructions/local/GUIDE.md`
- If this workspace already has a registered node under `~/.codex/memory/workspaces/`, also read its:
  - `instructions/repo/GUIDE.md`
  - `memories/MEMORY.md`
  - `runtime/active_context.md`
- After meaningful work, refresh memory with:
  - `python3 ~/.codex/scripts/refresh_memory.py --workspace-root "__WORKSPACE_ROOT__"`
- Do not create or maintain a second local memory system in this workspace unless the user explicitly asks for one.
