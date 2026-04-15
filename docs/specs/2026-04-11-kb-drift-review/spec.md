# Spec / 规格

## Goals / 目标

- 让 `knowledge-base` 有一个独立的 drift review 入口，用来识别“需要人工复核”的页面，而不是把这些信号全塞进 `maintain`。
- Give `knowledge-base` a dedicated drift-review entry point for identifying pages that may need human review instead of forcing all such signals into `maintain`.

- 让 drift review 同时适合 CLI 阅读、脚本消费和 report 留档。
- Make drift review suitable for CLI reading, script consumption, and report archival at the same time.

## Non-Goals / 非目标

- 不自动修复 drift
- 不重写 canonical 页内容
- 不把 drift signal 直接当成维护失败

- Do not auto-fix drift
- Do not rewrite canonical page content
- Do not treat drift signals as direct maintenance failures

## Functional Rules / 功能规则

- 新增 `drift-review` 子命令及 `drift` 别名
- drift review 至少识别这些 signals：
  - `source-lag`
  - `guide-lag`
  - `metadata-lag`
  - `report-lag`
- 输出 `drift_verdict`
- 支持 `--json`
- 支持 `--write-report`
- drift review 默认返回 0，不把“需要复核”视为命令失败

- Add a `drift-review` subcommand with the `drift` alias
- The drift review recognizes at least these signal types:
  - `source-lag`
  - `guide-lag`
  - `metadata-lag`
  - `report-lag`
- Return `drift_verdict`
- Support `--json`
- Support `--write-report`
- Return 0 by default so “needs review” is not treated as a command failure
