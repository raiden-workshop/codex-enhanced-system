# Strict-Original Memory System Design

## 1. Goal

This document defines the canonical memory system used by this Codex App environment. It strictly imitates the model described in the article about Claude Code's memory architecture, but renames internal instruction files to `GUIDE.md` to fit the Codex context.

The design goals are:

- keep instruction loading layered
- keep long-term memory human-readable and file-based
- record both corrections and confirmations
- preserve task continuity through graded compression
- run a periodic "dream" pass that repairs drift instead of only appending

This design intentionally stays close to the article's model and does not introduce a multi-writer shared-memory protocol. It replaces the older `state/memory/` shared-memory variant with one global memory root under `~/.codex/memory/`, plus workspace-scoped nodes under `workspaces/<workspace-key>/`.

## 2. Core Model

The system has four instruction layers, four long-term memory types, three compression levels, and one dream maintenance loop.

This revision also introduces a staging layer so extracted observations do not land in long-term memory immediately.

### 2.1 Instruction Layers

Instruction files load in this order:

1. company
2. user
3. repo
4. local

Conflict priority is the reverse of load order:

1. local
2. repo
3. user
4. company

This preserves the article's idea that instructions closer to the current execution context win.

### 2.2 Memory Types

The system stores four memory classes:

1. user memory
2. feedback memory
3. project memory
4. reference memory

Each memory is stored as its own Markdown file.

### 2.3 Compression

Compression is graded:

1. micro compression
2. automatic compression
3. full compression

Compression begins when working context approaches:

- `context_window_tokens - 13000 reserve_tokens`

### 2.4 Dream

Dream is a reflective maintenance pass over the memory files.

Dream runs when:

- at least 24 hours have passed since the last dream
- and at least 5 work sessions happened since the last dream

Dream stages:

1. orientation
2. collection
3. integration
4. pruning

## 3. Filesystem Layout

```text
~/.codex/memory/
  instructions/
  instructions/
    company/GUIDE.md
    user/GUIDE.md
    local/GUIDE.md
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
      memories/
        user/
        feedback/
        project/
        reference/
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
```

## 4. Memory File Rules

Every long-term memory entry is a standalone Markdown file with frontmatter and a short body.

Required metadata:

- `id`
- `key`
- `type`
- `created_at`
- `last_confirmed_at`
- `status`

Optional metadata:

- `source`
- `tags`
- `scope`

Allowed statuses:

- `candidate`
- `active`
- `stale`
- `superseded`
- `archived`

## 5. Type-Specific Schemas

### 5.1 User Memory

Purpose:

- stable user facts
- stable long-term preferences
- cross-task durable working habits

Body sections:

- `Fact`
- `Why it matters`
- `How to use`
- `Evidence`

### 5.2 Feedback Memory

Purpose:

- record corrections
- record confirmations

Body sections:

- `Rule`
- `Why`
- `How to apply`
- `Evidence`

This is the strictest schema because the article emphasizes it most.

### 5.3 Project Memory

Purpose:

- durable repo-level truths
- recurring project constraints
- project conventions that survive across sessions

Body sections:

- `Project fact`
- `Why it matters`
- `When relevant`
- `Evidence`

### 5.4 Reference Memory

Purpose:

- reusable conclusions derived from external materials
- not full copies of source content

Body sections:

- `Reference takeaway`
- `Why it matters`
- `How to reuse`
- `Source`

## 6. Index Rules

`memories/MEMORY.md` is an index, not a warehouse.

Rules:

- maximum 200 lines
- each entry should stay within 150 characters when possible
- entries point to actual memory files
- old, duplicate, or stale entries are pruned during dream

The index should stay skimmable and short.

## 7. Write Policy

The system should follow these rules when material becomes memory:

- extracted observations are written to `candidates/` first
- only high-confidence durable items are promoted into `memories/`
- prefer updating an existing memory over creating a duplicate
- store both negative and positive feedback
- convert relative time expressions into absolute dates
- do not store one-off noise as long-term memory
- keep memory text short and human-editable
- if new information invalidates an old memory, correct the old memory instead of keeping both active
- use a content-derived identity key instead of a title slug as the canonical dedupe key

Promotion guardrails:

- project memories must be declarative facts, not open questions
- reference memories must capture conclusions from analysis output, not merely the user's request to read a source
- task-scoped instructions must stay in candidates instead of being promoted as durable feedback
- reference promotion should prefer the top few reusable takeaways per source, not every analysis sentence in a source-related session
- runtime compressed context should bias toward the current task focus window rather than aggregating all recent sessions equally

## 8. Compression Requirements

All compression levels must preserve:

- current task goal
- user critical quotes when task is still active
- files changed
- errors encountered
- confirmed feedback
- remaining work

### 8.1 Micro Compression

Use when context is near the line but still manageable.

Behavior:

- drop greetings and low-signal turns
- remove duplicates
- keep conversation structure mostly intact

### 8.2 Automatic Compression

Use when context pressure is meaningful.

Behavior:

- collapse repeated turns into theme-based sections
- keep execution-critical facts only
- preserve strong continuity

### 8.3 Full Compression

Use when context is close to exhaustion.

Behavior:

- rebuild a fresh working context
- keep only the execution skeleton
- preserve exact user wording when precision matters

## 9. Dream Responsibilities

Dream must:

- read the layered instructions
- read the memory index
- inspect recent memory updates
- inspect recent session-derived context
- collect durable new information
- detect duplicated or drifted memories
- normalize dates into absolute time
- update the index
- prune stale or redundant entries

Dream should not behave like a blind append-only batch.

## 10. Non-Goals

This strict-original design does not include:

- a vector database-first architecture
- a multi-worker concurrent write protocol
- automatic trust of every session detail
- role-specific planner or executor memory views

Those can be added later, but they are outside the strict imitation target.
