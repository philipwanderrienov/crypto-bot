from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class MarketCandle:
    symbol: str
    timeframe: str
    open_time: datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float


@dataclass
class RealtimeMarketSnapshot:
    symbol: str
    timeframe: str
    source: str
    status: str
    last_updated: Optional[datetime] = None
    websocket_connected: bool = False
    polling_active: bool = False
    last_error: Optional[str] = None
    open_price: Optional[float] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    close_price: Optional[float] = None
    last_price: Optional[float] = None
    volume: Optional[float] = None
