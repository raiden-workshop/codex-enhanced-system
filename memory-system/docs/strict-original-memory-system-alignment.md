# Strict-Original Memory System Alignment

This checklist keeps the design document, development spec, and implementation aligned.

## 1. Scope Alignment

- Design says the system is a strict imitation of the article's single-agent-centered model.
- Development defines the canonical implementation under `~/.codex/memory/` with workspace-scoped nodes under `workspaces/<workspace-key>/`.
- Implementation may retire the deprecated `state/memory/` system and older workspace-local memory roots when migrating to the global model.

## 2. Structure Alignment

- Design requires four instruction layers.
- Development requires those files under `instructions/company|user|local/GUIDE.md` and `workspaces/<workspace-key>/instructions/repo/GUIDE.md`.
- Implementation must scaffold all four layers even if some start as templates.

## 3. Memory-Type Alignment

- Design defines four memory classes.
- Development requires staged candidates plus active memories under matching directories.
- Implementation must write:
  - `candidates/user/`
  - `candidates/feedback/`
  - `candidates/project/`
  - `candidates/reference/`
  - `memories/user/`
  - `memories/feedback/`
  - `memories/project/`
  - `memories/reference/`

## 4. Feedback Alignment

- Design requires feedback memories to include `Rule`, `Why`, and `How to apply`.
- Development requires extracting both corrections and confirmations.
- Implementation must distinguish durable defaults from task-scoped instructions.
- Implementation must keep task-scoped instructions in `candidates/` unless later promoted.

## 4.1 Quality Gates Alignment

- Design requires declarative long-term memory rather than question-shaped noise.
- Development requires question filtering for project/reference and assistant-summary extraction for references.
- Implementation must reject question-like project/reference candidates and must not store the user's "go read this" request as a reference takeaway.
- Implementation must cap active reference promotion per source and prefer only the highest-scoring reusable takeaways.

## 5. Index Alignment

- Design requires `MEMORY.md` to remain short, bounded, and index-like.
- Development sets `index_max_lines=200` and `index_max_chars_per_entry=150`.
- Implementation must rebuild `memories/MEMORY.md` from active memory files only and obey those limits.

## 6. Compression Alignment

- Design requires three compression levels.
- Development defines outputs under the workspace-scoped `runtime/`.
- Implementation must choose a compression level and emit:
  - `runtime/active_context.md`
  - `runtime/compression/latest.md`
- Implementation must build execution sections from the current focus window instead of blending all recent sessions indiscriminately.

## 7. Dream Alignment

- Design requires dream to orient, collect, integrate, and prune.
- Development defines threshold logic and report output.
- Implementation must maintain `dream/state.json` and emit dream reports when thresholds are met or forced.

## 8. Safety Alignment

- Design excludes multi-worker shared-write logic and vector-first retrieval.
- Development prohibits changes to Codex runtime state and sqlite databases.
- Implementation must stay within the global memory root, its workspace-scoped nodes, its own scripts/tests, and explicit migration edits.
- Implementation must not promote low-confidence extracted text directly into active long-term memory.

## 9. QA Alignment

- Development lists automated tests and real-workspace QA.
- Review must verify design drift, duplicate generation, and schema mismatches.
- QA must verify a real run plus at least one repeat run.
