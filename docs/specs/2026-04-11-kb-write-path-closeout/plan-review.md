# Plan Review / 计划复核

## Review / 复核

- 这些都属于“写入后还差半步”的 closeout 问题，优先修命令写入路径最合适。
- `cmd_add` 自动补 index 与前面 report 写入链路保持一致，能减少最常见的低摩擦残留。
- `--write-log` 作为可选增强，比直接改成默认更稳，兼顾自动流程和手工使用体验。
- 用单元测试覆盖真实写入语义，再用 live repo 命令做 dry-run 验证，可以避免不必要的真实内容扰动。

- These cases are all “one more step is still missing after write” closeout problems, so fixing the command write paths is the right first move.
- Auto-registering `cmd_add` in the index keeps it consistent with the earlier report-write path and removes a common low-friction residue.
- Optional `--write-log` is safer than forcing a new default, because it supports automated flows without making manual usage heavier.
- Covering real write semantics in unit tests and using dry-run checks in the live repo avoids unnecessary content churn.
