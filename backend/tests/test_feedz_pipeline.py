"""
End-to-End Verification Suite for Feedz L1-L6 Pipeline & Acceptance Criteria (§8, §11, §16).
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.data.instruments import INSTRUMENTS, search_instruments
from app.data.seed_corpus import PRESETS, SENTIMENT_BENCHMARK
from app.services.l1_ingestion import RawPayloadStore, run_scheduled_ingestion
from app.services.l2_normalisation import normalise_and_deduplicate
from app.services.l3_enrichment import enrich_articles, evaluate_sentiment_benchmark, extract_entities
from app.services.l4_personalisation import aggregate_client_book, compute_feed_overlap, rank_feed
from app.services.l5_intelligence import ask_feed, enforce_sebi_guardrail, why_this_matters
from app.services.portfolio_parser import parse_portfolio_csv
from app.services.sentiment_engine import market_mood, portfolio_mood


class TestFeedzPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.store = RawPayloadStore()
        run_scheduled_ingestion(cls.store, live_network=False)
        raw = [r["payload"] for r in cls.store.list_all()]
        cls.canonical, cls.dups = normalise_and_deduplicate(raw)
        cls.enriched = enrich_articles(cls.canonical)
        cls.mood = market_mood(cls.enriched)

    def test_instrument_master_coverage_and_alias(self):
        self.assertGreaterEqual(len(INSTRUMENTS), 150)
        res = search_instruments("the private lender")
        self.assertTrue(any(r["s"] == "HDFCBANK" for r in res))
        self.assertIn("HDFCBANK", extract_entities("The private lender cut deposit costs."))

    def test_l2_deduplication_catches_wire_copy(self):
        dup_ids = [d["id"] for d in self.dups]
        self.assertIn(39, dup_ids, "Article 39 (wire duplicate of RBI pause) should be deduplicated")

    def test_sentiment_benchmark_accuracy(self):
        res = evaluate_sentiment_benchmark(SENTIMENT_BENCHMARK)
        self.assertGreaterEqual(res["accuracy"], 0.75)

    def test_c2_persona_overlap_below_30_percent(self):
        feed_a = rank_feed(self.enriched, PRESETS["A"])
        feed_b = rank_feed(self.enriched, PRESETS["B"])
        overlap = compute_feed_overlap(feed_a, feed_b, top_n=10)
        self.assertTrue(
            overlap["passes_30pct_target"],
            f"Expected <=30% overlap between Investor A and B, got {overlap['overlap_pct']}%",
        )

    def test_c3_adding_holding_changes_feed(self):
        base_profile = {
            "persona": PRESETS["A"]["persona"],
            "interests": {"Rates & RBI": 1.0},
            "holdings": [{"s": "MF-DEBT", "w": 100}],
        }
        before = rank_feed(self.enriched, base_profile)
        after_profile = {
            **base_profile,
            "holdings": [{"s": "MF-DEBT", "w": 50}, {"s": "ULTRACEMCO", "w": 50}],
        }
        after = rank_feed(self.enriched, after_profile)
        self.assertNotEqual([x["id"] for x in before[:5]], [x["id"] for x in after[:5]])

    def test_csv_portfolio_parser(self):
        csv_data = "symbol,quantity,avg_price\nHDFCBANK,10,1600\nINE467B01029,5,3900\n122639,100,80\n"
        resolved, unresolved = parse_portfolio_csv(csv_data)
        self.assertEqual(len(unresolved), 0)
        syms = {h["s"] for h in resolved}
        self.assertEqual(syms, {"HDFCBANK", "TCS", "MF-FLEXI"})

    def test_p2_mfd_client_book_aggregation(self):
        agg = aggregate_client_book(PRESETS["MFD"]["clients"])
        self.assertGreater(len(agg), 3)
        p_mood = portfolio_mood(agg, self.mood["entity_scores"])
        self.assertIsNotNone(p_mood)

    def test_sebi_guardrails_block_advice(self):
        check = enforce_sebi_guardrail("You should buy HDFCBANK with a target price of 2100.")
        self.assertFalse(check["compliant"])
        feed_a = rank_feed(self.enriched, PRESETS["A"])
        qa = ask_feed("Should I buy Tata Steel right now?", feed_a, PRESETS["A"], self.mood)
        self.assertTrue(qa["refused_advisory"])
        why = why_this_matters(feed_a[0], PRESETS["A"])
        self.assertTrue(why["compliant"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
