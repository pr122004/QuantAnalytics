import streamlit as st
import pandas as pd

#KPI - Hedge Ratio, Rolling Correlation, Latest Z-Score

def render_kpis(beta, corr, z, window):
    k1, k2, k3 = st.columns(3)

    k1.metric("Hedge Ratio (β)", f"{beta:.4f}")

    k2.metric(
        f"Rolling Corr ({window})",
        "N/A" if pd.isna(corr) else f"{corr:.3f}",
    )

    k3.metric(
        "Latest Z-Score",
        "N/A" if pd.isna(z) else f"{z:.3f}",
    )
