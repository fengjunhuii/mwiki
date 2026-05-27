# Entity Types

Wiki pages for codebase analysis use 6 entity types. Each type has different required sections and writing focus.

---

## 1. `entity` — Core Classes/Modules

**When to create**: A class, struct, or module that is central to the project's architecture. Appears in 2+ other modules' import chains or is a primary entry point.

**Required sections**:
- **位置** — Source file path
- **概述** — 2-4 sentences: what it is, what problem it solves
- **类/结构定义** — Constructor/class signature with parameters
- **核心方法/函数** — Key public methods with signatures
- **关键属性** — Table of important attributes
- **设计要点** — Design decisions and rationale
- **相关页面** — Wiki-links to related concepts (min 2)
- **源码引用** — File paths with line ranges

**Writing focus**: Precision over explanation. Every claim backed by source code.

---

## 2. `concept` — Architecture Patterns/Design Decisions

**When to create**: An architectural pattern, system flow, or design decision that spans multiple files or modules. More than just "how one class works" — it's about how parts work together.

**Required sections**:
- **概述** — Definition and motivation
- **核心机制** — How it works, step by step
- **设计决策** — Table: decision | choice | reason | alternative
- **与其他系统的交互** — Wiki-links to related systems
- **已知限制** — Current limitations
- **相关页面** — Wiki-links (min 2)
- **源码引用** — File paths with line ranges

**Writing focus**: Why over what. Explain design intent and trade-offs.

---

## 3. `comparison` — Comparative Analysis

**When to create**: When the codebase implements 2+ approaches for the same problem, or when different modules can be contrasted meaningfully.

**Required sections**:
- **对比概述** — What's being compared and why
- **对比表格** — Structured comparison across dimensions
- **详细分析** — In-depth discussion per dimension
- **结论与建议** — When to use which approach
- **相关页面** — Wiki-links to compared items
- **源码引用** — File paths

**Writing focus**: Objectivity. Present strengths and weaknesses of each approach.

---

## 4. `changelog` — Version Analysis

**When to create**: After analyzing a new version or significant commit range from git history.

**Required sections**:
- **版本信息** — Version, commit count, date range
- **重大变更** — Architecture-level changes
- **新增功能** — Table: module | feature | source path
- **改进与优化** — Bullet list with source references
- **架构变更** — Detailed description of structural changes
- **影响的 Wiki 页面** — Which existing pages need updates

**Writing focus**: Impact over enumeration. Focus on what changed architecturally, not line-by-line diffs.

---

## 5. `overview` — Top-Level Summary

**When to create**: Only for the main `index.md`. Provides the navigational entry point for the entire wiki.

**Required sections**:
- **目录结构** — Organized by category with one-line descriptions
- **统计信息** — Page counts, coverage metrics
- **使用方式** — How to browse/use the wiki

**Writing focus**: Navigation and orientation. Help readers find what they need.

---

## 6. `pattern` — Design Patterns

**When to create**: When a reusable design pattern is identified in the codebase that isn't specific to one module.

**Required sections**:
- **问题** — What problem this pattern solves
- **方案** — The pattern's core approach
- **权衡** — Advantages and costs
- **示例** — Concrete implementation in this codebase
- **变体** — Variations found in the codebase
- **相关页面** — Wiki-links
- **源码引用** — File paths

**Writing focus**: Reusability. Help readers recognize and apply this pattern.

---

## Classification Priority

When deciding the type for a new page:

1. Is it about a specific class/module? → `entity`
2. Does it compare approaches? → `comparison`
3. Is it a version change summary? → `changelog`
4. Is it the main table of contents? → `overview`
5. Is it a reusable design pattern? → `pattern`
6. Is it an architectural concept spanning modules? → `concept`

## Page Creation Thresholds

- **Create**: Entity/concept appears in 2+ source files OR is a module's core content
- **Update**: Source code changes affect already-documented content
- **Skip**: Incidental mentions, trivial details, out-of-scope content
- **Split**: Page exceeds ~250 lines → split into sub-topics with cross-links
- **Merge**: Page under ~40 lines → merge into parent or related page
- **Archive**: Content fully superseded → move to `_archive/`, remove from index

## Directory Adaptation

If the wiki root contains `.wiki-schema.md` (global llm-wiki format):
- Entity pages → `wiki/entities/`
- Concept/topic pages → `wiki/topics/`

Otherwise use project-level defaults:
- Entity pages → `entities/`
- Concept/topic pages → `concepts/`

## Inline Comparison Detection

When scan finds 2+ implementations of the same abstraction (e.g., MRP Pipeline vs Wiki Agent, multiple AI providers), add a comparison section within the relevant concept page. Only create a separate comparison page if the comparison warrants 100+ lines.
