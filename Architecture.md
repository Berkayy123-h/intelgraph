# IntelGraph — Architecture

## High-Level Architecture Diagram (Text)

```
┌─────────────────────────────────────────────────────────┐
│                        CLI Layer                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │  intel   │  │  graph   │  │  verify  │  │ report │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └───┬────┘  │
└───────┼──────────────┼──────────────┼────────────┼──────┘
        │              │              │            │
┌───────┴──────────────┴──────────────┴────────────┴──────┐
│                    Orchestration Layer                    │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │  Job Runner  │  │  Plugin Mgr  │  │  Pipeline Exec │  │
│  └──────┬──────┘  └──────┬───────┘  └───────┬────────┘  │
└─────────┼─────────────────┼──────────────────┼──────────┘
          │                 │                  │
┌─────────┴─────────────────┴──────────────────┴──────────┐
│                    Collection Layer                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│  │ Domain   │ │ Person   │ │ Company  │ │ Social   │    │
│  │Collectors│ │Collectors│ │Collectors│ │Collectors│    │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘    │
└───────┼──────────────┼──────────────┼───────────┼───────┘
        │              │              │           │
┌───────┴──────────────┴──────────────┴───────────┴───────┐
│                   Normalization Layer                     │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │ Canonicalizer │  │Deduplicator  │  │ Alias Resolver│  │
│  └──────┬───────┘  └──────┬───────┘  └───────┬───────┘  │
└─────────┼──────────────────┼──────────────────┼──────────┘
          │                  │                  │
┌─────────┴──────────────────┴──────────────────┴──────────┐
│                     Entity Model Layer                     │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐  │
│  │Person│ │Company│ │Domain│ │Email │ │Phone │ │Social│  │
│  └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘  │
│  ┌──┴───┐ ┌──┴───┐ ┌──┴───┐ ┌──┴───┐ ┌──┴───┐ ┌──┴───┐  │
│  │Relationships between entities                          │
│  └──────────────────────────────────────────────────────┘ │
└──────────────────────────┬────────────────────────────────┘
                           │
┌──────────────────────────┴────────────────────────────────┐
│                     Storage Layer                           │
│  ┌────────────┐  ┌────────────┐  ┌────────────────────┐  │
│  │ SQLite     │  │ PostgreSQL │  │  Evidence Store     │  │
│  │ (dev)      │  │ (prod)     │  │  + Audit Trail      │  │
│  └────────────┘  └────────────┘  └────────────────────┘  │
└────────────────────────────────────────────────────────────┘
                           │
┌──────────────────────────┴────────────────────────────────┐
│                     Output Layer                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  JSON    │  │  HTML    │  │ Markdown │  │  GraphML  │  │
│  │ Export   │  │ Report   │  │ Report   │  │ Export    │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└────────────────────────────────────────────────────────────┘
```

## Layered Architecture Principles

### 1. Strict Separation of Concerns
Each layer has exactly one responsibility. No layer crosses boundaries.

### 2. Dependency Direction
Dependencies flow downward. CLI depends on Orchestration. Orchestration depends on Collection. No upward dependencies.

### 3. Plugin Architecture
Collectors are plugins. The platform runs with zero collectors. Collectors are loaded dynamically at runtime.

### 4. Event-Driven Pipeline
Each phase emits events. Downstream phases subscribe. Phases can be added, removed, or reordered without changing other phases.

### 5. Immutable Data Flow
Once a collector produces data, that raw data is never modified. Normalization creates new normalized records. Original raw data is preserved for audit.

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Language | Python 3.11+ | Best OSINT ecosystem, wide library support |
| CLI Framework | Click | Battle-tested, composable, well-documented |
| Storage (dev) | SQLite | Zero-config, portable, sufficient for development |
| Storage (prod) | PostgreSQL | Mature, reliable, excellent JSON support |
| Output Format | JSON (canonical) | Universal, composable, machine-readable |
| Plugin System | Python entry_points | Native, no custom loader needed |
| Config Format | YAML | Human-readable, supports complex structures |
| Logging | structlog | Structured, JSON-serializable, correlation IDs |

## Project Structure

```
intelgraph/
├── pyproject.toml
├── intelgraph/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── collect.py
│   │   ├── graph.py
│   │   ├── verify.py
│   │   └── report.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── logging.py
│   │   ├── job.py
│   │   ├── plugin.py
│   │   └── correlation.py
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── person.py
│   │   ├── company.py
│   │   ├── domain.py
│   │   ├── email.py
│   │   ├── username.py
│   │   ├── phone.py
│   │   ├── website.py
│   │   ├── social_profile.py
│   │   ├── ip_address.py
│   │   ├── technology.py
│   │   ├── certificate.py
│   │   └── relationships.py
│   ├── normalization/
│   │   ├── __init__.py
│   │   ├── canonicalizer.py
│   │   ├── deduplicator.py
│   │   └── alias_resolver.py
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── sqlite.py
│   │   ├── postgres.py
│   │   ├── migrations.py
│   │   └── models.py
│   ├── collectors/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── registry.py
│   ├── evidence/
│   │   ├── __init__.py
│   │   ├── chain.py
│   │   └── store.py
│   ├── output/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── json_output.py
│   │   ├── html_output.py
│   │   └── markdown_output.py
│   ├── review/
│   │   ├── __init__.py
│   │   ├── queue.py
│   │   ├── thresholds.py
│   │   └── merge.py
│   └── trust/
│       ├── __init__.py
│       ├── scorer.py
│       └── source_registry.py
└── docs/
    ├── Vision.md
    ├── Mission.md
    ├── Architecture.md
    └── ...
```

## Architectural Invariants

1. The platform MUST function with zero collectors installed
2. No collector can modify another collector's data
3. Every entity MUST have a globally unique ID (ULID)
4. Every relationship MUST reference two entity IDs
5. Every evidence item MUST reference an entity or relationship ID
6. Raw data is immutable once stored
7. All state changes MUST be logged
8. Every operation MUST carry a correlation ID
