from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class BotState:
    bot_name: str
    is_running: bool
    last_updated: datetime
    current_symbol: Optional[str] = None
    current_timeframe: Optional[str] = None
    last_error: Optional[str] = None
