import time
import requests
import streamlit as st

from components import (
    render_header,
    render_alert,
    render_metric,
    render_waiting_metric,
    render_safety,
    render_actions,
)

from charts import render_health_chart


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CareMatrix",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# BACKEND
# ============================================================

BACKEND_URL = "https://smart-patient-monitoring.onrender.com"

LATEST_URL = f"{BACKEND_URL}/latest"
HISTORY_URL = f"{BACKEND_URL}/history"


# ============================================================
# SESSION
# ============================================================

if "intro_done" not in st.session_state:
    st.session_state.intro_done = False


# ============================================================
# CSS
# ============================================================

st.markdown(
"""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);


* {
    box-sizing: border-box;
}


html,
body,
[class*="css"] {
    font-family: Inter, sans-serif;
}


.stApp {

    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(0,132,255,0.14),
            transparent 30%
        ),

        radial-gradient(
            circle at 90% 20%,
            rgba(0,210,190,0.08),
            transparent 30%
        ),

        #07111f;

    color: #f5f9ff;
}


.block-container {

    max-width: 1450px;

    padding-top: 25px;

    padding-bottom: 50px;
}


#MainMenu,
footer,
header {

    visibility: hidden;
}


/* ============================================================
HEADER
============================================================ */

.top-header {

    display: flex;

    align-items: center;

    justify-content: space-between;

    padding: 10px 0 22px;

    border-bottom:
        1px solid rgba(255,255,255,0.08);

    margin-bottom: 24px;
}


.brand-area {

    display: flex;

    align-items: center;

    gap: 14px;
}


.brand-logo {

    width: 52px;
    height: 52px;

    border-radius: 17px;

    display: flex;

    align-items: center;

    justify-content: center;

    background:
        linear-gradient(
            135deg,
            #0b8cff,
            #00d6c9
        );

    color: white;

    font-size: 28px;

    box-shadow:
        0 10px 30px
        rgba(0,150,255,0.25);
}


.brand-name {

    font-size: 31px;

    font-weight: 800;

    letter-spacing: -1px;
}


.brand-name span {

    color: #20a9ff;
}


.brand-subtitle {

    color: #8da2ba;

    font-size: 12px;

    margin-top: 2px;
}


.header-right {

    display: flex;

    align-items: center;

    gap: 12px;
}


.live-badge {

    padding: 9px 15px;

    border-radius: 30px;

    font-size: 11px;

    font-weight: 800;
}


.live-normal {

    color: #46dfa6;

    background:
        rgba(40,220,155,0.08);

    border:
        1px solid rgba(40,220,155,0.25);
}


.live-alert {

    color: #ff6678;

    background:
        rgba(255,50,70,0.10);

    border:
        1px solid rgba(255,50,70,0.35);
}


.live-waiting {

    color: #ffd166;

    background:
        rgba(255,209,102,0.08);

    border:
        1px solid rgba(255,209,102,0.25);
}


.live-dot {

    display: inline-block;

    width: 8px;
    height: 8px;

    margin-right: 6px;

    border-radius: 50%;

    background: currentColor;
}


.patient-badge {

    padding: 9px 14px;

    border-radius: 12px;

    background:
        rgba(255,255,255,0.04);

    border:
        1px solid rgba(255,255,255,0.08);

    color: #9bb0c8;

    font-size: 11px;
}


.patient-badge b {

    color: #e8f3ff;
}


.avatar {

    width: 39px;
    height: 39px;

    border-radius: 50%;

    background: #14304d;

    display: flex;

    align-items: center;

    justify-content: center;
}


/* ============================================================
ALERT
============================================================ */

.critical-alert {

    display: flex;

    align-items: center;

    gap: 18px;

    padding: 20px 24px;

    margin-bottom: 24px;

    border-radius: 18px;

    background:
        linear-gradient(
            135deg,
            rgba(115,20,38,0.55),
            rgba(40,10,20,0.85)
        );

    border:
        1px solid rgba(255,60,80,0.55);

    box-shadow:
        0 10px 40px
        rgba(255,30,60,0.10);
}


.alert-icon {

    width: 45px;
    height: 45px;

    border-radius: 13px;

    display: flex;

    align-items: center;

    justify-content: center;

    background:
        rgba(255,50,70,0.15);

    color: #ff596d;

    font-size: 24px;
}


.alert-content {

    flex: 1;
}


.alert-title {

    color: #ff5268;

    font-size: 18px;

    font-weight: 800;
}


.alert-message {

    color: #ffb5bd;

    font-size: 12px;

    margin-top: 4px;
}


.alert-symbol {

    font-size: 30px;
}


.stable-alert {

    display: flex;

    align-items: center;

    gap: 15px;

    padding: 19px 23px;

    margin-bottom: 24px;

    border-radius: 18px;

    background:
        linear-gradient(
            135deg,
            rgba(20,100,75,0.25),
            rgba(10,45,40,0.35)
        );

    border:
        1px solid rgba(40,220,155,0.25);
}


.stable-icon {

    width: 43px;
    height: 43px;

    border-radius: 50%;

    display: flex;

    align-items: center;

    justify-content: center;

    background:
        rgba(40,220,155,0.12);

    color: #42dfa5;

    font-size: 22px;

    font-weight: 800;
}


.stable-title {

    color: #43dfa6;

    font-size: 17px;

    font-weight: 800;
}


.stable-message {

    color: #91cdb9;

    font-size: 12px;

    margin-top: 3px;
}


.waiting-alert {

    display: flex;

    align-items: center;

    gap: 15px;

    padding: 20px;

    margin-bottom: 24px;

    border-radius: 18px;

    background:
        rgba(255,209,102,0.06);

    border:
        1px solid rgba(255,209,102,0.20);
}


.waiting-icon {

    font-size: 30px;

    color: #ffd166;
}


.waiting-title {

    color: #ffd166;

    font-size: 16px;

    font-weight: 800;
}


.waiting-message {

    color: #a8a8a8;

    font-size: 12px;

    margin-top: 3px;
}


/* ============================================================
SECTION
============================================================ */

.section-title {

    color: #dbe8f5;

    font-size: 14px;

    font-weight: 800;

    margin: 24px 0 12px;
}


/* ============================================================
METRICS
============================================================ */

.metric-card {

    min-height: 175px;

    padding: 21px;

    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            rgba(18,36,57,0.96),
            rgba(9,21,36,0.96)
        );

    border:
        1px solid rgba(120,170,220,0.13);

    box-shadow:
        0 15px 35px
        rgba(0,0,0,0.16);
}


.metric-card.abnormal {

    background:
        linear-gradient(
            145deg,
            rgba(70,20,32,0.90),
            rgba(25,10,18,0.96)
        );

    border:
        1px solid rgba(255,60,80,0.40);
}


.metric-top {

    display: flex;

    align-items: center;

    gap: 10px;
}


.metric-icon {

    font-size: 24px;
}


.metric-title {

    color: #8da4bd;

    font-size: 12px;

    font-weight: 600;
}


.metric-value {

    color: #f4f8ff;

    font-size: 31px;

    font-weight: 800;

    margin-top: 20px;
}


.metric-card.abnormal
.metric-value {

    color: #ff6173;
}


.metric-value span {

    color: #91a6bd;

    font-size: 13px;

    font-weight: 600;
}


.metric-status {

    display: inline-block;

    margin-top: 14px;

    padding: 5px 10px;

    border-radius: 20px;

    font-size: 10px;

    font-weight: 800;
}


.metric-status.normal {

    color: #43dfa6;

    background:
        rgba(40,220,155,0.09);
}


.metric-status.danger {

    color: #ff6173;

    background:
        rgba(255,50,70,0.12);
}


.metric-status.waiting {

    color: #ffd166;

    background:
        rgba(255,209,102,0.10);
}


.waiting-value {

    color: #71859b;

    font-size: 36px;
}


/* ============================================================
SAFETY
============================================================ */

.safety-grid {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 14px;
}


.safety-card {

    padding: 19px;

    border-radius: 17px;

    background:
        rgba(15,29,47,0.88);

    border:
        1px solid rgba(120,170,220,0.12);
}


.safety-label {

    color: #758da6;

    font-size: 10px;

    font-weight: 700;
}


.safety-value {

    margin-top: 8px;

    font-size: 18px;

    font-weight: 800;
}


.safe-text {

    color: #42dfa5;
}


.danger-text {

    color: #ff596d;
}


.waiting-text {

    color: #ffd166;
}


/* ============================================================
ACTION
============================================================ */

.action-panel {

    margin-top: 25px;

    padding: 21px;

    border-radius: 18px;
}


.normal-panel {

    background:
        rgba(15,65,55,0.25);

    border:
        1px solid rgba(40,220,155,0.22);
}


.abnormal-panel {

    background:
        rgba(70,15,28,0.30);

    border:
        1px solid rgba(255,60,80,0.35);
}


.waiting-panel {

    background:
        rgba(255,209,102,0.05);

    border:
        1px solid rgba(255,209,102,0.20);
}


.action-header {

    display: flex;

    align-items: center;

    gap: 14px;
}


.action-header > span {

    font-size: 26px;
}


.action-title {

    color: #eef7ff;

    font-size: 15px;

    font-weight: 800;
}


.action-subtitle {

    color: #8fa6be;

    font-size: 11px;

    margin-top: 3px;
}


.action-row {

    display: flex;

    gap: 10px;

    margin-top: 18px;
}


.action-item {

    flex: 1;

    padding: 11px;

    border-radius: 10px;

    background:
        rgba(255,255,255,0.035);

    color: #9db1c7;

    font-size: 11px;
}


/* ============================================================
FOOTER
============================================================ */

.footer {

    text-align: center;

    color: #526a83;

    font-size: 10px;

    margin-top: 45px;

    padding-top: 20px;

    border-top:
        1px solid rgba(255,255,255,0.06);
}


/* ============================================================
MOBILE
============================================================ */

@media (max-width: 900px) {

    .block-container {

        padding-left: 15px;

        padding-right: 15px;
    }


    .top-header {

        align-items: flex-start;
    }


    .header-right {

        flex-direction: column;

        align-items: flex-end;
    }


    .patient-badge,
    .avatar {

        display: none;
    }


    .brand-name {

        font-size: 25px;
    }


    .brand-subtitle {

        font-size: 10px;
    }


    .safety-grid {

        grid-template-columns: 1fr;
    }


    .action-row {

        flex-direction: column;
    }


    .metric-card {

        min-height: 150px;
    }
}

</style>
""",
unsafe_allow_html=True
)


# ============================================================
# INTRO
# ============================================================

if not st.session_state.intro_done:

    st.markdown(
    """
    <div style="
        min-height:75vh;
        display:flex;
        align-items:center;
        justify-content:center;
        text-align:center;
    ">

        <div style="
            max-width:700px;
            padding:60px 35px;
        ">

            <div style="
                font-size:60px;
                margin-bottom:15px;
            ">
                ❤️
            </div>

            <div style="
                color:#20a9ff;
                font-size:14px;
                font-weight:700;
                letter-spacing:2px;
            ">
                SMART PATIENT MONITORING
            </div>

            <h1 style="
                font-size:46px;
                margin:10px 0;
                color:#f4f8ff;
            ">
                CareMatrix
            </h1>

            <p style="
                color:#9eb2c8;
                font-size:17px;
                line-height:1.7;
            ">
                An IoT-based system that monitors patient vital signs
                in real time and detects abnormal conditions and falls early.
            </p>

            <div style="
                margin-top:35px;
                color:#42dfa5;
                font-size:13px;
            ">
                ● Starting patient monitoring...
            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True
    )

    time.sleep(5)

    st.session_state.intro_done = True

    st.rerun()


# ============================================================
# GET LATEST DATA
# ============================================================

def get_latest():

    try:

        response = requests.get(
            LATEST_URL,
            timeout=15
        )

        response.raise_for_status()

        result = response.json()

        if isinstance(result, dict):

            return result

    except Exception as error:

        return None

    return None


# ============================================================
# GET HISTORY
# ============================================================

def get_history():

    try:

        response = requests.get(
            HISTORY_URL,
            timeout=15
        )

        response.raise_for_status()

        result = response.json()

        if isinstance(result, list):

            return result

    except Exception:

        return []

    return []


# ============================================================
# DATA
# ============================================================

data = get_latest()

history = get_history()


# ============================================================
# NO DATA
# ============================================================

if data is None:

    render_header("WAITING")

    render_alert(
        abnormal=False,
        fall=False,
        waiting=True
    )

    st.markdown(
    """
    <div class="section-title">
        Current Patient Readings
    </div>
    """,
    unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        render_waiting_metric(
            "❤️",
            "Heart Rate"
        )

    with c2:
        render_waiting_metric(
            "🌡️",
            "Temperature"
        )

    with c3:
        render_waiting_metric(
            "🫁",
            "SpO₂"
        )

    render_safety(
        fall=False,
        patient_status="WAITING",
        mode="WAITING"
    )

    render_actions(
        abnormal=False,
        waiting=True
    )

    st.stop()


# ============================================================
# READ SENSOR DATA
# ============================================================

temperature = float(
    data.get("temperature", 0)
)

heart_rate = int(
    data.get("heart_rate", 0)
)

spo2 = int(
    data.get("spo2", 0)
)

fall = bool(
    data.get("fall", False)
)


# ============================================================
# DETECT EMPTY INITIAL DATA
# ============================================================

empty_data = (
    temperature == 0
    and heart_rate == 0
    and spo2 == 0
    and fall is False
)


# ============================================================
# EMPTY DATA SCREEN
# ============================================================

if empty_data:

    render_header("WAITING")

    render_alert(
        abnormal=False,
        fall=False,
        waiting=True
    )

    st.markdown(
    """
    <div class="section-title">
        Current Patient Readings
    </div>
    """,
    unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        render_waiting_metric(
            "❤️",
            "Heart Rate"
        )

    with c2:
        render_waiting_metric(
            "🌡️",
            "Temperature"
        )

    with c3:
        render_waiting_metric(
            "🫁",
            "SpO₂"
        )

    render_safety(
        False,
        "WAITING",
        "WAITING"
    )

    render_actions(
        False,
        waiting=True
    )

    st.stop()


# ============================================================
# NORMAL / ABNORMAL
# ============================================================

heart_abnormal = (
    heart_rate > 100
    or heart_rate < 60
)

temperature_abnormal = (
    temperature >= 38
)

spo2_abnormal = (
    spo2 < 94
)

abnormal = (
    heart_abnormal
    or temperature_abnormal
    or spo2_abnormal
    or fall
)


mode = (
    "ABNORMAL"
    if abnormal
    else "NORMAL"
)


patient_status = (
    "CRITICAL"
    if abnormal
    else "STABLE"
)


# ============================================================
# HEADER
# ============================================================

render_header(mode)


# ============================================================
# ALERT
# ============================================================

render_alert(
    abnormal,
    fall
)


# ============================================================
# CURRENT READINGS
# ============================================================

st.markdown(
"""
<div class="section-title">
    Current Patient Readings
</div>
""",
unsafe_allow_html=True
)


# ============================================================
# METRICS
# ============================================================

c1, c2, c3 = st.columns(3)


with c1:

    render_metric(
        "❤️",
        "Heart Rate",
        heart_rate,
        "BPM",
        "HIGH / LOW"
        if heart_abnormal
        else "NORMAL",
        heart_abnormal
    )


with c2:

    render_metric(
        "🌡️",
        "Temperature",
        f"{temperature:.1f}",
        "°C",
        "HIGH"
        if temperature_abnormal
        else "NORMAL",
        temperature_abnormal
    )


with c3:

    render_metric(
        "🫁",
        "SpO₂",
        spo2,
        "%",
        "LOW"
        if spo2_abnormal
        else "NORMAL",
        spo2_abnormal
    )


# ============================================================
# PATIENT SAFETY
# ============================================================

st.markdown(
"""
<div class="section-title">
    Patient Safety
</div>
""",
unsafe_allow_html=True
)


render_safety(
    fall,
    patient_status,
    mode
)


# ============================================================
# HEALTH TRENDS
# ============================================================

st.markdown(
"""
<div class="section-title">
    Health Trends
</div>
""",
unsafe_allow_html=True
)


render_health_chart(history)


# ============================================================
# CARETAKER ACTION
# ============================================================

render_actions(
    abnormal
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
"""
<div class="footer">

    ❤️ CareMatrix

    <br>

    Smart Patient Monitoring & Alert Network

    <br><br>

    ESP32 → Render Backend → CareMatrix

</div>
""",
unsafe_allow_html=True
)


# ============================================================
# REFRESH
# ============================================================

time.sleep(5)

st.rerun()