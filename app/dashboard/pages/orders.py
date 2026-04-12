import streamlit as st

from app.dashboard.components.tables import render_table_placeholder


def _calculate_notional(quantity: float, price: float, order_type: str) -> float:
    if quantity <= 0:
        return 0.0
    if order_type == "Market":
        return 0.0
    return quantity * price


def render_orders() -> None:
    st.header("Orders")
    st.caption("Prepare orders, review validation, and monitor active execution status.")

    summary_col1, summary_col2, summary_col3 = st.columns(3)
    summary_col1.metric("Open Orders", "0")
    summary_col2.metric("Pending Cancels", "0")
    summary_col3.metric("Rejected", "0")

    st.divider()

    entry_col, review_col = st.columns([2, 1])
    with entry_col:
        st.subheader("Create Order")
        symbol = st.selectbox("Symbol", ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"], index=0)
        side = st.radio("Side", ["Buy", "Sell"], horizontal=True)
        order_type = st.selectbox("Order Type", ["Market", "Limit", "Stop Market", "Stop Limit"], index=0)
        quantity = st.number_input("Quantity", min_value=0.0, value=0.001, step=0.001, format="%.6f")
        price_required = order_type in {"Limit", "Stop Limit"}
        price = st.number_input(
            "Price",
            min_value=0.0,
            value=0.0,
            step=0.1,
            format="%.2f",
            disabled=not price_required,
        )
        leverage = st.slider("Leverage", min_value=1, max_value=20, value=3)
        risk_pct = st.slider("Risk per trade (%)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
        stop_loss = st.number_input("Stop loss price", min_value=0.0, value=0.0, step=0.1, format="%.2f")
        take_profit = st.number_input("Take profit price", min_value=0.0, value=0.0, step=0.1, format="%.2f")
        time_in_force = st.selectbox("Time in force", ["GTC", "IOC", "FOK"], index=0)
        reduce_only = st.checkbox("Reduce only", value=False)

        order_price = price if price_required else 0.0
        notional = _calculate_notional(quantity, order_price if order_price > 0 else 0.0, order_type)
        margin_estimate = notional / leverage if notional > 0 else 0.0

        st.subheader("Order Preview")
        st.write(f"- Symbol: {symbol}")
        st.write(f"- Side: {side}")
        st.write(f"- Type: {order_type}")
        st.write(f"- Quantity: {quantity:.6f}")
        if price_required:
            st.write(f"- Price: {price:.2f}")
        st.write(f"- Leverage: {leverage}x")
        st.write(f"- Risk per trade: {risk_pct:.1f}%")
        st.write(f"- Estimated margin: {margin_estimate:.2f}")
        st.write(f"- Time in force: {time_in_force}")
        st.write(f"- Reduce only: {'Yes' if reduce_only else 'No'}")

        preview_col, submit_col = st.columns(2)
        preview_clicked = preview_col.button("Preview order", use_container_width=True)
        submit_clicked = submit_col.button("Submit order", use_container_width=True)

        validation_messages = []
        if quantity <= 0:
            validation_messages.append("Quantity must be greater than zero.")
        if price_required and price <= 0:
            validation_messages.append("A positive price is required for this order type.")
        if stop_loss > 0 and take_profit > 0 and side == "Buy" and stop_loss >= take_profit:
            validation_messages.append("For buy orders, stop loss should be below take profit.")
        if stop_loss > 0 and take_profit > 0 and side == "Sell" and stop_loss <= take_profit:
            validation_messages.append("For sell orders, stop loss should be above take profit.")

        if validation_messages:
            st.error("Order validation failed.")
            for message in validation_messages:
                st.write(f"- {message}")
        else:
            st.success("Order configuration is valid.")

        if preview_clicked:
            st.info("Preview generated. Review the configuration above before submitting.")
        if submit_clicked:
            if validation_messages:
                st.warning("Order cannot be submitted until validation issues are resolved.")
            else:
                st.success("Order submission is not wired to execution yet. This layout is ready for backend integration.")

    with review_col:
        st.subheader("Risk / Exposure")
        st.metric("Leverage", f"{leverage}x")
        st.metric("Risk per trade", f"{risk_pct:.1f}%")
        st.metric("Estimated margin", f"{margin_estimate:.2f}")
        st.metric("Estimated notional", f"{notional:.2f}" if notional > 0 else "Market order")
        st.info("Use these controls to prepare an order. Execution is intentionally disabled until the trading service is connected.")
        st.caption("Suggested checks before submitting: symbol, size, price, leverage, and protective exits.")

    st.divider()

    st.subheader("Active Orders")
    render_table_placeholder()

    st.divider()

    notes_col1, notes_col2 = st.columns([2, 1])
    with notes_col1:
        st.subheader("Execution Notes")
        st.text_area(
            "Order status log",
            value="No live order data is available yet. When connected, this section will show order lifecycle updates, fills, and cancellation reasons.",
            height=180,
        )
    with notes_col2:
        st.subheader("Order Actions")
        st.button("Refresh orders", use_container_width=True)
        st.button("Cancel all", use_container_width=True)
        st.button("Sync with exchange", use_container_width=True)
        st.warning("Action buttons are placeholders until backend handlers are connected.")