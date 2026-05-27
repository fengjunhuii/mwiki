# Wiki Schema

## Domain
PROJECT_NAME — [项目描述]，重点关注 [核心系统] 的架构与实现细节。

## Conventions
- 文件名：小写 + 连字符，无空格（如 `skills-system-architecture.md`）
- 每个 wiki 页面必须以 YAML frontmatter 开头
- 使用 wiki 双向链接（如 [[tool-registry-architecture]]）连接页面（每页至少 2 个出站链接）
- 更新页面时必须更新 `updated` 日期
- 新页面必须添加到 `index.md` 对应分类下
- 每个操作必须追加到 `log.md`

## Frontmatter
```yaml
---
title: 页面标题
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | changelog | overview
tags: [来自下方分类法]
sources: [源码文件路径列表]
---
```

## Tag Taxonomy
- **架构**: architecture, module, component, interface, reliability, extensibility
- **Meta**: comparison, code-pattern, best-practice
- **核心**: [根据项目自定义]
- **性能**: performance, concurrency, caching, optimization
- **安全**: security, authentication, authorization
- **数据**: data-flow, storage, serialization
- **运维**: configuration, deployment, monitoring
- **测试**: testing, quality, coverage

## Page Thresholds
- **创建页面**：当实体/概念在 2+ 源码文件中出现，或是某个模块的核心内容
- **更新已有页面**：当源码提到已覆盖的内容时
- **不创建页面**：对于偶然提及、次要细节或超出领域的内容
- **拆分页面**：超过 ~200 行时拆分为子主题并交叉链接
- **归档页面**：内容被完全取代时移至 `_archive/`，从 index 中移除

## Entity Pages
每个实体一页。包括：
- 概述 / 是什么
- 关键事实（文件路径、类名、关键函数）
- 与其他实体的关系（使用 wiki 双向链接）
- 源码引用

## Concept Pages
每个概念一页。包括：
- 定义 / 解释
- 核心机制 / 设计决策
- 与其他系统的交互
- 已知限制
- 相关概念（使用 wiki 双向链接）

## Update Policy
当新信息与已有内容冲突时：
1. 检查日期 — 较新源码通常覆盖旧源码
2. 如果确实矛盾，同时记录两种说法并注明日期和来源
3. 在 frontmatter 中标记：`contradictions: [page-name]`
4. 在 lint 报告中标记供用户审核
