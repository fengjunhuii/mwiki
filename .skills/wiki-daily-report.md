---
name: wiki-daily-report
description: 每日知识报告生成——扫描当日编辑的 wiki 文档，按模板生成日报
---

# /wiki-daily-report — 每日知识报告生成

扫描当日创建或编辑的所有 `wiki/` 文档，按 `templates/diary-template.md` 格式生成日报，存放在 `wiki/reports/daily/YYYY-MM-DD.md`。

> **数据安全约束**：本操作仅读取 `wiki/` 文件元数据与内容，写入 `wiki/reports/daily/` 和 `wiki/log.md`，不修改已有 wiki 页面。

---

## 前置准备

1. 读取 `ai/_index.json` 确认 `routes.reports.daily` 路径（默认 `wiki/reports/daily/`）
2. 确认 `wiki/` 目录存在且包含 `.md` 文件
3. 确认 `templates/diary-template.md` 存在作为格式参考
4. 确认 `wiki/reports/daily/` 目录存在，不存在则创建
5. 获取当前日期（格式 `YYYY-MM-DD`）

---

## Phase 1: 扫描当日活动

扫描 `wiki/` 下所有 `.md` 文件（含子目录），筛选当日有变动的文件。

### 1.1 筛选条件

对每个 `.md` 文件，检查以下任一条件是否满足：

- frontmatter 中 `created` 字段等于今日日期
- frontmatter 中 `updated` 字段等于今日日期
- 文件的最后修改时间（filesystem mtime）为今日

### 1.2 扫描范围

递归扫描以下目录：

| 目录 | 说明 |
|------|------|
| `wiki/concepts/` | 概念页 |
| `wiki/topics/` | 主题页 |
| `wiki/comparisons/` | 对比页 |
| `wiki/patterns/` | 模式页 |
| `wiki/`（根级文件） | purpose.md、index.md、log.md 等 |

**不扫描**：`_raw/`、`raw/`、`wiki/reports/`（避免日报本身被计入）、`wiki/graphs/`（非文本知识页）。

### 1.3 收集信息

对每个当日变动的文件，记录：

- 文件路径（相对 Vault 根目录）
- 标题（取 frontmatter `title`，无则取文件名去掉扩展名）
- 变动类型：`新建`（created == 今日）或 `编辑`（updated == 今日）
- 摘要（取 frontmatter `summary` 字段，无则标记"无摘要"）
- 标签（取 frontmatter `tags` 字段）
- entity_type（取 frontmatter `entity_type` 字段）

### 1.4 输出

```
日报扫描：
  扫描文件：N 个
  当日变动：M 个
    - [新建] wiki/concepts/prompt-engineering.md — "Prompt Engineering"
    - [编辑] wiki/topics/ai-overview.md — "AI 概述"
```

---

## Phase 2: 提取今日所学

从当日变动的文件中，提取核心知识点作为"今日所学"摘要。

### 2.1 提取策略

对每个当日变动的文件：

1. 读取文件 body 内容（跳过 frontmatter）
2. 提取各章节的一级标题和核心要点（每个文件提炼 1-3 条关键知识点）
3. 按主题分类聚合（同 `tags` 的文件归为一组）

### 2.2 去重与整合

- 多个文件中出现的相同概念，合并为一条知识点
- 每条知识点用一句话概括，不超过 50 字
- 引用来源文件：每条知识点后标注 `[来源](wikilink路径)`

### 2.3 输出

按主题标签分组列出今日所学，每组 3-8 条知识点。

---

## Phase 3: 生成思考与建议

基于当日活动数据，生成 Agent 分析与建议。

### 3.1 分析维度

1. **知识覆盖度**：今日活动涉及哪些 `entity_type`，是否有遗漏的知识领域
2. **知识关联度**：今日新增/编辑的页面之间是否存在 wikilink 关联，识别孤立页面
3. **知识健康度**：引用 `/wiki-lint` 的检查维度（不执行 lint，仅从已知状态推断）
4. **学习建议**：
   - 建议补充的关联概念（今日活动中提到但尚未建页的关键词）
   - 建议执行的维护操作（如某页面长时间未更新、某概念缺少关联页面）
   - 建议下一步学习方向（基于今日主题的延伸方向）

### 3.2 输出格式

```
### 知识覆盖
今日活动涉及 X 个 entity_type：concept(N)、topic(M)...

### 关联分析
[新建页面] prompt-engineering 与 [已有页面] rag-basics 有关联但未互相链接

### 建议
- 建议为 [[vector-embedding]] 概念补充与今日编辑的 [[prompt-engineering]] 的关联
- 建议执行 /wiki-lint 检查今日新增页面的断链情况
- 今日主题集中在 Prompt 领域，可考虑补充 RAG 相关对比页
```

---

## Phase 4: 生成日报文件

按 `templates/diary-template.md` 格式组装日报，写入文件。

### 4.1 文件路径与命名

- 路径：`wiki/reports/daily/YYYY-MM-DD.md`
- 日期取当前日期
- 如果文件已存在，在文件末尾追加更新时间戳，不覆盖已有内容

### 4.2 Frontmatter

```yaml
---
title: "YYYY-MM-DD 日报"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [daily-report]
sources: [wiki-daily-report]
summary: "今日编辑 N 篇文档，涵盖 M 个主题"
status: active
entity_type: overview
type: daily-report
---
```

### 4.3 Body 结构

```markdown
# YYYY-MM-DD 日报

## 今日活动

| 类型 | 页面 | 标题 | entity_type | 摘要 |
|------|------|------|-------------|------|
| 新建 | [[prompt-engineering]] | Prompt Engineering | concept | 提示工程核心概念与实践 |
| 编辑 | [[rag-basics]] | RAG 基础 | concept | RAG 流程与组件 |

> 共 N 篇文档变动

## 今日所学

### 主题A（标签）

- 关键知识点 1 [[来源页面]]
- 关键知识点 2 [[来源页面]]

### 主题B（标签）

- 关键知识点 3 [[来源页面]]

## 思考与建议

### 知识覆盖
[Phase 3 分析结果]

### 关联分析
[Phase 3 关联发现]

### 建议
- [Phase 3 建议]
```

### 4.4 编码要求

- 文件编码：UTF-8（无 BOM）
- 中文内容正常显示
- wikilinks 使用 Obsidian 原生 `[[页面名]]` 格式

---

## Phase 5: 日志与输出

### 5.1 日志记录

在 `wiki/log.md` 中追加记录：

```markdown
## YYYY-MM-DD HH:mm

- **操作**：`/wiki-daily-report` 每日报告生成
- **报告文件**：`wiki/reports/daily/YYYY-MM-DD.md`
- **扫描范围**：`wiki/` 下 N 个文件
- **当日变动**：M 篇（新建 X 篇、编辑 Y 篇）
- **状态**：完成
```

### 5.2 最终输出

```
/wiki-daily-report 完成
━━━━━━━━━━━━━━━━━━━━━
报告文件：wiki/reports/daily/YYYY-MM-DD.md
扫描文件：N 个
当日变动：M 篇（新建 X 篇、编辑 Y 篇）
涉及主题：T 个
━━━━━━━━━━━━━━━━━━━━━
```

### 5.3 无变动时

如果当日无任何 wiki 文件变动：

```
/wiki-daily-report 完成
━━━━━━━━━━━━━━━━━━━━━
今日无 wiki 文档变动，跳过日报生成。
如需强制生成，使用 /wiki-daily-report force
━━━━━━━━━━━━━━━━━━━━━
```

当使用 `force` 参数时，生成仅包含"今日活动：无"的空日报。

---

## 约束与安全

- 本操作**仅读取** `wiki/` 文件元数据与内容，不修改已有页面
- 写入仅限 `wiki/reports/daily/` 和 `wiki/log.md`
- `_raw/` 和 `raw/` 不参与扫描
- 不扫描 `wiki/reports/`（避免递归）和 `wiki/graphs/`（非文本知识页）
- 所有文件 UTF-8 无 BOM 编码
- 同一日期重复执行时追加更新，不覆盖已有日报内容
