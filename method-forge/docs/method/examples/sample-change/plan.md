# Plan

## Architecture

- 用根 `README.md` 负责入口导航，用 `docs/method/orchestration-rules.md` 负责总规则，用 `orchestrations/*/README.md` 负责每条编排的执行说明。

## Data Flow

- 请求先从 `route-request` 进入
- 复杂任务在 `spec-flow` 中产出 `spec.md`、`plan.md`、`plan-review.md`、`tasks.md`
- 实现完成后统一进入 `verify-and-memory`，产出 `verify.md` 和可选 memory candidate

## Touch Points

- files_or_modules:
  - `<repo-root>/method-forge/README.md`
  - `<repo-root>/method-forge/docs/method/orchestration-rules.md`
  - `<repo-root>/method-forge/orchestrations/route-request/README.md`
  - `<repo-root>/method-forge/orchestrations/spec-flow/README.md`
  - `<repo-root>/method-forge/orchestrations/verify-and-memory/README.md`
- docs_to_update:
  - `<repo-root>/method-forge/docs/method/codex-native-boundaries.md`
- external_inputs:
  - 当前环境的 Codex 规则与主方案文档

## Implementation Order

1. 先写总规则文档，避免入口文档和边界文档各自定义流程。
2. 再写 3 个 orchestration 文档，让每条路径都有明确说明。
3. 最后更新根 `README.md`，只做导航，不重复大段规则。

## Risks

- risk: README 与 orchestration 规则重复后容易漂移。
  mitigation: 让 README 只做入口导航，把细则放在方法文档与各 orchestration README。
- risk: 旧资料中 `automations` 一词残留，导致边界被误读。
  mitigation: 在边界文档和流程文档中显式写出术语修正。

## Test Strategy

- unit_or_local_checks: 检查目标文件是否全部存在，且都包含关键段落。
- integration_or_manual_checks: 人工顺读 `README -> route-request -> spec-flow -> verify-and-memory` 是否形成闭环。
- failure_cases_to_cover: 避免任何一处文档把会话内流程重新称为 `automations`。

## Rollout Strategy

- release_or_merge_notes: 文档落地后即可作为 workspace 默认方法层使用。
- rollback_notes: 若某条编排定义错误，优先修订对应文档，不引入第二套流程说明。

## Out Of Scope

- skill 加载器
- workflow 执行引擎
- 自动 memory 晋升
