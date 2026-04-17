# Tasks / 任务

## Task List / 任务列表

### T1

- id: `T1`
- goal: 在 `/Users/wz/project/knowledge-base/kb` 里实现 query 命令与 provenance 输出。
- goal_en: Implement the query command and provenance output in `/Users/wz/project/knowledge-base/kb`.
- files: `/Users/wz/project/knowledge-base/kb`
- depends_on: `none`
- verification: 直接运行 `python3 /Users/wz/project/knowledge-base/kb query ...`
- done_definition: 查询结果可读、可排序，并附带 `source_refs` / `related`

### T2

- id: `T2`
- goal: 补上无后缀短引用解析与回归测试。
- goal_en: Add extensionless shorthand reference resolution, provenance-aware maintain checks, and regression tests.
- files: `/Users/wz/project/knowledge-base/kb`, `/Users/wz/project/knowledge-base/tests/test_kb_query.py`
- depends_on: `T1`
- verification: `python3 -m unittest /Users/wz/project/knowledge-base/tests/test_kb_query.py`, `python3 /Users/wz/project/knowledge-base/kb maintain`
- done_definition: 测试覆盖查询与引用解析，`maintain` 能验证 `source_refs` 目标，且全部通过

### T3

- id: `T3`
- goal: 补命令文档与变更包验证记录。
- goal_en: Add command documentation and package verification records.
- files: `/Users/wz/project/knowledge-base/KB_COMMANDS.md`, `docs/specs/2026-04-11-kb-query-provenance/*`
- depends_on: `T1`, `T2`
- verification: 文档与实际命令一致，verify 记录完整
- done_definition: 文档可作为下一轮续跑的真相源

## Dependency Summary / 依赖摘要

- `T1 -> T2 -> T3`

## Execution Notes / 执行说明

- sequencing_notes: 先稳定行为，再补测试和文档。
- parallelism_notes: 当前改动集中在一个 CLI 脚本，平行化收益不高。
- rollback_notes: 若 query 行为不稳定，可只回退 `kb` 与新测试，不影响其他现有命令。
