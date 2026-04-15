# Install

This repository is the source of truth for the consolidated Codex enhancement stack.

## One-command bootstrap

From a fresh clone:

```bash
./scripts/bootstrap.sh
```

That installs the `method-forge` skills into `"$CODEX_HOME/skills"` by symlink, so the local Codex App can discover them.

## Recommended flow for teammates

1. Clone the repository.
2. Run `./scripts/bootstrap.sh`.
3. Open the repository root as a Codex workspace.
4. When the repo changes, pull the latest revision and re-run the bootstrap script.

## Notes

- The repository keeps the three subsystems together under:
  - `knowledge-base/`
  - `memory-system/`
  - `method-forge/`
- The bootstrap script only installs skills. It does not overwrite existing Codex memory data.
- If you want the global memory system refreshed for a workspace, use the memory-system refresh workflow in `memory-system/`.

