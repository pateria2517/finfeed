"""
Feedz FastAPI API.
"""

import os
from contextlib import asynccontextmanager
from typing import Dict, List

from fastapi import Depends, FastAPI, HTTPException, UploadFile, File, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.auth import create_session, get_current_user, hash_password, verify_password
from app.data.instruments import INSTRUMENTS, BY_SYMBOL, search_instruments
from app.data.sources import SOURCES_CONFIG, SOURCE_CATEGORIES
from app.data.seed_corpus import INTEREST_TAXONOMY
from app.db.store import FeedzStore
from app.models.schemas import (
    AskRequest,
    AuthLoginRequest,
    AuthRegisterRequest,
    BriefRequest,
    FeedbackRequest,
    HoldingInput,
    OnboardingRequest,
    WhyRequest,
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
store = FeedzStore()


@asynccontextmanager
async def lifespan(app: FastAPI):
    state.run_pipeline(live_network=False)
    yield


app = FastAPI(
    title="Feedz Financial Intelligence API",
    version="0.2.0",
    lifespan=lifespan,
)

cors_origins_setting = os.getenv("CORS_ALLOWED_ORIGINS")
is_production = os.getenv("APP_ENV", "development").lower() == "production"
allowed_origins = [
    origin.strip()
    for origin in (cors_origins_setting or ("http://localhost:3000" if not is_production else "")).split(",")
    if origin.strip()
]
if is_production:
    if not cors_origins_setting or not allowed_origins or "*" in allowed_origins:
        raise RuntimeError("Production requires CORS_ALLOWED_ORIGINS and does not allow wildcard origins")
    invalid_origins = [
        origin
        for origin in allowed_origins
        if not origin.startswith("https://")
        and not origin.startswith("http://localhost:")
        and not origin.startswith("http://127.0.0.1:")
    ]
    if invalid_origins:
        raise RuntimeError("Production CORS origins must use HTTPS or an explicit loopback origin")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > 5_000_000:
        return JSONResponse(status_code=413, content={"error": "payload_too_large"})
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "validation_error", "detail": exc.errors()},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    if os.getenv("APP_ENV", "development").lower() != "production":
        raise exc
    return JSONResponse(
        status_code=500,
        content={"error": "internal_server_error", "detail": "An unexpected error occurred"},
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "instruments_tracked": len(INSTRUMENTS),
        "sources_configured": len(SOURCES_CONFIG),
        "articles_enriched": len(state.enriched_articles),
    }


@app.get("/ready")
def readiness():
    try:
        store.healthcheck()
    except Exception:
        raise HTTPException(status_code=503, detail={"error": "not_ready", "detail": "Database unavailable"})
    if not state.enriched_articles:
        raise HTTPException(status_code=503, detail={"error": "not_ready", "detail": "Pipeline not initialized"})
    return {"status": "ready"}


@app.post("/api/auth/register", status_code=201)
def auth_register(req: AuthRegisterRequest):
    try:
        user = store.create_user(req.identifier, hash_password(req.password), req.name)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    return {"user": user, "access_token": create_session(user["user_id"]), "token_type": "bearer"}


@app.post("/api/auth/login")
def auth_login(req: AuthLoginRequest):
    user = store.get_by_identifier(req.identifier)
    if not user or not verify_password(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid identifier or password")
    user.pop("password_hash", None)
    return {"user": user, "access_token": create_session(user["user_id"]), "token_type": "bearer"}


@app.get("/api/me")
def get_me(current_user: Dict = Depends(get_current_user)):
    user = store.get_user(current_user["id"])
    if not user:
        raise HTTPException(status_code=401, detail="User no longer exists")
    return user


@app.get("/api/taxonomy")
def get_taxonomy():
    return {"taxonomy": INTEREST_TAXONOMY}


@app.get("/api/instruments/search")
def instruments_search(q: str = "", limit: int = 10):
    if len(q) > 100:
        raise HTTPException(status_code=422, detail="Query too long")
    return {"query": q, "results": search_instruments(q, max(1, min(limit, 50)))}


@app.get("/api/sources")
def get_sources():
    return {"categories": SOURCE_CATEGORIES, "sources": SOURCES_CONFIG}


@app.post("/api/ingest/run")
def trigger_ingest(live_network: bool = False, current_user: Dict = Depends(get_current_user)):
    if store.get_user(current_user["id"]).get("role") != "admin":
        raise HTTPException(status_code=403, detail="Administrator role required")
    if live_network and os.getenv("ALLOW_LIVE_INGEST", "false").lower() != "true":
        raise HTTPException(status_code=403, detail="Live network ingestion is disabled")
    return state.run_pipeline(live_network=live_network)


@app.get("/api/ingest/audit")
def ingest_audit():
    return {
        "raw_payload_count": state.raw_store.count(),
        "canonical_count": len(state.canonical_articles),
        "dedup_log": state.dedup_log,
    }


@app.post("/api/onboarding")
def save_onboarding(req: OnboardingRequest, current_user: Dict = Depends(get_current_user)):
    user = store.get_user(current_user["id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    profile = {
        "name": req.name,
        "mode": req.mode,
        "persona": req.persona.model_dump(),
        "interests": req.interests,
        "holdings": [{"s": h.symbol, "w": h.weight, "qty": h.quantity, "avg_price": h.avg_price} for h in req.holdings],
    }
    if len(profile["interests"]) > 50:
        raise HTTPException(status_code=422, detail="Too many interests")
    return {"saved": True, "profile": store.save_profile(current_user["id"], profile)}


@app.post("/api/portfolio/holding")
def add_or_update_holding(holding: HoldingInput, current_user: Dict = Depends(get_current_user)):
    if holding.symbol not in BY_SYMBOL:
        raise HTTPException(status_code=400, detail=f"Unknown instrument: {holding.symbol}")
    user = store.get_user(current_user["id"])
    holdings = [h for h in user["holdings"] if h["s"] != holding.symbol]
    holdings.append({"s": holding.symbol, "w": holding.weight, "qty": holding.quantity, "avg_price": holding.avg_price})
    return {"holdings": store.save_holdings(current_user["id"], holdings)["holdings"]}


@app.post("/api/portfolio/import-csv")
async def import_portfolio_csv(file: UploadFile = File(...), current_user: Dict = Depends(get_current_user)):
    content_bytes = await file.read(2_000_000)
    if len(content_bytes) >= 2_000_000:
        raise HTTPException(status_code=413, detail="CSV file too large")
    content = content_bytes.decode("utf-8", errors="replace")
    resolved, unresolved = parse_portfolio_csv(content)
    if not resolved:
        raise HTTPException(status_code=400, detail={"message": "No holdings resolved", "unresolved": unresolved})
    store.save_holdings(current_user["id"], resolved)
    return {"imported": len(resolved), "holdings": resolved, "unresolved": unresolved}


@app.get("/api/feed")
def get_feed(current_user: Dict = Depends(get_current_user)):
    profile = store.get_user(current_user["id"])
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    ranked = rank_feed(state.enriched_articles, profile)
    holdings = profile["holdings"] or aggregate_client_book([])
    p_mood = portfolio_mood(holdings, state.mood_cache["entity_scores"])
    return {
        "user_id": profile["user_id"],
        "name": profile["name"],
        "mode": profile["mode"],
        "count": len(ranked),
        "portfolio_mood": p_mood,
        "items": ranked,
    }


@app.get("/api/feed/compare")
def compare_feeds(top_n: int = 10, current_user: Dict = Depends(get_current_user)):
    if not 1 <= top_n <= 50:
        raise HTTPException(status_code=422, detail="top_n must be between 1 and 50")
    raise HTTPException(status_code=403, detail="Cross-user feed comparison is not available")


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
def ai_why(req: WhyRequest, current_user: Dict = Depends(get_current_user)):
    profile = store.get_user(current_user["id"])
    ranked = rank_feed(state.enriched_articles, profile)
    match = next((x for x in ranked if x["id"] == req.article_id), None)
    if not match:
        raise HTTPException(status_code=404, detail="Article not found")
    return why_this_matters(match, profile)


@app.post("/api/ai/brief")
def ai_brief(req: BriefRequest, current_user: Dict = Depends(get_current_user)):
    profile = store.get_user(current_user["id"])
    ranked = rank_feed(state.enriched_articles, profile)
    holdings = profile["holdings"] or aggregate_client_book([])
    p_mood = portfolio_mood(holdings, state.mood_cache["entity_scores"])
    return daily_brief(ranked, profile, state.mood_cache, p_mood)


@app.post("/api/ai/ask")
def ai_ask(req: AskRequest, current_user: Dict = Depends(get_current_user)):
    if len(req.question.strip()) > 500:
        raise HTTPException(status_code=422, detail="Question too long")
    profile = store.get_user(current_user["id"])
    ranked = rank_feed(state.enriched_articles, profile)
    return ask_feed(req.question, ranked, profile, state.mood_cache)


@app.post("/api/feedback")
def record_feedback(req: FeedbackRequest, current_user: Dict = Depends(get_current_user)):
    total = store.append_feedback(current_user["id"], {
        "article_id": req.article_id,
        "vote": req.vote,
    })
    return {"recorded": True, "total_feedback": total}
