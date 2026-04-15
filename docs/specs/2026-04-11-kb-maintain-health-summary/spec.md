# Spec / 规格

## Goals / 目标

- `maintain` 的人类输出能够让用户一眼看出当前是 `healthy`、`needs-attention` 还是 `failing`。
- The human-oriented `maintain` output should make it obvious at a glance whether the current state is `healthy`, `needs-attention`, or `failing`.

- `maintain --json` 和 generated report 都能表达 issue category 与 recommendation，而不是只有平铺列表。
- `maintain --json` and the generated report should express issue categories and recommendations instead of only a flat list.

## Non-Goals / 非目标

- 不新增维护规则本身
- 不做自动修复
- 不引入新的独立 drift 子命令

- Do not add new maintenance rules themselves
- Do not perform automatic fixes
- Do not introduce a separate drift subcommand

## Functional Rules / 功能规则

- 维护输出新增 `health_verdict`
- issue 至少分为：`provenance`、`guide-surface`、`frontmatter`、`links`、`index`、`general`
- JSON 输出新增 `issue_groups` 与 `recommendations`
- 文本输出显示 `health_verdict`、`issue_groups`，并在 issue 行中显示 category
- generated report 新增 `Issue Summary`、`Findings By Category` 和按类别生成的 recommendation

- Maintenance output adds `health_verdict`
- Issues are categorized into at least: `provenance`, `guide-surface`, `frontmatter`, `links`, `index`, and `general`
- JSON output adds `issue_groups` and `recommendations`
- Text output shows `health_verdict`, `issue_groups`, and includes the category on each issue line
- The generated report adds `Issue Summary`, `Findings By Category`, and category-aware recommendations
