import streamlit as st

from app.dashboard.components.charts import render_chart_placeholder
from app.dashboard.components.metrics import render_metrics_placeholder
from app.dashboard.components.tables import render_table_placeholder


def render_positions() -> None:
    st.header("Positions")
    st.caption("Open exposure, leverage, and portfolio concentration.")

    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Net Exposure", "0.00")
    metric_col2.metric("Unrealized PnL", "0.00")
    metric_col3.metric("Leverage", "0.0x")

    st.divider()

    left_col, right_col = st.columns([2, 1])
    with left_col:
        st.subheader("Exposure Trend")
        timeframe = st.selectbox("Time window", ["1h", "4h", "1d", "1w"], index=1)
        render_chart_placeholder()
        st.caption(f"Exposure trend for {timeframe} will appear here once live data is connected.")
    with right_col:
        st.subheader("Risk Snapshot")
        render_metrics_placeholder()
        st.slider("Target leverage", min_value=1, max_value=20, value=3)
        st.slider("Max drawdown guard (%)", min_value=1, max_value=25, value=10)
        st.checkbox("Auto-reduce positions on signal", value=False, disabled=True)
        st.info("Position risk metrics will populate once account and market data are connected.")

    st.divider()

    st.subheader("Open Positions")
    render_table_placeholder()

    st.divider()

    detail_col1, detail_col2 = st.columns([2, 1])
    with detail_col1:
        st.subheader("Position Notes")
        st.text_area(
            "Management notes",
            value="No open positions are currently displayed. Entry price, stop loss, take profit, and liquidation context will appear here when available.",
            height=180,
        )
    with detail_col2:
        st.subheader("Position Tools")
        st.button("Refresh positions", use_container_width=True)
        st.button("Close selected", use_container_width=True)
        st.button("Hedge exposure", use_container_width=True)
        st.warning("Position actions are placeholders until exchange-side handlers are connected.")