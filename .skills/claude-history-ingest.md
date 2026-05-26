---
name: claude-history-ingest
description: 导入 ~/.claude/ 对话历史，提取知识归档到 wiki/
---

# /claude-history-ingest — Claude 对话历史导入

从 `~/.claude/` 下的 Claude Code 对话历史中提取有价值的知识，归档到 `wiki/`，将过去踩过的坑、发现的方案转化为可检索的知识资产。

> **数据安全约束**：对话历史为只读源，不修改任何原始历史文件。导入前必须脱敏。

---

## 前置准备

1. 读取 `ai/_index.json` 确认路由配置
2. 读取 `wiki/index.md` 获取已有概念列表（避免重复创建）
3. 扫描 `~/.claude/history.jsonl` 获取对话摘要索引
4. 扫描 `~/.claude/projects/` 获取项目级对话会话文件列表
5. 如果 `~/.claude/` 不存在或无可读取的对话文件，输出「未找到 Claude 对话历史」并终止

---

## 数据源说明

Claude Code 对话历史存储在以下位置：

| 路径 | 格式 | 内容 |
|------|------|------|
| `~/.claude/history.jsonl` | JSON Lines | 全部会话摘要，每行一个 JSON：`{ display, timestamp, project, sessionId }` |
| `~/.claude/projects/<project>/` | 目录 | 按项目分组的会话目录 |
| `~/.claude/projects/<project>/<sessionId>.jsonl` | JSON Lines | 完整对话记录，每行一个 JSON，含 `type`（human/assistant/tool_use/tool_result）等字段 |

### 会话 JSONL 结构

每行 JSON 包含以下关键字段：

- `type`: 消息类型 — `human`（用户输入）、`assistant`（AI 回复）、`tool_use`（工具调用）、`tool_result`（工具返回）、`attachment`（附件/系统消息）
- `message.content`: 消息内容（文本或内容块数组）
- `timestamp`: ISO 8601 时间戳
- `sessionId`: 会话 ID
- `cwd`: 当前工作目录

---

## Stage 1: Scan（扫描与筛选）

### 1.1 扫描 history.jsonl

读取 `~/.claude/history.jsonl`，逐行解析 JSON：

1. **显示进度**：`Scanning history entries... [当前序号/总数]`
2. 对每个条目提取：`display`（用户意图摘要）、`timestamp`、`project`、`sessionId`
3. 按 `project` 分组统计每个项目的对话数量
4. 输出扫描摘要：
   ```
   扫描完成：共 N 条历史记录，覆盖 M 个项目
   项目列表：
     - project-name-1: K 条记录
     - project-name-2: J 条记录
     ...
   ```

### 1.2 筛选候选会话

根据以下规则筛选值得深度提取的会话：

1. **优先级排序**：按对话内容长度（display 字段丰富度）降序排列
2. **排除规则**：
   - 单条 `display` 少于 10 个字符的简短对话（如"ok"、"yes"、"continue"）
   - 仅包含 skill/plugin 安装类操作的会话
3. **数量控制**：首次导入选取 top 50 个最有价值的会话（后续可增量导入）
4. **显示筛选结果**：`筛选出 P 个候选会话用于深度提取`

---

## Stage 2: Read & Sanitize（读取与脱敏）

对筛选出的每个候选会话，读取完整对话内容并脱敏：

### 2.1 定位会话文件

1. 从 `history.jsonl` 条目中提取 `sessionId` 和 `project` 路径
2. 将 `project` 路径转换为 projects 目录格式（如 `C:\fengjunhuii\mwiki` → `C--fengjunhuii-mwiki`）
3. 拼接完整路径：`~/.claude/projects/<project-dir>/<sessionId>.jsonl`
4. 如果文件不存在，跳过并记录

### 2.2 逐行读取与解析

1. **显示进度**：`Reading session [当前序号/总数] <sessionId 前 8 位>`
2. 逐行读取 JSONL，按 `type` 分类提取内容：
   - `type: "human"` → 提取用户输入（`message.content` 中的文本部分）
   - `type: "assistant"` → 提取 AI 回复（`message.content` 中的文本部分）
   - 忽略 `type: "permission-mode"`、`type: "attachment"` 等系统消息
3. 将多轮对话拼接为连续文本，标记角色：
   ```
   [用户] 显示器上的定时任务有问题...
   [助手] 让我先查看 cron_task.txt...
   [用户] 为什么会有 46 个定时任务？
   [助手] 问题原因是循环创建未正确清理...
   ```

### 2.3 自动脱敏

对提取的文本执行以下脱敏规则（按顺序应用）：

| 规则 | 匹配模式 | 替换为 |
|------|---------|--------|
| API Key | `sk-[a-zA-Z0-9]{20,}` | `[REDACTED_API_KEY]` |
| OpenAI Key | `sk-[a-zA-Z0-9]{40,}` | `[REDACTED_OPENAI_KEY]` |
| Generic Token | `(api[_-]?key\|token\|secret\|password)\s*[:=]\s*['"]?[a-zA-Z0-9_\-]{16,}` | `[REDACTED_$1]` |
| Bearer Token | `Bearer\s+[a-zA-Z0-9_\-\.]{20,}` | `Bearer [REDACTED_TOKEN]` |
| Private IP | `(?:192\.168\|10\.\d+\|172\.(?:1[6-9]\|2\d\|3[01]))\.\d+\.\d+` | `[REDACTED_IP]` |
| Email | `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}` | `[REDACTED_EMAIL]` |
| File path (Windows) | `C:\\Users\\(?!(Administrator\|Default\|Public))[^\\]+` | `C:\\Users\\[REDACTED]` |

脱敏后在 `wiki/log.md` 记录脱敏统计：
```
- **脱敏统计**：会话 <id> — 替换 API Key N 处、Token M 处、其他 P 处
```

---

## Stage 3: Extract（知识提取）

对脱敏后的对话文本提取结构化知识：

### 3.1 知识分类

从对话中识别以下三类知识：

1. **概念（concept）**：技术概念、框架、算法、设计模式
   - 标志：对话中对某技术术语进行了讨论、解释或对比
   - 提取：概念名、定义描述、使用场景

2. **解决方案（solution）**：问题排查、调试过程、修复方案
   - 标志：用户提出问题 → 助手分析原因 → 给出修复方案
   - 提取：问题描述、根因分析、解决步骤、关键代码片段

3. **踩坑记录（pitfall）**：错误、陷阱、注意事项
   - 标志：对话中出现了错误信息、异常行为、意外结果
   - 提取：错误现象、触发条件、规避方法

### 3.2 提取规则

对每个会话：

1. **显示进度**：`Extracting knowledge [当前序号/总数]`
2. 识别对话主题：从用户的首条消息（display）提取核心主题
3. 按知识分类规则逐一提取知识点
4. 每个知识点生成结构化记录：
   ```
   {
     "type": "concept|solution|pitfall",
     "title": "知识点标题",
     "content": "知识点详细内容（≤ 500 字）",
     "tags": ["标签1", "标签2"],
     "source_session": "sessionId",
     "source_project": "项目名",
     "source_timestamp": "YYYY-MM-DD"
   }
   ```
5. 跳过无实质内容的会话（纯闲聊、简单确认等），标记为 `low-yield`

### 3.3 输出中间结果

将所有提取的知识点汇总为知识表（内存数据结构），格式：

```
知识点标题 -> {
  type: "concept|solution|pitfall",
  mentions: [
    { session: "xxx", project: "yyy", content: "...", timestamp: "..." }
  ],
  tags: [...]
}
```

---

## Stage 4: Merge & Write（合并与写入）

### 4.1 概念合并策略

将提取的知识与已有 wiki 内容合并：

1. **已存在同名概念页**（`wiki/concepts/` 下已有）：
   - 在对应章节追加新内容，标注来源为 `claude-history`
   - 格式：在内容末尾追加 `> **来源**：Claude 对话 — 项目/日期`
   - 不覆盖已有内容，不删除已有描述

2. **新概念**（wiki/ 中不存在）：
   - 创建新的 `wiki/concepts/<概念名>.md`（文件名 kebab-case）
   - 按以下 frontmatter 和内容结构生成

3. **冲突处理**：
   - 如果新提取的内容与已有描述矛盾，标记 `^[ambiguous]`
   - 格式：`> Claude 对话记录描述内容 ^[ambiguous]`

### 4.2 概念页 Frontmatter

```yaml
---
title: "概念名"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [从对话内容推断, 2-5 个]
sources: ["claude-history:sessionId"]
summary: "一句话描述（≤ 100 字）"
status: active
entity_type: concept
---
```

**关键**：`sources` 字段必须包含 `claude-history` 前缀，格式为 `claude-history:<sessionId 前 8 位>`，以区分来源于 _raw/ 素材的知识。

### 4.3 概念页内容结构

新建页面按 `templates/concept-template.md` 格式，内容结构：

```markdown
## 定义
从对话中提取的概念定义。

## 核心要点
- 要点 1
- 要点 2

## 应用场景
从对话中提取的实际使用场景。

## 局限性
已知的限制或注意事项。

## 相关概念
- [[相关概念A]]
- [[相关概念B]]

---
> 本页内容部分来源于 Claude Code 对话历史，由 `/claude-history-ingest` 自动生成。
```

### 4.4 踩坑记录特殊处理

`type: pitfall` 的知识点写入对应概念页的「局限性」章节，或在 `wiki/concepts/` 下创建专门的踩坑记录页：

- 文件名：`wiki/concepts/pitfall-<关键词>.md`
- `entity_type: pattern`
- 内容包含：`## 问题描述`、`## 触发条件`、`## 解决方案`、`## 规避建议`

---

## Stage 5: Schema（更新索引）

### 5.1 更新 wiki/index.md

在 `wiki/index.md` 的概念页表格中追加新条目：

- 为每个新建或更新的概念页添加/更新一行
- 格式：`| [[概念名]] | tag1, tag2 | N | active |`
- **不删除**既有条目

### 5.2 更新 wiki/log.md

追加本次操作记录：

```markdown
## YYYY-MM-DD HH:mm

- **操作**：`/claude-history-ingest` 对话历史导入
- **输入**：扫描 N 条历史记录，筛选 P 个候选会话
- **结果**：提取 M 个知识点，新建 K 个概念页，更新 J 个已有页面
- **脱敏**：替换 API Key X 处、Token Y 处
- **跳过**：L 个低产会话
- **概念页**：列出新建/更新的页面文件名
```

---

## 最终输出

处理完成后，向用户输出统计摘要：

```
/claude-history-ingest 完成
━━━━━━━━━━━━━━━━━━━━━
扫描历史记录：N 条
候选会话：P 个
脱敏处理：API Key X 处、Token Y 处
提取知识点：M 个
  - 概念：C 个
  - 解决方案：S 个
  - 踩坑记录：F 个
新建概念页：K 个（wiki/concepts/ 下）
更新已有页面：J 个
跳过（低产会话）：L 个
━━━━━━━━━━━━━━━━━━━━━
新建/更新文件列表：
  - wiki/concepts/xxx.md (新建)
  - wiki/concepts/yyy.md (更新)
  ...
```

---

## 约束与安全

- `~/.claude/` 对话历史为只读源，不得修改原始文件
- **脱敏为强制性**：任何知识点写入 wiki/ 前必须经过脱敏处理
- 脱敏规则覆盖 API Key、Token、密码、内部 IP、邮箱、个人路径
- 所有文件 UTF-8 无 BOM 编码
- frontmatter 必须包含：title, created, updated, tags, sources（含 claude-history 前缀）, summary, status, entity_type
- 文件名使用 kebab-case
- 合并到已有页面时不覆盖既有内容
- 冲突内容标记 `^[ambiguous]`
- 单次导入最多处理 50 个会话（可配置）
- 单个知识点内容 ≤ 500 字
