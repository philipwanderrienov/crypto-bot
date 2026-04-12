import streamlit as st

from app.dashboard.components.charts import render_chart_placeholder
from app.dashboard.components.tables import render_table_placeholder


def render_trades() -> None:
    st.header("Trades")
    st.caption("Filled orders, execution quality, and recent trade history.")

    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
    stats_col1.metric("Filled Trades", "0")
    stats_col2.metric("Win Rate", "0%")
    stats_col3.metric("Avg. Profit", "0.00")
    stats_col4.metric("Fees", "0.00")

    st.divider()

    chart_col, info_col = st.columns([2, 1])
    with chart_col:
        st.subheader("Trade Performance")
        lookback = st.selectbox("Lookback period", ["24h", "7d", "30d", "90d"], index=1)
        render_chart_placeholder()
        st.caption(f"Performance and execution quality for the last {lookback} will appear here once data is connected.")
    with info_col:
        st.subheader("Trade Summary")
        st.info("Trade history is not available yet. When data is connected, this section will include execution timing, slippage, and realized PnL.")
        st.write("- Best trade: pending")
        st.write("- Worst trade: pending")
        st.write("- Average hold time: pending")
        st.multiselect("Trade tags", ["Scalp", "Swing", "Breakout", "Mean Reversion"], default=["Scalp", "Breakout"])
        st.button("Refresh trades", use_container_width=True)

    st.divider()

    st.subheader("Recent Trades")
    render_table_placeholder()

    st.divider()

    notes_col1, notes_col2 = st.columns([2, 1])
    with notes_col1:
        st.subheader("Execution Notes")
        st.text_area(
            "Trade notes",
            value="No live trade history is available yet. Once filled trades are connected, this panel will show fill prices, slippage, realized PnL, and timestamps.",
            height=180,
        )
    with notes_col2:
        st.subheader("Trade Filters")
        st.checkbox("Show only profitable trades", value=False)
        st.checkbox("Include partial fills", value=True)
        st.checkbox("Include fees", value=True)
        st.button("Export trade log", use_container_width=True)