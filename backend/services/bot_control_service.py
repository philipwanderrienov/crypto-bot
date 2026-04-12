from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from backend.domain.interfaces import BotRepository


class BotControlService:
    def __init__(self, repository: BotRepository, bot_name: str) -> None:
        self.repository = repository
        self.bot_name = bot_name

    def start(self) -> dict[str, Any]:
        started_at = datetime.now(timezone.utc)
        return {
            "bot_name": self.bot_name,
            "status": "RUNNING",
            "started_at": started_at,
        }

    def stop(self) -> dict[str, Any]:
        stopped_at = datetime.now(timezone.utc)
        return {
            "bot_name": self.bot_name,
            "status": "STOPPED",
            "stopped_at": stopped_at,
        }

    def get_latest_state(self) -> dict | None:
        return None
