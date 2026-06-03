---
title: "Fine-tuning"
created: 2026-05-27
updated: 2026-05-27
tags: [fine-tuning, model-training, LLM, transfer-learning]
sources:
  - path: _raw/02-rag-basics.md
    provenance: extracted
  - path: _raw/05-llm-overview.md
    provenance: extracted
summary: "在预训练模型基础上使用特定领域数据进行二次训练，使模型适配特定任务或风格。"
status: active
entity_type: concept
---

# Fine-tuning（模型微调）

## 定义

Fine-tuning 是在已预训练的[[大语言模型]]基础上，使用特定领域或任务的标注数据进行二次训练，使模型适配特定任务、风格或领域知识的技术。

## 核心要点

- 基于预训练模型的权重继续训练，而非从头开始
- 所需数据量远小于预训练（数千到数万条）
- 可针对特定任务（分类、生成、翻译等）优化
- 常见方法：全量微调、LoRA、QLoRA 等

## 与 RAG 的对比

| 维度 | [[RAG]] | Fine-tuning |
|------|---------|-------------|
| 知识更新 | 实时（更新知识库） | 需要重新训练 |
| 成本 | 较低 | 较高 |
| 可解释性 | 强（可引用来源） | 弱 |
| 适用场景 | 知识密集型任务 | 风格/格式适配 |

## 应用场景

- 特定领域知识注入（医疗、法律、金融）
- 输出风格定制（品牌语气、写作风格）
- 特定任务优化（摘要、分类、实体提取）

## 相关概念

- [[大语言模型]]
- [[RAG]]
