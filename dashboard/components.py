import textwrap
import streamlit as st


# ============================================================
# HTML HELPER
# ============================================================

def html(content):
    st.markdown(
        textwrap.dedent(content),
        unsafe_allow_html=True
    )


# ============================================================
# HEADER
# ============================================================

def render_header(mode):

    if mode == "ABNORMAL":
        live_class = "live-alert"
        live_text = "LIVE MONITORING — ALERT"

    elif mode == "WAITING":
        live_class = "live-waiting"
        live_text = "WAITING FOR DATA"

    else:
        live_class = "live-normal"
        live_text = "LIVE MONITORING"

    html(f"""
    <div class="top-header">

        <div class="brand-area">

            <div class="brand-logo">
                ❤
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


        <div class="header-right">

            <div class="live-badge {live_class}">
                <span class="live-dot"></span>
                {live_text}
            </div>


            <div class="patient-badge">
                Patient ID: <b>CM-1024</b>
            </div>


            <div class="avatar">
                👤
            </div>

        </div>

    </div>
    """)


# ============================================================
# ALERT
# ============================================================

def render_alert(abnormal=False, fall=False, waiting=False):

    # --------------------------------------------------------
    # WAITING
    # --------------------------------------------------------

    if waiting:

        html("""
        <div class="waiting-alert">

            <div class="waiting-icon">
                ⟳
            </div>

            <div>

                <div class="waiting-title">
                    CONNECTING TO PATIENT MONITOR
                </div>

                <div class="waiting-message">
                    Waiting for the first sensor reading...
                </div>

            </div>

        </div>
        """)

        return


    # --------------------------------------------------------
    # ABNORMAL
    # --------------------------------------------------------

    if abnormal:

        if fall:
            message = (
                "Fall detected. Immediate patient attention required."
            )
        else:
            message = (
                "Abnormal vital signs detected. "
                "Immediate attention required."
            )

        html(f"""
        <div class="critical-alert">

            <div class="alert-icon">
                ⚠
            </div>


            <div class="alert-content">

                <div class="alert-title">
                    🚨 CRITICAL ALERT
                </div>

                <div class="alert-message">
                    {message}
                </div>

            </div>


            <div class="alert-symbol">
                🚨
            </div>

        </div>
        """)

        return


    # --------------------------------------------------------
    # NORMAL
    # --------------------------------------------------------

    html("""
    <div class="stable-alert">

        <div class="stable-icon">
            ✓
        </div>

        <div>

            <div class="stable-title">
                PATIENT STABLE
            </div>

            <div class="stable-message">
                All monitored vital signs are within the expected range.
            </div>

        </div>

    </div>
    """)


# ============================================================
# NORMAL / ABNORMAL METRIC
# ============================================================

def render_metric(
    icon,
    title,
    value,
    unit,
    status,
    abnormal=False
):

    if abnormal:
        card_class = "metric-card abnormal"
        status_class = "metric-status danger"
    else:
        card_class = "metric-card"
        status_class = "metric-status normal"

    html(f"""
    <div class="{card_class}">

        <div class="metric-top">

            <div class="metric-icon">
                {icon}
            </div>

            <div class="metric-title">
                {title}
            </div>

        </div>


        <div class="metric-value">

            {value}

            <span>
                {unit}
            </span>

        </div>


        <div class="{status_class}">
            {status}
        </div>

    </div>
    """)


# ============================================================
# WAITING METRIC
# ============================================================

def render_waiting_metric(icon, title):

    html(f"""
    <div class="metric-card">

        <div class="metric-top">

            <div class="metric-icon">
                {icon}
            </div>

            <div class="metric-title">
                {title}
            </div>

        </div>


        <div class="metric-value waiting-value">
            --
        </div>


        <div class="metric-status waiting">
            WAITING
        </div>

    </div>
    """)


# ============================================================
# SAFETY
# ============================================================

def render_safety(
    fall,
    patient_status,
    mode
):

    # --------------------------------------------------------
    # WAITING
    # --------------------------------------------------------

    if mode == "WAITING":

        fall_text = "WAITING"
        fall_class = "waiting-text"

        status_text = "WAITING"
        status_class = "waiting-text"

        mode_text = "WAITING"
        mode_class = "waiting-text"

    else:

        # Fall
        if fall:

            fall_text = "🚨 FALL DETECTED"
            fall_class = "danger-text"

        else:

            fall_text = "✓ SAFE"
            fall_class = "safe-text"


        # Patient status
        status_text = patient_status

        if patient_status == "CRITICAL":
            status_class = "danger-text"
        else:
            status_class = "safe-text"


        # Mode
        mode_text = mode

        if mode == "ABNORMAL":
            mode_class = "danger-text"
        else:
            mode_class = "safe-text"


    html(f"""
    <div class="safety-grid">


        <div class="safety-card">

            <div class="safety-label">
                FALL STATUS
            </div>

            <div class="safety-value {fall_class}">
                {fall_text}
            </div>

        </div>


        <div class="safety-card">

            <div class="safety-label">
                PATIENT STATUS
            </div>

            <div class="safety-value {status_class}">
                {status_text}
            </div>

        </div>


        <div class="safety-card">

            <div class="safety-label">
                MONITORING MODE
            </div>

            <div class="safety-value {mode_class}">
                {mode_text}
            </div>

        </div>


    </div>
    """)


# ============================================================
# CARETAKER ACTIONS
# ============================================================

def render_actions(
    abnormal=False,
    waiting=False
):

    # --------------------------------------------------------
    # WAITING
    # --------------------------------------------------------

    if waiting:

        html("""
        <div class="action-panel waiting-panel">

            <div class="action-header">

                <span>
                    📡
                </span>

                <div>

                    <div class="action-title">
                        Waiting for sensor data
                    </div>

                    <div class="action-subtitle">
                        CareMatrix will begin monitoring automatically.
                    </div>

                </div>

            </div>

        </div>
        """)

        return


    # --------------------------------------------------------
    # ABNORMAL
    # --------------------------------------------------------

    if abnormal:

        html("""
        <div class="action-panel abnormal-panel">

            <div class="action-header">

                <span>
                    🚨
                </span>

                <div>

                    <div class="action-title">
                        Caretaker Attention Required
                    </div>

                    <div class="action-subtitle">
                        Abnormal patient condition detected.
                    </div>

                </div>

            </div>


            <div class="action-row">

                <div class="action-item">
                    ✓ Caretaker notification
                </div>

                <div class="action-item">
                    ! Immediate review required
                </div>

                <div class="action-item">
                    ☎ Emergency contact
                </div>

            </div>

        </div>
        """)

        return


    # --------------------------------------------------------
    # NORMAL
    # --------------------------------------------------------

    html("""
    <div class="action-panel normal-panel">

        <div class="action-header">

            <span>
                ✓
            </span>

            <div>

                <div class="action-title">
                    Patient Monitoring Active
                </div>

                <div class="action-subtitle">
                    No immediate action is required.
                </div>

            </div>

        </div>


        <div class="action-row">

            <div class="action-item">
                ✓ Patient stable
            </div>

            <div class="action-item">
                ● Live monitoring
            </div>

            <div class="action-item">
                ↗ Data connected
            </div>

        </div>

    </div>
    """)