from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter

from app.api.health import health_check
from app.api.models import (
    BotStateResponse,
    HealthResponse,
    MarketSnapshotResponse,
    OrderResponse,
    PositionResponse,
    SettingsResponse,
    SettingsUpdateRequest,
    TradeResponse,
)
from app.bot.engine import TradingEngine
from app.config.settings import get_settings
from app.domain.models.bot_state import BotState
from app.domain.models.market import RealtimeMarketSnapshot
from app.domain.models.order import Order
from app.domain.models.position import Position
from app.infrastructure.database.repositories import SqlAlchemyBotRepository
from app.services.bot_control_service import BotControlService

router = APIRouter()

_settings = get_settings()
_repository = SqlAlchemyBotRepository()
_bot_control = BotControlService(repository=_repository, bot_name=_settings.app_name)


def _build_engine() -> TradingEngine:
    return TradingEngine()


def _to_bot_state_response(state: BotState) -> BotStateResponse:
    return BotStateResponse.model_validate(state)


def _to_market_snapshot_response(snapshot: RealtimeMarketSnapshot) -> MarketSnapshotResponse:
    return MarketSnapshotResponse.model_validate(snapshot)


def _sample_orders() -> list[Order]:
    now = datetime.now(timezone.utc)
    return [
        Order(
            order_id="ord_001",
            symbol=_settings.default_symbol,
            side="BUY",
            order_type="MARKET",
            quantity=0.01,
            price=None,
            status="FILLED",
            created_at=now,
        ),
        Order(
            order_id="ord_002",
            symbol=_settings.default_symbol,
            side="SELL",
            order_type="LIMIT",
            quantity=0.01,
            price=70000.0,
            status="OPEN",
            created_at=now,
        ),
    ]


def _sample_positions() -> list[Position]:
    return [
        Position(
            symbol=_settings.default_symbol,
            side="LONG",
            size=0.01,
            entry_price=68000.0,
            mark_price=69000.0,
            unrealized_pnl=10.0,
            updated_at=datetime.now(timezone.utc),
        )
    ]


def _sample_trades() -> list[TradeResponse]:
    now = datetime.now(timezone.utc)
    return [
        TradeResponse(
            trade_id="trade_001",
            order_id="ord_001",
            symbol=_settings.default_symbol,
            side="BUY",
            quantity=0.01,
            price=68250.0,
            fee=0.68,
            executed_at=now,
        )
    ]


@router.get("/health", response_model=HealthResponse)
def get_health() -> dict[str, str]:
    return health_check()


@router.get("/bot/status", response_model=BotStateResponse)
def get_bot_status() -> BotStateResponse:
    engine = _build_engine()
    state = engine.build_state(is_running=True)
    return _to_bot_state_response(state)


@router.get("/market/snapshot", response_model=MarketSnapshotResponse)
def get_market_snapshot() -> MarketSnapshotResponse:
    engine = _build_engine()
    snapshot = engine.get_realtime_snapshot()
    return _to_market_snapshot_response(snapshot)


@router.get("/orders", response_model=list[OrderResponse])
def get_orders() -> list[OrderResponse]:
    return [OrderResponse.model_validate(order) for order in _sample_orders()]


@router.get("/positions", response_model=list[PositionResponse])
def get_positions() -> list[PositionResponse]:
    positions = _sample_positions()
    return [PositionResponse.model_validate(position) for position in positions]


@router.get("/trades", response_model=list[TradeResponse])
def get_trades() -> list[TradeResponse]:
    return _sample_trades()


@router.get("/settings", response_model=SettingsResponse)
def get_settings_response() -> SettingsResponse:
    settings = get_settings()
    return SettingsResponse(
        app_env=settings.app_env,
        app_name=settings.app_name,
        log_level=settings.log_level,
        default_symbol=settings.default_symbol,
        default_timeframe=settings.default_timeframe,
        bybit_testnet=settings.bybit_testnet,
        bybit_base_url=settings.bybit_base_url,
        has_api_credentials=bool(settings.bybit_api_key and settings.bybit_api_secret),
    )


@router.put("/settings", response_model=SettingsResponse)
def update_settings(payload: SettingsUpdateRequest) -> SettingsResponse:
    settings = get_settings()
    updated = settings.model_copy(
        update={k: v for k, v in payload.model_dump(exclude_unset=True).items() if v is not None}
    )
    return SettingsResponse(
        app_env=updated.app_env,
        app_name=updated.app_name,
        log_level=updated.log_level,
        default_symbol=updated.default_symbol,
        default_timeframe=updated.default_timeframe,
        bybit_testnet=updated.bybit_testnet,
        bybit_base_url=updated.bybit_base_url,
        has_api_credentials=bool(updated.bybit_api_key and updated.bybit_api_secret),
    )


@router.get("/bot/control/start")
def start_bot() -> dict[str, Any]:
    return _bot_control.start()


@router.get("/bot/control/stop")
def stop_bot() -> dict[str, Any]:
    return _bot_control.stop()


