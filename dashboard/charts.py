import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def render_health_chart(history):

    if not history:
        st.info("Waiting for more sensor readings...")
        return

    df = pd.DataFrame(history)

    if df.empty:
        st.info("Waiting for more sensor readings...")
        return

    for column in [
        "heart_rate",
        "temperature",
        "spo2"
    ]:
        if column not in df.columns:
            df[column] = None

    df = df.tail(30).reset_index(drop=True)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=list(range(1, len(df) + 1)),
            y=df["heart_rate"],
            mode="lines+markers",
            name="Heart Rate",
            line=dict(width=3)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=list(range(1, len(df) + 1)),
            y=df["spo2"],
            mode="lines+markers",
            name="SpO₂",
            line=dict(width=3)
        )
    )

    fig.update_layout(
        title="Health Trends",
        height=350,

        margin=dict(
            l=20,
            r=20,
            t=55,
            b=30
        ),

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="#dce8f5",
            family="Inter, sans-serif"
        ),

        legend=dict(
            orientation="h",
            y=1.08,
            x=0
        ),

        xaxis=dict(
            title="Reading",
            gridcolor="rgba(255,255,255,0.06)"
        ),

        yaxis=dict(
            title="Value",
            gridcolor="rgba(255,255,255,0.06)"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )