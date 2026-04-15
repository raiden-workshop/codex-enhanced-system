# Codex Global Memory System Development Spec

## 1. Purpose

This spec describes how to implement the Codex global memory system defined in the design document.

It is an implementation-oriented contract, not a product pitch.

Primary references:

- design: `docs/codex-global-memory-system-design.md`
- alignment: `docs/codex-global-memory-system-alignment.md`

## 2. Canonical Roots

Global memory root:

- `~/.codex/memory/`

Global runtime entrypoint:

- `~/.codex/scripts/refresh_memory.py`

Current implementation source workspace:

- `<repo-root>/memory-system`

Current development source file:

- `scripts/refresh_strict_original_memory.py`

## 3. Implementation Phases

The implementation started as a phased plan, but the current runtime already ships the major capabilities from all three phases.

Use this section as a status map:

- `Phase 1`: shipped baseline
- `Phase 2`: shipped architecture
- `Phase 3`: shipped hardening baseline with room for future refinement

### Phase 1

Shipped baseline:

- one global root exists
- each workspace gets its own workspace node
- extraction is heuristic and file-based
- workspace memory and workspace runtime context are supported

### Phase 2

Shipped architecture:

- explicit `global/` root with candidates, memories, runtime, conflicts, and dream
- explicit `runs/` root for worker-run state
- promotion path from workspace to global
- conflict queue for unresolved global truth

### Phase 3

Current hardening baseline:

- stronger normalization for cross-workspace clustering
- better conflict scoring
- better runtime summarization
- stronger stale/archive lifecycle management
- historical metadata backfill for legacy memory files
- global candidate archive and overflow governance

## 4. Required Modules

The implementation must support these responsibilities.

### 4.1 Workspace Resolution

Responsibilities:

- normalize workspace paths
- compute `workspace-key`
- map workspace path to workspace node
- maintain `workspaces/index.json`

### 4.2 Session Ingestion

Responsibilities:

- scan `~/.codex/sessions/**/*.jsonl`
- parse session metadata and messages
- match sessions to the target workspace
- ignore low-signal sessions

### 4.3 Extraction

Responsibilities:

- extract `user`
- extract `feedback`
- extract `project`
- extract `reference`
- classify extracted data by scope candidacy

Rules:

- questions must not become active project or reference memory
- request-shaped source prompts must not become reference takeaways
- task-scoped instructions must not become durable active feedback

### 4.4 Worker-Run Materialization

Responsibilities:

- create a `run-id`
- persist `status.json`
- persist `summary.md`
- persist `scratch.md`
- persist `handoff.md`
- persist `extracted.json`

Worker-run material must be temporary by design.

### 4.5 Workspace Candidate And Active Memory

Responsibilities:

- write candidate memories under workspace scope
- promote durable workspace items into active memory
- keep file identity content-based
- preserve only one active truth per identity

### 4.6 Global Candidate And Active Memory

Responsibilities:

- scan workspace active and high-confidence candidates
- create global candidates
- promote only cross-workspace durable items into global active
- reject or defer uncertain items
- archive promoted, duplicate, expired, or overflow candidate files
- avoid counting copied workspace history as independent cross-workspace proof

### 4.7 Runtime Context

Responsibilities:

- rebuild `global_context.md`
- rebuild workspace `active_context.md`
- preserve bounded size
- keep runtime files readable and directly useful for workers

### 4.8 Dream

Responsibilities:

- workspace dream
- global dream
- stale detection
- supersede handling
- conflict creation and resolution-state tracking
- candidate archive governance
- legacy metadata migration before clustering

## 5. Required Files

### 5.1 Global Files

Must exist:

- `instructions/company/GUIDE.md`
- `instructions/user/GUIDE.md`
- `instructions/local/GUIDE.md`
- `global/config.json`
- `global/registry.json`
- `global/runtime/global_context.md`
- `global/dream/state.json`
- `global/candidates_archive/`
- `workspaces/index.json`

### 5.2 Workspace Files

For every workspace node:

- `instructions/repo/GUIDE.md`
- `config.json`
- `registry.json`
- `runtime/active_context.md`
- `dream/state.json`
- `memories/MEMORY.md`

### 5.3 Worker-Run Files

For every active run:

- `status.json`
- `summary.md`
- `scratch.md`
- `handoff.md`
- `extracted.json`

## 6. Object Fields

All long-term memory files must support:

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

- `source`
- `supersedes`
- `tags`

All time values must be absolute.

## 7. Promotion Rules

### 7.1 Worker-Run To Workspace Candidate

Threshold:

- minimum candidate quality gate around `0.55`

Required exclusions:

- greetings
- trivial confirmations
- open questions
- pure execution chatter

### 7.2 Workspace Candidate To Workspace Active

Default thresholds:

- `feedback >= 0.85`
- `project >= 0.80`
- `reference >= 0.80`
- `open_loop >= 0.90`

Required guards:

- task-scoped feedback must remain candidate-only
- project items must be declarative
- reference items must be takeaway-oriented

### 7.3 Workspace To Global

Global promotion requires:

- cross-workspace evidence
- or explicit global instruction from the user

Default thresholds:

- `global candidate >= 0.70`
- `global active >= 0.88`
- lower threshold allowed only when explicit global intent exists

Hard rule:

- unresolved conflicts must go to the conflict queue before activation

Additional rules:

- `user` may promote globally from workspace candidates when confidence is high enough
- `reference` requires stricter cross-workspace proof than `feedback`
- copied workspace history must not be treated as independent workspace proof

### 7.4 Global Candidate Governance

Rules:

- promoted keys must leave the active candidate pool
- duplicate candidate keys keep only the best current item
- expired candidates move to `global/candidates_archive/`
- overflow beyond per-type limits moves to `global/candidates_archive/`

## 8. Conflict Queue

The implementation must support:

- conflict item creation
- conflict state transitions
- conflict report output
- `scope_split` resolution

Minimum states:

- `open`
- `needs_review`
- `resolved_promote_a`
- `resolved_promote_b`
- `resolved_scope_split`
- `resolved_reject_both`
- `archived`

## 9. Runtime Templates

### 9.1 Global Context

Must contain:

- user defaults
- confirmed global feedback
- reusable references
- global warnings
- open global decisions

### 9.2 Workspace Active Context

Must contain:

- current goal
- active open loops
- confirmed workspace feedback
- project facts
- relevant references
- files in motion
- errors and risks
- next step
- important quotes

### 9.3 Worker Handoff

Must contain:

- current goal
- done
- next
- risks

## 10. Dream Requirements

### 10.1 Workspace Dream

Must:

- merge candidates
- mark stale or superseded memories
- rebuild workspace `MEMORY.md`
- rebuild workspace `active_context.md`
- write workspace dream reports

### 10.2 Global Dream

Must:

- cluster workspace memories across projects
- score global promotion candidates
- create conflict items for uncertain truth
- rebuild `global_context.md`
- rebuild global `MEMORY.md`
- write global dream reports

## 11. Safety Constraints

The implementation must not:

- modify `~/.codex/.codex-global-state.json`
- modify Codex sqlite databases
- treat runtime scratch state as active long-term truth
- keep two contradictory active truths with the same identity
- promote workspace-only facts into global memory

## 12. Test Requirements

Automated tests must cover:

1. workspace key generation
2. workspace index maintenance
3. session-to-workspace matching
4. candidate staging
5. workspace promotion thresholds
6. content-based identity keys
7. question rejection
8. task-scoped feedback demotion
9. reference request rejection
10. bounded workspace context generation
11. global candidate clustering
12. conflict queue creation

Manual QA must cover:

1. new worker startup read order
2. workspace node creation
3. repeated runs staying incremental
4. global conflict handling
5. workspace-to-global promotion sanity
