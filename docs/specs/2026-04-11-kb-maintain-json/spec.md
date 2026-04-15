# Spec / 规格

## Goals / 目标

- 让 `kb maintain` 的结果可以被脚本稳定读取，而不必解析人类文本输出。
- Let scripts read `kb maintain` results reliably without scraping the human-oriented text output.

- 保持现有文本输出不退化，同时让 `--write-report` 的副作用可见。
- Preserve the current text output while making `--write-report` side effects visible.

## Non-Goals / 非目标

- 不改变维护检查规则本身
- 不引入新的 maintenance 子命令
- 不做自动 report 上传或调度

- Do not change the maintenance rules themselves
- Do not add a new maintenance subcommand
- Do not add automatic report upload or scheduling

## Functional Rules / 功能规则

- `kb maintain --json` 返回：
  - `status`
  - `counts`
  - `issue_counts`
  - `issues`
- 若同时指定 `--write-report`，则额外返回 `report_path` 与 `report_action`
- 普通文本输出继续保留，并在有 issue 时展示聚合的 `issue_counts`

- `kb maintain --json` returns:
  - `status`
  - `counts`
  - `issue_counts`
  - `issues`
- When `--write-report` is also requested, the output additionally returns `report_path` and `report_action`
- The normal text output stays intact and now also shows aggregated `issue_counts` when issues exist
