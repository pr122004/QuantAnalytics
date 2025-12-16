import plotly.express as px
import plotly.graph_objects as go


def price_chart(df, title: str):
    """
    Line chart for price over time.
    Expects columns: ['ts', 'price']
    """
    fig = px.line(
        df,
        x="ts",
        y="price",
        title=title,
        template="plotly_dark",
    )

    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title="Time",
        yaxis_title="Price",
        hovermode="x unified",
    )

    return fig


def spread_zscore_chart(df):
    """
    Dual-axis chart:
    - Spread (left axis)
    - Z-score (right axis)

    Expects index = timestamp
    Columns: ['spread', 'zscore']
    """
    fig = go.Figure()

    # Spread
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["spread"],
            name="Spread",
            mode="lines",
            line=dict(width=2),
        )
    )

    # Z-score (handle NaNs safely)
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["zscore"],
            name="Z-score",
            mode="lines",
            yaxis="y2",
            line=dict(width=2, dash="dot"),
        )
    )

    fig.update_layout(
        title="Spread & Z-score",
        template="plotly_dark",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(title="Time"),
        yaxis=dict(title="Spread"),
        yaxis2=dict(
            title="Z-score",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )

    return fig
