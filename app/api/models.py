from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class BotStateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    bot_name: str
    is_running: bool
    last_updated: datetime
    current_symbol: Optional[str] = None
    current_timeframe: Optional[str] = None
    last_error: Optional[str] = None


class MarketSnapshotResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: str
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: Optional[float] = None
    status: str
    created_at: datetime


class PositionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    symbol: str
    side: str
    size: float
    entry_price: float
    mark_price: float
    unrealized_pnl: float
    updated_at: datetime


class TradeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    trade_id: str
    order_id: str
    symbol: str
    side: str
    quantity: float
    price: float
    fee: float
    executed_at: datetime


class SettingsResponse(BaseModel):
    app_env: str
    app_name: str
    log_level: str
    default_symbol: str
    default_timeframe: str
    bybit_testnet: bool
    bybit_base_url: str
    has_api_credentials: bool


class SettingsUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    app_env: Optional[str] = None
    app_name: Optional[str] = None
    log_level: Optional[str] = None
    default_symbol: Optional[str] = None
    default_timeframe: Optional[str] = None
    bybit_testnet: Optional[bool] = None
    bybit_base_url: Optional[str] = None


class HealthResponse(BaseModel):
    status: str = Field(default="ok")


class ApiErrorResponse(BaseModel):
    detail: str
    extra: dict[str, Any] | None = None