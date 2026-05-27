---
name: cross-linker
description: 自动补充 wikilinks——扫描 wiki/ 页面，将未链接的概念关键词转为 [[wikilinks]]，减少知识孤岛
---

# /cross-linker — 自动补充 wikilinks

扫描 `wiki/` 下所有页面，识别已存在概念页标题但未被 `[[wikilinks]]` 包裹的纯文本关键词，自动将其转为 `[[概念名]]` 格式，从而减少知识孤岛。

> **数据安全约束**：本操作**不修改** `_raw/` 和 `raw/` 目录下的任何文件。仅修改 `wiki/` 下的文件（不含 `wiki/graphs/`）。

---

## 前置准备

1. 读取 `ai/_index.json` 确认路由配置
2. 确认 `wiki/index.md` 存在且可读
3. 如果 `wiki/index.md` 不存在或为空模板，输出「知识库尚未初始化，请先执行 /wiki-setup」并终止

---

## Phase 1: 概念词典构建

### 1.1 扫描概念页标题

扫描 `wiki/concepts/` 下所有 `.md` 文件，提取概念名：

1. 优先取 frontmatter 中的 `title` 字段作为概念名
2. 若无 `title`，取文件名去除 `.md` 后缀
3. 同时收集每个概念页的**别名**（frontmatter 中的 `aliases` 数组，若存在）

### 1.2 构建词典

将所有概念名和别名构建为查找词典 `glossary[]`，每条记录包含：

```
{
  term: "Prompt Engineering",      // 概念名或别名
  pageFile: "wiki/concepts/prompt-engineering.md",
  isAlias: false,                   // true 表示来自 aliases 字段
  aliasOf: null                     // 若为别名，指向主概念名
}
```

### 1.3 排序规则

词典按 `term` 长度**降序**排列（优先匹配更长的术语，避免短术语吞没长术语）。

例如 `"向量数据库"` 排在 `"向量"` 之前。

### 1.4 输出

```
词典构建完成
  概念页：N 个
  总词条（含别名）：M 条
```

---

## Phase 2: 候选定位

### 2.1 扫描范围

扫描以下目录下的所有 `.md` 文件：

- `wiki/concepts/`（概念页之间互相补充）
- `wiki/topics/`
- `wiki/comparisons/`
- `wiki/patterns/`
- `wiki/` 根目录下的 `.md` 文件（如 `purpose.md`、`index.md`）

**排除**：

- `_raw/`（原始素材，只读）
- `raw/`（归档层，只读）
- `wiki/graphs/`（非文本内容）
- `wiki/reports/`（报告文件不做修改）
- `wiki/log.md`（操作日志不做修改）

### 2.2 已有 wikilink 检测

对每个文件的 body 内容（跳过 YAML frontmatter），先提取已有的 wikilink 目标：

- 正则 `\[?\[([^\]#|]+)` 提取所有 wikilink 目标
- 构建该文件已有链接集合 `existingLinks{}`
- 已有链接的概念不再重复补充

### 2.3 纯文本匹配

对每个文件 body 中的每个段落，逐个检查词典中的 `term`：

1. **精确匹配**：`term` 作为独立词出现在段落中（前后为非单词字符或段落首尾）
2. **排除已有链接**：`term` 不在 `[[...]]` 内部（检查匹配位置前后是否存在未闭合的 `[[`）
3. **排除自身页面**：不在该 term 对应的概念页本身中创建指向自身的链接

#### 匹配规则细节

- 中文概念名：直接匹配完整字符串（如 `"向量数据库"` 匹配段落中出现的 `向量数据库`）
- 英文概念名：大小写不敏感匹配，但替换时保留原文大小写，链接目标使用概念页实际标题
- 匹配位置不能在以下上下文中：
  - 已在 `[[...]]` 内部
  - 行内代码 `` `...` `` 内部
  - 代码块 ` ``` ` 内部
  - YAML frontmatter 内部
  - Markdown 链接文本 `[已有链接](url)` 内部

### 2.4 候选记录

每条匹配记录为：

```
{
  file: "wiki/topics/ai-overview.md",
  term: "Prompt Engineering",
  linkTarget: "prompt-engineering",   // 对应概念页文件名（去掉 .md）
  lineNumber: 42,
  context: "...深入研究 Prompt Engineering 的应用...",  // 前后各 30 字符
  isAlias: false
}
```

### 2.5 输出

```
候选定位完成
  扫描文件：F 个
  发现候选链接：C 条
```

---

## Phase 3: 链接补充

### 3.1 替换策略

对每个文件收集的所有候选链接，按行号分组，**从文件末尾向前替换**（避免替换导致行号偏移）。

同一行内的多个候选替换，同样从右向左执行。

#### 替换规则

1. 将匹配到的纯文本 `term` 替换为 `[[linkTarget|term]]`
   - 如果 `term` 与 `linkTarget` 完全相同（或仅大小写不同），使用简化形式 `[[term]]`
   - 如果 `term` 是别名，使用 `[[主概念名|term]]`
2. 替换后检查同一行不产生嵌套 `[[...[[...]]...]]`

### 3.2 安全边界

- **单文件最大替换数**：每文件不超过 30 处（防止过度链接降低可读性）
- **全局最大替换数**：每次执行总替换不超过 200 处（超出部分输出提示，下次执行可继续）
- **每个概念名单文件最多出现 3 处替换**（避免同一段落同一概念被反复链接）
- **替换后文件大小增长不超过 20%**（防止 wikilink 语法膨胀）

超出限制的候选记录为"未执行"，在统计中单独列出。

### 3.3 写入文件

1. 读取原文件内容
2. 执行所有替换
3. 更新 frontmatter 中的 `updated` 字段为当前日期（`YYYY-MM-DD`）
4. 写回文件（UTF-8，无 BOM）

---

## Phase 4: 结果输出

### 4.1 终端输出

```
/cross-linker 完成
━━━━━━━━━━━━━━━━━━━━━
词典词条：M 条（来自 N 个概念页）
扫描文件：F 个
补充链接：S 处
  - wiki/concepts/prompt-engineering.md: 3 处
  - wiki/topics/ai-overview.md: 5 处
  - wiki/concepts/rag.md: 2 处
未执行（达到限制）：R 处
未修改文件：U 个
━━━━━━━━━━━━━━━━━━━━━
```

### 4.2 无候选时

```
/cross-linker 完成
━━━━━━━━━━━━━━━━━━━━━
词典词条：M 条（来自 N 个概念页）
扫描文件：F 个
补充链接：0 处
所有可链接的概念已正确链接，无需补充。
━━━━━━━━━━━━━━━━━━━━━
```

### 4.3 日志记录

在 `wiki/log.md` 中追加记录：

```markdown
## YYYY-MM-DD HH:mm

- **操作**：`/cross-linker` 自动补充 wikilinks
- **词典**：M 条词条（N 个概念页）
- **扫描**：F 个文件
- **补充链接**：S 处
- **修改文件**：X 个
- **未执行**：R 处（达到限制）
```

---

## 约束与安全

- **禁止修改** `_raw/` 和 `raw/` 目录下的任何文件
- **禁止修改** `wiki/graphs/`、`wiki/reports/`、`wiki/log.md`
- 替换前必须确认匹配位置不在 frontmatter、代码块、行内代码内
- 不为页面创建指向自身的链接（避免循环引用）
- 每个概念名在同一文件中最多补充 3 处链接
- 全局单次执行上限 200 处替换
- 替换后 frontmatter 的 `updated` 字段自动更新
- 所有文件 UTF-8 无 BOM 编码
- wikilink 使用 Obsidian 原生格式（`[[页面名]]`、`[[页面名|别名]]`）
