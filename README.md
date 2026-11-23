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
# Run backend tests
cd backend && python3 -m unittest discover -s tests -v

# Run backend API
cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload

# Or run full stack with Docker
docker compose up --build
```
