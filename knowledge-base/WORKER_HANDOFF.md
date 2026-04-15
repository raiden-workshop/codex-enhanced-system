# Knowledge-Base Worker Handoff

This document is the current execution handoff for the `knowledge-base` worker.

It is intentionally short and current-state focused.

## 1. Official Workspace

- Official working directory: `<repo-root>/knowledge-base`
- Official repository: `raiden-workshop/codex-enhanced-system` (`knowledge-base/` subdirectory)
- Official memory node: `knowledge-base-<workspace-key>`

Do not treat `<archive-root>/knowledge-base` as an active workspace.
That path is only the historical seed origin.

## 2. What The New Scheme Is

This repository is now:

- an independent worker space
- a cross-project Markdown knowledge base
- a single-writer canonical graph by default
- a complement to the global memory system

It is not:

- a repo-local subfolder of `mult-agent`
- a replacement for the global memory system
- a fully multi-domain platform yet

## 3. Current Operating Mode

Current mode:

- `use-and-review mode`

Meaning:

- use the current graph for real work first
- ingest only when repeated questions reveal a real gap
- expand to a second domain only when the report layer justifies it

## 4. Current Scope

Current founding domain:

- `Codex-native memory governance`

Current graph size:

- Sources: `15`
- Entities: `2`
- Concepts: `4`
- Syntheses: `3`
- Domains: `1`
- Reports: `3`

## 5. Read Order

Read in this order:

1. `AGENTS.md`
2. `START_HERE.md`
3. `README.md`
4. `wiki/hot.md`
5. `wiki/domains/domain-codex-native-memory-governance.md`
6. `wiki/overview.md`
7. `wiki/index.md`
8. `wiki/reports/report-domain-expansion-readiness-2026-04-09.md`
9. `wiki/reports/report-lint-2026-04-09.md`
10. `wiki/reports/report-source-priority-2026-04-09.md`
11. `wiki/log.md`

## 6. What Counts As Canonical

Canonical:

- `wiki/domains/`
- `wiki/sources/`
- `wiki/entities/`
- `wiki/concepts/`
- `wiki/syntheses/`

Not canonical:

- `wiki/reports/`
- `output/`

## 7. How To Work

### Query

Recommended path:

1. read `wiki/hot.md`
2. jump to the most relevant synthesis or source
3. answer with explicit page references
4. only write back if the result has clear reuse value

### Ingest

Required order:

1. save raw material into `raw/`
2. create or update a source page
3. update concept, entity, or synthesis pages only if the graph actually changes
4. update `wiki/index.md`
5. append `wiki/log.md`
6. update `wiki/overview.md` or `wiki/hot.md` only when the high-level path really changed

### Report

Use `wiki/reports/` for:

- lint findings
- source-priority updates
- domain-expansion decisions
- future stale-review or drift checks

## 8. Rules About Expansion

Do not add a second domain because another project directory exists.

Before adding a new domain:

1. read `wiki/reports/report-domain-expansion-readiness-2026-04-09.md`
2. confirm the topic does not fit the founding domain
3. confirm repeated real usage justifies the split
4. write or update a report first
5. only then create `wiki/domains/domain-<slug>.md`

## 9. Current Key Pages

Main entry pages:

- `wiki/syntheses/synthesis-codex-native-memory-governance-baseline.md`
- `wiki/syntheses/synthesis-upstream-integration-rollout.md`
- `wiki/syntheses/synthesis-upstream-reviewer-packet.md`

Main governance pages:

- `wiki/reports/report-lint-2026-04-09.md`
- `wiki/reports/report-source-priority-2026-04-09.md`
- `wiki/reports/report-domain-expansion-readiness-2026-04-09.md`

## 10. What Not To Do

- Do not keep expanding support docs without a usage-driven reason
- Do not add `candidates/`, `state/`, or automation prematurely
- Do not widen the founding domain until the domain boundary is clearly broken by real work
- Do not treat migration history as active operating context

## 11. Bottom Line

This repository is already a stable working baseline.

The right next behavior is:

- use it
- review it
- patch real gaps

Not:

- rebuild it again
- over-platform it
- pretend it already needs many domains
