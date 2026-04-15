# Codex Global Memory System Design

## 1. Goal

This document defines the final target design for the Codex App global memory system.

The system must satisfy four goals:

- keep long-term memory file-based, inspectable, and editable
- make new workers start with the right shared context by default
- separate temporary thread state from project truth and global truth
- promote only durable, reusable memory into long-term layers

This design is intentionally close to the article-inspired model that shaped the current system, but it is adapted to Codex App terminology and runtime reality.

## 2. Scope Model

The system uses three scopes and one archive layer:

1. `global`
2. `workspace`
3. `worker-run`
4. `archive`

In this environment:

- `global` means the whole Codex App installation
- `workspace` means one project root
- `worker-run` means one thread or one concrete execution run inside a workspace
- `archive` means retained history that is not part of the hot path

Examples:

- `<legacy-worker-root>` and `<another-workspace-root>` are two different workspaces
- three active threads inside `对话` are three different `worker-run`s

## 3. Scope Responsibilities

### 3.1 Global

Global stores only cross-workspace durable memory.

Allowed memory types:

- `user`
- `feedback`
- `reference`

Examples:

- durable user defaults
- globally confirmed workflow preferences
- reusable conclusions that are not tied to one repo

Global must stay small, stable, and high-confidence.

### 3.2 Workspace

Workspace stores project-level durable memory.

Allowed memory types:

- `feedback`
- `project`
- `reference`
- `open_loop`

Examples:

- repo-specific conventions
- project facts
- project-scoped feedback
- current project open loops

Workspace is the main truth layer for project collaboration.

### 3.3 Worker-Run

Worker-run stores temporary execution state only.

Allowed data:

- current goal
- current plan
- scratch notes
- handoff notes
- temporary hypotheses
- extracted observations awaiting review

Worker-run is not a formal long-term truth layer.

### 3.4 Archive

Archive stores:

- raw sessions
- old compression outputs
- stale or superseded memories
- finished run artifacts

Archive is for traceability, not for default loading.

## 4. Precedence

Read precedence is:

1. `worker-run`
2. `workspace`
3. `global`

This means:

- current-task temporary context wins first
- project rules override global defaults
- global defaults fill gaps when nothing closer applies

## 5. Long-Term Memory Rules

Formal long-term memory may live only in:

- `global`
- `workspace`

Hard rules:

- `worker-run` never writes directly to long-term active memory
- `project` never promotes to `global`
- `open_loop` never promotes to `global`
- no item may go directly from `worker-run` to `global`

## 6. Filesystem Layout

```text
~/.codex/memory/
  README.md

  instructions/
    company/GUIDE.md
    user/GUIDE.md
    local/GUIDE.md

  global/
    candidates/
      user/
      feedback/
      reference/
    candidates_archive/
      user/
      feedback/
      reference/
    memories/
      user/
      feedback/
      reference/
      MEMORY.md
    runtime/
      global_context.md
    conflicts/
      open/
      resolved/
      archived/
    dream/
      state.json
      reports/
    config.json
    registry.json

  workspaces/
    index.json
    <workspace-key>/
      instructions/
        repo/GUIDE.md
      candidates/
        user/
        feedback/
        project/
        reference/
        open_loop/
      memories/
        feedback/
        project/
        reference/
        open_loop/
        MEMORY.md
      runtime/
        active_context.md
        compression/
          latest.md
          archive/
      dream/
        state.json
        reports/
      config.json
      registry.json

  runs/
    <workspace-key>/
      <run-id>/
        status.json
        summary.md
        scratch.md
        handoff.md
        extracted.json
        archived_at.txt
```

## 7. Memory Object Model

All long-term memory entries use one common metadata shape.

Required fields:

- `id`
- `key`
- `scope`
- `type`
- `status`
- `confidence`
- `created_at`
- `last_confirmed_at`
- `source_runs`
- `source_workspaces`

Optional fields:

- `supersedes`
- `source`
- `tags`

Allowed statuses:

- `candidate`
- `active`
- `stale`
- `superseded`
- `archived`

Historical backfill rules:

- legacy workspace files missing `source_workspaces` must be backfilled conservatively so copied history does not become fake cross-workspace evidence
- legacy files missing `source_runs` must receive a stable run-like identifier from existing file metadata

## 8. Memory Types

### 8.1 User

Purpose:

- stable user identity and cross-project preferences

Active scope:

- `global` only

### 8.2 Feedback

Purpose:

- durable rules derived from corrections or confirmations

Active scope:

- `workspace`
- `global`

### 8.3 Project

Purpose:

- stable project facts and repo conventions

Active scope:

- `workspace` only

### 8.4 Reference

Purpose:

- reusable conclusions from external materials

Active scope:

- `workspace`
- `global`

### 8.5 Open Loop

Purpose:

- unresolved project tasks worth carrying forward

Active scope:

- `workspace` only

## 9. Promotion And Demotion

### 9.1 Worker-Run To Workspace

Worker-run may produce observations that become `workspace candidates`.

Promotion conditions:

- explicitly stated by the user
- likely to matter again in the same project
- stable enough to survive beyond the current thread
- not a one-off task command

### 9.2 Workspace To Global

Workspace memory may become `global candidate` only when it is:

- clearly cross-project
- explicitly requested as a global default
- repeated across multiple workspaces
- independent from repo-specific structure

Candidate governance rules:

- items already promoted to `global active` should not remain in `global candidates`
- duplicate global candidates should be archived instead of accumulating
- expired or over-budget global candidates should move to `global/candidates_archive/`

### 9.3 Demotion

The system must support:

- `global -> workspace` when an item turns out to be project-specific
- `active -> candidate` when certainty drops
- `active -> stale` when the memory becomes outdated
- `stale -> archived` when the memory is no longer useful

## 10. Runtime Context

Workers should read memory in this order:

1. `instructions/company/GUIDE.md`
2. `instructions/user/GUIDE.md`
3. `instructions/local/GUIDE.md`
4. `global/runtime/global_context.md`
5. `workspaces/<workspace-key>/instructions/repo/GUIDE.md`
6. `workspaces/<workspace-key>/runtime/active_context.md`
7. `runs/<workspace-key>/<run-id>/handoff.md`

Hot-path budgets:

- `global_context.md`: 300 to 500 tokens
- `workspace MEMORY.md`: 300 to 600 tokens
- `workspace active_context.md`: 500 to 900 tokens
- `worker-run handoff.md`: 200 to 400 tokens

## 11. Compression Model

Compression stays graded:

1. `micro`
2. `automatic`
3. `full`

All compression outputs must preserve:

- current goal
- confirmed feedback
- files changed
- important errors and risks
- next-step entry point
- a small number of critical user quotes

## 12. Dream Model

The system has two dream loops.

### 12.1 Workspace Dream

Workspace dream:

- merges candidates
- removes question-shaped noise
- removes task-scoped rules from active memory
- promotes durable workspace candidates
- demotes stale workspace memories
- rebuilds workspace `MEMORY.md`
- rebuilds workspace `active_context.md`

### 12.2 Global Dream

Global dream:

- scans high-confidence workspace memory
- finds repeated cross-workspace patterns
- promotes only durable cross-project truth
- writes conflict items when scope or truth is unclear
- rebuilds global `MEMORY.md`
- rebuilds `global_context.md`

## 13. Conflict Queue

Global conflicts must not be resolved by silently keeping two active truths.

The conflict queue exists to hold:

- contradictory global candidates
- contradictions between `global candidate` and `global active`
- scope ambiguity between global truth and workspace-specific truth

Resolution modes:

- `promote_a`
- `promote_b`
- `scope_split`
- `reject_both`

Default safe choice:

- prefer `scope_split` over premature global unification

## 14. Core Invariants

The system must always preserve these invariants:

1. `worker-run` does not hold formal long-term truth
2. `workspace` is the primary truth layer for project work
3. `global` stores only cross-project durable truth
4. no direct `worker-run -> global` promotion
5. `project` and `open_loop` never become global
6. conflicts do not enter `global active` unresolved
7. only one active version of the same truth may exist
8. memory must remain readable, editable, and diffable
