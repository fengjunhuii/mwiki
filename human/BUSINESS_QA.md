---
title: "mwiki 业务逻辑问卷"
created: 2026-05-27
updated: 2026-05-27
tags: [meta, business-logic, human]
sources: [wiki/purpose.md]
summary: "记录 AI 无法从代码推断的业务决策、领域约束和用户偏好。内容不一致时以 wiki/ 为准。"
status: active
entity_type: overview
---

# mwiki 业务逻辑问卷

> **用途**：本文档记录那些 AI Agent 无法从代码或目录结构中推断的业务逻辑、决策背景和领域约束。Agent 在执行任务时应参考本文档，但不得修改标记 `<!-- no-edit -->` 的段落。
>
> **派生声明**：本文档从 `wiki/` 派生。内容不一致时以 `wiki/` 为唯一真相源。

## 1. 项目定位与决策背景

### 1.1 为什么选择 Obsidian + 文件系统而非数据库？

- **决策**：所有知识以 Markdown 文件存储，不引入数据库或后端服务
- **原因**：个人知识库规模有限（千篇级别），文件系统的直接读写性能足够；Obsidian 提供原生 wikilink 和图谱可视化，无需额外开发；Markdown 文件可被任何文本编辑器打开，避免供应商锁定
- **约束**：此决策为架构基线，不得因性能优化而引入数据库层

### 1.2 为什么区分 _raw/ 和 raw/ 两层？

- **决策**：`_raw/` 为用户暂存区，`raw/` 为已归档素材
- **原因**：用户习惯将素材随手丢入 `_raw/`，Agent Ingest 后移入 `raw/` 标记"已处理"，避免重复导入；两层隔离保证原始素材不被 Agent 误改
- **约束**：`_raw/` 对 Agent 只读，`raw/` 对 Agent 只追加

### 1.3 为什么采用 CLI Agent 而非 Web UI？

- **决策**：通过 Claude Code CLI + Skills（Slash Commands）交互，不构建 Web 界面
- **原因**：开发者日常在终端工作，CLI 集成成本最低；Claude Code 已提供 Skill 机制，无需自建 UI 框架；减少维护负担
- **约束**：所有用户交互通过 CLI 完成，不构建 HTTP 服务

## 2. 知识管理规则

### 2.1 概念合并策略

<!-- no-edit: 合并策略由 wiki-ingest skill 定义，本文档仅记录决策背景 -->

- **决策**：同名概念跨篇章合并为单一 `wiki/concepts/*.md` 页面，冲突内容标记 `^[ambiguous]`
- **原因**：自动合并可能丢失视角差异，标记后由用户裁决更安全
- **用户操作**：用户看到 `^[ambiguous]` 标记后，手动选择保留哪个版本或综合改写
- **约束**：Agent 不得自动删除或覆盖冲突内容

### 2.2 entity_type 推断规则

- **决策**：Ingest 阶段按关键词匹配优先级自动推断 `entity_type`
- **优先级**：comparison > tool > event > person > pattern > overview > concept（兜底）
- **原因**：comparison 最容易被其他类型吞没（如"对比两个工具"可能被误判为 tool），因此优先级最高
- **约束**：推断结果写入 frontmatter 后，用户可随时手动修正

### 2.3 低产文件处理

- **决策**：无概念可提取的文件标记为 `low-yield`，不删除
- **原因**：用户可能有未完成的笔记，标记提醒但不自动清理
- **约束**：`low-yield` 文件仍保留在 `wiki/` 中，Agent 不主动删除

## 3. 数据安全边界

### 3.1 不可逆操作清单

以下操作 **禁止 Agent 自动执行**，必须经用户确认：

| 操作 | 原因 |
|------|------|
| 删除 `_raw/` 中的文件 | 原始素材不可恢复 |
| 覆盖 `raw/` 中的已有文件 | 归档层只追加 |
| 删除 `wiki/` 中的概念页 | 可能破坏 wikilink 引用链 |
| 自动解决 `^[ambiguous]` 冲突 | 需要人工判断 |
| 修改 `human/` 中标记 `<!-- no-edit -->` 的区域 | 这些区域由 Agent 派生维护 |

### 3.2 脱敏规则

对话历史导入时，以下信息必须过滤：

- API Key（`sk-...`、`key-...` 等）
- Bearer Token
- 私有 IP 地址
- 个人邮箱地址
- Windows 本地路径（`C:\Users\...`）

## 4. 用户偏好

### 4.1 语言与格式

- **内容语言**：中文简体，技术术语首次出现附英文原文
- **文件编码**：UTF-8 无 BOM
- **注释风格**：中文注释，说明"为什么"而非"是什么"
- **文件命名**：kebab-case（如 `prompt-engineering.md`）

### 4.2 报告偏好

- **日报**：每日自动生成，存放 `wiki/reports/daily/YYYY-MM-DD.md`
- **周报**：按需生成，存放 `wiki/reports/weekly/`
- **格式**：遵循 `templates/diary-template.md` 和 `templates/report-template.md`

## 5. 多 Agent 共治规则

### 5.1 冲突处理

- 多个 Agent 同时操作时，以最后写入者为准（文件系统无锁机制）
- 建议不同 Agent 在不同时间段操作，或分工处理不同目录
- `.manifest.json` 的 hash 校验可检测并发冲突

### 5.2 Agent 权限矩阵

| Agent 类型 | `_raw/` | `raw/` | `wiki/` | `human/` | `ai/` |
|-----------|---------|--------|---------|----------|-------|
| Claude Code | 只读 | 只追加 | 读写 | 写入 | 读写 |
| Cursor | 只读 | 只追加 | 读写 | 写入 | 读写 |
| Codex | 只读 | 只追加 | 读写 | 写入 | 读写 |
| 其他 Agent | 只读 | 只追加 | 读写 | 写入 | 读写 |

> 注：所有 Agent 权限一致，通过 CLAUDE.md / GEMINI.md 等配置文件约束行为。

## 6. 已知限制

- **全文搜索**：依赖 Agent 逐文件读取，无搜索引擎索引，大规模知识库查询可能较慢
- **并发安全**：文件系统无事务机制，多 Agent 同时写入可能产生冲突
- **图谱可视化**：`graph.html` 为 Canvas 力导向布局，节点超过 500 时性能下降
- **中文分词**：wikilink 匹配基于精确文本，不支持模糊匹配或拼音搜索

## 7. 变更记录

| 日期 | 变更内容 |
|------|---------|
| 2026-05-27 | 初始创建，记录核心业务逻辑和决策背景 |
