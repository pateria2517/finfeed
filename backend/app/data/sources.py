"""
Data Sources Configuration (§5) — 28 configured sources across 6 categories.
Each source is a configuration row, not code (§4 L1).
"""

from typing import Dict, List

SOURCE_CATEGORIES: Dict[str, Dict] = {
    "exchange": {"label": "Exchange filing", "w": 1.0, "kind": "primary"},
    "regulator": {"label": "Regulator", "w": 1.0, "kind": "primary"},
    "wire": {"label": "Wire", "w": 0.85, "kind": "wire"},
    "business": {"label": "Business daily", "w": 0.70, "kind": "media"},
    "broker": {"label": "Broker note", "w": 0.60, "kind": "research"},
    "social": {"label": "Social / community", "w": 0.30, "kind": "social"},
}

SOURCES_CONFIG: List[Dict] = [
    # Exchange & Regulator (w = 1.0)
    {"id": "nse_corp", "name": "NSE Corporate Announcements", "category": "exchange", "method": "REST", "url": "https://www.nseindia.com/api/corporate-announcements", "poll_min": 5, "enabled": True},
    {"id": "bse_corp", "name": "BSE Corporate Filings", "category": "exchange", "method": "RSS", "url": "https://www.bseindia.com/data/xml/notices.xml", "poll_min": 5, "enabled": True},
    {"id": "sebi_pr", "name": "SEBI Press Releases & Circulars", "category": "regulator", "method": "RSS", "url": "https://www.sebi.gov.in/sebirss.xml", "poll_min": 15, "enabled": True},
    {"id": "rbi_pr", "name": "Reserve Bank of India Notifications", "category": "regulator", "method": "RSS", "url": "https://www.rbi.org.in/notifications_rss.xml", "poll_min": 15, "enabled": True},
    {"id": "pib_fin", "name": "PIB Ministry of Finance", "category": "regulator", "method": "RSS", "url": "https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1", "poll_min": 30, "enabled": True},
    {"id": "mospi_rel", "name": "MoSPI Macro Releases", "category": "regulator", "method": "SCRAPE", "url": "https://mospi.gov.in/press-release", "poll_min": 60, "enabled": True},
    {"id": "amfi_nav", "name": "AMFI NAV & Flow Disclosures", "category": "regulator", "method": "FILE", "url": "https://www.amfiindia.com/spages/NAVAll.txt", "poll_min": 60, "enabled": True},
    {"id": "imd_weather", "name": "IMD Monsoon & Agri Bulletins", "category": "regulator", "method": "RSS", "url": "https://mausam.imd.gov.in/rss.xml", "poll_min": 180, "enabled": True},

    # Wires & Global Macro (w = 0.85)
    {"id": "reuters_in", "name": "Reuters India Markets", "category": "wire", "method": "RSS", "url": "https://feeds.reuters.com/reuters/INbusinessNews", "poll_min": 10, "enabled": True},
    {"id": "pti_biz", "name": "PTI Business Wire", "category": "wire", "method": "RSS", "url": "https://www.ptinews.com/rss/business.xml", "poll_min": 10, "enabled": True},
    {"id": "bloomberg_hl", "name": "Bloomberg Macro Headlines", "category": "wire", "method": "API", "url": "https://api.bloomberg.com/headlines/in", "poll_min": 15, "enabled": True},
    {"id": "ft_macro", "name": "Financial Times Global Macro", "category": "wire", "method": "RSS", "url": "https://www.ft.com/world?format=rss", "poll_min": 30, "enabled": True},
    {"id": "fed_fomc", "name": "US Federal Reserve Releases", "category": "wire", "method": "RSS", "url": "https://www.federalreserve.gov/feeds/press_all.xml", "poll_min": 60, "enabled": True},

    # Business Media (w = 0.70)
    {"id": "mint_mkt", "name": "Mint Markets & Companies", "category": "business", "method": "RSS", "url": "https://www.livemint.com/rss/markets", "poll_min": 15, "enabled": True},
    {"id": "et_mkt", "name": "Economic Times Markets", "category": "business", "method": "RSS", "url": "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms", "poll_min": 15, "enabled": True},
    {"id": "bs_comp", "name": "Business Standard Companies", "category": "business", "method": "RSS", "url": "https://www.business-standard.com/rss/companies-101.rss", "poll_min": 15, "enabled": True},
    {"id": "mc_news", "name": "Moneycontrol Business", "category": "business", "method": "RSS", "url": "https://www.moneycontrol.com/rss/business.xml", "poll_min": 15, "enabled": True},
    {"id": "fe_fin", "name": "Financial Express Banking & Finance", "category": "business", "method": "RSS", "url": "https://www.financialexpress.com/economy/feed/", "poll_min": 30, "enabled": True},
    {"id": "bl_mkt", "name": "Hindu BusinessLine Markets", "category": "business", "method": "RSS", "url": "https://www.thehindubusinessline.com/markets/feeder/default.rss", "poll_min": 30, "enabled": True},
    {"id": "val_res", "name": "Value Research MF Insights", "category": "business", "method": "RSS", "url": "https://www.valueresearchonline.com/rss/stories/", "poll_min": 60, "enabled": True},

    # Fund Disclosures & Broker Research (w = 0.60)
    {"id": "amc_factsheet", "name": "AMC Monthly Factsheets & SID", "category": "broker", "method": "FILE", "url": "https://amc-disclosures.feedz.local/factsheets", "poll_min": 1440, "enabled": True},
    {"id": "crisil_rat", "name": "CRISIL & ICRA Credit Ratings", "category": "broker", "method": "RSS", "url": "https://www.crisilratings.com/rss/press.xml", "poll_min": 60, "enabled": True},
    {"id": "inst_res", "name": "Institutional Sector Notes", "category": "broker", "method": "REST", "url": "https://research.feedz.local/notes", "poll_min": 120, "enabled": True},
    {"id": "fii_dii", "name": "NSDL / NSE FII-DII Flow Data", "category": "broker", "method": "FILE", "url": "https://www.fpi.nsdl.co.in/web/Reports/Latest.aspx", "poll_min": 1440, "enabled": True},

    # Social & Community (w = 0.30, seeded/curated)
    {"id": "reddit_indinv", "name": "r/IndiaInvestments Curated", "category": "social", "method": "RSS", "url": "https://www.reddit.com/r/IndiaInvestments/top/.rss", "poll_min": 60, "enabled": True},
    {"id": "x_fin_list", "name": "Curated FinTwit India List", "category": "social", "method": "API", "url": "https://api.x.com/2/lists/feedz-india-fin", "poll_min": 30, "enabled": True},
    {"id": "substack_fin", "name": "Indian Capital Markets Newsletters", "category": "social", "method": "RSS", "url": "https://finshots.in/rss/", "poll_min": 120, "enabled": True},
    {"id": "forum_mf", "name": "Retail MF Investor Forums", "category": "social", "method": "RSS", "url": "https://forum.valuepickr.com/latest.rss", "poll_min": 120, "enabled": True},
]

SOURCE_BY_ID: Dict[str, Dict] = {s["id"]: s for s in SOURCES_CONFIG}
