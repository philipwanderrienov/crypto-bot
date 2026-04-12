from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter

from backend.api.health import health_check
from backend.api.models import (
    AnalysisResponse,
    BotStateResponse,
    HealthResponse,
    MarketSnapshotResponse,
    NewsItemResponse,
    NewsResponse,
    OrderResponse,
    PositionResponse,
    SettingsResponse,
    SettingsUpdateRequest,
    TradeResponse,
)
from backend.config.settings import get_settings
from backend.domain.models.bot_state import BotState
from backend.domain.models.market import RealtimeMarketSnapshot
from backend.domain.models.order import Order
from backend.domain.models.position import Position
from backend.infrastructure.bybit.client import BybitExchangeClient
from backend.infrastructure.database.repositories import SqlAlchemyBotRepository
from backend.services.bot_control_service import BotControlService
from backend.services.market_data_service import MarketDataService
from backend.services.portfolio_service import PortfolioService

router = APIRouter()

_settings = get_settings()
_repository = SqlAlchemyBotRepository()
_bot_control = BotControlService(repository=_repository, bot_name=_settings.app_name)
_portfolio = PortfolioService()
_market_data_service = MarketDataService(
    symbol=_settings.default_symbol,
    timeframe=_settings.default_timeframe,
)
_bybit_client = BybitExchangeClient()


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


def _normalize_text(value: str | None) -> str:
    return (value or "").lower()


def _price_snapshot_context(snapshot: RealtimeMarketSnapshot) -> dict[str, Any]:
    last_price = snapshot.last_price or snapshot.close_price or snapshot.open_price
    open_price = snapshot.open_price
    high_price = snapshot.high_price
    low_price = snapshot.low_price

    price_change_pct = None
    if last_price is not None and open_price not in (None, 0):
        price_change_pct = ((last_price - open_price) / open_price) * 100.0

    range_pct = None
    if high_price is not None and low_price not in (None, 0):
        range_pct = ((high_price - low_price) / low_price) * 100.0

    return {
        "last_price": last_price,
        "price_change_pct": price_change_pct,
        "range_pct": range_pct,
    }


def _build_news_feed() -> list[NewsItemResponse]:
    now = datetime.now(timezone.utc)
    items = [
        NewsItemResponse(
            title="Shipping risk rises near the Strait of Hormuz as tensions remain elevated",
            summary="Market participants are watching energy supply risk and broader geopolitical escalation around the Strait of Hormuz.",
            source="curated",
            url=None,
            published_at=now - timedelta(minutes=15),
            importance=0.98,
            tags=["geopolitical", "hormuz", "oil", "war"],
        ),
        NewsItemResponse(
            title="Iran-related developments keep traders focused on regional escalation risk",
            summary="Persistent headlines around Iran continue to influence risk sentiment and defensive positioning across markets.",
            source="curated",
            url=None,
            published_at=now - timedelta(minutes=35),
            importance=0.95,
            tags=["iran", "geopolitical", "war", "risk"],
        ),
        NewsItemResponse(
            title="Oil prices remain sensitive to Middle East disruption risk",
            summary="Energy markets can amplify crypto volatility when supply disruption headlines intensify.",
            source="curated",
            url=None,
            published_at=now - timedelta(hours=1),
            importance=0.9,
            tags=["oil", "macro", "geopolitical"],
        ),
        NewsItemResponse(
            title="Federal Reserve policy expectations remain a key macro driver",
            summary="Rate-cut and higher-for-longer expectations can shift liquidity appetite across BTC and ETH.",
            source="curated",
            url=None,
            published_at=now - timedelta(hours=2),
            importance=0.88,
            tags=["fed", "macro", "liquidity"],
        ),
        NewsItemResponse(
            title="Bitcoin and Ethereum remain the main risk assets for crypto sentiment",
            summary="BTC and ETH price leadership continues to set the tone for broader digital asset flows.",
            source="curated",
            url=None,
            published_at=now - timedelta(hours=3),
            importance=0.86,
            tags=["btc", "eth", "crypto"],
        ),
    ]
    return sorted(items, key=lambda item: (-item.importance, item.published_at), reverse=False)


def _filter_relevant_news(items: list[NewsItemResponse]) -> list[NewsItemResponse]:
    priority_terms = {
        "hormuz",
        "iran",
        "war",
        "oil",
        "fed",
        "federal reserve",
        "btc",
        "bitcoin",
        "eth",
        "ethereum",
        "crypto",
        "macro",
        "geopolitical",
    }

    filtered: list[NewsItemResponse] = []
    for item in items:
        text = f"{item.title} {item.summary} {' '.join(item.tags)}".lower()
        if any(term in text for term in priority_terms):
            filtered.append(item)

    filtered.sort(key=lambda item: (-item.importance, item.published_at))
    return filtered


def _fetch_relevant_news() -> list[NewsItemResponse]:
    print("[news] using curated fallback feed; no external provider configured")
    items = _build_news_feed()
    filtered = _filter_relevant_news(items)
    print(f"[news] curated feed prepared: {len(filtered)} relevant items")
    return filtered


def _build_analysis(snapshot: RealtimeMarketSnapshot, news_items: list[NewsItemResponse]) -> AnalysisResponse:
    now = datetime.now(timezone.utc)
    price_context = _price_snapshot_context(snapshot)
    last_price = price_context["last_price"]
    price_change_pct = price_context["price_change_pct"]

    bullish_news = 0
    bearish_news = 0
    key_factors: list[str] = []

    for item in news_items:
        text = f"{item.title} {item.summary} {' '.join(item.tags)}".lower()
        if any(term in text for term in ["fed", "bitcoin", "btc", "ethereum", "eth"]):
            bullish_news += 1
            key_factors.append(f"Supportive market backdrop: {item.title}")
        if any(term in text for term in ["hormuz", "iran", "war", "oil", "risk", "escalation"]):
            bearish_news += 1
            key_factors.append(f"Risk-off headline: {item.title}")

    if snapshot.last_error:
        key_factors.append(f"Live market feed degraded: {snapshot.last_error}")

    signal = "HOLD"
    confidence = 0.5
    reason_parts: list[str] = []

    if last_price is None:
        reason_parts.append("No reliable live price snapshot available, so the model is using fallback rules.")
        confidence = 0.42
    else:
        reason_parts.append(f"Latest observed price is {last_price:.2f}.")

    if price_change_pct is not None:
        if price_change_pct >= 0.75 and bullish_news >= bearish_news:
            signal = "BUY"
            confidence = min(0.92, 0.58 + abs(price_change_pct) / 10.0 + bullish_news * 0.05)
            reason_parts.append(f"Price momentum is positive at {price_change_pct:.2f}%, supported by news sentiment.")
        elif price_change_pct <= -0.75 and bearish_news >= bullish_news:
            signal = "SELL"
            confidence = min(0.9, 0.57 + abs(price_change_pct) / 10.0 + bearish_news * 0.05)
            reason_parts.append(f"Price momentum is negative at {price_change_pct:.2f}%, while risk headlines are elevated.")
        elif bullish_news > bearish_news:
            signal = "BUY"
            confidence = min(0.82, 0.54 + bullish_news * 0.06)
            reason_parts.append("News flow leans supportive for BTC/ETH and broader risk assets.")
        elif bearish_news > bullish_news:
            signal = "SELL"
            confidence = min(0.8, 0.53 + bearish_news * 0.06)
            reason_parts.append("Geopolitical and energy headlines imply higher downside risk.")
        else:
            reason_parts.append("Price action and news flow are mixed, so the stance remains neutral.")
            confidence = 0.55
    else:
        if bullish_news > bearish_news:
            signal = "BUY"
            confidence = min(0.78, 0.52 + bullish_news * 0.05)
            reason_parts.append("News sentiment is constructive even without a clean candle snapshot.")
        elif bearish_news > bullish_news:
            signal = "SELL"
            confidence = min(0.76, 0.51 + bearish_news * 0.05)
            reason_parts.append("Macro and geopolitical risk headlines dominate the tape.")
        else:
            reason_parts.append("There is insufficient directional evidence, so the analysis stays neutral.")
            confidence = 0.5

    if snapshot.status in {"degraded", "error"}:
        reason_parts.append(f"Market data status is {snapshot.status}, so fallback logic is being used.")

    if not key_factors:
        key_factors.append("Fallback rule set based on available market state")
        key_factors.append("Relevant macro/geopolitical news feed")

    confidence = max(0.05, min(0.99, round(confidence, 2)))
    reason = " ".join(reason_parts)

    print(
        "[analysis] generated",
        {
            "signal": signal,
            "confidence": confidence,
            "snapshot_status": snapshot.status,
            "news_items": len(news_items),
        },
    )

    return AnalysisResponse(
        signal=signal,
        reason=reason,
        confidence=confidence,
        key_factors=key_factors[:5],
        updated_at=now,
    )


@router.get("/health", response_model=HealthResponse)
def get_health() -> dict[str, str]:
    return health_check()


@router.get("/bot/status", response_model=BotStateResponse)
def get_bot_status() -> BotStateResponse:
    state = BotState(
        bot_name=_settings.app_name,
        is_running=True,
        last_updated=datetime.now(timezone.utc),
        current_symbol=_settings.default_symbol,
        current_timeframe=_settings.default_timeframe,
        last_error=None,
    )
    return _to_bot_state_response(state)


@router.get("/market/snapshot", response_model=MarketSnapshotResponse)
def get_market_snapshot() -> MarketSnapshotResponse:
    try:
        candle = _bybit_client.get_latest_candle(_settings.default_symbol, _settings.default_timeframe)
        snapshot = _market_data_service.update_snapshot_from_polling(candle)
        _market_data_service.set_error(None)
        print(f"[market/snapshot] live Bybit data: {snapshot}")
    except Exception as exc:
        error = str(exc)
        print(f"[market/snapshot] Bybit fetch failed: {error}")
        _market_data_service.set_error(error)
        snapshot = _market_data_service.get_latest_snapshot()
        if snapshot.symbol != _settings.default_symbol or snapshot.timeframe != _settings.default_timeframe:
            snapshot = RealtimeMarketSnapshot(
                symbol=_settings.default_symbol,
                timeframe=_settings.default_timeframe,
                source="fallback",
                status="degraded",
                last_updated=datetime.now(timezone.utc),
                websocket_connected=False,
                polling_active=False,
                last_error=error,
            )
        elif snapshot.last_error is None:
            snapshot.last_error = error
            snapshot.source = "fallback"
            snapshot.status = "degraded"
    return _to_market_snapshot_response(snapshot)


@router.get("/analysis", response_model=AnalysisResponse)
def get_analysis() -> AnalysisResponse:
    try:
        candle = _bybit_client.get_latest_candle(_settings.default_symbol, _settings.default_timeframe)
        snapshot = _market_data_service.update_snapshot_from_polling(candle)
        _market_data_service.set_error(None)
        print(f"[analysis] live market snapshot refreshed: {snapshot}")
    except Exception as exc:
        error = str(exc)
        print(f"[analysis] live market fetch failed, falling back: {error}")
        _market_data_service.set_error(error)
        snapshot = _market_data_service.get_latest_snapshot()
        if snapshot.symbol != _settings.default_symbol or snapshot.timeframe != _settings.default_timeframe:
            snapshot = RealtimeMarketSnapshot(
                symbol=_settings.default_symbol,
                timeframe=_settings.default_timeframe,
                source="fallback",
                status="degraded",
                last_updated=datetime.now(timezone.utc),
                websocket_connected=False,
                polling_active=False,
                last_error=error,
            )
        elif snapshot.last_error is None:
            snapshot.last_error = error
            snapshot.source = "fallback"
            snapshot.status = "degraded"

    news_items = _fetch_relevant_news()
    return _build_analysis(snapshot, news_items)


@router.get("/news", response_model=NewsResponse)
def get_news() -> NewsResponse:
    items = _fetch_relevant_news()
    return NewsResponse(items=items, updated_at=datetime.now(timezone.utc))


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