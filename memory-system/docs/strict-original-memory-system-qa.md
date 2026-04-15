# Strict-Original Memory System QA

This QA log was extracted from the original `对话` workspace during the workspace split.
Historical entries may reference `<legacy-worker-root>` because that was the original execution root before the memory-system workspace was separated.

## Test Matrix

- Automated unit tests for scaffolding, parsing, memory generation, index generation, compression output, and dream triggering
- Real workspace refresh run after migration
- Reference scan to confirm old `state/memory/` entrypoints and `CLAUDE.md` naming are gone from active workspace docs

## Expected Result

- Workspace docs point to `~/.codex/memory/` and workspace-scoped nodes under `workspaces/<workspace-key>/`
- The refresh command is `python3 ~/.codex/scripts/refresh_memory.py --workspace-root <legacy-worker-root>`
- The retired `state/memory/` tree and older workspace-local memory roots are not used by active docs
- The global memory runtime context rebuild succeeds after migration

## QA Notes

- Runtime summaries intentionally remain heuristic and may still surface historical statements from prior sessions.
- That remaining noise is a content-quality issue, not a migration-integrity failure.

## Executed Results

- `2026-04-02` ran `python3 -m unittest <legacy-worker-root>/tests/test_refresh_strict_original_memory.py`
- Result: `Ran 2 tests ... OK`
- `2026-04-02` ran `python3 <legacy-worker-root>/scripts/refresh_strict_original_memory.py --workspace-root <legacy-worker-root> --force --force-dream`
- Result summary:
  - `matching_sessions: 5`
  - `processed: 5`
  - `updated_memories: 23`
  - `index_lines: 36`
  - `dream.ran: true`
  - `dream.report_path: <legacy-worker-root>/state/strict_original_memory/dream/reports/20260402T155944Z.md`
- Verified that these retired artifacts are absent:
  - `state/memory/`
  - `scripts/refresh_codex_memory.py`
  - `codex-memory-kit/`
  - `codex-memory-kit.zip`

## Executed Results: High-Yield Fix Round

- `2026-04-03` updated code and docs for:
  - candidate staging before promotion
  - question filtering for `project` and `reference`
  - assistant-summary-based reference extraction
  - content-hash identity keys
  - task-scoped feedback demotion
- `2026-04-03` ran `python3 -m unittest <legacy-worker-root>/tests/test_refresh_strict_original_memory.py`
- Result: `Ran 4 tests ... OK`
- `2026-04-03` rebuilt generated memory artifacts from scratch and ran:
  - `python3 <legacy-worker-root>/scripts/refresh_strict_original_memory.py --workspace-root <legacy-worker-root> --force --force-dream`
- Result summary after final rebuild:
  - `matching_sessions: 5`
  - `processed: 5`
  - `candidate_created: 50`
  - `created_memories: 15`
  - `index_lines: 28`
  - `dream.ran: true`
  - `dream.report_path: <legacy-worker-root>/state/strict_original_memory/dream/reports/20260402T232244Z.md`
- Manual QA spot-checks confirmed:
  - no active `project` memories remain from question-like prompts
  - task-scoped instructions such as the “我要睡觉了...” run command are staged in `candidates/`, not active long-term memory
  - active feedback is now limited to durable defaults
  - non-ASCII title collisions no longer overwrite each other

## Executed Results: Second Alignment Round

- `2026-04-03` added:
  - per-source cap for active reference promotion
  - stricter reference meta exclusions
  - runtime focus window for active compression
  - test coverage for promotion caps and focus-window compression
- `2026-04-03` ran `python3 -m unittest <legacy-worker-root>/tests/test_refresh_strict_original_memory.py`
- Result: `Ran 6 tests ... OK`
- `2026-04-03` rebuilt generated memory artifacts from scratch and ran:
  - `python3 <legacy-worker-root>/scripts/refresh_strict_original_memory.py --workspace-root <legacy-worker-root> --force --force-dream`
- Final rebuild summary:
  - `matching_sessions: 5`
  - `processed: 5`
  - `candidate_created: 48`
  - `created_memories: 10`
  - `index_lines: 23`
  - `dream.ran: true`
  - `dream.report_path: <legacy-worker-root>/state/strict_original_memory/dream/reports/20260402T232807Z.md`
- Manual QA spot-checks confirmed:
  - active long-term memory now contains only `feedback`, `user`, and a small capped set of `reference` memories
  - `active_context.md` reflects the current task and current file set more cleanly than earlier versions
  - no new must-fix architectural drift was found against the article-aligned target

## Executed Results: Globalization And Naming Cleanup

- `2026-04-03` updated the implementation to:
  - use `~/.codex/memory/` as the global memory root
  - create workspace-scoped nodes under `workspaces/<workspace-key>/`
  - replace internal `CLAUDE.md` instruction naming with `GUIDE.md`
  - add the global runtime entrypoint `~/.codex/scripts/refresh_memory.py`
- `2026-04-03` ran `python3 -m unittest <legacy-worker-root>/tests/test_refresh_strict_original_memory.py`
- Result: `Ran 6 tests ... OK`
- `2026-04-03` ran:
  - `python3 ~/.codex/scripts/refresh_memory.py --workspace-root <legacy-worker-root> --memory-home ~/.codex/memory --force --force-dream`
- Result summary:
  - `workspace_memory_home: ~/.codex/memory/workspaces/workspace-<workspace-key>`
  - `matching_sessions: 3`
  - `processed: 3`
  - `candidate_created: 39`
  - `created_memories: 5`
  - `index_lines: 15`
  - `dream.ran: true`
  - `dream.report_path: ~/.codex/memory/workspaces/workspace-<workspace-key>/dream/reports/20260402T235444Z.md`
- Manual QA spot-checks confirmed:
  - new shared guides now live under `~/.codex/memory/instructions/`
  - the current workspace is indexed in `~/.codex/memory/workspaces/index.json`
  - the current workspace repo guide lives at `~/.codex/memory/workspaces/workspace-<workspace-key>/instructions/repo/GUIDE.md`
  - active workspace docs now point at the global memory system instead of `state/strict_original_memory/`
- `2026-04-03` also ran the default-path smoke test:
  - `python3 ~/.codex/scripts/refresh_memory.py --workspace-root <legacy-worker-root> --force`
- Smoke-test summary:
  - `memory_home: ~/.codex/memory`
  - `workspace_memory_home: ~/.codex/memory/workspaces/workspace-<workspace-key>`
  - `processed: 3`
  - `dream.ran: false`
- Final spot-check:
  - no active `CLAUDE.md` files remain under `<legacy-worker-root>`
