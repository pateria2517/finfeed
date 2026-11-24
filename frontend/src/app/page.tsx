"use client";

import { useEffect, useState, type FormEvent } from "react";
import {
  BarChart3,
  BriefcaseBusiness,
  LayoutDashboard,
  LogOut,
  Search,
  TrendingUp,
  Upload,
} from "lucide-react";
import { feedzApi } from "../lib/api";

const heroPhoto =
  "https://cdn.21st.dev/assets/mirror/ea/ea9270b3b7246283219ac52fa77a1213e9d1efb285d76348d3620609ba6cefa7.jpg";

type Tab = "feed" | "mood" | "portfolio" | "brief";

export default function FeedzPage() {
  const [authenticated, setAuthenticated] = useState(false);
  const [checkingSession, setCheckingSession] = useState(true);
  const [authMode, setAuthMode] = useState<"login" | "register">("login");
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [tab, setTab] = useState<Tab>("feed");
  const [feedData, setFeedData] = useState<any>(null);
  const [mood, setMood] = useState<any>(null);
  const [me, setMe] = useState<any>(null);
  const [brief, setBrief] = useState<any>(null);
  const [whyMap, setWhyMap] = useState<Record<number, string>>({});
  const [askQ, setAskQ] = useState("");
  const [askRes, setAskRes] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [instrumentQuery, setInstrumentQuery] = useState("");
  const [instrumentResults, setInstrumentResults] = useState<any[]>([]);
  const [portfolioWeight, setPortfolioWeight] = useState("10");
  const [taxonomy, setTaxonomy] = useState<any>(null);

  useEffect(() => {
    const token = window.localStorage.getItem("feedz-access-token");
    if (!token) {
      setCheckingSession(false);
      return;
    }
    feedzApi
      .getMe()
      .then((user) => {
        setMe(user);
        setAuthenticated(true);
      })
      .catch(() => window.localStorage.removeItem("feedz-access-token"))
      .finally(() => setCheckingSession(false));
  }, []);

  useEffect(() => {
    if (!authenticated) return;
    setError(null);
    Promise.all([feedzApi.getMe(), feedzApi.getFeed(), feedzApi.getMarketMood(), feedzApi.getTaxonomy()])
      .then(([user, feed, marketMood, taxonomyData]) => {
        setMe(user);
        setFeedData(feed);
        setMood(marketMood);
        setTaxonomy(taxonomyData);
        setBrief(null);
        setWhyMap({});
      })
      .catch((err: Error) => setError(err.message));
  }, [authenticated]);

  const submitAuth = async (event: FormEvent) => {
    event.preventDefault();
    try {
      setError(null);
      const result =
        authMode === "register"
          ? await feedzApi.register(identifier, password, name)
          : await feedzApi.login(identifier, password);
      window.localStorage.setItem("feedz-access-token", result.access_token);
      setMe(result.user);
      setAuthenticated(true);
    } catch (err: any) {
      setError(err.message);
    }
  };

  const logout = () => {
    window.localStorage.removeItem("feedz-access-token");
    setAuthenticated(false);
    setFeedData(null);
    setMood(null);
    setMe(null);
  };

  const handleWhy = async (articleId: number) => {
    try {
      setError(null);
      const response = await feedzApi.whyThisMatters(articleId);
      setWhyMap((current) => ({ ...current, [articleId]: response.insight }));
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleFeedback = async (articleId: number, vote: "up" | "down") => {
    try {
      await feedzApi.recordFeedback(articleId, vote);
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleBrief = async () => {
    try {
      setError(null);
      setBrief(await feedzApi.dailyBrief());
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleAsk = async (event: FormEvent) => {
    event.preventDefault();
    if (!askQ.trim()) return;
    try {
      setError(null);
      setAskRes(await feedzApi.askFeed(askQ));
    } catch (err: any) {
      setError(err.message);
    }
  };

  const searchInstruments = async (event: FormEvent) => {
    event.preventDefault();
    if (!instrumentQuery.trim()) return;
    try {
      setError(null);
      const response = await feedzApi.searchInstruments(instrumentQuery);
      setInstrumentResults(response.results || []);
    } catch (err: any) {
      setError(err.message);
    }
  };

  const addHolding = async (symbol: string) => {
    const weight = Number(portfolioWeight);
    if (!Number.isFinite(weight) || weight <= 0 || weight > 100) {
      setError("Weight must be greater than zero and no more than 100.");
      return;
    }
    try {
      setError(null);
      await feedzApi.addHolding({ symbol, weight });
      const [user, feed] = await Promise.all([feedzApi.getMe(), feedzApi.getFeed()]);
      setMe(user);
      setFeedData(feed);
    } catch (err: any) {
      setError(err.message);
    }
  };

  const importCsv = async (file?: File) => {
    if (!file) return;
    try {
      setError(null);
      await feedzApi.importCsv(file);
      const [user, feed] = await Promise.all([feedzApi.getMe(), feedzApi.getFeed()]);
      setMe(user);
      setFeedData(feed);
    } catch (err: any) {
      setError(err.message);
    }
  };

  const savePreferences = async (event: FormEvent) => {
    event.preventDefault();
    if (!me) return;
    try {
      setError(null);
      const interests: Record<string, number> = {};
      const form = new FormData(event.currentTarget as HTMLFormElement);
      taxonomyTopics.forEach((topic: string) => {
        if (form.has(`topic-${topic}`)) interests[topic] = 1;
      });
      const result = await feedzApi.saveOnboarding({
        name: me.name,
        mode: me.mode || "P1_RETAIL",
        persona: me.persona,
        interests,
        holdings: (me.holdings || []).map((holding: any) => ({
          symbol: holding.s,
          weight: holding.w,
          quantity: holding.qty,
          avg_price: holding.avg_price,
        })),
      });
      setMe(result.profile);
    } catch (err: any) {
      setError(err.message);
    }
  };

  if (checkingSession) {
    return <main className="landing-shell" aria-label="Loading Feedz" />;
  }

  const taxonomyTopics =
    taxonomy?.taxonomy?.flatMap((group: any) => group.children || [group.label]) || [];

  if (!authenticated) {
    return (
      <main className="landing-shell">
        <nav className="landing-nav" aria-label="Primary navigation">
          <div className="brand-mark">
            <span className="brand-glyph">FZ</span>
            <span>FEEDZ</span>
          </div>
          <div className="nav-links">
            <a href="#features">Intelligence</a>
            <a href="#process">How it works</a>
            <a href="#account">Account</a>
          </div>
        </nav>

        <section className="hero enter-reveal">
          <div className="hero-copy">
            <div className="hero-kicker">FINANCIAL INTELLIGENCE FOR PEOPLE WHO HOLD</div>
            <div>
              <h1>Read what moves your money.</h1>
              <p className="hero-subcopy">
                Live market context shaped around your portfolio, interests, and point of view.
              </p>
              <a className="primary-button" href="#account">
                Open your feed
              </a>
            </div>
          </div>
          <div className="hero-media">
            <img src={heroPhoto} alt="Editorial view of a modern investment workspace" />
            <div className="media-caption">
              <span>01 / SIGNAL</span>
              <span>Less noise. Better context.</span>
            </div>
          </div>
        </section>

        <section id="features" className="feature-section">
          <div className="feature-inner">
            <div className="feature-head">
              <h2>Your portfolio has a point of view.</h2>
              <p>
                Feedz ranks public news by relevance, market evidence, and the holdings you choose.
              </p>
            </div>
            <div className="feature-grid">
              <article className="feature-cell">
                <h3>One signal feed, ranked for you.</h3>
                <div className="signal-line" aria-hidden="true">
                  {[34, 54, 42, 76, 62, 92, 70, 48].map((height, index) => (
                    <i key={index} style={{ height: `${height}%` }} />
                  ))}
                </div>
              </article>
              <article className="feature-cell">
                <h3>Market mood.</h3>
                <p>Track the direction of current public market signals.</p>
              </article>
              <article className="feature-cell">
                <h3>Plain-language context.</h3>
                <p>Ask how a story connects to the assets you hold.</p>
              </article>
            </div>
          </div>
        </section>

        <section id="process" className="process-section">
          <div className="process-inner">
            <h2>From headline to context.</h2>
            <div className="process-list">
              <article className="process-item">
                <strong>01</strong>
                <h3>Set your account</h3>
                <p>Create a private account and choose how you read the market.</p>
              </article>
              <article className="process-item">
                <strong>02</strong>
                <h3>Add holdings</h3>
                <p>Search instruments manually or import a portfolio CSV.</p>
              </article>
              <article className="process-item">
                <strong>03</strong>
                <h3>Read with context</h3>
                <p>Get ranked public news, mood, briefs, and guarded AI answers.</p>
              </article>
            </div>
          </div>
        </section>

        <section id="account" className="account-section">
          <div className="account-inner">
            <form className="auth-card" onSubmit={submitAuth}>
              <div className="auth-tabs" role="tablist" aria-label="Account access">
                <button
                  type="button"
                  role="tab"
                  aria-selected={authMode === "login"}
                  className={`auth-tab ${authMode === "login" ? "active" : ""}`}
                  onClick={() => {
                    setAuthMode("login");
                    setError(null);
                  }}
                >
                  Sign in
                </button>
                <button
                  type="button"
                  role="tab"
                  aria-selected={authMode === "register"}
                  className={`auth-tab ${authMode === "register" ? "active" : ""}`}
                  onClick={() => {
                    setAuthMode("register");
                    setError(null);
                  }}
                >
                  Create account
                </button>
              </div>
              {authMode === "register" && (
                <div className="auth-field">
                  <label htmlFor="name">Name</label>
                  <input id="name" value={name} onChange={(event) => setName(event.target.value)} required maxLength={100} />
                </div>
              )}
              <div className="auth-field">
                <label htmlFor="identifier">Email or phone</label>
                <input
                  id="identifier"
                  value={identifier}
                  onChange={(event) => setIdentifier(event.target.value)}
                  required
                  minLength={3}
                  maxLength={320}
                  autoComplete="username"
                />
              </div>
              <div className="auth-field">
                <label htmlFor="password">Password</label>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  required
                  minLength={8}
                  maxLength={128}
                  autoComplete={authMode === "login" ? "current-password" : "new-password"}
                />
              </div>
              {error && <p className="auth-error" role="alert">{error}</p>}
              <button type="submit" className="primary-button">
                {authMode === "login" ? "Sign in" : "Create account"}
              </button>
            </form>
            <div className="account-copy">
              <h2>Build your own market lens.</h2>
              <p>
                Your account keeps your holdings and preferences private. News ingestion is limited to configured public sources.
              </p>
            </div>
          </div>
        </section>
      </main>
    );
  }

  const nav = [
    { id: "feed" as const, label: "Feed", icon: LayoutDashboard },
    { id: "mood" as const, label: "Market Mood", icon: TrendingUp },
    { id: "portfolio" as const, label: "Portfolio", icon: BarChart3 },
    { id: "brief" as const, label: "Brief and Ask", icon: BriefcaseBusiness },
  ];

  return (
    <main className="app-shell">
      <header className="app-nav">
        <div className="brand-mark">
          <span className="brand-glyph">FZ</span>
          <span>FEEDZ</span>
        </div>
        <div className="app-nav-actions">
          <button className="icon-button" type="button" aria-label="Log out" onClick={logout}>
            <LogOut size={18} />
          </button>
        </div>
      </header>

      <div className="app-layout">
        <nav className="app-rail" aria-label="App sections">
          {nav.map(({ id, label, icon: Icon }) => (
            <button
              type="button"
              key={id}
              className={tab === id ? "active" : ""}
              onClick={() => setTab(id)}
              aria-current={tab === id ? "page" : undefined}
            >
              <Icon size={17} />
              <span>{label}</span>
            </button>
          ))}
        </nav>

        <section className="app-main enter-reveal" key={tab}>
          {error && <div className="app-error" role="alert">{error}</div>}

          {tab === "feed" && feedData && (
            <>
              <div className="app-heading">
                <h1>Ranked by what it touches.</h1>
                {mood && (
                  <div className="mood-chip">
                    <span>Market mood</span>
                    <strong>{mood.index}</strong>
                  </div>
                )}
              </div>
              <div className="story-list">
                {feedData.items.map((item: any, index: number) => (
                  <article className="story-card" key={item.id}>
                    <span className="story-index">{String(index + 1).padStart(2, "0")}</span>
                    <div>
                      <h2>{item.headline}</h2>
                      <p>{item.summary}</p>
                    </div>
                    <button className="story-action" type="button" onClick={() => handleWhy(item.id)}>
                      Why it matters
                    </button>
                    {whyMap[item.id] && <div className="why-answer">{whyMap[item.id]}</div>}
                    <button
                      className="story-action"
                      type="button"
                      onClick={() => handleFeedback(item.id, "up")}
                      aria-label="Mark this story relevant"
                    >
                      Relevant
                    </button>
                  </article>
                ))}
              </div>
            </>
          )}

          {tab === "mood" && mood && (
            <>
              <div className="app-heading">
                <h1>Market mood</h1>
                <div className="mood-chip">
                  <span>Current index</span>
                  <strong>{mood.index}</strong>
                </div>
              </div>
              <div className="mood-grid">
                <div className="metric-cell"><span>Polarity</span><strong>{mood.polarity.toFixed(2)}</strong></div>
                <div className="metric-cell"><span>Breadth</span><strong>{Math.round(mood.breadth * 100)}%</strong></div>
                <div className="metric-cell"><span>Momentum</span><strong>{Math.round(mood.momentum * 100)}%</strong></div>
                <div className="metric-cell"><span>Dispersion</span><strong>{Math.round(mood.dispersion * 100)}%</strong></div>
              </div>
            </>
          )}

          {tab === "portfolio" && me && (
            <>
              <div className="app-heading">
                <h1>Your portfolio lens.</h1>
                {feedData?.portfolio_mood && (
                  <div className="mood-chip">
                    <span>Portfolio mood</span>
                    <strong>{feedData.portfolio_mood.score.toFixed(2)}</strong>
                  </div>
                )}
              </div>
              <div className="portfolio-grid">
                <div className="metric-cell">
                  <span>Manual holding</span>
                  <form className="ask-form" onSubmit={searchInstruments} style={{ marginTop: 24 }}>
                    <input
                      value={instrumentQuery}
                      onChange={(event) => setInstrumentQuery(event.target.value)}
                      placeholder="Search symbol or name"
                      aria-label="Search instruments"
                    />
                    <button className="story-action" type="submit" aria-label="Search instruments"><Search size={16} /></button>
                  </form>
                  <div style={{ marginTop: 8 }}>
                    <label htmlFor="weight" style={{ fontSize: 12, fontWeight: 800 }}>Weight percent</label>
                    <input
                      id="weight"
                      className="auth-field"
                      type="number"
                      min="0.01"
                      max="100"
                      step="0.01"
                      value={portfolioWeight}
                      onChange={(event) => setPortfolioWeight(event.target.value)}
                    />
                  </div>
                  {instrumentResults.map((instrument: any) => (
                    <button
                      className="story-action"
                      type="button"
                      key={instrument.symbol}
                      onClick={() => addHolding(instrument.symbol)}
                      style={{ margin: "6px 6px 0 0" }}
                    >
                      {instrument.symbol} · {instrument.name}
                    </button>
                  ))}
                </div>
                <div className="metric-cell">
                  <span>Import CSV</span>
                  <label className="story-action" style={{ display: "inline-flex", alignItems: "center", gap: 8, marginTop: 24, cursor: "pointer" }}>
                    <Upload size={16} />
                    Choose file
                    <input
                      type="file"
                      accept=".csv,text/csv"
                      onChange={(event) => importCsv(event.target.files?.[0])}
                      style={{ position: "absolute", opacity: 0, width: 1, height: 1 }}
                    />
                  </label>
                </div>
                {(me.holdings || []).map((holding: any) => (
                  <div className="portfolio-row" key={holding.s}>
                    <span>{holding.s}</span>
                    <strong>{holding.w}%</strong>
                  </div>
                ))}
              </div>

              {taxonomyTopics.length > 0 && (
                <form className="brief-panel" onSubmit={savePreferences} style={{ marginTop: 12 }}>
                  <div className="metric-cell" style={{ minHeight: 120 }}>
                    <span>Interests</span>
                    <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginTop: 20 }}>
                      {taxonomyTopics.map((topic: string) => (
                        <label key={topic} className="story-action" style={{ display: "inline-flex", alignItems: "center" }}>
                          <input
                            type="checkbox"
                            name={`topic-${topic}`}
                            defaultChecked={Boolean(me.interests?.[topic])}
                            style={{ marginRight: 7 }}
                          />
                          {topic}
                        </label>
                      ))}
                    </div>
                  </div>
                  <button type="submit" className="primary-button" style={{ width: "fit-content" }}>
                    Save preferences
                  </button>
                </form>
              )}
            </>
          )}

          {tab === "brief" && (
            <>
              <div className="app-heading">
                <h1>Brief and ask.</h1>
              </div>
              <div className="brief-panel">
                <button className="primary-button" type="button" onClick={handleBrief} style={{ width: "fit-content" }}>
                  Generate daily brief
                </button>
                {brief && (
                  <div className="brief-output">
                    <strong>{brief.line}</strong>
                    {brief.divergence && <p>{brief.divergence}</p>}
                  </div>
                )}
                <form className="ask-form" onSubmit={handleAsk}>
                  <input
                    value={askQ}
                    onChange={(event) => setAskQ(event.target.value)}
                    placeholder="Ask about your portfolio or the current feed"
                    maxLength={500}
                  />
                  <button className="primary-button" type="submit">Ask Feedz</button>
                </form>
                {askRes && <div className="ask-output">{askRes.answer}</div>}
              </div>
            </>
          )}
        </section>
      </div>
    </main>
  );
}
