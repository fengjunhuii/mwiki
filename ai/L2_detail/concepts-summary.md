---
title: "L2 概念摘要"
created: 2026-05-27
updated: 2026-05-27
tags: [meta, L2, concepts]
sources: []
summary: "搜索定位阶段按需加载的概念摘要，用于快速匹配和定位"
status: active
entity_type: overview
---

# L2 概念摘要

> 本文件由 `/wiki-ingest` 和 `/wiki-update` 自动维护。
> 每个概念仅保留一行摘要，完整内容在 `wiki/concepts/` 对应页面（L3）。

## 使用方式

1. 用户发起查询或搜索时，Agent 先读本文件定位候选概念
2. 确认相关概念后，再加载对应的 L3 完整页面
3. 本文件控制在 2-5K token 以内，仅包含概念名和一句话摘要

## 概念列表

| 概念名 | entity_type | 一句话摘要 | 页面路径 |
|--------|-------------|-----------|---------|
<!-- 条目由 Agent 自动添加，格式：| 概念名 | concept | 摘要 | wiki/concepts/concept-name.md | -->

## 匹配策略

- **精确匹配**：查询词与概念名完全一致
- **别名匹配**：查询词命中 frontmatter aliases 字段
- **标签匹配**：查询词命中概念 tags 中的标签
- **语义关联**：查询词与概念摘要有语义重叠，按相关度排序
