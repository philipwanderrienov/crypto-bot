from abc import ABC, abstractmethod
from typing import Iterable, Optional

from app.domain.models.market import MarketCandle
from app.domain.models.order import Order
from app.domain.models.position import Position
from app.domain.models.strategy import StrategySignal


class ExchangeClient(ABC):
    @abstractmethod
    def get_balance(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_candles(self, symbol: str, timeframe: str, limit: int = 200) -> list[MarketCandle]:
        raise NotImplementedError

    @abstractmethod
    def get_position(self, symbol: str) -> Optional[Position]:
        raise NotImplementedError

    @abstractmethod
    def get_open_orders(self, symbol: str) -> list[Order]:
        raise NotImplementedError

    @abstractmethod
    def place_order(self, signal: StrategySignal) -> Order:
        raise NotImplementedError

    @abstractmethod
    def cancel_order(self, order_id: str, symbol: str) -> bool:
        raise NotImplementedError


class Strategy(ABC):
    @abstractmethod
    def generate_signal(self, candles: Iterable[MarketCandle]) -> StrategySignal:
        raise NotImplementedError


class BotRepository(ABC):
    @abstractmethod
    def save_order(self, order: Order) -> None:
        raise NotImplementedError

    @abstractmethod
    def save_position(self, position: Position) -> None:
        raise NotImplementedError

    @abstractmethod
    def save_signal(self, signal: StrategySignal) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_latest_bot_state(self, bot_name: str) -> dict | None:
        raise NotImplementedError
