# Temporal Context Time Decay Agent

> **Domain:** Autonomous Agent Systems & Context State Architecture  
> **Reference Guidelines & Standards:** `Distributed Systems RFC & State Machine Verification`

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

**Temporal Context Time Decay Agent** is an advanced analytical and computational platform implementing Ebbinghaus exponential forgetting curves for time-weighted memory salience.

---

## ⚙️ Key Capabilities & Algorithmic Modules

- **Deterministic Calculation Engine**: Strict compliance with standard reference formulations and thresholds.
- **Risk & Urgency Classification**: Multi-tier categorization with automated clinical/operational action recommendations.
- **Validation & Guardrails**: Rigorous input bounds checking and anomaly detection.

---

## 💻 CLI Quickstart & Usage

### 1. Run a Single Audit
```bash
python cli.py audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### 2. Chat with the Supervisor
```bash
python cli.py chat "What is the system status?"
```

### 3. Batch Process CSV Records
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 4. Verify Audit Trail Integrity
```bash
python cli.py verify-audit
```

### 5. Launch REST API Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### Input Data Schema

| Field | Type | Description | Requirement |
|:------|:-----|:------------|:------------|
| `task_id` | string (max 128 chars) | Unique task identifier | Required |
| `target_identifier` | string (max 128 chars) | Target entity key | Required |
| `primary_metric` | float (finite) | Primary measurement value | Required |
| `secondary_metric` | float (finite) | Secondary metric value | Optional (default 0.0) |
| `is_critical_flag` | boolean | Emergency escalation flag | Optional (default false) |
| `status_descriptor` | string (max 64 chars) | Status code descriptor | Optional (default "NOMINAL") |

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active regex inspection blocking SSNs, MRNs, phone numbers, emails, and patient identifiers.
* **Tamper-evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition.
* **Air-Gapped LLM Reasoning Adapter:** Agnostic integration for local Ollama instances (`llama3`, `mistral`), Claude 3.5 Sonnet, GPT-4o, and deterministic test mocks.
* **Active Learning Bayesian Calibration:** Dynamic tracker updating worker reliability weights and monitoring Brier calibration drift.
* **FastAPI & Prometheus Telemetry:** Exposes OpenAPI 3.1 REST endpoints and operational Prometheus metrics (`/metrics`).

### Security Configuration

Set a persistent audit secret key via environment variable:

```bash
# Linux/macOS
export AUDIT_SECRET_KEY="your-256-bit-secret-key"

# Windows
set AUDIT_SECRET_KEY=your-256-bit-secret-key
```

Without this variable, the system generates an ephemeral key at startup (suitable for development/testing but not for production).

---

## 🧪 Testing & Verification

Install dev dependencies and run the automated test suite:

```bash
pip install pytest
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py 1000
```

---

## 🐳 Container Deployment

```bash
docker build -t temporal-context-time-decay-agent .
docker run -p 8000:8000 temporal-context-time-decay-agent
```
