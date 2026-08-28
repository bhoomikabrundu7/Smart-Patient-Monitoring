import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def render_health_trends(history, abnormal=False):
    """
    Plot ONLY readings received from the backend.
    No values are generated or interpolated by the dashboard.

    The chart uses the real timestamp when available and shows
    the most recent 10 minutes of stored sensor data.
    """

    if not history:
        st.markdown(
            """
            <div class="cm-chart-empty">
                Waiting for live Wokwi / ESP32 sensor readings...
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    df = pd.DataFrame(history)

    required = ["heart_rate", "temperature", "spo2"]
    for col in required:
        if col not in df.columns:
            df[col] = None
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Timestamp is important: the chart must not pretend that
    # two readings arrived at equal time intervals.
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(
            df["timestamp"], errors="coerce", utc=True
        )
        df = df.sort_values("timestamp")
        latest_time = df["timestamp"].max()

        if pd.notna(latest_time):
            cutoff = latest_time - pd.Timedelta(minutes=10)
            df = df[df["timestamp"] >= cutoff]

            x = df["timestamp"].dt.tz_convert(None)
            x_title = "Time"
        else:
            x = list(range(len(df)))
            x_title = "Reading"
    else:
        x = list(range(len(df)))
        x_title = "Reading"

    df = df.dropna(subset=required, how="all").tail(120).reset_index(drop=True)

    if df.empty:
        st.markdown(
            '<div class="cm-chart-empty">Waiting for valid sensor readings...</div>',
            unsafe_allow_html=True,
        )
        return

    # Rebuild x after filtering.
    if "timestamp" in df.columns and df["timestamp"].notna().any():
        x = df["timestamp"].dt.tz_convert(None)
        x_title = "Time"
    else:
        x = list(range(len(df)))
        x_title = "Reading"

    if abnormal:
        bg = "#17080b"
        grid = "#54252d"
        text = "#f5e1e4"
        heart_color = "#ff4050"
        temp_color = "#ff9b3d"
        spo2_color = "#8d70ff"
    else:
        bg = "#ffffff"
        grid = "#e2ebf2"
        text = "#173b55"
        heart_color = "#18a66f"
        temp_color = "#f19a22"
        spo2_color = "#7045e8"

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=df["heart_rate"],
            mode="lines+markers",
            name="Heart Rate (BPM)",
            line=dict(color=heart_color, width=3),
            marker=dict(size=5),
            connectgaps=False,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=df["temperature"],
            mode="lines+markers",
            name="Temperature (°C)",
            line=dict(color=temp_color, width=3),
            marker=dict(size=5),
            connectgaps=False,
            yaxis="y2",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=df["spo2"],
            mode="lines+markers",
            name="SpO₂ (%)",
            line=dict(color=spo2_color, width=3),
            marker=dict(size=5),
            connectgaps=False,
            yaxis="y3",
        )
    )

    fig.update_layout(
        height=405,
        paper_bgcolor=bg,
        plot_bgcolor=bg,
        margin=dict(l=48, r=78, t=52, b=45),
        hovermode="x unified",
        uirevision="carematrix-health-trends",
        font=dict(color=text, size=11),
        legend=dict(
            orientation="h",
            x=0,
            y=1.12,
            font=dict(size=10),
        ),
        xaxis=dict(
            title=x_title,
            showgrid=False,
            color=text,
            fixedrange=True,
        ),
        yaxis=dict(
            title="Heart Rate (BPM)",
            showgrid=True,
            gridcolor=grid,
            zeroline=False,
            color=heart_color,
            fixedrange=True,
        ),
        yaxis2=dict(
            title="Temperature (°C)",
            overlaying="y",
            side="right",
            showgrid=False,
            color=temp_color,
            fixedrange=True,
        ),
        yaxis3=dict(
            title="SpO₂ (%)",
            overlaying="y",
            side="right",
            position=0.94,
            showgrid=False,
            color=spo2_color,
            fixedrange=True,
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
            "scrollZoom": False,
        },
        key="carematrix_health_trends",
    )

    # Be explicit when the backend has only supplied a small number of points.
    if len(df) < 3:
        st.caption(
            f"Live data received: {len(df)} reading(s). "
            "The graph does not create artificial points."
        )
