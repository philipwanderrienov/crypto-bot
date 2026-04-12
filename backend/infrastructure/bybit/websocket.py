from __future__ import annotations

from datetime import datetime, timezone
from threading import Event, Thread
from time import sleep
from typing import Callable, Optional

from app.domain.models.market import MarketCandle


class BybitWebSocketClient:
    def __init__(self, symbol: str, timeframe: str) -> None:
        self.symbol = symbol
        self.timeframe = timeframe
        self._connected = False
        self._last_error: Optional[str] = None
        self._stop_event = Event()
        self._thread: Optional[Thread] = None

    def start(self, on_candle: Callable[[MarketCandle], None]) -> None:
        if self._thread and self._thread.is_alive():
            return

        self._stop_event.clear()
        self._thread = Thread(target=self._run, args=(on_candle,), daemon=True)
        self._thread.start()

    def _run(self, on_candle: Callable[[MarketCandle], None]) -> None:
        self._connected = True
        self._last_error = None

        while not self._stop_event.is_set():
            now = datetime.now(timezone.utc)
            price = 100.0
            candle = MarketCandle(
                symbol=self.symbol,
                timeframe=self.timeframe,
                open_time=now,
                open_price=price,
                high_price=price + 1,
                low_price=price - 1,
                close_price=price,
                volume=1.0,
            )
            on_candle(candle)
            sleep(1)

        self._connected = False

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2)

    def is_connected(self) -> bool:
        return self._connected

    def get_last_error(self) -> Optional[str]:
        return self._last_error
