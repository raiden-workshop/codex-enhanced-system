# Plan Review / 计划复核

## Review / 复核

- 这是 metadata closeout 问题，不需要引入新的 graph state。
- 用现有 `render_page` 渲染 index 可以保持 frontmatter 和 body 更新路径一致。
- 通过测试覆盖 `reindex` 与 index-entry removal 两条路径，就能验证真实语义而不必在 live repo 做破坏性实验。

- This is a metadata-closeout problem and does not require a new graph state layer.
- Rendering the index through the existing `render_page` path keeps frontmatter and body updates consistent.
- Covering both `reindex` and the index-entry removal path in tests verifies the semantics without needing destructive experiments in the live repo.
