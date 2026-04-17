# Verify / 验证

## Change Summary / 变更摘要

- 新增 `/Users/wz/project/knowledge-base/kb query` 命令，支持 `search` / `ask` 别名。
- Added the `/Users/wz/project/knowledge-base/kb query` command with `search` / `ask` aliases.
- 查询结果现在会输出 `matched_fields`、`snippet`、`source_refs` 和 `related`。
- Query results now include `matched_fields`, `snippet`, `source_refs`, and `related`.
- provenance 解析现在兼容无 `.md` 后缀的 frontmatter 短引用。
- Provenance resolution now supports extensionless frontmatter shorthand references.
- `maintain` 现在会额外检查 `source_refs` 是否仍然落在合理支持位置。
- `maintain` now additionally validates whether `source_refs` still point to valid support locations.
- 新增 `/Users/wz/project/knowledge-base/tests/test_kb_query.py` 回归测试。
- Added `/Users/wz/project/knowledge-base/tests/test_kb_query.py` regression tests.

## Status / 状态

| Field | Value |
| --- | --- |
| behavior_check | `pass` |
| test_check | `pass` |
| regression_risk | `medium` |
| doc_sync_needed | `completed` |
| memory_candidate | `no` |
| final_status | `passed` |

## Behavior Validation / 行为验证

- 运行：`python3 /Users/wz/project/knowledge-base/kb query "formal memory" --limit 3`
- Result: 返回了排序结果、命中字段、摘要片段和 provenance 字段。
- Result_en: Returned ranked results with matched fields, snippets, and provenance.

- 运行：`python3 /Users/wz/project/knowledge-base/kb query "formal memory" --json --limit 2`
- Result: 返回结构化 JSON，可直接给后续自动流程消费。
- Result_en: Returned structured JSON suitable for later automated consumers.

- 运行：`python3 /Users/wz/project/knowledge-base/kb maintain`
- Result: 当前仓库输出 `issues: none`。
- Result_en: The current repository reported `issues: none`.

## Test Validation / 测试验证

- 运行：`python3 -m unittest /Users/wz/project/knowledge-base/tests/test_kb_query.py`
- Result: `Ran 4 tests ... OK`

## Regression Risk / 回归风险

- 风险点主要在 `extract_frontmatter_links()` 的引用解析行为变化。
- The main regression surface is the changed reference-resolution behavior inside `extract_frontmatter_links()`.
- 当前通过新增测试覆盖了 query 和 shorthand resolution，但还没有覆盖 `maintain` 的更广泛页面集。
- The new tests cover query behavior and shorthand resolution, but they do not yet cover the full `maintain` flow across the broader page set.

## Documentation Sync / 文档同步

- 已更新 `/Users/wz/project/knowledge-base/KB_COMMANDS.md` 的命令说明。
- Updated the command documentation in `/Users/wz/project/knowledge-base/KB_COMMANDS.md`.
- 已新增本轮双语变更包文档。
- Added the bilingual change-package documents for this round.

## Memory Candidate / 记忆候选

- eligible: `no`
- candidate_summary: 
- why_stable: 
- why_not: 这是 repo 内的增量功能交付，不属于应进入长期 memory 的跨项目稳定偏好或长期原则。

## Open Issues / 未决问题

- 下一轮可以继续补 query 结果去重、report 降权和 provenance lint。
- The next slice can continue with result dedupe, report down-ranking, and provenance linting.
