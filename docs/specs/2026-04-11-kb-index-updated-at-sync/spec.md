# Spec / 规格

## Goals / 目标

- 让所有实际改写 `wiki/index.md` 的主路径都同步刷新它自己的 `updated_at`。
- Ensure that the main paths which actually rewrite `wiki/index.md` also refresh its own `updated_at`.

- 保持当前知识库的 `healthy` / `stable` 基线不被打破。
- Preserve the current `healthy` / `stable` baseline of the knowledge base.

## Non-Goals / 非目标

- 不改 `query`、`maintain`、`drift-review` 的检测逻辑
- 不自动改写 `hot.md`、`overview.md` 或 `log.md`
- 不扩大 index 自动润色范围

- Do not change the detection logic of `query`, `maintain`, or `drift-review`
- Do not automatically rewrite `hot.md`, `overview.md`, or `log.md`
- Do not widen the scope of index auto-polishing

## Functional Rules / 功能规则

- `reindex --write` / `reindex --write --prune` 若实际写入 `wiki/index.md`，必须同步刷新 `updated_at`
- 删除路径若实际移除了 index 条目，也必须同步刷新 `updated_at`
- dry-run 继续保持无副作用
- 新逻辑不能打破 `kb maintain` 的 `healthy` 与 `kb drift-review` 的 `stable`

- If `reindex --write` / `reindex --write --prune` actually writes `wiki/index.md`, it must also refresh `updated_at`
- If the delete path actually removes index entries, it must also refresh `updated_at`
- Dry-run remains side-effect free
- The new logic must not break `kb maintain`'s `healthy` or `kb drift-review`'s `stable`
