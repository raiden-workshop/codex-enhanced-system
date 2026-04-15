# Memory Scope Design

## 1. Scope Model

The memory system uses three scopes and one archive layer:

1. `global`
2. `workspace`
3. `worker-run`
4. `raw archive`

In this Codex App environment:

- `global` means the whole Codex App
- `workspace` means one project root
- `worker-run` means one thread or one concrete execution run inside a workspace

Examples:

- `对话` and `Return Management` are two different workspaces
- three threads under `对话` are three different `worker-run`s

## 2. Responsibility Split

### 2.1 Global

Global stores only cross-workspace durable memory.

Examples:

- long-term user preferences
- cross-project default workflows
- globally confirmed feedback
- reusable reference conclusions that are not project-specific

### 2.2 Workspace

Workspace stores project-level durable memory.

Examples:

- project facts
- repo-level conventions
- project-specific feedback
- project-specific references
- open loops that matter to this project

### 2.3 Worker-Run

Worker-run stores temporary execution state only.

Examples:

- current goal
- current task plan
- temporary hypotheses
- local debugging notes
- handoff notes
- unconfirmed observations

Worker-run is not a long-term truth layer.

## 3. Promotion Rules

### 3.1 Worker-Run -> Workspace

Promote when an item is:

- explicitly stated by the user
- useful beyond the current thread
- likely to matter again in the same project
- a stable project fact or project rule
- not a one-off task instruction

### 3.2 Workspace -> Global

Promote only when an item is:

- clearly cross-project
- explicitly requested as a global default
- repeated and confirmed across multiple workspaces
- independent from repo-specific context

Default rule:

- do not promote directly from `worker-run` to `global`
- promote to `workspace` first
- promote to `global` only after stronger evidence

## 4. Demotion Rules

### 4.1 Global -> Workspace

Demote when a supposedly global rule turns out to be only a project-specific convention.

### 4.2 Workspace -> Candidate

Demote when an active workspace memory no longer looks stable enough.

### 4.3 Workspace or Global -> Stale

Mark stale when the memory is outdated, contradicted, or no longer useful.

### 4.4 Worker-Run -> Archive

Archive worker-run material when the task is done or no longer active.

## 5. Read Order

Workers should read memory in this order:

1. `worker-run`
2. `workspace`
3. `global`

This means:

- current-task temporary context wins first
- project rules override global defaults
- global defaults fill in when nothing closer applies

## 6. Storage Principle

Formal long-term memory should live only in:

- `global`
- `workspace`

`worker-run` should remain temporary by design.

This avoids giving every thread its own permanent long-term memory silo.

## 7. Dream Split

### 7.1 Workspace Dream

Workspace dream should:

- merge workspace candidates
- demote unstable workspace memories
- prune stale workspace items
- rebuild workspace `MEMORY.md`
- rebuild workspace runtime context

### 7.2 Global Dream

Global dream should:

- detect repeated durable patterns across workspaces
- decide what deserves global promotion
- clean global drift
- keep global memory small and high-confidence

## 8. Core Rule

The core rule is:

- `worker-run` produces observations
- `workspace` stores project truth
- `global` stores cross-project truth
