from app.domain.models.strategy import StrategySignal


class RiskService:
    def validate_signal(self, signal: StrategySignal) -> bool:
        return 0.0 <= signal.confidence <= 1.0

    def calculate_position_size(self, balance: float, risk_percent: float, entry_price: float) -> float:
        if balance <= 0 or risk_percent <= 0 or entry_price <= 0:
            return 0.0
        risk_amount = balance * risk_percent
        return risk_amount / entry_price
