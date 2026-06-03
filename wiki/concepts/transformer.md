---
title: "Transformer"
created: 2026-05-27
updated: 2026-05-27
tags: [transformer, attention, deep-learning, neural-network]
sources:
  - path: _raw/05-llm-overview.md
    provenance: extracted
summary: "基于自注意力机制的深度学习架构，是现代大语言模型的基础。"
status: active
entity_type: concept
---

# Transformer

## 定义

Transformer 是 2017 年由 Google 在论文《Attention Is All You Need》中提出的深度学习架构，核心创新是自注意力机制（Self-Attention）。它是所有现代[[大语言模型]]的基础架构。

## 核心要点

- **自注意力机制**：允许模型在处理序列时关注任意位置的信息
- **并行计算**：相比 RNN/LSTM，Transformer 可并行处理序列，训练效率高
- **位置编码**：通过位置编码解决序列顺序问题
- **多头注意力**：多个注意力头捕获不同维度的语义关系

## 应用场景

- [[大语言模型]]的基础架构（GPT、Claude、BERT 等）
- 机器翻译
- 文本摘要
- 图像处理（Vision Transformer）

## 相关概念

- [[大语言模型]]
- [[Prompt Engineering]]
