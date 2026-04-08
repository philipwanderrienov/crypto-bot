from typing import Iterable

from app.domain.enums import SignalType
from app.domain.interfaces import Strategy
from app.domain.models.market import MarketCandle
from app.domain.models.strategy import StrategySignal


class StrategyService:
    def __init__(self, strategy: Strategy) -> None:
        self.strategy = strategy

    def generate_signal(self, candles: Iterable[MarketCandle]) -> StrategySignal:
        signal = self.strategy.generate_signal(candles)
        if signal.signal_type not in {SignalType.LONG.value, SignalType.SHORT.value, SignalType.EXIT.value, SignalType.HOLD.value}:
            raise ValueError(f"Unsupported signal type: {signal.signal_type}")
        return signal
