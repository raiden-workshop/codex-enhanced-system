# Output Budget Policy

## 1. Purpose

本策略吸收 `rtk` 的输出压缩思想，但不安装 `rtk`，不启用全局 hook，也不透明改写命令。

目标是减少上下文污染，同时保留足够证据让调试和验证可信。

## 2. Non-Goals

- 不执行 `rtk init --global`。
- 不安装 Codex hook。
- 不安装 shell hook。
- 不替换 `git`、`npm`、`pytest`、`cargo` 等命令。
- 不吞掉失败输出。
- 不把压缩摘要当作唯一证据。

## 3. Default Rules

运行可能产生长输出的命令前，先选择窄口径：

- `git status --short --branch`
- `git diff --stat`
- `git diff -- <path>`
- `git log --oneline -n <n>`
- 只跑 touched files 或 touched modules 的测试
- 先跑 typecheck / lint / unit 的最窄有效检查

当输出仍然很长：

- 摘要写入对话。
- 原始输出保留在终端或日志文件中。
- 失败时优先保留错误块、文件路径、行号、断言、stderr 和退出码。
- 不为了省 token 删除可定位根因的信息。

## 4. Evidence Contract

任何压缩后的验证记录都必须说明：

- 原命令是什么。
- 是否通过。
- 失败时关键错误是什么。
- 原始输出在哪里还能追溯。
- 是否有未运行检查。

推荐格式：

```text
command: <exact command>
status: pass | fail | not-run
summary: <short result>
evidence: <terminal output, log path, or captured excerpt>
missing: <checks not run and why>
```

## 5. Safe Wrapper Path

如果后续需要工具化，只允许从显式 wrapper 开始：

```text
codex command
-> explicit wrapper
-> raw command
-> raw log saved
-> compact summary printed
```

wrapper 约束：

- 必须由用户或 agent 明确调用。
- 默认不接管 shell。
- 默认不改写原始命令。
- 必须保留原始日志。
- 遇到解析失败时输出原始命令结果。

## 6. Forbidden Paths

禁止在本仓库方案里默认采用：

- 全局 shell alias。
- 全局 command rewrite hook。
- 后台常驻输出代理。
- 未经确认的 Codex lifecycle hook 安装。
- 只显示摘要、不保留原文的压缩器。

