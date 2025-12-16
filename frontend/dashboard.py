import streamlit as st
import pandas as pd

from frontend.controls import sidebar_controls
from frontend.alerts_view import show_alerts

from frontend.views.kpi_view import render_kpis
from frontend.views.prices_view import render_prices_tab
from frontend.views.signals_view import render_signals_tab
from frontend.views.stats_view import render_stats_tab

from backend.analytics.regression import hedge_ratio
from backend.analytics.spread import compute_spread
from backend.analytics.zscore import compute_zscore
from backend.analytics.correlation import rolling_correlation


def run_dashboard(service):
    st.set_page_config(
        page_title="Quant Analytics Dashboard",
        layout="wide",
    )

    st.title("📊 Real-Time Quant Analytics Dashboard")
    st.caption(
        "Research-oriented real-time analytics for pair trading & mean-reversion"
    )

    controls = sidebar_controls()

    df_y = service.get_resampled_data(
        controls["symbol_y"], controls["timeframe"]
    )
    df_x = service.get_resampled_data(
        controls["symbol_x"], controls["timeframe"]
    )

    if df_y.empty or df_x.empty:
        st.info("⏳ Waiting for sufficient market data...")
        return

    df = (
        pd.merge(
            df_y, df_x, on="ts", suffixes=("_y", "_x")
        )
        .set_index("ts")
        .sort_index()
    )

    beta = hedge_ratio(df["price_y"], df["price_x"])
    df["spread"] = compute_spread(
        df["price_y"], df["price_x"], beta
    )
    df["zscore"] = compute_zscore(
        df["spread"], controls["window"]
    )
    df["corr"] = rolling_correlation(
        df["price_y"], df["price_x"], controls["window"]
    )

    latest_z = df["zscore"].iloc[-1]
    latest_corr = df["corr"].iloc[-1]

    render_kpis(
        beta,
        latest_corr,
        latest_z,
        controls["window"],
    )
    # alerts
    show_alerts(
        z=latest_z,
        z_threshold=controls["z_threshold"],
        corr=latest_corr,
        spread=df["spread"],
        window=controls["window"],
    )

    tab_prices, tab_signals, tab_stats = st.tabs(
        ["📈 Prices", "📉 Mean Reversion", "📊 Stats & Tests"]
    )

    with tab_prices:
        render_prices_tab(
            df_y,
            df_x,
            controls["symbol_y"],
            controls["symbol_x"],
        )

    with tab_signals:
        render_signals_tab(
            df,
            controls["window"],
            latest_z,
            latest_corr,
            controls["z_threshold"] 
        )

    with tab_stats:
        render_stats_tab(
            df,
            beta,
            latest_corr,
            latest_z,
        )

    st.divider()
    st.download_button(
        "⬇️ Download Analytics CSV",
        df.reset_index().to_csv(index=False),
        file_name="analytics_output.csv",
        mime="text/csv",
    )
