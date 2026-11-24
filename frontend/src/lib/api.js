const BASE = (process.env.NEXT_PUBLIC_API_URL || "").replace(/\/$/, "");

async function request(path, options = {}) {
  const token = typeof window !== "undefined" ? window.localStorage.getItem("feedz-access-token") : null;
  let res;
  try {
    res = await fetch(`${BASE}${path}`, {
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...(options.headers || {}),
      },
      ...options,
    });
  } catch {
    throw new Error(`Unable to reach the Feedz server. Confirm the frontend and API are running, and NEXT_PUBLIC_API_URL points to the API.`);
  }
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || `Request failed (${res.status})`);
  }
  return res.json();
}

export const feedzApi = {
  register: (identifier, password, name) =>
    request("/api/auth/register", {
      method: "POST",
      body: JSON.stringify({ identifier, password, name }),
    }),
  login: (identifier, password) =>
    request("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ identifier, password }),
    }),
  getMe: () => request("/api/me"),
  getTaxonomy: () => request("/api/taxonomy"),
  searchInstruments: (q) => request(`/api/instruments/search?q=${encodeURIComponent(q)}`),
  saveOnboarding: (payload) => request("/api/onboarding", { method: "POST", body: JSON.stringify(payload) }),
  getFeed: () => request("/api/feed"),
  compareFeeds: () => request("/api/feed/compare"),
  getMarketMood: () => request("/api/mood"),
  getEntityMood: (symbol) => request(`/api/mood/entity/${encodeURIComponent(symbol)}`),
  addHolding: (holding) =>
    request("/api/portfolio/holding", {
      method: "POST",
      body: JSON.stringify(holding),
    }),
  importCsv: async (file) => {
    const form = new FormData();
    form.append("file", file);
    const token = typeof window !== "undefined" ? window.localStorage.getItem("feedz-access-token") : null;
    const res = await fetch(`${BASE}/api/portfolio/import-csv`, {
      method: "POST",
      body: form,
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
  whyThisMatters: (articleId) =>
    request("/api/ai/why", { method: "POST", body: JSON.stringify({ article_id: articleId }) }),
  dailyBrief: () =>
    request("/api/ai/brief", { method: "POST", body: JSON.stringify({}) }),
  askFeed: (question) =>
    request("/api/ai/ask", { method: "POST", body: JSON.stringify({ question }) }),
  recordFeedback: (articleId, vote) =>
    request("/api/feedback", { method: "POST", body: JSON.stringify({ article_id: articleId, vote }) }),
  getAudit: () => request("/api/ingest/audit"),
};
