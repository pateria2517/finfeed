"""
Seed Corpus, Interest Taxonomy, Benchmark Set & Investor Presets (§4, §6.2, §8, §16).
"""

from typing import Dict, List

INTEREST_TAXONOMY: List[Dict] = [
    {"id": "markets", "label": "Markets", "children": ["Equity markets", "Flows & liquidity", "Index changes", "Volatility"]},
    {"id": "macro", "label": "Economy & macro", "children": ["Inflation", "Growth & GDP", "Rates & RBI", "Currency"]},
    {"id": "policy", "label": "Government & policy", "children": ["Taxation", "Regulation", "Trade & tariffs", "Public spending"]},
    {"id": "corporate", "label": "Corporate actions", "children": ["Earnings", "M&A", "Management change", "Disputes & litigation", "Credit ratings"]},
    {"id": "personal", "label": "Personal finance", "children": ["Mutual funds", "SIP & flows", "Fixed income", "Tax planning"]},
    {"id": "global", "label": "Global markets", "children": ["US markets", "Crude & commodities", "China", "Central banks"]},
    {"id": "sectors", "label": "Sector watch", "children": ["Banking", "IT", "Auto", "FMCG", "Pharma", "Energy", "Metals", "Infra"]},
]

MOOD_HISTORY_7D: List[int] = [44, 47, 52, 49, 46, 51, 54]

SEED_ARTICLES: List[Dict] = [
    {"id": 1, "h": "RBI holds repo rate, signals extended pause through the December review", "s": "regulator", "src": "Reserve Bank of India", "source_id": "rbi_pr", "t": 3, "e": [], "sec": ["Banking", "NBFC"], "top": ["Rates & RBI", "Regulation"], "ev": "macro", "p": 0.15, "c": 0.92, "m": 0.90, "sum": "Policy rate unchanged for a fourth consecutive meeting. Commentary points to comfort on the inflation path with a watchful stance on food prices."},
    {"id": 2, "h": "Retail inflation eases to 3.9% in July, third straight month inside the target band", "s": "regulator", "src": "MoSPI", "source_id": "mospi_rel", "t": 9, "e": [], "sec": [], "top": ["Inflation", "Growth & GDP"], "ev": "macro", "p": 0.55, "c": 0.90, "m": 0.85, "sum": "Food and fuel both cooled. Core inflation was broadly flat, keeping the disinflation trend intact."},
    {"id": 3, "h": "IT services majors guide to low single-digit revenue growth as discretionary spend stays soft", "s": "wire", "src": "Reuters India", "source_id": "reuters_in", "t": 5, "e": ["TCS", "INFY", "HCLTECH", "WIPRO"], "sec": ["IT"], "top": ["Earnings", "IT"], "ev": "earnings", "p": -0.45, "c": 0.85, "m": 0.80, "sum": "Deal pipelines remain healthy but conversion is slow. Managements flagged client caution in BFSI and retail verticals."},
    {"id": 4, "h": "Bank credit growth moderates to 11.2% year-on-year, deposit competition intensifies", "s": "regulator", "src": "Reserve Bank of India", "source_id": "rbi_pr", "t": 14, "e": [], "sec": ["Banking"], "top": ["Banking", "Flows & liquidity"], "ev": "macro", "p": -0.42, "c": 0.88, "m": 0.75, "sum": "Slower credit offtake alongside sticky deposit costs points to continued margin pressure across the sector."},
    {"id": 5, "h": "HDFC Bank reports improvement in liability mix, cost of funds down 14 basis points", "s": "exchange", "src": "NSE Corporate Announcements", "source_id": "nse_corp", "t": 7, "e": ["HDFCBANK"], "sec": ["Banking"], "top": ["Earnings", "Banking"], "ev": "earnings", "p": 0.60, "c": 0.90, "m": 0.85, "sum": "Deposit accretion outpaced loan growth in the quarter, easing a concern that has weighed on the stock."},
    {"id": 6, "h": "Equity mutual fund inflows hold above the monthly average; SIP book sets a fresh high", "s": "regulator", "src": "AMFI", "source_id": "amfi_nav", "t": 11, "e": ["MF-FLEXI", "MF-SMALL", "MF-BAF"], "sec": ["Equity Fund"], "top": ["Mutual funds", "SIP & flows", "Flows & liquidity"], "ev": "flows", "p": 0.65, "c": 0.90, "m": 0.70, "sum": "Systematic contributions continue to cushion the market against foreign selling. Small and mid cap categories saw the largest share."},
    {"id": 7, "h": "Foreign investors turn net sellers for the month; domestic institutions absorb the supply", "s": "wire", "src": "PTI Business Wire", "source_id": "pti_biz", "t": 4, "e": [], "sec": [], "top": ["Flows & liquidity", "Equity markets"], "ev": "flows", "p": -0.35, "c": 0.80, "m": 0.70, "sum": "Selling concentrated in financials and IT. Domestic flows offset the bulk of the outflow, limiting index damage."},
    {"id": 8, "h": "Passenger vehicle dispatches rise 6% ahead of the festive season, entry-level segment lags", "s": "business", "src": "Mint Markets", "source_id": "mint_mkt", "t": 8, "e": ["MARUTI", "TATAMOTORS", "MAHINDRA"], "sec": ["Auto"], "top": ["Auto", "Earnings"], "ev": "sales", "p": 0.40, "c": 0.75, "m": 0.65, "sum": "Utility vehicles drove the growth. Small car demand remains subdued, a continuing drag on volume-led names."},
    {"id": 9, "h": "Crude slips below the recent range on softer demand forecasts", "s": "wire", "src": "Bloomberg Macro", "source_id": "bloomberg_hl", "t": 2, "e": ["RELIANCE", "ONGC"], "sec": ["Energy"], "top": ["Crude & commodities", "Energy"], "ev": "commodity", "p": 0.30, "c": 0.70, "m": 0.70, "sum": "Lower crude is a net positive for the import bill and downstream margins, and a negative for upstream realisations."},
    {"id": 10, "h": "SEBI issues consultation paper on disclosure norms for mutual fund schemes", "s": "regulator", "src": "SEBI", "source_id": "sebi_pr", "t": 6, "e": ["MF-FLEXI", "MF-SMALL", "MF-BAF", "MF-DEBT"], "sec": ["Equity Fund", "Hybrid Fund", "Debt Fund"], "top": ["Regulation", "Mutual funds"], "ev": "regulatory", "p": 0.10, "c": 0.80, "m": 0.60, "sum": "Proposals cover portfolio disclosure frequency and standardised risk communication. Comments open for thirty days."},
    {"id": 11, "h": "Rupee steadies after early weakness as importers step back", "s": "wire", "src": "Reuters India", "source_id": "reuters_in", "t": 1, "e": [], "sec": ["IT"], "top": ["Currency"], "ev": "macro", "p": 0.05, "c": 0.65, "m": 0.50, "sum": "A weaker rupee mildly benefits export-led sectors and pressures import-heavy input costs."},
    {"id": 12, "h": "Cement dispatch volumes pick up as monsoon recedes in the western region", "s": "business", "src": "Business Standard", "source_id": "bs_comp", "t": 16, "e": ["ULTRACEMCO", "LT"], "sec": ["Infra"], "top": ["Infra", "Earnings"], "ev": "sales", "p": 0.45, "c": 0.70, "m": 0.60, "sum": "Realisations improved modestly. Infrastructure order books remain the primary demand driver into the second half."},
    {"id": 13, "h": "Steel prices firm on restocking demand; import pressure eases", "s": "business", "src": "Economic Times", "source_id": "et_mkt", "t": 20, "e": ["TATASTEEL", "JSWSTEEL", "HINDALCO"], "sec": ["Metals"], "top": ["Metals", "China", "Crude & commodities"], "ev": "commodity", "p": 0.50, "c": 0.70, "m": 0.60, "sum": "Domestic mills raised list prices. Sustainability depends on whether the restocking cycle extends past the quarter."},
    {"id": 14, "h": "Telecom tariff discipline holds; average revenue per user inches up across operators", "s": "broker", "src": "Institutional Sector Notes", "source_id": "inst_res", "t": 13, "e": ["BHARTIARTL"], "sec": ["Telecom"], "top": ["Earnings"], "ev": "earnings", "p": 0.35, "c": 0.65, "m": 0.60, "sum": "Subscriber mix continues to shift toward higher-value plans, supporting the revenue trajectory."},
    {"id": 15, "h": "Rural FMCG volumes grow ahead of urban for a second consecutive quarter", "s": "business", "src": "Moneycontrol", "source_id": "mc_news", "t": 22, "e": ["HINDUNILVR", "ITC", "NESTLEIND"], "sec": ["FMCG"], "top": ["FMCG", "Growth & GDP"], "ev": "sales", "p": 0.28, "c": 0.75, "m": 0.65, "sum": "A better monsoon and softer food inflation supported rural demand. Urban premium categories showed some fatigue."},
    {"id": 16, "h": "Small cap valuations stretch past long-term averages, fund managers turn selective", "s": "broker", "src": "Institutional Sector Notes", "source_id": "inst_res", "t": 10, "e": ["MF-SMALL"], "sec": ["Equity Fund"], "top": ["Equity markets", "Mutual funds", "Volatility"], "ev": "valuation", "p": -0.50, "c": 0.70, "m": 0.70, "sum": "Several schemes are holding elevated cash. The concern is concentration risk rather than an imminent correction call."},
    {"id": 17, "h": "Index review adds two names to the benchmark, triggering passive rebalancing flows", "s": "exchange", "src": "NSE Corporate Announcements", "source_id": "nse_corp", "t": 18, "e": ["TRENT", "BEL"], "sec": [], "top": ["Index changes", "Flows & liquidity"], "ev": "index", "p": 0.20, "c": 0.85, "m": 0.55, "sum": "Passive funds will adjust weights ahead of the effective date, creating short-term flow in affected counters."},
    {"id": 18, "h": "Government raises capital expenditure disbursal pace in the first half", "s": "regulator", "src": "PIB Ministry of Finance", "source_id": "pib_fin", "t": 26, "e": ["LT", "ULTRACEMCO", "NTPC", "POWERGRID"], "sec": ["Infra", "Power"], "top": ["Public spending", "Infra"], "ev": "policy", "p": 0.60, "c": 0.85, "m": 0.75, "sum": "Front-loaded spending supports order inflows for infrastructure and capital goods through the rest of the year."},
    {"id": 19, "h": "US Federal Reserve minutes point to a data-dependent path, markets pare rate cut bets", "s": "wire", "src": "US Federal Reserve Releases", "source_id": "fed_fomc", "t": 12, "e": [], "sec": [], "top": ["Central banks", "US markets"], "ev": "macro", "p": -0.25, "c": 0.80, "m": 0.70, "sum": "Global rate expectations feed directly into emerging market flows and the rupee."},
    {"id": 20, "h": "Pharma export volumes to regulated markets rise; pricing pressure persists", "s": "business", "src": "Financial Express", "source_id": "fe_fin", "t": 24, "e": ["SUNPHARMA", "CIPLA"], "sec": ["Pharma"], "top": ["Pharma", "Trade & tariffs"], "ev": "sales", "p": 0.05, "c": 0.70, "m": 0.55, "sum": "Volume growth is offsetting price erosion for now. Specialty portfolios are the differentiator across the sector."},
    {"id": 21, "h": "Corporate bond spreads narrow as issuance calendar picks up", "s": "wire", "src": "Bloomberg Macro", "source_id": "bloomberg_hl", "t": 30, "e": ["MF-DEBT"], "sec": ["Debt Fund"], "top": ["Fixed income", "Rates & RBI"], "ev": "credit_event", "p": 0.35, "c": 0.75, "m": 0.50, "sum": "Improved appetite for corporate paper is supportive for accrual-oriented debt schemes."},
    {"id": 22, "h": "Consumer discretionary demand holds up in the run-up to the festive period", "s": "broker", "src": "Institutional Sector Notes", "source_id": "inst_res", "t": 28, "e": ["TITAN", "DMART"], "sec": ["Consumer"], "top": ["Equity markets"], "ev": "sales", "p": 0.12, "c": 0.60, "m": 0.50, "sum": "Jewellery and organised retail channel checks point to steady footfalls, with some trading down in value segments."},
    {"id": 23, "h": "Board approves capacity expansion at an existing manufacturing site", "s": "exchange", "src": "BSE Corporate Filings", "source_id": "bse_corp", "t": 15, "e": ["RELIANCE"], "sec": ["Energy"], "top": ["Earnings"], "ev": "capex", "p": 0.35, "c": 0.90, "m": 0.60, "sum": "Phased commissioning over the next eight quarters. Funding to be met through internal accruals."},
    {"id": 24, "h": "Rating agency reaffirms outlook on the domestic banking sector as stable", "s": "wire", "src": "CRISIL & ICRA Ratings", "source_id": "crisil_rat", "t": 34, "e": [], "sec": ["Banking", "NBFC"], "top": ["Credit ratings", "Banking"], "ev": "credit_event", "p": 0.40, "c": 0.80, "m": 0.60, "sum": "Asset quality metrics remain near cycle bests. Unsecured retail is flagged as the segment to watch."},
    {"id": 25, "h": "Direct tax collections track ahead of the budget estimate at the halfway mark", "s": "regulator", "src": "PIB Ministry of Finance", "source_id": "pib_fin", "t": 32, "e": [], "sec": [], "top": ["Taxation", "Public spending"], "ev": "policy", "p": 0.50, "c": 0.85, "m": 0.60, "sum": "A buoyant revenue picture reduces pressure on the borrowing programme, which is supportive for bond yields."},
    {"id": 26, "h": "Power demand sets a seasonal record; generation capacity additions accelerate", "s": "business", "src": "Hindu BusinessLine", "source_id": "bl_mkt", "t": 36, "e": ["NTPC", "POWERGRID"], "sec": ["Power"], "top": ["Public spending"], "ev": "sales", "p": 0.22, "c": 0.70, "m": 0.55, "sum": "Peak demand growth continues to outpace GDP, keeping the capacity addition cycle running."},
    {"id": 27, "h": "Trade talks on tariff lines enter a further round without a concluding agreement", "s": "wire", "src": "Financial Times", "source_id": "ft_macro", "t": 21, "e": [], "sec": ["Pharma", "IT", "Metals"], "top": ["Trade & tariffs"], "ev": "policy", "p": -0.48, "c": 0.70, "m": 0.60, "sum": "Prolonged uncertainty weighs on export-facing sectors and on capital expenditure planning."},
    {"id": 28, "h": "Primary market activity picks up with several issues opening this month", "s": "business", "src": "Mint Markets", "source_id": "mint_mkt", "t": 19, "e": [], "sec": [], "top": ["Equity markets", "Flows & liquidity"], "ev": "market", "p": 0.20, "c": 0.60, "m": 0.40, "sum": "Heavy issuance can pull liquidity from the secondary market when sentiment is already fragile."},
    {"id": 29, "h": "Volatility index eases from recent highs as event risk passes", "s": "exchange", "src": "NSE Corporate Announcements", "source_id": "nse_corp", "t": 6, "e": [], "sec": [], "top": ["Volatility", "Equity markets"], "ev": "market", "p": 0.30, "c": 0.75, "m": 0.45, "sum": "Lower implied volatility usually accompanies a period of range-bound trading."},
    {"id": 30, "h": "Retail investors debate whether to trim small cap allocations after the recent run", "s": "social", "src": "r/IndiaInvestments", "source_id": "reddit_indinv", "t": 5, "e": ["MF-SMALL"], "sec": ["Equity Fund"], "top": ["Mutual funds", "Equity markets"], "ev": "sentiment", "p": -0.40, "c": 0.35, "m": 0.25, "sum": "Community sentiment has turned cautious, though this is opinion rather than reported fact."},
    {"id": 31, "h": "Deposit rate revisions announced across several banks", "s": "exchange", "src": "BSE Corporate Filings", "source_id": "bse_corp", "t": 27, "e": ["SBIN", "ICICIBANK", "AXISBANK", "KOTAKBANK"], "sec": ["Banking"], "top": ["Banking", "Rates & RBI", "Fixed income"], "ev": "pricing", "p": -0.38, "c": 0.85, "m": 0.55, "sum": "Higher deposit rates support liability growth but compress net interest margins in the near term."},
    {"id": 32, "h": "Unsecured lending growth cools following earlier regulatory tightening", "s": "regulator", "src": "Reserve Bank of India", "source_id": "rbi_pr", "t": 23, "e": ["BAJFINANCE"], "sec": ["NBFC", "Banking"], "top": ["Regulation", "Banking"], "ev": "regulatory", "p": -0.35, "c": 0.85, "m": 0.70, "sum": "Growth normalisation was the intended outcome. Attention now shifts to whether credit costs follow."},
    {"id": 33, "h": "Monsoon ends above the long period average, reservoir levels comfortable", "s": "regulator", "src": "IMD Bulletins", "source_id": "imd_weather", "t": 40, "e": [], "sec": ["FMCG", "Auto"], "top": ["Growth & GDP", "Inflation"], "ev": "macro", "p": 0.55, "c": 0.85, "m": 0.65, "sum": "A good monsoon supports the rabi sowing outlook, rural incomes and the food inflation trajectory."},
    {"id": 34, "h": "Production-linked incentive disbursements expand to additional sectors", "s": "regulator", "src": "PIB Ministry of Finance", "source_id": "pib_fin", "t": 38, "e": [], "sec": ["Metals", "Auto", "Pharma"], "top": ["Public spending", "Regulation"], "ev": "policy", "p": 0.22, "c": 0.80, "m": 0.55, "sum": "Scheme expansion is incrementally positive for domestic manufacturing capacity plans."},
    # Additional rich stories covering M&A, management change, litigation, and a deliberate wire duplicate for L2 dedup
    {"id": 35, "h": "UltraTech Cement completes acquisition of regional clinker assets to expand southern footprint", "s": "exchange", "src": "NSE Corporate Announcements", "source_id": "nse_corp", "t": 4, "e": ["ULTRACEMCO"], "sec": ["Infra"], "top": ["M&A", "Infra"], "ev": "M&A", "p": 0.45, "c": 0.90, "m": 0.75, "sum": "Deal adds 10.5 MTPA grinding capacity and reduces logistics lead times in southern markets."},
    {"id": 36, "h": "Infosys appoints new Chief Delivery Officer to oversee AI-led enterprise transformation deals", "s": "exchange", "src": "BSE Corporate Filings", "source_id": "bse_corp", "t": 8, "e": ["INFY"], "sec": ["IT"], "top": ["Management change", "IT"], "ev": "management_change", "p": 0.25, "c": 0.85, "m": 0.50, "sum": "Internal elevation from the European financial services unit; transition effective next quarter."},
    {"id": 37, "h": "Tax tribunal grants interim stay on ₹1,200 crore GST demand notice against Sun Pharma", "s": "business", "src": "Economic Times", "source_id": "et_mkt", "t": 11, "e": ["SUNPHARMA"], "sec": ["Pharma"], "top": ["Disputes & litigation", "Pharma", "Taxation"], "ev": "litigation_disputes", "p": 0.30, "c": 0.80, "m": 0.60, "sum": "Final hearing scheduled in Q4; company had previously disclosed the contingent liability in notes."},
    {"id": 38, "h": "TCS wins multi-year core banking modernisation mandate from Nordic lender", "s": "exchange", "src": "NSE Corporate Announcements", "source_id": "nse_corp", "t": 3, "e": ["TCS"], "sec": ["IT"], "top": ["Earnings", "IT"], "ev": "product", "p": 0.55, "c": 0.88, "m": 0.65, "sum": "Deal value undisclosed; platform migration expected to ramp up over 18 months."},
    # Deliberate near-duplicate wire copy of Article #1 to demonstrate L2 Shingling/Cosine Deduplication
    {"id": 39, "h": "RBI holds repo rate steady, signals extended pause through December policy review", "s": "wire", "src": "PTI Business Wire", "source_id": "pti_biz", "t": 3.5, "e": [], "sec": ["Banking", "NBFC"], "top": ["Rates & RBI", "Regulation"], "ev": "macro", "p": 0.15, "c": 0.85, "m": 0.85, "sum": "Policy rate unchanged for a fourth consecutive meeting as commentary points to comfort on inflation with a watchful stance on food prices."},
]

PRESETS: Dict[str, Dict] = {
    "A": {
        "user_id": "investor_a",
        "name": "Investor A",
        "note": "Long-term, fund-heavy, macro reader",
        "mode": "P1_RETAIL",
        "persona": {"type": "Active investor", "horizon": "Long term", "style": "Deep analysis", "alerts": "Daily digest"},
        "interests": {"Rates & RBI": 1.0, "Inflation": 1.0, "Mutual funds": 1.0, "SIP & flows": 0.7, "Fixed income": 0.7, "Public spending": 0.7, "Banking": 0.7},
        "holdings": [
            {"s": "MF-FLEXI", "w": 30}, {"s": "MF-BAF", "w": 20}, {"s": "MF-DEBT", "w": 15},
            {"s": "HDFCBANK", "w": 12}, {"s": "ITC", "w": 8}, {"s": "NTPC", "w": 8}, {"s": "SUNPHARMA", "w": 7},
        ],
    },
    "B": {
        "user_id": "investor_b",
        "name": "Investor B",
        "note": "Trader, direct equity, sector rotation",
        "mode": "P1_RETAIL",
        "persona": {"type": "Professional", "horizon": "Trading", "style": "Data first", "alerts": "Real time"},
        "interests": {"Equity markets": 1.0, "Volatility": 1.0, "Metals": 1.0, "IT": 0.8, "Index changes": 0.8, "Crude & commodities": 0.8, "US markets": 0.6},
        "holdings": [
            {"s": "TATASTEEL", "w": 22}, {"s": "JSWSTEEL", "w": 15}, {"s": "INFY", "w": 18},
            {"s": "RELIANCE", "w": 15}, {"s": "MF-SMALL", "w": 18}, {"s": "TITAN", "w": 12},
        ],
    },
    "MFD": {
        "user_id": "mfd_advisor",
        "name": "Lark MFD Desk",
        "note": "AMFI distributor · 3 sample client books aggregated",
        "mode": "P2_MFD",
        "persona": {"type": "Distributor / advisor", "horizon": "1 to 3 years", "style": "Deep analysis", "alerts": "Daily digest"},
        "interests": {"Mutual funds": 1.0, "SIP & flows": 1.0, "Regulation": 1.0, "Rates & RBI": 0.8, "Taxation": 0.8},
        "clients": [
            {"id": "c1", "name": "R. Sharma (₹18L)", "aum": 1800000, "holdings": [{"s": "MF-FLEXI", "w": 45}, {"s": "MF-BAF", "w": 35}, {"s": "MF-DEBT", "w": 20}]},
            {"id": "c2", "name": "A. Mehta (₹32L)", "aum": 3200000, "holdings": [{"s": "MF-SMALL", "w": 40}, {"s": "MF-FLEXI", "w": 35}, {"s": "HDFCBANK", "w": 15}, {"s": "TCS", "w": 10}]},
            {"id": "c3", "name": "K. Nair (₹12L)", "aum": 1200000, "holdings": [{"s": "MF-DEBT", "w": 50}, {"s": "MF-BAF", "w": 30}, {"s": "ITC", "w": 20}]},
        ],
    },
}

# Hand-labelled sentiment benchmark subset (§6.2)
SENTIMENT_BENCHMARK: List[Dict] = [
    {"text": "HDFC Bank reports improvement in liability mix, cost of funds down 14 basis points", "expected_sign": 1},
    {"text": "IT services majors guide to low single-digit revenue growth as discretionary spend stays soft", "expected_sign": -1},
    {"text": "Retail inflation eases to 3.9% in July, third straight month inside the target band", "expected_sign": 1},
    {"text": "Small cap valuations stretch past long-term averages, fund managers turn selective", "expected_sign": -1},
    {"text": "Equity mutual fund inflows hold above the monthly average; SIP book sets a fresh high", "expected_sign": 1},
    {"text": "Unsecured lending growth cools following earlier regulatory tightening", "expected_sign": -1},
    {"text": "Trade talks on tariff lines enter a further round without a concluding agreement", "expected_sign": -1},
    {"text": "Government raises capital expenditure disbursal pace in the first half", "expected_sign": 1},
]
