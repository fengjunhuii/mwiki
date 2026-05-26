---
title: "mwiki 项目综合手册"
created: 2026-05-27
updated: 2026-05-27
tags: [meta, handbook, human]
sources: [wiki/purpose.md, wiki/index.md, CLAUDE.md, ai/_index.json]
summary: "人读综合手册，从 wiki/ 自动派生。内容不一致时以 wiki/ 为准。"
status: active
entity_type: overview
---

# mwiki 项目综合手册

> **派生声明**：本文档由 Agent 从 `wiki/` 自动派生生成。`wiki/` 为唯一真相源，如本文档内容与 `wiki/` 不一致，以 `wiki/` 为准。本文档禁止手动修改业务逻辑段落（标记 `<!-- no-edit -->` 的区域由 Agent 维护）。

## 1. 项目概述

mwiki 是基于 Obsidian Vault 文件系统 + Claude Code CLI Agent 的 **AI 共治** 个人知识管理平台。

- **用户职责**：输入原始素材和意图
- **Agent 职责**：整理、归档、查询、报告生成、图谱可视化等重复性劳动
- **目标**：从"手动管理笔记"到"Agent 代管知识"的范式升级

### 核心目标

| 目标 | 指标 |
|------|------|
| 降低上手门槛 | 新用户从零到可用知识库 < 10 分钟 |
| 知识整理自动化 | 手动整理操作减少 80% |
| 知识资产可视化 | Graph 导出（Gephi / Neo4j / HTML） |
| 多 Agent 共享 | 一份 Wiki 同时被 14+ Agent 读写 |
| 历史沉淀 | 对话历史自动转化为知识资产 |

## 2. 目录结构

```
mwiki/
├── _raw/                  # 用户暂存层（Agent 只读）
├── raw/                   # 已归档素材（Agent 只追加）
├── wiki/                  # 结构化知识（唯一真相源）
│   ├── concepts/          # 概念页（跨源合并）
│   ├── topics/            # 主题页（按领域聚合）
│   ├── comparisons/       # 对比页
│   ├── patterns/          # 模式页
│   ├── reports/daily/     # 日报
│   ├── reports/weekly/    # 周报
│   ├── graphs/            # 图谱导出
│   ├── purpose.md         # 知识库目标
│   ├── index.md           # 全局概念索引
│   └── log.md             # 操作历史日志
├── human/                 # 人读综合手册（本文档所在目录）
├── ai/                    # AI 路由层
│   ├── _index.json        # 路由配置
│   ├── L0_profile.md      # L0 技术约束
│   ├── L1_architecture.md # L1 架构总览
│   └── L2_detail/         # L2 详情页
├── templates/             # 模板文件
├── .cache/                # SHA256 增量缓存
├── .manifest.json         # 文件哈希清单
├── CLAUDE.md              # Claude Code 配置
└── setup.sh               # 多 Agent 安装脚本
```

### 数据流

```
_raw/（暂存） → raw/（归档） → wiki/（结构化） → human/（人读） + ai/（AI 路由）
```

## 3. 可用命令（Skills）

<!-- no-edit: 此区域由 Agent 根据 wiki/ 和 ai/_index.json 自动派生 -->

| 命令 | 用途 | Token 开销 |
|------|------|-----------|
| `/wiki-setup` | 初始化六层目录结构 | L1 |
| `/wiki-ingest` | 四阶段全量导入（Ingest → Extract → Resolve → Schema） | L3 |
| `/wiki-update` | 增量更新（基于 `.manifest.json` SHA256 对比） | L2-L3 |
| `/wiki-query` | 语义查询（完整 + quick answer 模式） | L1-L3 |
| `/wiki-lint` | 质量检查（断链 / 缺失页 / 矛盾 / 过时） | L2 |
| `/wiki-export` | 知识图谱导出（JSON / GraphML / Cypher / HTML） | L2-L3 |
| `/cross-linker` | 自动补充 [[wikilinks]] | L2-L3 |
| `/claude-history-ingest` | 导入 Claude 对话历史 | L3 |
| `/codex-history-ingest` | 导入 Codex 对话历史 | L3 |
| `/wiki-daily-report` | 每日知识报告生成 | L2 |

## 4. 实体类型（Entity Types）

<!-- no-edit: 此区域由 Agent 根据 templates/ 自动派生 -->

| 类型 | 说明 | 必需章节 | 存放目录 |
|------|------|---------|---------|
| concept | 抽象概念、理论、算法 | 定义/核心要点/应用场景/局限性 | `wiki/concepts/` |
| person | 人物、团队、组织 | 简介/贡献/关联项目 | `wiki/concepts/` |
| tool | 软件、框架、平台 | 功能/安装/使用场景/替代方案 | `wiki/concepts/` |
| event | 发布、突破、历史节点 | 时间线/背景/影响 | `wiki/concepts/` |
| comparison | 多方案对比分析 | 对比维度/优劣/选型建议 | `wiki/comparisons/` |
| pattern | 方法论、流程、最佳实践 | 问题描述/解决方案/适用条件 | `wiki/patterns/` |
| overview | 领域/子领域总览 | 范围/核心概念/学习路径 | `wiki/topics/` |

Ingest 阶段按优先级自动推断 `entity_type`：comparison > tool > event > person > pattern > overview > concept（兜底）。

## 5. Token 预算（L0-L3）

| 级别 | Token 量 | 触发时机 | 加载内容 |
|------|---------|---------|---------|
| L0 | ~200 | 每次会话启动 | `ai/L0_profile.md`（技术约束） |
| L1 | ~1-2K | 会话开始 | `wiki/purpose.md` + `ai/L1_architecture.md` |
| L2 | ~2-5K | 搜索/定位阶段 | `ai/L2_detail/` 按需加载 |
| L3 | 5-20K | 深度读写操作 | 完整文章或原始素材 |

## 6. 数据安全规则

- `_raw/` 原始素材：Agent 只读，不得修改或删除
- `raw/` 收录层：只可追加，不可覆盖
- `.manifest.json` 每次操作前自动备份为 `.manifest.json.bak`
- 对话历史导入前必须脱敏（过滤 API Key / Token 等敏感字段）
- 概念合并冲突标记 `^[ambiguous]`，等用户裁决
- 以 `wiki/` 为唯一真相源，`human/` 和 `ai/` 为派生视图

## 7. 技术约束

- 所有知识页面以 `.md` 文件存储，禁止数据库或后端服务作为核心数据层
- Frontmatter 使用 YAML 格式，必需字段：title / created / updated / tags / summary / entity_type / status / sources
- Wikilinks 使用 Obsidian 原生 `[[页面名]]` 格式
- 文件编码统一 UTF-8（无 BOM）
- 文件名使用 kebab-case

## 8. 性能基准

| 操作 | 规模 | 耗时上限 |
|------|------|---------|
| 全量 Ingest | 100 篇 × ~3000 字 | < 10 分钟 |
| 查询响应 | - | < 30 秒 |
| Graph 导出 | 500 节点 | < 1 分钟 |
| 增量 Update | 变更 5 篇 | < 2 分钟 |

## 9. 多 Agent 支持

`setup.sh` 自动将 Skills symlink 到以下 Agent 的全局 skills 目录：

**全局 Agent**（skills 安装到 `$HOME` 下）：Claude Code、Cursor、Codex、Gemini CLI、Hermes、OpenClaw、Aider、Copilot、Zed、PearAI

**项目级 Agent**（skills 安装到 Vault 内）：Devika、Cline、Continue、Windsurf
