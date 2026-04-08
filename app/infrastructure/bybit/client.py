from datetime import datetime, timezone
from typing import Optional

from app.domain.enums import OrderSide, OrderType, SignalType
from app.domain.interfaces import ExchangeClient
from app.domain.models.market import MarketCandle
from app.domain.models.order import Order
from app.domain.models.position import Position
from app.domain.models.strategy import StrategySignal
from app.config.settings import get_settings


class BybitExchangeClient(ExchangeClient):
    def __init__(self) -> None:
        self.settings = get_settings()

    def get_balance(self) -> dict:
        return {"equity": 0.0, "available_balance": 0.0, "currency": "USDT"}

    def get_candles(self, symbol: str, timeframe: str, limit: int = 200) -> list[MarketCandle]:
        return []

    def get_position(self, symbol: str) -> Optional[Position]:
        return None

    def get_open_orders(self, symbol: str) -> list[Order]:
        return []

    def place_order(self, signal: StrategySignal) -> Order:
        side = OrderSide.BUY.value if signal.signal_type == SignalType.LONG.value else OrderSide.SELL.value
        order_type = OrderType.MARKET.value
        now = datetime.now(timezone.utc)
        return Order(
            order_id="demo-order-id",
            symbol=signal.symbol,
            side=side,
            order_type=order_type,
            quantity=0.0,
            price=signal.price,
            status="NEW",
            created_at=now,
        )

    def cancel_order(self, order_id: str, symbol: str) -> bool:
        return True
