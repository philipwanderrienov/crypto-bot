from __future__ import annotations

from app.bot.engine import TradingEngine
from app.bot.scheduler import BotScheduler


class BotRunner:
    def __init__(self) -> None:
        self.engine = TradingEngine()
        self.scheduler = BotScheduler(self.engine)

    def run(self) -> dict:
        return self.scheduler.run_once()

    def run_forever(self) -> dict:
        return self.scheduler.run_forever()
