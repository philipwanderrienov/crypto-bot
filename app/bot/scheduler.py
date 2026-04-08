from __future__ import annotations

from typing import Optional

from app.bot.engine import TradingEngine


class BotScheduler:
    def __init__(self, engine: TradingEngine) -> None:
        self.engine = engine
        self._running = False

    def run_forever(self) -> dict:
        self._running = True
        return self.engine.run_forever()

    def stop(self) -> None:
        self._running = False
        self.engine.stop()

    def is_running(self) -> bool:
        return self._running

    def run_once(self) -> dict:
        self.engine.start_realtime_pipeline()
        return {
            "state": self.engine.build_state(is_running=True),
            "market_snapshot": self.engine.get_realtime_snapshot(),
            "market_status": self.engine.get_realtime_status(),
        }
