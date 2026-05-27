# Compilation Guide

Writing standards for wiki pages generated during codebase analysis.

---

## Writing Principles

1. **Source-first**: Every statement must trace to specific source code
2. **Why over what**: Explain design intent, not just describe code
3. **Chinese content, English code**: Prose in Chinese Simplified, identifiers in English
4. **No hype**: Objective, factual descriptions only
5. **Right-sized**: 60-200 lines typical; entity pages can be shorter (precision-focused), concept pages can be longer (explanation-focused). Split at >250 lines.

### Directory Adaptation

If the wiki root contains `.wiki-schema.md` (global llm-wiki format), write pages into:
- `wiki/entities/` for entity pages
- `wiki/topics/` for concept/topic pages

Otherwise use the project-level defaults:
- `entities/` for entity pages
- `concepts/` for concept/topic pages

---

## Page Structure

### Frontmatter (Always First)

```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | changelog | overview
tags: [tag1, tag2, tag3]
sources: [src/path/file1.py, src/path/file2.py]
---
```

### Opening Paragraph (导语段)

2-4 sentences covering:
1. What is this?
2. Why does it matter?
3. What does this page cover?

No first person. No marketing language. State the page's thesis.

---

## Content Standards

### Code Snippets

- Use **real code** from the source, not invented examples
- Include file path reference: `source/path/file.py:LINE`
- Trim to essential lines (don't copy-paste entire functions unless short)
- Always specify language in code fence

```python
# Good: Real code with context
def process_data(data: List[Dict]) -> Result:
    """Process incoming data stream"""
    validated = self.validator.check(data)
    return self.transformer.apply(validated)
```

### Tables

Use tables for:
- Method/function signatures
- Configuration options
- Design decisions
- Comparisons

```markdown
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `max_retries` | `int` | `3` | 最大重试次数 |
```

### Diagrams

Use text-based diagrams for:
- Data flows
- Component interactions
- State machines

```
Request → [Auth Middleware] → [Router] → [Controller]
                                  ↓
                            [Service Layer]
                                  ↓
                            [Data Access]
```

---

## Wiki-link Guidelines

### When to Link

- First mention of a concept/entity that has (or will have) its own page
- Cross-referencing related systems
- Referencing source analysis context

### Link Format

- `[[page-name]]` — standard link (matches filename without .md)
- `[[page-name|display text]]` — link with display text

### Link Density

- Minimum: 2 outbound links per page
- Maximum: ~15 outbound links per page
- Aim for 5-10 links per page as optimal

### Link Audit

After generating all pages, verify:
1. Every `[[target]]` has a corresponding `.md` file
2. Bidirectional links exist (if A links to B, B should link to A where relevant)
3. No orphan pages (pages with no inbound links)

---

## Source Citation Format

### Inline Citation
```
在 `src/core/engine.py:45-60` 中实现了核心调度逻辑。
```

### Section-End Citation
```
## 源码引用

- `src/core/engine.py:45-120` — 核心调度器实现
- `src/utils/parser.py:10-30` — 配置解析工具
```

---

## Quality Checklist

Before marking a page as complete:

- [ ] Frontmatter complete and valid
- [ ] Opening paragraph covers what/why/scope
- [ ] All code snippets are from real source files
- [ ] Min 2 outbound wiki-links
- [ ] Source file references include line ranges
- [ ] No TODO or placeholder content
- [ ] Page length appropriate for type (entity: 60-150, concept: 100-250)
- [ ] Tables used where appropriate
- [ ] No hype or marketing language
- [ ] Chinese prose, English identifiers
