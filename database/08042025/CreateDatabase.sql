CREATE TABLE IF NOT EXISTS bot_runs (
    id SERIAL PRIMARY KEY,
    bot_name VARCHAR(100) NOT NULL,
    started_at TIMESTAMPTZ NOT NULL,
    stopped_at TIMESTAMPTZ NULL,
    status VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS market_candles (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    timeframe VARCHAR(10) NOT NULL,
    open_time TIMESTAMPTZ NOT NULL,
    open_price DOUBLE PRECISION NOT NULL,
    high_price DOUBLE PRECISION NOT NULL,
    low_price DOUBLE PRECISION NOT NULL,
    close_price DOUBLE PRECISION NOT NULL,
    volume DOUBLE PRECISION NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_market_candles_symbol ON market_candles(symbol);
CREATE INDEX IF NOT EXISTS idx_market_candles_timeframe ON market_candles(timeframe);
CREATE INDEX IF NOT EXISTS idx_market_candles_open_time ON market_candles(open_time);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(100) NOT NULL UNIQUE,
    symbol VARCHAR(20) NOT NULL,
    side VARCHAR(10) NOT NULL,
    order_type VARCHAR(30) NOT NULL,
    quantity DOUBLE PRECISION NOT NULL,
    price DOUBLE PRECISION NULL,
    status VARCHAR(30) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_orders_symbol ON orders(symbol);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);

CREATE TABLE IF NOT EXISTS positions (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    side VARCHAR(10) NOT NULL,
    size DOUBLE PRECISION NOT NULL,
    entry_price DOUBLE PRECISION NOT NULL,
    mark_price DOUBLE PRECISION NOT NULL,
    unrealized_pnl DOUBLE PRECISION NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_positions_symbol ON positions(symbol);

CREATE TABLE IF NOT EXISTS strategy_signals (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    timeframe VARCHAR(10) NOT NULL,
    signal_type VARCHAR(20) NOT NULL,
    confidence DOUBLE PRECISION NOT NULL,
    reason TEXT NOT NULL,
    generated_at TIMESTAMPTZ NOT NULL,
    price DOUBLE PRECISION NULL
);

CREATE INDEX IF NOT EXISTS idx_strategy_signals_symbol ON strategy_signals(symbol);
CREATE INDEX IF NOT EXISTS idx_strategy_signals_timeframe ON strategy_signals(timeframe);
CREATE INDEX IF NOT EXISTS idx_strategy_signals_generated_at ON strategy_signals(generated_at);

CREATE TABLE IF NOT EXISTS app_settings (
    id SERIAL PRIMARY KEY,
    key VARCHAR(100) NOT NULL UNIQUE,
    value TEXT NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS trades (
    id SERIAL PRIMARY KEY,
    trade_id VARCHAR(100) NOT NULL UNIQUE,
    order_id VARCHAR(100) NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    side VARCHAR(10) NOT NULL,
    quantity DOUBLE PRECISION NOT NULL,
    price DOUBLE PRECISION NOT NULL,
    fee DOUBLE PRECISION NOT NULL,
    executed_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_trades_order_id ON trades(order_id);
CREATE INDEX IF NOT EXISTS idx_trades_symbol ON trades(symbol);
CREATE INDEX IF NOT EXISTS idx_trades_executed_at ON trades(executed_at);
