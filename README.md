# IntelGraph

> IntelGraph is an **open-source threat intelligence platform** that helps SOC analysts and incident responders investigate threats by correlating indicators across multiple intelligence sources and explaining every alert with an evidence-based reasoning chain.

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests: 1450+](https://img.shields.io/badge/Tests-1450%2B-brightgreen.svg)](#testing)
[![Status: Active Development](https://img.shields.io/badge/Status-Active%20Development-yellow.svg)](#)

---

## Built With

✔ **1,535+** automated tests  
✔ **5** CTI sources (URLhaus, OTX, CISA KEV, Shodan, VirusTotal)  
✔ **STIX 2.1** export compatible  
✔ **Knowledge Graph** engine with temporal tracking  
✔ **Real-time** enrichment & correlation  

---

## Use Cases

- **Investigate threats** - Suspicious IPs, domains, URLs, hashes, and CVEs from multiple intelligence sources
- **Correlate indicators** - Link related IOCs into an interactive knowledge graph
- **Reduce false positives** - Validate indicators across multiple trusted sources
- **Support investigations** - Explainable evidence chains for every alert
- **Share intelligence** - Export investigations as STIX 2.1 bundles for MISP, OpenCTI, or other platforms

---

## Why IntelGraph?

Unlike traditional threat intelligence platforms that only aggregate indicators, **IntelGraph explains WHY an IOC is malicious**.

| Feature | Description |
|---------|-------------|
| 🔗 **Multi-source Correlation** | Correlates data from 5 threat sources |
| 📋 **Evidence Chains** | Tracks provenance and reasoning |
| 📊 **Knowledge Graph** | Visualizes threat relationships |
| 🚨 **Contradiction Detection** | Identifies conflicting intelligence |
| 📤 **STIX Export** | Standards-compliant sharing |

### Positioning

IntelGraph complements existing CTI platforms by focusing on:

- **Explainable intelligence** - See why an indicator is malicious
- **Evidence-driven correlation** - Track the reasoning chain
- **Knowledge graph analysis** - Visualize threat relationships
- **Automated enrichment workflows** - Real-time data integration

**Compared with:**
- **OpenCTI** - Extensive CTI management platform
- **MISP** - Collaborative IOC sharing platform  
- **Commercial TIPs** - Enterprise intelligence suites

---

## ✨ Core Features

### 📊 Multi-Source Pipeline (5 Sources)
```python
# Automatically aggregates from:
- URLhaus       # Malicious URLs
- OTX           # Community intelligence  
- CISA KEV      # Known exploited vulnerabilities
- Shodan        # Device data
- VirusTotal    # File analysis
```

### 🧠 Entity Processing
- **Custom NER** - Extracts threats from raw text
- **Deduplication** - O(n) hash-index matching
- **Confidence Scoring** - Evidence-based reliability
- **Contradiction Detection** - Conflicting intelligence alerts

### 📈 Temporal Knowledge Graph
- Timeline tracking of threat evolution
- Attack path visualization
- Relationship mapping
- Historical trend analysis

### ⚡ Real-Time Enrichment
```python
POST /api/v1/enrichment/ip
{"ip": "192.0.2.1"}
# Returns: Shodan data + reputation + CVEs
```

### 🤖 Automated Playbooks
- Event-driven response rules
- Alert enrichment workflows
- Webhook integration
- Custom automation framework

### 📱 Real-Time Dashboard
- D3.js force graph visualization
- Live data streaming (SSE)
- Full-text search
- Interactive threat correlation

### 🔐 Security Features
- JWT authentication
- Role-based access control
- Sliding-window rate limiting
- Audit logging

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL or SQLite

### Installation

```bash
git clone https://github.com/Berkayy123-h/intelgraph.git
cd intelgraph

uv sync
cp .env.example .env
```

### Configuration

Edit `.env`:
```env
DATABASE_URL=postgresql://user:pass@localhost/intelgraph
JWT_SECRET_KEY=your-secret-key
SHODAN_API_KEY=your-key
VIRUSTOTAL_API_KEY=your-key
```

### Run

```bash
uv run python -m intelgraph.api.server
# Open http://localhost:8000
```

### Test

```bash
uv run pytest tests/ -v --cov=intelgraph
```

---

## 📊 Architecture

```
Threat Feeds (5 sources)
       │
       ▼
   Collectors
       │
       ▼
  Normalization
       │
       ▼
 Knowledge Graph
       │
   ┌───┴────┐
   ▼        ▼
Alerts  Investigation
   │        │
   └────┬───┘
        ▼
  STIX/TAXII Export
```

**Project Structure:**
```
intelgraph/
├── api/              # FastAPI endpoints
├── core/             # Intelligence engine
├── pipeline/         # Multi-source aggregation
├── graph/            # Knowledge graph
├── enrichment/       # Shodan, VirusTotal
├── search/           # Full-text search (FTS5)
├── auth/             # JWT + RBAC
├── models/           # STIX data models
└── config/           # Configuration

tests/                # 1450+ tests
docs/                 # Documentation
```

---

## 🔌 API Examples

### Search Threats
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/v1/threats/search?q=ransomware"
```

### Enrich IP Address
```bash
curl -X POST http://localhost:8000/api/v1/enrichment/ip \
  -H "Content-Type: application/json" \
  -d '{"ip": "192.0.2.1"}'

# Response:
# {
#   "ip": "192.0.2.1",
#   "shodan": {...},
#   "reputation": "malicious",
#   "cves": [...]
# }
```

### Export as STIX
```bash
curl http://localhost:8000/api/v1/export/stix?threat_id=threat_123
# Returns STIX 2.1 formatted JSON
```

### Knowledge Graph
```bash
curl http://localhost:8000/api/v1/graph/relationships?entity_id=malware_456
# Returns: Related entities, attack paths, timeline
```

---

## 🧪 Testing

```bash
# Run all tests
uv run pytest tests/ -v

# With coverage
uv run pytest tests/ --cov=intelgraph --cov-report=html

# Specific module
uv run pytest tests/test_pipeline.py -v
```

**Coverage Target**: 100%  
**Current**: 95%+  
**Total Tests**: 1,535+

---

## 📚 Documentation

- **[Architecture](./Architecture.md)** - System design & components
- **[Deployment](./DEPLOYMENT.md)** - Docker, K8s, production setup
- **[API Reference](./README.md#-api-examples)** - Endpoint documentation
- **[Contributing](./CONTRIBUTING.md)** - Development guide
- **[Security Policy](./SECURITY.md)** - Responsible disclosure

---

## 🛣️ Roadmap

### v1.1 (Q3 2026)
- [ ] ML-based threat scoring
- [ ] Advanced anomaly detection
- [ ] Threat actor attribution
- [ ] Custom connector framework

### v1.2 (Q4 2026)
- [ ] GraphQL API
- [ ] Kubernetes Helm charts
- [ ] SIEM integrations (Splunk, ELK)

### v2.0 (2027)
- [ ] Distributed architecture
- [ ] Collaborative analysis features
- [ ] Decentralized intelligence sharing

**Note**: Roadmap items marked as planned (not yet implemented).

---

## 🔒 Security

⚠️ **For security issues**, please refer to [SECURITY.md](./SECURITY.md) - **Do NOT open public issues**.

### Security Features
- JWT-based authentication
- Role-based access control (RBAC)
- Rate limiting & DDoS protection
- Input validation & sanitization
- Audit logging

---

## 📞 Contact & Support

- **Website**: [intelgraph.vercel.app](https://intelgraph.vercel.app)
- **GitHub**: [Berkayy123-h/intelgraph](https://github.com/Berkayy123-h/intelgraph)
- **Issues**: [GitHub Issues](https://github.com/Berkayy123-h/intelgraph/issues)
- **Questions**: [GitHub Discussions](https://github.com/Berkayy123-h/intelgraph/discussions)
- **Email**: berkayaltintas@intelgraph.io
- **Support**: contact@intelgraph.io

---

## 📜 License

MIT License - See [LICENSE](./LICENSE) for details.

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for:
- Code of conduct
- Development setup
- Testing requirements
- Pull request process

---

## 📚 Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | FastAPI, SQLAlchemy |
| Database | PostgreSQL, SQLite |
| Frontend | D3.js, Chart.js |
| Testing | pytest, 1450+ tests |
| Standards | STIX 2.1 |
| Deployment | Docker, Kubernetes |

---

**Questions?** Open an [issue](https://github.com/Berkayy123-h/intelgraph/issues) or start a [discussion](https://github.com/Berkayy123-h/intelgraph/discussions).

⭐ If this project helps you, please consider starring it!
