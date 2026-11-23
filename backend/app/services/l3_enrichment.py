"""
L3 — ENRICHMENT (§4 & §6.1–6.2)
- Entity extraction & linking against the 200+ Instrument Master (ticker, ISIN, aliases).
- Event classification (earnings, regulatory, M&A, management_change, litigation_disputes, macro, etc.).
- 3-axis article sentiment scoring (polarity -1..1, confidence 0..1, materiality 0..1).
"""

import re
from typing import Dict, List, Tuple

from app.data.instruments import INSTRUMENTS, BY_SYMBOL


EVENT_KEYWORDS: Dict[str, List[str]] = {
    "earnings": ["quarter", "margin", "revenue", "guidance", "ebitda", "profit", "cost of funds", "arpu"],
    "regulatory": ["sebi", "rbi", "consultation paper", "circular", "norm", "regulatory", "tightening"],
    "M&A": ["acquisition", "merger", "acquire", "stake sale", "buyout", "clinker assets"],
    "management_change": ["appoints", "ceo", "cfo", "chief", "resigns", "elevation", "board"],
    "litigation_disputes": ["tribunal", "stay", "demand notice", "litigation", "dispute", "penalty", "court"],
    "macro": ["repo rate", "inflation", "gdp", "fed", "federal reserve", "rupee", "credit growth", "monsoon"],
    "flows": ["inflows", "outflows", "sip", "net sellers", "fii", "dii", "rebalancing"],
    "policy": ["government", "budget", "tax", "tariff", "pli", "capex", "disbursal"],
    "credit_event": ["bond spreads", "rating", "outlook", "downgrade", "upgrade", "default"],
    "commodity": ["crude", "steel prices", "brent", "oil", "restocking"],
    "sales": ["dispatches", "volumes", "footfalls", "demand", "festive"],
    "capex": ["capacity expansion", "commissioning", "plant", "greenfield"],
}

POSITIVE_LEXICON = {
    "eases", "cooled", "improvement", "hold above", "fresh high", "rise", "pick up",
    "firm", "grow", "raises", "supports", "narrow", "ahead", "record", "completes",
    "grants", "stay", "wins", "up", "comfort", "healthy", "buoyant", "positive",
}

NEGATIVE_LEXICON = {
    "soft", "moderates", "pressure", "sellers", "lags", "slips", "stretch", "cools",
    "tightening", "uncertainty", "prolonged", "fragile", "cautious", "compress",
    "drag", "pare", "slow", "erosion", "weakness", "down",
}


def extract_entities(text: str) -> List[str]:
    """
    Precision-first alias & ticker resolution (§6.1).
    "HDFC Bank", "HDFCBANK", and "the private lender" all resolve to HDFCBANK.
    """
    lower = text.lower()
    matched: List[str] = []
    for inst in INSTRUMENTS:
        sym = inst["s"]
        # Exact ticker word boundary
        if re.search(rf"\b{re.escape(sym.lower())}\b", lower):
            if sym not in matched:
                matched.append(sym)
            continue
        # Alias match
        for alias in inst.get("a", []):
            if len(alias) >= 3 and re.search(rf"\b{re.escape(alias.lower())}\b", lower):
                if sym not in matched:
                    matched.append(sym)
                break
    return matched


def classify_event(text: str) -> str:
    lower = text.lower()
    best_ev = "market"
    best_hits = 0
    for ev, kws in EVENT_KEYWORDS.items():
        hits = sum(1 for kw in kws if kw in lower)
        if hits > best_hits:
            best_hits = hits
            best_ev = ev
    return best_ev


def score_sentiment_3axis(text: str, source_cat: str) -> Tuple[float, float, float]:
    """
    Rule-based + rubric 3-axis sentiment scorer (used for new ingested items when no LLM key
    is present, or to benchmark against hand-labelled set).
    """
    lower = text.lower()
    pos = sum(1 for w in POSITIVE_LEXICON if w in lower)
    neg = sum(1 for w in NEGATIVE_LEXICON if w in lower)
    total = pos + neg
    if total == 0:
        polarity = 0.05
    else:
        polarity = max(-0.95, min(0.95, (pos - neg) / max(2, total)))

    src_conf = {"exchange": 0.90, "regulator": 0.90, "wire": 0.80, "business": 0.72, "broker": 0.65, "social": 0.35}
    confidence = src_conf.get(source_cat, 0.70)
    materiality = 0.75 if source_cat in ("exchange", "regulator") else 0.60 if source_cat in ("wire", "business") else 0.40
    return round(polarity, 2), round(confidence, 2), round(materiality, 2)


def enrich_articles(articles: List[Dict]) -> List[Dict]:
    """Run L3 enrichment on canonical articles, preserving pre-scored benchmark fields if present."""
    enriched = []
    for a in articles:
        item = dict(a)
        text = f"{item['h']} {item.get('sum', '')}"
        detected_entities = extract_entities(text)
        # Union with any explicit seed entity tags
        existing = list(item.get("e", []))
        for sym in detected_entities:
            if sym not in existing and sym in BY_SYMBOL:
                existing.append(sym)
        item["e"] = existing

        # Infer sectors from linked entities if empty
        sectors = list(item.get("sec", []))
        for sym in existing:
            sec = BY_SYMBOL[sym]["sec"]
            if sec not in sectors:
                sectors.append(sec)
        item["sec"] = sectors

        if not item.get("ev"):
            item["ev"] = classify_event(text)

        if "p" not in item or "c" not in item or "m" not in item:
            p, c, m = score_sentiment_3axis(text, item.get("s", "business"))
            item.setdefault("p", p)
            item.setdefault("c", c)
            item.setdefault("m", m)

        enriched.append(item)
    return enriched


def evaluate_sentiment_benchmark(benchmark: List[Dict]) -> Dict:
    """Evaluate scorer accuracy against the hand-labelled benchmark set (§6.2)."""
    correct = 0
    details = []
    for row in benchmark:
        p, c, m = score_sentiment_3axis(row["text"], "business")
        pred_sign = 1 if p >= 0 else -1
        ok = pred_sign == row["expected_sign"]
        if ok:
            correct += 1
        details.append({"text": row["text"][:60], "expected": row["expected_sign"], "predicted": p, "ok": ok})
    acc = correct / len(benchmark) if benchmark else 0.0
    return {"total": len(benchmark), "correct": correct, "accuracy": round(acc, 3), "details": details}
