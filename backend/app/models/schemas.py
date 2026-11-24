"""Pydantic schemas for Feedz L1–L6 API contracts (§7)."""

from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, Field


class PersonaVector(BaseModel):
    type: Literal["Beginner", "Active investor", "Professional", "Distributor / advisor"] = "Active investor"
    horizon: Literal["Trading", "1 to 3 years", "Long term"] = "Long term"
    style: Literal["Headlines only", "Deep analysis", "Data first"] = "Deep analysis"
    alerts: Literal["Real time", "Daily digest", "Weekly only"] = "Daily digest"


class HoldingInput(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=30)
    weight: float = Field(..., gt=0, le=100)
    quantity: Optional[float] = Field(default=None, ge=0, le=1e12)
    avg_price: Optional[float] = Field(default=None, ge=0, le=1e12)
    client_id: Optional[str] = None  # For P2 MFD client-book mode


class OnboardingRequest(BaseModel):
    user_id: str = "default_user"
    name: str = "You"
    mode: Literal["P1_RETAIL", "P2_MFD"] = "P1_RETAIL"
    persona: PersonaVector
    interests: Dict[str, float]  # topic -> weight (0.5 or 1.0)
    holdings: List[HoldingInput]


class AuthLoginRequest(BaseModel):
    identifier: str  # phone or email
    password: str = Field(..., min_length=8, max_length=128)


class AuthRegisterRequest(BaseModel):
    identifier: str = Field(..., min_length=3, max_length=320)
    password: str = Field(..., min_length=8, max_length=128)
    name: str = Field(..., min_length=1, max_length=100)


class SentimentScore(BaseModel):
    polarity: float = Field(..., ge=-1.0, le=1.0)
    confidence: float = Field(..., ge=0.0, le=1.0)
    materiality: float = Field(..., ge=0.0, le=1.0)


class ScoreBreakdown(BaseModel):
    interest: float
    exposure_pct: float
    impact: float
    novelty: float
    quality: float
    staleness: float
    redundancy: float = 0.0
    matched_topic: Optional[str] = None
    weights: Dict[str, float]


class TouchedHolding(BaseModel):
    symbol: str
    name: str
    weight: float
    relevance: float


class FeedItemResponse(BaseModel):
    id: int
    headline: str
    summary: str
    source_category: str
    source_name: str
    source_url: Optional[str] = None
    hours_ago: float
    event_type: str
    topics: List[str]
    entities: List[str]
    sectors: List[str]
    sentiment: SentimentScore
    rank_score: float
    score_breakdown: ScoreBreakdown
    touched_holdings: List[TouchedHolding]
    exposure_pct: float


class EntityContributor(BaseModel):
    article_id: int
    headline: str
    source_name: str
    source_category: str
    hours_ago: float
    polarity: float
    confidence: float
    materiality: float
    relevance: float
    weight: float


class EntityMoodDetail(BaseModel):
    symbol: str
    name: str
    sector: str
    score: float
    evidence: float
    contributors: List[EntityContributor]


class MarketMoodResponse(BaseModel):
    index: int
    polarity: float
    breadth: float
    momentum: float
    dispersion: float
    tracked_count: int
    history_7d: List[int]
    entity_scores: Dict[str, EntityMoodDetail]
    breadth_constituents: List[Dict]
    dispersion_constituents: List[Dict]


class PortfolioMoodResponse(BaseModel):
    score: float
    coverage_pct: float
    breakdown: List[Dict]


class WhyRequest(BaseModel):
    user_id: str = "default_user"
    article_id: int


class BriefRequest(BaseModel):
    user_id: str = "default_user"


class AskRequest(BaseModel):
    user_id: str = "default_user"
    question: str = Field(..., min_length=1, max_length=500)


class FeedbackRequest(BaseModel):
    user_id: str = "default_user"
    article_id: int
    vote: Literal["up", "down"]
