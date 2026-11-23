"""
Sentiment Engine (§6.3 & §16)
- Entity-level sentiment with 36-hour exponential decay half-life.
- §16 Lesson 1: Breadth uses a materiality/evidence floor so sector propagation
  does not inflate breadth to 85% on a single macro story.
- Market Mood Index (0-100): 40% Polarity + 25% Breadth + 20% Momentum + 15% (1 - Dispersion).
- Full drill-down: every score traces back to its exact constituent articles.
- Exposure-weighted Portfolio Mood (and P2 MFD client-book mood).
"""

import math
from typing import Dict, List, Optional

from app.data.instruments import INSTRUMENTS, BY_SYMBOL
from app.data.sources import SOURCE_CATEGORIES
from app.data.seed_corpus import MOOD_HISTORY_7D

HALF_LIFE_H = 36.0


def decay(hours: float) -> float:
    return math.exp((-math.log(2.0) / HALF_LIFE_H) * max(0.0, hours))


def entity_relevance(article: Dict, symbol: str) -> float:
    """
    1.0 if article names the instrument directly,
    0.45 if it only covers the instrument's sector (precision over recall, §6.1).
    """
    if symbol in article.get("e", []):
        return 1.0
    inst = BY_SYMBOL.get(symbol)
    if inst and inst["sec"] in article.get("sec", []):
        return 0.45
    return 0.0


def entity_sentiment(symbol: str, articles: List[Dict], min_evidence: float = 0.05) -> Optional[Dict]:
    num = 0.0
    den = 0.0
    direct_evidence = 0.0
    contributors: List[Dict] = []

    for a in articles:
        rel = entity_relevance(a, symbol)
        if rel == 0.0:
            continue
        w_source = SOURCE_CATEGORIES.get(a["s"], {"w": 0.7})["w"]
        w = a["c"] * w_source * decay(a["t"]) * a["m"] * rel
        num += a["p"] * w
        den += w
        if rel == 1.0:
            direct_evidence += w
        contributors.append({
            "article_id": a["id"],
            "headline": a["h"],
            "source_name": a.get("src", a["s"]),
            "source_category": a["s"],
            "hours_ago": a["t"],
            "polarity": a["p"],
            "confidence": a["c"],
            "materiality": a["m"],
            "relevance": rel,
            "weight": round(w, 4),
        })

    if den < min_evidence:
        return None

    contributors.sort(key=lambda x: x["weight"], reverse=True)
    inst = BY_SYMBOL.get(symbol, {"n": symbol, "sec": "Unknown"})
    return {
        "symbol": symbol,
        "name": inst["n"],
        "sector": inst["sec"],
        "score": round(num / den, 4),
        "evidence": round(den, 4),
        "direct_evidence": round(direct_evidence, 4),
        "contributors": contributors,
    }


def market_mood(articles: List[Dict]) -> Dict:
    """
    Computes Market Mood Index (0-100) with 4 separately reported sub-signals (§6.3).
    Applies §16 fix: Breadth requires a materiality/evidence floor (>= 0.14) rather than
    just a polarity sign test, keeping breadth discriminating (~60-72% instead of 85%).
    """
    scores: Dict[str, Dict] = {}
    cap_num = 0.0
    cap_den = 0.0

    for inst in INSTRUMENTS:
        sym = inst["s"]
        if inst.get("type") == "INDEX":
            continue
        res = entity_sentiment(sym, articles)
        if not res:
            continue
        scores[sym] = res
        cap_w = max(10000.0, float(inst.get("cap", 50000) or 50000))
        cap_num += res["score"] * cap_w
        cap_den += cap_w

    if not scores:
        return {
            "index": 50,
            "polarity": 0.0,
            "breadth": 0.5,
            "momentum": 0.5,
            "dispersion": 0.0,
            "tracked_count": 0,
            "history_7d": MOOD_HISTORY_7D,
            "entity_scores": {},
            "breadth_constituents": [],
            "dispersion_constituents": [],
        }

    # Cap-weighted mean entity sentiment (§6.3)
    polarity = cap_num / cap_den if cap_den > 0 else 0.0

    # §16 fix: Materiality-floored breadth (evidence >= 0.14 & score > 0.12)
    material_entities = [r for r in scores.values() if r["evidence"] >= 0.14]
    breadth_pool = material_entities if material_entities else list(scores.values())
    positive_names = [r for r in breadth_pool if r["score"] > 0.12]
    breadth = len(positive_names) / len(breadth_pool)

    # Momentum vs 7-day trailing average
    hist_mean = sum(MOOD_HISTORY_7D) / len(MOOD_HISTORY_7D)
    raw_today = 50.0 + polarity * 50.0
    momentum = max(0.0, min(1.0, 0.5 + (raw_today - hist_mean) / 40.0))

    # Dispersion (cross-entity / cross-source disagreement)
    vals = [r["score"] for r in scores.values()]
    mean_s = sum(vals) / len(vals)
    variance = sum((v - mean_s) ** 2 for v in vals) / len(vals)
    dispersion = min(1.0, math.sqrt(variance) / 0.6)

    index_val = (
        40.0 * ((polarity + 1.0) / 2.0)
        + 25.0 * breadth
        + 20.0 * momentum
        + 15.0 * (1.0 - dispersion)
    )

    breadth_constituents = sorted(
        [{"symbol": r["symbol"], "name": r["name"], "score": r["score"], "evidence": r["evidence"], "positive": r["score"] > 0.12} for r in breadth_pool],
        key=lambda x: x["score"],
        reverse=True,
    )

    dispersion_constituents = sorted(
        [{"symbol": r["symbol"], "name": r["name"], "score": r["score"], "deviation": round(abs(r["score"] - mean_s), 3), "contributors_count": len(r["contributors"])} for r in scores.values()],
        key=lambda x: x["deviation"],
        reverse=True,
    )[:15]

    return {
        "index": round(index_val),
        "polarity": round(polarity, 4),
        "breadth": round(breadth, 4),
        "momentum": round(momentum, 4),
        "dispersion": round(dispersion, 4),
        "tracked_count": len(scores),
        "history_7d": MOOD_HISTORY_7D + [round(index_val)],
        "entity_scores": scores,
        "breadth_constituents": breadth_constituents,
        "dispersion_constituents": dispersion_constituents,
    }


def portfolio_mood(holdings: List[Dict], entity_scores: Dict[str, Dict]) -> Optional[Dict]:
    """Exposure-weighted mood of what the user actually owns (§8 C4)."""
    total_w = sum(h["w"] for h in holdings) or 1.0
    num = 0.0
    den = 0.0
    breakdown = []

    for h in holdings:
        r = entity_scores.get(h["s"])
        if not r:
            continue
        num += r["score"] * h["w"]
        den += h["w"]
        breakdown.append({
            "symbol": h["s"],
            "name": r["name"],
            "weight_pct": round((h["w"] / total_w) * 100, 1),
            "score": r["score"],
            "contributors_count": len(r["contributors"]),
        })

    if den <= 0:
        return None

    breakdown.sort(key=lambda x: abs(x["score"] * x["weight_pct"]), reverse=True)
    return {
        "score": round(num / den, 4),
        "coverage_pct": round((den / total_w) * 100, 1),
        "breakdown": breakdown,
    }
