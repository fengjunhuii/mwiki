---
title: "L2 Entity Type 推断规则"
created: 2026-05-27
updated: 2026-05-27
tags: [meta, L2, entity-type]
sources: []
summary: "Ingest/Update 阶段按需加载的 entity_type 推断规则和模板路由"
status: active
entity_type: overview
---

# L2 Entity Type 推断规则

## 推断优先级

按以下顺序匹配信号关键词，首个命中即确定类型：

| 优先级 | entity_type | 信号关键词 | 目标模板 |
|--------|-------------|-----------|---------|
| 1 | comparison | 对比、比较、vs、versus、优劣、选型 | `templates/comparison-template.md` |
| 2 | tool | 工具、框架、库、平台、软件、SDK、CLI | `templates/tool-template.md` |
| 3 | event | 发布、版本、突破、里程碑、更新日志 | `templates/event-template.md` |
| 4 | person | 人物、团队、组织、作者、贡献者 | `templates/person-template.md` |
| 5 | pattern | 模式、最佳实践、方法论、流程、范式 | `templates/pattern-template.md` |
| 6 | overview | 总览、概述、入门、指南、介绍 | `templates/overview-template.md` |
| 7 | concept | （兜底，无匹配信号时） | `templates/concept-template.md` |

## 路由规则

| entity_type | 目标子目录 | 说明 |
|-------------|-----------|------|
| concept | `wiki/concepts/` | 默认子目录 |
| person | `wiki/concepts/` | 人物页归入概念目录 |
| tool | `wiki/concepts/` | 工具页归入概念目录 |
| event | `wiki/concepts/` | 事件页归入概念目录 |
| comparison | `wiki/comparisons/` | 独立对比目录 |
| pattern | `wiki/patterns/` | 独立模式目录 |
| overview | `wiki/topics/` | 归入主题目录 |

## 推断注意事项

- 推断结果写入 frontmatter 的 `entity_type` 字段
- 用户可随时手动修正 `entity_type`，Agent 不得覆盖手动修改
- 修正后需将页面移动到对应目标子目录
- 多信号冲突时取最高优先级（comparison > tool > ... > concept）
