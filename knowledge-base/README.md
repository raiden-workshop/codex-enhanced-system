# Knowledge Base Workspace

这是一个独立的 `knowledge-base` worker space。

它已经从 `mult-agent/knowledge-base` 迁出，并升级为一个跨项目知识库的根 workspace。
旧的 `mult-agent/knowledge-base` 路径现在只表示历史 seed 来源，不再是正式工作目录。

当前定位：

- 阶段：`v1`
- 模式：跨项目知识库外壳 + 当前 1 个 founding domain
- founding domain：`Codex-native memory governance`
- 作用：承载跨项目知识与当前已落地领域的原始资料、正式知识层和轻治理层
- 边界：补充全局 memory system，而不是替代它

当前原则：

- `raw/` 放原始资料
- `wiki/` 放正式知识
- `wiki/domains/` 放领域注册页
- `wiki/hot.md` 放热路径导航，不单独构成正式事实
- `wiki/reports/` 放轻量治理与健康检查结果
- `output/` 放临时导出结果
- 默认只有 knowledge worker 写 `wiki/`
- 当前阶段只引入轻量 `hot.md` 与 `wiki/reports/`，其余 `v1.5` 治理层继续延后

当前已纳入的 seed 来源：

- `codex-memory-kit` 仓库 `README`
- `docs/README.md`
- `docs/raiden-lab-repository-map.md`
- `docs/raiden-lab-naming-convention.md`
- `oh-my-codex Memory Integration Executive Summary`
- `ADR-001: oh-my-codex 接入当前记忆系统的权威边界`
- `oh-my-codex Memory Integration Specification`
- `oh-my-codex 与当前记忆系统集成设计`
- `oh-my-codex 与当前记忆系统集成开发计划`
- `oh-my-codex Upstream Review Summary`
- `oh-my-codex Verification Evidence Gate Design`
- `oh-my-codex Upstream First Integration Status`
- `oh-my-codex Memory Integration Review Checklist`
- `oh-my-codex Upstream First Integration Apply Guide`
- `oh-my-codex Upstream Review Notes`

当前正式知识页：

- `wiki/sources/`: 15 个来源页
- `wiki/entities/`: `codex-memory-kit`, `oh-my-codex`
- `wiki/concepts/`: 治理层定位、strict integration mode、formal memory authority、verification evidence gate
- `wiki/syntheses/`: 3 个综合页，覆盖领域基线、upstream rollout、reviewer packet
- `wiki/domains/`: 1 个领域注册页，记录当前 founding domain
- `wiki/hot.md`: 新 worker 的短热路径入口
- `wiki/reports/`: 3 个轻量报告，覆盖 lint、source priority 与跨项目扩域准入判断

新 worker 进入本目录后，先读：

1. `AGENTS.md`
2. `START_HERE.md`
3. `wiki/hot.md`
4. `wiki/domains/domain-codex-native-memory-governance.md`
5. `wiki/index.md`
6. `wiki/overview.md`
7. `wiki/reports/`
8. `wiki/log.md`

协作与提交流程见：

- `CONTRIBUTING.md`

如果需要实施完整知识库项目，设计总文档在：

- `<legacy-worker-root>/docs/knowledge-base-system-design-and-execution-plan.md`
