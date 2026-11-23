"""
L5 — INTELLIGENCE (GENERATIVE) & SEBI COMPLIANCE GUARDRAILS (§6.5 & §11)
- Prompt-level and output-level compliance filters blocking buy/sell/hold advice,
  price targets, and return forecasts.
- Calls Anthropic Claude API when ANTHROPIC_API_KEY is configured; otherwise runs
  a grounded, deterministic analysis engine using only supplied structured data.
"""

import json
import os
import re
from typing import Dict, List, Optional
from urllib.request import Request, urlopen

from app.data.instruments import BY_SYMBOL
from app.data.sources import SOURCE_CATEGORIES

SEBI_SYSTEM_GUARD = """You are the analysis layer of Feedz, an information product for Indian retail investors.

Hard rules, no exceptions:
- Never recommend buying, selling, holding, adding or trimming anything.
- Never give price targets, return forecasts, or predictions of direction.
- Use only facts present in the supplied data. Do not introduce numbers, names or events that are not there.
- Where the user's own holdings are relevant, name them and their portfolio weight.
- Plain English. Indian market context. No filler, no hedging padding, no headline restating.
- If the supplied data does not support an answer, say so plainly.

You explain what happened and what it touches. You never tell anyone what to do."""

PROHIBITED_ADVICE_PATTERN = re.compile(
    r"\b(strong buy|strong sell|target price|price target|you should buy|you should sell|"
    r"recommend buying|recommend selling|guaranteed return|multibagger|accumulate now|exit immediately)\b",
    re.IGNORECASE,
)

DISCLOSURE_FOOTER = "Feedz is an information product. Nothing here is investment advice, a recommendation, or a forecast."


def enforce_sebi_guardrail(text: str) -> Dict:
    """Output-level compliance filter (§11). Flags or redacts prohibited advisory phrasing."""
    matches = PROHIBITED_ADVICE_PATTERN.findall(text)
    if matches:
        sanitized = PROHIBITED_ADVICE_PATTERN.sub("[redacted: non-advisory policy]", text)
        return {"text": sanitized, "compliant": False, "flagged_terms": matches}
    return {"text": text, "compliant": True, "flagged_terms": []}


def _call_claude_if_configured(prompt: str, max_tokens: int = 800) -> Optional[str]:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    payload = json.dumps({
        "model": "claude-sonnet-4-6",
        "max_tokens": max_tokens,
        "system": SEBI_SYSTEM_GUARD,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")
    req = Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return "\n".join(b["text"] for b in data.get("content", []) if b.get("type") == "text").strip()
    except Exception:
        return None


def why_this_matters(item: Dict, profile: Dict) -> Dict:
    """Two-sentence portfolio-specific insight (§8 C5)."""
    holdings = profile.get("holdings", [])
    total_w = sum(h["w"] for h in holdings) or 1.0
    touched = item.get("touched_holdings", [])

    if touched:
        top_t = touched[0]
        pct = round((top_t["weight"] / total_w) * 100)
        rel_desc = "named directly in this filing" if top_t["relevance"] == 1.0 else "in the same sector"
        prompt = (
            f"Write two concise sentences explaining why '{item['headline']}' ({item['summary']}) "
            f"matters to a holder of {top_t['name']} ({pct}% of portfolio, {rel_desc}). "
            f"Sentence 1: concrete mechanism. Sentence 2: what would make it matter more or less."
        )
        llm_out = _call_claude_if_configured(prompt, 250)
        if llm_out:
            checked = enforce_sebi_guardrail(llm_out)
            return {"insight": checked["text"], "grounded_in": [item["id"]], "model": "claude-sonnet-4-6", "compliant": checked["compliant"]}

        direction = "constructive" if item["sentiment"]["polarity"] > 0.12 else "cautious" if item["sentiment"]["polarity"] < -0.12 else "neutral"
        s1 = (
            f"This {item['event_type'].replace('_', ' ')} update from {item['source_name']} directly touches "
            f"{top_t['name']} ({pct}% of your portfolio, {rel_desc}), carrying a {direction} signal "
            f"(polarity {item['sentiment']['polarity']:+.2f}, materiality {item['sentiment']['materiality']:.2f})."
        )
        s2 = (
            f"It would matter more if follow-on disclosures or quarterly numbers confirm the trend across "
            f"{', '.join(t['name'] for t in touched[:2])}, and less if broader sector flows offset the move."
        )
        return {"insight": f"{s1} {s2}", "grounded_in": [item["id"]], "model": "feedz-grounded-v1", "compliant": True}

    topic = item["score_breakdown"].get("matched_topic") or "general markets"
    s1 = (
        f"While none of your current holdings are named, this {item['source_name']} update maps to your "
        f"followed interest in {topic} with materiality {item['sentiment']['materiality']:.2f}."
    )
    s2 = "It becomes portfolio-relevant only if second-order effects spill over into your held sectors."
    return {"insight": f"{s1} {s2}", "grounded_in": [item["id"]], "model": "feedz-grounded-v1", "compliant": True}


def daily_brief(top_feed: List[Dict], profile: Dict, mood: Dict, p_mood: Optional[Dict]) -> Dict:
    """Morning brief: 1-line summary, 3 themes, 2 watch items, divergence note (§8 C5)."""
    top8 = top_feed[:8]
    holdings = profile.get("holdings", [])
    total_w = sum(h["w"] for h in holdings) or 1.0
    top_holding = max(holdings, key=lambda h: h["w"]) if holdings else None
    top_h_name = BY_SYMBOL[top_holding["s"]]["n"] if top_holding and top_holding["s"] in BY_SYMBOL else "your portfolio"

    exposed = [a for a in top8 if a["exposure_pct"] > 0]
    lead = exposed[0] if exposed else (top8[0] if top8 else None)

    gap = (p_mood["score"] - mood["polarity"]) if p_mood else 0.0
    if p_mood and abs(gap) > 0.08:
        side = "more positive" if gap > 0 else "more negative"
        div_text = (
            f"Your portfolio mood ({p_mood['score']:+.2f}) reads {abs(gap * 100):.0f} points {side} "
            f"than the overall Market Mood ({mood['polarity']:+.2f}), driven by your concentration in {top_h_name}."
        )
    else:
        div_text = "Your portfolio mood is broadly aligned with the wider market today."

    themes = []
    used_ids = set()
    for item in top8:
        if len(themes) >= 3:
            break
        if item["id"] in used_ids:
            continue
        used_ids.add(item["id"])
        t_names = ", ".join(t["name"] for t in item["touched_holdings"][:2]) or (item["score_breakdown"].get("matched_topic") or "broad markets")
        themes.append({
            "title": f"{item['event_type'].replace('_', ' ').title()} in {t_names[:28]}",
            "detail": f"{item['headline']} ({item['source_name']}). {item['summary']}",
            "source_article_id": item["id"],
        })

    watch = [
        f"Source dispersion stands at {round(mood['dispersion'] * 100)}% across {mood['tracked_count']} tracked instruments — watch for consensus shifts.",
        f"Monitor follow-on filings for {lead['touched_holdings'][0]['name'] if lead and lead['touched_holdings'] else top_h_name} over the next 36-hour decay window.",
    ]

    line = (
        f"Today centers on {lead['touched_holdings'][0]['name'] if lead and lead['touched_holdings'] else 'macro & policy signals'} "
        f"with {len(exposed)} of your top 8 stories touching your holdings."
    )

    return {
        "line": line,
        "divergence": div_text,
        "themes": themes,
        "watch": watch,
        "disclosure": DISCLOSURE_FOOTER,
        "model": "feedz-grounded-v1",
    }


def ask_feed(question: str, feed: List[Dict], profile: Dict, mood: Dict) -> Dict:
    """Scoped Q&A over user's feed & portfolio with citations and refuse-and-flag path (§6.5)."""
    q_lower = question.lower()
    if PROHIBITED_ADVICE_PATTERN.search(q_lower) or any(w in q_lower for w in ["should i buy", "should i sell", "which stock to buy", "target price"]):
        return {
            "answer": "Feedz is an information product and cannot recommend buying, selling, or holding securities, nor provide price targets. I can, however, summarise the factual news and sentiment touching your holdings.",
            "citations": [],
            "refused_advisory": True,
            "disclosure": DISCLOSURE_FOOTER,
        }

    # Find relevant articles by keyword overlap + rank score
    q_tokens = set(re.findall(r"[a-z0-9]+", q_lower)) - {"the", "is", "my", "and", "or", "in", "on", "to", "what", "affecting", "today"}
    scored = []
    for item in feed[:20]:
        text = f"{item['headline']} {item['summary']} {' '.join(item['entities'])} {' '.join(item['topics'])}".lower()
        hits = sum(1 for tok in q_tokens if tok in text)
        scored.append((hits * 2 + item["exposure_pct"] * 3 + item["rank_score"] * 0.1, hits, item))
    scored.sort(key=lambda x: x[0], reverse=True)

    top_hits = [row[2] for row in scored[:3] if row[1] > 0] or feed[:3]

    # Check for dispersion / contradiction across retrieved items
    pols = [a["sentiment"]["polarity"] for a in top_hits]
    conflict_note = ""
    if pols and (max(pols) - min(pols) > 0.7):
        conflict_note = " Note: sources in your feed diverge sharply on direction here, so both views are cited rather than averaged."

    bullets = [
        f"[{a['source_name']}] {a['headline']} (polarity {a['sentiment']['polarity']:+.2f}, touches {round(a['exposure_pct']*100)}% of portfolio)."
        for a in top_hits
    ]
    answer = f"Based on your ranked feed (Market Mood {mood['index']}/100): " + " ".join(bullets) + conflict_note
    return {
        "answer": answer,
        "citations": [{"id": a["id"], "headline": a["headline"], "source": a["source_name"]} for a in top_hits],
        "refused_advisory": False,
        "disclosure": DISCLOSURE_FOOTER,
    }
