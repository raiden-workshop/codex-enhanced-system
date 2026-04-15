# Intake / 需求摄取

## Request / 请求

- 用户要求“不断点续跑，按切片逐个验证，不把验证完全省掉”。
- The user asked to keep rolling slice by slice, with verification on every slice instead of skipping validation.

## Problem / 问题

- 现有 `kb query` 已可用，但默认排序仍偏词面命中，容易把 `source` 大量顶到前面。
- `report` 即使被纳入查询，也不该和答案型 canonical 页处在同一优先级。
- 未来双语页或镜像页增多后，查询结果会出现明显重复。

- The current `kb query` works, but ranking still leans too much on lexical hits and can crowd the top with `source` pages.
- Even when included, `report` pages should not share the same default priority as answer-like canonical pages.
- As bilingual or mirrored pages increase, obvious duplicate results will show up in queries.

## Scope / 范围

- 调整 `kb query` 排序分数
- 为镜像重复结果增加保守去重
- 保持 CLI 和 JSON 输出可解释
- 补测试与双语命令文档

- Adjust `kb query` ranking scores
- Add conservative dedupe for mirrored duplicate results
- Keep CLI and JSON output explainable
- Add tests and bilingual command docs
