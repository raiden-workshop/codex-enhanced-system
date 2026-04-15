# Spec / 规格

## Goals / 目标

- 让 `kb drift-review --write-report` 产出的报告反映写入后的最终状态，而不是写入前的瞬时状态。
- Ensure that `kb drift-review --write-report` archives the final post-write state rather than a transient pre-write state.

- 保持 `drift-review` 的检测逻辑不变，只修正 report 写入语义。
- Keep the `drift-review` detection logic unchanged and only correct the report writeback semantics.

## Non-Goals / 非目标

- 不新增 drift signal 类型
- 不修改 `maintain` 的行为
- 不在真实仓库里额外生成多余的 drift report 只为了验证

- Do not add new drift signal types
- Do not change `maintain`
- Do not generate extra drift reports in the live repository only for verification

## Functional Rules / 功能规则

- `drift-review --write-report` 的归档内容应等价于“写入后再次观察到的状态”
- 因为写入新 report 会解决 `report-lag`，归档报告不应继续记录这条已被自身解决的信号
- 命令在真实仓库上的文本/JSON摘要也应与写入后的状态保持一致
- `--dry-run` 继续只做路径与摘要预览，不实际改动仓库

- The archived result of `drift-review --write-report` should be equivalent to the state observed after the write
- Because a fresh report resolves `report-lag`, the archived report should not keep recording that self-resolved signal
- The command's real text/JSON summary should also stay aligned with the post-write state
- `--dry-run` remains a non-mutating preview of the path and summary
