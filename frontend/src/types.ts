export type HealthResponse = {
  status: string;
};

export type BotStateResponse = {
  bot_name: string;
  is_running: boolean;
  last_updated: string;
  current_symbol: string | null;
  current_timeframe: string | null;
  last_error: string | null;
};

export type MarketSnapshotResponse = {
  symbol: string;
  timeframe: string;
  source: string;
  status: string;
  last_updated: string | null;
  websocket_connected: boolean;
  polling_active: boolean;
  last_error: string | null;
  open_price: number | null;
  high_price: number | null;
  low_price: number | null;
  close_price: number | null;
  last_price: number | null;
  volume: number | null;
};

export type OrderResponse = {
  order_id: string;
  symbol: string;
  side: string;
  order_type: string;
  quantity: number;
  price: number | null;
  status: string;
  created_at: string;
};

export type PositionResponse = {
  symbol: string;
  side: string;
  size: number;
  entry_price: number;
  mark_price: number;
  unrealized_pnl: number;
  updated_at: string;
};

export type TradeResponse = {
  trade_id: string;
  order_id: string;
  symbol: string;
  side: string;
  quantity: number;
  price: number;
  fee: number;
  executed_at: string;
};

export type SettingsResponse = {
  app_env: string;
  app_name: string;
  log_level: string;
  default_symbol: string;
  default_timeframe: string;
  bybit_testnet: boolean;
  bybit_base_url: string;
  has_api_credentials: boolean;
};

export type SettingsUpdateRequest = {
  app_env?: string;
  app_name?: string;
  log_level?: string;
  default_symbol?: string;
  default_timeframe?: string;
  bybit_testnet?: boolean;
  bybit_base_url?: string;
};

export type OverviewResponse = {
  bot: BotStateResponse;
  market: MarketSnapshotResponse;
  orders: OrderResponse[];
  positions: PositionResponse[];
  trades: TradeResponse[];
  settings: SettingsResponse;
};

export type AnalysisSignal = "bullish" | "bearish" | "neutral" | "cautious" | "mixed";

export type AnalysisResponse = {
  signal: AnalysisSignal;
  reason: string;
  confidence: number;
  key_factors: string[];
  updated_at: string;
};

export type NewsItem = {
  id: string;
  headline: string;
  source: string;
  published_at: string;
  summary: string;
  importance: "high" | "medium" | "low";
  tags: string[];
  url: string | null;
};

export type NewsResponse = {
  items: NewsItem[];
  updated_at: string;
};