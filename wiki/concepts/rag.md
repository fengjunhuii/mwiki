---
title: "RAG（检索增强生成）"
created: 2026-05-27
updated: 2026-05-27
tags: [RAG, retrieval-augmented-generation, LLM, vector-database, hallucination]
sources:
  - path: _raw/02-rag-basics.md
    provenance: extracted
  - path: _raw/01-prompt-engineering.md
    provenance: extracted
  - path: _raw/05-llm-overview.md
    provenance: extracted
summary: "将信息检索与大语言模型生成结合的技术架构，通过检索相关文档减少幻觉并提升知识实时性。"
status: active
entity_type: concept
---

# RAG（检索增强生成）

## 定义

RAG（Retrieval-Augmented Generation）是一种将信息检索与[[大语言模型]]生成相结合的技术架构。它通过在生成回答前先检索相关文档，有效缓解 LLM 的[[幻觉]]问题和知识过时问题。

## 核心要点

### 工作流程

1. **文档索引**：将知识库文档切分为 chunk，通过[[向量嵌入]]模型转换为向量，存入[[向量数据库]]
2. **查询检索**：用户提问时，将问题转换为向量，在向量数据库中检索最相关的文档片段
3. **上下文注入**：将检索到的文档片段作为上下文拼接到 [[Prompt Engineering|prompt]] 中
4. **生成回答**：LLM 基于检索到的上下文生成回答

### 核心组件

| 组件 | 说明 | 常用方案 |
|------|------|---------|
| 向量嵌入模型 | 将文本转换为高维向量 | OpenAI text-embedding-ada-002, BGE, E5 |
| 向量数据库 | 存储和检索向量 | ChromaDB, Pinecone, Milvus, FAISS |
| 文档切分策略 | 将长文档分段处理 | 固定长度、按段落/章节、语义切分 |

## 应用场景

- **企业知识库**：基于内部文档的智能问答
- **客服系统**：基于产品文档的自动回答
- **研究助手**：基于论文库的文献检索与综述
- **代码助手**：基于代码库的智能补全

## 局限性

- 检索质量直接影响回答质量
- 文档切分粒度需要调优
- 多跳推理场景下效果有限
- 向量相似度不等于语义相关度

## 与 Fine-tuning 的对比

| 维度 | RAG | [[Fine-tuning]] |
|------|-----|-----------------|
| 知识更新 | 实时 | 需要重新训练 |
| 成本 | 较低 | 较高 |
| 可解释性 | 强（可引用来源） | 弱 |
| 适用场景 | 知识密集型任务 | 风格/格式适配 |

## 相关概念

- [[大语言模型]]
- [[向量嵌入]]
- [[向量数据库]]
- [[幻觉]]
- [[Prompt Engineering]]
- [[Fine-tuning]]
