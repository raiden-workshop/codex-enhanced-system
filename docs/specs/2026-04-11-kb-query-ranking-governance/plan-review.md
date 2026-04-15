# Plan Review / 计划复核

## Review / 复核

- 方案保持在 `kb query` 这条竖线内，没有扩大到 wiki 内容重写。
- locale mirror dedupe 采用保守识别，只处理带明显语言后缀的标题或 slug，避免误伤不同主题页。
- 排序治理保留 `match_score`，避免最终分数完全黑盒化。

- The plan stays inside the `kb query` vertical slice and does not expand into wiki content rewriting.
- Locale-mirror dedupe uses conservative detection and only handles titles or slugs with obvious language suffixes, reducing the chance of collapsing distinct topics.
- Ranking governance retains `match_score` so the final score does not become fully opaque.
