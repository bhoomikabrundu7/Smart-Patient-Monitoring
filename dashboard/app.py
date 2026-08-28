import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

# ============================================================
# CAREMATRIX - FINAL LOCAL LIVE DASHBOARD
#
# Wokwi ESP32 -> local Flask server.py -> Streamlit
# No Render / ThingSpeak / bridge.py required.
# ============================================================

API_BASE = "http://127.0.0.1:5000"
LATEST_URL = f"{API_BASE}/latest"
HISTORY_URL = f"{API_BASE}/history"

st.set_page_config(
    page_title="CareMatrix | Smart Patient Monitoring",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# STYLE
# ============================================================

st.markdown("""
<style>
.stApp {
    background: #080a0d;
    color: #f5e8eb;
}
.block-container {
    max-width: 1450px;
    padding: 28px 38px 45px 38px;
}
#MainMenu, footer {
    visibility: hidden;
}
.cm-top {
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:20px;
    margin-bottom:24px;
}
.cm-brand {
    display:flex;
    align-items:center;
    gap:14px;
}
.cm-logo {
    width:52px;
    height:52px;
    border-radius:15px;
    display:flex;
    align-items:center;
    justify-content:center;
    background:#15191e;
    border:1px solid #292f36;
    font-size:25px;
}
.cm-title {
    font-size:29px;
    font-weight:800;
    color:#f7eef0;
    letter-spacing:-1px;
}
.cm-title span {
    color:#e63848;
}
.cm-subtitle {
    color:#927d83;
    font-size:12px;
    margin-top:2px;
}
.cm-live {
    padding:10px 15px;
    border-radius:999px;
    background:#161b1f;
    border:1px solid #293038;
    color:#20c975;
    font-size:11px;
    font-weight:800;
}
.cm-critical {
    background:linear-gradient(135deg,#321218,#211014);
    border:1px solid #61232d;
    border-radius:18px;
    padding:22px 25px;
    margin-bottom:20px;
}
.cm-critical-title {
    font-size:21px;
    font-weight:800;
    color:#ff5362;
}
.cm-critical-text {
    margin-top:6px;
    color:#d6b9bf;
    font-size:13px;
}
.cm-normal-banner {
    background:linear-gradient(135deg,#10251b,#0d1914);
    border:1px solid #1e5b3c;
    border-radius:18px;
    padding:22px 25px;
    margin-bottom:20px;
}
.cm-normal-title {
    color:#20d27c;
    font-size:21px;
    font-weight:800;
}
.cm-status-panel {
    background:#101318;
    border:1px solid #252c34;
    border-radius:18px;
    padding:20px 22px;
    min-height:105px;
}
.cm-label {
    color:#8e7b81;
    font-size:10px;
    font-weight:800;
    letter-spacing:1px;
}
.cm-status-danger {
    color:#ff4c5b;
    font-size:20px;
    font-weight:800;
    margin-top:6px;
}
.cm-status-safe {
    color:#20c975;
    font-size:20px;
    font-weight:800;
    margin-top:6px;
}
.cm-description {
    color:#927f85;
    font-size:11px;
    margin-top:7px;
    line-height:1.5;
}
.cm-section-title {
    font-size:20px;
    font-weight:800;
    color:#f5e8eb;
    margin:23px 0 12px;
}
.cm-card {
    background:#101318;
    border:1px solid #252c34;
    border-radius:18px;
    padding:20px;
    min-height:150px;
}
.cm-danger {
    border-color:#63242e;
    background:linear-gradient(145deg,#141114,#111216);
}
.cm-safe-card {
    border-color:#23553c;
}
.cm-card-inner {
    display:flex;
    gap:16px;
    align-items:flex-start;
}
.cm-icon {
    width:46px;
    height:46px;
    border-radius:13px;
    background:#191d22;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:21px;
    flex-shrink:0;
}
.cm-spo2-icon {
    color:#6fd6ff;
    font-size:18px;
    font-weight:900;
    letter-spacing:-1px;
}
.cm-card-title {
    color:#8e7b81;
    font-size:10px;
    font-weight:800;
    letter-spacing:1px;
}
.cm-value {
    color:#f7eef0;
    font-size:31px;
    font-weight:800;
    line-height:1.15;
    margin-top:5px;
}
.cm-unit {
    color:#9a858b;
    font-size:12px;
    font-weight:600;
}
.cm-warning {
    color:#ff4d5c;
    font-size:10px;
    font-weight:800;
    margin-top:9px;
}
.cm-normal {
    color:#20c975;
    font-size:10px;
    font-weight:800;
    margin-top:9px;
}
.cm-safe {
    color:#20c975;
    font-size:25px;
    font-weight:800;
    margin-top:5px;
}
.cm-fall-danger {
    color:#ff4d5c;
    font-size:25px;
    font-weight:800;
    margin-top:5px;
}
.cm-panel {
    background:#101318;
    border:1px solid #252c34;
    border-radius:18px;
    overflow:hidden;
    margin-top:20px;
}
.stPlotlyChart {
    background: #101318;
    border: 1px solid #252c34;
    border-radius: 14px;
    padding: 4px;
    overflow: hidden;
}
.cm-panel-header {
    padding:19px 21px 10px;
}
.cm-panel-title {
    color:#f5e8eb;
    font-size:17px;
    font-weight:800;
}
.cm-panel-subtitle {
    color:#8e7b81;
    font-size:10px;
    margin-top:4px;
}
.cm-alert {
    background:#191216;
    border-left:3px solid #e63848;
    border-radius:8px;
    padding:11px 13px;
    margin:8px 20px;
    color:#f0d9dd;
    font-size:12px;
    font-weight:600;
}
.cm-action {
    padding:9px 0;
    color:#bda9ae;
    font-size:12px;
}
.cm-footer {
    margin-top:20px;
    background:#101318;
    border:1px solid #252c34;
    border-radius:18px;
    padding:20px;
}
.cm-live-dot {
    color:#20c975;
    font-weight:800;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# API HELPERS
# ============================================================

def get_json(url):
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        return response.json(), None
    except requests.RequestException as exc:
        return None, str(exc)


def clean_latest(data):
    if not isinstance(data, dict):
        data = {}

    return {
        "temperature": float(data.get("temperature", 0)),
        "heart_rate": int(data.get("heart_rate", 0)),
        "spo2": int(data.get("spo2", 0)),
        "fall": bool(data.get("fall", False)),
        "mode": str(data.get("mode", "WAITING")).upper(),
        "status": str(data.get("status", "WAITING")).upper(),
        "alerts": data.get("alerts", []) or [],
    }


def clean_history(data):
    if not isinstance(data, list):
        return []

    rows = []

    for item in data:
        if not isinstance(item, dict):
            continue

        rows.append({
            "temperature": float(item.get("temperature", 0)),
            "heart_rate": int(item.get("heart_rate", 0)),
            "spo2": int(item.get("spo2", 0)),
            "fall": bool(item.get("fall", False)),
            "mode": str(item.get("mode", "NORMAL")).upper(),
            "status": str(item.get("status", "NORMAL")).upper(),
            "alerts": item.get("alerts", []) or [],
            "timestamp": item.get("timestamp", ""),
        })

    return rows


# ============================================================
# LIVE DASHBOARD
# ============================================================

@st.fragment(run_every=2)
def render_dashboard():

    latest_raw, latest_error = get_json(LATEST_URL)
    history_raw, history_error = get_json(HISTORY_URL)

    latest = clean_latest(latest_raw)
    history = clean_history(history_raw)

    is_abnormal = (
        latest["status"] == "ABNORMAL"
        or latest["mode"] == "ABNORMAL"
        or latest["fall"]
        or bool(latest["alerts"])
    )

    # ========================================================
    # HEADER
    # ========================================================

    st.markdown(
        '<div class="cm-top">'
        '<div class="cm-brand">'
        '<div class="cm-logo">❤️</div>'
        '<div>'
        '<div class="cm-title">Care<span>Matrix</span></div>'
        '<div class="cm-subtitle">Smart Patient Monitoring</div>'
        '</div>'
        '</div>'
        '<div class="cm-live">● LIVE MONITORING</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    if latest_error or history_error:
        st.error(
            "Cannot connect to local server.py. "
            "Make sure it is running on http://127.0.0.1:5000."
        )

    # ========================================================
    # MAIN STATUS
    # ========================================================

    if is_abnormal:
        st.markdown(
            '<div class="cm-critical">'
            '<div class="cm-critical-title">⚠️ CRITICAL ALERT</div>'
            '<div class="cm-critical-text">'
            'Abnormal vital signs detected. Immediate attention required.'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="cm-normal-banner">'
            '<div class="cm-normal-title">✓ PATIENT STABLE</div>'
            '<div class="cm-critical-text">'
            'Patient vital signs are currently within the normal range.'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    # ========================================================
    # STATUS / MODE
    # ========================================================

    col1, col2 = st.columns([2, 1])

    status_class = "cm-status-danger" if is_abnormal else "cm-status-safe"
    status_text = "CRITICAL ALERT" if is_abnormal else "NORMAL"

    with col1:
        st.markdown(
            '<div class="cm-status-panel">'
            '<div class="cm-label">PATIENT STATUS</div>'
            f'<div class="{status_class}">{status_text}</div>'
            '<div class="cm-description">'
            + (
                "Abnormal vital signs or fall activity detected."
                if is_abnormal
                else "Patient vital signs are currently stable."
            )
            + '</div></div>',
            unsafe_allow_html=True,
        )

    with col2:
        mode_class = "cm-status-danger" if latest["mode"] == "ABNORMAL" else "cm-status-safe"

        st.markdown(
            '<div class="cm-status-panel">'
            '<div class="cm-label">CURRENT MODE</div>'
            f'<div class="{mode_class}">{latest["mode"]}</div>'
            '<div class="cm-description">'
            'Live mode received from Wokwi / ESP32.'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    # ========================================================
    # PATIENT READINGS
    # ========================================================

    st.markdown(
        '<div class="cm-section-title">Current Patient Readings</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    hr_bad = latest["heart_rate"] > 100 or latest["heart_rate"] < 50
    temp_bad = latest["temperature"] > 37.5 or latest["temperature"] < 35
    spo2_bad = latest["spo2"] < 95

    with c1:
        st.markdown(
            '<div class="cm-card ' + ("cm-danger" if hr_bad else "") + '">'
            '<div class="cm-card-inner">'
            '<div class="cm-icon">❤️</div>'
            '<div>'
            '<div class="cm-card-title">HEART RATE</div>'
            f'<div class="cm-value">{latest["heart_rate"]} '
            '<span class="cm-unit">BPM</span></div>'
            f'<div class="{"cm-warning" if hr_bad else "cm-normal"}">'
            + ("⚠ HIGH / ABNORMAL" if hr_bad else "✓ NORMAL")
            + '</div></div></div></div>',
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            '<div class="cm-card ' + ("cm-danger" if temp_bad else "") + '">'
            '<div class="cm-card-inner">'
            '<div class="cm-icon">🌡</div>'
            '<div>'
            '<div class="cm-card-title">TEMPERATURE</div>'
            f'<div class="cm-value">{latest["temperature"]:.1f} '
            '<span class="cm-unit">°C</span></div>'
            f'<div class="{"cm-warning" if temp_bad else "cm-normal"}">'
            + ("⚠ ABNORMAL" if temp_bad else "✓ NORMAL")
            + '</div></div></div></div>',
            unsafe_allow_html=True,
        )

    with c3:
        # Use plain text O₂ instead of 🫁 so the icon works
        # even when the browser/OS has no lung emoji font.
        st.markdown(
            '<div class="cm-card ' + ("cm-danger" if spo2_bad else "") + '">'
            '<div class="cm-card-inner">'
            '<div class="cm-icon cm-spo2-icon">O₂</div>'
            '<div>'
            '<div class="cm-card-title">SpO₂</div>'
            f'<div class="cm-value">{latest["spo2"]} '
            '<span class="cm-unit">%</span></div>'
            f'<div class="{"cm-warning" if spo2_bad else "cm-normal"}">'
            + ("⚠ LOW / ABNORMAL" if spo2_bad else "✓ NORMAL")
            + '</div></div></div></div>',
            unsafe_allow_html=True,
        )

    with c4:
        if latest["fall"]:
            st.markdown(
                '<div class="cm-card cm-danger">'
                '<div class="cm-card-inner">'
                '<div class="cm-icon">🚶</div>'
                '<div>'
                '<div class="cm-card-title">FALL STATUS</div>'
                '<div class="cm-fall-danger">FALL DETECTED</div>'
                '<div class="cm-warning">⚠ IMMEDIATE ATTENTION</div>'
                '</div></div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="cm-card cm-safe-card">'
                '<div class="cm-card-inner">'
                '<div class="cm-icon">🚶</div>'
                '<div>'
                '<div class="cm-card-title">FALL STATUS</div>'
                '<div class="cm-safe">SAFE</div>'
                '<div class="cm-normal">✓ NO FALL DETECTED</div>'
                '</div></div></div>',
                unsafe_allow_html=True,
            )

    # ========================================================
    # HEALTH TRENDS - PROFESSIONAL LIVE CHARTS
    # ========================================================

    st.markdown(
        '<div class="cm-panel">'
        '<div class="cm-panel-header">'
        '<div class="cm-panel-title">Health Trends</div>'
        '<div class="cm-panel-subtitle">'
        'Live readings from Wokwi / ESP32 • Last 10 minutes'
        '</div></div></div>',
        unsafe_allow_html=True,
    )

    if history:
        df = pd.DataFrame(history)
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["timestamp"]).sort_values("timestamp")

        if not df.empty:
            newest = df["timestamp"].max()
            recent = df[
                df["timestamp"] >= newest - pd.Timedelta(minutes=10)
            ].copy()

            if recent.empty:
                recent = df.tail(30).copy()

            # Keep the graph readable if the simulator has produced a lot
            # of readings in a short period.
            recent = recent.tail(60)

            def professional_chart(
                data,
                column,
                title,
                unit,
                y_range=None,
                threshold=None,
                threshold_label=None,
            ):
                fig = go.Figure()

                fig.add_trace(
                    go.Scatter(
                        x=data["timestamp"],
                        y=data[column],
                        mode="lines+markers",
                        name=title,
                        line=dict(width=2.5, shape="spline"),
                        marker=dict(size=5),
                        hovertemplate=(
                            "%{x|%H:%M:%S}<br>"
                            f"<b>{title}</b>: %{{y:.1f}} {unit}"
                            "<extra></extra>"
                        ),
                    )
                )

                if threshold is not None:
                    fig.add_hline(
                        y=threshold,
                        line_dash="dash",
                        annotation_text=threshold_label or "Limit",
                        annotation_position="top right",
                    )

                fig.update_layout(
                    height=310,
                    margin=dict(l=12, r=12, t=42, b=12),
                    title=dict(
                        text=f"<b>{title}</b> <span style='font-size:11px'>({unit})</span>",
                        x=0.02,
                        xanchor="left",
                        y=0.96,
                        yanchor="top",
                    ),
                    hovermode="x unified",
                    showlegend=False,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(size=11),
                    xaxis=dict(
                        title=None,
                        showgrid=False,
                        showline=False,
                        fixedrange=True,
                        tickformat="%H:%M",
                    ),
                    yaxis=dict(
                        title=None,
                        range=y_range,
                        showgrid=True,
                        gridcolor="rgba(140,150,165,0.16)",
                        zeroline=False,
                        fixedrange=True,
                    ),
                )

                return fig

            # Use sensible clinical-display ranges so the small changes in
            # the simulator are visible instead of being flattened.
            temp_min = min(float(recent["temperature"].min()) - 0.5, 35)
            temp_max = max(float(recent["temperature"].max()) + 0.5, 40)

            hr_min = max(40, float(recent["heart_rate"].min()) - 10)
            hr_max = min(160, float(recent["heart_rate"].max()) + 10)

            spo2_min = max(80, float(recent["spo2"].min()) - 5)
            spo2_max = 100

            chart1, chart2, chart3 = st.columns(3)

            with chart1:
                st.plotly_chart(
                    professional_chart(
                        recent,
                        "temperature",
                        "🌡 Temperature",
                        "°C",
                        (temp_min, temp_max),
                        37.5,
                        "High limit",
                    ),
                    use_container_width=True,
                    config={
                        "displayModeBar": False,
                        "responsive": True,
                    },
                )

            with chart2:
                st.plotly_chart(
                    professional_chart(
                        recent,
                        "heart_rate",
                        "❤️ Heart Rate",
                        "BPM",
                        (hr_min, hr_max),
                        100,
                        "High limit",
                    ),
                    use_container_width=True,
                    config={
                        "displayModeBar": False,
                        "responsive": True,
                    },
                )

            with chart3:
                st.plotly_chart(
                    professional_chart(
                        recent,
                        "spo2",
                        "O₂ SpO₂",
                        "%",
                        (spo2_min, spo2_max),
                        95,
                        "Minimum",
                    ),
                    use_container_width=True,
                    config={
                        "displayModeBar": False,
                        "responsive": True,
                    },
                )

            st.caption(
                "Charts show the most recent 10 minutes. Hover over a point for the exact reading and time."
            )
        else:
            st.info("Waiting for valid timestamps...")
    else:
        st.info("Waiting for sensor history from server.py...")

    # ========================================================
    # ALERTS + ACTIONS
    # ========================================================

    left, right = st.columns([1.25, 1])

    with left:
        st.markdown(
            '<div class="cm-panel">'
            '<div class="cm-panel-header">'
            '<div class="cm-panel-title">Active Alerts</div>'
            '<div class="cm-panel-subtitle">'
            'Current patient safety notifications.'
            '</div></div></div>',
            unsafe_allow_html=True,
        )

        alerts = list(latest["alerts"])

        if latest["fall"] and "Fall detected" not in alerts:
            alerts.append("Fall detected")

        if alerts:
            for alert in alerts:
                st.markdown(
                    f'<div class="cm-alert">⚠ {alert}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                '<div class="cm-alert" style="border-left-color:#20b96d;">'
                '✓ No active alerts'
                '</div>',
                unsafe_allow_html=True,
            )

    with right:
        st.markdown(
            '<div class="cm-panel">'
            '<div class="cm-panel-header">'
            '<div class="cm-panel-title">⚠️ Alert Actions</div>'
            '<div class="cm-panel-subtitle">'
            'Patient attention required.'
            '</div></div></div>',
            unsafe_allow_html=True,
        )

        # Streamlit components are used here instead of a nested
        # HTML block, preventing raw HTML from appearing.
        st.markdown(
            '<div class="cm-action"><span style="color:#20b96d">●</span> '
            'Caretaker notified</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="cm-action"><span style="color:#e63848">●</span> '
            'Check patient immediately</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="cm-action">☎ Emergency contact if required</div>',
            unsafe_allow_html=True,
        )

    # ========================================================
    # LIVE MONITORING FOOTER
    # ========================================================

    st.markdown(
        '<div class="cm-footer">'
        '<div style="font-size:15px;font-weight:800;color:#f5e8eb;">'
        '<span class="cm-live-dot">📡 Live Monitoring Active</span>'
        '</div>'
        '<div class="cm-description">'
        'CareMatrix is continuously receiving patient sensor data from Wokwi.'
        '</div>'
        '<div style="display:flex;gap:30px;margin-top:14px;'
        'color:#aa8e95;font-size:11px;flex-wrap:wrap;">'
        f'<div><b>Stored readings:</b> {len(history)}</div>'
        f'<div><b>Mode:</b> {latest["mode"]}</div>'
        f'<div><b>Status:</b> {latest["status"]}</div>'
        '</div></div>',
        unsafe_allow_html=True,
    )


render_dashboard()
