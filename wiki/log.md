---
title: "mwiki 操作历史日志"
created: 2026-05-26
updated: 2026-05-26
tags: [meta, log]
sources: []
summary: "记录知识库所有操作的变更历史"
status: active
entity_type: overview
---

# mwiki 操作历史日志

> 本日志由 Agent 操作自动追加，记录每次 ingest / update / lint 等操作的详细信息。

## 2026-05-26

- **操作**：`/wiki-setup` 初始化
- **内容**：创建六层目录结构、模板文件、核心配置
- **结果**：初始化完成

## 2026-05-27 15:30

- **操作**：`/wiki-ingest` 全量导入
- **输入**：`_raw/` 下 6 个文件
- **结果**：导入 6 篇，提取 11 个概念，合并为 11 个页面
- **跳过**：0 个编码异常
- **标记**：1 个低产文件（`06-quick-notes.md`）
- **已收录到 raw/**：6 篇
- **概念页**：
  - `wiki/concepts/prompt-engineering.md`（来源：01 + 04）
  - `wiki/concepts/rag.md`（来源：02）
  - `wiki/concepts/vector-embedding.md`（来源：03）
  - `wiki/concepts/llm.md`（来源：05）
  - `wiki/concepts/chain-of-thought.md`（来源：01 + 04）
  - `wiki/concepts/few-shot-learning.md`（来源：01 + 04）
  - `wiki/concepts/transformer.md`（来源：05）
  - `wiki/concepts/vector-database.md`（来源：02 + 03）
  - `wiki/concepts/fine-tuning.md`（来源：02 + 05）
  - `wiki/concepts/hallucination.md`（来源：02 + 05）
  - `wiki/concepts/cosine-similarity.md`（来源：03）

## 2026-05-27 15:45

- **操作**：`/wiki-export` 知识图谱导出
- **节点**：14 个（concept 11 / overview 3）
- **边**：40 条
- **输出**：graph.json / graph.graphml / graph.cypher / graph.html
- **着色**：按 entity_type（默认）
