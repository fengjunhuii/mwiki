# 文档导出指南

## 支持的导出格式

### 1. Markdown（默认输出）
PRD 的原生格式，所有文档首先以 Markdown 输出。

### 2. Word (.docx)
将 Markdown PRD 转换为格式化的 Word 文档，支持：
- 标题层级（H1-H4，非斜体，居中 H1）
- 表格（带样式，表头着色）
- 列表（有序/无序，紧凑间距）
- Mermaid 流程图 → 并行预加载 → 转为图片嵌入（智能缩放）
- 引用块（缩进 + 灰色斜体）
- 代码块和行内代码
- 加粗 / 斜体文本

### 3. HTML 原型
参见 [prototype-guide.md](prototype-guide.md)

---

## Word 导出实现方案

### 方案 A：使用 python-docx（推荐）

```bash
pip install python-docx httpx Pillow
```

**依赖说明：**
- `python-docx` — Word 文档构建
- `httpx` — 异步 HTTP 客户端，用于 Mermaid 图片获取
- `Pillow` — 图片尺寸智能计算（可选，缺失时使用默认宽度）

核心流程（两遍扫描）：

```
第一遍：扫描所有 Mermaid 代码块 → 并行预加载图片（asyncio.gather）
第二遍：逐行解析 Markdown → 构建 Word 文档 → 插入已缓存的图片
```

---

### Mermaid 图片转换（多服务 + 重试 + 并行）

**服务优先级：**

| 优先级 | 服务 | URL | 编码方式 |
|--------|------|-----|---------|
| 1 | Mermaid.ink | `https://mermaid.ink/img/{encoded}` | URL-safe Base64 |
| 2 | Kroki | `https://kroki.io/mermaid/png/{encoded}` | 标准 Base64 |

**重试策略：**
- 最大重试 5 次
- 503 错误：指数退避（3s × 重试次数）
- 超时：60 秒
- 其他错误：等待 2 秒后重试

```python
import base64
import httpx

async def mermaid_to_image(mermaid_code: str, service_index: int = 0) -> bytes | None:
    """将 Mermaid 代码转换为 PNG 图片（带多服务回退）"""
    services = [
        {"name": "Mermaid.ink", "url": "https://mermaid.ink/img/", "method": "urlsafe"},
        {"name": "Kroki", "url": "https://kroki.io/mermaid/png/", "method": "standard"},
    ]

    code_bytes = mermaid_code.strip().encode('utf-8')

    for service in services[service_index:]:
        # 编码
        if service["method"] == "urlsafe":
            encoded = base64.urlsafe_b64encode(code_bytes).decode('utf-8').rstrip('=')
        else:
            encoded = base64.b64encode(code_bytes).decode('utf-8')

        url = f"{service['url']}{encoded}"

        # 重试
        for attempt in range(5):
            try:
                async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
                    response = await client.get(url)
                    if response.status_code == 200:
                        content_type = response.headers.get('content-type', '')
                        if 'image' in content_type:
                            return response.content
                    elif response.status_code == 503:
                        await asyncio.sleep((attempt + 1) * 3)
                    else:
                        await asyncio.sleep(2)
            except Exception:
                await asyncio.sleep(2)

    return None
```

**并行预加载（关键优化）：**

```python
import asyncio

async def preload_mermaid_images(mermaid_blocks: list[str]) -> dict[int, bytes]:
    """并行预加载所有 Mermaid 图片"""
    tasks = [
        mermaid_to_image(code, idx)
        for idx, code in enumerate(mermaid_blocks)
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    cache = {}
    for idx, result in enumerate(results):
        if result and not isinstance(result, Exception):
            cache[idx] = result
    return cache
```

> **性能提示：** 10 个 Mermaid 图表串行加载需要 ~60 秒，并行预加载仅需 ~8 秒。

---

### 智能图片尺寸计算

使用 Pillow 根据图片实际宽高比计算嵌入尺寸，避免变形：

```python
from PIL import Image
from io import BytesIO
from docx.shared import Inches

MAX_WIDTH = Inches(5.5)
MAX_HEIGHT = Inches(7.0)

def calculate_image_size(image_data: bytes) -> tuple:
    """根据宽高比计算图片嵌入尺寸"""
    img = Image.open(BytesIO(image_data))
    width, height = img.size
    aspect = width / height

    new_width = MAX_WIDTH
    new_height = Inches(MAX_WIDTH.inches / aspect)

    # 限制最大高度
    if new_height > MAX_HEIGHT:
        new_height = MAX_HEIGHT
        new_width = Inches(MAX_HEIGHT.inches * aspect)

    # 小图不放大
    if new_width < Inches(4.0) or new_height < Inches(3.0):
        new_width = Inches(new_width.inches * 0.9)
        new_height = Inches(new_height.inches * 0.9)

    return new_width, new_height
```

---

### 文档样式配置（紧凑排版 + 中文字体）

```python
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

doc = Document()

# 紧凑页边距
for section in doc.sections:
    section.top_margin = Inches(0.6)
    section.bottom_margin = Inches(0.6)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

# 正文字体
normal = doc.styles['Normal']
normal.font.name = 'Microsoft YaHei'
normal.font.size = Pt(10.5)
normal.paragraph_format.line_spacing = 1.15
normal.paragraph_format.space_after = Pt(6)

# 设置东亚文字字体（中文显示关键）
def set_east_asia_font(run, font_name: str):
    r = run._element
    rPr = r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), font_name)

# 标题样式（非斜体，这是默认问题）
heading_sizes = {1: Pt(18), 2: Pt(15), 3: Pt(13), 4: Pt(11.5)}
for i in range(1, 5):
    heading = doc.styles[f'Heading {i}']
    heading.font.name = 'Microsoft YaHei'
    heading.font.size = heading_sizes[i]
    heading.font.color.rgb = RGBColor(102, 126, 234)
    heading.font.bold = True
    heading.font.italic = False  # 关键：Word 默认标题是斜体
    heading.paragraph_format.space_before = Pt(8)
    heading.paragraph_format.space_after = Pt(6)
```

---

### 表格样式（表头着色）

```python
from docx.oxml import parse_xml

def add_styled_table(doc, headers: list, rows: list):
    table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    table.style = 'Light Grid Accent 1'

    # 表头
    for i, text in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = text
        for run in cell.paragraphs[0].runs:
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
        # 紫色表头背景
        shading = parse_xml(
            r'<w:shd {} w:fill="667eea"/>'.format(
                'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
            )
        )
        cell._element.get_or_add_tcPr().append(shading)

    # 数据行
    for row_idx, row_data in enumerate(rows, start=1):
        for col_idx, text in enumerate(row_data):
            if col_idx < len(headers):
                table.rows[row_idx].cells[col_idx].text = text
```

---

### 富文本格式（加粗 / 斜体 / 行内代码）

```python
import re

def add_rich_paragraph(doc, text: str):
    """支持 **加粗**、*斜体*、`代码` 的段落"""
    p = doc.add_paragraph()

    # 分割行内代码
    parts = re.split(r'(`[^`]+`)', text)

    for part in parts:
        if part.startswith('`') and part.endswith('`'):
            run = p.add_run(part[1:-1])
            run.font.name = 'Courier New'
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(232, 62, 140)
        else:
            # 处理加粗和斜体
            for match in re.finditer(r'(\*\*([^*]+)\*\*|\*([^*]+)\*)', part):
                # 添加 match 之前的普通文本
                # 添加加粗或斜体文本
                pass
```

---

### 失败回退（Mermaid 占位符）

当图片获取失败时，插入占位文本：

```python
def add_mermaid_placeholder(doc, reason: str):
    p = doc.add_paragraph()
    run1 = p.add_run("[流程图] ")
    run1.bold = True
    run1.font.color.rgb = RGBColor(102, 126, 234)
    run2 = p.add_run(f"({reason}，请查看 Markdown 文件)")
    p.paragraph_format.left_indent = Inches(0.3)
```

---

### 方案 B：使用 Pandoc（简单场景）

```bash
# macOS: brew install pandoc
# Windows: choco install pandoc

# Markdown → Word
pandoc PRD.md -o PRD.docx

# 使用自定义模板
pandoc PRD.md -o PRD.docx --reference-doc=template.docx
```

优点：简单快速，一行命令
缺点：不支持 Mermaid 转图片，中文样式可能需要调整

---

## 完整导出流程

```
Markdown 文本
  │
  ├── 第一遍扫描：收集所有 ```mermaid 代码块
  │
  ├── 并行预加载 Mermaid 图片（asyncio.gather）
  │     ├── mermaid.ink（优先）
  │     └── kroki.io（回退）
  │
  └── 第二遍扫描：逐行构建 Word
        ├── # 标题 → Heading 1-4（非斜体，中文宋体）
        ├── | 表格 | → Styled Table（紫色表头）
        ├── - 列表 → List Bullet（紧凑间距）
        ├── > 引用 → 缩进 + 灰色斜体
        ├── ```代码块``` → Courier New
        ├── **加粗** / *斜体* / `代码` → 富文本
        ├── ```mermaid``` → 缓存图片（智能缩放）或占位符
        └── --- → 分隔线
```

---

## 输出文件命名规范

```
output/
├── prd.md                    # Markdown 源文件
├── PRD_20260411_143022.docx  # Word 导出（带时间戳）
├── feature_list.md           # 功能清单
├── design-system/            # 设计系统
│   └── project-name/
│       ├── MASTER.md
│       └── pages/
└── prototype/
    └── index.html            # HTML 原型
```

---

## 注意事项

1. **并行预加载**是性能关键 — 10 张图从 ~60s 降到 ~8s
2. **东亚字体**必须通过 `w:rFonts` 的 `w:eastAsia` 属性设置，否则中文显示为宋体
3. **标题非斜体**需显式设置 `italic = False`，Word 默认 Heading 样式是斜体
4. **Mermaid 图片转换**需要网络访问 mermaid.ink 或 kroki.io
5. **离线环境**可使用 Pandoc 方案，但无法转换 Mermaid 图为图片
6. **大文档**注意 Word 文件大小限制（复杂 Mermaid 图可能较大）
