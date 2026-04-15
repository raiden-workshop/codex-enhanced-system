# Spec / 规格

## Goals / 目标

- 让先前的 drift signals 在内容层得到真实响应，而不是只通过忽略或降级处理。
- Ensure the previous drift signals receive a real content-level response rather than being merely ignored or downgraded.

- 让 `drift-review` 在当前仓库上重新回到 `stable`，同时保持 `maintain` 为 `healthy`。
- Bring `drift-review` back to `stable` on the current repository while keeping `maintain` at `healthy`.

## Non-Goals / 非目标

- 不扩展新的 drift heuristics
- 不扩大领域范围
- 不改 query / maintain 的接口契约

- Do not expand the drift heuristics
- Do not widen the domain scope
- Do not change the `query` / `maintain` interface contracts

## Functional Rules / 功能规则

- 只有在 newer source 提供了稳定新增信息时，才刷新 canonical 页内容
- guide 页刷新要同时更新导航入口，不做纯时间戳漂白
- drift review report 应反映最终当前状态，而不是停留在“写入前”的瞬时残余信号
- 最终状态要求：
  - `kb drift-review` -> `stable`
  - `kb maintain` -> `healthy`

- Refresh canonical page content only when newer sources add stable information
- Refresh guide pages together with their navigation entry points instead of performing timestamp-only whitening
- The drift-review report should reflect the final current state instead of a transient pre-write residual signal
- Final-state requirements:
  - `kb drift-review` -> `stable`
  - `kb maintain` -> `healthy`
