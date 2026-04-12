import streamlit as st


def render_settings() -> None:
    st.header("Settings")
    st.caption("Dashboard preferences and bot configuration summary.")

    bot_col1, bot_col2 = st.columns(2)
    with bot_col1:
        st.subheader("Bot Settings")
        st.checkbox("Enable live trading", value=False, disabled=True)
        st.checkbox("Enable websocket feed", value=True, disabled=True)
        st.checkbox("Auto-reconnect", value=True, disabled=True)
        st.selectbox("Default timeframe", ["1m", "5m", "15m", "1h"], index=1, disabled=True)
        st.slider("Max concurrent positions", min_value=1, max_value=10, value=3, disabled=True)
    with bot_col2:
        st.subheader("Dashboard Settings")
        st.checkbox("Compact layout", value=False, disabled=True)
        st.checkbox("Show advanced metrics", value=True, disabled=True)
        st.checkbox("Dark mode", value=True, disabled=True)
        st.selectbox("Refresh interval", ["5s", "15s", "30s", "60s"], index=1, disabled=True)
        st.checkbox("Show order confirmations", value=True, disabled=True)

    st.divider()

    config_col1, config_col2 = st.columns([2, 1])
    with config_col1:
        st.subheader("Configuration Details")
        st.text_area(
            "Current runtime notes",
            value="Settings are currently read-only placeholders. Hook these controls to the settings service when configuration persistence is available.",
            height=180,
        )
    with config_col2:
        st.subheader("Configuration Status")
        status_col1, status_col2, status_col3 = st.columns(3)
        status_col1.metric("Config Loaded", "Yes")
        status_col2.metric("Secrets Loaded", "Partial")
        status_col3.metric("Runtime Mode", "Preview")
        st.button("Reload configuration", use_container_width=True)
        st.button("Validate secrets", use_container_width=True)
        st.button("Export config snapshot", use_container_width=True)
        st.info("Settings are currently read-only placeholders. Hook these controls to the settings service when configuration persistence is available.")