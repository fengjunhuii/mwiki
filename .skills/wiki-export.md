---
name: wiki-export
description: 知识图谱导出——从 wiki/ 页面提取概念节点和 wikilink 边，生成 JSON / GraphML / Cypher / HTML 四种格式
---

# /wiki-export — 知识图谱导出

扫描 `wiki/` 下所有概念页面，提取概念节点和 `[[wikilinks]]` 引用关系，生成四种格式的知识图谱文件到 `wiki/graphs/`。

支持自然语言上色命令：`color my graph`、`color code by category`。

> **数据安全约束**：本操作为只读扫描（不修改 wiki/ 文件），仅写入 `wiki/graphs/` 输出目录和 `wiki/log.md` 日志。

---

## 前置准备

1. 读取 `ai/_index.json` 确认 `routes.export` 配置：
   - `output`：输出目录（默认 `wiki/graphs/`）
   - `formats`：需生成的格式列表
2. 扫描以下目录收集页面文件：
   - `wiki/concepts/*.md`（概念页，主要节点来源）
   - `wiki/topics/*.md`（主题页）
   - `wiki/comparisons/*.md`（对比页）
   - `wiki/patterns/*.md`（模式页）
   - `wiki/*.md`（根级页面，如 `purpose.md`、`index.md`）
3. 如果扫描结果为空（无任何 `.md` 文件），输出「知识库尚无结构化页面，请先执行 /wiki-ingest 导入素材」并终止

---

## Phase 1: 数据采集

### 1.1 节点采集

对每个扫描到的 `.md` 文件，提取以下信息作为**节点**：

1. **node_id**：文件名去除 `.md` 后缀（如 `prompt-engineering`）
2. **label**：frontmatter 中的 `title` 字段；若无则取第一个 `#` 标题；再无则用 node_id
3. **entity_type**：frontmatter 中的 `entity_type` 字段；若无则按目录推断：
   - `wiki/concepts/` → `concept`
   - `wiki/topics/` → `topic`
   - `wiki/comparisons/` → `comparison`
   - `wiki/patterns/` → `pattern`
   - 其他 → `page`
4. **tags**：frontmatter 中的 `tags` 数组
5. **status**：frontmatter 中的 `status` 字段（默认 `active`）
6. **summary**：frontmatter 中的 `summary` 字段

将所有节点收集到内存列表 `nodes[]`。

### 1.2 边采集

对每个节点对应的文件内容（跳过 frontmatter），提取所有 `[[wikilinks]]`：

#### wikilink 解析规则

与 `/wiki-lint` 保持一致，正则 `\[?\[([^\]#|]+)` 提取目标页名：

- `[[概念名]]` → 目标 `概念名`
- `[[概念名|显示文本]]` → 目标 `概念名`
- `[[概念名#章节标题]]` → 目标 `概念名`
- `[[概念名#章节标题|显示文本]]` → 目标 `概念名`

#### 边构建

对每条 wikilink：

1. 将目标页名转换为可能的 node_id（kebab-case，去除扩展名）
2. 检查目标是否存在于 `nodes[]` 中（按 node_id 匹配）
3. 如果存在，创建一条边：`{ source: 当前node_id, target: 目标node_id }`
4. 如果不存在（指向 wiki/ 外部或未创建页面），跳过（不计入图谱）
5. 去重：同一对 source→target 只保留一条边

将所有边收集到内存列表 `edges[]`。

### 1.3 输出统计

```
数据采集完成
  节点数：N 个
    - concept: C 个
    - topic: T 个
    - comparison: X 个
    - pattern: P 个
    - page: G 个
  边数：M 条
```

---

## Phase 2: 着色处理

### 2.1 默认着色

按 `entity_type` 分配颜色（用于 graph.json 和 graph.html）：

| entity_type | 颜色 | Hex |
|-------------|------|-----|
| concept | 蓝 | `#4A90D9` |
| tool | 绿 | `#27AE60` |
| person | 橙 | `#E67E22` |
| event | 红 | `#E74C3C` |
| comparison | 紫 | `#9B59B6` |
| pattern | 青 | `#1ABC9C` |
| overview | 灰 | `#95A6C8` |
| topic | 黄绿 | `#A3BE8C` |
| page | 浅灰 | `#BDC3C7` |

### 2.2 自然语言着色命令

如果用户在 `/wiki-export` 后附带以下命令，按指定规则重新着色：

- `color my graph` 或 `color by category`：按 entity_type 着色（默认行为）
- `color by tag`：按第一个 tag 分组着色，相同 tag 的节点同色
- `color by status`：active=绿、deprecated=红、draft=黄
- `color code by ...`：按指定 frontmatter 字段值分组着色

着色结果写入每个节点的 `color` 属性，供所有输出格式使用。

---

## Phase 3: 文件生成

按顺序生成四种格式文件到 `wiki/graphs/`。

### 3.1 graph.json

通用节点/边 JSON 格式：

```json
{
  "metadata": {
    "generated": "YYYY-MM-DDTHH:mm:ss",
    "nodeCount": N,
    "edgeCount": M,
    "source": "wiki/",
    "tool": "/wiki-export"
  },
  "nodes": [
    {
      "id": "prompt-engineering",
      "label": "Prompt Engineering",
      "entity_type": "concept",
      "tags": ["llm", "prompt"],
      "status": "active",
      "summary": "...",
      "color": "#4A90D9"
    }
  ],
  "edges": [
    {
      "source": "prompt-engineering",
      "target": "rag",
      "type": "wikilink"
    }
  ]
}
```

### 3.2 graph.graphml

Gephi 兼容的 GraphML XML 格式：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphstruct.org/graphml">
  <key id="label" for="node" attr.name="label" attr.type="string"/>
  <key id="entity_type" for="node" attr.name="entity_type" attr.type="string"/>
  <key id="tags" for="node" attr.name="tags" attr.type="string"/>
  <key id="color" for="node" attr.name="color" attr.type="string"/>
  <graph id="mwiki" edgedefault="directed">
    <node id="prompt-engineering">
      <data key="label">Prompt Engineering</data>
      <data key="entity_type">concept</data>
      <data key="tags">llm,prompt</data>
      <data key="color">#4A90D9</data>
    </node>
    <edge source="prompt-engineering" target="rag">
      <data key="type">wikilink</data>
    </edge>
  </graph>
</graphml>
```

注意：
- `<key id="type" for="edge" attr.name="type" attr.type="string"/>` 也需声明
- XML 特殊字符（`&`、`<`、`>`、`"`、`'`）必须转义
- 节点 `id` 和边 `source`/`target` 必须与 graph.json 中的 `id` 一致

### 3.3 graph.cypher

Neo4j Cypher CREATE 语句：

```cypher
// mwiki 知识图谱 — YYYY-MM-DD 生成
// 节点数: N, 边数: M

// 清除已有数据（可选，取消注释以启用）
// MATCH (n) DETACH DELETE n;

// 创建节点
CREATE (n_prompt_engineering:Concept {id: 'prompt-engineering', label: 'Prompt Engineering', tags: ['llm','prompt'], status: 'active', summary: '...'})
CREATE (n_rag:Concept {id: 'rag', label: 'RAG', tags: ['rag','retrieval'], status: 'active', summary: '...'})

// 创建关系
CREATE (n_prompt_engineering)-[:REFERENCES]->(n_rag)

;
```

注意：
- 节点变量名 = `n_` + node_id 中的 `-` 替换为 `_`
- Neo4j label 按 entity_type 大驼峰映射：`concept`→`Concept`、`tool`→`Tool`、`comparison`→`Comparison`、`pattern`→`Pattern`、`topic`→`Topic`、`page`→`Page`
- 字符串值中的单引号需转义为 `\'`
- 每条 CREATE 语句单独一行，全部语句以 `;` 结尾

### 3.4 graph.html

可在浏览器双击打开的交互式可视化 HTML 文件。使用内联 CSS + JavaScript（无外部依赖），基于 Canvas 绘制力导向图。

#### HTML 结构要求

1. **自包含**：所有 CSS 和 JavaScript 内联，不依赖 CDN 或外部文件
2. **交互功能**：
   - 节点可拖拽
   - 鼠标悬停显示 tooltip（label、entity_type、tags）
   - 鼠标滚轮缩放
   - 点击节点高亮其直接关联节点和边
3. **视觉设计**：
   - 深色背景（`#1a1a2e`）
   - 节点按 entity_type 着色（颜色表见 Phase 2.1）
   - 边为半透明浅色线条
   - 左上角显示图例（entity_type → 颜色）
   - 右上角显示统计信息（节点数、边数）
4. **力导向布局**：实现简单的力导向算法（斥力+引力+阻尼），或使用 Canvas 2D 绘制静态布局
5. **数据嵌入**：将 Phase 1 采集的 nodes 和 edges 数据以 JSON 格式嵌入 `<script>` 标签内

#### 实现模板

使用以下结构生成 HTML：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>mwiki 知识图谱</title>
<style>
/* 内联样式：深色背景、Canvas 全屏、图例/统计面板 */
</style>
</head>
<body>
<canvas id="graph"></canvas>
<div id="legend"><!-- entity_type 图例 --></div>
<div id="stats"><!-- 节点数/边数 --></div>
<div id="tooltip" style="display:none;"></div>
<script>
// 嵌入图数据
const GRAPH_DATA = { nodes: [...], edges: [...] };
// 力导向布局算法
// Canvas 渲染
// 交互处理（拖拽、缩放、悬停、点击）
</script>
</body>
</html>
```

Agent 应根据实际节点和边数据填充 GRAPH_DATA，并实现完整的力导向布局和交互逻辑。

---

## Phase 4: 结果输出

### 4.1 终端输出

```
/wiki-export 完成
━━━━━━━━━━━━━━━━━━━━━
节点：N 个（concept C / topic T / comparison X / pattern P）
边：M 条
输出文件：
  ✓ wiki/graphs/graph.json
  ✓ wiki/graphs/graph.graphml
  ✓ wiki/graphs/graph.cypher
  ✓ wiki/graphs/graph.html
━━━━━━━━━━━━━━━━━━━━━
在浏览器打开 wiki/graphs/graph.html 查看交互式图谱
```

### 4.2 空图谱处理

如果 Phase 1 采集结果为 0 节点：

```
/wiki-export 完成
━━━━━━━━━━━━━━━━━━━━━
知识库尚无结构化页面，图谱为空。
请先执行 /wiki-ingest 导入素材后重试。
━━━━━━━━━━━━━━━━━━━━━
```

不生成任何输出文件。

### 4.3 日志记录

在 `wiki/log.md` 中追加记录：

```markdown
## YYYY-MM-DD HH:mm

- **操作**：`/wiki-export` 知识图谱导出
- **节点**：N 个（concept C / topic T / comparison X / pattern P）
- **边**：M 条
- **输出**：graph.json / graph.graphml / graph.cypher / graph.html
- **着色**：按 entity_type（默认）/ 按用户指定字段
```

---

## 约束与安全

- `wiki/` 文件只读扫描，不修改任何 wiki 内容
- 仅写入 `wiki/graphs/` 输出目录和 `wiki/log.md` 日志
- `_raw/` 和 `raw/` 不参与图谱构建
- 所有文件 UTF-8 无 BOM 编码
- graph.html 必须自包含，无外部依赖
- graph.graphml 必须是合法 XML
- graph.cypher 必须是可执行的 Cypher 语句
- 已存在的输出文件直接覆盖（每次导出为最新快照）
