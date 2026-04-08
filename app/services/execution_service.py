from datetime import datetime, timezone

from app.domain.interfaces import BotRepository, ExchangeClient
from app.domain.models.strategy import StrategySignal


class ExecutionService:
    def __init__(self, exchange_client: ExchangeClient, repository: BotRepository) -> None:
        self.exchange_client = exchange_client
        self.repository = repository

    def execute_signal(self, signal: StrategySignal) -> None:
        order = self.exchange_client.place_order(signal)
        self.repository.save_signal(signal)
        self.repository.save_order(order)
        self.repository.save_position(
            position=type(
                "PositionSnapshot",
                (),
                {
                    "symbol": signal.symbol,
                    "side": signal.signal_type,
                    "size": 0.0,
                    "entry_price": signal.price or 0.0,
                    "mark_price": signal.price or 0.0,
                    "unrealized_pnl": 0.0,
                    "updated_at": datetime.now(timezone.utc),
                },
            )()
        )
