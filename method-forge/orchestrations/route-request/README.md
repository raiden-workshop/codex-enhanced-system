# route-request

## Purpose

`route-request` 是默认入口 orchestration。

它只做两件事：

- 运行 `method-forge-feature-intake`
- 根据 `intake.md` 把请求送往合适路径

## Inputs

- 用户原始请求
- 当前 workspace 上下文
- `AGENTS.md`
- 必要的 memory / knowledge-base 索引

## Outputs

- `intake.md`
- 一条明确的下一步路径

## Flow

1. 调用 [method-forge-feature-intake](../../skills/method-forge-feature-intake/SKILL.md)。
2. 若 `need_research=true`，先补 research 或 knowledge-base 输入。
3. 若 `need_spec=false`，进入直接实现路径。
4. 若 `need_spec=true`，进入 [spec-flow](../spec-flow/README.md)。
5. 实现完成后统一进入 [verify-and-memory](../verify-and-memory/README.md)。

## Branch Rules

| Condition | Route |
| --- | --- |
| `suggested_path=direct-implement` | 直接实现，再进入 `verify-and-memory` |
| `suggested_path=research-first` | 先 research，再回到 `spec-clarify` 或实现 |
| `suggested_path=spec-flow` | 进入 `spec-flow` |

## Stop Conditions

- 仍无法判断真实目标
- 高风险前提尚未确认
- 依赖信息缺失到无法稳定给出 `next_step`

## Boundaries

- 不直接实现功能
- 不直接写长期 memory
- 不把 research 输出当作最终交付
