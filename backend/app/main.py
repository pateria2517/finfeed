"""
Feedz Backend API (L6 Delivery) — FastAPI Application
Runs the complete L1-L5 pipeline with replayable raw payload store,
P1 Retail & P2 MFD modes, Market Mood drill-down, and SEBI-guarded AI layer.
"""

from contextlib import asynccontextmanager
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from app.data.instruments import INSTRUMENTS, BY_SYMBOL, search_instruments
from app.data.sources import SOURCES_CONFIG, SOURCE_CATEGORIES
from app.data.seed_corpus import INTEREST_TAXONOMY, PRESETS, SENTIMENT_BENCHMARK
from app.models.schemas import (
    AskRequest, AuthLoginRequest, BriefRequest, FeedbackRequest,
    HoldingInput, OnboardingRequest, WhyRequest,
)
from app.services.l1_ingestion import RawPayloadStore, run_scheduled_ingestion
from app.services.l2_normalisation import normalise_and_deduplicate
from app.services.l3_enrichment import enrich_articles, evaluate_sentiment_benchmark
from app.services.l4_personalisation import aggregate_client_book, compute_feed_overlap, rank_feed
from app.services.l5_intelligence import ask_feed, daily_brief, why_this_matters
from app.services.portfolio_parser import parse_portfolio_csv
from app.services.sentiment_engine import entity_sentiment, market_mood, portfolio_mood


class FeedzState:
    def __init__(self):
        self.raw_store = RawPayloadStore()
        self.canonical_articles: List[Dict] = []
        self.dedup_log: List[Dict] = []
        self.enriched_articles: List[Dict] = []
        self.mood_cache: Dict = {}
        self.users: Dict[str, Dict] = {
            "investor_a": dict(PRESETS["A"]),
            "investor_b": dict(PRESETS["B"]),
            "mfd_advisor": dict(PRESETS["MFD"]),
        }
        self.feedback: List[Dict] = []

    def run_pipeline(self, live_network: bool = False) -> Dict:
        ingest_res = run_scheduled_ingestion(self.raw_store, live_network=live_network)
        raw_items = [r["payload"] for r in self.raw_store.list_all()]
        canonical, dups = normalise_and_deduplicate(raw_items)
        enriched = enrich_articles(canonical)
        self.canonical_articles = canonical
        self.dedup_log = dups
        self.enriched_articles = enriched
        self.mood_cache = market_mood(enriched)
        return {
            "ingestion": ingest_res,
            "raw_payloads": self.raw_store.count(),
            "canonical_articles": len(canonical),
            "duplicates_filtered": len(dups),
            "market_mood_index": self.mood_cache["index"],
        }


state = FeedzState()


@asynccontextmanager
async def lifespan(app: FastAPI):
    state.run_pipeline(live_network=False)
    yield


app = FastAPI(
    title="Feedz Financial Intelligence API",
    version="0.2.0",
    description="Hyper-personal financial intelligence feed with SEBI-guarded AI analysis layer.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "instruments_tracked": len(INSTRUMENTS),
        "sources_configured": len(SOURCES_CONFIG),
        "articles_enriched": len(state.enriched_articles),
        "duplicates_filtered": len(state.dedup_log),
    }


@app.post("/api/auth/login")
def auth_login(req: AuthLoginRequest):
    """Stubbed OTP / Magic Link auth for demo (§8 C1)."""
    return {
        "authenticated": True,
        "identifier": req.identifier,
        "channel": req.channel,
        "session_token": f"fz_demo_{abs(hash(req.identifier)) % 100000}",
    }


@app.get("/api/taxonomy")
def get_taxonomy():
    return {"taxonomy": INTEREST_TAXONOMY, "presets": list(PRESETS.keys())}


@app.get("/api/instruments/search")
def instruments_search(q: str = "", limit: int = 10):
    return {"query": q, "results": search_instruments(q, limit=limit)}


@app.get("/api/sources")
def get_sources():
    return {"categories": SOURCE_CATEGORIES, "sources": SOURCES_CONFIG}


@app.post("/api/ingest/run")
def trigger_ingest(live_network: bool = False):
    return state.run_pipeline(live_network=live_network)


@app.get("/api/ingest/audit")
def ingest_audit():
    return {
        "raw_payload_count": state.raw_store.count(),
        "canonical_count": len(state.canonical_articles),
        "dedup_log": state.dedup_log,
        "benchmark": evaluate_sentiment_benchmark(SENTIMENT_BENCHMARK),
    }


@app.post("/api/onboarding")
def save_onboarding(req: OnboardingRequest):
    profile = {
        "user_id": req.user_id,
        "name": req.name,
        "mode": req.mode,
        "persona": req.persona.model_dump(),
        "interests": req.interests,
        "holdings": [{"s": h.symbol, "w": h.weight, "qty": h.quantity, "avg_price": h.avg_price} for h in req.holdings],
    }
    state.users[req.user_id] = profile
    return {"saved": True, "profile": profile}


@app.post("/api/portfolio/{user_id}/holding")
def add_or_update_holding(user_id: str, holding: HoldingInput):
    if user_id not in state.users:
        raise HTTPException(status_code=404, detail="User not found")
    if holding.symbol not in BY_SYMBOL:
        raise HTTPException(status_code=400, detail=f"Unknown instrument: {holding.symbol}")
    user = state.users[user_id]
    holdings = [h for h in user.get("holdings", []) if h["s"] != holding.symbol]
    holdings.append({"s": holding.symbol, "w": holding.weight, "qty": holding.quantity, "avg_price": holding.avg_price})
    user["holdings"] = holdings
    return {"holdings": holdings}


@app.post("/api/portfolio/{user_id}/import-csv")
async def import_portfolio_csv(user_id: str, file: UploadFile = File(...)):
    if user_id not in state.users:
        raise HTTPException(status_code=404, detail="User not found")
    content = (await file.read()).decode("utf-8", errors="replace")
    resolved, unresolved = parse_portfolio_csv(content)
    if not resolved:
        raise HTTPException(status_code=400, detail={"message": "No holdings resolved", "unresolved": unresolved})
    state.users[user_id]["holdings"] = resolved
    return {"imported": len(resolved), "holdings": resolved, "unresolved": unresolved}


@app.get("/api/feed")
def get_feed(user_id: str = "investor_a"):
    profile = state.users.get(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    ranked = rank_feed(state.enriched_articles, profile)
    holdings = profile.get("holdings") or aggregate_client_book(profile.get("clients", []))
    p_mood = portfolio_mood(holdings, state.mood_cache["entity_scores"])
    return {
        "user_id": user_id,
        "name": profile["name"],
        "mode": profile.get("mode", "P1_RETAIL"),
        "count": len(ranked),
        "portfolio_mood": p_mood,
        "items": ranked,
    }


@app.get("/api/feed/compare")
def compare_feeds(user_a: str = "investor_a", user_b: str = "investor_b", top_n: int = 10):
    pa = state.users.get(user_a)
    pb = state.users.get(user_b)
    if not pa or not pb:
        raise HTTPException(status_code=404, detail="One or both users not found")
    fa = rank_feed(state.enriched_articles, pa)
    fb = rank_feed(state.enriched_articles, pb)
    return {
        "user_a": user_a,
        "user_b": user_b,
        "overlap": compute_feed_overlap(fa, fb, top_n=top_n),
        "top_a": [{"id": x["id"], "headline": x["headline"], "score": x["rank_score"]} for x in fa[:top_n]],
        "top_b": [{"id": x["id"], "headline": x["headline"], "score": x["rank_score"]} for x in fb[:top_n]],
    }


@app.get("/api/mood")
def get_market_mood():
    return state.mood_cache


@app.get("/api/mood/entity/{symbol}")
def get_entity_mood(symbol: str):
    res = entity_sentiment(symbol.upper(), state.enriched_articles)
    if not res:
        raise HTTPException(status_code=404, detail=f"No material sentiment evidence for {symbol}")
    return res


@app.post("/api/ai/why")
def ai_why(req: WhyRequest):
    profile = state.users.get(req.user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    ranked = rank_feed(state.enriched_articles, profile)
    match = next((x for x in ranked if x["id"] == req.article_id), None)
    if not match:
        raise HTTPException(status_code=404, detail="Article not found")
    return why_this_matters(match, profile)


@app.post("/api/ai/brief")
def ai_brief(req: BriefRequest):
    profile = state.users.get(req.user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    ranked = rank_feed(state.enriched_articles, profile)
    holdings = profile.get("holdings") or aggregate_client_book(profile.get("clients", []))
    p_mood = portfolio_mood(holdings, state.mood_cache["entity_scores"])
    return daily_brief(ranked, profile, state.mood_cache, p_mood)


@app.post("/api/ai/ask")
def ai_ask(req: AskRequest):
    profile = state.users.get(req.user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    ranked = rank_feed(state.enriched_articles, profile)
    return ask_feed(req.question, ranked, profile, state.mood_cache)


@app.post("/api/feedback")
def record_feedback(req: FeedbackRequest):
    state.feedback.append(req.model_dump())
    return {"recorded": True, "total_feedback": len(state.feedback)}
