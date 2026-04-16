# Install

This repository is the source of truth for `memory-system` and `method-forge`.
The knowledge base now lives in the standalone repo at `/Users/wz/project/knowledge-base`.

## One-command bootstrap

From a fresh clone:

```bash
./scripts/bootstrap.sh
```

That installs the `method-forge` skills into `"$CODEX_HOME/skills"` by symlink, so the local Codex App can discover them.

If you see older or external Codex docs mention `$HOME/.agents/skills`, treat that as a legacy or alternate naming surface. In this repository and the current local Codex App runtime, prefer `~/.codex/skills/` or `"$CODEX_HOME/skills"`.

## Recommended flow for teammates

1. Clone the repository.
2. Run `./scripts/bootstrap.sh`.
3. Open the repository root as a Codex workspace.
4. When the repo changes, pull the latest revision and re-run the bootstrap script.

## Notes

- The repository now keeps these local subsystems together:
  - `memory-system/`
  - `method-forge/`
- Knowledge-base runtime, docs, and CLI entry have moved to `/Users/wz/project/knowledge-base`
- The bootstrap script only installs skills. It does not overwrite existing Codex memory data.
- Keep the shared coding principles aligned across the stack: think before coding, simplicity first, surgical changes, and goal-driven verification.
- If you want the global memory system refreshed for a workspace, use the memory-system refresh workflow in `memory-system/`.
