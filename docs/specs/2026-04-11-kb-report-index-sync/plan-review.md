# Plan Review / 计划复核

## Review / 复核

- 这是一个 command writeback closeout 问题，最合适的修法是共享一个小型 index registration helper，而不是把逻辑散落到各个命令里。
- 通过测试夹具覆盖真实写入，可以验证写后健康状态，同时避免为了验证在真实仓库里新增无意义 report。
- 文档需要同步说明“`--write-report` 不只写 report，也会把 report 纳入 index”，否则行为变化会很隐蔽。

- This is a command writeback closeout problem, so the best fix is a small shared index-registration helper rather than duplicating logic across commands.
- Covering the real write path in tests verifies the post-write healthy state without creating meaningless extra reports in the live repository.
- The docs should explicitly say that `--write-report` not only writes a report but also registers it in the index, otherwise the behavior change stays too implicit.
