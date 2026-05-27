---
name: llm-wiki
description: "Analyze any codebase and generate structured architecture Wiki documentation. Supports multi-agent parallel analysis, auto-detection of project type, and Obsidian-compatible output with bidirectional links."
version: 1.1.0
---

# LLM Wiki — Codebase Architecture Wiki Generator

Analyze any codebase and generate structured architecture Wiki documentation following the Hermes-Wiki pattern. Multi-agent parallel analysis with Obsidian-compatible output.

## When to Use

- User wants to analyze a codebase and generate architecture documentation
- User says "generate wiki", "analyze project", "create architecture docs", or "build knowledge base" for a codebase
- User wants to update/extend an existing codebase wiki
- User wants to initialize a new wiki vault for a software project
- User gives a project path and says "scan" or "generate wiki for this"

## When NOT to Use

- General knowledge base (not code-specific) — use the global `llm-wiki` skill instead
- One-off code questions without persistent documentation
- Non-code documentation (books, papers, articles)

## Coexistence with Global llm-wiki

Two different `llm-wiki` skills may exist:

| Skill | Scope | Purpose | Directory Pattern |
|-------|-------|---------|-------------------|
| **Project-level** (this skill) | `PROJECT_DIR/.claude/skills/llm-wiki/` | Codebase analysis → Wiki pages | `entities/`, `concepts/` |
| **Global** | `~/.claude/skills/llm-wiki/` | Material ingestion → Knowledge base | `wiki/entities/`, `wiki/topics/` |

**Adaptation rule**: If the target wiki already has a `.wiki-schema.md` (global format), write pages into `wiki/entities/` and `wiki/topics/` instead of `entities/` and `concepts/`. Detect the schema file at the wiki root and adjust paths accordingly.

## Core Principles

1. **Source-first analysis** — every wiki claim must trace to specific source files and line ranges
2. **Multi-agent parallel exploration** — scan codebase with parallel agents for speed
3. **Structured output** — every page follows frontmatter + section templates
4. **Bidirectional links** — wiki-links create a navigable knowledge graph (min 2 outbound per page)
5. **Incremental updates** — new analysis augments existing wiki, never overwrites
6. **Auto-detection** — identify language, framework, build system, architecture pattern automatically

## Pipeline

| Stage | Input | Output | Agents |
|-------|-------|--------|--------|
| **Init** | Project path | Wiki vault structure | Single |
| **Scan** | Project path | Project profile + module map | Parallel (3-5) |
| **Analyze** | Module map | Entity + Concept candidates | Parallel (per module) |
| **Generate** | Analysis results | Wiki pages (entities/, concepts/) | Parallel (per page) |
| **Link** | All pages | Cross-references + index.md | Sequential |
| **Lint** | Full wiki | Health report | Single |

## Commands

| Command | Description |
|---------|-------------|
| `init <project-path> [--name <wiki-name>]` | Initialize wiki vault for a project |
| `full <project-path>` | **One-shot**: init + scan + analyze + generate (recommended for first use) |
| `scan` | Auto-detect project type, scan structure, build module map |
| `analyze [module]` | Deep-dive into specific or all modules |
| `generate` | Generate wiki pages from analysis |
| `update <source-path>` | Incremental update from changed source files |
| `lint` | Health check: broken links, missing pages, format violations |
| `query <question>` | Answer from wiki, cite sources |

### The `full` Command (Recommended)

Most users should start with `full`, which executes the entire pipeline:

```
init → scan (parallel agents) → analyze (parallel per module) → generate (parallel per page) → link → update index/log
```

**Workflow**:
1. Validate project path exists
2. Detect wiki root (check `.wiki-schema.md` or create new vault)
3. Fill `purpose.md` with detected project scope and key questions
4. Launch 3-5 parallel scan agents (structure, modules, dependencies, config, API)
5. Merge scan results into module map
6. For each module, launch analyze agent (or combine into fewer agents for small projects)
7. Generate pages: entities for core classes/modules, topics for architecture concepts
8. Add bidirectional wiki-links between all pages
9. Update `index.md`, `overview.md`, `log.md`

**Agent count guidance**:
- Small project (< 20 source files): 2-3 agents
- Medium project (20-100 files): 3-5 agents  
- Large project (100+ files): 5 agents for scan, then per-module for analyze

## Entity Types

6 types specific to codebase analysis:

| Type | Directory | When to Create |
|------|-----------|----------------|
| `entity` | `entities/` | Core classes, modules, key data structures |
| `concept` | `concepts/` or `topics/` | Architectural patterns, design decisions, system flows |
| `comparison` | `concepts/` or `comparisons/` | When 2+ approaches/modules are contrasted |
| `changelog` | `changelog/` | Version-by-version analysis (from git/migration history) |
| `overview` | root | Top-level architecture summary (index.md) |
| `pattern` | `concepts/` or `topics/` | Reusable design patterns found in codebase |

**Directory adaptation**: If the wiki root contains `.wiki-schema.md` (global llm-wiki format), use `wiki/entities/` for entities and `wiki/topics/` for concepts. Otherwise use the project-level `entities/` and `concepts/` directories.

### Auto-Detection of Comparisons

When the scan phase finds multiple implementations of the same abstraction (e.g., MRP Pipeline vs Wiki Agent, multiple AI providers), automatically create a comparison section within the relevant concept page. Do NOT create a separate comparison page unless the comparison is complex enough to warrant 100+ lines.

### Page Sizing Guidelines

- **Target**: 80-200 lines per page (flexible, not rigid)
- **Entity pages**: 60-150 lines (precision-focused)
- **Concept/topic pages**: 100-250 lines (explanation-focused)
- **Split threshold**: > 250 lines → consider splitting
- **Merge threshold**: < 40 lines → merge into parent or related page
- Quality matters more than line count — a precise 60-line entity page is better than a padded 150-line one

## Token Budget

| Level | ~Tokens | When | What |
|-------|---------|------|------|
| L0 | ~200 | Every session | SKILL.md frontmatter |
| L1 | ~2K | Session start | SCHEMA.md + index.md |
| L2 | ~5K | Module scan | Directory tree + config files |
| L3 | ~20K | Deep analysis | Full source files |

## Multi-Agent Strategy

### Phase 1: Scan (3-5 parallel agents, run in background)

```
Agent 1: Project structure + build system detection
Agent 2: Core module identification (entry points, main classes)
Agent 3: Dependency graph + import analysis
Agent 4: Configuration + deployment analysis
Agent 5: Test structure + API surface detection
```

**Concrete implementation**:
- Launch all scan agents with `run_in_background: true`
- Each agent uses `subagent_type: Explore` for efficient codebase traversal
- Agents should read ALL files in their scope, not just headers
- While scan agents run, start generating high-level pages from initial knowledge

### Phase 2: Analyze + Generate (overlapping, not sequential)

**Key insight from practice**: Don't wait for all scans to complete before generating pages. Start generating as soon as you have enough information about a module.

```
Pattern A (recommended — overlapping):
  Scan agents launch → 
  Initial exploration data arrives → 
  Start generating high-level pages (architecture overview, main entities) →
  Deep scan results arrive → 
  Generate detailed pages + enrich existing ones

Pattern B (for small projects < 20 files):
  Single agent reads everything → generates all pages sequentially
```

### Phase 3: Generate (parallel per page, run in background)

```
Agent: For each entity/concept:
  - Apply entity type template
  - Fill frontmatter
  - Write content sections
  - Add wiki-links to related pages
  - Track source files
```

**Practical notes**:
- Use `Write` tool directly for pages where you already have enough context
- Reserve background agents for pages requiring deep source code reading
- Generate 3-5 pages at a time to avoid overwhelming the context

### Phase 4: Link + Reconcile (sequential)

```
Single agent:
  - Build cross-reference map from all generated pages
  - Verify bidirectional links exist (if A links to B, B should link back)
  - Detect orphan pages and add links from related pages
  - Generate/update index.md with all pages
  - Generate/update overview.md with knowledge map
  - Append log.md with operation details
  - Update purpose.md if scope expanded during analysis
```

**Reconciliation checklist**:
- [ ] Every page has ≥ 2 outbound wiki-links
- [ ] Every page is referenced by at least 1 other page
- [ ] index.md lists all pages
- [ ] overview.md has knowledge map section
- [ ] log.md records the generation operation
- [ ] No `[[target]]` links point to non-existent pages (or are marked `[待创建]`)

## Conventions

- **File naming**: lowercase + hyphens, no spaces (`skills-system-architecture.md`)
- **Frontmatter**: required on every page (see `references/frontmatter-schemas.md`)
- **Wiki-links**: `[[filename-without-extension]]` for internal references
- **Source tracking**: every page lists source files in `sources` frontmatter
- **Language**: Chinese (Simplified) for content, English for code/identifiers
- **Verification**: all claims traceable to source code with file:line references

## References

- `references/operations.md` — Full procedures for all commands
- `references/frontmatter-schemas.md` — Frontmatter field definitions
- `references/entity-types.md` — Page type definitions and section structures
- `references/analysis-patterns.md` — How to analyze different project types
- `references/compilation-guide.md` — Writing standards for wiki pages

## Assets

- `assets/purpose-template.md` — Wiki purpose/goals template
- `assets/entity-template.md` — Entity page template
- `assets/concept-template.md` — Concept page template
- `assets/changelog-template.md` — Changelog page template
- `assets/schema-template.md` — SCHEMA.md template
- `assets/index-template.md` — index.md template
- `assets/readme-template.md` — README.md template
- `assets/log-template.md` — log.md template

## Scripts

- `scripts/init-wiki.sh` — Initialize wiki vault directory structure
- `scripts/init-wiki.bat` — Windows version
