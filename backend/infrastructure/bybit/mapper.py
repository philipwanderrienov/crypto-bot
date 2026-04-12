from datetime import datetime, timezone

from app.domain.models.market import MarketCandle


def map_candle(
    symbol: str,
    timeframe: str,
    raw_candle: list[str | float | int],
) -> MarketCandle:
    open_time = datetime.fromtimestamp(int(raw_candle[0]) / 1000, tz=timezone.utc)
    return MarketCandle(
        symbol=symbol,
        timeframe=timeframe,
        open_time=open_time,
        open_price=float(raw_candle[1]),
        high_price=float(raw_candle[2]),
        low_price=float(raw_candle[3]),
        close_price=float(raw_candle[4]),
        volume=float(raw_candle[5]),
    )
