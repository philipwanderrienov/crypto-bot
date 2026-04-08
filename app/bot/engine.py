from __future__ import annotations

from datetime import datetime, timezone
from time import sleep

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
        self._refresh_market_snapshot()
        self.websocket_client.start(self._handle_candle)

    def _refresh_market_snapshot(self) -> None:
        try:
            candle = self.exchange_client.get_latest_candle(
                symbol=self.settings.default_symbol,
                timeframe=self.settings.default_timeframe,
            )
            self.market_data_service.update_snapshot_from_polling(candle)
            self.market_data_service.set_error(None)
        except Exception as exc:
            self.market_data_service.set_error(str(exc))

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
                self._refresh_market_snapshot()
                sleep(5)
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
