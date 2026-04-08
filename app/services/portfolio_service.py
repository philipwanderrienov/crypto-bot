from app.domain.models.position import Position


class PortfolioService:
    def get_unrealized_pnl(self, position: Position) -> float:
        return position.unrealized_pnl

    def is_position_open(self, position: Position | None) -> bool:
        return position is not None and position.size > 0
