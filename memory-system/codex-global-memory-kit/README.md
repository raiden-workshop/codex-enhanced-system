# Codex Global Memory System Kit

如果你是 Codex，请读取本 README，并把这套记忆系统安全地安装或升级到目标 Codex App。

这个包可以放在任意位置。

## 目标

- 只安装或升级记忆系统脚手架
- 不导入作者机器上的任何具体记忆
- 不覆盖目标 Codex App 里已有的记忆内容
- 让新开的 worker 默认启用这套全局记忆系统

## 默认目标

- `CODEX_HOME`：默认 `~/.codex`
- `TARGET_WORKSPACE`：默认当前工作区

如果用户明确给了别的 Codex home 或 workspace 路径，以用户提供的路径为准。

## 严格禁止覆盖的内容

不要删除、覆盖或清空这些路径里的现有内容：

- `CODEX_HOME/memory/global/memories/`
- `CODEX_HOME/memory/global/candidates/`
- `CODEX_HOME/memory/global/candidates_archive/`
- `CODEX_HOME/memory/workspaces/`
- `CODEX_HOME/memory/runs/`
- `CODEX_HOME/sessions/`
- `CODEX_HOME/archived_sessions/`
- `CODEX_HOME/*.sqlite`
- `CODEX_HOME/.codex-global-state.json`

也不要删除目标工作区里已经存在的旧记忆系统目录。旧内容先保留，除非用户明确要求清理。

## 允许的升级动作

只允许做这些安全动作：

1. 创建缺失目录
2. 复制缺失模板文件
3. 合并 `CODEX_HOME/AGENTS.md` 里的记忆护栏，如果已有同类段落则不要重复追加
4. 升级 `CODEX_HOME/scripts/refresh_memory.py`
   这是系统代码，可以直接替换为本包模板版本
5. 合并 `CODEX_HOME/memory/global/config.json`
   只补缺失键，不覆盖目标机器已有值
6. 可选地把工作区模板写入 `TARGET_WORKSPACE`
   只在文件缺失时创建；已有文件只补充缺失的记忆系统段落，不整体覆盖

## 不要自动做的事

- 不要自动初始化旧 sessions
- 不要自动运行 `--force`
- 不要自动清理旧记忆文件
- 不要自动删除 legacy 本地记忆目录

如果用户只是让你“安装/升级记忆系统”，做到脚手架安装为止就停。

只有用户明确要求“初始化当前 workspace 记忆”时，才运行：

```bash
python3 CODEX_HOME/scripts/refresh_memory.py --workspace-root TARGET_WORKSPACE
```

## 可选初始化问答

安装完成后，可以额外做一次“第①层 company + 第②层 user”的初始化。

这一步默认不执行。

只有当使用者明确说：

- 要初始化这两层
- 或接受默认答案写入这两层

你才可以把下面的问答结果写入：

- `CODEX_HOME/memory/instructions/company/GUIDE.md`
- `CODEX_HOME/memory/instructions/user/GUIDE.md`

如果使用者没有明确确认，就只展示这些问题和默认答案，不要落盘。

### 初始化执行规则

1. 先问使用者要不要做 `company` 层初始化
2. 再问要不要做 `user` 层初始化
3. 对每一层，允许三种选择：
   - 接受全部默认答案
   - 修改部分答案
   - 整层跳过
4. 如果目标文件已经有内容，不要整体覆盖
   - 只在使用者确认后，追加一个新的 `Initialization Answers` 段落
   - 或按使用者要求合并

### Company 初始化问题与默认答案

#### C1 长期记忆总原则

问题：这套 Codex 的长期记忆总原则是什么？

默认答案：长期记忆必须文件化、可读、可改、可 diff；只记录稳定、可复用、对后续协作有帮助的信息。

#### C2 禁止进入长期记忆的内容

问题：哪些内容绝不能进入长期记忆？

默认答案：一次性任务要求、临时猜测、寒暄、纯过程噪音、未经确认的偏好、敏感凭证。

#### C3 时间写法

问题：时间信息怎么写？

默认答案：一律优先绝对时间，如 `2026-04-03`，避免“今天”“明天”“下周四”。

#### C4 反馈记忆原则

问题：反馈记忆记录原则是什么？

默认答案：同时记录纠正和确认；不要只记“做错了什么”，也要记“什么做法被明确认可”。

#### C5 记忆写入流程

问题：记忆写入流程是什么？

默认答案：先写候选，再 promotion；不要直接把新信息写成长期真相。

#### C6 多层记忆优先级

问题：多层记忆的优先级是什么？

默认答案：近处优先：当前任务/运行态 > workspace > global。

#### C7 哪些作用域允许保存正式长期记忆

问题：哪些作用域允许保存正式长期记忆？

默认答案：只允许 `global` 和 `workspace` 保存正式长期记忆，`worker-run` 只保存临时态。

#### C8 冲突记忆处理

问题：冲突记忆怎么处理？

默认答案：冲突先进入 conflict queue，不直接写成 active truth；不要并存两条互相矛盾的 active 规则。

#### C9 Global 层职责

问题：Global 层应该保存什么？

默认答案：只保存跨项目稳定成立的用户偏好、全局反馈和通用 reference，不保存项目事实。

#### C10 Workspace 层职责

问题：Workspace 层应该保存什么？

默认答案：保存项目事实、项目反馈、项目 reference、open loops。

#### C11 历史迁移原则

问题：历史迁移的原则是什么？

默认答案：旧记忆可以迁移，但默认保守，不把复制出来的历史误判为跨项目共识。

#### C12 候选层治理原则

问题：候选层治理原则是什么？

默认答案：promoted、duplicate、expired、overflow 的 candidate 要归档，不允许无限膨胀。

#### C13 Dream 的职责

问题：Dream 的职责是什么？

默认答案：Dream 是治理器，不是堆积器；负责去重、降级、纠偏、修剪、更新热路径。

#### C14 Runtime 热路径目标

问题：Runtime 热路径的目标是什么？

默认答案：给新 worker 一个短、小、可执行的上下文，不让它直接扫全库。

#### C15 新 worker 默认读取顺序

问题：新 worker 默认应先读什么？

默认答案：先读共享 Guide，再读 global context，再读 workspace guide 和 workspace active context。

#### C16 刷新时机

问题：什么时候刷新记忆系统？

默认答案：完成重要工作后刷新；不要为每一句闲聊都刷新。

#### C17 自动提升到 global 的条件

问题：什么时候允许自动提升到 global？

默认答案：只有用户明确说全局适用，或跨多个 workspace 重复成立时才允许。

#### C18 必须人工确认的情况

问题：什么时候必须人工确认？

默认答案：涉及范围不清、冲突、敏感信息、可能覆盖旧规则时。

### User 初始化问题与默认答案

#### U1 主要工作台

问题：你主要用哪个 AI 工作台？

默认答案：默认以当前 Codex App 为主工作台，尽量少切换工具。

#### U2 偏好的工作方式

问题：你更偏好什么工作方式？

默认答案：偏好直接、低摩擦、少折腾的流程，优先可立即执行的方案。

#### U3 多种实现路径时怎么选

问题：遇到多种实现路径时，默认怎么选？

默认答案：默认优先最简单、最稳定、最少额外依赖的方案。

#### U4 不确定时的处理方式

问题：你希望 AI 在不确定时怎么做？

默认答案：先做合理假设继续推进；只有存在明显风险时再停下来确认。

#### U5 默认工作节奏

问题：你偏好 AI 先讲计划还是直接动手？

默认答案：默认先设计，对齐设计文档和开发文档，再动手。

#### U6 解释深度偏好

问题：你偏好长解释还是短结论？

默认答案：默认短结论、高信息密度；需要时再展开。

#### U7 输出风格

问题：你对输出风格的偏好是什么？

默认答案：偏好结构清晰、少废话、可直接执行的表达。

#### U8 代劳程度

问题：你更喜欢命令式建议还是让 AI 代劳？

默认答案：默认由 AI 直接完成，不把明显可执行的工作再推回给你。

#### U9 网页检查方式

问题：对网页检查或页面调试，默认用什么方式？

默认答案：用户明确要求时，优先使用 Chrome CDP。

#### U10 安装升级产物

问题：对安装/升级类任务，默认产物是什么？

默认答案：优先 README 驱动说明，不默认生成 `install.sh`。

#### U11 对长期记忆的期望

问题：你对“长期记忆”的期望是什么？

默认答案：希望长期记忆稳定、可复用、别乱记一次性要求。

#### U12 对自动化的偏好

问题：你对自动化的偏好是什么？

默认答案：自动化可以做，但默认安静、保守、可审查，不要乱改已有状态。

#### U13 文件修改偏好

问题：你对文件修改的偏好是什么？

默认答案：尽量小改、定点改、不要无关重写。

#### U14 对 review 的期望

问题：你对 review 的期望是什么？

默认答案：先讲问题和风险，再讲总结；不要只给泛泛好评。

#### U15 对测试的期望

问题：你对测试的期望是什么？

默认答案：改代码后尽量跑可行验证，并明确说明哪些没验证。

#### U16 新旧规则冲突时怎么处理

问题：你对记忆覆盖旧规则的偏好是什么？

默认答案：新规则若明确替代旧规则，以新规则为准，但要保留可审查痕迹。

#### U17 跨项目共享偏好的态度

问题：你对多项目共享偏好的态度是什么？

默认答案：跨项目稳定偏好可以进 global；项目特例不要污染 global。

#### U18 提问方式偏好

问题：你对问题收集方式的偏好是什么？

默认答案：先问最少必要问题，不要一次抛很多开放题。

#### U19 AI 的默认节奏

问题：你对 AI 的默认节奏偏好是什么？

默认答案：持续推进，阶段性同步，不要频繁停下来。

#### U20 记忆质量优先级

问题：你对“记不住事”的容忍边界是什么？

默认答案：宁可少记但记准，也不要多记乱记。

## 从本包复制哪些文件

复制或合并这些模板：

- `templates/codex/AGENTS.md` -> `CODEX_HOME/AGENTS.md`
- `templates/codex/scripts/refresh_memory.py` -> `CODEX_HOME/scripts/refresh_memory.py`
- `templates/codex/memory/README.md` -> `CODEX_HOME/memory/README.md`
- `templates/codex/memory/instructions/company/GUIDE.md` -> `CODEX_HOME/memory/instructions/company/GUIDE.md`
- `templates/codex/memory/instructions/user/GUIDE.md` -> `CODEX_HOME/memory/instructions/user/GUIDE.md`
- `templates/codex/memory/instructions/local/GUIDE.md` -> `CODEX_HOME/memory/instructions/local/GUIDE.md`
- `templates/codex/memory/global/config.json` -> merge into `CODEX_HOME/memory/global/config.json`

可选的工作区模板：

- `templates/workspace/AGENTS.md` -> `TARGET_WORKSPACE/AGENTS.md`
- `templates/workspace/WORKSPACE_GUIDE.md` -> `TARGET_WORKSPACE/WORKSPACE_GUIDE.md`

写入工作区模板前，把里面的 `__WORKSPACE_ROOT__` 占位符替换成真实 workspace 绝对路径。

## 合并规则

### `CODEX_HOME/AGENTS.md`

- 如果文件不存在，直接从模板创建
- 如果文件已存在：
  - 保留原内容
  - 只在缺少 `Global Codex Memory Guardrails` 段落时追加模板段落
  - 不要重复追加

### `CODEX_HOME/memory/global/config.json`

- 如果文件不存在，直接从模板创建
- 如果文件已存在，只补模板里缺失的键
- 目标机器已有值优先，不要用模板覆盖

### `TARGET_WORKSPACE/AGENTS.md`

- 如果文件不存在，直接从模板创建
- 如果文件已存在，只在缺少 `Workspace Memory Bridge` 段落时追加相关段落

### `TARGET_WORKSPACE/WORKSPACE_GUIDE.md`

- 如果文件不存在，直接从模板创建
- 如果文件已存在，不整体覆盖
- 只有当文件里完全没有全局记忆系统说明时，才追加简短段落

## 安装后检查

确认这些文件存在：

- `CODEX_HOME/AGENTS.md`
- `CODEX_HOME/scripts/refresh_memory.py`
- `CODEX_HOME/memory/README.md`
- `CODEX_HOME/memory/instructions/company/GUIDE.md`
- `CODEX_HOME/memory/instructions/user/GUIDE.md`
- `CODEX_HOME/memory/instructions/local/GUIDE.md`
- `CODEX_HOME/memory/global/config.json`

如果创建了工作区模板，再确认：

- `TARGET_WORKSPACE/AGENTS.md`
- `TARGET_WORKSPACE/WORKSPACE_GUIDE.md`

最后只汇报：

- 创建了哪些文件
- 合并了哪些文件
- 明确保留了哪些原有记忆内容未被覆盖

然后停止。
