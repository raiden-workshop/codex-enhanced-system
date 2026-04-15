# Workflow Health Check

## 1. 目的

workflow health check 用于判断一套 `method-forge` 流程是否还在健康运行，而不是只检查文件是否存在。

## 2. 何时检查

推荐在以下时点做一次：

- 一个里程碑结束后
- 引入新 worker 或新 workspace 时
- 连续出现 plan 漂移或 verify 失败时
- 准备从 `v1` 升级到 `v1.5+` 时

## 3. 健康信号

### 3.1 入口健康

- 非闲聊请求是否都先经过 `intake`
- `need_spec` 判定是否稳定
- 轻任务是否没有被过度流程化

### 3.2 文档流健康

- `spec -> plan -> review -> tasks -> verify` 是否仍按顺序执行
- 是否出现平行真相源
- 是否出现长期未关闭的 `open_questions`

### 3.3 质量门健康

- `plan-review` 是否真的拦住了问题，而不是永远 `approved`
- `verify` 是否记录了真实测试证据，而不是模板化空话
- 高风险改动是否在需要时引入 `code-review`

### 3.4 记忆边界健康

- `verify.md` 是否只提出 memory candidate，不直接写 memory
- `memory-candidate.md` 是否只整理稳定结论
- 是否把一次性分析误晋升为长期规则

### 3.5 术语健康

- 是否仍统一使用 `orchestrations`
- 是否有人把会话内流程重新叫成 `automations`

## 4. 轻量检查方法

1. 抽查最近一组变更文档包。
2. 检查 `intake/spec/plan/plan-review/tasks/verify` 是否成链。
3. 检查 `verify` 是否有测试与风险证据。
4. 检查是否有孤立的文档草稿或未回收失败分支。
5. 检查 memory candidate 是否谨慎。

## 5. 触发修复的信号

- 同一类请求在不同 worker 手里走出不同主流程
- `plan-review` 长期没有实质 findings
- `verify.md` 经常只写“已完成”
- memory candidate 经常是一次性结论
- 文档命名开始出现 `final-v2-latest`

## 6. 输出建议

健康检查至少给出：

- overall_status
- strongest_signal
- weakest_signal
- actions

推荐输出到 `workflow-health-report.md`。

当前已提供：

- 模板：[docs/templates/workflow-health-report-template.md](../templates/workflow-health-report-template.md)
- 样例：[docs/method/examples/health-check/workflow-health-report.md](examples/health-check/workflow-health-report.md)
