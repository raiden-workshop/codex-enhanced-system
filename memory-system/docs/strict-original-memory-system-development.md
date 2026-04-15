# Strict-Original Memory System Development Spec

## 1. Implementation Scope

This spec defines the canonical implementation for the Codex App global memory system.

Implementation root:

- `~/.codex/memory/`
- workspace-scoped nodes under `~/.codex/memory/workspaces/<workspace-key>/`

Main scripts:

- development source: `scripts/refresh_strict_original_memory.py`
- global runtime entrypoint: `~/.codex/scripts/refresh_memory.py`

The implementation must be self-contained and safe to run repeatedly.

## 2. Responsibilities

The implementation must do the following:

1. scaffold the global memory directory structure
2. parse Codex Desktop session logs from `~/.codex/sessions/`
3. filter sessions that belong to the target workspace
4. extract candidate memories into the four article-aligned types
5. write staged observations into `candidates/`
6. promote only durable high-confidence items into `memories/`
7. regenerate `memories/MEMORY.md`
8. regenerate runtime compression outputs
9. maintain dream state and write dream reports when thresholds are met
10. keep a registry so repeat runs are incremental

## 3. CLI

Required flags:

- `--workspace-root`
- `--codex-home`
- `--force`
- `--limit`
- `--force-dream`
- `--memory-home`

Optional behavior:

- if omitted, `workspace-root` defaults to current working directory
- if omitted, `codex-home` defaults to `~/.codex`
- if omitted, `memory-home` defaults to `~/.codex/memory`

## 4. Config Schema

The script must create and merge a default config file at the workspace-scoped node:

- `~/.codex/memory/workspaces/<workspace-key>/config.json`

Default fields:

```json
{
  "version": 1,
  "context_window_tokens": 200000,
  "reserve_tokens": 13000,
  "index_max_lines": 200,
  "index_max_chars_per_entry": 150,
  "dream": {
    "min_hours_since_last": 24,
    "min_sessions_since_last": 5
  },
  "compression": {
    "quote_limit": 3,
    "recent_session_limit": 8
  },
  "promotion": {
    "feedback_min_confidence": 0.85,
    "project_min_confidence": 0.8,
    "reference_min_confidence": 0.8,
    "user_min_confidence": 0.85,
    "reference_max_promoted_per_source": 3
  },
  "runtime": {
    "focus_session_limit": 2
  }
}
```

## 5. Session Parsing

The parser may reuse the existing Codex session JSONL shape already observed in Codex Desktop session logs.

Expected flow:

1. load JSONL rows
2. read the session `cwd`
3. reject rows outside the target workspace
4. extract user turns and assistant turns
5. build a compact session record

Each parsed session should expose:

- session id
- started_at
- day
- workspace path
- user turns
- assistant turns
- summary
- extracted candidate memories

## 6. Extraction Heuristics

The prototype should use deterministic heuristics instead of black-box inference.

### 6.1 User Memory

Detect durable user facts and habits from phrases such as:

- `我常用`
- `我现在常用`
- `我是重度`
- `默认`
- `长期`

### 6.2 Feedback Memory

Detect both:

- correction signals
- confirmation signals

Correction examples:

- `不要`
- `别`
- `改成`
- `以后都`
- `优先`

Confirmation examples:

- `可以`
- `就这样`
- `先这样`
- `对`
- `没问题`

Additionally classify each feedback candidate as either:

- durable default guidance
- task-scoped instruction

Task-scoped instructions must remain in `candidates/` unless explicitly promoted later.

### 6.3 Project Memory

Detect workspace-level durable facts from:

- repo name
- current execution mode
- repeated project constraints
- persistent operational notes

Project candidates must be dropped if the source fragment is a question or request for advice rather than a fact.

### 6.4 Reference Memory

Detect reusable external references when a session includes:

- URLs
- article or documentation discussion
- explicit “参考/文章/文档” style language

The implementation should store conclusions from the assistant's analysis output, not the user's original request to inspect the source.

Only the top-scoring reusable conclusions per source should be promoted into active long-term memory.

## 7. Memory File Naming

Each memory file should use a stable filename derived from a content identity key:

- `<date>-<key>-<slug>.md`

The identity key must be computed from normalized semantic content, not from the title alone.

If a matching active memory already exists, update it instead of creating a duplicate.

## 8. MEMORY.md Generation

The index should be rebuilt from active memories.

Ordering:

1. feedback
2. project
3. user
4. reference

Then sort inside each type by recency descending.

Index entries must:

- fit within the character budget where possible
- include type
- include a short summary
- include a relative path to the source memory file

If the line budget is exceeded, keep the most recent active entries only.

## 9. Runtime Compression

Outputs:

- `runtime/active_context.md`
- `runtime/compression/latest.md`
- `runtime/compression/archive/*.md`

Compression should be built from recent session records and active feedback/project memories.

Selection rule:

1. estimate recent working-context tokens
2. compare with `context_window_tokens - reserve_tokens`
3. choose micro, automatic, or full compression
4. write a single normalized compressed-context file

Runtime context should prefer a small focus window of the most recent task-relevant sessions for:

- `Files Changed`
- `Errors Encountered`
- `Decisions Made`
- `Remaining Work`

Compressed output sections:

- `Current Goal`
- `Confirmed Feedback`
- `Files Changed`
- `Errors Encountered`
- `Decisions Made`
- `Remaining Work`
- `Important Quotes`

## 10. Dream Engine

Dream state file:

- `dream/state.json`

Dream report output:

- `dream/reports/<timestamp>.md`

The implementation should track:

- last dream time
- sessions processed since last dream
- last report path

When dream triggers:

1. scan all active memories
2. rebuild `MEMORY.md`
3. mark obvious duplicates or stale copies
4. normalize any remaining relative-date phrases when possible
5. demote obvious quality failures such as question-shaped project memories or task-scoped feedback that slipped into active storage
5. emit a report with:
   - created memories
   - updated memories
   - stale or superseded memories
   - index result

## 11. Safety Constraints

The implementation must not:

- modify `~/.codex/.codex-global-state.json`
- modify Codex sqlite databases
- remove user-authored files outside the global memory root unless they are explicitly deprecated migration leftovers such as the retired `state/memory/` system or older workspace-local memory caches

## 12. Test Plan

Automated tests should cover:

1. scaffolding a clean prototype root
2. parsing a minimal Codex session JSONL
3. writing candidates separately from active memories
4. rejecting question-shaped project/reference candidates
5. extracting reference takeaways from assistant analysis text
6. preventing title-slug collisions through content-based keys
7. building a bounded `MEMORY.md`
8. generating compressed runtime context
9. triggering dream after threshold conditions
10. preserving incremental behavior through the registry

QA should additionally run the script against the real workspace to verify:

- directories are created
- files are readable
- outputs are deterministic
- repeat runs do not explode duplicates
