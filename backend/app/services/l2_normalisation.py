"""
L2 — NORMALISATION & DE-DUPLICATION (§4)
De-duplication using 3-gram shingling (Jaccard) + TF-IDF cosine similarity,
canonical article schema, language detection, snippet-only enforcement (§5), and spam filtering.
"""

import math
import re
from collections import Counter
from typing import Dict, List, Set, Tuple


SPAM_PATTERNS = re.compile(
    r"\b(guaranteed returns|multibagger alert|join telegram|100% sure shot|dm for tips)\b",
    re.IGNORECASE,
)


def detect_language(text: str) -> str:
    """Lightweight ASCII/Devanagari heuristic."""
    if any("\u0900" <= ch <= "\u097F" for ch in text):
        return "hi"
    return "en"


def is_spam(headline: str, snippet: str) -> bool:
    return bool(SPAM_PATTERNS.search(f"{headline} {snippet}"))


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def shingles(text: str, k: int = 3) -> Set[str]:
    tokens = _tokenize(text)
    if len(tokens) < k:
        return set(tokens)
    return {" ".join(tokens[i : i + k]) for i in range(len(tokens) - k + 1)}


def jaccard_similarity(a: Set[str], b: Set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def cosine_similarity(text_a: str, text_b: str) -> float:
    ca = Counter(_tokenize(text_a))
    cb = Counter(_tokenize(text_b))
    common = set(ca.keys()) & set(cb.keys())
    if not common:
        return 0.0
    dot = sum(ca[w] * cb[w] for w in common)
    na = math.sqrt(sum(v * v for v in ca.values()))
    nb = math.sqrt(sum(v * v for v in cb.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def normalise_and_deduplicate(raw_articles: List[Dict], similarity_threshold: float = 0.55) -> Tuple[List[Dict], List[Dict]]:
    """
    Normalises raw articles to canonical schema, enforces snippet-only policy (§5),
    filters spam, and deduplicates wire copies using shingling + cosine similarity.
    Returns (canonical_articles, duplicates_log).
    """
    canonical: List[Dict] = []
    duplicates: List[Dict] = []

    for art in raw_articles:
        h = art["h"].strip()
        # §5 & §11: Never store or display full copyrighted body text — cap at snippet
        snippet = re.sub(r"<[^>]+>", "", art.get("sum", "")).strip()[:360]
        if is_spam(h, snippet):
            duplicates.append({"id": art.get("id"), "headline": h, "reason": "spam_filter"})
            continue

        lang = detect_language(f"{h} {snippet}")
        text_sig = f"{h} {snippet}"
        sig_shingles = shingles(text_sig, k=3)

        dup_of = None
        best_sim = 0.0
        for kept in canonical:
            j_sim = jaccard_similarity(sig_shingles, kept["_shingles"])
            c_sim = cosine_similarity(text_sig, f"{kept['h']} {kept['sum']}")
            combined = 0.5 * j_sim + 0.5 * c_sim
            if combined >= similarity_threshold or c_sim >= 0.78:
                dup_of = kept["id"]
                best_sim = combined
                break

        if dup_of is not None:
            duplicates.append({
                "id": art.get("id"),
                "headline": h,
                "source": art.get("src"),
                "duplicate_of": dup_of,
                "similarity": round(best_sim, 3),
                "reason": "shingle_cosine_dedup",
            })
            continue

        item = dict(art)
        item["h"] = h
        item["sum"] = snippet
        item["lang"] = lang
        item["_shingles"] = sig_shingles
        canonical.append(item)

    # Strip internal _shingles before returning
    for item in canonical:
        item.pop("_shingles", None)

    return canonical, duplicates
