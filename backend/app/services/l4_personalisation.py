"""
L4 — PERSONALISATION & RANKING ENGINE (§4, §6.4, §8, §16)
Score = α·InterestMatch + β·PortfolioExposure + γ·Impact + δ·Novelty
        + ε·SourceQuality - ζ·Redundancy - η·Staleness

Includes:
- Persona-driven weight shifting (§8 C1)
- P2 MFD client-book aggregation (§2)
- Redundancy penalty across repeated entity/topic clusters
- Overlap measurement proving <30% overlap between divergent personas (§8 C2 & §16)
"""

from typing import Dict, List, Set

from app.data.instruments import BY_SYMBOL
from app.data.sources import SOURCE_CATEGORIES
from app.services.sentiment_engine import decay, entity_relevance


def persona_weights(persona: Dict) -> Dict[str, float]:
    """
    Structured persona vector alters ranking weights (§8 C1 & §16 Lesson 2).
    Materiality/impact weight raised slightly so exposure does not completely drown macro events.
    """
    base = {
        "interest": 1.0,
        "exposure": 1.45,
        "impact": 1.35,
        "novelty": 0.5,
        "quality": 0.6,
        "redundancy": 0.35,
        "staleness": 0.5,
    }
    horizon = persona.get("horizon", "Long term")
    ptype = persona.get("type", "Active investor")
    if horizon == "Trading":
        return {**base, "novelty": 1.1, "impact": 1.25, "staleness": 1.1, "interest": 0.9}
    if horizon == "Long term":
        return {**base, "novelty": 0.3, "staleness": 0.3, "quality": 0.85}
    if ptype == "Beginner":
        return {**base, "quality": 1.1, "impact": 0.8, "exposure": 1.7}
    if ptype == "Distributor / advisor":
        return {**base, "quality": 0.9, "impact": 1.3, "exposure": 1.5}
    return base


def aggregate_client_book(clients: List[Dict]) -> List[Dict]:
    """
    P2 MFD / Advisor configuration (§2):
    Aggregates client-book holdings weighted by each client's AUM.
    """
    total_aum = sum(c.get("aum", 1.0) for c in clients) or 1.0
    agg: Dict[str, float] = {}
    for c in clients:
        c_share = c.get("aum", 1.0) / total_aum
        c_total = sum(h["w"] for h in c.get("holdings", [])) or 1.0
        for h in c.get("holdings", []):
            agg[h["s"]] = agg.get(h["s"], 0.0) + c_share * (h["w"] / c_total) * 100.0
    return [{"s": sym, "w": round(w, 2)} for sym, w in sorted(agg.items(), key=lambda x: -x[1])]


def rank_feed(articles: List[Dict], profile: Dict) -> List[Dict]:
    weights = persona_weights(profile.get("persona", {}))
    holdings = profile.get("holdings", [])
    if not holdings and profile.get("clients"):
        holdings = aggregate_client_book(profile["clients"])

    total_w = sum(h["w"] for h in holdings) or 1.0
    interests = profile.get("interests", {})

    preliminary = []
    for a in articles:
        # Interest match — best-matching selected topic
        interest = 0.0
        matched_topic = None
        for t in a.get("top", []):
            v = float(interests.get(t, 0.0))
            if v > interest:
                interest = v
                matched_topic = t

        # Portfolio exposure = Σ(holding_weight × entity_relevance)
        exposure_pct = 0.0
        touched = []
        for h in holdings:
            rel = entity_relevance(a, h["s"])
            if rel > 0:
                exposure_pct += (h["w"] / total_w) * rel
                inst = BY_SYMBOL.get(h["s"], {"n": h["s"]})
                touched.append({
                    "symbol": h["s"],
                    "name": inst["n"],
                    "weight": h["w"],
                    "relevance": rel,
                })
        touched.sort(key=lambda x: x["weight"] * x["relevance"], reverse=True)

        impact = float(a.get("m", 0.5))
        novelty = decay(float(a.get("t", 12)))
        quality = SOURCE_CATEGORIES.get(a["s"], {"w": 0.7})["w"]
        staleness = min(1.0, float(a.get("t", 12)) / 48.0)

        base_score = (
            weights["interest"] * interest
            + weights["exposure"] * min(1.0, exposure_pct * 1.4)
            + weights["impact"] * impact
            + weights["novelty"] * novelty
            + weights["quality"] * quality
            - weights["staleness"] * staleness
        )

        preliminary.append({
            "article": a,
            "base_score": base_score,
            "interest": interest,
            "matched_topic": matched_topic,
            "exposure_pct": exposure_pct,
            "touched": touched,
            "impact": impact,
            "novelty": novelty,
            "quality": quality,
            "staleness": staleness,
        })

    # Sort by base_score, then apply Redundancy penalty (-ζ·Redundancy) for repeated primary entity/event
    preliminary.sort(key=lambda x: x["base_score"], reverse=True)
    seen_clusters: Set[str] = set()
    ranked: List[Dict] = []

    for row in preliminary:
        a = row["article"]
        cluster_key = f"{a.get('ev', 'market')}:{','.join(sorted(a.get('e', [])[:2]))}"
        redundancy = 1.0 if (a.get("e") and cluster_key in seen_clusters) else 0.0
        if a.get("e"):
            seen_clusters.add(cluster_key)

        final_score = row["base_score"] - weights["redundancy"] * redundancy
        ranked.append({
            "id": a["id"],
            "headline": a["h"],
            "summary": a["sum"],
            "source_category": a["s"],
            "source_name": a.get("src", a["s"]),
            "source_url": a.get("url"),
            "hours_ago": a["t"],
            "event_type": a.get("ev", "market"),
            "topics": a.get("top", []),
            "entities": a.get("e", []),
            "sectors": a.get("sec", []),
            "sentiment": {"polarity": a["p"], "confidence": a["c"], "materiality": a["m"]},
            "rank_score": round(final_score, 4),
            "score_breakdown": {
                "interest": round(row["interest"], 3),
                "exposure_pct": round(row["exposure_pct"], 4),
                "impact": round(row["impact"], 3),
                "novelty": round(row["novelty"], 3),
                "quality": round(row["quality"], 3),
                "staleness": round(row["staleness"], 3),
                "redundancy": round(redundancy, 3),
                "matched_topic": row["matched_topic"],
                "weights": weights,
            },
            "touched_holdings": row["touched"],
            "exposure_pct": round(row["exposure_pct"], 4),
        })

    ranked.sort(key=lambda x: x["rank_score"], reverse=True)
    return ranked


def compute_feed_overlap(feed_a: List[Dict], feed_b: List[Dict], top_n: int = 10) -> Dict:
    """Proves §8 C2 acceptance criterion: two distinct personas share < 30% of top N stories."""
    ids_a = {item["id"] for item in feed_a[:top_n]}
    ids_b = {item["id"] for item in feed_b[:top_n]}
    shared = ids_a & ids_b
    overlap_pct = (len(shared) / top_n) * 100.0 if top_n > 0 else 0.0
    return {
        "top_n": top_n,
        "shared_ids": sorted(shared),
        "shared_count": len(shared),
        "overlap_pct": round(overlap_pct, 1),
        "passes_30pct_target": overlap_pct <= 30.0,
    }
