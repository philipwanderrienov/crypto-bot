import streamlit as st

from app.dashboard.components.charts import render_chart_placeholder
from app.dashboard.components.metrics import render_metrics_placeholder
from app.dashboard.components.tables import render_table_placeholder


def render_overview() -> None:
    st.header("Overview")
    st.caption("Realtime bot summary, market state, and the latest signal context.")

    top_col1, top_col2 = st.columns([2, 1])
    with top_col1:
        st.subheader("Account Snapshot")
        render_metrics_placeholder()
    with top_col2:
        st.subheader("Status")
        st.info("No live snapshot is connected yet. Once the bot is running, key execution and market details will appear here.")
        st.write("- Bot state: pending")
        st.write("- Market snapshot: pending")
        st.write("- Strategy mode: pending")

    st.divider()

    chart_col, side_col = st.columns([2, 1])
    with chart_col:
        st.subheader("Price / Performance")
        render_chart_placeholder()
    with side_col:
        st.subheader("Quick Actions")
        refresh_interval = st.selectbox(
            "Auto refresh",
            ["Off", "5 seconds", "15 seconds", "30 seconds", "60 seconds"],
            index=2,
        )
        st.button("Refresh snapshot", use_container_width=True)
        st.button("Reload bot state", use_container_width=True)
        st.button("Open settings", use_container_width=True)
        st.caption(f"Refresh cadence: {refresh_interval}")
        st.warning("These controls are placeholders until dashboard actions are wired to backend callbacks.")

    st.divider()

    left_col, right_col = st.columns([2, 1])
    with left_col:
        st.subheader("Recent Activity")
        render_table_placeholder()
    with right_col:
        st.subheader("Signal Notes")
        signal_filter = st.multiselect(
            "Show context for",
            ["Entries", "Exits", "Risk", "Warnings"],
            default=["Entries", "Risk", "Warnings"],
        )
        st.text_area(
            "Latest signal summary",
            value="No live signal summary is available yet. This area will show strategy observations, trade rationale, and key alerts.",
            height=180,
        )
        st.caption(f"Visible context: {', '.join(signal_filter) if signal_filter else 'None'}")