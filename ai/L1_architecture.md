---
title: "L1 架构总览"
created: 2026-05-27
updated: 2026-05-27
tags: [meta, L1, architecture]
sources: []
summary: "会话启动时加载的架构总览，含 Concept Index 和 Dashboard"
status: active
entity_type: overview
---

# L1 架构总览

## 数据流

```
_raw/（暂存） → raw/（归档） → wiki/（结构化） → human/（人读） + ai/（AI 路由）
```

## Concept Index

概念索引由 `/wiki-ingest` 自动维护，存储在 `wiki/index.md`。

按 entity_type 分目录存放：

| 类型 | 目录 | 必需章节 |
|------|------|---------|
| concept | `wiki/concepts/` | 定义/核心要点/应用场景/局限性 |
| person | `wiki/concepts/` | 简介/贡献/关联项目 |
| tool | `wiki/concepts/` | 功能/安装/使用场景/替代方案 |
| event | `wiki/concepts/` | 时间线/背景/影响 |
| comparison | `wiki/comparisons/` | 对比维度/优劣/选型建议 |
| pattern | `wiki/patterns/` | 问题描述/解决方案/适用条件 |
| overview | `wiki/topics/` | 范围/核心概念/学习路径 |

## Dashboard

### 可用 Skill

| 指令 | 用途 | Token 开销 |
|------|------|-----------|
| `/wiki-ingest` | 四阶段全量导入 | L3 |
| `/wiki-update` | 增量更新（SHA256） | L2-L3 |
| `/wiki-query` | 语义查询（full/quick） | L1-L3 |
| `/wiki-lint` | 质量检查 | L2 |
| `/wiki-export` | 图谱导出（4 格式） | L2-L3 |
| `/cross-linker` | 自动补充 wikilinks | L2-L3 |
| `/claude-history-ingest` | 对话历史导入 | L3 |
| `/wiki-daily-report` | 每日知识报告 | L2 |

### 路由规则

完整路由定义在 `ai/_index.json`，按任务类型加载对应级别：

- **查询**：quick → `wiki/index.md`（L1），full → `wiki/concepts/`（L3）
- **导入**：source `_raw/` → output `wiki/`（L3）
- **更新**：对比 `.manifest.json` hash（L2-L3）
- **导出**：扫描 `wiki/` → 写入 `wiki/graphs/`（L2）

### 增量缓存

`.manifest.json` 记录每个文件的 SHA256 hash 和处理时间，支持断点续传。
`.cache/` 目录存放中间计算结果，Agent 自动管理。
