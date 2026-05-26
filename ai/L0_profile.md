---
title: "L0 技术约束"
created: 2026-05-27
updated: 2026-05-27
tags: [meta, L0, constraint]
sources: []
summary: "每次会话必读的技术约束，控制在 200 token 以内"
status: active
entity_type: overview
---

# L0 技术约束

## 核心规则

- **存储**：仅 Markdown 文件，禁止数据库或后端服务
- **编码**：UTF-8 无 BOM
- **Frontmatter 必需字段**：title / created / updated / tags / summary / entity_type / status / sources
- **数据安全**：`_raw/` 只读、`raw/` 只追加、`wiki/` 为唯一真相源
- **冲突**：合并冲突标记 `^[ambiguous]`，等用户裁决
- **文件名**：kebab-case

## Entity Types

concept | person | tool | event | comparison | pattern | overview

## Token 预算

| 级别 | 触发时机 | 加载内容 |
|------|---------|---------|
| L0 | 每次会话 | 本文件 |
| L1 | 会话开始 | `wiki/purpose.md` + `ai/L1_architecture.md` |
| L2 | 搜索定位 | `ai/L2_detail/` 按需 |
| L3 | 深度读写 | 完整概念页或原始素材 |
