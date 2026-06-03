---
title: "Few-shot Learning"
created: 2026-05-27
updated: 2026-05-27
tags: [few-shot, in-context-learning, LLM, prompt-engineering]
sources:
  - path: _raw/01-prompt-engineering.md
    provenance: extracted
  - path: _raw/04-prompt-basics.md
    provenance: extracted
summary: "通过提供少量输入-输出示例引导模型理解期望模式的提示技术。"
status: active
entity_type: concept
---

# Few-shot Learning（少样本学习）

## 定义

Few-shot Learning 是一种 [[Prompt Engineering]] 技术，通过在 prompt 中提供几个输入-输出对作为示例，让[[大语言模型]]理解期望的模式并按此格式生成回答。

## 核心要点

- 提供输入-输出的示例，让模型理解期望的模式
- 示例数量通常 2-5 个，过多会消耗上下文窗口
- 无需示例时使用 Zero-shot（直接给指令）
- 示例的质量和代表性直接影响输出质量

## 应用场景

- 格式化输出（如要求 JSON、表格等特定格式）
- 分类任务（提供各类别的示例）
- 风格模仿（提供目标风格的写作示例）
- 翻译任务（提供源语言-目标语言对）

## 相关概念

- [[Prompt Engineering]]
- [[Chain of Thought]]
- [[大语言模型]]
