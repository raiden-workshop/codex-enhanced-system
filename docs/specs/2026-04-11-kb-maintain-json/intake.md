# Intake / 需求摄取

## Request / 请求

- 用户要求在做完 provenance lint 与健康检查后继续写代码。
- The user asked to keep coding after provenance lint and health checks were completed.

## Problem / 问题

- 现在 `kb maintain` 虽然能输出更强的健康检查结果，但默认仍只有文本摘要。
- 查询已经有 `--json`，维护命令还没有同等级的结构化出口，不利于后续 automation 和程序化消费。

- `kb maintain` now returns stronger health-check results, but it still only emits a text summary by default.
- Query already has `--json`, while maintenance has no equivalent structured output yet, which makes later automation and programmatic consumption harder.

## Scope / 范围

- 为 `kb maintain` 增加 `--json`
- 输出 `counts`、`issue_counts`、`issues`
- 在 `--write-report` 场景下补 `report_path` 与 `report_action`
- 补测试与双语文档

- Add `--json` to `kb maintain`
- Return `counts`, `issue_counts`, and `issues`
- Add `report_path` and `report_action` when `--write-report` is in play
- Add tests and bilingual docs
