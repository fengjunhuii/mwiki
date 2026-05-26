---
name: wiki-lint
description: 知识质量检查——检测断链、缺失页、待裁决冲突、过时标记
---

# /wiki-lint — 知识质量检查

扫描 `wiki/` 目录下所有 Markdown 文件，检测四类质量问题：**断链**、**缺失页**、**待裁决冲突**、**过时页面**，输出分类问题列表。

> **数据安全约束**：本操作为只读扫描，不修改任何文件（除 `wiki/log.md` 追加日志外）。

---

## 前置准备

1. 读取 `ai/_index.json` 确认路由配置
2. 确认 `wiki/index.md` 存在且可读
3. 如果 `wiki/index.md` 不存在或为空模板，输出「知识库尚未初始化，请先执行 /wiki-setup」并终止
4. 构建 wiki/ 文件名集合：扫描 `wiki/` 下所有 `.md` 文件，收集每个文件的**去除扩展名后的文件名**作为页面名集合
   - 同时扫描 `wiki/concepts/`、`wiki/topics/`、`wiki/comparisons/`、`wiki/patterns/`、`wiki/reports/` 等所有子目录
   - 页面名 = 文件名去掉 `.md` 后缀（如 `prompt-engineering.md` → 页面名 `prompt-engineering`）

---

## Check 1: 断链检测

扫描 `wiki/` 下所有 `.md` 文件的 body 内容，查找所有 `[[wikilinks]]` 引用，检查每个引用是否有对应的 `.md` 文件存在。

### 1.1 wikilink 解析规则

对每个文件，使用正则 `\[?\[([^\]]+)\]\]?` 提取所有 wikilink 目标：

- `[[概念名]]` → 目标为 `概念名`
- `[[概念名|显示文本]]` → 目标为 `概念名`（管道符前为目标页）
- `[[概念名#章节标题]]` → 目标为 `概念名`（井号前为目标页）
- `[[概念名#章节标题|显示文本]]` → 目标为 `概念名`

### 1.2 断链判断

对每个提取到的 wikilink 目标，检查以下路径是否存在对应的 `.md` 文件：

1. `wiki/concepts/目标.md`
2. `wiki/topics/目标.md`
3. `wiki/comparisons/目标.md`
4. `wiki/patterns/目标.md`
5. `wiki/目标.md`
6. 在整个 `wiki/` 目录下递归搜索 `目标.md`

如果以上路径均不存在，则判定为**断链**。

### 1.3 记录断链

每条断链记录：
- 来源文件路径
- 来源文件中的行号或上下文
- 断链目标名

### 1.4 输出

```
断链检测：
  扫描文件：N 个
  发现断链：M 个
    - wiki/concepts/prompt-engineering.md → [[不存在的概念]] (第 42 行)
    - wiki/topics/ai-overview.md → [[missing-page]] (相关概念章节)
```

---

## Check 2: 缺失页检测（Index 引用）

检查 `wiki/index.md` 的概念表格中引用的概念页是否实际存在。

### 2.1 解析 index 表格

读取 `wiki/index.md`，解析所有表格中的 `[[wikilinks]]`：

- 概念页表格中的 `[[概念名]]`
- 主题页表格中的 `[[主题名]]`
- 对比页表格中的 `[[对比名]]`
- 模式页表格中的 `[[模式名]]`

### 2.2 缺失判断

对每个 index 中引用的概念名，检查对应的 `.md` 文件是否存在于 `wiki/` 的对应子目录下：

- 概念页 → 检查 `wiki/concepts/概念名.md`
- 主题页 → 检查 `wiki/topics/主题名.md`
- 对比页 → 检查 `wiki/comparisons/对比名.md`
- 模式页 → 检查 `wiki/patterns/模式名.md`

### 2.3 记录缺失页

每条缺失页记录：
- index 表格中的概念名
- 期望文件路径
- 缺失原因（文件不存在）

### 2.4 输出

```
缺失页检测：
  Index 引用：N 个
  缺失页面：K 个
    - [[RAG]] → wiki/concepts/rag.md 不存在
    - [[向量数据库]] → wiki/concepts/向量数据库.md 不存在
```

---

## Check 3: 待裁决冲突检测

扫描 `wiki/` 下所有 `.md` 文件，查找包含 `^[ambiguous]` 标记的内容。

### 3.1 扫描规则

对每个文件逐行扫描，查找包含 `^[ambiguous]` 的行：

- 匹配模式：行中包含 `^[ambiguous]` 字面量
- 提取该行的完整内容（包含来源和冲突描述）

### 3.2 记录待裁决项

每条待裁决项记录：
- 文件路径
- 冲突内容（包含 `^[ambiguous]` 标记的完整段落）
- 涉及的来源文件（从上下文中提取）

### 3.3 输出

```
待裁决冲突检测：
  发现待裁决项：J 个
    - wiki/concepts/prompt-engineering.md
      > 01-prompt-engineering.md 描述为"零样本提示不需要示例" ^[ambiguous]
      > 04-prompt-basics.md 描述为"零样本提示有时需要格式示例" ^[ambiguous]
```

---

## Check 4: 过时页面检测

扫描 `wiki/` 下所有 `.md` 文件的 YAML frontmatter，查找 `status: deprecated` 的页面。

### 4.1 解析 frontmatter

对每个 `.md` 文件：

1. 读取文件开头的 YAML frontmatter（`---` 包裹部分）
2. 解析 `status` 字段
3. 如果 `status` 为 `deprecated`，标记为过时页面

### 4.2 记录过时页面

每条过时页面记录：
- 文件路径
- 标题（取 frontmatter 中的 `title`）
- 最后更新时间（取 frontmatter 中的 `updated`）

### 4.3 输出

```
过时页面检测：
  发现过时页面：P 个
    - wiki/concepts/old-framework.md — "Old Framework"（最后更新: 2025-01-15）
```

---

## 结果汇总

### 有问题时

```
/wiki-lint 检查完成
━━━━━━━━━━━━━━━━━━━━━
发现 N 个问题：
  - 断链：M 个
  - 缺失页：K 个
  - 待裁决：J 个
  - 过时页：P 个
━━━━━━━━━━━━━━━━━━━━━

详细列表：

### 断链（M 个）
[列出所有断链，含来源文件和目标]

### 缺失页（K 个）
[列出所有 index 引用但文件不存在的页面]

### 待裁决（J 个）
[列出所有 ambiguous 标记及冲突内容]

### 过时页（P 个）
[列出所有 deprecated 状态的页面]
```

### 无问题时

```
/wiki-lint 检查完成
━━━━━━━━━━━━━━━━━━━━━
无异常
━━━━━━━━━━━━━━━━━━━━━
扫描文件：N 个
检查 wikilinks：W 个
Index 引用：I 个
```

---

## 日志记录

检查完成后，在 `wiki/log.md` 中追加记录：

```markdown
## YYYY-MM-DD HH:mm

- **操作**：`/wiki-lint` 知识质量检查
- **扫描范围**：`wiki/` 下 N 个文件
- **检查结果**：发现 M 个断链、K 个缺失页、J 个待裁决、P 个过时页
- **状态**：有异常 / 无异常
```

---

## 约束与安全

- 本操作为**只读扫描**，不修改任何 wiki/ 文件（除 `wiki/log.md` 追加日志外）
- `_raw/` 和 `raw/` 不参与 lint 检查
- 所有文件 UTF-8 无 BOM 编码
- wikilink 解析遵循 Obsidian 原生格式（`[[页面名]]`、`[[页面名|别名]]`、`[[页面名#标题]]`）
- 断链判断仅在 `wiki/` 目录内查找，不跨 Vault
