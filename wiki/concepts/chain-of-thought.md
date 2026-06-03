---
title: "Chain of Thought"
created: 2026-05-27
updated: 2026-05-27
tags: [chain-of-thought, CoT, reasoning, LLM, prompt-engineering]
sources:
  - path: _raw/01-prompt-engineering.md
    provenance: extracted
  - path: _raw/04-prompt-basics.md
    provenance: extracted
summary: "要求大语言模型逐步推理的提示技术，显著提升复杂问题的准确率。"
status: active
entity_type: concept
---

# Chain of Thought（思维链）

## 定义

Chain of Thought（CoT）是一种 [[Prompt Engineering]] 技术，要求[[大语言模型]]逐步推理而非直接给出答案，显著提升复杂问题的准确率。

## 核心要点

- 在 prompt 中加入"让我们一步一步思考"即可触发
- 将复杂任务拆解为子步骤，每步推理可见
- 适用于数学推理、逻辑分析、多步决策等场景
- 可与 [[Few-shot Learning]] 结合，提供推理链示例

## 应用场景

- 数学问题求解
- 多步逻辑推理
- 复杂决策分析
- 代码调试与错误定位

## 局限性

- 增加 token 消耗（输出更长）
- 简单任务不需要，反而降低效率
- 推理链中某步出错会导致后续全错

## 相关概念

- [[Prompt Engineering]]
- [[Few-shot Learning]]
- [[大语言模型]]
