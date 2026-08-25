import api from "./client";

export async function scanUrl(url) {
  const cleaned = url.trim();

  // Dot na ho to ye domain hai hi nahi
  if (!cleaned.includes(".")) {
    throw new Error("Please enter a valid URL (e.g. example.com)");
  }

  const fullUrl = /^https?:\/\//i.test(cleaned) ? cleaned : `http://${cleaned}`;

  const res = await api.post("/api/v1/scan/url", { url: fullUrl });
  return res.data;
}

export async function getHistory() {
  const res = await api.get("/api/v1/scan/history");
  return res.data;
}