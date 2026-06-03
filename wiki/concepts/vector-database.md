---
title: "向量数据库"
created: 2026-05-27
updated: 2026-05-27
tags: [vector-database, vector-search, similarity, embedding]
sources:
  - path: _raw/02-rag-basics.md
    provenance: extracted
  - path: _raw/03-vector-embedding.md
    provenance: extracted
summary: "存储和检索向量数据的专用数据库，支持高维向量的相似度搜索。"
status: active
entity_type: concept
---

# 向量数据库

## 定义

向量数据库是存储和检索[[向量嵌入]]数据的专用数据库，支持在高维向量空间中进行快速相似度搜索，是 [[RAG]] 架构的核心组件。

## 核心要点

### 常用方案

| 数据库 | 特点 |
|--------|------|
| ChromaDB | 开源、轻量、适合原型 |
| Pinecone | 托管服务、生产级 |
| Milvus | 开源、高性能、分布式 |
| FAISS | Meta 开源、库级、高性能 |

### 核心操作

1. **写入**：将[[向量嵌入]]连同元数据存入数据库
2. **检索**：给定查询向量，返回最相似的 K 个向量
3. **过滤**：结合元数据过滤和向量搜索

## 应用场景

- [[RAG]] 系统的文档检索
- 语义搜索引擎
- 推荐系统的物品相似度计算
- 图像/音频检索

## 相关概念

- [[向量嵌入]]
- [[RAG]]
- [[余弦相似度]]
