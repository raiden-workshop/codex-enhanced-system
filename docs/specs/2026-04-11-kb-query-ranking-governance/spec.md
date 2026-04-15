# Spec / 规格

## Goals / 目标

- `query` 默认优先返回更接近“答案页”的结果。
- `report` 只有在显式纳入时参与结果集，但仍保持降权。
- 明显的 locale mirror 结果默认收口为一条，并保留被折叠路径信息。

- `query` should prefer results that behave more like answer pages by default.
- `report` pages may join the result set only when explicitly included, but they remain downweighted.
- Obvious locale-mirror results should collapse into one default result while preserving the suppressed paths.

## Non-Goals / 非目标

- 不做语义向量检索
- 不自动重写 wiki 页面内容
- 不做跨文件 citation 修复

- No semantic vector retrieval
- No automatic wiki page rewriting
- No cross-file citation repair

## Functional Rules / 功能规则

- 查询结果增加类型治理分：`concept`、`synthesis`、`entity`、`domain` 优先于 `source`，`report` 明显降权。
- 查询结果增加轻量质量分：有 `source_refs` 和稳定结论的页更容易排前。
- 带 locale 后缀的标题或 slug 视为镜像候选；若同 kind 下出现同基准 stem 或 title，则默认只保留最高优先结果。
- 默认输出保留 `score`，并新增 `match_score` 区分词面命中分。
- 去重后若有被折叠页面，输出 `suppressed_duplicates`。
- 提供 `--no-dedupe` 以便显式查看原始重复结果。

- Add type-governance ranking so `concept`, `synthesis`, `entity`, and `domain` outrank `source`, while `report` is materially downweighted.
- Add small quality bonuses so pages with `source_refs` and stable claims surface more easily.
- Treat locale-suffixed titles or slugs as mirror candidates; when the same kind shares a normalized base stem or title, keep only the highest-priority result by default.
- Keep `score` in the default output and add `match_score` so lexical matching remains visible.
- Emit `suppressed_duplicates` when dedupe collapses mirrored pages.
- Provide `--no-dedupe` for explicit raw duplicate inspection.
