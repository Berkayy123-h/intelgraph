# IntelGraph

**Open-source threat intelligence platform** — correlates IOCs from multiple sources using a knowledge graph with explainable, evidence-based alerts.

Built for **SOC analysts**, **threat intelligence teams**, **incident responders**, and **security researchers** who need to validate indicators faster and reduce false positives.

## What It Does

IntelGraph collects raw threat data from public intelligence feeds, extracts entities (IPs, domains, URLs, hashes, CVEs), resolves them into a knowledge graph, and generates evidence-backed alerts. Every alert includes a complete reasoning chain showing **why** a decision was reached.

### Differentiating Features

- **Multi-source IOC correlation** — URLhaus, CISA KEV, AlienVault OTX, Shodan, VirusTotal
- **Knowledge graph** — D3.js interactive visualization with graph algorithms (centrality, communities, attack paths)
- **Explainable alerts** — Every decision includes an evidence chain with source attribution and confidence scoring
- **STIX 2.1 / TAXII 2.1** — Industry-standard export and sharing
- **Anomaly detection** — Z-score, temporal spike, and relationship outlier algorithms
- **Playbook automation** — Rule-based response engine with 11 matching criteria
- **Enterprise features** — Multi-tenant isolation, TOTP 2FA, OAuth2, API key rotation, role-based access

## Quick Start

### Prerequisites

- Python 3.11+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Berkayy123-h/intelgraph.git
cd intelgraph

# Create a virtual environment
python3 -m venv .venv && source .venv/bin/activate

# Install the package and dependencies
pip install -e .

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your settings (minimal: set INTELGRAPH_SECRET_KEY)
```

### Run the CLI

```bash
# View available commands
intelgraph --help

# Collect intelligence from sources
intelgraph collect --sources urlhaus,kev

# Query the knowledge graph
intelgraph graph summary
```

### Run the Web Dashboard

```bash
uvicorn intelgraph.api.main:create_app --factory --host 0.0.0.0 --port 8000
```

Open http://localhost:8000 in your browser. Register a user via the login panel, then explore the dashboard.

### Run Tests

```bash
pip install -e ".[dev]"
python3 -m pytest tests/ -q
```

## Architecture

IntelGraph is organized into three layers:

```
CLI Layer         — Click-based command-line interface (18 commands)
API Layer         — FastAPI web server with dashboard, REST API, SSE streaming
Core Library      — Pipeline engine, knowledge graph, collectors, analyzers, exporters
```

Key directories:

| Path | Purpose |
|---|---|
| `intelgraph/cli/` | CLI commands (collect, graph, verify, report, etc.) |
| `intelgraph/api/` | FastAPI application, routers, auth, middleware |
| `intelgraph/core/` | Core engine: graph, pipeline, collectors, export, notification, etc. |
| `intelgraph/web/` | Dashboard HTML (single-page app) |
| `docs/` | Landing page and deployment config |
| `tests/` | 1,535+ tests |

## Environment Variables

See [.env.example](.env.example) for all available configuration options. Key variables:

| Variable | Required | Default | Description |
|---|---|---|---|
| `INTELGRAPH_SECRET_KEY` | Yes | — | JWT signing key (min 32 chars) |
| `OTX_API_KEY` | No | — | AlienVault OTX API key |
| `VIRUSTOTAL_API_KEY` | No | — | VirusTotal API key |
| `SHODAN_API_KEY` | No | — | Shodan API key |
| `INTELGRAPH_DB_PATH` | No | `intelgraph.db` | SQLite database path |

## Project Status

- **1,535+ passing tests**
- **37 active modules**
- **5 intelligence source integrations**
- **~94% average alert confidence**

## Contact

- **Email:** [contact@intelgraph.io](mailto:contact@intelgraph.io)
- **GitHub:** [github.com/Berkayy123-h/intelgraph](https://github.com/Berkayy123-h/intelgraph)
- **Landing Page:** [intelgraph.vercel.app](https://intelgraph.vercel.app)

## License

MIT
