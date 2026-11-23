"use client";

import { useEffect, useState } from "react";
import { feedzApi } from "../lib/api";

export default function HomePage() {
  const [userId, setUserId] = useState("investor_a");
  const [tab, setTab] = useState("feed");
  const [feedData, setFeedData] = useState(null);
  const [mood, setMood] = useState(null);
  const [brief, setBrief] = useState(null);
  const [askQ, setAskQ] = useState("");
  const [askRes, setAskRes] = useState(null);
  const [whyMap, setWhyMap] = useState({});
  const [drillSymbol, setDrillSymbol] = useState(null);
  const [drillData, setDrillData] = useState(null);
  const [error, setError] = useState(null);

  const loadAll = async (uid) => {
    try {
      setError(null);
      const [f, m] = await Promise.all([feedzApi.getFeed(uid), feedzApi.getMarketMood()]);
      setFeedData(f);
      setMood(m);
      setBrief(null);
      setWhyMap({});
    } catch (e) {
      setError(e.message);
    }
  };

  useEffect(() => {
    loadAll(userId);
  }, [userId]);

  const handleWhy = async (articleId) => {
    const res = await feedzApi.whyThisMatters(userId, articleId);
    setWhyMap((prev) => ({ ...prev, [articleId]: res }));
  };

  const handleDrill = async (symbol) => {
    setDrillSymbol(symbol);
    const data = await feedzApi.getEntityMood(symbol);
    setDrillData(data);
  };

  const handleBrief = async () => {
    setBrief(await feedzApi.dailyBrief(userId));
  };

  const handleAsk = async (e) => {
    e.preventDefault();
    if (!askQ.trim()) return;
    setAskRes(await feedzApi.askFeed(userId, askQ));
  };

  return (
    <div className="min-h-screen flex flex-col md:flex-row">
      <nav className="w-full md:w-56 bg-[#18232E] border-b md:border-b-0 md:border-r border-[#2C3E4E] p-4 flex md:flex-col gap-2">
        <div className="font-bold text-xl tracking-tight mb-2">
          feed<span className="text-[#F0B429]">z</span>
        </div>
        {["feed", "brief", "mood", "portfolio", "ask"].map((k) => (
          <button
            key={k}
            onClick={() => setTab(k)}
            className={`text-left px-3 py-2 rounded-lg text-sm capitalize ${
              tab === k ? "bg-[#20303E] text-[#E9EEF3] font-semibold" : "text-[#93A6B6]"
            }`}
          >
            {k}
          </button>
        ))}
        <div className="md:mt-auto pt-3 border-t border-[#2C3E4E]">
          <div className="text-[10px] uppercase tracking-widest text-[#61758A] mb-2">Active Persona</div>
          <select
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            className="w-full bg-[#101820] border border-[#2C3E4E] rounded px-2 py-1.5 text-xs"
          >
            <option value="investor_a">Investor A (P1 · Fund-heavy)</option>
            <option value="investor_b">Investor B (P1 · Trader)</option>
            <option value="mfd_advisor">Lark MFD Desk (P2 · Client Book)</option>
          </select>
        </div>
      </nav>

      <main className="flex-1 p-6 max-w-4xl">
        {error && <div className="p-3 mb-4 rounded bg-red-900/30 border border-red-500/40 text-sm">{error}</div>}

        {tab === "feed" && feedData && (
          <div className="space-y-4">
            <div className="flex items-baseline justify-between">
              <h1 className="text-2xl font-semibold">Ranked by what it touches</h1>
              <span className="text-xs text-[#61758A]">{feedData.count} stories · {feedData.mode}</span>
            </div>
            {feedData.items.map((item) => (
              <article key={item.id} className="flex gap-3 bg-[#18232E] border border-[#2C3E4E] rounded-xl p-4">
                <div className="w-1 bg-[#2C3E4E] rounded relative overflow-hidden flex-none">
                  <div
                    className="absolute bottom-0 left-0 right-0 bg-[#F0B429]"
                    style={{ height: `${Math.min(100, Math.max(item.exposure_pct > 0 ? 10 : 0, item.exposure_pct * 100))}%` }}
                  />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex flex-wrap gap-2 text-xs text-[#61758A] mb-1">
                    <span className="uppercase px-1.5 py-0.5 rounded border border-[#2C3E4E]">{item.source_category}</span>
                    <span>{item.source_name}</span>
                    {item.exposure_pct > 0 && (
                      <span className="px-1.5 py-0.5 rounded bg-[#F0B429]/15 text-[#F0B429] border border-[#F0B429]/40">
                        {Math.round(item.exposure_pct * 100)}% of portfolio
                      </span>
                    )}
                    <span className="ml-auto font-mono">{item.sentiment.polarity.toFixed(2)}</span>
                  </div>
                  <h2 className="text-lg font-medium">{item.headline}</h2>
                  <p className="text-sm text-[#93A6B6] mt-1">{item.summary}</p>
                  <div className="mt-3 flex gap-2">
                    <button
                      onClick={() => handleWhy(item.id)}
                      className="px-3 py-1 rounded bg-[#F0B429] text-[#1A1206] text-xs font-semibold"
                    >
                      Why this matters to me
                    </button>
                  </div>
                  {whyMap[item.id] && (
                    <div className="mt-3 p-3 rounded-lg bg-[#F0B429]/10 border border-[#F0B429]/30 text-sm">
                      {whyMap[item.id].insight}
                    </div>
                  )}
                </div>
              </article>
            ))}
          </div>
        )}

        {tab === "mood" && mood && (
          <div className="space-y-4">
            <h1 className="text-2xl font-semibold">Market Mood Index: {mood.index} / 100</h1>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {[
                ["Polarity (40%)", `${((mood.polarity + 1) * 50).toFixed(0)}`],
                ["Breadth (25%)", `${(mood.breadth * 100).toFixed(0)}%`],
                ["Momentum (20%)", `${(mood.momentum * 100).toFixed(0)}`],
                ["Dispersion (15%)", `${(mood.dispersion * 100).toFixed(0)}%`],
              ].map(([k, v]) => (
                <div key={k} className="bg-[#18232E] border border-[#2C3E4E] rounded-xl p-3">
                  <div className="text-xs text-[#61758A]">{k}</div>
                  <div className="text-xl font-mono font-semibold mt-1">{v}</div>
                </div>
              ))}
            </div>
            <div className="bg-[#18232E] border border-[#2C3E4E] rounded-xl p-4">
              <div className="text-xs uppercase tracking-widest text-[#61758A] mb-3">Click any instrument to drill down to constituent articles</div>
              <div className="flex flex-wrap gap-2">
                {Object.values(mood.entity_scores).slice(0, 20).map((e) => (
                  <button
                    key={e.symbol}
                    onClick={() => handleDrill(e.symbol)}
                    className="px-2.5 py-1 rounded border border-[#2C3E4E] text-xs hover:border-[#F0B429]"
                  >
                    {e.symbol} ({e.score >= 0 ? "+" : ""}{e.score.toFixed(2)})
                  </button>
                ))}
              </div>
              {drillData && (
                <div className="mt-4 pt-4 border-t border-[#2C3E4E]">
                  <div className="font-semibold mb-2">{drillData.name} ({drillData.symbol}) — {drillData.contributors.length} constituent articles</div>
                  {drillData.contributors.map((c) => (
                    <div key={c.article_id} className="text-xs text-[#93A6B6] py-1 border-b border-[#2C3E4E]/50">
                      [{c.source_name}] {c.headline} · polarity {c.polarity.toFixed(2)} · weight {c.weight.toFixed(3)}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {tab === "brief" && (
          <div className="space-y-4">
            <h1 className="text-2xl font-semibold">Morning Brief</h1>
            <button onClick={handleBrief} className="px-4 py-2 rounded bg-[#F0B429] text-[#1A1206] text-sm font-semibold">
              Generate Brief
            </button>
            {brief && (
              <div className="bg-[#18232E] border border-[#2C3E4E] rounded-xl p-5 space-y-3">
                <div className="text-lg font-medium">{brief.line}</div>
                <div className="text-sm text-[#93A6B6] border-l-2 border-[#F0B429] pl-3">{brief.divergence}</div>
                {brief.themes.map((t, i) => (
                  <div key={i} className="pt-2 border-t border-[#2C3E4E]">
                    <div className="font-semibold text-sm">{t.title}</div>
                    <div className="text-sm text-[#93A6B6]">{t.detail}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {tab === "ask" && (
          <div className="space-y-4">
            <h1 className="text-2xl font-semibold">Ask Your Feed</h1>
            <form onSubmit={handleAsk} className="flex gap-2">
              <input
                value={askQ}
                onChange={(e) => setAskQ(e.target.value)}
                placeholder="Ask about your portfolio and today's feed..."
                className="flex-1 bg-[#18232E] border border-[#2C3E4E] rounded px-3 py-2 text-sm"
              />
              <button type="submit" className="px-4 py-2 rounded bg-[#F0B429] text-[#1A1206] text-sm font-semibold">Ask</button>
            </form>
            {askRes && (
              <div className="bg-[#18232E] border border-[#2C3E4E] rounded-xl p-4 text-sm space-y-2">
                <div>{askRes.answer}</div>
                <div className="text-xs text-[#61758A]">{askRes.disclosure}</div>
              </div>
            )}
          </div>
        )}

        {tab === "portfolio" && feedData?.portfolio_mood && (
          <div className="space-y-4">
            <h1 className="text-2xl font-semibold">Portfolio Sentiment: {feedData.portfolio_mood.score.toFixed(2)}</h1>
            <div className="text-sm text-[#93A6B6]">Coverage: {feedData.portfolio_mood.coverage_pct}% of portfolio weight</div>
            {feedData.portfolio_mood.breakdown.map((b) => (
              <div key={b.symbol} className="flex justify-between bg-[#18232E] border border-[#2C3E4E] rounded-lg p-3 text-sm">
                <span>{b.name} ({b.weight_pct}%)</span>
                <span className="font-mono">{b.score.toFixed(2)} ({b.contributors_count} stories)</span>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
