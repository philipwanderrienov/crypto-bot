from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.bot.runner import BotRunner


def main() -> None:
    runner = BotRunner()
    print("Starting realtime bot service...")
    result = runner.run_forever()
    state = result["state"]
    snapshot = result["market_snapshot"]
    status = result["market_status"]

    print("Bot stopped.")
    print(f"Bot Name      : {state.bot_name}")
    print(f"Running       : {state.is_running}")
    print(f"Symbol        : {state.current_symbol}")
    print(f"Timeframe     : {state.current_timeframe}")
    print(f"Last Updated  : {state.last_updated.isoformat()}")
    print(f"Last Error    : {state.last_error}")
    print(f"WS Status     : {status.get('websocket_connected')}")
    print(f"WS Error      : {status.get('last_error')}")
    if snapshot is not None:
        print(f"Snapshot Src  : {snapshot.source}")
        print(f"Last Price    : {snapshot.last_price}")
        print(f"Poll Active   : {snapshot.polling_active}")


if __name__ == "__main__":
    main()
