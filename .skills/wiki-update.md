---
name: wiki-update
description: 增量更新——基于 .manifest.json SHA256 对比，仅处理新增或变更的 _raw/ 素材
---

# /wiki-update — 增量知识更新

对比 `.manifest.json` 中的 SHA256 hash 与当前 `_raw/` 文件，仅处理新增或变更的素材，跳过未变化的文件。

> **数据安全约束**：`_raw/` 原始素材只读，Agent 不得修改或删除。`raw/` 只追加不覆盖。

---

## 前置准备

1. 读取 `.manifest.json` 获取已处理文件列表及对应 SHA256 hash
2. **备份** `.manifest.json` → `.manifest.json.bak`（每次操作前自动备份）
3. 扫描 `_raw/` 下所有 `.md` 文件，按文件名排序得到当前文件列表
4. 如果 `_raw/` 为空，输出「_raw/ 目录为空，无文件可处理」并终止

---

## Stage 1: Hash 对比与分类

对 `_raw/` 下每个 `.md` 文件：

1. 计算文件内容的 **SHA256 hash**（使用 `sha256sum` 或等价命令）
2. 与 `.manifest.json` 中该文件的记录对比：

| 条件 | 分类 | 操作 |
|------|------|------|
| 文件名不在 manifest.files 中 | `new` | 需要处理 |
| hash 与 manifest 中记录不同 | `changed` | 需要处理 |
| hash 与 manifest 中记录相同 | `unchanged` | 跳过 |
| manifest 中有记录但 _raw/ 中无对应文件 | `deleted` | 输出警告，不删除 wiki 页面 |

3. 输出分类结果：

```
_hash 对比完成_
  新增：N 个（文件列表）
  变更：M 个（文件列表）
  未变：K 个（跳过）
  缺失：J 个（_raw/ 中已不存在，输出警告）
```

4. 如果 `new` + `changed` 为 0，输出「所有文件均为最新，无需更新」并终止

---

## Stage 2: 增量处理（仅 new + changed 文件）

对分类为 `new` 或 `changed` 的文件，逐一执行以下操作：

### 2.1 逐文件处理

对每个待处理文件（按文件名排序）：

1. **显示进度**：`Updating [当前序号/待处理总数] 文件名.md`
2. **读取文件内容**：以 UTF-8 读取。编码异常则跳过并在 `wiki/log.md` 记录：
   ```
   - **编码异常**：`文件名` — 跳过（原因：编码解析失败）
   ```
3. **解析 frontmatter**：解析已有字段，缺失的用合理默认值填充
4. **生成/更新 summary**：阅读全文，生成 ≤ 100 字中文摘要
5. **补全 frontmatter 字段**：确保 title / created / updated / tags / sources / summary / status / entity_type 齐全
6. **提取概念**：识别文中的技术概念、术语、框架名称

### 2.2 概念合并与页面更新

对每个提取出的概念：

1. **检查 wiki/concepts/ 下是否已存在对应页面**
   - 已存在 → 将新来源的内容**追加**到对应章节（不覆盖既有内容）
   - 不存在 → 新建概念页（遵循 `templates/concept-template.md` 格式）
2. **冲突处理**：如果新旧来源对同一概念描述矛盾，保留所有描述并标记 `^[ambiguous]`
3. **更新 frontmatter**：
   - `sources`：追加新来源路径
   - `tags`：合并新旧标签
   - `updated`：更新为当前日期

### 2.3 收录原始素材

- 将已成功处理的 `_raw/` 文件**复制**到 `raw/`（只追加不覆盖）
- `raw/` 中已存在同名文件则跳过

---

## Stage 3: 更新索引与元数据

### 3.1 更新 wiki/index.md

- 为新建的概念页追加表格行（不删除既有条目）
- 格式：`| [[概念名]] | tag1, tag2 | N | active |`
- 按概念名字母排序插入

### 3.2 更新 .manifest.json

**增量更新**（保留未变化文件的记录不变）：

- 新增文件：添加完整记录
- 变更文件：更新 hash、processedAt、concepts 等字段
- 未变文件：保持原记录不动
- 删除文件：保留记录但标记 `status: "source_removed"`

```json
{
  "version": "1.0",
  "created": "保持原值",
  "updated": "当前日期",
  "files": {
    "01-prompt-engineering.md": {
      "sha256": "新的hash值",
      "processedAt": "2026-05-26T23:45:00",
      "status": "success",
      "concepts": ["Prompt Engineering", "Chain of Thought"],
      "entityType": "concept"
    }
  },
  "stats": {
    "totalFiles": "所有已处理文件总数",
    "totalConcepts": "概念总数",
    "lastIngest": "保持原值",
    "lastUpdate": "当前时间戳"
  }
}
```

### 3.3 更新 wiki/log.md

追加本次操作记录：

```markdown
## YYYY-MM-DD HH:mm

- **操作**：`/wiki-update` 增量更新
- **新增**：N 个文件
- **变更**：M 个文件
- **跳过**：K 个未变化文件
- **概念页更新**：列出更新的概念页
- **新建概念页**：列出新建的概念页
```

---

## 断点续传机制

为确保中途中断后能从断点继续：

1. **每处理完一个文件**，立即更新 `.manifest.json` 中该文件的记录（写入新 hash 和 processedAt）
2. **中断恢复**：下次执行时，对比 manifest 中的 hash 与当前文件 hash：
   - 如果一致 → 说明该文件已在上次会话中成功处理，跳过
   - 如果不一致 → 说明该文件在上次会话中未被处理，需要处理
3. 概念页的创建/更新是**幂等操作**：重复执行不会产生重复内容

---

## 最终输出

处理完成后，向用户输出统计摘要：

```
/wiki-update 完成
━━━━━━━━━━━━━━━━━━━━━
新增文件：N 篇
变更文件：M 篇
跳过（未变化）：K 篇
更新概念页：U 个
新建概念页：N 个
已收录到 raw/：X 篇
━━━━━━━━━━━━━━━━━━━━━
处理文件列表：
  - 01-prompt-engineering.md (new)
  - 04-prompt-basics.md (changed)
  ...
```

---

## 约束与安全

- `_raw/` 文件只读，不得修改或删除
- `raw/` 只追加，不覆盖
- `.manifest.json` 操作前必须备份
- 所有文件 UTF-8 无 BOM 编码
- frontmatter 必须包含：title, created, updated, tags, sources, summary, status, entity_type
- 文件名使用 kebab-case
- 概念页更新为幂等操作，重复执行不产生重复内容
