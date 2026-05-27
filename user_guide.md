# mwiki 用户指南

> 从零开始使用 mwiki 知识库系统的完整指南。覆盖安装、日常使用、高级功能和故障排查。

---

## 目录

- [1. 安装与初始化](#1-安装与初始化)
- [2. 完整目录结构](#2-完整目录结构)
- [3. 日常使用流程](#3-日常使用流程)
- [4. 命令详解](#4-命令详解)
- [5. 实体类型系统](#5-实体类型系统)
- [6. Token 预算与性能优化](#6-token-预算与性能优化)
- [7. 知识图谱可视化](#7-知识图谱可视化)
- [8. 多 Agent 安装](#8-多-agent-安装)
- [9. 对话历史导入](#9-对话历史导入)
- [10. 每日报告](#10-每日报告)
- [11. 数据安全与约束](#11-数据安全与约束)
- [12. 目录权限速查表](#12-目录权限速查表)
- [13. Frontmatter 规范](#13-frontmatter-规范)
- [14. 故障排查](#14-故障排查)
- [15. 常见问题](#15-常见问题)

---

## 1. 安装与初始化

### 1.1 环境要求

| 工具 | 用途 | 安装方式 |
|------|------|---------|
| Obsidian | 可视化浏览知识库 | [obsidian.md](https://obsidian.md) 下载安装 |
| Claude Code CLI | Agent 执行引擎 | `npm install -g @anthropic-ai/claude-code` |
| Git | 版本管理 | 系统包管理器安装 |
| Python 3.10+（可选） | Graph 导出脚本 | [python.org](https://python.org) 下载 |

### 1.2 获取项目

```bash
git clone https://github.com/fengjunhuii/mwiki.git
cd mwiki
```

### 1.3 在 Obsidian 中打开

1. 启动 Obsidian
2. 点击「打开文件夹作为仓库」
3. 选择 `mwiki/` 目录
4. Obsidian 自动识别目录结构

### 1.4 验证安装

```bash
# 在 mwiki/ 目录下启动 Claude Code
claude

# 验证目录结构已就绪
> ls _raw/ wiki/ templates/ .manifest.json
```

如果以上目录和文件都存在，说明初始化完成。

---

## 2. 完整目录结构

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
│   ├── PROJECT_WIKI.md              #   人读综合手册（9 章）
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
│   ├── concept-template.md          #   concept 类型：定义/核心要点/应用场景/局限性
│   ├── tool-template.md             #   tool 类型：功能/安装/使用场景/替代方案
│   ├── person-template.md           #   person 类型：简介/贡献/关联项目
│   ├── event-template.md            #   event 类型：时间线/背景/影响
│   ├── comparison-template.md       #   comparison 类型：对比维度/优劣/选型建议
│   ├── pattern-template.md          #   pattern 类型：问题描述/解决方案/适用条件
│   ├── overview-template.md         #   overview 类型：范围/核心概念/学习路径
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
├── README.md                        # 项目概览
├── user_guide.md                    # 本文档（用户指南）
├── setup.sh                         # 多 Agent 安装脚本（14 种 Agent，跨平台 symlink/Junction）
└── .gitignore
```

### 数据流

```
_raw/（用户暂存） → raw/（归档备份） → wiki/（结构化知识） → human/（人读） + ai/（Agent 路由）
```

### 六层架构说明

| 层级 | 目录 | 职责 | 用户权限 | Agent 权限 |
|------|------|------|---------|-----------|
| 暂存层 | `_raw/` | 用户存放原始素材的入口 | 可写 | 只读 |
| 收录层 | `raw/` | 已归档的素材原文 | 只读 | 只追加 |
| 结构化层 | `wiki/` | LLM 重写后的结构化知识页面 | 可编辑 | 读写 |
| 人读层 | `human/` | 给人看的综合手册和业务问卷 | 审阅 | 写入 |
| AI 路由层 | `ai/` | Agent 按任务类型精准加载的路由索引 | 只读 | 读写 |
| 缓存层 | `.cache/` | SHA256 增量缓存，跳过未变化资料 | 无感知 | 自动管理 |

---

## 3. 日常使用流程

### 2.1 典型工作日

```
08:00  将昨天的笔记、文章、对话记录拖入 _raw/
08:05  执行 /wiki-update（增量更新新素材）
08:10  执行 /wiki-query 查找需要的知识
18:00  执行 /wiki-daily-report 生成当日知识报告
```

### 2.2 首次使用

```
1. 将所有待整理的笔记放入 _raw/
2. 执行 /wiki-ingest（全量导入）
3. 在 Obsidian 中浏览 wiki/ 下的结构化页面
4. 手动修正不准确的 entity_type 或标签
5. 执行 /cross-linker 补充知识关联
6. 执行 /wiki-export 生成知识图谱
```

### 2.3 素材准备规范

放入 `_raw/` 的文件应遵循以下规范：

- **格式**：Markdown（`.md`）
- **编码**：UTF-8（无 BOM）
- **建议包含**：一级标题（`#`）、合理的段落结构
- **不需要**：完美的 frontmatter（Agent 会自动补全）

示例素材：

```markdown
# Prompt Engineering 技巧

Prompt Engineering 是设计和优化输入提示的技术...

## 主要方法

### Chain of Thought (CoT)
通过分步推理引导模型...

### Few-Shot Learning
提供少量示例...
```

---

## 4. 命令详解

### 3.1 `/wiki-ingest` — 全量导入

**用途**：首次导入或重新处理所有 `_raw/` 素材。

**流程**：

```
Stage 1: Ingest（收录）
  ├── 逐文件读取 _raw/ 下所有 .md
  ├── 生成摘要（summary）
  ├── 推断 entity_type
  └── 计算 SHA256 hash

Stage 2: Extract（提取）
  ├── 提取概念/实体/关系三元组
  └── 标记低产文件（low-yield）

Stage 3: Resolve（合并）
  ├── 同概念跨文件归一
  ├── 选择实体类型模板
  ├── 创建 wiki/ 页面
  └── 冲突标记 ^[ambiguous]

Stage 4: Schema（更新索引）
  ├── 更新 wiki/index.md
  ├── 更新 .manifest.json
  └── 更新 wiki/log.md
```

**使用**：

```bash
> /wiki-ingest
```

**输出示例**：

```
/wiki-ingest 完成
━━━━━━━━━━━━━━━━━━━━━
导入文件：6 篇
提取概念：12 个
合并页面：8 个（wiki/concepts/ 下）
跳过（编码异常）：0 个
标记（低产文件）：1 个
已收录到 raw/：6 篇
━━━━━━━━━━━━━━━━━━━━━
```

### 3.2 `/wiki-update` — 增量更新

**用途**：只处理新增或变更的文件，跳过未变化的素材。

**机制**：对比 `.manifest.json` 中的 SHA256 hash，仅处理 hash 不一致或未记录的文件。

**使用**：

```bash
> /wiki-update
```

**适用场景**：
- 往 `_raw/` 添加了新笔记
- 修改了 `_raw/` 中已有笔记的内容

### 3.3 `/wiki-query` — 知识查询

**用途**：在知识库中语义检索。

**完整查询**（读取索引 + 全文）：

```bash
> /wiki-query LangChain Memory 模块有几种类型
```

**快速查询**（仅读索引，省 token）：

```bash
> /wiki-query quick answer Prompt Engineering 的核心技巧
```

**输出格式**：

```
## 查询结果：LangChain Memory 模块类型

**命中来源：** 04 篇 + 11 篇 + 19 篇

### 三种 Memory 类型
1. ConversationBufferMemory — 完整保留对话历史
2. ConversationSummaryMemory — LLM 压缩摘要
3. VectorStoreRetrieverMemory — 向量检索长期记忆

**原文链接：** [[04-memory-basics]] [[11-advanced-memory]] [[19-rag-memory]]
```

### 3.4 `/wiki-lint` — 质量检查

**用途**：检测知识库中的问题。

**检测项**：

| 检测类型 | 说明 |
|---------|------|
| 断链 | `[[wikilink]]` 指向不存在的页面 |
| 缺失页 | 概念索引中引用但未创建的页面 |
| 冲突 | 标记了 `^[ambiguous]` 的待裁决内容 |
| 过时 | `status: deprecated` 但仍被引用的页面 |

**使用**：

```bash
> /wiki-lint
```

**输出示例**：

```
/wiki-lint 检查完成
━━━━━━━━━━━━━━━━━━━━━
断链：3 个（[[xxx]] 页面不存在）
缺失页：1 个（[[yyy]] 在索引中但未创建）
冲突：0 个
过时：1 个（[[zzz]] 已标记 deprecated）
━━━━━━━━━━━━━━━━━━━━━
```

### 3.5 `/wiki-export` — 知识图谱导出

**用途**：从 `wiki/` 提取概念节点和 wikilink 边，生成图谱文件。

**输出格式**：

| 文件 | 用途 | 使用方式 |
|------|------|---------|
| `graph.json` | 通用节点/边 JSON | 自定义程序读取 |
| `graph.graphml` | Gephi 网络分析 | Gephi 导入 |
| `graph.cypher` | Neo4j 图数据库 | Neo4j 执行 |
| `graph.html` | 交互式可视化 | 浏览器打开 |

**使用**：

```bash
> /wiki-export
```

**查看 HTML 图谱**：

```bash
# 直接双击打开
start wiki/graphs/graph.html     # Windows
open wiki/graphs/graph.html      # macOS
xdg-open wiki/graphs/graph.html  # Linux
```

### 3.6 `/cross-linker` — 自动补链

**用途**：扫描 `wiki/` 页面，将提到其他概念但未添加 wikilink 的地方自动补充 `[[链接]]`。

**使用**：

```bash
> /cross-linker
```

**限制**（防止过度链接）：
- 每次运行最多 200 处替换
- 每个文件最多 30 处替换
- 每个术语在每个文件中最多替换 3 次

### 3.7 `/claude-history-ingest` — 对话历史导入

**用途**：将 `~/.claude/` 下的历史对话导入知识库。

**处理流程**：
1. 扫描对话记录文件
2. 过滤敏感信息（API Key、Token 等）
3. 提取有价值的知识点
4. 创建或合并到对应概念页

**使用**：

```bash
> /claude-history-ingest
```

### 3.8 `/wiki-daily-report` — 每日报告

**用途**：扫描当日编辑的 `wiki/` 文档，按模板生成日报。

**使用**：

```bash
> /wiki-daily-report
```

**输出位置**：`wiki/reports/daily/YYYY-MM-DD.md`

---

## 5. 实体类型系统

### 4.1 概述

每个 `wiki/` 页面都有一个 `entity_type` 字段，决定页面结构和必需章节。Ingest 阶段自动推断，用户可手动修正。

### 4.2 推断规则

按以下优先级从高到低匹配：

| 优先级 | 类型 | 匹配信号 |
|--------|------|---------|
| 1 | `comparison` | "对比"、"比较"、"vs"、"选型"、"优劣" |
| 2 | `tool` | "安装"、"配置"、"使用方法"、"API"，主体描述软件/框架 |
| 3 | `event` | 具体日期 + 事件描述，"发布"、"上线"、"突破" |
| 4 | `person` | "简介"、"贡献"、"成就"，主体描述人物/团队 |
| 5 | `pattern` | "步骤"、"流程"、"方案"、"实践"，描述方法论 |
| 6 | `overview` | "概述"、"总览"、"入门"、"全景"，描述领域全貌 |
| 7 | `concept` | 默认兜底 |

### 4.3 手动修正

直接编辑页面 frontmatter 中的 `entity_type` 字段：

```yaml
---
title: "React vs Vue"
entity_type: comparison    # 可手动修改
---
```

修改后下次 Ingest 不会覆盖用户的手动修正。

### 4.4 各类型模板

每种实体类型都有对应的模板文件：

| 类型 | 模板文件 | 必需章节 |
|------|---------|---------|
| `concept` | `templates/concept-template.md` | 定义、核心要点、应用场景、局限性 |
| `tool` | `templates/tool-template.md` | 功能、安装、使用场景、替代方案 |
| `person` | `templates/person-template.md` | 简介、贡献、关联项目 |
| `event` | `templates/event-template.md` | 时间线、背景、影响 |
| `comparison` | `templates/comparison-template.md` | 对比维度、优劣分析、选型建议 |
| `pattern` | `templates/pattern-template.md` | 问题描述、解决方案、适用条件 |
| `overview` | `templates/overview-template.md` | 范围、核心概念、学习路径 |

---

## 6. Token 预算与性能优化

### 5.1 四级加载策略

| 级别 | Token 量 | 触发时机 | 加载内容 |
|------|---------|---------|---------|
| L0 | ~200 | 每次会话启动 | `CLAUDE.md` frontmatter |
| L1 | ~1-2K | 会话开始 | `wiki/purpose.md` + `wiki/index.md` |
| L2 | ~2-5K | 搜索/定位 | `ai/L2_detail/` 按需加载 |
| L3 | 5-20K | 深度读写 | 完整文章或原始素材 |

### 5.2 省 Token 技巧

1. **使用快速查询**：`/wiki-query quick answer ...` 仅读索引
2. **增量更新代替全量导入**：日常使用 `/wiki-update` 代替 `/wiki-ingest`
3. **分批导入**：大量素材分批放入 `_raw/`，每批 10-20 篇
4. **避免不必要的重新导入**：已处理的素材不要再次放入 `_raw/`

---

## 7. 知识图谱可视化

### 6.1 生成图谱

```bash
> /wiki-export
```

文件输出到 `wiki/graphs/`。

### 6.2 浏览器可视化

直接打开 `wiki/graphs/graph.html`，可交互式浏览概念关系网络。

### 6.3 Gephi 分析

1. 打开 Gephi
2. 文件 → 打开 → 选择 `wiki/graphs/graph.graphml`
3. 运行布局算法（推荐 ForceAtlas 2）
4. 按概念类型或标签着色

### 6.4 Neo4j 导入

```bash
# 在 Neo4j Browser 中执行
:play wiki/graphs/graph.cypher
```

或通过 cypher-shell：

```bash
cypher-shell -u neo4j -p password < wiki/graphs/graph.cypher
```

---

## 8. 多 Agent 安装

### 7.1 运行安装脚本

```bash
# 交互模式（提示输入 Vault 路径）
bash setup.sh

# 指定路径模式
bash setup.sh /path/to/mwiki
```

### 7.2 支持的 Agent

**全局 Agent**（skills 安装到 `$HOME` 下）：

| Agent | Skills 目录 |
|-------|-----------|
| Claude Code | `~/.claude/skills/mwiki` |
| Codex | `~/.codex/skills/mwiki` |
| Gemini CLI | `~/.gemini/skills/mwiki` |
| Hermes | `~/.hermes/skills/mwiki` |
| OpenClaw | `~/.openclaw/skills/mwiki` |
| Aider | `~/.aider/skills/mwiki` |
| Copilot | `~/.copilot/skills/mwiki` |
| Zed | `~/.zed/skills/mwiki` |
| PearAI | `~/.pearai/skills/mwiki` |

**项目级 Agent**（skills 安装到 Vault 内）：

| Agent | Skills 目录 |
|-------|-----------|
| Cursor | `.cursor/skills/mwiki` |

### 7.3 Windows 注意事项

- 在 Git Bash 或 MSYS2 终端中运行 `setup.sh`
- 使用 Junction 链接（而非 symlink）
- 如 Junction 失败，自动回退到目录副本

---

## 9. 对话历史导入

### 8.1 Claude 对话历史

```bash
> /claude-history-ingest
```

自动扫描 `~/.claude/` 下的对话记录，提取知识点并归档。

### 8.2 脱敏规则

导入前自动过滤以下敏感信息：

| 类型 | 匹配模式 | 处理方式 |
|------|---------|---------|
| API Key | `sk-*`、`key-*` | 替换为 `[REDACTED_API_KEY]` |
| Token | Bearer token、auth token | 替换为 `[REDACTED_TOKEN]` |
| 密码 | password 字段 | 替换为 `[REDACTED_PASSWORD]` |
| 私有 URL | 内网地址、localhost | 替换为 `[REDACTED_URL]` |

### 8.3 建议频率

- 每月执行一次
- 或在完成重要项目后执行

---

## 10. 每日报告

### 9.1 生成日报

```bash
> /wiki-daily-report
```

### 9.2 报告内容

| 章节 | 内容 |
|------|------|
| 今日活动 | 编辑了哪些笔记、导入了哪些素材 |
| 今日所学 | 从素材中提取的关键知识 |
| 思考与建议 | Agent 基于知识库状态给出的建议 |

### 9.3 输出位置

`wiki/reports/daily/YYYY-MM-DD.md`

### 9.4 在 Obsidian 中查看

报告使用 Obsidian 原生 `[[wikilinks]]` 格式，可直接在 Obsidian 中点击跳转。

---

## 11. 数据安全与约束

### 10.1 核心规则

| 规则 | 说明 |
|------|------|
| `_raw/` 只读 | Agent 不得修改或删除用户原始素材 |
| `raw/` 只追加 | 已归档素材不可覆盖 |
| `.manifest.json` 自动备份 | 每次操作前备份为 `.manifest.json.bak` |
| 冲突不自动覆盖 | 概念合并冲突标记 `^[ambiguous]`，等用户裁决 |
| `wiki/` 为真相源 | `human/` 和 `ai/` 为派生视图，不一致时以 `wiki/` 为准 |

### 10.2 概念冲突处理

当不同来源对同一概念有矛盾描述时：

```
> 来源 A: Prompt Engineering 仅指提示词设计 ^[ambiguous]
> 来源 B: Prompt Engineering 包含上下文工程和系统设计 ^[ambiguous]
```

- Agent 保留所有来源描述
- 标记 `^[ambiguous]` 等待用户裁决
- 用户手动编辑页面，选择保留哪个描述或合并

---

## 12. 目录权限速查表

| 目录 | 用户权限 | Agent 权限 | 说明 |
|------|---------|-----------|------|
| `_raw/` | 可写（存放素材） | 只读 | 用户唯一的写入入口 |
| `raw/` | 只读 | 只追加 | 已归档素材的备份 |
| `wiki/` | 可编辑 | 读写 | 唯一真相源 |
| `wiki/concepts/` | 可编辑 | 读写 | 概念页 |
| `wiki/comparisons/` | 可编辑 | 读写 | 对比页 |
| `wiki/patterns/` | 可编辑 | 读写 | 模式页 |
| `wiki/topics/` | 可编辑 | 读写 | 主题页 |
| `wiki/reports/` | 只读 | 写入 | 报告 |
| `wiki/graphs/` | 只读 | 写入 | 图谱导出 |
| `human/` | 审阅 | 写入 | 人读手册 |
| `ai/` | 只读 | 读写 | Agent 路由 |
| `templates/` | 只读 | 写入 | 模板文件 |
| `.cache/` | 无感知 | 自动管理 | SHA256 缓存 |

---

## 13. Frontmatter 规范

每个 `wiki/` 页面的 frontmatter 必须包含以下字段：

```yaml
---
title: "页面标题"              # 必需：页面标题
created: 2026-05-27            # 必需：创建日期（YYYY-MM-DD）
updated: 2026-05-27            # 必需：更新日期（YYYY-MM-DD）
tags: [tag1, tag2, tag3]       # 必需：标签列表
summary: "一句话摘要"          # 必需：≤ 100 字的中文摘要
entity_type: concept           # 必需：7 种类型之一
status: active                 # 必需：active | deprecated | ambiguous
sources:                       # 必需：来源列表
  - path: _raw/01-example.md
    provenance: extracted      # extracted（直接提取）或 ^[inferred]（推断）
---
```

### provenance 标记

| 标记 | 含义 |
|------|------|
| `extracted` | 直接从原文提取，无歧义 |
| `^[inferred]` | Agent 推断得出，建议人工复核 |
| `^[ambiguous]` | 存在矛盾（如版本差异），需用户裁决 |

---

## 14. 故障排查

### 13.1 常见问题及解决方案

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| `/wiki-ingest` 报"目录为空" | `_raw/` 中没有 `.md` 文件 | 将素材复制到 `_raw/` |
| 编码异常跳过文件 | 文件非 UTF-8 编码 | 用编辑器转为 UTF-8 后重新放入 |
| 概念被错误分类 | `entity_type` 推断不准 | 手动编辑 frontmatter 修正 |
| 增量更新没检测到变更 | hash 缓存一致 | 检查 `.manifest.json` 中的 hash 记录 |
| Graph 导出为空 | `wiki/` 下没有知识页面 | 先执行 `/wiki-ingest` |
| setup.sh 链接失败 | 权限不足 | 以管理员身份运行或手动创建链接 |

### 13.2 日志查看

```bash
# 查看操作历史
cat wiki/log.md

# 查看 manifest 记录
cat .manifest.json
```

### 13.3 重置知识库

```bash
# 清空所有 Agent 生成的内容（保留原始素材）
rm -rf wiki/concepts/ wiki/comparisons/ wiki/patterns/ wiki/topics/
rm -rf wiki/graphs/ wiki/reports/daily/ wiki/reports/weekly/
rm -rf raw/ human/ ai/L2_detail/ .cache/

# 重置 manifest
echo '{"version":"1.0","created":"2026-05-27","updated":"2026-05-27","files":{},"stats":{"totalFiles":0,"totalConcepts":0,"lastIngest":null}}' > .manifest.json

# 重新导入
> /wiki-ingest
```

> **注意**：重置操作不可逆，建议先 `git commit` 保存当前状态。

---

## 15. 常见问题

**Q: 可以在 Obsidian 中直接编辑 `wiki/` 下的页面吗？**

A: 可以。`wiki/` 是用户可编辑的。Agent 在后续操作中会检测到用户的手动修改并保留。

**Q: `_raw/` 中的文件什么时候会被移走？**

A: 执行 `/wiki-ingest` 或 `/wiki-update` 后，已处理的文件会复制到 `raw/`（归档层）。原始文件仍在 `_raw/` 中，Agent 不会删除。

**Q: 支持哪些文件格式？**

A: 目前仅支持 `.md`（Markdown）文件。其他格式会被跳过并记录在日志中。

**Q: 多个 Agent 同时写入会冲突吗？**

A: 当前版本使用文件级锁和 `.manifest.json` 冲突检测。建议避免多个 Agent 同时执行写入操作（如同时 `/wiki-ingest`）。

**Q: 如何备份知识库？**

A: mwiki 基于纯文件系统，直接 `git commit` 或复制整个目录即可备份。

**Q: 知识库可以多人共享吗？**

A: mwiki 设计为个人知识库。如需多人共享，建议通过 Git 仓库协作，每个人独立使用 Agent 操作。

**Q: 删除一个概念页面后，相关 wikilink 会怎样？**

A: 指向已删除页面的 `[[wikilinks]]` 会变成断链。执行 `/wiki-lint` 可检测所有断链。

---

## 术语表

| 术语 | 含义 |
|------|------|
| Vault | Obsidian 的仓库目录，即 mwiki 项目根目录 |
| wikilinks | Obsidian 原生链接格式 `[[页面名]]` |
| frontmatter | Markdown 文件顶部的 YAML 元数据块 |
| entity_type | 知识页面的分类标签（7 种之一） |
| manifest | `.manifest.json`，记录已处理文件的 hash 和进度 |
| provenance | 来源可信度标记（extracted / inferred / ambiguous） |
| L0-L3 | Token 预算的四个级别，控制上下文加载量 |
| Skill | Agent 的指令集文件（Markdown 格式），定义命令行为 |
