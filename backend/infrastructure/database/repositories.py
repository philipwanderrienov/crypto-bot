from datetime import datetime, timezone
from typing import Optional

from app.domain.interfaces import BotRepository
from app.domain.models.order import Order
from app.domain.models.position import Position
from app.domain.models.strategy import StrategySignal
from app.infrastructure.database.models import (
    AppSettingModel,
    BotRunModel,
    MarketCandleModel,
    OrderModel,
    PositionModel,
    StrategySignalModel,
    TradeModel,
)
from app.infrastructure.database.session import SessionLocal


class SqlAlchemyBotRepository(BotRepository):
    def save_order(self, order: Order) -> None:
        with SessionLocal() as session:
            model = OrderModel(
                order_id=order.order_id,
                symbol=order.symbol,
                side=order.side,
                order_type=order.order_type,
                quantity=order.quantity,
                price=order.price,
                status=order.status,
                created_at=order.created_at,
            )
            session.merge(model)
            session.commit()

    def save_position(self, position: Position) -> None:
        with SessionLocal() as session:
            model = PositionModel(
                symbol=position.symbol,
                side=position.side,
                size=position.size,
                entry_price=position.entry_price,
                mark_price=position.mark_price,
                unrealized_pnl=position.unrealized_pnl,
                updated_at=position.updated_at,
            )
            session.add(model)
            session.commit()

    def save_signal(self, signal: StrategySignal) -> None:
        with SessionLocal() as session:
            model = StrategySignalModel(
                symbol=signal.symbol,
                timeframe=signal.timeframe,
                signal_type=signal.signal_type,
                confidence=signal.confidence,
                reason=signal.reason,
                generated_at=signal.generated_at,
                price=signal.price,
            )
            session.add(model)
            session.commit()

    def get_latest_bot_state(self, bot_name: str) -> dict | None:
        with SessionLocal() as session:
            result = (
                session.query(BotRunModel)
                .filter(BotRunModel.bot_name == bot_name)
                .order_by(BotRunModel.started_at.desc())
                .first()
            )
            if result is None:
                return None

            return {
                "bot_name": result.bot_name,
                "status": result.status,
                "started_at": result.started_at,
                "stopped_at": result.stopped_at,
            }


class PostgresRepositoryExtras:
    @staticmethod
    def save_bot_run(bot_name: str, status: str, started_at: datetime | None = None) -> None:
        with SessionLocal() as session:
            model = BotRunModel(
                bot_name=bot_name,
                started_at=started_at or datetime.now(timezone.utc),
                stopped_at=None,
                status=status,
            )
            session.add(model)
            session.commit()

    @staticmethod
    def save_trade(
        trade_id: str,
        order_id: str,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
        fee: float,
        executed_at: datetime | None = None,
    ) -> None:
        with SessionLocal() as session:
            model = TradeModel(
                trade_id=trade_id,
                order_id=order_id,
                symbol=symbol,
                side=side,
                quantity=quantity,
                price=price,
                fee=fee,
                executed_at=executed_at or datetime.now(timezone.utc),
            )
            session.add(model)
            session.commit()
