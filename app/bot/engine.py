from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from time import sleep
from typing import Optional

from app.config.logging import configure_logging
from app.config.settings import get_settings
from app.domain.models.bot_state import BotState
from app.domain.models.market import MarketCandle, RealtimeMarketSnapshot
from app.infrastructure.bybit.client import BybitExchangeClient
from app.infrastructure.bybit.websocket import BybitWebSocketClient
from app.services.market_data_service import MarketDataService


class TradingEngine:
    def __init__(self) -> None:
        self.settings = get_settings()
        configure_logging()
        self.market_data_service = MarketDataService(
            symbol=self.settings.default_symbol,
            timeframe=self.settings.default_timeframe,
        )
        self.exchange_client = BybitExchangeClient()
        self.websocket_client = BybitWebSocketClient(
            symbol=self.settings.default_symbol,
            timeframe=self.settings.default_timeframe,
        )
        self._started = False

    def _handle_candle(self, candle: MarketCandle) -> None:
        self.market_data_service.update_snapshot_from_candle(candle)

    def start_realtime_pipeline(self) -> None:
        if self._started:
            return

        self._started = True
        self.market_data_service.set_websocket_status(True, None)
        self.websocket_client.start(self._handle_candle)
        self._start_polling_loop()

    def _start_polling_loop(self) -> None:
        candle = MarketCandle(
            symbol=self.settings.default_symbol,
            timeframe=self.settings.default_timeframe,
            open_time=datetime.now(timezone.utc),
            open_price=100.0,
            high_price=101.0,
            low_price=99.0,
            close_price=100.5,
            volume=1.0,
        )
        self.market_data_service.update_snapshot_from_polling(candle)

    def build_state(self, is_running: bool, last_error: str | None = None) -> BotState:
        return BotState(
            bot_name=self.settings.app_name,
            is_running=is_running,
            last_updated=datetime.now(timezone.utc),
            current_symbol=self.settings.default_symbol,
            current_timeframe=self.settings.default_timeframe,
            last_error=last_error,
        )

    def get_realtime_snapshot(self) -> RealtimeMarketSnapshot:
        return self.market_data_service.get_latest_snapshot()

    def get_realtime_status(self) -> dict:
        return self.market_data_service.get_status()

    def stop(self) -> None:
        self.websocket_client.stop()
        self.market_data_service.set_websocket_status(False, self.websocket_client.get_last_error())

    def run_forever(self) -> dict:
        self.start_realtime_pipeline()
        try:
            while True:
                sleep(1)
        except KeyboardInterrupt:
            self.stop()

        state = self.build_state(is_running=False)
        snapshot = self.get_realtime_snapshot()
        status = self.get_realtime_status()
        return {
            "state": state,
            "market_snapshot": snapshot,
            "market_status": status,
        }
