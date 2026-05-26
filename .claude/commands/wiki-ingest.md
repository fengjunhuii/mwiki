---
name: wiki-ingest
description: 四阶段全量导入 _raw/ 素材到 wiki/（Ingest → Extract → Resolve → Schema）
---

# /wiki-ingest — 全量知识导入

将 `_raw/` 下所有 Markdown 文件经过四阶段处理，转化为 `wiki/` 下的结构化知识页面。

> **数据安全约束**：`_raw/` 原始素材只读，Agent 不得修改或删除。

---

## 前置准备

1. 读取 `ai/_index.json` 确认路由配置
2. 读取 `.manifest.json` 获取已处理文件列表
3. 备份 `.manifest.json` → `.manifest.json.bak`（每次操作前自动备份）
4. 扫描 `_raw/` 下所有 `.md` 文件，按文件名排序得到待处理列表
5. 如果 `_raw/` 为空，输出「_raw/ 目录为空，无文件可导入」并终止

---

## Stage 1: Ingest（收录）

对 `_raw/` 下每个 `.md` 文件执行以下操作：

### 1.1 逐文件处理

对每个文件（按文件名排序）：

1. **显示进度**：`Ingesting [当前序号/总数] 文件名.md`
2. **读取文件内容**：尝试以 UTF-8 读取。如果编码异常，跳过该文件并在 `wiki/log.md` 中记录：
   ```
   - **编码异常**：`文件名` — 跳过（原因：编码解析失败）
   ```
3. **解析 frontmatter**：
   - 如果文件已有 YAML frontmatter（`---` 包裹），解析已有字段
   - 如果没有 frontmatter，为其创建
4. **生成 summary**：阅读文件全文，生成一句简洁的中文摘要（≤ 100 字），写入 frontmatter 的 `summary` 字段
5. **补全 frontmatter 字段**：确保以下字段存在，缺失的用合理默认值填充：
   - `title`：取第一个 `#` 标题，或取文件名（去掉序号前缀和扩展名）
   - `created`：取文件修改时间，格式 `YYYY-MM-DD`
   - `updated`：同 created
   - `tags`：根据内容推断 2-5 个标签
   - `sources`：`["_raw/文件名"]`
   - `status`：`active`
   - `entity_type`：推断类型（`concept` / `tool` / `overview` / `pattern` / `comparison`）
6. **计算 SHA256**：对文件原始内容计算 SHA256 hash
7. **记录到 manifest**：将文件信息暂存（Stage 4 统一写入）

### 1.2 处理结果

- 将每个文件的处理结果（summary、tags、entity_type、概念列表）收集到内存数据结构中
- 每个文件提取一个「概念列表」，概念 = 文中出现的关键技术术语和专有名词

---

## Stage 2: Extract（提取）

对 Stage 1 中所有成功处理的文件，提取结构化知识：

### 2.1 概念提取

对每个文件：

1. 识别文中**明确出现**的技术概念、术语、框架、算法名称
2. 每个概念提取以下信息：
   - `name`：概念名称（中文或英文原名）
   - `aliases`：别名列表（如中英文同义名）
   - `definition`：文中对该概念的定义或描述（引用原文，≤ 200 字）
   - `source_file`：来源文件名
   - `source_section`：来源章节标题
   - `relations`：与其他概念的语义关系（如"是...的技术"、"包含..."、"与...相关"）

### 2.2 低产文件标记

- 如果一个文件无法提取出任何有意义的「概念」，标记为 `low-yield`
- 在 `wiki/log.md` 中记录：
  ```
  - **低产文件**：`文件名` — 无概念可提取
  ```

### 2.3 输出中间结果

将提取结果整理为概念表（内存数据结构），格式：

```
概念名 -> {
  aliases: [...],
  mentions: [
    { file: "01-xxx.md", section: "什么是X", definition: "..." },
    { file: "04-xxx.md", section: "简介", definition: "..." }
  ],
  relations: [{ target: "概念Y", type: "相关" }]
}
```

---

## Stage 3: Resolve（合并）

将跨文件出现的同一概念合并为单一 `wiki/concepts/` 页面：

### 3.1 概念归一

1. 对概念表按名称分组，使用以下规则判断同一概念：
   - 名称完全相同
   - 名称互为别名（中英文对应，如"大语言模型"与"LLM"）
   - 名称大小写无关相同
2. 合并后的概念取**出现次数最多的名称**作为主名称

### 3.2 创建概念页

对每个合并后的概念，创建 `wiki/concepts/概念名.md`（文件名使用 kebab-case）：

1. **Frontmatter**：
   ```yaml
   ---
   title: "概念名"
   created: YYYY-MM-DD
   updated: YYYY-MM-DD
   tags: [从所有来源聚合]
   sources: [来源文件列表]
   summary: "概念的一句话描述"
   status: active
   entity_type: concept
   ---
   ```

2. **内容结构**（参考 `templates/concept-template.md`）：
   - `## 定义`：合并所有来源的定义描述
   - `## 核心要点`：从各来源提取的关键要点
   - `## 应用场景`：实际应用案例
   - `## 局限性`：限制和注意事项
   - `## 相关概念`：使用 `[[wikilinks]]` 链接

### 3.3 冲突处理

如果同一概念在不同文件中有**矛盾的定义或描述**：
- 保留所有来源的描述
- 在冲突处标记 `^[ambiguous]`
- 格式：`> 来源文件名 描述内容 ^[ambiguous]`

### 3.4 收录原始素材

- 将已成功处理的 `_raw/` 文件**复制**到 `raw/`（收录层，只追加不覆盖）
- 如果 `raw/` 中已存在同名文件，跳过（不覆盖）

---

## Stage 4: Schema（更新索引）

### 4.1 更新 wiki/index.md

在 `wiki/index.md` 的对应表格中追加条目：

- **概念页表格**：为每个新建的 `wiki/concepts/*.md` 添加一行
  ```
  | [[概念名]] | tag1, tag2 | N | active |
  ```
- **不要删除**既有结构（保留模板注释行）
- 按概念名字母排序

### 4.2 更新 .manifest.json

将所有已处理文件的信息写入 `.manifest.json`：

```json
{
  "version": "1.0",
  "created": "原值保持",
  "updated": "当前日期",
  "files": {
    "01-prompt-engineering.md": {
      "sha256": "计算值",
      "processedAt": "2026-05-26T23:30:00",
      "status": "success",
      "concepts": ["Prompt Engineering", "Chain of Thought"],
      "entityType": "concept"
    }
  },
  "stats": {
    "totalFiles": 6,
    "totalConcepts": 5,
    "lastIngest": "2026-05-26T23:30:00"
  }
}
```

### 4.3 更新 wiki/log.md

追加本次操作记录：

```markdown
## YYYY-MM-DD HH:mm

- **操作**：`/wiki-ingest` 全量导入
- **输入**：`_raw/` 下 N 个文件
- **结果**：导入 N 篇，提取 M 个概念，合并 K 个页面
- **跳过**：E 个编码异常，L 个低产文件
- **概念页**：列出新建的概念页文件名
```

---

## 最终输出

处理完成后，向用户输出统计摘要：

```
/wiki-ingest 完成
━━━━━━━━━━━━━━━━━━━━━
导入文件：N 篇
提取概念：M 个
合并页面：K 个（wiki/concepts/ 下）
跳过（编码异常）：E 个
标记（低产文件）：L 个
已收录到 raw/：N 篇
━━━━━━━━━━━━━━━━━━━━━
新建文件列表：
  - wiki/concepts/prompt-engineering.md
  - wiki/concepts/rag.md
  ...
```

---

## 约束与安全

- `_raw/` 文件只读，不得修改
- `raw/` 只追加，不覆盖
- `.manifest.json` 操作前必须备份
- 所有文件 UTF-8 无 BOM 编码
- frontmatter 必须包含：title, created, updated, tags, sources, summary, status, entity_type
- 文件名使用 kebab-case
