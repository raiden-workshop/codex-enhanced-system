# Plan / 计划

## Architecture / 架构

- 在 `knowledge-base/kb` 内直接增加 query 子命令，复用现有 page 解析、canonical page 枚举和 frontmatter 结构。
- Add the query subcommand directly inside `knowledge-base/kb`, reusing existing page parsing, canonical-page enumeration, and frontmatter structures.

## Data Flow / 数据流

- 用户输入查询词。
- The user provides search terms.
- CLI 枚举 canonical pages，按标题、路径、标题层级、稳定结论和正文计算分值。
- The CLI enumerates canonical pages and scores them across title, path, heading, stable-claim, and body matches.
- 结果返回 `snippet`、`source_refs` 和 `related`。
- The result includes `snippet`, `source_refs`, and `related`.
- 若使用 `--json`，则返回结构化 JSON 供后续 automation 或脚本消费。
- With `--json`, the command returns structured JSON for later automation or scripts.

## Touch Points / 触点

- files_or_modules: `knowledge-base/kb`, `knowledge-base/tests/test_kb_query.py`
- docs_to_update: `knowledge-base/KB_COMMANDS.md`, `docs/specs/2026-04-11-kb-query-provenance/*`
- external_inputs: 当前 canonical pages 与其 frontmatter

## Implementation Order / 实现顺序

1. 在 `kb` 中补 query 结果模型、匹配打分和 provenance 渲染。
2. 在 `kb` 中统一 frontmatter 短引用解析，并把 `maintain` 升级为 provenance-aware 检查。
3. 补测试与命令文档，并做本地验证。

## Risks / 风险

- risk: 旧页面的 `related` 或 `source_refs` 使用无后缀短引用，解析不一致会导致 provenance 失真。
  mitigation: 统一引入 `resolve_repo_reference()`，优先复用到 provenance 相关路径解析。
- risk: 查询结果过于依赖正文命中，导致噪音偏高。
  mitigation: 提高标题、标题层级和稳定结论的权重，并限制 body hit 的加分上限。

## Test Strategy / 测试策略

- unit_or_local_checks: `python3 -m unittest knowledge-base/tests/test_kb_query.py`
- integration_or_manual_checks: `python3 knowledge-base/kb query "formal memory" --limit 3`
- integration_or_manual_checks_2: `python3 knowledge-base/kb maintain`
- failure_cases_to_cover: 无后缀短引用、`--json` 输出、`--type` 过滤、`source_refs` 目标分类

## Rollout Strategy / 发布策略

- release_or_merge_notes: 这是增量命令增强，不需要迁移已有知识页。
- rollback_notes: 若查询结果不稳，可先回退 `kb` 的 query 子命令与引用解析改动，不影响已有 add/log/maintain/reindex/delete/distill-memory。

## Out Of Scope / 范围外

- 复杂 ranking 调优
- Query result dedupe for bilingual mirror pages
- 自动健康检查与 query 合约版本化
