---
l0_context: "ai/L0_profile.md"
l1_context:
  - "wiki/purpose.md"
  - "ai/L1_architecture.md"
l2_context: "ai/L2_detail/"
l3_context: "wiki/concepts/"
token_budget:
  L0: "~200 token，每次会话必读"
  L1: "~1-2K token，会话开始时读"
  L2: "~2-5K token，搜索定位时读"
  L3: "5-20K token，深度读写时读"
---

# mwiki 知识库配置

## 编码规范

- 所有 markdown 文件使用 UTF-8 编码（无 BOM）
- Frontmatter 必须包含：title / created / updated / tags / summary / entity_type / status / sources
- 文件名使用 kebab-case（如 `prompt-template.md`）
- 注释和内容使用中文

## 目录规范

| 目录 | 用途 | 用户权限 | Agent 权限 |
|------|------|---------|-----------|
| `_raw/` | 用户存放原始素材（暂存层） | 可写 | 只读，不修改不删除 |
| `raw/` | 已归档素材（收录层） | 只读 | 只追加，不覆盖 |
| `wiki/` | Agent 重写后的结构化页面 | 可编辑 | 读写 |
| `wiki/concepts/` | 概念页（跨源合并） | 可编辑 | 读写 |
| `wiki/topics/` | 主题页（按领域聚合） | 可编辑 | 读写 |
| `wiki/comparisons/` | 对比页 | 可编辑 | 读写 |
| `wiki/patterns/` | 模式页 | 可编辑 | 读写 |
| `wiki/reports/daily/` | 日报 | 只读 | 写入 |
| `wiki/reports/weekly/` | 周报 | 只读 | 写入 |
| `wiki/graphs/` | 图谱导出 | 只读 | 写入 |
| `human/` | 人读综合手册与业务问卷 | 审阅 | 写入 |
| `ai/` | AI 路由层（_index.json + L0-L3） | 只读 | 读写 |
| `templates/` | 模板文件 | 只读 | 写入 |
| `.cache/` | SHA256 增量缓存 | 无感知 | 自动管理 |

## 操作规范

- 用户只往 `_raw/` 存放原始素材
- `wiki/` 页面由 Agent 生成和维护
- 已收录素材从 `_raw/` 移至 `raw/`（Ingest 后置动作）
- 概念合并冲突标记 `^[ambiguous]`，不自动覆盖
- `.manifest.json` 每次操作前自动备份为 `.manifest.json.bak`
- 以 `wiki/` 为唯一真相源，`human/` 和 `ai/` 为派生视图

## 可用 Skill 指令

| 指令 | 用途 |
|------|------|
| `/wiki-setup` | 初始化六层目录结构 |
| `/wiki-ingest` | 四阶段全量导入（Ingest → Extract → Resolve → Schema） |
| `/wiki-update` | 增量更新（基于 .manifest.json SHA256 对比） |
| `/wiki-query` | 语义查询（完整 + quick answer 模式） |
| `/wiki-lint` | 质量检查（断链 / 缺失页 / 矛盾 / 过时） |
| `/wiki-export` | 知识图谱导出（JSON / GraphML / Cypher / HTML） |
| `/cross-linker` | 自动补充 [[wikilinks]] |
| `/claude-history-ingest` | 导入 Claude 对话历史 |
| `/codex-history-ingest` | 导入 Codex 对话历史 |

## Token 预算

| 级别 | Token 量 | 触发时机 | 内容 |
|------|---------|---------|------|
| L0 | ~200 | 每次会话启动 | `CLAUDE.md` frontmatter |
| L1 | ~1-2K | 会话开始 | `wiki/purpose.md` + `wiki/index.md` |
| L2 | ~2-5K | 搜索/定位阶段 | `ai/L2_detail/` 按需加载 |
| L3 | 5-20K | 深度读写操作 | 完整文章或原始资料 |

## 数据安全

- `_raw/` 原始素材：Agent 不得修改或删除
- `raw/` 收录层：只可追加，不可覆盖
- 对话历史导入前必须脱敏（API Key / Token 等敏感字段）
- 概念合并冲突标记 `^[ambiguous]`，等用户裁决
