# Plan Review / 计划复核

## Review / 复核

- 方案把 drift remediation 分成“内容页刷新”和“导航层收口”两部分，符合当前 signal 的真实来源。
- 通过要求 `drift-review` 回到 `stable`，我们能直接验证这次内容修复是否真的奏效。
- report 自身也要收口，否则会留下“修完以后 report 反而变旧”的假信号。

- The plan splits drift remediation into “canonical content refresh” and “guide-layer closeout,” which matches the real source of the current signals.
- Requiring `drift-review` to return to `stable` gives a direct check that the remediation actually worked.
- The report itself must also be closed out; otherwise it leaves a false signal where the remediation is done but the report is stale.
