# Prompt Engineering 技巧

## 什么是 Prompt Engineering

Prompt Engineering 是指通过精心设计输入提示（prompt）来引导大语言模型（LLM）生成更准确、更有用的输出的技术。它是与 LLM 交互的核心技能。

## 核心原则

- **明确性**：指令越清晰，输出越准确
- **上下文丰富**：提供充分的背景信息
- **示例驱动**：通过 few-shot examples 展示期望格式
- **分步引导**：将复杂任务拆解为子步骤（Chain of Thought）
- **约束明确**：设定输出的格式、长度和风格

## 常用模式

### Zero-shot Prompting
直接给模型指令，不提供示例。适用于简单任务。

### Few-shot Prompting
提供几个输入-输出对作为示例，让模型理解期望的模式。

### Chain of Thought (CoT)
要求模型逐步推理，显著提升复杂问题的准确率。可以在 prompt 中加入"让我们一步一步思考"。

### Role Prompting
给模型设定角色（如"你是一位资深 Python 工程师"），使输出更专业。

## 最佳实践

1. 使用分隔符（如 ``` 或 ###）区分指令和内容
2. 明确输出格式要求（JSON、Markdown、列表等）
3. 对于长文档，先要求摘要再提问
4. 迭代优化 prompt，记录效果变化
5. 使用系统消息设定全局行为

## 局限性

- 不同模型对相同 prompt 的响应可能差异很大
- 过于复杂的 prompt 可能导致模型困惑
- prompt 注入攻击是安全风险

## 相关概念

- [[大语言模型]]
- [[向量嵌入]]
- [[RAG]]
