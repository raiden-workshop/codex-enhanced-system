# Codex Global Memory System Alignment

This document keeps the design and development specifications aligned.

## 1. Scope Alignment

- Design defines three scopes: `global`, `workspace`, and `worker-run`, plus archive.
- Development must implement explicit storage for all three active scopes.
- Development must not collapse `worker-run` into long-term memory.

## 2. Responsibility Alignment

- Design says `worker-run` produces observations.
- Design says `workspace` stores project truth.
- Design says `global` stores cross-project truth.
- Development must preserve exactly that split.

## 3. Filesystem Alignment

- Design defines one global root under `~/.codex/memory/`.
- Development must implement:
  - shared guides under `instructions/`
  - workspace nodes under `workspaces/<workspace-key>/`
  - global node under `global/`
  - temporary run nodes under `runs/`

## 4. Type Alignment

- Design allows:
  - `user`, `feedback`, `reference` in `global`
  - `feedback`, `project`, `reference`, `open_loop` in `workspace`
- Development must enforce that `project` and `open_loop` never become global active memory.

## 5. Promotion Alignment

- Design forbids direct `worker-run -> global` promotion.
- Development must enforce staged flow:
  - `worker-run -> workspace candidate`
  - `workspace candidate -> workspace active`
  - `workspace active -> global candidate`
  - `global candidate -> global active`

## 6. Demotion Alignment

- Design requires demotion and archive paths.
- Development must implement:
  - `active -> stale`
  - `stale -> archived`
  - `global -> workspace` when scope was over-promoted

## 7. Runtime Alignment

- Design defines a fixed read order:
  1. shared guides
  2. global context
  3. workspace repo guide
  4. workspace active context
  5. worker handoff
- Development must keep runtime outputs small and hot-path oriented.

## 8. Compression Alignment

- Design keeps graded compression.
- Development must preserve:
  - current goal
  - feedback
  - files changed
  - errors and risks
  - next step
  - critical quotes

## 9. Dream Alignment

- Design defines both workspace dream and global dream.
- Development must implement both, not just workspace cleanup.

Workspace dream must:

- merge candidates
- promote durable workspace truth
- mark stale or superseded items
- rebuild workspace runtime files

Global dream must:

- cluster cross-workspace evidence
- create global candidates
- create conflict items when truth is unclear
- rebuild global runtime files
- archive promoted, duplicate, expired, and overflow global candidates
- migrate missing origin metadata before counting cross-workspace evidence

## 10. Conflict Alignment

- Design requires a conflict queue for unresolved global truth.
- Development must not write conflicting truths directly into `global active`.
- Development must support `scope_split` as a first-class resolution mode.

## 11. Safety Alignment

- Design requires file-based, human-readable memory.
- Development must keep every long-term item as a readable file.
- Development must not introduce opaque-only storage as the truth layer.

## 12. Delivery Alignment

The specs are aligned when all of these are true:

1. naming uses `GUIDE.md`, not `CLAUDE.md`
2. all three scopes exist in storage and in runtime behavior
3. runtime read order matches the design
4. promotion and demotion rules match the design
5. workspace dream and global dream both exist
6. conflict queue exists for unresolved global truth
7. legacy workspace memory can be backfilled with origin metadata
8. global candidate accumulation is bounded by archive governance
