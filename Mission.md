# IntelGraph — Mission

## Mission Statement

Build a production-grade, open-source intelligence platform that ingests raw public data, resolves it into verified entities with evidence-backed relationships, and outputs structured intelligence graphs suitable for investigation, analysis, and decision-making.

## Core Objectives

1. **Deterministic Collection** — Given the same input, produce the same output. Every time.
2. **Verification-First Architecture** — No data point enters the graph without a confidence score, trust score, and provenance record.
3. **Complete Evidence Chains** — Every relationship in the graph must be traceable from source to conclusion through explicit, auditable steps.
4. **Human-in-the-Loop Verification** — Automation handles volume; humans handle ambiguity. Threshold-driven review queues ensure quality.
5. **Open and Auditable** — Every action is logged. Every decision is explainable. Every output is JSON-serializable.

## Scope Boundaries

### IN SCOPE
- Public DNS records, WHOIS data, Certificate Transparency logs
- Public social media profiles and usernames
- Public company registries and official websites
- Public conference talks, author pages, and publications
- Open-source code repositories and public commits

### OUT OF SCOPE
- Private databases, leaked credentials, stolen data
- Social engineering or phishing
- Active scanning without authorization
- Private API access without agreement
- Any data that requires authentication bypass

## Success Metrics

| Metric | Target |
|--------|--------|
| Collector reproducibility | 100% (same input → same output) |
| Evidence chain completeness | Every relationship ≥ 1 evidence item |
| System uptime | 99.9% (platform components) |
| False positive rate | < 5% on auto-merged entities |
| Human review coverage | 100% of entities below 90 confidence |

## Non-Goals (v1.0)

- Real-time streaming
- API-first access (CLI-first in v1.0)
- Graphical UI (HTML reports are sufficient)
- Machine learning classification
- Automated exploitation or validation
