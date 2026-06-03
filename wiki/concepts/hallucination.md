---
title: "幻觉"
created: 2026-05-27
updated: 2026-05-27
tags: [hallucination, LLM, AI-safety, reliability]
sources:
  - path: _raw/02-rag-basics.md
    provenance: extracted
  - path: _raw/05-llm-overview.md
    provenance: extracted
summary: "大语言模型生成看似合理但实际错误的内容的现象，是 LLM 应用的主要可靠性挑战。"
status: active
entity_type: concept
---

# 幻觉（Hallucination）

## 定义

幻觉是指[[大语言模型]]生成看似合理、连贯但实际不正确或虚构的内容。这是 LLM 应用的主要可靠性挑战之一。

## 核心要点

- 模型基于统计概率生成文本，不保证事实正确性
- 常见类型：事实性错误、编造引用、虚构数据
- 成因：训练数据不完整、知识截止、过度泛化

## 缓解策略

- [[RAG]]：基于真实文档生成回答，提供可追溯来源
- [[Prompt Engineering]]：明确约束输出范围
- 事实核查：对关键输出进行人工或自动验证
- 多模型交叉验证

## 相关概念

- [[大语言模型]]
- [[RAG]]
- [[Prompt Engineering]]
