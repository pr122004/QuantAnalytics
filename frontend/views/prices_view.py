import streamlit as st
from frontend.charts import price_chart


# Render the Prices tab with price charts for two assets
def render_prices_tab(df_y, df_x, sym_y, sym_x):
    st.subheader("Asset Prices")

    c1, c2 = st.columns(2)

    with c1:
        st.plotly_chart(
            price_chart(df_y, f"{sym_y} Price"),
            width="stretch",
            key="price_y_chart",
        )

    with c2:
        st.plotly_chart(
            price_chart(df_x, f"{sym_x} Price"),
            width="stretch",
            key="price_x_chart",
        )
