"use client";

import { useEffect, useState, type CSSProperties } from "react";
import { feedzApi } from "../lib/api";
import { Bell, BarChart3, BriefcaseBusiness, LayoutDashboard, Moon, Sun, TrendingUp } from "lucide-react";

const studioPhoto = "https://cdn.21st.dev/assets/mirror/ea/ea9270b3b7246283219ac52fa77a1213e9d1efb285d76348d3620609ba6cefa7.jpg";

export default function FeedzGlassyPage() {
  const [userId, setUserId] = useState("investor_a");
  const [tab, setTab] = useState<"feed" | "mood" | "portfolio" | "brief">("feed");
  const [theme, setTheme] = useState<"light" | "dark">("light");
  const [feedData, setFeedData] = useState<any>(null);
  const [mood, setMood] = useState<any>(null);
  const [brief, setBrief] = useState<any>(null);
  const [whyMap, setWhyMap] = useState<Record<number, string>>({});
  const [askQ, setAskQ] = useState("");
  const [askRes, setAskRes] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const storedTheme = window.localStorage.getItem("feedz-theme");
    if (storedTheme === "light" || storedTheme === "dark") {
      setTheme(storedTheme);
    } else if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
      setTheme("dark");
    }
  }, []);

  useEffect(() => {
    const root = document.documentElement;
    root.classList.toggle("dark", theme === "dark");
    root.dataset.theme = theme;
    root.style.colorScheme = theme;
    window.localStorage.setItem("feedz-theme", theme);
  }, [theme]);

  useEffect(() => {
    (async () => {
      try {
        setError(null);
        const [f, m] = await Promise.all([feedzApi.getFeed(userId), feedzApi.getMarketMood()]);
        setFeedData(f);
        setMood(m);
        setBrief(null);
        setWhyMap({});
      } catch (e: any) {
        setError(e.message);
      }
    })();
  }, [userId]);

  const handleWhy = async (id: number) => {
    const res = await feedzApi.whyThisMatters(userId, id);
    setWhyMap((p) => ({ ...p, [id]: res.insight }));
  };

  const handleBrief = async () => setBrief(await feedzApi.dailyBrief(userId));

  const handleAsk = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!askQ.trim()) return;
    setAskRes(await feedzApi.askFeed(userId, askQ));
  };

  const nav = [
    { id: "feed", label: "Feed", icon: LayoutDashboard },
    { id: "mood", label: "Market Mood", icon: TrendingUp },
    { id: "portfolio", label: "Portfolio", icon: BarChart3 },
    { id: "brief", label: "Brief & Ask", icon: BriefcaseBusiness },
  ] as const;

  return (
    <div
      className="min-h-screen relative isolate font-sans text-[13px]"
      style={{
        background: theme === "dark" ? "#40322b" : "#ab8e76",
        color: theme === "dark" ? "#fff6e9" : "#25201e",
      } as CSSProperties}
    >
      <img
        src={studioPhoto}
        alt=""
        aria-hidden="true"
        className="fixed inset-0 w-full h-full object-cover -z-20 pointer-events-none"
        style={{ filter: theme === "dark" ? "sepia(.15) saturate(.75) brightness(.61)" : "sepia(.22) saturate(.78) brightness(.86)" }}
      />
      <div className="max-w-[1340px] mx-auto px-4 md:px-10 py-5 pb-24">
        <header className="grid grid-cols-[1fr_auto] items-center gap-3 min-h-[58px] rounded-full px-3 py-1.5 border border-white/40 backdrop-blur-xl bg-white/30 dark:bg-black/30 shadow-lg">
          <div className="flex items-center gap-2.5 pl-1">
            <span className="w-9 h-9 rounded-full grid place-items-center bg-[#fff9f3] text-[#241b17] font-extrabold text-sm shadow">Fz</span>
            <div>
              <strong className="block text-xs tracking-[0.17em] font-extrabold">FEEDZ</strong>
              <small className="block text-[10px] opacity-75">Financial Intelligence</small>
            </div>
          </div>
          <div className="flex items-center justify-end gap-2">
            <select
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              className="h-9 rounded-full px-3 text-xs font-semibold bg-white/40 text-[#25201e] border border-black/15"
            >
              <option value="investor_a">Investor A (P1)</option>
              <option value="investor_b">Investor B (P1)</option>
              <option value="mfd_advisor">Lark MFD (P2)</option>
            </select>
            <button
              type="button"
              onClick={() => setTheme(theme === "light" ? "dark" : "light")}
              className="w-10 h-10 rounded-full grid place-items-center border border-black/15 bg-white/30"
              aria-label="Toggle theme"
            >
              {theme === "light" ? <Moon className="w-4 h-4" /> : <Sun className="w-4 h-4" />}
            </button>
            <button
              type="button"
              onClick={() => setTab("mood")}
              className="w-10 h-10 rounded-full grid place-items-center border border-black/15 bg-white/40"
              aria-label="Market Mood"
            >
              <Bell className="w-4 h-4" />
            </button>
          </div>
        </header>

        <div className="relative mt-3">
          <main className="rounded-[32px] border border-white/40 backdrop-blur-md bg-[#f7eadb]/35 dark:bg-[#2a1f1d]/55 shadow-2xl p-5 md:p-9 min-h-[600px]">
            {error && <div className="p-3 mb-4 rounded-xl bg-red-500/20 border border-red-500/40 text-xs">{error}</div>}

            {tab === "feed" && feedData && (
              <div className="space-y-4">
                <div className="flex items-end justify-between">
                  <div>
                    <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight">Ranked by what it touches</h1>
                    <p className="text-xs opacity-75 mt-1">{feedData.count} stories · {feedData.mode}</p>
                  </div>
                  {mood && (
                    <div className="px-4 py-2 rounded-2xl bg-[#1e7461] text-white text-right shadow">
                      <div className="text-[10px] uppercase tracking-wider opacity-80">Market Mood</div>
                      <div className="text-xl font-extrabold">{mood.index} / 100</div>
                    </div>
                  )}
                </div>
                <div className="grid gap-3">
                  {feedData.items.map((item: any) => (
                    <article key={item.id} className="flex gap-3 rounded-2xl border border-white/45 bg-white/45 dark:bg-black/30 p-4 shadow-sm">
                      <div className="w-1.5 rounded-full bg-black/10 relative overflow-hidden flex-none">
                        <div className="absolute bottom-0 left-0 right-0 bg-[#09644f]" style={{ height: `${Math.min(100, Math.max(item.exposure_pct > 0 ? 12 : 0, item.exposure_pct * 100))}%` }} />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex flex-wrap items-center gap-2 text-[11px] opacity-75 mb-1">
                          <span className="uppercase font-bold px-2 py-0.5 rounded-full bg-black/10">{item.source_category}</span>
                          <span>{item.source_name}</span>
                          {item.exposure_pct > 0 && (
                            <span className="px-2 py-0.5 rounded-full bg-[#09644f]/15 text-[#09644f] dark:text-[#75dac0] font-bold">
                              {Math.round(item.exposure_pct * 100)}% of portfolio
                            </span>
                          )}
                          <span className="ml-auto font-mono font-bold">{item.sentiment.polarity.toFixed(2)}</span>
                        </div>
                        <h2 className="text-base font-bold">{item.headline}</h2>
                        <p className="text-xs opacity-80 mt-1">{item.summary}</p>
                        <button onClick={() => handleWhy(item.id)} className="mt-2.5 px-3 py-1.5 rounded-full bg-[#261e1b] text-[#fffaf5] text-[11px] font-bold">
                          Why this matters to me
                        </button>
                        {whyMap[item.id] && <div className="mt-2.5 p-3 rounded-xl bg-white/60 dark:bg-black/35 border border-black/10 text-xs">{whyMap[item.id]}</div>}
                      </div>
                    </article>
                  ))}
                </div>
              </div>
            )}

            {tab === "mood" && mood && (
              <div className="space-y-4">
                <h1 className="text-3xl font-extrabold tracking-tight">Market Mood: {mood.index} / 100</h1>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {[
                    ["Polarity (40%)", ((mood.polarity + 1) * 50).toFixed(0)],
                    ["Breadth (25%)", `${(mood.breadth * 100).toFixed(0)}%`],
                    ["Momentum (20%)", `${(mood.momentum * 100).toFixed(0)}%`],
                    ["Dispersion (15%)", `${(mood.dispersion * 100).toFixed(0)}%`],
                  ].map(([k, v], i) => (
                    <div key={k} className={`rounded-2xl p-4 border border-white/40 ${i === 0 ? "bg-[#1e7461] text-white" : "bg-white/45 dark:bg-black/30"}`}>
                      <div className="text-xs opacity-80">{k}</div>
                      <div className="text-2xl font-extrabold mt-1">{v}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {tab === "portfolio" && feedData?.portfolio_mood && (
              <div className="space-y-4">
                <h1 className="text-3xl font-extrabold tracking-tight">Portfolio Sentiment: {feedData.portfolio_mood.score.toFixed(2)}</h1>
                <div className="grid gap-2">
                  {feedData.portfolio_mood.breakdown.map((b: any) => (
                    <div key={b.symbol} className="flex justify-between rounded-2xl border border-white/40 bg-white/45 dark:bg-black/30 p-3.5 text-xs font-semibold">
                      <span>{b.name} ({b.weight_pct}%)</span>
                      <span className="font-mono">{b.score.toFixed(2)} · {b.contributors_count} stories</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {tab === "brief" && (
              <div className="space-y-5">
                <h1 className="text-3xl font-extrabold tracking-tight">Morning Brief & Ask Feedz</h1>
                <button onClick={handleBrief} className="px-4 py-2 rounded-full bg-[#261e1b] text-[#fffaf5] text-xs font-bold">
                  Generate Morning Brief
                </button>
                {brief && (
                  <div className="rounded-2xl border border-white/40 bg-white/50 dark:bg-black/35 p-5 space-y-3">
                    <div className="text-base font-bold">{brief.line}</div>
                    <div className="text-xs opacity-80">{brief.divergence}</div>
                  </div>
                )}
                <form onSubmit={handleAsk} className="flex gap-2">
                  <input value={askQ} onChange={(e) => setAskQ(e.target.value)} placeholder="Ask about your portfolio and feed..." className="flex-1 rounded-full px-4 py-2 text-xs bg-white/60 text-[#25201e] border border-black/15" />
                  <button type="submit" className="px-4 py-2 rounded-full bg-[#261e1b] text-[#fffaf5] text-xs font-bold">Ask</button>
                </form>
                {askRes && <div className="rounded-2xl border border-white/40 bg-white/50 dark:bg-black/35 p-4 text-xs">{askRes.answer}</div>}
              </div>
            )}
          </main>

          <nav className="fixed bottom-4 left-1/2 -translate-x-1/2 z-30 flex items-center gap-1 p-1.5 rounded-full border border-white/50 backdrop-blur-xl bg-[#f1dece]/75 dark:bg-[#2d201e]/80 shadow-xl">
            {nav.map(({ id, label, icon: Icon }) => (
              <button
                key={id}
                type="button"
                onClick={() => setTab(id)}
                className={`flex items-center gap-1.5 px-4 py-2 rounded-full text-xs font-extrabold transition ${
                  tab === id ? "bg-[#fff9f3] text-[#241b17] shadow" : "opacity-80 hover:opacity-100"
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{label}</span>
              </button>
            ))}
          </nav>
        </div>
      </div>
    </div>
  );
}
