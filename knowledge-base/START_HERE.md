# Start Here

This file is the shortest current-state brief for the `knowledge-base` worker.

## Official Position

- Official workspace root: `<repo-root>/knowledge-base`
- Official GitHub repo: `raiden-workshop/codex-enhanced-system` (`knowledge-base/` subdirectory)
- Old path `<archive-root>/knowledge-base` is no longer the working directory
- The old path matters only as historical seed origin, not as an active workspace

## Current Strategy

- This repository is an independent cross-project Markdown knowledge base
- It currently runs with one mature founding domain:
  - `Codex-native memory governance`
- Current mode is:
  - `use-and-review mode`
- That means:
  - use the current graph in real work first
  - add new sources only when repeated questions reveal a real gap
  - add a second domain only when the domain-expansion report says it is justified

## Read Order

1. `AGENTS.md`
2. `README.md`
3. `wiki/hot.md`
4. `wiki/domains/domain-codex-native-memory-governance.md`
5. `wiki/overview.md`
6. `wiki/index.md`
7. `wiki/reports/report-domain-expansion-readiness-2026-04-09.md`
8. `wiki/reports/report-lint-2026-04-09.md`
9. `wiki/reports/report-source-priority-2026-04-09.md`
10. `wiki/log.md`

## What You Should Treat As Canonical

- `wiki/domains/`
- `wiki/sources/`
- `wiki/entities/`
- `wiki/concepts/`
- `wiki/syntheses/`

Do not treat these as canonical truth:

- `wiki/reports/`
- `output/`

## Current Working Rules

- Save raw first, then write canonical knowledge
- Do not write canonical conclusions without supporting source pages
- Update `wiki/index.md` and `wiki/log.md` whenever canonical knowledge changes
- Keep the graph centered on explicit domain boundaries
- Do not silently widen the founding domain to absorb unrelated project topics

## Current Do / Do Not

Do now:

- Answer real questions using the current founding domain
- Ingest new sources only when they clearly close a repeated gap
- Write lightweight reports before making broader structural changes

Do not do now:

- Do not create a second domain just because another project exists
- Do not add `candidates/`, `state/`, or automation prematurely
- Do not keep expanding support docs without a real usage-driven reason

## If The Task Is About Expansion

- Read `wiki/reports/report-domain-expansion-readiness-2026-04-09.md` first
- If the new topic does not fit the founding domain, write or update a report before creating canonical pages
- Only create `wiki/domains/domain-<slug>.md` after the boundary is clear

## Current Baseline Snapshot

- Sources: `15`
- Entities: `2`
- Concepts: `4`
- Syntheses: `3`
- Domains: `1`
- Reports: `3`

## Key Pages

- `wiki/syntheses/synthesis-codex-native-memory-governance-baseline.md`
- `wiki/syntheses/synthesis-upstream-integration-rollout.md`
- `wiki/syntheses/synthesis-upstream-reviewer-packet.md`

## If You Are Unsure

- Start with `wiki/hot.md`
- Prefer a small report or issue over speculative graph expansion
- Keep the repository cleaner and smaller rather than broader and noisier
