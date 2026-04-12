const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export async function fetchJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`);

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export interface MarketSummaryResponse {
  symbol: string;
  price: number | null;
  change24h: number | null;
  timestamp: string;
}

export function getMarketSummary() {
  return fetchJson<MarketSummaryResponse>("/api/market/summary");
}

export type { AnalysisResponse, NewsResponse } from "./types";

export function getAnalysis() {
  return fetchJson<import("./types").AnalysisResponse>("/api/analysis");
}

export function getNews() {
  return fetchJson<import("./types").NewsResponse>("/api/news");
}