import streamlit as st


def render_table_placeholder() -> None:
    st.table(
        [
            {"symbol": "BTCUSDT", "side": "LONG", "size": 0.0},
            {"symbol": "ETHUSDT", "side": "SHORT", "size": 0.0},
        ]
    )