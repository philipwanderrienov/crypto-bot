export type AnalysisSignal = "bullish" | "bearish" | "cautious" | "neutral";

export interface AnalysisResponse {
  signal: AnalysisSignal;
  reason: string;
  confidence: number;
  key_factors: string[];
  updated_at: string;
}

export type NewsImportance = "high" | "medium" | "low";

export interface NewsItem {
  id: string;
  headline: string;
  summary: string;
  source: string;
  published_at: string;
  importance: NewsImportance;
  tags: string[];
}

export interface NewsResponse {
  items: NewsItem[];
  updated_at: string;
}

export interface OrderItem {
  id: string;
  symbol: string;
  side: string;
  quantity: number;
  price: number;
  status: string;
  created_at: string;
}

export interface PositionItem {
  symbol: string;
  side: string;
  size: number;
  entry_price: number;
  mark_price: number;
  unrealized_pnl: number;
  updated_at: string;
}

export interface TradeItem {
  id: string;
  order_id: string;
  symbol: string;
  side: string;
  quantity: number;
  price: number;
  fee: number;
  executed_at: string;
}

export interface SettingsResponse {
  app_env: string;
  app_name: string;
  log_level: string;
  default_symbol: string;
  default_timeframe: string;
  bybit_testnet: boolean;
  bybit_base_url: string;
  has_api_credentials: boolean;
}
