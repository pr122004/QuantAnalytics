import streamlit as st

# Sidebar controls for user input parameters

def sidebar_controls():
    st.sidebar.header("Controls")

    symbol_y = st.sidebar.selectbox(
        "Asset Y (dependent)",
        ["BTCUSDT", "ETHUSDT"],
        index=0,
    )

    symbol_x = st.sidebar.selectbox(
        "Asset X (hedge)",
        ["ETHUSDT", "BTCUSDT"],
        index=1,
    )

    timeframe = st.sidebar.selectbox(
        "Timeframe",
        ["1s", "1m", "5m"],
        index=1,
    )

    window = st.sidebar.slider(
        "Rolling Window",
        min_value=10,
        max_value=100,
        value=20,
        step=5,
    )

    z_threshold = st.sidebar.slider(
        "Z-score Alert Threshold",
        min_value=1.0,
        max_value=3.0,
        value=2.0,
        step=0.1,
    )

 

    return {
        "symbol_y": symbol_y,
        "symbol_x": symbol_x,
        "timeframe": timeframe,
        "window": window,
        "z_threshold": z_threshold,
    }
