"""
L1 — INGESTION (§4)
Pull-based collectors on a schedule: RSS/Atom parsers, REST clients, exchange filing scrapers.
Each source is a configuration row. Raw payloads land in object storage before processing
for replayability when enrichment logic changes.
"""

import hashlib
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Dict, List, Optional
from urllib.request import Request, urlopen

from app.data.sources import SOURCES_CONFIG, SOURCE_BY_ID
from app.data.seed_corpus import SEED_ARTICLES


class RawPayloadStore:
    """In-memory + JSONL object store for replayable raw ingestion payloads."""

    def __init__(self):
        self._payloads: Dict[str, Dict] = {}

    def put(self, source_id: str, payload: Dict) -> Optional[str]:
        raw_str = json.dumps(payload, sort_keys=True)
        content_hash = hashlib.sha256(raw_str.encode("utf-8")).hexdigest()
        if content_hash in self._payloads:
            return None  # Already captured
        self._payloads[content_hash] = {
            "content_hash": content_hash,
            "source_id": source_id,
            "ingested_at": datetime.now(timezone.utc).isoformat(),
            "payload": payload,
        }
        return content_hash

    def list_all(self) -> List[Dict]:
        return list(self._payloads.values())

    def count(self) -> int:
        return len(self._payloads)


def fetch_rss_feed(url: str, timeout: int = 5) -> List[Dict]:
    """Pull and parse RSS/Atom XML items (returns headline + snippet only, §5)."""
    req = Request(url, headers={"User-Agent": "FeedzBot/1.0 (+https://feedz.in)"})
    with urlopen(req, timeout=timeout) as resp:
        xml_bytes = resp.read()
    root = ET.fromstring(xml_bytes)
    items = []
    for item in root.findall(".//item")[:15]:
        title = (item.findtext("title") or "").strip()
        desc = (item.findtext("description") or "").strip()[:320]
        link = (item.findtext("link") or "").strip()
        if title:
            items.append({"h": title, "sum": desc, "url": link})
    return items


def ingest_seed_corpus(store: RawPayloadStore) -> List[Dict]:
    """Ingest the seeded corpus into the raw payload store for deterministic replayability."""
    ingested = []
    for art in SEED_ARTICLES:
        sid = art.get("source_id", "nse_corp")
        h = store.put(sid, art)
        if h:
            ingested.append({"hash": h, "source_id": sid, "payload": art})
    return ingested


def run_scheduled_ingestion(store: RawPayloadStore, live_network: bool = False) -> Dict:
    """Run L1 ingestion across enabled sources. Falls back gracefully if offline."""
    results = {"sources_checked": 0, "new_payloads": 0, "errors": []}
    if not live_network:
        new_items = ingest_seed_corpus(store)
        results["sources_checked"] = len([s for s in SOURCES_CONFIG if s["enabled"]])
        results["new_payloads"] = len(new_items)
        return results

    for src in SOURCES_CONFIG:
        if not src["enabled"] or src["method"] != "RSS":
            continue
        results["sources_checked"] += 1
        try:
            items = fetch_rss_feed(src["url"])
            for it in items:
                payload = {
                    "h": it["h"],
                    "sum": it["sum"],
                    "url": it["url"],
                    "s": src["category"],
                    "src": src["name"],
                    "source_id": src["id"],
                    "t": 0.5,
                }
                if store.put(src["id"], payload):
                    results["new_payloads"] += 1
        except Exception as exc:
            results["errors"].append({"source_id": src["id"], "error": str(exc)})
    return results
