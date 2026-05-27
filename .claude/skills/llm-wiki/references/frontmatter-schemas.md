# Frontmatter Schemas

Every wiki page must start with YAML frontmatter. This document defines the schema for each page type.

---

## Common Fields (All Page Types)

```yaml
---
title: string          # Required. Page title (matches H1 heading)
created: YYYY-MM-DD    # Required. Initial creation date
updated: YYYY-MM-DD    # Required. Last modification date (must update on every edit)
type: string           # Required. One of: entity, concept, comparison, changelog, overview
tags: [string]         # Required. At least 2 tags from SCHEMA.md taxonomy
sources: [string]      # Required. Source file paths relative to project root
---
```

---

## Entity Page

```yaml
---
title: ClassName
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity
tags: [component, module, TAG]
sources: [src/module/class.py]
---
```

**Additional conventions**:
- `title` matches the class/struct/module name exactly
- `sources` lists the primary file(s) where this entity is defined
- Must include sections: 位置, 概述, 类/结构定义, 核心方法, 相关页面, 源码引用

---

## Concept Page

```yaml
---
title: Concept Name
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: concept
tags: [architecture, TAG, TAG]
sources: [src/module1/file1.py, src/module2/file2.py]
---
```

**Additional conventions**:
- `title` uses descriptive name with hyphens in filename
- `sources` lists all files that contribute to this concept
- Must include sections: 概述, 核心机制, 设计决策, 与其他系统的交互, 相关页面, 源码引用

---

## Comparison Page

```yaml
---
title: Approach A vs Approach B
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: concept
tags: [comparison, TAG]
sources: [src/file1.py, src/file2.py]
---
```

**Additional conventions**:
- Stored in `concepts/` directory
- Must include comparison table
- Must include conclusion/recommendation

---

## Changelog Page

```yaml
---
title: vX.Y.Z Update
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: changelog
tags: [changelog, release]
sources: [git log analysis]
version: vX.Y.Z
commit_count: number
base_version: vX.Y.W
---
```

**Additional conventions**:
- Filename: `YYYY-MM-DD-update.md` (date of analysis)
- Must include: 版本信息, 新增功能, 改进, 影响的 Wiki 页面

---

## Overview Page

```yaml
---
title: Project Architecture Overview
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: overview
tags: [architecture, overview]
sources: [src/]
---
```

**Additional conventions**:
- Typically the `index.md` file
- Must include: complete table of contents with descriptions
- Must track statistics (page counts, coverage)

---

## Pattern Page

```yaml
---
title: Pattern Name
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: pattern
tags: [pattern, TAG, TAG]
sources: [src/module1/file1.py, src/module2/file2.py]
---
```

**Additional conventions**:
- Document reusable design patterns found in the codebase
- Must include: 问题, 方案, 权衡, 示例, 变体, 相关页面, 源码引用

---

## Field Validation Rules

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `title` | string | Yes | Non-empty, matches H1 |
| `created` | date | Yes | YYYY-MM-DD format |
| `updated` | date | Yes | Must be >= created |
| `type` | enum | Yes | entity/concept/comparison/changelog/overview/pattern |
| `tags` | list | Yes | Min 2 items, from SCHEMA.md taxonomy |
| `sources` | list | Yes | Min 1 item, valid file paths |
| `version` | string | Changelog only | SemVer format |
| `commit_count` | number | Changelog only | Positive integer |
| `base_version` | string | Changelog only | SemVer format |

---

## Filename Convention

- Lowercase + hyphens, no spaces
- Entity: `classname.md` (e.g., `aiagent-class.md`)
- Concept: `descriptive-name.md` (e.g., `skills-system-architecture.md`)
- Changelog: `YYYY-MM-DD-update.md` (e.g., `2026-04-09-update.md`)
