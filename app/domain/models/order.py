from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class Order:
    order_id: str
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: Optional[float]
    status: str
    created_at: datetime
