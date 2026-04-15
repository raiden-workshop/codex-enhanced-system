# Plan Review / 计划复核

## Review / 复核

- 方案把 drift 视为“review signal”而不是“hard failure”，更符合知识库治理的实际语义。
- heuristics 都依赖现有 frontmatter 与引用图，不需要额外数据库或状态层。
- 当前仓库本身就存在近期 source 更新，因此这套命令很可能一落地就能产出真实信号。

- The plan treats drift as a review signal rather than a hard failure, which better matches the real semantics of knowledge-base governance.
- The heuristics rely only on existing frontmatter and the reference graph, so they do not require extra databases or state layers.
- The current repository already contains recent source updates, so the command is likely to produce real signals immediately after landing.
