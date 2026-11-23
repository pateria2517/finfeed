"""
Portfolio CSV / Broker / CAS Parser (§8 C3)
Parses broker CSV exports (Zerodha, Groww, Kuvera, or generic symbol/isin/weight/quantity/avg_price)
and resolves each row to canonical instruments via the Instrument Master.
"""

import csv
import io
from typing import Dict, List, Tuple

from app.data.instruments import BY_SYMBOL, BY_ISIN, BY_SCHEME, search_instruments


def parse_portfolio_csv(csv_text: str) -> Tuple[List[Dict], List[Dict]]:
    """
    Returns (resolved_holdings, unresolved_rows).
    Supports columns: symbol/ticker/tradingsymbol, isin, scheme_code, name/instrument, weight, quantity, avg_price.
    """
    reader = csv.DictReader(io.StringIO(csv_text.strip()))
    if not reader.fieldnames:
        return [], [{"row": 0, "error": "Empty or invalid CSV header"}]

    resolved: List[Dict] = []
    unresolved: List[Dict] = []

    raw_rows = list(reader)
    computed_values: List[Tuple[Dict, float]] = []

    for idx, row in enumerate(raw_rows, start=1):
        norm = {k.strip().lower(): (v or "").strip() for k, v in row.items() if k}
        sym = norm.get("symbol") or norm.get("tradingsymbol") or norm.get("ticker") or ""
        isin = norm.get("isin") or ""
        scheme = norm.get("scheme_code") or norm.get("amfi_code") or ""
        name = norm.get("name") or norm.get("instrument") or norm.get("scheme_name") or ""

        inst = None
        if sym.upper() in BY_SYMBOL:
            inst = BY_SYMBOL[sym.upper()]
        elif isin.upper() in BY_ISIN or sym.upper() in BY_ISIN:
            inst = BY_ISIN.get(isin.upper()) or BY_ISIN.get(sym.upper())
        elif scheme in BY_SCHEME or sym in BY_SCHEME:
            inst = BY_SCHEME.get(scheme) or BY_SCHEME.get(sym)
        elif name or sym:
            matches = search_instruments(name or sym, limit=1)
            if matches:
                inst = matches[0]

        if not inst:
            unresolved.append({"row": idx, "input": sym or isin or name, "reason": "Instrument not in master"})
            continue

        wt = _to_float(norm.get("weight") or norm.get("weight_pct"))
        qty = _to_float(norm.get("quantity") or norm.get("qty") or norm.get("units"))
        avg = _to_float(norm.get("avg_price") or norm.get("average_price") or norm.get("nav"))
        val = _to_float(norm.get("value") or norm.get("current_value"))

        if val is None and qty and avg:
            val = qty * avg
        computed_values.append(({"s": inst["s"], "w": wt, "qty": qty, "avg_price": avg}, val or 0.0))

    total_val = sum(v for _, v in computed_values)
    for h, val in computed_values:
        if h["w"] is not None and h["w"] > 0:
            w = h["w"]
        elif total_val > 0 and val > 0:
            w = round((val / total_val) * 100.0, 2)
        else:
            w = round(100.0 / max(1, len(computed_values)), 2)
        resolved.append({"s": h["s"], "w": w, "qty": h["qty"], "avg_price": h["avg_price"]})

    merged: Dict[str, Dict] = {}
    for h in resolved:
        if h["s"] in merged:
            merged[h["s"]]["w"] = round(merged[h["s"]]["w"] + h["w"], 2)
        else:
            merged[h["s"]] = h

    return list(merged.values()), unresolved


def _to_float(val: str) -> float | None:
    if not val:
        return None
    try:
        cleaned = val.replace(",", "").replace("%", "").replace("₹", "").strip()
        return float(cleaned)
    except ValueError:
        return None
