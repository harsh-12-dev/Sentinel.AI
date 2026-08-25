import api from "./client";

export async function scanUrl(url) {
  const res = await api.post("/api/v1/scan/url", { url });
  return res.data;
}

export async function getHistory() {
  const res = await api.get("/api/v1/scan/history");
  return res.data;
}