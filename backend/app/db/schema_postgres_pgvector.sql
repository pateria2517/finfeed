-- Production PostgreSQL + pgvector Schema for Feedz (§7 & §10)
-- Designed so P2 (MFD / Advisor client-book aggregation) is a configuration layer on top of P1.

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE users (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    email           TEXT UNIQUE,
    phone           TEXT UNIQUE,
    mode            TEXT NOT NULL DEFAULT 'P1_RETAIL', -- P1_RETAIL | P2_MFD
    persona_type    TEXT NOT NULL,
    persona_horizon TEXT NOT NULL,
    persona_style   TEXT NOT NULL,
    persona_alerts  TEXT NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE user_interests (
    user_id         TEXT REFERENCES users(id) ON DELETE CASCADE,
    topic           TEXT NOT NULL,
    weight          REAL NOT NULL DEFAULT 1.0,
    PRIMARY KEY (user_id, topic)
);

CREATE TABLE instruments (
    symbol          TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    isin            TEXT UNIQUE,
    scheme_code     TEXT,
    amc             TEXT,
    sector          TEXT NOT NULL,
    instrument_type TEXT NOT NULL, -- EQUITY | MUTUAL_FUND | ETF | INDEX
    market_cap_cr   REAL DEFAULT 0,
    indices         TEXT[] DEFAULT '{}',
    aliases         TEXT[] DEFAULT '{}'
);

CREATE TABLE clients (
    id              TEXT PRIMARY KEY,
    advisor_user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    client_name     TEXT NOT NULL,
    aum_inr         REAL DEFAULT 0
);

CREATE TABLE portfolios (
    id              TEXT PRIMARY KEY,
    user_id         TEXT REFERENCES users(id) ON DELETE CASCADE,
    client_id       TEXT REFERENCES clients(id) ON DELETE SET NULL,
    name            TEXT NOT NULL DEFAULT 'Primary Portfolio',
    source          TEXT NOT NULL DEFAULT 'manual', -- manual | csv | cas_stub
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE holdings (
    portfolio_id    TEXT REFERENCES portfolios(id) ON DELETE CASCADE,
    symbol          TEXT REFERENCES instruments(symbol),
    weight          REAL NOT NULL,
    quantity        REAL,
    avg_price       REAL,
    PRIMARY KEY (portfolio_id, symbol)
);

CREATE TABLE sources (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    category        TEXT NOT NULL,
    method          TEXT NOT NULL,
    url             TEXT NOT NULL,
    credibility_w   REAL NOT NULL,
    poll_min        INTEGER NOT NULL,
    enabled         BOOLEAN DEFAULT TRUE
);

CREATE TABLE raw_payloads (
    id              BIGSERIAL PRIMARY KEY,
    source_id       TEXT REFERENCES sources(id),
    content_hash    TEXT UNIQUE NOT NULL,
    raw_json        JSONB NOT NULL,
    ingested_at     TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE articles (
    id              BIGSERIAL PRIMARY KEY,
    raw_payload_id  BIGINT REFERENCES raw_payloads(id),
    source_id       TEXT REFERENCES sources(id),
    headline        TEXT NOT NULL,
    snippet         TEXT NOT NULL, -- Never store/display full copyrighted article body (§5)
    source_url      TEXT,
    published_at    TIMESTAMPTZ NOT NULL,
    language        TEXT DEFAULT 'en',
    event_type      TEXT NOT NULL,
    topics          TEXT[] DEFAULT '{}',
    sectors         TEXT[] DEFAULT '{}',
    polarity        REAL NOT NULL,
    confidence      REAL NOT NULL,
    materiality     REAL NOT NULL,
    embedding       vector(384),
    is_duplicate_of BIGINT REFERENCES articles(id)
);

CREATE TABLE article_entities (
    article_id      BIGINT REFERENCES articles(id) ON DELETE CASCADE,
    symbol          TEXT REFERENCES instruments(symbol),
    relevance       REAL NOT NULL, -- 1.0 direct, 0.45 sector
    PRIMARY KEY (article_id, symbol)
);

CREATE TABLE feed_items (
    user_id         TEXT REFERENCES users(id) ON DELETE CASCADE,
    article_id      BIGINT REFERENCES articles(id) ON DELETE CASCADE,
    rank_score      REAL NOT NULL,
    score_breakdown JSONB NOT NULL, -- Explainability & tuning (§7)
    computed_at     TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, article_id)
);

CREATE TABLE insights (
    id              BIGSERIAL PRIMARY KEY,
    user_id         TEXT REFERENCES users(id) ON DELETE CASCADE,
    article_id      BIGINT REFERENCES articles(id) ON DELETE CASCADE,
    insight_type    TEXT NOT NULL, -- why_matters | daily_brief | ask_qa
    model_version   TEXT NOT NULL,
    content_json    JSONB NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
