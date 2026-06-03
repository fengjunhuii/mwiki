---
title: "向量嵌入"
created: 2026-05-27
updated: 2026-05-27
tags: [vector-embedding, embedding, semantic-search, similarity]
sources:
  - path: _raw/03-vector-embedding.md
    provenance: extracted
  - path: _raw/01-prompt-engineering.md
    provenance: extracted
  - path: _raw/02-rag-basics.md
    provenance: extracted
  - path: _raw/05-llm-overview.md
    provenance: extracted
summary: "将非结构化数据转换为高维数值向量的技术，使语义相近的文本在向量空间中距离更近。"
status: active
entity_type: concept
---

# 向量嵌入（Vector Embedding）

## 定义

向量嵌入是将文本、图像等非结构化数据转换为高维数值向量的技术。在自然语言处理中，向量嵌入使得语义相近的文本在向量空间中距离更近。

## 核心要点

### 嵌入维度

常见的嵌入维度有 768、1024、1536 等。维度越高，表达力越强，但计算成本也越高。

### 余弦相似度

衡量两个向量方向的相似程度，取值范围 [-1, 1]：

- 1 表示完全相同方向
- 0 表示正交（无关）
- -1 表示相反方向

公式：`cos(A, B) = (A · B) / (|A| × |B|)`

### 向量空间

嵌入模型将文本映射到一个高维空间，使得语义相似的文本在空间中靠近。

### 常用嵌入模型

| 模型 | 维度 | 提供方 | 特点 |
|------|------|--------|------|
| text-embedding-3-small | 1536 | OpenAI | 性价比高 |
| text-embedding-3-large | 3072 | OpenAI | 精度高 |
| BGE-large-zh | 1024 | BAAI | 中文优秀 |
| E5-large | 1024 | Microsoft | 多语言 |
| Cohere Embed | 1024 | Cohere | 多语言 |

## 应用场景

- **语义搜索**：基于语义而非关键词匹配进行搜索
- **[[RAG]]**：检索增强生成中的文档检索
- **聚类分析**：对文本进行主题聚类
- **相似度计算**：判断两段文本的语义相似程度
- **推荐系统**：基于内容相似度进行推荐

## 局限性

- **多语言一致性**：不同语言的相同含义文本应映射到相近向量
- **领域适配**：通用模型在专业领域表现可能不佳
- **时效性**：新词、新概念可能无法准确嵌入
- **长文本处理**：长文档需要先切分再嵌入

## 相关概念

- [[RAG]]
- [[大语言模型]]
- [[向量数据库]]
- [[余弦相似度]]
