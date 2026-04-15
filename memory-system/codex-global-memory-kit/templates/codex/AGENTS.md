# Global Codex Memory Guardrails

- Codex App uses one global memory system rooted at `~/.codex/memory`.
- Before substantial work, read the shared guides when they exist:
  - `~/.codex/memory/instructions/company/GUIDE.md`
  - `~/.codex/memory/instructions/user/GUIDE.md`
  - `~/.codex/memory/instructions/local/GUIDE.md`
- Then check `~/.codex/memory/workspaces/index.json` for the current workspace path.
- If the current workspace is registered, read its workspace-scoped files under the mapped directory:
  - `instructions/repo/GUIDE.md`
  - `memories/MEMORY.md`
  - `runtime/active_context.md`
- If the workspace is not registered yet, shared guides still apply; the first refresh will create its workspace-scoped memory node.
- Treat BuddyPulse, status boards, and raw logs as telemetry, not as long-term memory.
- After meaningful work, refresh the global memory system with:
  - `python3 ~/.codex/scripts/refresh_memory.py --workspace-root <current-workspace-root>`
- Only store stable, reusable, user-helpful facts in long-term memory. Keep guesses and one-off details out.
