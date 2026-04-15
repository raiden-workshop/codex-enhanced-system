# Plan Review / 计划复核

## Review / 复核

- 这个问题属于“写回语义”而不是“检测逻辑”错误，所以应该小范围修补命令路径，而不是重写 drift heuristics。
- 通过测试夹具覆盖“只有 report-lag 的场景”，可以在不污染真实知识库的前提下验证写后稳定行为。
- 用户面文档需要同步更新，否则命令行为变化会只停留在代码层。

- This is a writeback-semantics issue rather than a detector-logic bug, so a focused command-path fix is better than reworking the drift heuristics.
- Covering the “report-lag only” scenario in tests verifies the post-write stable behavior without polluting the live knowledge base.
- The user-facing command docs should be updated as well so the behavior change does not live only in code.
