# Intake / 需求入口

## Request / 请求

- goal: 为当前 consolidated repo 同时补齐 3 件事：真正接上 autonomous heartbeat、补最小 GitHub checks、并完成一次端到端验收。
- goal_en: Complete three things for the consolidated repo in one pass: attach a real autonomous heartbeat, add minimal GitHub checks, and finish an end-to-end validation pass.

## Constraints / 约束

- 不重复实现第二套调度器，继续使用 Codex App 原生 heartbeat automation。
- 只补最小但稳定的 GitHub checks，不引入额外框架。
- 文档需要保持中英文双语。

- Do not rebuild a second scheduler; keep using Codex App native heartbeat automation.
- Add only the smallest stable GitHub checks and avoid introducing extra frameworks.
- Keep new docs bilingual.

## Expected Outcome / 期望结果

- 当前线程存在一个可运行的 heartbeat automation。
- 仓库具备基础 CI，可在 GitHub 上运行知识库测试和健康检查。
- 有一份可追溯的验证记录说明本轮收口结果。

- The current thread has a runnable heartbeat automation.
- The repository has baseline CI for knowledge-base tests and health checks on GitHub.
- A traceable verification record explains the closeout result.
