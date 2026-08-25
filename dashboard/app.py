import streamlit as st
import requests
import time
import html

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CareMatrix",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CONFIG
# ============================================================

BACKEND_URL = "https://smart-patient-monitoring.onrender.com"

LATEST_URL = f"{BACKEND_URL}/latest"
HISTORY_URL = f"{BACKEND_URL}/history"

# ============================================================
# SESSION STATE
# ============================================================

if "sound_enabled" not in st.session_state:
    st.session_state.sound_enabled = False

if "intro_done" not in st.session_state:
    st.session_state.intro_done = False

if "last_mode" not in st.session_state:
    st.session_state.last_mode = None

if "last_alert" not in st.session_state:
    st.session_state.last_alert = False


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(20, 130, 255, 0.12),
            transparent 28%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(0, 210, 190, 0.08),
            transparent 25%
        ),
        #07111f;
    color: #f5f9ff;
}

/* Remove default Streamlit top spacing */
.block-container {
    max-width: 1450px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

/* Hide menu/footer */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* =========================================================
   BRAND
   ========================================================= */

.brand {
    display: flex;
    align-items: center;
    gap: 13px;
}

.brand-heart {
    width: 48px;
    height: 48px;
    border-radius: 15px;

    display: flex;
    align-items: center;
    justify-content: center;

    background:
        linear-gradient(
            135deg,
            #0b8cff,
            #00d6c9
        );

    box-shadow:
        0 10px 30px rgba(0, 150, 255, 0.25);

    font-size: 27px;
}

.brand-name {
    font-size: 31px;
    font-weight: 800;
    letter-spacing: -1.3px;
}

.brand-name span {
    color: #28a9ff;
}

.brand-subtitle {
    color: #91a5bd;
    font-size: 12px;
    margin-top: -3px;
}

/* =========================================================
   LIVE PILL
   ========================================================= */

.live-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;

    padding: 8px 13px;

    border-radius: 30px;

    background: rgba(0, 220, 150, 0.09);

    border: 1px solid rgba(0, 220, 150, 0.28);

    color: #51e6ac;

    font-size: 12px;
    font-weight: 700;
}

.live-dot {
    width: 8px;
    height: 8px;

    background: #35e39d;

    border-radius: 50%;

    box-shadow:
        0 0 12px #35e39d;
}

/* =========================================================
   TOP BAR
   ========================================================= */

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;

    padding-bottom: 18px;

    border-bottom:
        1px solid rgba(255,255,255,0.08);

    margin-bottom: 22px;
}

/* =========================================================
   INTRO
   ========================================================= */

.intro {
    text-align: center;

    padding: 70px 20px;

    max-width: 800px;

    margin: 80px auto;
}

.intro-heart {
    font-size: 52px;
}

.intro h1 {
    font-size: 42px;
    margin: 12px 0 8px;
}

.intro h1 span {
    color: #20a9ff;
}

.intro p {
    color: #8fa4bd;
    font-size: 16px;
    line-height: 1.7;
}

.intro-small {
    color: #5f7892;
    font-size: 12px;
    margin-top: 25px;
}

/* =========================================================
   ALERT
   ========================================================= */

.alert-critical {
    border:
        1px solid rgba(255, 61, 83, 0.65);

    background:
        linear-gradient(
            135deg,
            rgba(120, 20, 35, 0.45),
            rgba(55, 10, 20, 0.75)
        );

    border-radius: 18px;

    padding: 18px 22px;

    margin-bottom: 22px;

    box-shadow:
        0 0 35px rgba(255, 30, 60, 0.12);
}

.alert-critical-title {
    color: #ff5268;
    font-size: 18px;
    font-weight: 800;
}

.alert-critical-text {
    color: #ffb0b9;
    font-size: 13px;
    margin-top: 4px;
}

/* =========================================================
   NORMAL STATUS
   ========================================================= */

.status-normal {
    border:
        1px solid rgba(40, 220, 155, 0.25);

    background:
        linear-gradient(
            135deg,
            rgba(20, 100, 75, 0.25),
            rgba(10, 50, 45, 0.35)
        );

    border-radius: 18px;

    padding: 18px 22px;

    margin-bottom: 22px;
}

.status-normal-title {
    color: #43dfa6;
    font-size: 18px;
    font-weight: 800;
}

.status-normal-text {
    color: #91cdb9;
    font-size: 13px;
}

/* =========================================================
   CARDS
   ========================================================= */

.metric-card {
    position: relative;

    min-height: 145px;

    padding: 20px;

    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            rgba(20, 35, 55, 0.95),
            rgba(10, 21, 36, 0.95)
        );

    border:
        1px solid rgba(120, 170, 220, 0.14);

    box-shadow:
        0 15px 40px rgba(0,0,0,0.16);
}

.metric-card.alert {
    border:
        1px solid rgba(255, 60, 80, 0.4);

    background:
        linear-gradient(
            145deg,
            rgba(65, 20, 30, 0.85),
            rgba(25, 12, 20, 0.95)
        );
}

.metric-icon {
    font-size: 25px;
}

.metric-name {
    color: #849bb4;
    font-size: 12px;
    margin-top: 8px;
}

.metric-value {
    color: #f4f8ff;

    font-size: 28px;
    font-weight: 800;

    margin-top: 5px;
}

.metric-card.alert .metric-value {
    color: #ff5268;
}

.metric-normal {
    display: inline-block;

    margin-top: 8px;

    padding: 4px 9px;

    border-radius: 20px;

    background: rgba(40,220,155,0.09);

    color: #43dfa6;

    font-size: 10px;
    font-weight: 700;
}

.metric-danger {
    display: inline-block;

    margin-top: 8px;

    padding: 4px 9px;

    border-radius: 20px;

    background: rgba(255,50,70,0.12);

    color: #ff6173;

    font-size: 10px;
    font-weight: 700;
}

/* =========================================================
   SECTION
   ========================================================= */

.section-title {
    color: #dce8f5;

    font-size: 15px;

    font-weight: 800;

    margin:
        24px 0 12px;
}

/* =========================================================
   SAFETY CARDS
   ========================================================= */

.safety-card {
    padding: 18px;

    border-radius: 17px;

    background:
        rgba(16, 29, 47, 0.88);

    border:
        1px solid rgba(120,170,220,0.12);
}

.safety-label {
    color: #758ca5;
    font-size: 11px;
}

.safety-value {
    margin-top: 6px;

    font-size: 20px;
    font-weight: 800;
}

.safe {
    color: #42dfa5;
}

.danger {
    color: #ff5268;
}

/* =========================================================
   INFO PANEL
   ========================================================= */

.info-panel {
    padding: 20px;

    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            rgba(18,34,54,0.95),
            rgba(8,20,34,0.95)
        );

    border:
        1px solid rgba(100,160,220,0.13);
}

.info-label {
    color: #7189a2;
    font-size: 11px;
}

.info-value {
    color: #e9f3ff;
    font-weight: 700;
    margin-top: 4px;
}

/* =========================================================
   FOOTER
   ========================================================= */

.footer {
    text-align: center;

    color: #506982;

    font-size: 11px;

    margin-top: 40px;

    padding-top: 20px;

    border-top:
        1px solid rgba(255,255,255,0.06);
}

/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 768px) {

    .block-container {
        padding-left: 13px;
        padding-right: 13px;
    }

    .brand-name {
        font-size: 24px;
    }

    .brand-heart {
        width: 42px;
        height: 42px;
    }

    .intro {
        padding: 45px 12px;
        margin: 30px auto;
    }

    .intro h1 {
        font-size: 31px;
    }

    .intro p {
        font-size: 14px;
    }

    .metric-card {
        min-height: 125px;
    }

    .metric-value {
        font-size: 24px;
    }
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# INTRO SCREEN — ABOUT THE PROJECT
# ============================================================

if not st.session_state.intro_done:

    st.markdown(
        """
        <div class="intro">

            <div class="intro-heart">❤️</div>

            <h1>
                Welcome to <span>CareMatrix</span>
            </h1>

            <p>
                Smart Patient Monitoring & Alert Network
            </p>

            <p>
                An IoT-based monitoring system that watches
                patient vital signs in real time and detects
                abnormal conditions and falls early.
            </p>

            <div class="intro-small">
                Starting patient monitoring...
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    time.sleep(5)

    st.session_state.intro_done = True
    st.rerun()


# ============================================================
# FETCH LATEST DATA
# ============================================================

def get_latest():

    try:

        response = requests.get(
            LATEST_URL,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if not isinstance(data, dict):
            return None

        return data

    except Exception:
        return None


def get_history():

    try:

        response = requests.get(
            HISTORY_URL,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if isinstance(data, list):
            return data

        return []

    except Exception:
        return []


# ============================================================
# DATA
# ============================================================

data = get_latest()

history = get_history()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="topbar">

        <div class="brand">

            <div class="brand-heart">
                ❤️
            </div>

            <div>

                <div class="brand-name">
                    Care<span>Matrix</span>
                </div>

                <div class="brand-subtitle">
                    Smart Patient Monitoring & Alert Network
                </div>

            </div>

        </div>

        <div class="live-pill">
            <span class="live-dot"></span>
            LIVE MONITORING
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# BACKEND ERROR
# ============================================================

if data is None:

    st.markdown(
        """
        <div class="alert-critical">

            <div class="alert-critical-title">
                ⚠ Backend connection unavailable
            </div>

            <div class="alert-critical-text">
                CareMatrix cannot currently retrieve patient
                data from the monitoring server.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# ============================================================
# READ DATA
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

mode = str(
    data.get("mode", "NORMAL")
).upper()


# ============================================================
# DETERMINE STATUS
# ============================================================

abnormal = (
    mode == "ABNORMAL"
    or temperature >= 38
    or heart_rate > 100
    or heart_rate < 60
    or spo2 < 94
    or fall
)


if abnormal:
    patient_status = "CRITICAL"
else:
    patient_status = "STABLE"


# ============================================================
# ALERT
# ============================================================

if abnormal:

    st.markdown(
        f"""
        <div class="alert-critical">

            <div class="alert-critical-title">
                🚨 CRITICAL ALERT
            </div>

            <div class="alert-critical-text">
                Abnormal patient condition detected.
                Immediate attention may be required.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        """
        <div class="status-normal">

            <div class="status-normal-title">
                ✓ PATIENT STABLE
            </div>

            <div class="status-normal-text">
                All monitored vital signs are currently
                within the expected range.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CURRENT READINGS
# ============================================================

st.markdown(
    '<div class="section-title">Current Patient Readings</div>',
    unsafe_allow_html=True
)


c1, c2, c3 = st.columns(3)


# ------------------------------------------------------------
# HEART RATE
# ------------------------------------------------------------

with c1:

    heart_alert = (
        heart_rate > 100 or
        heart_rate < 60
    )

    card_class = (
        "metric-card alert"
        if heart_alert
        else "metric-card"
    )

    badge_class = (
        "metric-danger"
        if heart_alert
        else "metric-normal"
    )

    badge_text = (
        "HIGH / LOW"
        if heart_alert
        else "NORMAL"
    )

    st.markdown(
        f"""
        <div class="{card_class}">

            <div class="metric-icon">
                ❤️
            </div>

            <div class="metric-name">
                HEART RATE
            </div>

            <div class="metric-value">
                {heart_rate} <span style="font-size:14px">BPM</span>
            </div>

            <span class="{badge_class}">
                {badge_text}
            </span>

        </div>
        """,
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# TEMPERATURE
# ------------------------------------------------------------

with c2:

    temp_alert = (
        temperature >= 38
    )

    card_class = (
        "metric-card alert"
        if temp_alert
        else "metric-card"
    )

    badge_class = (
        "metric-danger"
        if temp_alert
        else "metric-normal"
    )

    badge_text = (
        "HIGH"
        if temp_alert
        else "NORMAL"
    )

    st.markdown(
        f"""
        <div class="{card_class}">

            <div class="metric-icon">
                🌡️
            </div>

            <div class="metric-name">
                TEMPERATURE
            </div>

            <div class="metric-value">
                {temperature:.1f}
                <span style="font-size:14px">°C</span>
            </div>

            <span class="{badge_class}">
                {badge_text}
            </span>

        </div>
        """,
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# SPO2
# ------------------------------------------------------------

with c3:

    spo2_alert = (
        spo2 < 94
    )

    card_class = (
        "metric-card alert"
        if spo2_alert
        else "metric-card"
    )

    badge_class = (
        "metric-danger"
        if spo2_alert
        else "metric-normal"
    )

    badge_text = (
        "LOW"
        if spo2_alert
        else "NORMAL"
    )

    st.markdown(
        f"""
        <div class="{card_class}">

            <div class="metric-icon">
                🫁
            </div>

            <div class="metric-name">
                BLOOD OXYGEN
            </div>

            <div class="metric-value">
                {spo2}
                <span style="font-size:14px">%</span>
            </div>

            <span class="{badge_class}">
                {badge_text}
            </span>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SAFETY
# ============================================================

st.markdown(
    '<div class="section-title">Patient Safety</div>',
    unsafe_allow_html=True
)


s1, s2, s3 = st.columns(3)


with s1:

    fall_class = (
        "danger"
        if fall
        else "safe"
    )

    fall_text = (
        "🚨 FALL DETECTED"
        if fall
        else "✓ SAFE"
    )

    st.markdown(
        f"""
        <div class="safety-card">

            <div class="safety-label">
                FALL DETECTION
            </div>

            <div class="safety-value {fall_class}">
                {fall_text}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with s2:

    status_class = (
        "danger"
        if abnormal
        else "safe"
    )

    st.markdown(
        f"""
        <div class="safety-card">

            <div class="safety-label">
                PATIENT STATUS
            </div>

            <div class="safety-value {status_class}">
                {patient_status}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with s3:

    mode_class = (
        "danger"
        if mode == "ABNORMAL"
        else "safe"
    )

    st.markdown(
        f"""
        <div class="safety-card">

            <div class="safety-label">
                MONITORING MODE
            </div>

            <div class="safety-value {mode_class}">
                {mode}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# ALERT SOUND
# ============================================================

st.markdown(
    '<div class="section-title">Alert System</div>',
    unsafe_allow_html=True
)


if abnormal:

    if st.button(
        "🔊 Enable Alert Sound",
        use_container_width=False
    ):

        st.session_state.sound_enabled = True

    if st.session_state.sound_enabled:

        st.markdown(
            """
            <audio autoplay>
                <source
                    src="https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg"
                    type="audio/ogg"
                >
            </audio>
            """,
            unsafe_allow_html=True
        )

        st.success(
            "Alert sound enabled."
        )

    else:

        st.caption(
            "Click Enable Alert Sound to allow browser audio."
        )


# ============================================================
# HEALTH TRENDS
# ============================================================

st.markdown(
    '<div class="section-title">Health Trends</div>',
    unsafe_allow_html=True
)


if history:

    try:

        import pandas as pd

        df = pd.DataFrame(history)

        if not df.empty:

            # Make sure expected columns exist

            for column in [
                "heart_rate",
                "temperature",
                "spo2"
            ]:

                if column not in df.columns:
                    df[column] = 0

            chart_df = df[
                [
                    "heart_rate",
                    "temperature",
                    "spo2"
                ]
            ].copy()

            st.line_chart(
                chart_df,
                height=350
            )

    except Exception as e:

        st.info(
            "Health trend data is being prepared."
        )

else:

    st.info(
        "Waiting for more sensor readings..."
    )


# ============================================================
# CARETAKER / ALERT ACTIONS
# ============================================================

st.markdown(
    '<div class="section-title">Caregiver Actions</div>',
    unsafe_allow_html=True
)


a1, a2 = st.columns(2)


with a1:

    if abnormal:

        st.markdown(
            """
            <div class="alert-critical">

                <div class="alert-critical-title">
                    🔔 Caretaker Attention Required
                </div>

                <div class="alert-critical-text">
                    Abnormal patient readings have been
                    detected. Review the patient immediately.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="status-normal">

                <div class="status-normal-title">
                    ✓ No Immediate Action
                </div>

                <div class="status-normal-text">
                    Patient readings are currently stable.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


with a2:

    st.markdown(
        f"""
        <div class="info-panel">

            <div class="info-label">
                SYSTEM CONNECTION
            </div>

            <div class="info-value">
                🟢 ESP32 → Render → CareMatrix
            </div>

            <br>

            <div class="info-label">
                CURRENT MODE
            </div>

            <div class="info-value">
                {mode}
            </div>

            <br>

            <div class="info-label">
                LAST DATA
            </div>

            <div class="info-value">
                Live sensor reading
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        ❤️ CareMatrix —
        Smart Patient Monitoring & Alert Network

        <br><br>

        Real-time IoT monitoring • Early detection • Safer care

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# AUTO REFRESH
# ============================================================

time.sleep(5)

st.rerun()