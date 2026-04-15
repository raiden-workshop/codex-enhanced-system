# Spec / 规格

## Goal / 目标

- 为 `knowledge-base` 增加 `query/search/ask` 命令，支持按标题、路径、标题层级、稳定结论和正文做轻量检索，并输出基础 provenance。
- Add a `query/search/ask` command to `knowledge-base` that performs lightweight search over titles, paths, headings, stable claims, and body text, then returns basic provenance.

## User Value / 用户价值

- 用户现在可以先“查到什么页最相关”，再顺着 `source_refs` 与 `related` 去追溯，不必只靠手工打开 `index.md` 和 `overview.md`。
- Users can now first ask “which pages are most relevant,” then follow `source_refs` and `related` to trace support, instead of relying only on manual navigation through `index.md` and `overview.md`.

## In Scope / 范围内

- 新增 `kb query` 命令及 `search` / `ask` 别名。
- Add the `kb query` command and the `search` / `ask` aliases.
- 结果排序、命中字段说明、摘要片段输出。
- Add ranking, matched-field explanations, and snippet output.
- 输出 `source_refs` 与 `related`。
- Return `source_refs` and `related`.
- 兼容无 `.md` 后缀的 frontmatter 短引用解析。
- Resolve extensionless frontmatter shorthand references.
- 为 `maintain` 补 provenance-aware 的 `source_refs` 目标校验。
- Add provenance-aware `source_refs` target validation to `maintain`.
- 补充命令文档与回归测试。
- Add command docs and regression tests.

## Out Of Scope / 范围外

- 向量检索、embedding、数据库索引。
- Vector search, embeddings, or database-backed indexing.
- 自动 citation 编排或跨页证据聚合。
- Automatic citation composition or cross-page evidence aggregation.
- page evolution 状态机。
- A page-evolution state machine.
- 自动健康检查调度。
- Automated health-check scheduling.

## Constraints / 约束

- technical_constraints: 继续使用标准库；不引入新的服务依赖；保持脚本可直接执行。
- technical_constraints_en: Stay within the standard library, add no service dependencies, and keep the script directly executable.
- workflow_constraints: 不动现有知识页内容，只增强 CLI 和说明文档。
- workflow_constraints_en: Do not rewrite existing knowledge pages; only enhance the CLI and its documentation.
- policy_constraints: provenance 只做轻量展示，不把 raw 命中直接提升为 canonical answer。
- policy_constraints_en: Provenance remains lightweight and must not promote raw hits into canonical answers by itself.

## Acceptance Criteria / 验收标准

- `python3 knowledge-base/kb query "formal memory"` 可以返回排序结果。
- `python3 knowledge-base/kb query "formal memory"` returns ranked results.
- 结果里包含 `matched_fields`、`snippet`、`source_refs`、`related`。
- Results include `matched_fields`, `snippet`, `source_refs`, and `related`.
- `--json` 输出可被机器读取。
- `--json` output is machine-readable.
- 无后缀短引用在 provenance 解析中可正确补成 `.md`。
- Extensionless shorthand references are resolved to `.md` correctly in provenance handling.
- `python3 knowledge-base/kb maintain` 在当前仓库上可通过，并能检查 `source_refs` 的目标位置是否合法。
- `python3 knowledge-base/kb maintain` passes on the current repository and validates whether `source_refs` point to valid support locations.
- 新增测试覆盖查询和引用解析。
- New tests cover both query behavior and reference resolution.

## Open Questions / 未决问题

- 下一轮是否把 `report` 结果默认降权，而不是简单排除。
- Whether the next slice should down-rank `report` results by default instead of simply excluding them.
- 下一轮是否把 bilingual 镜像页做结果去重。
- Whether the next slice should dedupe bilingual mirrored pages in search results.
