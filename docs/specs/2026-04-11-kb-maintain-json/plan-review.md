# Plan Review / 计划复核

## Review / 复核

- 方案没有重做一套新维护接口，而是在现有 `maintain` 上补结构化出口，变更面小。
- 通过共享 payload/renderer，可以避免文本输出和 JSON 输出逻辑漂移。
- report 元信息只在相关场景出现，避免默认输出膨胀。

- The plan does not rebuild maintenance as a new interface; it adds a structured exit to the existing `maintain` command, keeping the change surface small.
- Shared payload and renderer helpers avoid drift between text and JSON output.
- Report metadata appears only when relevant, which keeps the default output compact.
