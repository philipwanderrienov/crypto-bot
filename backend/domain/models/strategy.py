from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class StrategySignal:
    symbol: str
    timeframe: str
    signal_type: str
    confidence: float
    reason: str
    generated_at: datetime
    price: Optional[float] = None
