---
title: "Prompt Engineering"
created: 2026-05-27
updated: 2026-05-27
tags: [prompt-engineering, LLM, AI, few-shot, chain-of-thought]
sources:
  - path: _raw/01-prompt-engineering.md
    provenance: extracted
  - path: _raw/04-prompt-basics.md
    provenance: extracted
summary: "通过精心设计输入提示引导大语言模型生成高质量输出的技术，包含 Zero-shot、Few-shot、CoT 等核心模式。"
status: active
entity_type: concept
---

# Prompt Engineering

## 定义

Prompt Engineering 是指通过精心设计输入提示（prompt）来引导大语言模型（LLM）生成更准确、更有用的输出的技术。它是与 LLM 交互的核心技能。

Prompt 是用户与大语言模型交互的输入文本。良好的 prompt 设计是获取高质量 AI 输出的关键，核心在于让模型准确理解用户意图。

## 核心要点

### 核心原则

- **明确性**：指令越清晰，输出越准确
- **上下文丰富**：提供充分的背景信息
- **示例驱动**：通过 few-shot examples 展示期望格式
- **分步引导**：将复杂任务拆解为子步骤（[[Chain of Thought]]）
- **约束明确**：设定输出的格式、长度和风格

### Prompt 基本结构

一个完整的 prompt 通常包含：

1. **角色设定**：告诉模型以什么身份回答
2. **背景上下文**：提供必要的背景信息
3. **具体指令**：明确要求模型做什么
4. **输出格式**：指定回答的格式要求
5. **约束条件**：限定范围和边界

### 常用模式

| 模式 | 说明 |
|------|------|
| Zero-shot Prompting | 直接给模型指令，不提供示例，适用于简单任务 |
| [[Few-shot Learning]] | 提供几个输入-输出对作为示例，让模型理解期望模式 |
| [[Chain of Thought]] | 要求模型逐步推理，显著提升复杂问题准确率 |
| Role Prompting | 给模型设定角色，使输出更专业化 |

### 常用技巧

- **明确指令**：将模糊问题改为具体指令，如"写一篇 500 字的技术博客，主题是 Prompt Engineering，面向初级开发者"
- **使用分隔符**：用 ` ``` ` 或 `###` 区分指令和内容
- **明确输出格式**：要求 JSON、Markdown、列表等
- **迭代优化**：根据输出结果不断调整 prompt，记录效果变化
- **系统消息**：使用系统消息设定全局行为

## 应用场景

- 与 [[大语言模型]] 交互获取高质量输出
- 构建 AI 应用的 prompt 模板
- [[RAG]] 系统中的上下文注入设计
- 多轮对话的 prompt 策略优化

## 局限性

- 不同模型对相同 prompt 的响应可能差异很大
- 过于复杂的 prompt 可能导致模型困惑
- prompt 注入攻击是安全风险
- 避免在 prompt 中包含敏感信息
- 注意 token 限制（不同模型有不同上限）

## 实用模板

```
角色：你是一位 [领域] 专家
任务：[具体任务描述]
上下文：[相关背景]
格式要求：[输出格式]
约束：[限制条件]
```

## 相关概念

- [[大语言模型]]
- [[向量嵌入]]
- [[RAG]]
- [[Chain of Thought]]
- [[Few-shot Learning]]
