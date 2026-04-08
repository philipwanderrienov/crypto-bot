from __future__ import annotations

from dataclasses import asdict
from threading import Lock
from typing import Optional

from app.domain.models.market import MarketCandle, RealtimeMarketSnapshot


class MarketDataService:
    def __init__(self, symbol: str, timeframe: str) -> None:
        self.symbol = symbol
        self.timeframe = timeframe
        self._lock = Lock()
        self._snapshot = RealtimeMarketSnapshot(
            symbol=symbol,
            timeframe=timeframe,
            source="bootstrap",
            status="starting",
        )

    def update_snapshot_from_candle(self, candle: MarketCandle) -> RealtimeMarketSnapshot:
        with self._lock:
            self._snapshot = RealtimeMarketSnapshot(
                symbol=candle.symbol,
                timeframe=candle.timeframe,
                source="websocket",
                status="running",
                last_updated=candle.open_time,
                websocket_connected=True,
                polling_active=True,
                open_price=candle.open_price,
                high_price=candle.high_price,
                low_price=candle.low_price,
                close_price=candle.close_price,
                last_price=candle.close_price,
                volume=candle.volume,
            )
            return self._snapshot

    def update_snapshot_from_polling(self, candle: MarketCandle) -> RealtimeMarketSnapshot:
        with self._lock:
            self._snapshot = RealtimeMarketSnapshot(
                symbol=candle.symbol,
                timeframe=candle.timeframe,
                source="polling",
                status="running",
                last_updated=candle.open_time,
                websocket_connected=self._snapshot.websocket_connected,
                polling_active=True,
                open_price=candle.open_price,
                high_price=candle.high_price,
                low_price=candle.low_price,
                close_price=candle.close_price,
                last_price=candle.close_price,
                volume=candle.volume,
            )
            return self._snapshot

    def set_websocket_status(self, connected: bool, error: Optional[str] = None) -> None:
        with self._lock:
            self._snapshot.websocket_connected = connected
            self._snapshot.last_error = error
            self._snapshot.status = "running" if connected else "degraded"

    def set_error(self, error: Optional[str]) -> None:
        with self._lock:
            self._snapshot.last_error = error
            if error:
                self._snapshot.status = "error"

    def get_latest_snapshot(self) -> RealtimeMarketSnapshot:
        with self._lock:
            return self._snapshot

    def get_status(self) -> dict:
        with self._lock:
            return {
                "websocket_connected": self._snapshot.websocket_connected,
                "polling_active": self._snapshot.polling_active,
                "last_error": self._snapshot.last_error,
                "status": self._snapshot.status,
                "snapshot": asdict(self._snapshot),
            }
