# mwiki — Obsidian + Claude Code 个人知识库系统

> 基于 Obsidian Vault + Claude Code Agent 的 **AI 共治** 知识管理平台。你负责输入素材，Agent 代管整理、归档、查询、报告和可视化。

---

## 特性

- **四阶段知识导入**：Ingest → Extract → Resolve → Schema，将原始笔记自动转化为结构化知识页面
- **七种实体类型**：concept / tool / person / event / comparison / pattern / overview，每种有专属模板和必需章节
- **语义查询**：完整查询（跨篇章聚合）和快速查询（仅读索引，省 token）
- **知识图谱导出**：JSON / GraphML / Cypher / HTML 四种格式，支持 Gephi / Neo4j / 浏览器可视化
- **对话历史沉淀**：将 Claude / Codex 对话自动转化为可检索的知识资产
- **14+ Agent 共享**：一份 Wiki 同时被 Claude Code / Cursor / Codex / Gemini / Hermes 等读写
- **渐进式上下文加载**：L0-L3 四级 Token 预算，按需加载减少开销
- **双轨知识输出**：`human/` 人读手册 + `ai/` Agent 路由索引

---

## 快速开始

### 前置条件

- [Obsidian](https://obsidian.md) 桌面应用
- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) (`claude` 命令可用)
- Git

### 1. 获取项目

```bash
git clone https://github.com/fengjunhuii/mwiki.git
cd mwiki
```

### 2. 在 Obsidian 中打开

1. 打开 Obsidian → 「打开文件夹作为仓库」
2. 选择 `mwiki/` 根目录
3. Obsidian 会自动识别配置

### 3. 使用 Claude Code 开始管理知识

```bash
# 在 mwiki/ 目录下启动 Claude Code
claude

# 将原始素材放入 _raw/
cp ~/notes/*.md _raw/

# 执行全量导入
> /wiki-ingest
```

### 4. 多 Agent 安装（可选）

```bash
# 将 Skills 链接到 14+ Agent
bash setup.sh /path/to/mwiki
```

---

## 目录结构

```
mwiki/
├── _raw/                            # 暂存层 — 用户存放原始素材（Agent 只读）
│   ├── 01-prompt-engineering.md     #   示例素材：Prompt Engineering
│   ├── 02-rag-basics.md             #   示例素材：RAG 基础
│   ├── 03-vector-embedding.md       #   示例素材：向量嵌入
│   ├── 04-prompt-basics.md          #   示例素材：Prompt 基础（与 01 有重叠概念，测试合并）
│   ├── 05-llm-overview.md           #   示例素材：LLM 概述
│   └── 06-quick-notes.md            #   示例素材：低产文件（测试 low-yield 标记）
│
├── raw/                             # 收录层 — 已归档的素材原文（只追加，不覆盖）
│
├── wiki/                            # 结构化层 — Agent 重写后的知识页面（唯一真相源）
│   ├── concepts/                    #   概念页（跨源合并后的知识页面）
│   ├── topics/                      #   主题页（按领域聚合，entity_type=overview）
│   ├── comparisons/                 #   对比页（多方案分析，entity_type=comparison）
│   ├── patterns/                    #   模式页（方法论/最佳实践，entity_type=pattern）
│   ├── reports/
│   │   ├── daily/                   #   每日知识报告（YYYY-MM-DD.md）
│   │   └── weekly/                  #   每周知识报告
│   ├── graphs/                      #   图谱导出（graph.json / graphml / cypher / html）
│   ├── purpose.md                   #   知识库目标锚定（L1 必读）
│   ├── index.md                     #   全局概念索引（自动维护）
│   └── log.md                       #   操作历史日志（自动维护）
│
├── human/                           # 人读层 — Agent 自动派生的综合文档
│   ├── PROJECT_WIKI.md              #   人读综合手册（9 章：概述/目录/命令/实体类型/Token/安全/约束/性能/多Agent）
│   └── BUSINESS_QA.md               #   业务问卷（Agent 读不出的逻辑，用户填写）
│
├── ai/                              # AI 路由层 — Agent 按任务精准加载的索引
│   ├── _index.json                  #   路由配置（query/ingest/context/reports/export/history/cross-linker/human）
│   ├── L0_profile.md                #   技术约束（~200 token，每次会话必读）
│   ├── L1_architecture.md           #   系统架构总览（~1-2K token，会话开始加载）
│   └── L2_detail/                   #   按需加载详情页（~2-5K token）
│       ├── concepts-summary.md      #     概念摘要
│       └── entity-type-guide.md     #     实体类型推断指南
│
├── templates/                       # 模板文件（9 套）
│   ├── concept-template.md          #   concept 类型模板
│   ├── tool-template.md             #   tool 类型模板
│   ├── person-template.md           #   person 类型模板
│   ├── event-template.md            #   event 类型模板
│   ├── comparison-template.md       #   comparison 类型模板
│   ├── pattern-template.md          #   pattern 类型模板
│   ├── overview-template.md         #   overview 类型模板
│   ├── diary-template.md            #   每日报告模板
│   └── report-template.md           #   每周报告模板
│
├── .skills/                         # mwiki Skill 定义文件（8 个，Agent 读取执行）
│   ├── wiki-ingest.md               #   /wiki-ingest   — 四阶段全量导入
│   ├── wiki-update.md               #   /wiki-update   — 增量更新（SHA256 hash 对比）
│   ├── wiki-query.md                #   /wiki-query    — 语义查询（完整 + quick answer）
│   ├── wiki-lint.md                 #   /wiki-lint     — 质量检查（断链/缺失页/矛盾/过时）
│   ├── wiki-export.md               #   /wiki-export   — 知识图谱导出（4 格式）
│   ├── wiki-daily-report.md         #   /wiki-daily-report — 每日报告生成
│   ├── cross-linker.md              #   /cross-linker  — 自动补充 [[wikilinks]]
│   └── claude-history-ingest.md     #   /claude-history-ingest — Claude 对话历史导入
│
├── .claude/                         # Claude Code 项目级配置
│   ├── commands/
│   │   └── wiki-ingest.md           #   本地 slash command 注册
│   ├── rules/                       #   编码规范（始终生效）
│   │   ├── cplusplus-coding.md      #     C++ 编码规范 V2.1
│   │   ├── python-coding.md         #     Python 编码规范
│   │   ├── markdown-docs.md         #     Markdown 文档规则
│   │   ├── security.md              #     安全规则
│   │   └── thinking.md              #     思考协议
│   ├── skills/                      #   其他 Claude Code Skills（辅助工具）
│   │   ├── acquire-codebase-knowledge/  #  代码库知识获取
│   │   ├── excalidraw-diagram-generator/ # Excalidraw 图表生成
│   │   ├── fireworks-tech-graph/    #     SVG 技术图表生成（7 种风格）
│   │   ├── frontend-design/         #     前端设计
│   │   ├── html-sliders/            #     HTML 幻灯片
│   │   ├── llm-wiki/                #     LLM Wiki（参考实现）
│   │   └── prd-writer/              #     PRD 撰写工具
│   └── settings.json                #   项目级设置
│
├── .cursor/skills/mwiki/            # Cursor Agent symlink（8 个 Skill → .skills/）
│
├── .cache/                          # SHA256 增量缓存（Agent 自动管理）
├── .manifest.json                   # 源文件哈希清单 + 导入进度 + 统计
├── .omc/                            # oh-my-claudecode 插件状态（notepad / sessions / state）
│
├── CLAUDE.md                        # Claude Code 项目级配置（Token 预算 L0-L3 + 编码/目录/操作规范）
├── README.md                        # 本文档
├── user_guide.md                    # 用户指南（14 章，681 行）
├── setup.sh                         # 多 Agent 安装脚本（14 种 Agent，跨平台 symlink/Junction）
└── .gitignore
```

### 数据流

```
_raw/（用户暂存） → raw/（归档备份） → wiki/（结构化知识） → human/（人读） + ai/（Agent 路由）
```

---

## 可用命令

在 Claude Code 中通过 slash command 调用：

| 命令 | 用途 | Token 开销 |
|------|------|-----------|
| `/wiki-ingest` | 四阶段全量导入（Ingest → Extract → Resolve → Schema） | L3 |
| `/wiki-update` | 增量更新（基于 `.manifest.json` SHA256 hash 对比） | L2-L3 |
| `/wiki-query` | 语义查询（完整查询 + quick answer 快速模式） | L1-L3 |
| `/wiki-lint` | 质量检查（断链 / 缺失页 / 矛盾 / 过时） | L2 |
| `/wiki-export` | 知识图谱导出（JSON / GraphML / Cypher / HTML） | L2-L3 |
| `/cross-linker` | 自动补充 [[wikilinks]] | L2-L3 |
| `/claude-history-ingest` | 导入 `~/.claude/` 对话历史 | L3 |
| `/wiki-daily-report` | 每日知识报告生成 | L2 |

---

## 七种实体类型

每个知识页面都有 `entity_type` 标签，Ingest 阶段自动推断：

| 类型 | 适用场景 | 必需章节 | 存放目录 |
|------|---------|---------|---------|
| `concept` | 抽象概念、理论、算法 | 定义 / 核心要点 / 应用场景 / 局限性 | `wiki/concepts/` |
| `tool` | 软件、框架、平台 | 功能 / 安装 / 使用场景 / 替代方案 | `wiki/concepts/` |
| `person` | 人物、团队、组织 | 简介 / 贡献 / 关联项目 | `wiki/concepts/` |
| `event` | 发布、突破、历史节点 | 时间线 / 背景 / 影响 | `wiki/concepts/` |
| `comparison` | 多方案对比分析 | 对比维度 / 优劣 / 选型建议 | `wiki/comparisons/` |
| `pattern` | 方法论、流程、最佳实践 | 问题描述 / 解决方案 / 适用条件 | `wiki/patterns/` |
| `overview` | 领域/子领域总览 | 范围 / 核心概念 / 学习路径 | `wiki/topics/` |

推断优先级：comparison > tool > event > person > pattern > overview > concept（兜底）

---

## 渐进式上下文加载（L0-L3）

| 级别 | Token 量 | 触发时机 | 加载内容 |
|------|---------|---------|---------|
| L0 | ~200 | 每次会话 | `CLAUDE.md` frontmatter |
| L1 | ~1-2K | 会话开始 | `wiki/purpose.md` + `wiki/index.md` |
| L2 | ~2-5K | 搜索/定位 | `ai/L2_detail/` 按需加载 |
| L3 | 5-20K | 深度读写 | 完整文章或原始素材 |

---

## 多 Agent 支持

`setup.sh` 自动将 `.skills/` 链接到以下 Agent：

**全局 Agent**（链接到 `$HOME` 下）：Claude Code、Codex、Gemini CLI、Hermes、OpenClaw、Aider、Copilot、Zed、PearAI

**项目级 Agent**（链接到 Vault 内）：Cursor

```bash
bash setup.sh              # 交互模式
bash setup.sh /path/to/mwiki   # 指定路径
```

---

## 数据安全

- `_raw/` 原始素材：Agent **只读**，不得修改或删除
- `raw/` 收录层：**只追加**，不可覆盖
- `.manifest.json` 每次操作前自动备份为 `.manifest.json.bak`
- 对话历史导入前自动**脱敏**（过滤 API Key / Token 等敏感字段）
- 概念合并冲突标记 `^[ambiguous]`，不自动覆盖，等用户裁决
- 以 `wiki/` 为**唯一真相源**，`human/` 和 `ai/` 为派生视图

---

## 技术栈

- **载体**：Obsidian Vault 文件系统（纯 Markdown，无数据库）
- **Agent**：Claude Code CLI（Skills 以 Markdown 指令集形式定义）
- **编码**：UTF-8（无 BOM）
- **链接格式**：Obsidian 原生 `[[wikilinks]]`
- **Frontmatter**：YAML，必需字段：title / created / updated / tags / summary / entity_type / status / sources

---

## 项目结构来源

本项目融合了四个技术流派的设计思路：

| 流派 | 代表项目 | 借鉴点 |
|------|---------|--------|
| Karpathy Wiki 流 | `ragwiki/karpathy-wiki` | 四阶段流水线 + 7 种实体类型 + L0-L3 Token 预算 |
| Code-to-Wiki 流 | `code2wiki` | 渐进式上下文加载 + 域聚合 |
| Spec Skill 流 | `codebase-knowledge-skills` | 窄范围 Skill 拆分哲学 |
| 知识图谱流 | `dead-reckoning` | 图谱版本 diff + hybrid search |

---

## 许可

MIT License
