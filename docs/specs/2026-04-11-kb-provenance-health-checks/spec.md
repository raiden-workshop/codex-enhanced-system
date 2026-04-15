# Spec / 规格

## Goals / 目标

- `kb maintain` 不仅能发现引用断裂，还能发现“canonical answer 页只靠 raw 支撑”的弱 provenance。
- `kb maintain` should detect not only broken references, but also weak provenance where canonical answer pages rely only on raw support.

- `kb maintain` 能在导航层页面漂移前发出提醒。
- `kb maintain` should warn before guide-surface pages drift too far.

## Non-Goals / 非目标

- 不做自动修复 wiki 页面
- 不引入定时健康检查 automation
- 不实现完整的 page-evolution 状态机

- No automatic wiki-page repair
- No scheduled health-check automation
- No full page-evolution state machine

## Functional Rules / 功能规则

- `entity / concept / synthesis` 页面若 `source_refs` 没有任何 `wiki/sources/` 支撑页，则发出 warning。
- `source_refs` 与 `related` 若出现重复目标或自指目标，则发出 warning。
- `index / overview / hot / log` 四个 guide-surface 页面必须存在，并拥有基本 frontmatter、可解析链接和关键互链。
- `overview` 必须继续覆盖至少一个 `domain` 与 `report` 入口。
- `hot` 必须继续覆盖至少一个 `domain`、`synthesis`、`report` 入口。

- Emit a warning when an `entity / concept / synthesis` page has `source_refs` but none of them point to `wiki/sources/`.
- Emit a warning when `source_refs` or `related` contain duplicate or self-referential targets.
- Require the four guide-surface pages `index / overview / hot / log` to exist with basic frontmatter, resolvable links, and key cross-links.
- Require `overview` to keep at least one `domain` and one `report` entry point.
- Require `hot` to keep at least one `domain`, `synthesis`, and `report` entry point.
