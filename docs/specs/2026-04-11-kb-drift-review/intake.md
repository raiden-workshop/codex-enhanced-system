# Intake / 需求摄取

## Request / 请求

- 用户继续要求推进代码实现。
- The user asked to continue advancing the implementation.

## Problem / 问题

- `maintain` 现在已经能给健康结论，但它仍然以“维护错误/告警”为主视角。
- 对于“支持页后来更新了、导航页可能落后了、report 层整体偏旧了”这类信号，更适合单独做 drift review，而不是混进硬错误检查里。

- `maintain` can now provide a health verdict, but it still looks at the world mainly through maintenance errors and warnings.
- Signals such as “support pages were updated later,” “guide pages may be lagging,” or “the report layer is overall older” fit a dedicated drift review better than they fit hard maintenance errors.

## Scope / 范围

- 新增 `kb drift-review` / `kb drift`
- 输出 drift verdict、signal counts、signal groups、recommendations
- 支持 JSON 和 report 写入
- 补测试和双语文档

- Add `kb drift-review` / `kb drift`
- Return a drift verdict, signal counts, signal groups, and recommendations
- Support JSON and report writing
- Add tests and bilingual docs
