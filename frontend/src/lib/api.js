"""Typed API client for Feedz FastAPI backend."""

const BASE = process.env.NEXT_PUBLIC_API_URL || "";

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || `Request failed (${res.status})`);
  }
  return res.json();
}

export const feedzApi = {
  getTaxonomy: () => request("/api/taxonomy"),
  searchInstruments: (q) => request(`/api/instruments/search?q=${encodeURIComponent(q)}`),
  saveOnboarding: (payload) => request("/api/onboarding", { method: "POST", body: JSON.stringify(payload) }),
  getFeed: (userId) => request(`/api/feed?user_id=${encodeURIComponent(userId)}`),
  compareFeeds: (userA = "investor_a", userB = "investor_b") =>
    request(`/api/feed/compare?user_a=${userA}&user_b=${userB}`),
  getMarketMood: () => request("/api/mood"),
  getEntityMood: (symbol) => request(`/api/mood/entity/${encodeURIComponent(symbol)}`),
  addHolding: (userId, holding) =>
    request(`/api/portfolio/${encodeURIComponent(userId)}/holding`, {
      method: "POST",
      body: JSON.stringify(holding),
    }),
  importCsv: async (userId, file) => {
    const form = new FormData();
    form.append("file", file);
    const res = await fetch(`${BASE}/api/portfolio/${encodeURIComponent(userId)}/import-csv`, {
      method: "POST",
      body: form,
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
  whyThisMatters: (userId, articleId) =>
    request("/api/ai/why", { method: "POST", body: JSON.stringify({ user_id: userId, article_id: articleId }) }),
  dailyBrief: (userId) =>
    request("/api/ai/brief", { method: "POST", body: JSON.stringify({ user_id: userId }) }),
  askFeed: (userId, question) =>
    request("/api/ai/ask", { method: "POST", body: JSON.stringify({ user_id: userId, question }) }),
  recordFeedback: (userId, articleId, vote) =>
    request("/api/feedback", { method: "POST", body: JSON.stringify({ user_id: userId, article_id: articleId, vote }) }),
  getAudit: () => request("/api/ingest/audit"),
};
