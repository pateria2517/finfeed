# Feedz — Hyper-Personal Financial Intelligence Feed

Full-stack implementation of the Feedz v0.2 Project Model (`L1`–`L6`).

## Architecture
- **Backend (`backend/`)**: Python 3.11 + FastAPI
  - **L1 Ingestion (`app/services/l1_ingestion.py`)**: 28 configured sources (`exchange`, `regulator`, `wire`, `business`, `broker`, `social`), RSS parser, and replayable `RawPayloadStore` (SHA-256 content-hashed).
  - **L2 Normalisation (`app/services/l2_normalisation.py`)**: 3-gram shingling (Jaccard) + TF-IDF cosine deduplication, language detection, spam filtering, and snippet-only copyright enforcement.
  - **L3 Enrichment (`app/services/l3_enrichment.py`)**: Precision-first entity linking against ~170+ Indian equities, mutual funds (with AMFI scheme codes), ETFs, and indices (`app/data/instruments.py`), event classification, and 3-axis sentiment scoring.
  - **Sentiment Engine (`app/services/sentiment_engine.py`)**: 36-hour exponential decay, §16 materiality-floored Breadth, 4-component Market Mood Index (`40% Polarity + 25% Breadth + 20% Momentum + 15% Agreement`), and full article-level drill-down.
  - **L4 Personalisation (`app/services/l4_personalisation.py`)**: Persona-weighted ranking formula, redundancy penalty, P2 MFD client-book aggregation, and `<30%` overlap verification.
  - **L5 Intelligence (`app/services/l5_intelligence.py`)**: SEBI-compliant guardrails (blocks buy/sell/hold advice and price targets) with optional Anthropic Claude API (`ANTHROPIC_API_KEY`) and grounded deterministic fallback.
  - **Portfolio CSV/CAS Parser (`app/services/portfolio_parser.py`)**: Resolves broker CSVs by ticker, ISIN, AMFI scheme code, or alias.
- **Frontend (`frontend/`)**: Next.js 14 + React + Tailwind CSS.
- **Database Schema (`backend/app/db/schema_postgres_pgvector.sql`)**: Production PostgreSQL + `pgvector` schema.

## Quick Start
```bash
# Backend development (SQLite fallback)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend development
cd frontend
npm install
npm run dev
```

The backend development fallback uses `sqlite:///./feedz.db`. Set `APP_ENV=production`
and `DATABASE_URL` to a PostgreSQL URL for production.

## Docker setup

Docker Compose runs PostgreSQL, FastAPI, Next.js, and Nginx as one stack. Nginx is
the only public application entrypoint. It sends `/api/*` to FastAPI and every
other path to Next.js, so browsers use the same origin without a separate API domain.

### Prerequisites

- Docker Engine or Docker Desktop with the Compose plugin
- Ports `3000` available on the host for the Nginx entrypoint
- Linux host access for production deployment
- OpenSSL for generating local secrets

Docker Desktop and Docker Engine must be running before Compose commands.

### Configure the environment

Create the local environment file from the template:

```bash
cp .env.example .env
```

Replace every placeholder in `.env`. Do not commit `.env`.

```bash
openssl rand -base64 48
```

Use separate generated values for `POSTGRES_PASSWORD` and `AUTH_SECRET`.
`AUTH_SECRET` must contain at least 32 characters. URL-encode special characters in
`POSTGRES_PASSWORD`, then set `DATABASE_URL` to match the PostgreSQL service:

```text
postgresql://feedz:<url-encoded-password>@postgres:5432/feedz
```

Keep these same-origin values for the initial localhost setup:

```text
CORS_ALLOWED_ORIGINS=http://localhost:3000
NEXT_PUBLIC_API_URL=
INTERNAL_API_URL=http://backend:8000
```

Do not set `NEXT_PUBLIC_API_URL` to a separate public API domain.

Required environment variables:

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | PostgreSQL SQLAlchemy URL in production |
| `AUTH_SECRET` | Signing secret, at least 32 characters |
| `APP_ENV` | Set to `production` outside development |
| `CORS_ALLOWED_ORIGINS` | Comma-separated browser origins |
| `NEXT_PUBLIC_API_URL` | Leave blank for same-origin `/api` routing |
| `INTERNAL_API_URL` | Internal API URL used by the Next.js server; defaults to `http://backend:8000` in Compose |
| `ANTHROPIC_API_KEY` | Optional AI provider credential |
| `ALLOW_LIVE_INGEST` | Set to `true` only for explicitly enabled live ingestion |

Register or log in through `/api/auth/register` and `/api/auth/login`. Protected
endpoints require `Authorization: Bearer <access_token>`. Portfolio and feed state
belongs only to the authenticated account.

### Start and verify

Build and start all services:

```bash
docker compose up --build -d
```

Check service status and logs:

```bash
docker compose ps
docker compose logs -f
```

The application is initially available at `http://localhost:3000`.
Verify the API health routes through the same-origin proxy:

```bash
curl --fail http://localhost:3000/api/health
curl --fail http://localhost:3000/api/ready
```

`/api/health` reports pipeline status. `/api/ready` requires the PostgreSQL
database and pipeline to be available.

### Architecture

- `postgres`: PostgreSQL 16 persistent data service
- `backend`: FastAPI API on the internal Compose network
- `frontend`: Next.js standalone server on the internal Compose network
- `nginx`: Public HTTP entrypoint at `127.0.0.1:3000`

PostgreSQL, FastAPI, and Next.js ports are not published to the host. The stack
uses a persistent named volume named `postgres-data`.

### Migrations and persistence

The backend container applies Alembic migrations with
`alembic upgrade head` before starting Uvicorn. PostgreSQL data remains in the
`postgres-data` volume across container stop, restart, and rebuild operations.
Removing the volume deletes all users and saved portfolios.

### Stop, restart, rebuild, and logs

```bash
docker compose stop
docker compose start
docker compose restart
docker compose up --build -d
docker compose down
docker compose logs --tail=200 backend
docker compose logs --tail=200 nginx
```

`docker compose down` stops and removes containers and networks but preserves the
`postgres-data` volume. Add `--volumes` only when intentional complete data deletion
is required.

### Backup and restore

Create a SQL backup:

```bash
docker compose exec -T postgres sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB"' > feedz-backup.sql
```

Restore a backup after the stack is running:

```bash
docker compose exec -T postgres sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"' < feedz-backup.sql
```

Store backups outside the repository and protect them as application data.

## Linux host deployment checklist

1. Copy `.env.example` to `.env` and replace every `replace-with-*` value.
2. Generate secrets locally with `openssl rand -base64 48` and use the output for
   `POSTGRES_PASSWORD` and `AUTH_SECRET`. Do not commit `.env`.
3. Set `DATABASE_URL` to
   `postgresql://<POSTGRES_USER>:<url-encoded-password>@postgres:5432/<POSTGRES_DB>`.
4. For local startup, keep `CORS_ALLOWED_ORIGINS=http://localhost:3000`. When
   production TLS is configured, replace it with the exact HTTPS frontend origin,
   with no trailing slash. Use a comma-separated list only when multiple origins
   are intentional.
5. Leave `NEXT_PUBLIC_API_URL` blank for one-origin deployments. Set it to the public
   API origin only when the API is hosted on a separate origin. Keep
   `INTERNAL_API_URL=http://backend:8000` for Compose routing.
6. Build and start with `docker compose up --build -d`.
7. Confirm migrations and health checks with `docker compose ps`. Open
   `http://localhost:3000`; Nginx routes `/api/*` to FastAPI and all other paths
   to Next.js.
8. For production, terminate TLS with the host HTTPS proxy or replace
   `deployment/nginx.conf` with a TLS-enabled server. Publish only HTTPS port 443,
   set `CORS_ALLOWED_ORIGINS=https://app.example.com`, keep
   `NEXT_PUBLIC_API_URL` blank, and preserve `/api/*` proxying to `backend:8000`.
9. Do not publish separate public API routing or set `NEXT_PUBLIC_API_URL` to a
   separate domain.
10. Keep PostgreSQL, FastAPI, and Next.js off public host ports. Nginx remains the
    only application entrypoint on port 3000 locally and should be replaced or
    fronted by HTTPS on the production host. Back up the `postgres-data` volume.
