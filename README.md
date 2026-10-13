# Temporal Context Time Decay Agent

A Python toolkit and standalone browser calculator for time-weighted context salience. It also retains the repository's original threshold-based, multi-worker audit workflow.

## What it does

**Temporal memory scoring:** an explicit exponential-decay heuristic in `temporal_decay.decay`:

```text
salience = min(1, base_salience × 2^(-age_hours / half_life_hours)
                  × (1 + access_boost × ln(1 + access_count)))
```

The score is bounded between 0 and 1. Inputs require a nonnegative age, positive half-life, initial salience in [0, 1], nonnegative integer access count, and nonnegative boost. `rank_memories` sorts records by score using timezone-aware timestamps. **This is an illustrative context-ranking heuristic, not a validated model of human memory.**

**Legacy threshold audit:** three deterministic workers flag primary metric >25, secondary metric >12 (or an explicit critical flag), and descriptors containing discordance markers. This independent workflow is retained for backward compatibility, and its thresholds are not derived from Ebbinghaus theory.

## Browser application

Open [`web/index.html`](web/index.html) in a modern browser to calculate and visualize salience, export calculation history to CSV, or evaluate legacy thresholds without starting a server. The page uses native HTML, CSS, and JavaScript; no Pyodide or Python runtime is necessary.

All browser calculations execute locally. No analytics, remote requests, browser storage, or sensitive-data processing are needed. The browser audit is **not** an HMAC-signed server audit. Do not enter personal identifiers.

## Install and run locally

Requires Python 3.9+; CI runs on Python 3.10–3.12.

```bash
python -m pip install -e .
python -m pip install pytest
python -m pytest -q
```

Calculate salience:

```bash
temporal-context-time-decay-engine score --age-hours 12 --half-life-hours 24 --base-salience 0.85 --access-count 3
python cli.py score --age-hours 24 --half-life-hours 24
```

Run the original audit workflow:

```bash
python cli.py audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
python cli.py batch -i sample.csv -o results.csv
python cli.py chat "What is the system status?"
python cli.py verify-audit
```

Batch CSV must supply `task_id`, `target_identifier`, and finite numeric fields. Boolean `is_critical_flag` accepts `true/false`, `1/0`, `yes/no`, or `y/n` (case-insensitive); other values are rejected.

Launch the FastAPI service:

```bash
export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
uvicorn agents.api:app --host 127.0.0.1 --port 8000
```

API documentation is served at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). Available endpoints include `POST /api/audit`, `POST /api/decay`, `POST /api/chat`, `GET /metrics` (Prometheus text), `GET /api/audit/logs`, and `GET /health`.

## Security, limitations, and privacy

- The server applies a **regex-based identifier guard** to selected inputs; it is not a guarantee of PHI detection or HIPAA compliance. Avoid sending sensitive data. The default mock chat engine does not invoke remote LLM providers.
- The audit trail is **in-memory**, chained with HMAC-SHA256, and verifies record signatures and links. It is not durable or independently anchored. Restarting the process loses this history, and the CLI `verify-audit` command checks only that process's current trail.
- Set a persistent, secret `AUDIT_SECRET_KEY` for deployments. The Compose file requires it from the environment. Any previously published Compose key should be treated as disclosed and rotated if it was used.
- API endpoints have no authentication, persistence layer, or deployment-grade rate limiting. Do not expose the API directly to an untrusted network.
- The original `temporal_decay` threshold coordinator and `agents` supervisor have different historical thresholds; they are preserved as separate compatibility interfaces.

Run in Docker using `docker build -t temporal-decay .` then `docker run -e AUDIT_SECRET_KEY=... -p 8000:8000 temporal-decay`. For Compose, export the key before `docker compose up --build`.

## Technology and license

Python, Pydantic, FastAPI, Uvicorn; browser interface in vanilla JavaScript. Tests use pytest and GitHub Actions. Desktop and mobile browsers with modern JavaScript and SVG support are suitable. Licensed under [MIT](LICENSE).
