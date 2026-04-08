from pathlib import Path
import sys

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.bot.runner import BotRunner
from app.config.settings import get_settings


def main() -> None:
    settings = get_settings()
    runner = BotRunner()
    result = runner.run()
    state = result["state"]
    snapshot = result.get("market_snapshot")
    market_status = result.get("market_status", {})

    st.set_page_config(page_title=settings.app_name, layout="wide")
    st.title("Crypto Bot Dashboard")
    st.subheader("Realtime Overview")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Bot Name", state.bot_name)
    col2.metric("Running", str(state.is_running))
    col3.metric("Symbol", state.current_symbol or "-")
    col4.metric("Timeframe", state.current_timeframe or "-")

    st.divider()

    if snapshot:
        st.subheader("Latest Market Snapshot")
        snap_col1, snap_col2, snap_col3 = st.columns(3)
        snap_col1.metric("Source", snapshot.source)
        snap_col2.metric("Last Price", f"{snapshot.last_price:.4f}" if snapshot.last_price is not None else "-")
        snap_col3.metric("Last Update", snapshot.last_updated.isoformat() if snapshot.last_updated else "-")

        detail_col1, detail_col2, detail_col3 = st.columns(3)
        detail_col1.write(f"Websocket Connected: `{snapshot.websocket_connected}`")
        detail_col2.write(f"Polling Active: `{snapshot.polling_active}`")
        detail_col3.write(f"Status: `{snapshot.status}`")

        price_cols = st.columns(4)
        price_cols[0].metric("Open", f"{snapshot.open_price:.4f}" if snapshot.open_price is not None else "-")
        price_cols[1].metric("High", f"{snapshot.high_price:.4f}" if snapshot.high_price is not None else "-")
        price_cols[2].metric("Low", f"{snapshot.low_price:.4f}" if snapshot.low_price is not None else "-")
        price_cols[3].metric("Close", f"{snapshot.close_price:.4f}" if snapshot.close_price is not None else "-")
    else:
        st.info("Waiting for market snapshot...")

    st.divider()

    st.subheader("Market Status")
    status_col1, status_col2, status_col3 = st.columns(3)
    status_col1.write(f"Websocket Connected: `{market_status.get('websocket_connected', False)}`")
    status_col2.write(f"Polling Active: `{market_status.get('polling_active', False)}`")
    status_col3.write(f"Last Error: `{market_status.get('last_error')}`")

    if state.last_error:
        st.error(state.last_error)
    else:
        st.success("Realtime pipeline running.")


if __name__ == "__main__":
    main()
