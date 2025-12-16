import streamlit as st
from frontend.charts import spread_zscore_chart
from frontend.interpretation import (
    interpret_zscore,
    interpret_correlation,
    next_steps_guidance,
)

#Interpretation of Singals to help user make decisions

def render_signals_tab(
    df,
    window,
    latest_z,
    latest_corr,
    z_threshold,
):
    st.subheader("Spread & Z-Score")

    if df["zscore"].isna().all():
        st.info(
            f"Z-score unavailable — need at least {window} data points."
        )

    st.plotly_chart(
        spread_zscore_chart(df),
        width="stretch",
        key="spread_zscore_chart",
    )

    st.divider()
    st.subheader("Signal Interpretation")

    st.markdown("**Current Spread Context**")
    st.write(
        interpret_zscore(latest_z, z_threshold)
    )

    st.markdown("**Signal Confidence**")
    st.write(
        interpret_correlation(latest_corr)
    )

    st.markdown("**Research Guidance (Next Steps)**")
    steps = next_steps_guidance(
        latest_z,
        latest_corr,
        z_threshold,
    )

    for step in steps:
        st.write(f"• {step}")
