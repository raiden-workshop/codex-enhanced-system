# Plan / 计划

1. 在 `knowledge-base/kb` 中拆分 `match_score` 与最终排序分，并加入类型、状态、质量、locale 变体修正。
   In `knowledge-base/kb`, split `match_score` from the final ranking score and add type, status, quality, and locale-variant adjustments.

2. 为 query 结果增加保守 dedupe，只折叠明显的 locale mirror 结果。
   Add conservative dedupe for query results and collapse only obvious locale-mirror duplicates.

3. 更新输出契约、命令文档和测试。
   Update the output contract, command docs, and tests.

4. 跑单测与真实 CLI 查询验证。
   Run unit tests and real CLI query verification.
