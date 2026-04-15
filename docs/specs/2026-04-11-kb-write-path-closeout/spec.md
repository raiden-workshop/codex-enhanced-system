# Spec / 规格

## Goals / 目标

- 让常用 `kb` 写路径在单次写入后就尽量收敛到更健康的状态，而不是依赖额外人工补一步。
- Make common `kb` write paths converge to a healthier state after a single write instead of depending on an extra manual cleanup step.

- 保持当前真实仓库的 `healthy` / `stable` 基线不被打破。
- Preserve the current `healthy` / `stable` baseline of the live repository.

## Non-Goals / 非目标

- 不新增新的 maintenance 或 drift heuristics
- 不把 `--write-log` 变成强制默认行为
- 不扩大 canonical page 模板范围

- Do not add new maintenance or drift heuristics
- Do not turn `--write-log` into a mandatory default behavior
- Do not widen the canonical page template scope

## Functional Rules / 功能规则

- `cmd_log` 的真实写入必须同步刷新 `wiki/log.md.updated_at`
- `cmd_add` 的真实写入必须自动把新 canonical page 补入 `wiki/index.md`
- `cmd_add --write-log` 与 `cmd_delete --write-log` 应能自动补默认结构化日志
- `cmd_add --dry-run` 和 `cmd_log --dry-run` 继续保持无副作用
- `cmd_delete --dry-run` 与 `--write-log` 组合时也必须保持无副作用
- 新逻辑不能打破 `kb maintain` 的 `healthy` 与 `kb drift-review` 的 `stable`

- A real `cmd_log` write must refresh `wiki/log.md.updated_at`
- A real `cmd_add` write must auto-register the new canonical page in `wiki/index.md`
- `cmd_add --write-log` and `cmd_delete --write-log` should be able to append default structured log entries automatically
- `cmd_add --dry-run` and `cmd_log --dry-run` remain side-effect free
- `cmd_delete --dry-run` combined with `--write-log` must also remain side-effect free
- The new logic must not break `kb maintain`'s `healthy` or `kb drift-review`'s `stable`
