import streamlit as st
import pandas as pd
from backend.analytics.adf_test import adf_test


def render_stats_tab(df, beta, corr, z):
    st.subheader("Statistical Diagnostics")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**ADF Stationarity Test (Spread)**")
        run_adf = st.button(
            "Run ADF Test", key="run_adf_tab"
        )

        if run_adf:
            result = adf_test(df["spread"])
            st.write(
                {
                    "ADF Statistic": round(
                        result["adf_statistic"], 4
                    ),
                    "P-Value": round(result["p_value"], 4),
                }
            )
        else:
            st.caption(
                "Run the test to evaluate spread stationarity."
            )

    with c2:
        st.markdown("**Latest Metrics Snapshot**")
        st.write(
            {
                "Hedge Ratio (β)": round(beta, 4),
                "Rolling Correlation": None
                if pd.isna(corr)
                else round(corr, 4),
                "Latest Z-Score": None
                if pd.isna(z)
                else round(z, 4),
            }
        )
