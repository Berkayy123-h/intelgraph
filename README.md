# 🔍 IntelGraph - Threat Intelligence Platform

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](#)

> **Enterprise-grade threat intelligence aggregation, enrichment, and analysis platform with real-time knowledge graph visualization and automated playbook execution.**

## 🎯 Overview

IntelGraph is a **comprehensive threat intelligence platform** designed for cybersecurity teams and SOC analysts. It aggregates data from multiple threat sources, performs advanced entity extraction and deduplication, maintains a temporal knowledge graph, and provides real-time intelligence dashboards with automated response capabilities.

### 🌐 Live Demo
👉 **[IntelGraph Dashboard](https://intelgraph.vercel.app)**

---

## ✨ Key Features

### 📊 Multi-Source Intelligence Pipeline
- **URLhaus** - Malicious URLs and phishing sites
- **Open Threat Exchange (OTX)** - Community threat intelligence  
- **CISA KEV** - Known exploited vulnerabilities
- **Shodan** - Internet-wide device scanning
- **VirusTotal** - File and URL threat analysis

### 🧠 Advanced Entity Processing
- **Custom NER Engine** - Named entity recognition optimized for threats
- **Entity Deduplication** - O(n) hash-index based matching
- **Relationship Mapping** - Interconnected threat entities
- **Confidence Calibration** - Evidence-based confidence scoring

### 📈 Temporal Knowledge Graph
- **Timeline Tracking** - Threat evolution over time
- **Relationship Chains** - Attack path visualization
- **Contradiction Detection** - Conflicting intelligence identification
- **Evidence Chains** - Provenance tracking

### ⚡ Intelligence Enrichment
- **Shodan Connectors** - Device enrichment from internet scans
- **VirusTotal Enrichment** - Detailed malware analysis
- **IP/Domain Reputation** - Historical threat data
- **Vulnerability Correlation** - CVE linkage

### 🤖 Automated Playbook System
- **Event-Driven Automation** - Trigger-based response rules
- **Custom Playbooks** - Define your own workflows
- **Alert Enrichment** - Automatic threat contextualization
- **Integration Ready** - Webhook and API support

### 📋 Compliance & Standards
- **STIX 2.1 Export** - Standardized threat intelligence format
- **TAXII 2.1 Protocol** - Industry-standard sharing
- **Data Provenance** - Complete source tracking
- **Retention Policies** - Configurable data lifecycle
- **Trust Models** - Source reliability scoring

### 🔐 Security & Performance
- **JWT Authentication** - Secure token-based access
- **Role-Based Authorization** - Granular permissions
- **Sliding-Window Rate Limiting** - 4-category traffic control
- **Full-Text Search (FTS5)** - 3-level fallback search
- **Multi-Backend Support** - SQLite + PostgreSQL

### 📱 Real-Time Dashboard
- **Server-Sent Events (SSE)** - Live data streaming
- **D3.js Force Graph** - Interactive threat visualization
- **Chart.js Analytics** - Real-time statistics
- **Advanced Search** - Semantic and fuzzy matching

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- `uv` package manager (recommended) or `pip`

### Installation

```bash
# Clone the repository
git clone https://github.com/Berkayy123-h/intelgraph.git
cd intelgraph

# Install dependencies
uv sync
# or with pip:
# pip install -e .
```

### Running the Platform

```bash
# Start the server
python -m intelgraph.api.server

# Access dashboard
# Open http://localhost:8000 in your browser
```

---

## 📁 Project Structure

```
intelgraph/
├── intelgraph/              # Main package
│   ├── api/                 # FastAPI server & REST endpoints
│   ├── core/                # Core threat intelligence engine
│   ├── enrichment/          # Enrichment connectors (Shodan, VT)
│   ├── graph/               # Knowledge graph implementation
│   ├── models/              # Data models (STIX compatible)
│   ├── pipeline/            # Multi-source data pipeline
│   ├── search/              # FTS5 search engine
│   ├── auth/                # JWT authentication & authorization
│   └── config/              # Configuration management
├── docs/                    # Documentation
├── tests/                   # 1450+ test suite
├── scripts/                 # Utility scripts
├── Architecture.md          # Detailed architecture document
├── ROADMAP.md               # Development roadmap
├── SECURITY.md              # Security policies
└── pyproject.toml           # Project metadata
```

---

## 📚 Documentation

- **[Architecture](./Architecture.md)** - System design and components
- **[ROADMAP](./ROADMAP.md)** - Future development plans
- **[CONTRIBUTING](./CONTRIBUTING.md)** - Contribution guidelines
- **[SECURITY](./SECURITY.md)** - Security policies and responsible disclosure
- **[DATA_POLICY](./DATA_POLICY.md)** - Data handling policies
- **[FINAL_STATUS](./FINAL_STATUS.md)** - Project completion report
- **[LIMITATIONS](./LIMITATIONS.md)** - Known limitations and constraints

---

## 🔌 API Endpoints

### Intelligence Queries
```bash
# Search threats
GET /api/v1/threats/search?q=malware

# Get specific threat
GET /api/v1/threats/{threat_id}

# Correlate indicators
POST /api/v1/threats/correlate
```

### Enrichment
```bash
# Enrich IP address
POST /api/v1/enrichment/ip
{"ip": "192.0.2.1"}

# Enrich domain
POST /api/v1/enrichment/domain
{"domain": "example.com"}
```

### Knowledge Graph
```bash
# Get relationship graph
GET /api/v1/graph/relationships?entity_id={id}

# Timeline view
GET /api/v1/graph/timeline?entity_id={id}
```

### STIX Export
```bash
# Export as STIX 2.1
GET /api/v1/export/stix?threat_id={id}
```

---

## 🔧 Configuration

Create a `.env` file or use environment variables:

```env
# Database
DATABASE_URL=sqlite:///intelgraph.db
# DATABASE_URL=postgresql://user:pass@localhost/intelgraph

# API Keys
SHODAN_API_KEY=your_key
VIRUSTOTAL_API_KEY=your_key
OTX_API_KEY=your_key

# Security
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256

# Server
ENVIRONMENT=production
DEBUG=false
```

---

## 🧪 Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=intelgraph

# Run specific test
uv run pytest tests/test_pipeline.py -v
```

The project includes **1450+ tests** covering:
- Pipeline integration
- Entity deduplication
- Graph operations
- API endpoints
- Authentication
- Rate limiting

---

## 📊 Features Checklist

- ✅ Multi-source threat data pipeline
- ✅ Custom NER + entity extraction
- ✅ Hash-index based deduplication (O(n))
- ✅ Temporal knowledge graph
- ✅ Evidence chain tracking
- ✅ Confidence calibration
- ✅ Contradiction detection
- ✅ Playbook automation system
- ✅ STIX 2.1 / TAXII 2.1 compliance
- ✅ FTS5 full-text search (3-level fallback)
- ✅ Real-time SSE dashboard
- ✅ JWT authentication + authorization
- ✅ Rate limiting (4 categories)
- ✅ SQLite + PostgreSQL support
- ✅ 1450+ enterprise test suite
- ✅ Production-ready metrics & observability

---

## 🛣️ Roadmap

Key upcoming features:
- [ ] ML-based threat scoring
- [ ] Advanced anomaly detection
- [ ] Threat actor attribution
- [ ] Custom intel source connectors
- [ ] GraphQL API
- [ ] Kubernetes deployment templates
- [ ] SIEM integration plugins

See [ROADMAP.md](./ROADMAP.md) for detailed plans.

---

## 🔒 Security

### Reporting Security Issues
⚠️ **Do NOT open public issues for security vulnerabilities**

Please refer to [SECURITY.md](./SECURITY.md) for responsible disclosure procedures.

### Security Features
- JWT-based authentication
- Role-based access control (RBAC)
- Rate limiting and DDoS protection
- Input validation and sanitization
- HTTPS/TLS support
- Audit logging

---

## 📜 License

This project is licensed under the **MIT License** - see [LICENSE](./LICENSE) file for details.

---

## 👥 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for:
- Code of conduct
- Development setup
- Coding standards
- Pull request process
- Testing requirements

---

## 📞 Support & Contact

- 📧 **Issues**: [GitHub Issues](https://github.com/Berkayy123-h/intelgraph/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Berkayy123-h/intelgraph/discussions)
- 🌐 **Website**: [intelgraph.vercel.app](https://intelgraph.vercel.app)

---

## 🙏 Acknowledgments

Built with:
- FastAPI - Modern Python web framework
- SQLAlchemy - Database ORM
- D3.js - Data visualization
- STIX/TAXII - Threat intelligence standards

---

**Made with ❤️ for the cybersecurity community**

⭐ If this project helps you, please consider giving it a star!
