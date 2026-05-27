# Operations Reference

Complete procedures for each pipeline stage. SKILL.md contains the decision framework; this file contains the execution details.

---

## Init — Initialize Wiki

### Usage
```bash
bash .claude/skills/llm-wiki/scripts/init-wiki.sh <project-path> [--name <wiki-name>]
```

### Steps

1. **Validate project path**: confirm directory exists and contains source code
2. **Detect project type** (auto):
   - Language detection: file extension analysis
   - Framework detection: config file patterns
   - Build system detection: Makefile, CMakeLists.txt, package.json, pyproject.toml, etc.
3. **Create directory structure**:
   ```
   <wiki-name>/
   ├── entities/          # Core classes, modules
   ├── concepts/          # Architecture patterns, design decisions
   ├── changelog/         # Version history
   ├── _archive/          # Deprecated pages
   ├── SCHEMA.md          # Wiki schema and conventions
   ├── index.md           # Main table of contents
   ├── README.md          # Wiki introduction
   ├── log.md             # Operations log
   └── purpose.md         # Wiki goals and scope
   ```
4. **Generate SCHEMA.md**: from template, filled with detected project metadata
5. **Generate index.md**: from template, empty categories
6. **Generate README.md**: from template, filled with project info
7. **Generate log.md**: from template, first entry
8. **Generate purpose.md**: from template, filled with detected project scope
9. **Initialize git** (if not already a repo)

### Project Detection Rules

| Config File | Language | Framework | Build System |
|-------------|----------|-----------|--------------|
| `pyproject.toml` | Python | Detect from deps | uv/poetry/setuptools |
| `package.json` | JavaScript/TypeScript | Detect from deps | npm/yarn/pnpm |
| `Cargo.toml` | Rust | Detect from deps | cargo |
| `go.mod` | Go | Detect from deps | go modules |
| `CMakeLists.txt` | C/C++ | Detect | cmake |
| `Makefile` | C/C++/Any | Detect | make |
| `pom.xml` / `build.gradle` | Java | Spring/etc | maven/gradle |
| `*.sln` / `*.csproj` | C# | .NET/ASP.NET | msbuild/dotnet |
| `Gemfile` | Ruby | Rails/Sinatra | bundler |
| `mix.exs` | Elixir | Phoenix | mix |
| `composer.json` | PHP | Laravel/Symfony | composer |

---

## Full — One-Shot Pipeline (Recommended for First Use)

### When to Use
- First time analyzing a project
- User says "generate wiki for this project" or gives a project path without specific command

### Steps

1. **Validate project path**: confirm directory exists and contains source code
2. **Detect wiki root**:
   - Check if current directory has `.wiki-schema.md` → use as wiki root
   - Check if `~/.llm-wiki-path` exists → use that path
   - Otherwise → ask user for wiki location or auto-create `<project-dir>-Wiki/`
3. **Determine directory structure**: if wiki has `.wiki-schema.md`, use `wiki/entities/` + `wiki/topics/`; otherwise use `entities/` + `concepts/`
4. **Fill purpose.md**: write research goals based on detected project type
5. **Launch parallel scan agents** (3-5, based on project size):
   - Each agent gets a specific scope (AI modules, database, services, frontend, docs)
   - Run in background (`run_in_background: true`)
6. **Start generating high-level pages** while scans run:
   - Architecture overview (topic page)
   - Main entity pages based on initial exploration
7. **When scan agents complete**: use detailed results to generate/enrich remaining pages
8. **Reconcile**:
   - Build cross-reference map
   - Add bidirectional links
   - Verify all `[[target]]` links resolve
   - Update index.md, overview.md, log.md
9. **Output summary**: show user what was created

### Practical Tips (from real usage)

- **Don't wait for all scans to finish** before generating pages. Start with high-level pages from initial exploration, then enrich when detailed scans complete.
- **4 agents is the sweet spot** for most projects: (1) AI/core modules, (2) database/models, (3) services/routers/config, (4) frontend/docs/infra
- **Write pages directly with Write tool** when you have enough context; reserve background agents for deep source reading
- **Generate 3-5 pages at a time** in parallel Write calls to maximize throughput
- **Purpose.md is critical**: fill it early. It guides what entities and concepts to prioritize
- **Comparison detection**: if you find two approaches to the same problem (e.g., MRP Pipeline vs Wiki Agent), add a comparison section within the relevant concept page

---

## Scan — Project Structure Analysis

### Pre-scan: Determine Agent Count

Before launching agents, quickly assess project size:
```bash
# Count source files (exclude node_modules, .git, __pycache__, etc.)
find <project-path> -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.go" -o -name "*.rs" -o -name "*.java" -o -name "*.cpp" -o -name "*.c" -o -name "*.h" \) | grep -v node_modules | grep -v __pycache__ | grep -v .git | wc -l
```

| File Count | Strategy | Agents |
|------------|----------|--------|
| < 20 | Single agent reads everything | 1 |
| 20-100 | 3 parallel agents | 3 |
| 100-500 | 5 parallel agents | 5 |
| > 500 | 5 scan agents + per-module analyze | 5 + N |

### Multi-Agent Parallel Scan

Launch 3-5 parallel agents:

**Agent 1: Structure Scanner**
```
Goal: Build complete directory tree, identify entry points
Output: Directory tree + entry point list
```

**Agent 2: Module Mapper**
```
Goal: Identify core modules, their responsibilities and boundaries
Output: Module map with file assignments
```

**Agent 3: Dependency Analyzer**
```
Goal: Map import/dependency relationships between modules
Output: Dependency graph
```

**Agent 4: Config Analyzer**
```
Goal: Analyze configuration, build, deployment setup
Output: Config summary + environment requirements
```

**Agent 5: API Surface Detector**
```
Goal: Find public APIs, interfaces, exported functions/classes
Output: API surface map
```

### Output: Project Profile

```json
{
  "name": "project-name",
  "language": "Python",
  "framework": "FastAPI",
  "build_system": "uv",
  "entry_points": ["main.py", "cli.py"],
  "modules": [
    {
      "name": "core",
      "path": "src/core/",
      "responsibility": "Core business logic",
      "key_files": ["core.py", "models.py"],
      "dependencies": ["utils", "db"]
    }
  ],
  "architecture_pattern": "layered",
  "has_tests": true,
  "has_docs": true
}
```

Save to `<wiki-root>/.cache/project-profile.json`

---

## Analyze — Deep Module Analysis

### Single Module Analysis

For each module identified in Scan:

1. **Read all source files** in module (L3 token budget)
2. **Extract**:
   - Classes with their methods and attributes
   - Functions with signatures and docstrings
   - Constants and configuration
   - Import relationships
   - Error handling patterns
   - Threading/concurrency patterns
3. **Identify design patterns**:
   - Factory, Observer, Strategy, Adapter, etc.
   - Architecture patterns (MVC, MVVM, Clean Architecture, etc.)
   - Custom patterns specific to the project
4. **Map interactions**:
   - Which other modules does this one call?
   - Which modules call this one?
   - What events/callbacks does it produce/consume?
5. **Generate analysis summary**:
   - Module purpose (2-3 sentences)
   - Key entities (classes worth documenting)
   - Key concepts (patterns worth explaining)
   - Source files list

### Output Per Module

```json
{
  "module": "core",
  "purpose": "Core business logic for...",
  "entities": [
    {"name": "UserManager", "type": "entity", "priority": "high"},
    {"name": "AuthMiddleware", "type": "entity", "priority": "medium"}
  ],
  "concepts": [
    {"name": "authentication-flow", "type": "concept", "priority": "high"},
    {"name": "caching-strategy", "type": "concept", "priority": "medium"}
  ],
  "source_files": ["src/core/user.py", "src/core/auth.py"],
  "dependencies": ["utils", "db"],
  "dependents": ["api", "cli"]
}
```

---

## Generate — Create Wiki Pages

### Page Generation Strategy

Launch parallel agents, one per page to generate.

**For Entity pages**:
1. Read entity template (`assets/entity-template.md`)
2. Read analysis result for this entity
3. Read source files referenced in analysis (L3)
4. Fill template with extracted information
5. Add wiki-links to related entities/concepts
6. Write frontmatter with tags and sources

**For Concept pages**:
1. Read concept template (`assets/concept-template.md`)
2. Read analysis result for this concept
3. Read all source files that contribute to this concept (L3)
4. Fill template with architecture explanation
5. Add design decision table
6. Add data flow diagram (text-based)
7. Add wiki-links to related entities/concepts
8. Write frontmatter with tags and sources

### Quality Standards

- Every page: min 100 lines, max 300 lines
- Every page: min 2 outbound wiki-links
- Every page: source file references with line ranges
- Every page: frontmatter complete
- Code snippets: real code from source, not invented
- No "TODO" or placeholder content in generated output

---

## Update — Incremental Update

### Steps

1. **Detect changes**: `git diff --name-only HEAD~N` or file modification time
2. **Classify changes**:
   - New files → may need new pages
   - Modified files → check which pages reference these files
   - Deleted files → mark affected pages for review
3. **Update affected pages**:
   - Re-read changed source files
   - Update page content using structured diff format
   - Show diff to user for confirmation
4. **Add new pages** if new significant entities/concepts emerged
5. **Update index.md** with any new pages
6. **Append log.md**

### Structured Diff Format

```markdown
### Change: [description]

**Current**: [existing text]
**Proposed**: [new text]
**Reason**: [why this changes]
**Source**: `file:line-range`
```

---

## Lint — Health Check

### Automated Checks

| Check | Description | Fix |
|-------|-------------|-----|
| Broken wikilinks | `[[target]]` page doesn't exist | Create stub or remove link |
| Missing frontmatter | Page lacks YAML frontmatter | Add from template |
| Stale content | `updated:` older than source change | Flag for re-analysis |
| Orphan pages | No inbound links | Add links from related pages |
| Missing index entries | Page not in `index.md` | Add to appropriate category |
| Over-length pages | > 300 lines | Suggest split points |
| Under-linked pages | < 2 outbound links | Suggest link targets |
| Missing sources | No source file references | Flag for re-analysis |
| Format violations | Missing sections per entity type | Add missing sections |

### Graph Analysis

```bash
# Bridge nodes (link to 3+ different categories)
grep -roh '\[\[[^/\]]*/' concepts/ entities/ | sort | uniq -c | sort -rn

# Isolated pages (< 2 links)
grep -rl '\[\[' . | while read f; do
  links=$(grep -o '\[\[[^]]*\]\]' "$f" | wc -l)
  [ "$links" -lt 2 ] && echo "$links $f"
done

# Missing pages (referenced but don't exist)
grep -roh '\[\[[^]/|]*' . | sed 's/\[\[//' | sort | uniq -c | sort -rn | head -20 | while read count name; do
  find . -name "${name}.md" -print -quit | grep -q . || echo "$count $name (MISSING)"
done
```

### Output: Health Report

Save to `<wiki-root>/lint-report.md`

---

## Query — Ask from Wiki

### Steps

1. Read `index.md` (L1) to find relevant pages
2. Read relevant pages (L3) following one layer of wiki-links
3. Synthesize answer with citations: `(from [[page-name]])`
4. Mark gaps: "No wiki page about X"
5. Save answer to conversation (no file output needed for codebase wiki)

### Anti-patterns

- Answer from memory without reading wiki
- No citations
- Skip gap identification

---

## Log — Append to log.md

After every operation. Format: `## [YYYY-MM-DD] <operation> | <description>`

Operations: `init` · `scan` · `analyze` · `generate` · `update` · `lint` · `query` · `create` · `archive` · `delete`

```bash
# Recent activity
grep "^## \[" log.md | tail -10

# Total pages generated
grep "^## \[.*generate" log.md | wc -l
```
