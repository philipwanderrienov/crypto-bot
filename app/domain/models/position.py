from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Position:
    symbol: str
    side: str
    size: float
    entry_price: float
    mark_price: float
    unrealized_pnl: float
    updated_at: datetime
