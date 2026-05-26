---
title: "mwiki 知识库目标"
created: 2026-05-26
updated: 2026-05-26
tags: [meta, purpose]
sources: []
summary: "mwiki 知识库的目标锚定文档，定义知识管理方向和约束"
status: active
entity_type: overview
---

# mwiki 知识库目标

## 愿景

基于 Obsidian Vault 文件系统 + Claude Code CLI Agent，构建 **AI 共治** 的个人知识管理平台。用户负责输入原始素材和意图，Agent 负责整理、归档、查询、报告生成等重复性劳动。

## 核心目标

- **降低上手门槛**：新用户从零到可用知识库 < 10 分钟
- **知识整理自动化**：手动整理操作减少 80%
- **知识资产可视化**：支持 Graph 导出（Gephi / Neo4j / HTML）
- **多 Agent 共享**：一份 Wiki 同时被 Claude Code / Cursor / Codex 等读写
- **历史沉淀**：对话历史自动转化为知识资产

## 知识库范围

- AI / 编程学习笔记的结构化整理
- 跨项目知识聚合与复用
- 对话历史沉淀为可检索知识
- 概念关联与知识图谱可视化

## 数据流

```
_raw/（暂存） → raw/（归档） → wiki/（结构化） → human/（人读） + ai/（AI 路由）
```

## 约束

- 所有知识页面以 `.md` 文件存储，禁止数据库或后端服务作为核心数据层
- `_raw/` 原始素材 Agent 只读，不可修改或删除
- `raw/` 收录层只追加，不可覆盖
- 以 `wiki/` 为唯一真相源
- 文件编码统一 UTF-8（无 BOM）
