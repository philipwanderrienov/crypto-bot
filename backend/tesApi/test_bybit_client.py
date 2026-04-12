import json
import sys
from pathlib import Path

project_root = Path("/Users/philipwanderrienov/Documents/crypto-bot")
backend_root = project_root / "backend"
for path in (str(backend_root), str(project_root)):
    if path not in sys.path:
        sys.path.insert(0, path)

from backend.infrastructure.bybit.client import BybitExchangeClient

client = BybitExchangeClient()

try:
    candle = client.get_latest_candle("BTCUSDT", "5m")
    print(json.dumps({"ok": True, "candle": candle.model_dump()}, default=str))
except Exception as exc:
    print(json.dumps({"ok": False, "error": str(exc), "last_error": client.get_last_error()}, default=str))
