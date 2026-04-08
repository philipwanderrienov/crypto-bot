import streamlit as st


def render_metrics_placeholder() -> None:
    col1, col2, col3 = st.columns(3)
    col1.metric("Equity", "0.00")
    col2.metric("PnL", "0.00")
    col3.metric("Win Rate", "0%")
