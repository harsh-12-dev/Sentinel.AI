import api from "./client";

export async function scanUrl(url) {
  // Log aksar scheme ke bina URL paste karte hain
  const cleaned = url.trim();
  const fullUrl = /^https?:\/\//i.test(cleaned) ? cleaned : `http://${cleaned}`;

  const res = await api.post("/api/v1/scan/url", { url: fullUrl });
  return res.data;
}

export async function getHistory() {
  const res = await api.get("/api/v1/scan/history");
  return res.data;
}