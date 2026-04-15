# Intake / 需求摄取

## Request / 请求

- 用户继续要求推进代码实现。
- The user asked to continue pushing the implementation forward.

## Problem / 问题

- `maintain` 已经能输出结构化结果，但还不够“可读即判断”。
- 现在用户或后续 automation 还要自己解释每条 issue 属于哪类问题、整体健康处于什么状态、下一步应该先修什么。

- `maintain` already returns structured data, but it is not yet “readable enough to judge immediately.”
- A user or later automation still has to infer what kind of issue each item represents, what the overall health state is, and what should be fixed first.

## Scope / 范围

- 给维护结果增加 `health_verdict`
- 按类别归组 issue
- 生成建议列表
- 把这些信息同步到文本、JSON 和 report 输出

- Add `health_verdict` to maintenance results
- Group issues by category
- Generate recommendation lists
- Sync those signals into text, JSON, and report output
