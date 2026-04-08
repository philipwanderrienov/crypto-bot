from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.session import Base


class BotRunModel(Base):
    __tablename__ = "bot_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bot_name: Mapped[str] = mapped_column(String(100), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    stopped_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False)


class MarketCandleModel(Base):
    __tablename__ = "market_candles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    timeframe: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    open_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    open_price: Mapped[float] = mapped_column(Float, nullable=False)
    high_price: Mapped[float] = mapped_column(Float, nullable=False)
    low_price: Mapped[float] = mapped_column(Float, nullable=False)
    close_price: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[float] = mapped_column(Float, nullable=False)


class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    side: Mapped[str] = mapped_column(String(10), nullable=False)
    order_type: Mapped[str] = mapped_column(String(30), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    price: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class PositionModel(Base):
    __tablename__ = "positions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    side: Mapped[str] = mapped_column(String(10), nullable=False)
    size: Mapped[float] = mapped_column(Float, nullable=False)
    entry_price: Mapped[float] = mapped_column(Float, nullable=False)
    mark_price: Mapped[float] = mapped_column(Float, nullable=False)
    unrealized_pnl: Mapped[float] = mapped_column(Float, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class StrategySignalModel(Base):
    __tablename__ = "strategy_signals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    timeframe: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    signal_type: Mapped[str] = mapped_column(String(20), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    price: Mapped[float | None] = mapped_column(Float, nullable=True)


class AppSettingModel(Base):
    __tablename__ = "app_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class TradeModel(Base):
    __tablename__ = "trades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    trade_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    order_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    side: Mapped[str] = mapped_column(String(10), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    fee: Mapped[float] = mapped_column(Float, nullable=False)
    executed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
