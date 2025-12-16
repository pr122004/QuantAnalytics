import streamlit as st
import pandas as pd


def flash_alert(message, level="warning"):
   
    # alert levels: info | warning | error
    
    if level == "error":
        st.error(message)
    elif level == "warning":
        st.warning(message)
    else:
        st.info(message)


def show_alerts(
    z,
    z_threshold,
    corr,
    spread,
    window,
    adf_pvalue=None,
):
   

    # Z-Score Alert
    if not pd.isna(z) and abs(z) >= z_threshold:
        flash_alert(
            f"🚨 Z-Score Alert: |z| = {z:.2f} exceeds threshold ({z_threshold})",
            level="error",
        )

    # Correlation Breakdown 
    if not pd.isna(corr) and corr < 0.5:
        flash_alert(
            f"⚠️ Correlation Weakening: rolling corr = {corr:.2f}",
            level="warning",
        )

    # Spread Volatility Spike
    if len(spread) > window:
        recent_vol = spread[-window:].std()
        long_vol = spread.std()

        if recent_vol > 2 * long_vol:
            flash_alert(
                "⚠️ Spread Volatility Spike detected — possible regime change",
                level="warning",
            )

    # Stationarity Warning
    if adf_pvalue is not None and adf_pvalue > 0.05:
        flash_alert(
            f"⚠️ Stationarity Risk: ADF p-value = {adf_pvalue:.3f}",
            level="info",
        )
