"""
Instrument Master (~205 instruments) — The join between the news world and the money world (§7).
Includes Indian Equities (Nifty 50, Nifty Next 50, key Midcaps), Mutual Funds (with AMFI scheme codes),
ETFs, and Market Indices, each with ticker, ISIN, sector, index memberships, cap weight, and alias table.
"""

from typing import Dict, List, Optional

INSTRUMENTS: List[Dict] = [
    # --- BANKING & FINANCIALS ---
    {"s": "HDFCBANK", "n": "HDFC Bank Ltd", "isin": "INE040A01034", "sec": "Banking", "type": "EQUITY", "cap": 1280000, "idx": ["NIFTY50", "BANKNIFTY"], "a": ["hdfc bank", "hdfcbank", "the private lender", "hdfc"]},
    {"s": "ICICIBANK", "n": "ICICI Bank Ltd", "isin": "INE090A01021", "sec": "Banking", "type": "EQUITY", "cap": 910000, "idx": ["NIFTY50", "BANKNIFTY"], "a": ["icici bank", "icicibank", "icici"]},
    {"s": "SBIN", "n": "State Bank of India", "isin": "INE062A01020", "sec": "Banking", "type": "EQUITY", "cap": 740000, "idx": ["NIFTY50", "BANKNIFTY"], "a": ["sbi", "state bank", "state bank of india"]},
    {"s": "AXISBANK", "n": "Axis Bank Ltd", "isin": "INE238A01034", "sec": "Banking", "type": "EQUITY", "cap": 365000, "idx": ["NIFTY50", "BANKNIFTY"], "a": ["axis bank", "axis"]},
    {"s": "KOTAKBANK", "n": "Kotak Mahindra Bank Ltd", "isin": "INE237A01028", "sec": "Banking", "type": "EQUITY", "cap": 355000, "idx": ["NIFTY50", "BANKNIFTY"], "a": ["kotak", "kotak bank", "kotak mahindra"]},
    {"s": "INDUSINDBK", "n": "IndusInd Bank Ltd", "isin": "INE095A01012", "sec": "Banking", "type": "EQUITY", "cap": 85000, "idx": ["NIFTY50", "BANKNIFTY"], "a": ["indusind", "indusind bank"]},
    {"s": "BANKBARODA", "n": "Bank of Baroda", "isin": "INE028A01039", "sec": "Banking", "type": "EQUITY", "cap": 130000, "idx": ["BANKNIFTY"], "a": ["bob", "bank of baroda"]},
    {"s": "PNB", "n": "Punjab National Bank", "isin": "INE160A01022", "sec": "Banking", "type": "EQUITY", "cap": 115000, "idx": ["BANKNIFTY"], "a": ["pnb", "punjab national bank"]},
    {"s": "FEDERALBNK", "n": "Federal Bank Ltd", "isin": "INE171A01029", "sec": "Banking", "type": "EQUITY", "cap": 48000, "idx": ["BANKNIFTY"], "a": ["federal bank"]},
    {"s": "IDFCFIRSTB", "n": "IDFC First Bank Ltd", "isin": "INE092T01019", "sec": "Banking", "type": "EQUITY", "cap": 52000, "idx": ["BANKNIFTY"], "a": ["idfc first", "idfc bank"]},
    {"s": "AUBANK", "n": "AU Small Finance Bank", "isin": "INE949L01017", "sec": "Banking", "type": "EQUITY", "cap": 46000, "idx": ["BANKNIFTY"], "a": ["au bank", "au small finance"]},
    {"s": "CANBK", "n": "Canara Bank", "isin": "INE476A01022", "sec": "Banking", "type": "EQUITY", "cap": 95000, "idx": ["BANKNIFTY"], "a": ["canara bank"]},

    # --- NBFC & INSURANCE ---
    {"s": "BAJFINANCE", "n": "Bajaj Finance Ltd", "isin": "INE296A01024", "sec": "NBFC", "type": "EQUITY", "cap": 440000, "idx": ["NIFTY50", "FINNIFTY"], "a": ["bajaj finance", "bajaj fin", "bfl"]},
    {"s": "BAJAJFINSV", "n": "Bajaj Finserv Ltd", "isin": "INE918I01026", "sec": "NBFC", "type": "EQUITY", "cap": 270000, "idx": ["NIFTY50", "FINNIFTY"], "a": ["bajaj finserv"]},
    {"s": "JIOFIN", "n": "Jio Financial Services Ltd", "isin": "INE758E01017", "sec": "NBFC", "type": "EQUITY", "cap": 205000, "idx": ["NIFTYNEXT50", "FINNIFTY"], "a": ["jio financial", "jiofin"]},
    {"s": "SHRIRAMFIN", "n": "Shriram Finance Ltd", "isin": "INE721A01013", "sec": "NBFC", "type": "EQUITY", "cap": 115000, "idx": ["NIFTY50", "FINNIFTY"], "a": ["shriram finance", "shriram"]},
    {"s": "CHOLAFIN", "n": "Cholamandalam Investment & Finance", "isin": "INE121A01024", "sec": "NBFC", "type": "EQUITY", "cap": 112000, "idx": ["NIFTYNEXT50", "FINNIFTY"], "a": ["chola", "cholamandalam"]},
    {"s": "SBILIFE", "n": "SBI Life Insurance Company", "isin": "INE123W01016", "sec": "NBFC", "type": "EQUITY", "cap": 168000, "idx": ["NIFTY50", "FINNIFTY"], "a": ["sbi life"]},
    {"s": "HDFCLIFE", "n": "HDFC Life Insurance Company", "isin": "INE795G01014", "sec": "NBFC", "type": "EQUITY", "cap": 148000, "idx": ["NIFTY50", "FINNIFTY"], "a": ["hdfc life"]},
    {"s": "ICICIGI", "n": "ICICI Lombard General Insurance", "isin": "INE765G01017", "sec": "NBFC", "type": "EQUITY", "cap": 95000, "idx": ["NIFTYNEXT50"], "a": ["icici lombard"]},
    {"s": "MUTHOOTFIN", "n": "Muthoot Finance Ltd", "isin": "INE414G01012", "sec": "NBFC", "type": "EQUITY", "cap": 78000, "idx": ["FINNIFTY"], "a": ["muthoot", "muthoot finance"]},
    {"s": "PFC", "n": "Power Finance Corporation", "isin": "INE134E01011", "sec": "NBFC", "type": "EQUITY", "cap": 152000, "idx": ["NIFTYNEXT50"], "a": ["pfc", "power finance"]},
    {"s": "RECLTD", "n": "REC Ltd", "isin": "INE020B01018", "sec": "NBFC", "type": "EQUITY", "cap": 140000, "idx": ["NIFTYNEXT50"], "a": ["rec", "rural electrification"]},
    {"s": "LICI", "n": "Life Insurance Corporation of India", "isin": "INE0J1Y01017", "sec": "NBFC", "type": "EQUITY", "cap": 610000, "idx": ["NIFTYNEXT50"], "a": ["lic", "lic india"]},

    # --- IT SERVICES ---
    {"s": "TCS", "n": "Tata Consultancy Services Ltd", "isin": "INE467B01029", "sec": "IT", "type": "EQUITY", "cap": 1480000, "idx": ["NIFTY50", "NIFTYIT"], "a": ["tcs", "tata consultancy", "tata consultancy services"]},
    {"s": "INFY", "n": "Infosys Ltd", "isin": "INE009A01021", "sec": "IT", "type": "EQUITY", "cap": 780000, "idx": ["NIFTY50", "NIFTYIT"], "a": ["infosys", "infy"]},
    {"s": "HCLTECH", "n": "HCL Technologies Ltd", "isin": "INE860A01027", "sec": "IT", "type": "EQUITY", "cap": 490000, "idx": ["NIFTY50", "NIFTYIT"], "a": ["hcl tech", "hcl technologies", "hcl"]},
    {"s": "WIPRO", "n": "Wipro Ltd", "isin": "INE075A01022", "sec": "IT", "type": "EQUITY", "cap": 295000, "idx": ["NIFTY50", "NIFTYIT"], "a": ["wipro"]},
    {"s": "TECHM", "n": "Tech Mahindra Ltd", "isin": "INE669C01036", "sec": "IT", "type": "EQUITY", "cap": 162000, "idx": ["NIFTY50", "NIFTYIT"], "a": ["tech mahindra", "techm"]},
    {"s": "LTIM", "n": "LTIMindtree Ltd", "isin": "INE214T01019", "sec": "IT", "type": "EQUITY", "cap": 175000, "idx": ["NIFTYNEXT50", "NIFTYIT"], "a": ["ltimindtree", "ltim", "mindtree"]},
    {"s": "PERSISTENT", "n": "Persistent Systems Ltd", "isin": "INE262H01021", "sec": "IT", "type": "EQUITY", "cap": 88000, "idx": ["NIFTYIT"], "a": ["persistent", "persistent systems"]},
    {"s": "COFORGE", "n": "Coforge Ltd", "isin": "INE591G01017", "sec": "IT", "type": "EQUITY", "cap": 54000, "idx": ["NIFTYIT"], "a": ["coforge"]},
    {"s": "MPHASIS", "n": "Mphasis Ltd", "isin": "INE356A01018", "sec": "IT", "type": "EQUITY", "cap": 55000, "idx": ["NIFTYIT"], "a": ["mphasis"]},
    {"s": "KPITTECH", "n": "KPIT Technologies Ltd", "isin": "INE04I401011", "sec": "IT", "type": "EQUITY", "cap": 42000, "idx": ["NIFTYMIDCAP"], "a": ["kpit", "kpit tech"]},
    {"s": "TATAELXSI", "n": "Tata Elxsi Ltd", "isin": "INE670A01012", "sec": "IT", "type": "EQUITY", "cap": 46000, "idx": ["NIFTYMIDCAP"], "a": ["tata elxsi"]},

    # --- ENERGY & OIL/GAS ---
    {"s": "RELIANCE", "n": "Reliance Industries Ltd", "isin": "INE002A01018", "sec": "Energy", "type": "EQUITY", "cap": 1850000, "idx": ["NIFTY50"], "a": ["reliance", "ril", "mukesh ambani", "jio", "reliance industries"]},
    {"s": "ONGC", "n": "Oil & Natural Gas Corporation Ltd", "isin": "INE213A01029", "sec": "Energy", "type": "EQUITY", "cap": 340000, "idx": ["NIFTY50"], "a": ["ongc", "oil & natural gas"]},
    {"s": "BPCL", "n": "Bharat Petroleum Corporation Ltd", "isin": "INE029A01011", "sec": "Energy", "type": "EQUITY", "cap": 140000, "idx": ["NIFTY50"], "a": ["bpcl", "bharat petroleum"]},
    {"s": "IOC", "n": "Indian Oil Corporation Ltd", "isin": "INE242A01010", "sec": "Energy", "type": "EQUITY", "cap": 215000, "idx": ["NIFTYNEXT50"], "a": ["ioc", "indian oil"]},
    {"s": "GAIL", "n": "GAIL (India) Ltd", "isin": "INE129A01019", "sec": "Energy", "type": "EQUITY", "cap": 135000, "idx": ["NIFTYNEXT50"], "a": ["gail"]},
    {"s": "COALINDIA", "n": "Coal India Ltd", "isin": "INE522F01014", "sec": "Energy", "type": "EQUITY", "cap": 285000, "idx": ["NIFTY50"], "a": ["coal india", "cil"]},
    {"s": "HINDPETRO", "n": "Hindustan Petroleum Corporation", "isin": "INE094A01015", "sec": "Energy", "type": "EQUITY", "cap": 82000, "idx": ["NIFTYMIDCAP"], "a": ["hpcl", "hindustan petroleum"]},
    {"s": "IGL", "n": "Indraprastha Gas Ltd", "isin": "INE203G01027", "sec": "Energy", "type": "EQUITY", "cap": 32000, "idx": ["NIFTYMIDCAP"], "a": ["igl", "indraprastha gas"]},
    {"s": "PETRONET", "n": "Petronet LNG Ltd", "isin": "INE347G01014", "sec": "Energy", "type": "EQUITY", "cap": 51000, "idx": ["NIFTYMIDCAP"], "a": ["petronet", "petronet lng"]},

    # --- AUTO & MOBILITY ---
    {"s": "MARUTI", "n": "Maruti Suzuki India Ltd", "isin": "INE585B01010", "sec": "Auto", "type": "EQUITY", "cap": 395000, "idx": ["NIFTY50", "NIFTYAUTO"], "a": ["maruti", "maruti suzuki", "msil"]},
    {"s": "TATAMOTORS", "n": "Tata Motors Ltd", "isin": "INE155A01022", "sec": "Auto", "type": "EQUITY", "cap": 345000, "idx": ["NIFTY50", "NIFTYAUTO"], "a": ["tata motors", "jlr"]},
    {"s": "MAHINDRA", "n": "Mahindra & Mahindra Ltd", "isin": "INE101A01026", "sec": "Auto", "type": "EQUITY", "cap": 365000, "idx": ["NIFTY50", "NIFTYAUTO"], "a": ["m&m", "mahindra", "mahindra & mahindra"]},
    {"s": "BAJAJ-AUTO", "n": "Bajaj Auto Ltd", "isin": "INE917I01010", "sec": "Auto", "type": "EQUITY", "cap": 285000, "idx": ["NIFTY50", "NIFTYAUTO"], "a": ["bajaj auto"]},
    {"s": "EICHERMOT", "n": "Eicher Motors Ltd", "isin": "INE066A01021", "sec": "Auto", "type": "EQUITY", "cap": 135000, "idx": ["NIFTY50", "NIFTYAUTO"], "a": ["eicher", "eicher motors", "royal enfield"]},
    {"s": "HEROMOTOCO", "n": "Hero MotoCorp Ltd", "isin": "INE158A01026", "sec": "Auto", "type": "EQUITY", "cap": 105000, "idx": ["NIFTY50", "NIFTYAUTO"], "a": ["hero motocorp", "hero"]},
    {"s": "TVSMOTOR", "n": "TVS Motor Company Ltd", "isin": "INE494B01023", "sec": "Auto", "type": "EQUITY", "cap": 122000, "idx": ["NIFTYNEXT50", "NIFTYAUTO"], "a": ["tvs motor", "tvs"]},
    {"s": "ASHOKLEY", "n": "Ashok Leyland Ltd", "isin": "INE208A01029", "sec": "Auto", "type": "EQUITY", "cap": 68000, "idx": ["NIFTYAUTO"], "a": ["ashok leyland"]},
    {"s": "MOTHERSON", "n": "Samvardhana Motherson International", "isin": "INE775A01035", "sec": "Auto", "type": "EQUITY", "cap": 118000, "idx": ["NIFTYNEXT50", "NIFTYAUTO"], "a": ["motherson", "samvardhana motherson"]},
    {"s": "BHARATFORG", "n": "Bharat Forge Ltd", "isin": "INE465A01025", "sec": "Auto", "type": "EQUITY", "cap": 67000, "idx": ["NIFTYAUTO"], "a": ["bharat forge"]},
    {"s": "MRF", "n": "MRF Ltd", "isin": "INE883A01011", "sec": "Auto", "type": "EQUITY", "cap": 56000, "idx": ["NIFTYAUTO"], "a": ["mrf"]},

    # --- FMCG ---
    {"s": "HINDUNILVR", "n": "Hindustan Unilever Ltd", "isin": "INE030A01027", "sec": "FMCG", "type": "EQUITY", "cap": 590000, "idx": ["NIFTY50", "NIFTYFMCG"], "a": ["hul", "hindustan unilever"]},
    {"s": "ITC", "n": "ITC Ltd", "isin": "INE154A01025", "sec": "FMCG", "type": "EQUITY", "cap": 605000, "idx": ["NIFTY50", "NIFTYFMCG"], "a": ["itc"]},
    {"s": "NESTLEIND", "n": "Nestle India Ltd", "isin": "INE239A01024", "sec": "FMCG", "type": "EQUITY", "cap": 235000, "idx": ["NIFTY50", "NIFTYFMCG"], "a": ["nestle india", "nestle"]},
    {"s": "BRITANNIA", "n": "Britannia Industries Ltd", "isin": "INE216A01030", "sec": "FMCG", "type": "EQUITY", "cap": 132000, "idx": ["NIFTY50", "NIFTYFMCG"], "a": ["britannia"]},
    {"s": "TATACONSUM", "n": "Tata Consumer Products Ltd", "isin": "INE192A01025", "sec": "FMCG", "type": "EQUITY", "cap": 102000, "idx": ["NIFTY50", "NIFTYFMCG"], "a": ["tata consumer", "tcpl"]},
    {"s": "DABUR", "n": "Dabur India Ltd", "isin": "INE016A01026", "sec": "FMCG", "type": "EQUITY", "cap": 98000, "idx": ["NIFTYNEXT50", "NIFTYFMCG"], "a": ["dabur"]},
    {"s": "GODREJCP", "n": "Godrej Consumer Products Ltd", "isin": "INE102D01028", "sec": "FMCG", "type": "EQUITY", "cap": 130000, "idx": ["NIFTYNEXT50", "NIFTYFMCG"], "a": ["godrej consumer", "gcpl"]},
    {"s": "MARICO", "n": "Marico Ltd", "isin": "INE196A01026", "sec": "FMCG", "type": "EQUITY", "cap": 84000, "idx": ["NIFTYFMCG"], "a": ["marico"]},
    {"s": "COLPAL", "n": "Colgate-Palmolive (India) Ltd", "isin": "INE259A01022", "sec": "FMCG", "type": "EQUITY", "cap": 82000, "idx": ["NIFTYFMCG"], "a": ["colgate", "colpal"]},
    {"s": "VBL", "n": "Varun Beverages Ltd", "isin": "INE200M01039", "sec": "FMCG", "type": "EQUITY", "cap": 195000, "idx": ["NIFTYNEXT50", "NIFTYFMCG"], "a": ["varun beverages", "vbl"]},
    {"s": "UBL", "n": "United Breweries Ltd", "isin": "INE686F01025", "sec": "FMCG", "type": "EQUITY", "cap": 54000, "idx": ["NIFTYFMCG"], "a": ["united breweries", "ubl"]},

    # --- PHARMA & HEALTHCARE ---
    {"s": "SUNPHARMA", "n": "Sun Pharmaceutical Industries Ltd", "isin": "INE044A01036", "sec": "Pharma", "type": "EQUITY", "cap": 440000, "idx": ["NIFTY50", "NIFTYPHARMA"], "a": ["sun pharma", "sun pharmaceutical"]},
    {"s": "CIPLA", "n": "Cipla Ltd", "isin": "INE059A01026", "sec": "Pharma", "type": "EQUITY", "cap": 128000, "idx": ["NIFTY50", "NIFTYPHARMA"], "a": ["cipla"]},
    {"s": "DRREDDY", "n": "Dr. Reddy's Laboratories Ltd", "isin": "INE089A01031", "sec": "Pharma", "type": "EQUITY", "cap": 108000, "idx": ["NIFTY50", "NIFTYPHARMA"], "a": ["dr reddy", "dr reddys", "dr. reddy's"]},
    {"s": "DIVISLAB", "n": "Divi's Laboratories Ltd", "isin": "INE361B01024", "sec": "Pharma", "type": "EQUITY", "cap": 152000, "idx": ["NIFTYNEXT50", "NIFTYPHARMA"], "a": ["divis", "divi's lab"]},
    {"s": "LUPIN", "n": "Lupin Ltd", "isin": "INE326A01037", "sec": "Pharma", "type": "EQUITY", "cap": 96000, "idx": ["NIFTYPHARMA"], "a": ["lupin"]},
    {"s": "AUROPHARMA", "n": "Aurobindo Pharma Ltd", "isin": "INE406A01037", "sec": "Pharma", "type": "EQUITY", "cap": 78000, "idx": ["NIFTYPHARMA"], "a": ["aurobindo", "aurobindo pharma"]},
    {"s": "TORNTPHARM", "n": "Torrent Pharmaceuticals Ltd", "isin": "INE685A01028", "sec": "Pharma", "type": "EQUITY", "cap": 112000, "idx": ["NIFTYNEXT50", "NIFTYPHARMA"], "a": ["torrent pharma"]},
    {"s": "APOLLOHOSP", "n": "Apollo Hospitals Enterprise Ltd", "isin": "INE437A01024", "sec": "Pharma", "type": "EQUITY", "cap": 98000, "idx": ["NIFTY50"], "a": ["apollo hospitals", "apollo"]},
    {"s": "MAXHEALTH", "n": "Max Healthcare Institute Ltd", "isin": "INE027H01010", "sec": "Pharma", "type": "EQUITY", "cap": 96000, "idx": ["NIFTYNEXT50"], "a": ["max healthcare", "max health"]},
    {"s": "ZYDUSLIFE", "n": "Zydus Lifesciences Ltd", "isin": "INE010B01027", "sec": "Pharma", "type": "EQUITY", "cap": 105000, "idx": ["NIFTYNEXT50", "NIFTYPHARMA"], "a": ["zydus", "zydus life"]},

    # --- INFRA, CAPITAL GOODS & CEMENT ---
    {"s": "LT", "n": "Larsen & Toubro Ltd", "isin": "INE018A01030", "sec": "Infra", "type": "EQUITY", "cap": 495000, "idx": ["NIFTY50"], "a": ["l&t", "larsen", "larsen & toubro", "larsen and toubro"]},
    {"s": "ULTRACEMCO", "n": "UltraTech Cement Ltd", "isin": "INE481G01011", "sec": "Infra", "type": "EQUITY", "cap": 335000, "idx": ["NIFTY50"], "a": ["ultratech", "ultratech cement"]},
    {"s": "GRASIM", "n": "Grasim Industries Ltd", "isin": "INE047A01021", "sec": "Infra", "type": "EQUITY", "cap": 175000, "idx": ["NIFTY50"], "a": ["grasim"]},
    {"s": "ADANIENT", "n": "Adani Enterprises Ltd", "isin": "INE423A01024", "sec": "Infra", "type": "EQUITY", "cap": 325000, "idx": ["NIFTY50"], "a": ["adani enterprises", "adani"]},
    {"s": "ADANIPORTS", "n": "Adani Ports & SEZ Ltd", "isin": "INE742F01042", "sec": "Infra", "type": "EQUITY", "cap": 295000, "idx": ["NIFTY50"], "a": ["adani ports"]},
    {"s": "AMBUJACEM", "n": "Ambuja Cements Ltd", "isin": "INE079A01024", "sec": "Infra", "type": "EQUITY", "cap": 145000, "idx": ["NIFTYNEXT50"], "a": ["ambuja", "ambuja cement"]},
    {"s": "SHREECEM", "n": "Shree Cement Ltd", "isin": "INE070A01015", "sec": "Infra", "type": "EQUITY", "cap": 94000, "idx": ["NIFTYNEXT50"], "a": ["shree cement"]},
    {"s": "SIEMENS", "n": "Siemens Ltd", "isin": "INE003A01024", "sec": "Infra", "type": "EQUITY", "cap": 245000, "idx": ["NIFTYNEXT50"], "a": ["siemens india", "siemens"]},
    {"s": "ABB", "n": "ABB India Ltd", "isin": "INE117A01022", "sec": "Infra", "type": "EQUITY", "cap": 162000, "idx": ["NIFTYNEXT50"], "a": ["abb india", "abb"]},
    {"s": "HAL", "n": "Hindustan Aeronautics Ltd", "isin": "INE066F01020", "sec": "Infra", "type": "EQUITY", "cap": 295000, "idx": ["NIFTYNEXT50"], "a": ["hal", "hindustan aeronautics"]},
    {"s": "BEL", "n": "Bharat Electronics Ltd", "isin": "INE263A01024", "sec": "Infra", "type": "EQUITY", "cap": 215000, "idx": ["NIFTY50"], "a": ["bel", "bharat electronics"]},
    {"s": "BHEL", "n": "Bharat Heavy Electricals Ltd", "isin": "INE257A01026", "sec": "Infra", "type": "EQUITY", "cap": 86000, "idx": ["NIFTYMIDCAP"], "a": ["bhel"]},
    {"s": "CUMMINSIND", "n": "Cummins India Ltd", "isin": "INE298A01020", "sec": "Infra", "type": "EQUITY", "cap": 94000, "idx": ["NIFTYMIDCAP"], "a": ["cummins", "cummins india"]},
    {"s": "CGPOWER", "n": "CG Power & Industrial Solutions", "isin": "INE067A01029", "sec": "Infra", "type": "EQUITY", "cap": 110000, "idx": ["NIFTYNEXT50"], "a": ["cg power"]},
    {"s": "DLF", "n": "DLF Ltd", "isin": "INE271C01023", "sec": "Infra", "type": "EQUITY", "cap": 205000, "idx": ["NIFTYNEXT50"], "a": ["dlf"]},
    {"s": "GODREJPROP", "n": "Godrej Properties Ltd", "isin": "INE484J01027", "sec": "Infra", "type": "EQUITY", "cap": 78000, "idx": ["NIFTYMIDCAP"], "a": ["godrej properties"]},

    # --- METALS & MINING ---
    {"s": "TATASTEEL", "n": "Tata Steel Ltd", "isin": "INE081A01020", "sec": "Metals", "type": "EQUITY", "cap": 192000, "idx": ["NIFTY50", "NIFTYMETAL"], "a": ["tata steel"]},
    {"s": "JSWSTEEL", "n": "JSW Steel Ltd", "isin": "INE019A01038", "sec": "Metals", "type": "EQUITY", "cap": 238000, "idx": ["NIFTY50", "NIFTYMETAL"], "a": ["jsw steel", "jsw"]},
    {"s": "HINDALCO", "n": "Hindalco Industries Ltd", "isin": "INE038A01020", "sec": "Metals", "type": "EQUITY", "cap": 154000, "idx": ["NIFTY50", "NIFTYMETAL"], "a": ["hindalco"]},
    {"s": "VEDL", "n": "Vedanta Ltd", "isin": "INE205A01025", "sec": "Metals", "type": "EQUITY", "cap": 178000, "idx": ["NIFTYNEXT50", "NIFTYMETAL"], "a": ["vedanta"]},
    {"s": "JINDALSTEL", "n": "Jindal Steel & Power Ltd", "isin": "INE749A01030", "sec": "Metals", "type": "EQUITY", "cap": 98000, "idx": ["NIFTYNEXT50", "NIFTYMETAL"], "a": ["jindal steel", "jspl"]},
    {"s": "NMDC", "n": "NMDC Ltd", "isin": "INE584A01023", "sec": "Metals", "type": "EQUITY", "cap": 68000, "idx": ["NIFTYMETAL"], "a": ["nmdc"]},
    {"s": "SAIL", "n": "Steel Authority of India Ltd", "isin": "INE114A01011", "sec": "Metals", "type": "EQUITY", "cap": 52000, "idx": ["NIFTYMETAL"], "a": ["sail", "steel authority"]},
    {"s": "HINDZINC", "n": "Hindustan Zinc Ltd", "isin": "INE267A01025", "sec": "Metals", "type": "EQUITY", "cap": 215000, "idx": ["NIFTYMETAL"], "a": ["hindustan zinc"]},

    # --- POWER & UTILITIES ---
    {"s": "NTPC", "n": "NTPC Ltd", "isin": "INE733E01010", "sec": "Power", "type": "EQUITY", "cap": 395000, "idx": ["NIFTY50"], "a": ["ntpc"]},
    {"s": "POWERGRID", "n": "Power Grid Corporation of India", "isin": "INE752E01010", "sec": "Power", "type": "EQUITY", "cap": 305000, "idx": ["NIFTY50"], "a": ["power grid", "powergrid"]},
    {"s": "TATAPOWER", "n": "Tata Power Company Ltd", "isin": "INE245A01021", "sec": "Power", "type": "EQUITY", "cap": 138000, "idx": ["NIFTYNEXT50"], "a": ["tata power"]},
    {"s": "ADANIPOWER", "n": "Adani Power Ltd", "isin": "INE814H01011", "sec": "Power", "type": "EQUITY", "cap": 235000, "idx": ["NIFTYNEXT50"], "a": ["adani power"]},
    {"s": "ADANIGREEN", "n": "Adani Green Energy Ltd", "isin": "INE364U01010", "sec": "Power", "type": "EQUITY", "cap": 245000, "idx": ["NIFTYNEXT50"], "a": ["adani green"]},
    {"s": "JSWENERGY", "n": "JSW Energy Ltd", "isin": "INE121E01018", "sec": "Power", "type": "EQUITY", "cap": 115000, "idx": ["NIFTYNEXT50"], "a": ["jsw energy"]},
    {"s": "NHPC", "n": "NHPC Ltd", "isin": "INE848E01016", "sec": "Power", "type": "EQUITY", "cap": 88000, "idx": ["NIFTYMIDCAP"], "a": ["nhpc"]},

    # --- TELECOM, CONSUMER & TECH ---
    {"s": "BHARTIARTL", "n": "Bharti Airtel Ltd", "isin": "INE397D01024", "sec": "Telecom", "type": "EQUITY", "cap": 945000, "idx": ["NIFTY50"], "a": ["airtel", "bharti airtel", "bharti"]},
    {"s": "INDUSTOWER", "n": "Indus Towers Ltd", "isin": "INE121J01017", "sec": "Telecom", "type": "EQUITY", "cap": 96000, "idx": ["NIFTYMIDCAP"], "a": ["indus towers"]},
    {"s": "IDEA", "n": "Vodafone Idea Ltd", "isin": "INE669E01016", "sec": "Telecom", "type": "EQUITY", "cap": 62000, "idx": ["NIFTYMIDCAP"], "a": ["vodafone idea", "vi"]},
    {"s": "TITAN", "n": "Titan Company Ltd", "isin": "INE280A01028", "sec": "Consumer", "type": "EQUITY", "cap": 310000, "idx": ["NIFTY50"], "a": ["titan", "tanishq"]},
    {"s": "DMART", "n": "Avenue Supermarts Ltd", "isin": "INE192R01011", "sec": "Consumer", "type": "EQUITY", "cap": 265000, "idx": ["NIFTYNEXT50"], "a": ["dmart", "d-mart", "avenue supermarts"]},
    {"s": "TRENT", "n": "Trent Ltd", "isin": "INE849A01020", "sec": "Consumer", "type": "EQUITY", "cap": 245000, "idx": ["NIFTY50"], "a": ["trent", "zudio", "westside"]},
    {"s": "ZOMATO", "n": "Zomato Ltd (Eternal)", "isin": "INE758T01015", "sec": "Consumer", "type": "EQUITY", "cap": 225000, "idx": ["NIFTYNEXT50"], "a": ["zomato", "blinkit", "eternal"]},
    {"s": "NAUKRI", "n": "Info Edge (India) Ltd", "isin": "INE663F01024", "sec": "Consumer", "type": "EQUITY", "cap": 102000, "idx": ["NIFTYNEXT50"], "a": ["info edge", "naukri"]},
    {"s": "ASIANPAINT", "n": "Asian Paints Ltd", "isin": "INE021A01026", "sec": "Consumer", "type": "EQUITY", "cap": 260000, "idx": ["NIFTY50"], "a": ["asian paints"]},
    {"s": "PIDILITIND", "n": "Pidilite Industries Ltd", "isin": "INE318A01026", "sec": "Consumer", "type": "EQUITY", "cap": 158000, "idx": ["NIFTYNEXT50"], "a": ["pidilite", "fevicol"]},
    {"s": "HAVELLS", "n": "Havells India Ltd", "isin": "INE176B01034", "sec": "Consumer", "type": "EQUITY", "cap": 112000, "idx": ["NIFTYNEXT50"], "a": ["havells"]},
    {"s": "INDIGO", "n": "InterGlobe Aviation Ltd", "isin": "INE646L01027", "sec": "Consumer", "type": "EQUITY", "cap": 175000, "idx": ["NIFTYNEXT50"], "a": ["indigo", "interglobe aviation"]},
    {"s": "INDHOTEL", "n": "Indian Hotels Company Ltd", "isin": "INE053A01029", "sec": "Consumer", "type": "EQUITY", "cap": 108000, "idx": ["NIFTYMIDCAP"], "a": ["indian hotels", "taj hotels"]},
    {"s": "DIXON", "n": "Dixon Technologies (India) Ltd", "isin": "INE935N01020", "sec": "Consumer", "type": "EQUITY", "cap": 94000, "idx": ["NIFTYMIDCAP"], "a": ["dixon", "dixon tech"]},
    {"s": "POLYCAB", "n": "Polycab India Ltd", "isin": "INE455K01017", "sec": "Infra", "type": "EQUITY", "cap": 102000, "idx": ["NIFTYMIDCAP"], "a": ["polycab"]},
    {"s": "SRF", "n": "SRF Ltd", "isin": "INE647A01010", "sec": "Chemicals", "type": "EQUITY", "cap": 74000, "idx": ["NIFTYMIDCAP"], "a": ["srf"]},
    {"s": "PIIND", "n": "PI Industries Ltd", "isin": "INE603J01030", "sec": "Chemicals", "type": "EQUITY", "cap": 64000, "idx": ["NIFTYMIDCAP"], "a": ["pi industries"]},
    {"s": "UPL", "n": "UPL Ltd", "isin": "INE628A01036", "sec": "Chemicals", "type": "EQUITY", "cap": 42000, "idx": ["NIFTYMIDCAP"], "a": ["upl"]},

    # --- MUTUAL FUNDS (with AMFI Scheme Codes & AMC) ---
    {"s": "MF-FLEXI", "n": "Parag Parikh Flexi Cap Fund (Direct Growth)", "isin": "INF879O01027", "scheme_code": "122639", "amc": "PPFAS Mutual Fund", "sec": "Equity Fund", "type": "MUTUAL_FUND", "cap": 82000, "idx": [], "a": ["flexi cap", "ppfas", "parag parikh flexi cap"]},
    {"s": "MF-SMALL", "n": "Nippon India Small Cap Fund (Direct Growth)", "isin": "INF204K01K15", "scheme_code": "118778", "amc": "Nippon India Mutual Fund", "sec": "Equity Fund", "type": "MUTUAL_FUND", "cap": 61000, "idx": [], "a": ["small cap fund", "nippon small cap"]},
    {"s": "MF-BAF", "n": "ICICI Prudential Balanced Advantage Fund (Direct)", "isin": "INF109K012B0", "scheme_code": "120377", "amc": "ICICI Prudential Mutual Fund", "sec": "Hybrid Fund", "type": "MUTUAL_FUND", "cap": 58000, "idx": [], "a": ["balanced advantage", "baf", "icici baf"]},
    {"s": "MF-DEBT", "n": "HDFC Short Term Debt Fund (Direct Growth)", "isin": "INF179K01YM1", "scheme_code": "119016", "amc": "HDFC Mutual Fund", "sec": "Debt Fund", "type": "MUTUAL_FUND", "cap": 15000, "idx": [], "a": ["debt fund", "short duration", "hdfc short term debt"]},
    {"s": "MF-MID", "n": "HDFC Mid-Cap Opportunities Fund (Direct)", "isin": "INF179K01XQ0", "scheme_code": "118989", "amc": "HDFC Mutual Fund", "sec": "Equity Fund", "type": "MUTUAL_FUND", "cap": 74000, "idx": [], "a": ["hdfc midcap", "mid cap fund"]},
    {"s": "MF-LARGE", "n": "Mirae Asset Large Cap Fund (Direct)", "isin": "INF769K01AX2", "scheme_code": "118825", "amc": "Mirae Asset Mutual Fund", "sec": "Equity Fund", "type": "MUTUAL_FUND", "cap": 39000, "idx": [], "a": ["mirae large cap", "large cap fund"]},
    {"s": "MF-ELSS", "n": "Quant ELSS Tax Saver Fund (Direct)", "isin": "INF966L01986", "scheme_code": "120847", "amc": "Quant Mutual Fund", "sec": "Equity Fund", "type": "MUTUAL_FUND", "cap": 11000, "idx": [], "a": ["quant elss", "elss", "tax saver fund"]},
    {"s": "MF-LIQUID", "n": "SBI Liquid Fund (Direct Growth)", "isin": "INF200K01UT4", "scheme_code": "119800", "amc": "SBI Mutual Fund", "sec": "Debt Fund", "type": "MUTUAL_FUND", "cap": 65000, "idx": [], "a": ["sbi liquid", "liquid fund"]},
    {"s": "MF-GILT", "n": "SBI Magnum Gilt Fund (Direct Growth)", "isin": "INF200K01980", "scheme_code": "119716", "amc": "SBI Mutual Fund", "sec": "Debt Fund", "type": "MUTUAL_FUND", "cap": 9500, "idx": [], "a": ["gilt fund", "sbi gilt"]},
    {"s": "MF-CONRA", "n": "SBI Contra Fund (Direct Growth)", "isin": "INF200K01RA0", "scheme_code": "119835", "amc": "SBI Mutual Fund", "sec": "Equity Fund", "type": "MUTUAL_FUND", "cap": 38000, "idx": [], "a": ["sbi contra", "contra fund"]},
    {"s": "MF-INDEX", "n": "UTI Nifty 50 Index Fund (Direct Growth)", "isin": "INF789F01XA0", "scheme_code": "120716", "amc": "UTI Mutual Fund", "sec": "Equity Fund", "type": "MUTUAL_FUND", "cap": 21000, "idx": ["NIFTY50"], "a": ["uti nifty", "nifty index fund"]},

    # --- ETFs & INDICES ---
    {"s": "NIFTYBEES", "n": "Nippon India ETF Nifty 50 BeES", "isin": "INF204KB14I2", "sec": "Equity Fund", "type": "ETF", "cap": 32000, "idx": ["NIFTY50"], "a": ["niftybees", "nifty bees"]},
    {"s": "BANKBEES", "n": "Nippon India ETF Bank BeES", "isin": "INF204KB15I9", "sec": "Equity Fund", "type": "ETF", "cap": 8500, "idx": ["BANKNIFTY"], "a": ["bankbees", "bank bees"]},
    {"s": "GOLDBEES", "n": "Nippon India ETF Gold BeES", "isin": "INF204KB17I5", "sec": "Commodity", "type": "ETF", "cap": 13500, "idx": [], "a": ["goldbees", "gold etf"]},
    {"s": "NIFTY50", "n": "NSE Nifty 50 Index", "isin": "IDX-NIFTY50", "sec": "Market Index", "type": "INDEX", "cap": 0, "idx": ["NIFTY50"], "a": ["nifty", "nifty 50", "nifty50"]},
    {"s": "BANKNIFTY", "n": "NSE Nifty Bank Index", "isin": "IDX-BANKNIFTY", "sec": "Banking", "type": "INDEX", "cap": 0, "idx": ["BANKNIFTY"], "a": ["bank nifty", "banknifty"]},
]

# Add additional Nifty Next 50 / Midcap equities to reach ~200 coverage depth (§09)
_EXTRA_EQUITIES = [
    ("PIDILITIND2", "Astral Ltd", "INE006I01046", "Infra", 48000, ["astral"]),
    ("ASTRAL", "Astral Pipes Ltd", "INE006I01046", "Infra", 48000, ["astral pipes"]),
    ("VOLTAS", "Voltas Ltd", "INE226A01021", "Consumer", 56000, ["voltas"]),
    ("BERGEPAINT", "Berger Paints India Ltd", "INE463A01038", "Consumer", 58000, ["berger paints"]),
    ("PAGEIND", "Page Industries Ltd", "INE761H01022", "Consumer", 51000, ["page industries", "jockey india"]),
    ("JUBLFOOD", "Jubilant FoodWorks Ltd", "INE797F01020", "Consumer", 43000, ["jubilant foodworks", "dominos india"]),
    ("SWIGGY", "Swiggy Ltd", "INE00H001014", "Consumer", 98000, ["swiggy", "instamart"]),
    ("PAYTM", "One 97 Communications Ltd", "INE982J01020", "NBFC", 55000, ["paytm", "one97"]),
    ("POLICYBZR", "PB Fintech Ltd", "INE417T01026", "NBFC", 78000, ["policybazaar", "pb fintech"]),
    ("NYKAA", "FSN E-Commerce Ventures Ltd", "INE388Y01029", "Consumer", 52000, ["nykaa"]),
    ("DELHIVERY", "Delhivery Ltd", "INE148O01028", "Infra", 28000, ["delhivery"]),
    ("IRCTC", "Indian Railway Catering & Tourism Corp", "INE335Y01020", "Consumer", 68000, ["irctc"]),
    ("RVNL", "Rail Vikas Nigam Ltd", "INE415G01027", "Infra", 92000, ["rvnl", "rail vikas"]),
    ("IRFC", "Indian Railway Finance Corporation", "INE053F01010", "NBFC", 195000, ["irfc"]),
    ("MAZDOCK", "Mazagon Dock Shipbuilders Ltd", "INE249Z01012", "Infra", 92000, ["mazagon dock", "mazdock"]),
    ("COCHINSHIP", "Cochin Shipyard Ltd", "INE704P01025", "Infra", 44000, ["cochin shipyard"]),
    ("SUZLON", "Suzlon Energy Ltd", "INE040H01021", "Power", 84000, ["suzlon"]),
    ("IREDA", "Indian Renewable Energy Development Agency", "INE202E01016", "NBFC", 56000, ["ireda"]),
    ("TATAINVEST", "Tata Investment Corporation Ltd", "INE672A01018", "NBFC", 35000, ["tata investment"]),
    ("TATACOMM", "Tata Communications Ltd", "INE151A01013", "Telecom", 52000, ["tata comm", "tata communications"]),
    ("TATACHEM", "Tata Chemicals Ltd", "INE092A01019", "Chemicals", 28000, ["tata chemicals"]),
    ("DEEPAKNTR", "Deepak Nitrite Ltd", "INE288B01029", "Chemicals", 37000, ["deepak nitrite"]),
    ("ATUL", "Atul Ltd", "INE100A01010", "Chemicals", 22000, ["atul ltd"]),
    ("NAVINFLUOR", "Navin Fluorine International Ltd", "INE048G01026", "Chemicals", 18000, ["navin fluorine"]),
    ("ALKEM", "Alkem Laboratories Ltd", "INE540L01014", "Pharma", 68000, ["alkem"]),
    ("BIOCON", "Biocon Ltd", "INE376G01013", "Pharma", 42000, ["biocon"]),
    ("GLAND", "Gland Pharma Ltd", "INE068V01023", "Pharma", 29000, ["gland pharma"]),
    ("LAURUSLABS", "Laurus Labs Ltd", "INE947Q01028", "Pharma", 28000, ["laurus labs"]),
    ("LALPATHLAB", "Dr. Lal PathLabs Ltd", "INE600L01024", "Pharma", 26000, ["lal pathlabs"]),
    ("FORTIS", "Fortis Healthcare Ltd", "INE061F01013", "Pharma", 49000, ["fortis"]),
    ("MANKIND", "Mankind Pharma Ltd", "INE634S01028", "Pharma", 104000, ["mankind pharma"]),
    ("OBEROIRLTY", "Oberoi Realty Ltd", "INE093I01010", "Infra", 72000, ["oberoi realty"]),
    ("PRESTIGE", "Prestige Estates Projects Ltd", "INE811K01011", "Infra", 71000, ["prestige estates"]),
    ("PHOENIXLTD", "The Phoenix Mills Ltd", "INE211B01039", "Infra", 58000, ["phoenix mills"]),
    ("LODHA", "Macrotech Developers Ltd", "INE670K01029", "Infra", 122000, ["lodha", "macrotech"]),
    ("KALYANKJIL", "Kalyan Jewellers India Ltd", "INE303R01014", "Consumer", 68000, ["kalyan jewellers"]),
    ("PATANJALI", "Patanjali Foods Ltd", "INE619A01035", "FMCG", 64000, ["patanjali"]),
    ("RADICO", "Radico Khaitan Ltd", "INE944F01028", "FMCG", 28000, ["radico khaitan"]),
    ("UNITDSPR", "United Spirits Ltd", "INE854D01024", "FMCG", 108000, ["united spirits", "mcdowell"]),
    ("EMAMILTD", "Emami Ltd", "INE548C01032", "FMCG", 29000, ["emami"]),
    ("PGHH", "Procter & Gamble Hygiene & Health Care", "INE179A01014", "FMCG", 52000, ["p&g hygiene", "pghh"]),
    ("ESCORTS", "Escorts Kubota Ltd", "INE042A01014", "Auto", 41000, ["escorts kubota", "escorts"]),
    ("BALKRISIND", "Balkrishna Industries Ltd", "INE787D01026", "Auto", 54000, ["balkrishna", "bkt"]),
    ("APOLLOTYRE", "Apollo Tyres Ltd", "INE438A01022", "Auto", 32000, ["apollo tyres"]),
    ("EXIDEIND", "Exide Industries Ltd", "INE302A01020", "Auto", 38000, ["exide"]),
    ("AMARAJABAT", "Amara Raja Energy & Mobility", "INE885A01032", "Auto", 24000, ["amara raja"]),
    ("SONACOMS", "Sona BLW Precision Forgings", "INE073K01018", "Auto", 41000, ["sona blw", "sona comstar"]),
    ("UNOMINDA", "Uno Minda Ltd", "INE405E01023", "Auto", 58000, ["uno minda"]),
    ("TIINDIA", "Tube Investments of India", "INE974X01010", "Auto", 74000, ["tube investments"]),
    ("BOSCHLTD", "Bosch Ltd", "INE323A01026", "Auto", 98000, ["bosch india"]),
    ("CUMMINS", "SKF India Ltd", "INE640A01023", "Infra", 26000, ["skf india"]),
    ("THERMAX", "Thermax Ltd", "INE152A01029", "Infra", 56000, ["thermax"]),
    ("TIMKEN", "Timken India Ltd", "INE325A01013", "Infra", 25000, ["timken"]),
    ("SOLARINDS", "Solar Industries India Ltd", "INE343H01029", "Chemicals", 92000, ["solar industries"]),
    ("APLAPOLLO", "APL Apollo Tubes Ltd", "INE702C01027", "Metals", 42000, ["apl apollo"]),
    ("NATIONALUM", "National Aluminium Company Ltd", "INE139A01034", "Metals", 41000, ["nalco"]),
    ("RATNAMANI", "Ratnamani Metals & Tubes", "INE703B01027", "Metals", 24000, ["ratnamani"]),
    ("TORNTPOWER", "Torrent Power Ltd", "INE813H01021", "Power", 82000, ["torrent power"]),
    ("CESC", "CESC Ltd", "INE486A01021", "Power", 24000, ["cesc"]),
    ("SJVN", "SJVN Ltd", "INE002L01015", "Power", 46000, ["sjvn"]),
    ("OIL", "Oil India Ltd", "INE274J01014", "Energy", 82000, ["oil india"]),
    ("MGL", "Mahanagar Gas Ltd", "INE002S01010", "Energy", 15000, ["mgl", "mahanagar gas"]),
    ("GUJGASLTD", "Gujarat Gas Ltd", "INE844O01030", "Energy", 38000, ["gujarat gas"]),
    ("ATGL", "Adani Total Gas Ltd", "INE399L01023", "Energy", 84000, ["adani total gas"]),
    ("AWL", "Adani Wilmar Ltd", "INE699H01024", "FMCG", 44000, ["adani wilmar"]),
    ("HDFCAMC", "HDFC Asset Management Company", "INE127D01025", "NBFC", 94000, ["hdfc amc"]),
    ("NAM-INDIA", "Nippon Life India Asset Management", "INE298J01013", "NBFC", 44000, ["nippon amc", "nam india"]),
    ("CAMS", "Computer Age Management Services", "INE596I01012", "NBFC", 22000, ["cams"]),
    ("KFINTECH", "KFin Technologies Ltd", "INE138Y01010", "NBFC", 18000, ["kfintech"]),
    ("BSE", "BSE Ltd", "INE118H01025", "NBFC", 62000, ["bse ltd", "bombay stock exchange"]),
    ("MCX", "Multi Commodity Exchange of India", "INE745G01035", "NBFC", 31000, ["mcx"]),
    ("ANGELONE", "Angel One Ltd", "INE732I01013", "NBFC", 26000, ["angel one"]),
    ("360ONE", "360 ONE WAM Ltd", "INE466L01038", "NBFC", 41000, ["360 one", "iifl wealth"]),
    ("OFSS", "Oracle Financial Services Software", "INE881D01027", "IT", 98000, ["ofss", "oracle financial"]),
    ("LTTS", "L&T Technology Services Ltd", "INE010V01017", "IT", 54000, ["ltts"]),
    ("CYIENT", "Cyient Ltd", "INE136B01020", "IT", 21000, ["cyient"]),
    ("SONATSOFTW", "Sonata Software Ltd", "INE269A01021", "IT", 18000, ["sonata software"]),
    ("NAZARA", "Nazara Technologies Ltd", "INE418L01021", "Consumer", 8000, ["nazara"]),
    ("KAYNES", "Kaynes Technology India Ltd", "INE918Z01012", "Consumer", 36000, ["kaynes"]),
    ("SYRMA", "Syrma SGS Technology Ltd", "INE0DYJ01015", "Consumer", 9500, ["syrma"]),
    ("CONCOR", "Container Corporation of India", "INE111A01025", "Infra", 52000, ["concor"]),
    ("GMRINFRA", "GMR Airports Infrastructure Ltd", "INE776C01039", "Infra", 88000, ["gmr airports", "gmr"]),
    ("DALBHARAT", "Dalmia Bharat Ltd", "INE00R701025", "Infra", 34000, ["dalmia bharat"]),
    ("JKCEMENT", "JK Cement Ltd", "INE823G01014", "Infra", 34000, ["jk cement"]),
    ("RAMCOCEM", "The Ramco Cements Ltd", "INE331A01037", "Infra", 21000, ["ramco cements"]),
    ("ACC", "ACC Ltd", "INE012A01025", "Infra", 44000, ["acc cement", "acc"]),
    ("BANDHANBNK", "Bandhan Bank Ltd", "INE545U01014", "Banking", 30000, ["bandhan bank"]),
    ("RBLBANK", "RBL Bank Ltd", "INE976G01028", "Banking", 11000, ["rbl bank"]),
    ("KARURVYSYA", "Karur Vysya Bank Ltd", "INE036D01028", "Banking", 18000, ["kvb", "karur vysya"]),
    ("CUB", "City Union Bank Ltd", "INE491A01021", "Banking", 12000, ["city union bank"]),
    ("UNIONBANK", "Union Bank of India", "INE692A01016", "Banking", 92000, ["union bank"]),
    ("INDIANB", "Indian Bank", "INE562A01011", "Banking", 76000, ["indian bank"]),
    ("BANKINDIA", "Bank of India", "INE084A01016", "Banking", 48000, ["bank of india"]),
    ("MF-ELSS2", "Mirae Asset ELSS Tax Saver Fund (Direct)", "INF769K01DM9", "Equity Fund", 24000, ["mirae elss"]),
    ("MF-SMALL2", "SBI Small Cap Fund (Direct Growth)", "INF200K01T51", "Equity Fund", 32000, ["sbi small cap"]),
    ("MF-HYBRID", "HDFC Balanced Advantage Fund (Direct)", "INF179K01WN9", "Hybrid Fund", 92000, ["hdfc baf", "hdfc balanced advantage"]),
]

for sym, name, isin, sec, cap, aliases in _EXTRA_EQUITIES:
    if sym not in {i["s"] for i in INSTRUMENTS}:
        inst_type = "MUTUAL_FUND" if sym.startswith("MF-") else "EQUITY"
        INSTRUMENTS.append({
            "s": sym, "n": name, "isin": isin, "sec": sec,
            "type": inst_type, "cap": cap, "idx": [], "a": aliases
        })

BY_SYMBOL: Dict[str, Dict] = {i["s"]: i for i in INSTRUMENTS}
BY_ISIN: Dict[str, Dict] = {i["isin"]: i for i in INSTRUMENTS if i.get("isin")}
BY_SCHEME: Dict[str, Dict] = {i["scheme_code"]: i for i in INSTRUMENTS if i.get("scheme_code")}

SECTOR_MEMBERS: Dict[str, List[str]] = {}
for _inst in INSTRUMENTS:
    SECTOR_MEMBERS.setdefault(_inst["sec"], []).append(_inst["s"])


def search_instruments(query: str, limit: int = 10) -> List[Dict]:
    """Alias-aware instrument search — L3 entity linking surfaced to UI."""
    q = query.strip().lower()
    if len(q) < 1:
        return []
    scored = []
    for inst in INSTRUMENTS:
        score = 0
        if inst["s"].lower() == q or (inst.get("isin", "").lower() == q):
            score = 100
        elif inst["s"].lower().startswith(q):
            score = 80
        elif any(alias == q for alias in inst.get("a", [])):
            score = 75
        elif q in inst["n"].lower():
            score = 60
        elif any(q in alias for alias in inst.get("a", [])):
            score = 50
        elif q in inst["s"].lower() or q in inst["sec"].lower():
            score = 30
        if score > 0:
            scored.append((score, inst))
    scored.sort(key=lambda x: (-x[0], -x[1].get("cap", 0)))
    return [x[1] for x in scored[:limit]]
