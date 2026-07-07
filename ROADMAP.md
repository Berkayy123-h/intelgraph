# IntelGraph — ROADMAP

## Phase Overview

| Phase | Name | Status | Dependencies |
|-------|------|--------|--------------|
| 0 | Foundation | ✅ COMPLETE | None |
| 1 | Core Platform | ⏳ PENDING | Phase 0 |
| 2 | Entity Model | ⏳ PENDING | Phase 1 |
| 2.5 | Canonicalization | ⏳ PENDING | Phase 2 |
| 3 | Storage Layer | ⏳ PENDING | Phase 2.5 |
| 3.5 | Source Registry | ⏳ PENDING | Phase 3 |
| 4 | Collection Framework | ⏳ PENDING | Phase 3.5 |
| 5-N | Individual Collectors | ⏳ PENDING | Phase 4 |
| 8.25 | Evidence Chain Engine | ⏳ PENDING | Phase 4 |
| 8.5 | Human Review Layer | ⏳ PENDING | Phase 8.25 |
| 16 | Release Hardening | ⏳ PENDING | Phase 8.5 |
| 17 | v1.0 Release | ⏳ PENDING | Phase 16 |

## Phase Details

### PHASE 0 — Foundation (CURRENT)
- [x] Vision.md
- [x] Mission.md
- [x] Architecture.md
- [x] ROADMAP.md
- [x] CONTRIBUTING.md
- [ ] SECURITY.md
- [ ] DATA_POLICY.md
- [ ] PROVENANCE_POLICY.md
- [ ] SOURCE_TRUST_MODEL.md
- [ ] RETENTION_POLICY.md

### PHASE 1 — Core Platform
- CLI system with Click
- Config system (YAML-based)
- Structured logging (structlog)
- Correlation ID propagation
- Job runner with dry-run support
- Plugin loader via entry_points
- Output system (JSON, HTML, Markdown)

### PHASE 2 — Entity Model
- Base entity class with ULID, provenance, confidence, trust
- All entity types: Person, Company, Domain, Email, Username, Phone, Website, SocialProfile, IPAddress, Technology, Certificate
- Relationship types: WORKS_FOR, OWNS, USES, CONNECTED_TO, MENTIONS, REGISTERED_TO, ASSOCIATED_WITH, AUTHORED, RELATED_TO
- Relationship validation and constraint enforcement

### PHASE 2.5 — Canonicalization
- Attribute normalization (names, emails, domains, phones)
- Alias resolution rules
- Deduplication engine
- Entity merging with evidence preservation
- Conflict resolution strategy

### PHASE 3 — Storage Layer
- SQLite adapter (dev, default)
- PostgreSQL adapter (prod)
- Schema versioning with migrations
- Audit trail storage
- Historical snapshots
- Provenance and confidence persistence

### PHASE 3.5 — Source Registry
- Source metadata schema
- Trust score calculator
- Reliability score calculator
- Source tier classification
- Validation timestamp tracking

### PHASE 4 — Collection Framework
- Base collector class
- Retry with exponential backoff
- Timeout enforcement
- Dry-run mode
- Rate limiting
- Output schema enforcement
- Independent testability

### PHASE 5-N — Individual Collectors
- Domain WHOIS collector
- DNS resolution collector
- Certificate Transparency log collector
- Website scraper (basic)
- Social username checker
- Email format generator
- Technology stack detector
- Public repository scanner

### PHASE 8.25 — Evidence Chain Engine
- Evidence chain construction
- Step-by-step traceability
- Source lineage tracking
- Chain validation
- Chain visualization support

### PHASE 8.5 — Human Review Layer
- Confidence threshold configuration
- Auto-merge (90-100)
- Review queue (70-89)
- Reject (0-69)
- Manual override with audit log
- Merge explainability

### PHASE 16 — Release Hardening
- CI/CD pipeline (GitHub Actions)
- Security audit
- Full test matrix
- Fresh install validation
- Cross-platform testing (Ubuntu, Kali, Windows, macOS)

### PHASE 17 — v1.0 Release
- Stable release tagging
- User documentation
- Sample investigations
- Sample datasets
- Release announcement

## Timeline Estimates

| Phase | Estimated Effort | Complexity |
|-------|-----------------|------------|
| Phase 0 | 1 session | Low |
| Phase 1 | 2-3 sessions | Medium |
| Phase 2 | 2-3 sessions | Medium |
| Phase 2.5 | 1-2 sessions | Medium |
| Phase 3 | 2-3 sessions | High |
| Phase 3.5 | 1 session | Low |
| Phase 4 | 2 sessions | Medium |
| Phase 5-N | 1-2 sessions per collector | Varies |
| Phase 8.25 | 2 sessions | High |
| Phase 8.5 | 1-2 sessions | Medium |
| Phase 16 | 2-3 sessions | High |
| Phase 17 | 1 session | Low |

## Guiding Principles for Roadmap Execution

1. **No phase skipping** — Each phase builds on the previous
2. **Quality gates** — Each phase must pass review before next begins
3. **Test coverage** — Each phase must include tests
4. **Documentation** — Each phase must include documentation
5. **Backward compatibility** — No breaking changes within a release cycle
