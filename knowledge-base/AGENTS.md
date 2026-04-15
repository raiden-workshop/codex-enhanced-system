# Knowledge Base Workspace Guide

## Purpose

- This workspace is an independent knowledge-base worker space.
- It exists to hold cross-project canonical knowledge in Markdown.
- It complements the global memory system and must not replace it.
- The global memory system remains the authority for stable user preferences, project rules, and hot-path execution context.

## Current Stage

- Stage: `v1`
- Status: migrated into an independent worker space and upgraded to a cross-project knowledge-base shell on `2026-04-09`
- Scope: cross-project knowledge base with one seeded founding domain
- Founding domain: `Codex-native memory governance`
- Seed corpus: `codex-memory-kit` repository baseline, docs index, repository map, naming convention, `oh-my-codex` integration contract docs, and rollout or review docs

This workspace originally started without `hot.md`, `domains/`, `candidates/`, `reports/`, or `state/`.
A lightweight `hot.md` and `wiki/reports/` are now allowed because the source graph is large enough to justify a short onboarding path plus a small health layer.
The rest still belong to `v1.5+` and remain deferred until repeated usage proves the need.

## Read Order

1. `START_HERE.md`
2. `README.md`
3. `wiki/hot.md`
4. `wiki/domains/domain-codex-native-memory-governance.md`
5. `wiki/index.md`
6. `wiki/overview.md`
7. `wiki/reports/`
8. `wiki/log.md`
9. Relevant pages under `wiki/`

## Roles

### Human

- Decides when a new project or domain is important enough to enter the cross-project graph
- Provides seed sources
- Resolves disputes
- Decides whether any short, stable conclusion should be promoted into the global memory system

### Task Worker

- May read `wiki/` and `output/`
- Should delegate to the knowledge worker when a task needs cross-source synthesis, historical context, or cited answers
- Must not directly edit `wiki/` unless explicitly asked to act as the knowledge worker

### Knowledge Worker

- Default single writer for `wiki/`
- Reads from `raw/`
- Writes canonical pages to `wiki/`
- May write temporary deliverables to `output/`

## Directory Rules

- `raw/`
  - Source intake layer
  - Save-first area for articles, papers, repo notes, and other source material
  - Treat as append-first and effectively read-only after ingest
- `wiki/`
  - Canonical knowledge layer
  - All durable source summaries, concepts, entities, and syntheses go here
- `wiki/domains/`
  - Domain registry layer
  - Each page describes one domain's scope, entry points, and status inside the cross-project graph
- `wiki/reports/`
  - Lightweight governance layer
  - Holds lint reports, health snapshots, and review-oriented checks
  - Do not treat reports as domain truth; treat them as maintenance artifacts
- `output/`
  - Temporary exports, ad hoc reports, and non-canonical deliverables
  - Do not treat as canonical knowledge

## Writing Rules

- Save raw first, then write canonical knowledge
- One source page per source
- Do not create canonical conclusions without a supporting source page
- Update `wiki/index.md` and `wiki/log.md` in the same change whenever canonical knowledge changes
- Do not silently overwrite old conclusions
- Do not silently mix new domains into the graph without adding or updating a domain registry page
- Keep one founding domain stable before seeding broad new domains
- Treat the old `mult-agent/knowledge-base` path as historical seed origin only, not as an active workspace
- Only short, stable, reusable conclusions may be proposed for promotion into the global memory system, and only on explicit request
- Do not ingest secrets, tokens, private credentials, or material that should not live in a local knowledge store

## Naming Rules

- Use kebab-case filenames
- Use these filename prefixes for canonical pages:
  - `wiki/sources/source-<slug>.md`
  - `wiki/entities/entity-<slug>.md`
  - `wiki/concepts/concept-<slug>.md`
  - `wiki/syntheses/synthesis-<slug>.md`

## Operations

### First Seed

The founding domain seed is already complete:

1. Founding domain fixed as `Codex-native memory governance`
2. Initial seed imported from `<archive-root>`
3. Canonical source pages created under `wiki/sources/`
4. Initial entity, concept, and synthesis pages created under `wiki/`
5. Domain registry page created under `wiki/domains/`

For future ingest, stay inside this founding domain unless a new cross-project domain is explicitly added.

### Ingest

1. Save the source into the appropriate `raw/` bucket
2. Read the full source before summarizing it
3. Create or update a `source` page under `wiki/sources/`
4. Update affected `concept`, `entity`, or `synthesis` pages when the source changes the knowledge graph
5. Update `wiki/overview.md` if the big picture changed
6. Update `wiki/index.md`
7. Append an entry to `wiki/log.md`

### Query

1. Read `wiki/index.md`
2. Read `wiki/overview.md`
3. Open the relevant canonical pages
4. Answer with explicit page references
5. If the answer has reuse value, write it back as a `synthesis` page or a temporary deliverable under `output/`

### Lint

For `v1`, lint is minimal and manual-first. Check at least:

- frontmatter present and valid
- `source_refs` not empty when a page depends on sources
- broken internal links
- pages missing from `wiki/index.md`
- obvious overview/index drift

Now that `wiki/reports/` exists, record important manual lint results there before reaching for heavier `v1.5` state or automation.

## Method Forge Autonomous Coding

- 当用户表达“开始落地代码”“开始实现”“开始写代码”“继续写代码”“进入实现阶段”等实现意图时，默认进入 `method-forge` autonomous mode，除非用户明确要求不要自动、先别写代码或只做方案。
- autonomous mode 使用 Codex 原生 heartbeat / background automation 作为监听者，不重做第二套调度器。
- autonomous mode 的内层默认执行引擎是 `method-forge-execute`；在 autonomous 已经启动后，后续续跑周期不需要用户再次指定“按 method-forge 执行”。
- 若当前任务还没有标准变更包，先建立 `docs/specs/<change-id>/`、`package-index.md` 和 `runtime/run-state.md`。
- 若已有需求或设计草稿，先由 `method-forge-execute` 归一化为 `intake/spec/plan/tasks`，再进入实现。
- 实现完成后必须产出 `verify.md`；高风险改动可在 verify 前追加 `code-review.md`。
- 若 `verify.md` 认为存在稳定可复用结论，只能提出 `memory-candidate.md`，不得直接写长期 memory。
- autonomous mode 必须执行 loop guard：同一步最多重试 3 次，同一错误签名最多重复 2 次，连续无进展最多 2 轮，单任务最多 12 个周期。
- 不要把单个微切片或一次 `verify` 通过误记为 `completed`；若同一用户目标下下一安全切片已明确，应保持 `running` 并自动推进。 / Do not mark the run `completed` just because a single micro-slice or one `verify` pass finished; if the next safe slice inside the same user goal is already known, keep it `running` and continue automatically.
- 触发 `blocked`、`waiting-human`、`waiting-external` 或 `completed` 后必须停止自动推进，并在 `run-state.md` 写明 `stop_reason` 与 `next_action`。
- 若本文件已有更具体的 knowledge-base 写入、晋升或单一写入者规则，以更具体规则为准，但不得取消 `verify` 或 loop guard。
