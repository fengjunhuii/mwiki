# Analysis Patterns

How to analyze different types of projects. This guide helps agents adapt their analysis strategy based on the detected project type.

---

## Python Projects

### Detection
- `pyproject.toml`, `setup.py`, `requirements.txt`, `Pipfile`
- `*.py` files

### Key Files to Analyze
| Priority | Pattern | What to Look For |
|----------|---------|------------------|
| P0 | `__main__.py`, `main.py`, `app.py` | Entry points |
| P0 | `pyproject.toml` | Dependencies, project metadata |
| P1 | `src/*/` or `*/__init__.py` | Package structure |
| P1 | `*/models.py`, `*/schemas.py` | Data models |
| P1 | `*/routes.py`, `*/views.py`, `*/api.py` | API surface |
| P2 | `*/config.py`, `*/settings.py` | Configuration |
| P2 | `tests/` | Test structure |
| P3 | `*/utils.py`, `*/helpers.py` | Utility functions |

### Framework-Specific Patterns

**FastAPI**: Look for `APIRouter`, `Depends`, `BaseModel`
- Async patterns: `async def`, `async with`, `AsyncSession`
- Dependency injection: `Depends(get_db)`, `Depends(get_current_user)`
- Background tasks: `arq` workers, `BackgroundTasks`, Redis job queues
- ORM: SQLAlchemy 2.0 async (`select()`, `scalars()`, `execute()`)
- Pydantic models: separate input/output/response schemas
- Middleware: auth, CORS, error handling chains
- API versioning: router prefixes (`/api/v1/`)
- File handling: `UploadFile`, MinIO/S3 integration
**Django**: Look for `models.py`, `views.py`, `urls.py`, `settings.py`
**Flask**: Look for `Flask(__name__)`, `@app.route`, blueprints
**CLI (Click/Typer)**: Look for `@click.command`, `@app.command`
**AI/ML**: Look for `torch`, `transformers`, `openai`, model definitions

### Module Detection Strategy
1. Identify top-level packages (directories with `__init__.py`)
2. For each package, check if it's a standalone module or sub-package
3. Map import chains: who imports whom
4. Identify circular dependencies (warning sign)

---

## JavaScript/TypeScript Projects

### Detection
- `package.json`, `tsconfig.json`, `*.js`, `*.ts`, `*.tsx`

### Key Files to Analyze
| Priority | Pattern | What to Look For |
|----------|---------|------------------|
| P0 | `package.json` | Dependencies, scripts, entry points |
| P0 | `src/index.ts`, `src/main.ts`, `src/app.ts` | Entry points |
| P1 | `src/routes/`, `src/controllers/` | API surface |
| P1 | `src/models/`, `src/types/` | Data models |
| P1 | `src/services/`, `src/lib/` | Business logic |
| P2 | `src/config/`, `.env.example` | Configuration |
| P2 | `src/middleware/` | Middleware chains |
| P3 | `tests/`, `__tests__/` | Test structure |

### Framework-Specific Patterns

**React**: Look for `components/`, `hooks/`, `pages/`, `useContext`
**Next.js**: Look for `app/` or `pages/` directory, `getServerSideProps`
**Express**: Look for `router`, `middleware`, controller pattern
**NestJS**: Look for `@Module`, `@Controller`, `@Injectable` decorators

---

## Go Projects

### Detection
- `go.mod`, `*.go`

### Key Files to Analyze
| Priority | Pattern | What to Look For |
|----------|---------|------------------|
| P0 | `go.mod` | Module name, dependencies |
| P0 | `main.go`, `cmd/` | Entry points |
| P1 | `internal/` | Private packages |
| P1 | `pkg/` | Public packages |
| P1 | `api/` | API definitions |
| P2 | `config/` | Configuration |
| P3 | `*_test.go` | Test files |

### Pattern Detection
- Interface-based design: `type Foo interface { ... }`
- Error wrapping: `fmt.Errorf("...: %w", err)`
- Goroutine patterns: `go func()`, channels
- Middleware chains: `func(http.Handler) http.Handler`

---

## Rust Projects

### Detection
- `Cargo.toml`, `*.rs`

### Key Files to Analyze
| Priority | Pattern | What to Look For |
|----------|---------|------------------|
| P0 | `Cargo.toml` | Dependencies, features |
| P0 | `src/main.rs`, `src/lib.rs` | Entry points |
| P1 | `src/*/mod.rs` | Module structure |
| P1 | `src/models/` | Data structures |
| P2 | `src/config/` | Configuration |
| P3 | `tests/` | Integration tests |

### Pattern Detection
- Trait-based design: `trait Foo { ... }`
- Error handling: `Result<T, E>`, `?` operator
- Async: `async fn`, `tokio`, `async-std`
- Macro usage: `macro_rules!`, proc macros

---

## C/C++ Projects

### Detection
- `CMakeLists.txt`, `Makefile`, `*.c`, `*.cpp`, `*.h`

### Key Files to Analyze
| Priority | Pattern | What to Look For |
|----------|---------|------------------|
| P0 | `CMakeLists.txt`, `Makefile` | Build configuration |
| P0 | `src/main.c`, `src/main.cpp` | Entry points |
| P1 | `include/` | Public headers |
| P1 | `src/core/` | Core implementation |
| P2 | `src/utils/` | Utilities |
| P3 | `test/` | Test files |

### Pattern Detection
- OOP vs procedural style
- Memory management patterns (RAII, manual alloc/free)
- Threading model (pthreads, std::thread)
- Callback/function pointer patterns

---

## Architecture Pattern Detection

Regardless of language, detect these common patterns:

| Pattern | Indicators |
|---------|------------|
| Layered | Clear separation: presentation → business → data |
| MVC | Models, Views, Controllers directories |
| Microservices | Multiple services, API gateways, service discovery |
| Event-driven | Event bus, pub/sub, message queues |
| Pipeline | Sequential processing stages |
| Plugin | Dynamic loading, registration systems |
| Adapter/Strategy | Multiple implementations behind interface |
| Repository | Data access abstraction layer |
| CQRS | Separate read/write models |
| Hexagonal | Ports and adapters |

---

## Multi-Agent Scan Strategy

When scanning a codebase with parallel agents, assign scopes based on project type:

### Typical 4-Agent Split (Medium Projects, 20-100 files)

| Agent | Scope | Key Questions |
|-------|-------|---------------|
| Structure Scanner | Directory tree, configs, build files, env | What's the tech stack? Entry points? |
| Core Module Mapper | Business logic, models, core classes | What are the main entities? Design patterns? |
| Service/API Analyzer | Routes, controllers, middleware, external APIs | What's the API surface? Auth model? |
| Infrastructure Scanner | Tests, deployment, CI/CD, docs | How is it deployed? Test coverage? |

### Agent Prompt Template

```
Goal: [specific scope description]
Output: [what information to collect]
Focus files: [glob patterns]
Skip: [directories to ignore, e.g., node_modules, __pycache__, .git]
```

### Practical Tips (from real usage)

- **4 agents is the sweet spot** for most medium projects
- Don't wait for all scans to finish before generating pages — start with initial exploration
- Agents sometimes drift off-task — check their output for relevance before using
- Structure scanner should run first and lightest — its output guides the other agents
- For AI/LLM projects, dedicate an agent to the AI pipeline (providers, embeddings, agent loops)

---

## Module Boundary Detection Heuristics

1. **Directory = module**: Top-level directories usually represent modules
2. **Namespace = module**: Package/namespace declarations indicate boundaries
3. **Config file scope**: Each config section often maps to a module
4. **Test file mapping**: Test directories mirror source structure
5. **Import clustering**: Files that import each other frequently form a module
