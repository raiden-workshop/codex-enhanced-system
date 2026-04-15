# Intake / 需求摄取

## Request / 请求

- 用户要求继续做 `provenance lint 强化 + 知识页健康检查`，并在做完后继续写代码。
- The user asked to continue with `provenance lint hardening + knowledge-page health checks`, then keep coding after that slice.

## Problem / 问题

- 现有 `maintain` 已经能检查 `source_refs` 的目标位置是否合法，但还不能判断“支持质量是否足够好”。
- `wiki/index.md`、`wiki/overview.md`、`wiki/hot.md`、`wiki/log.md` 这些导航层页面还没有被系统检查，未来容易静默漂移。

- The current `maintain` command already validates whether `source_refs` point to valid locations, but it still cannot judge whether the support quality is good enough.
- The guide-layer pages `wiki/index.md`, `wiki/overview.md`, `wiki/hot.md`, and `wiki/log.md` are not yet checked systematically and could silently drift over time.

## Scope / 范围

- 为 `entity / concept / synthesis` 增加更强的 `source_refs` 质量检查
- 为重复 / 自指的 `source_refs` 与 `related` 增加 lint
- 为 guide-surface 页面增加健康检查
- 补测试、双语文档和验证

- Add stronger `source_refs` quality checks for `entity / concept / synthesis`
- Add lint for duplicate or self-referential `source_refs` and `related`
- Add health checks for guide-surface pages
- Add tests, bilingual docs, and verification
