---
title: "余弦相似度"
created: 2026-05-27
updated: 2026-05-27
tags: [cosine-similarity, similarity-metric, vector, math]
sources:
  - path: _raw/03-vector-embedding.md
    provenance: extracted
summary: "衡量两个向量方向相似程度的指标，是向量检索中最常用的距离度量。"
status: active
entity_type: concept
---

# 余弦相似度

## 定义

余弦相似度（Cosine Similarity）衡量两个向量方向的相似程度，取值范围 [-1, 1]。是[[向量嵌入]]检索中最常用的相似度度量。

## 核心要点

- **1** 表示完全相同方向
- **0** 表示正交（无关）
- **-1** 表示相反方向
- 公式：`cos(A, B) = (A · B) / (|A| × |B|)`
- 只关注方向，不受向量长度影响

## 应用场景

- [[向量数据库]]中的相似度检索
- [[RAG]] 系统的文档匹配
- 文本语义相似度计算
- 推荐系统的物品匹配

## 相关概念

- [[向量嵌入]]
- [[向量数据库]]
- [[RAG]]
