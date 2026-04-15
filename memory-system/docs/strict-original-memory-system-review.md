# Strict-Original Memory System Review

## Findings

### Resolved

- Old and new memory systems coexisted, which left the workspace instructions pointing at the retired `state/memory/` tree while newer logic lived elsewhere.
- The strict-original implementation originally treated itself as a side-by-side prototype instead of the canonical system, which created documentation drift.
- Runtime compressed context could retain deleted-file references from old sessions because file extraction accepted historical absolute paths without checking whether they still existed.
- Long-term memory used to accept question-shaped project items, task-scoped feedback, and request-shaped references directly into active memory.
- Title-only slug dedupe could collide for non-ASCII titles such as repeated `Confirmed: ...` memories.
- Reference promotion used to over-collect source-related analysis sentences into active memory instead of selecting only the strongest reusable takeaways.
- Runtime compressed context used to blend all recent sessions equally, which made `Errors Encountered` and `Decisions Made` noisier than the article-aligned model.
- Internal instruction files were unnecessarily named `CLAUDE.md`, which copied the article/source naming instead of matching the Codex environment.

### Residual Risk

- Heuristic extraction is intentionally conservative but still imperfect; some reference memories still capture meta-analysis around an external source, not just the cleanest reusable conclusion.
- Active context extraction for `Errors Encountered` and `Decisions Made` is still regex-based and can surface historical noise from recent sessions.

### Current Assessment

- No blocking design drift remains relative to the article's core shape:
  - four instruction layers
  - four memory types
  - file-based long-term memory
  - staged write path
  - graded compression
  - dream maintenance loop
- Remaining issues are now quality-optimization items rather than architectural mismatches.

## Review Decision

- Make `~/.codex/memory/` the official global memory root, with workspace-scoped nodes under `workspaces/<workspace-key>/`.
- Retire `state/memory/`, older workspace-local memory roots, and stale workspace-only entrypoints.
- Keep the new system article-aligned and single-agent-centered.
- Introduce a staged `candidates/` layer and promote only high-confidence durable items into `memories/`.
- Use content-derived identity keys for file naming and update detection.
