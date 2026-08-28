import streamlit as st


def inject_css(theme="light", abnormal=False):
    """
    CareMatrix visual system.

    Normal:
      soft white / blue dashboard.

    Abnormal:
      dark red emergency dashboard.

    The abnormal state intentionally overrides the selected theme
    so an emergency cannot visually look like the normal state.
    """

    if abnormal:
        background = "#100509"
        card = "#1d0b10"
        text = "#ffffff"
        muted = "#d0aeb6"
        border = "#6d2530"
        accent = "#ff3e50"
        sidebar = "#13070b"
    elif theme == "dark":
        background = "#071321"
        card = "#101d2c"
        text = "#f5f9ff"
        muted = "#9cafc1"
        border = "#2a4058"
        accent = "#42b8ff"
        sidebar = "#06111f"
    else:
        background = "#eef5fb"
        card = "#ffffff"
        text = "#12344d"
        muted = "#71869a"
        border = "#d7e4ee"
        accent = "#168be8"
        sidebar = "#081a30"

    st.markdown(
        f"""
        <style>
        /* ---------- APP ---------- */
        .stApp {{
            background:{background};
            color:{text};
        }}

        .block-container {{
            max-width:1280px;
            padding-top:1.15rem;
            padding-bottom:2.5rem;
        }}

        [data-testid="stHeader"] {{
            background:transparent;
        }}

        /* Prevent Streamlit status/tool elements from changing layout. */
        [data-testid="stToolbar"] {{
            visibility:hidden;
        }}

        /* ---------- SIDEBAR ---------- */
        section[data-testid="stSidebar"] {{
            background:{sidebar};
            min-width:245px;
            max-width:245px;
        }}

        section[data-testid="stSidebar"] * {{
            color:#ffffff !important;
        }}

        .cm-sidebar-brand {{
            text-align:center;
            padding:18px 5px 25px;
        }}

        .cm-sidebar-heart {{
            font-size:48px;
            line-height:1;
            color:{accent};
        }}

        .cm-sidebar-title {{
            font-size:26px;
            font-weight:900;
            margin-top:7px;
        }}

        .cm-sidebar-title span {{
            color:{accent};
        }}

        .cm-sidebar-subtitle {{
            font-size:10px;
            opacity:.72;
            margin-top:3px;
        }}

        .cm-sidebar-item {{
            padding:12px 14px;
            margin:4px 0;
            border-radius:9px;
            font-size:13px;
            font-weight:750;
        }}

        .cm-sidebar-active {{
            background:linear-gradient(90deg,#238be8,#6957d8);
        }}

        .cm-sidebar-system {{
            margin-top:30px;
            padding:16px;
            border-radius:13px;
            border:1px solid #365371;
            background:rgba(255,255,255,.04);
        }}

        .cm-sidebar-system-title {{
            font-size:13px;
            font-weight:900;
            margin-bottom:10px;
        }}

        .cm-sidebar-system-line {{
            font-size:10px;
            margin-top:8px;
            opacity:.86;
        }}

        /* ---------- HEADER ---------- */
        .cm-header {{
            display:flex;
            justify-content:space-between;
            align-items:center;
            gap:20px;
            margin-bottom:18px;
        }}

        .cm-brand {{
            display:flex;
            align-items:center;
            gap:12px;
        }}

        .cm-logo {{
            width:52px;
            height:52px;
            border-radius:14px;
            border:2px solid {accent};
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:29px;
            color:{accent};
            background:{card};
        }}

        .cm-title {{
            font-size:29px;
            line-height:1;
            font-weight:900;
            color:{text};
        }}

        .cm-title span {{
            color:{accent};
        }}

        .cm-subtitle {{
            color:{muted};
            font-size:10px;
            margin-top:4px;
        }}

        .cm-header-right {{
            display:flex;
            align-items:center;
            gap:10px;
        }}

        .cm-live-pill {{
            padding:9px 15px;
            border-radius:25px;
            background:{"#50131c" if abnormal else "#e6f8ee"};
            color:{"#ff6874" if abnormal else "#13864f"};
            font-size:11px;
            font-weight:900;
        }}

        .cm-patient-id {{
            padding:9px 13px;
            border-radius:22px;
            background:{card};
            border:1px solid {border};
            color:{muted};
            font-size:10px;
        }}

        .cm-avatar {{
            width:35px;
            height:35px;
            border-radius:50%;
            background:{"#59121c" if abnormal else "#dceaf5"};
            display:flex;
            align-items:center;
            justify-content:center;
            color:{accent};
            font-size:11px;
            font-weight:900;
        }}

        /* ---------- GREETING ---------- */
        .cm-greeting {{
            font-size:25px;
            font-weight:900;
            color:{text};
            margin-top:8px;
        }}

        .cm-greeting-sub {{
            font-size:12px;
            color:{muted};
            margin-top:4px;
            margin-bottom:18px;
        }}

        /* ---------- STATUS ---------- */
        .cm-status-banner {{
            position:relative;
            padding:18px 22px;
            border-radius:14px;
            border:1px solid {"#8d2935" if abnormal else "#a7e4c2"};
            background:{"#351016" if abnormal else "#effbf5"};
            margin-bottom:20px;
        }}

        .cm-status-label {{
            font-size:9px;
            font-weight:900;
            color:{muted};
            letter-spacing:.6px;
        }}

        .cm-status-main {{
            font-size:24px;
            font-weight:900;
            margin-top:5px;
            color:{"#ff4354" if abnormal else "#11784b"};
        }}

        .cm-status-detail {{
            color:{muted};
            font-size:11px;
            margin-top:4px;
        }}

        .cm-status-mode {{
            position:absolute;
            right:18px;
            top:20px;
            padding:7px 14px;
            border-radius:15px;
            background:{"#66151f" if abnormal else "#dff6e9"};
            color:{"#ff6370" if abnormal else "#13834e"};
            font-size:9px;
            font-weight:900;
        }}

        /* ---------- ALERT BANNER ---------- */
        .cm-critical-banner {{
            display:flex;
            align-items:center;
            gap:15px;
            padding:17px 20px;
            border-radius:14px;
            margin-bottom:18px;
            background:linear-gradient(90deg,#451018,#250a0e);
            border:1px solid #a52d3a;
        }}

        .cm-critical-icon {{
            width:45px;
            height:45px;
            border-radius:50%;
            display:flex;
            align-items:center;
            justify-content:center;
            background:#7c1724;
            color:#fff;
            font-size:24px;
        }}

        .cm-critical-title {{
            color:#ff4354;
            font-size:21px;
            font-weight:900;
        }}

        .cm-critical-text {{
            color:#e4bcc2;
            font-size:11px;
            margin-top:3px;
        }}

        /* ---------- READINGS ---------- */
        .cm-section-title {{
            font-size:15px;
            font-weight:900;
            color:{text};
            margin:7px 0 10px;
        }}

        .metric-card {{
            min-height:150px;
            background:{card};
            border:1px solid {border};
            border-radius:14px;
            padding:18px;
            box-shadow:0 5px 18px rgba(20,50,80,.07);
        }}

        .metric-card-bad {{
            background:{"#240c11" if abnormal else "#fff4f5"};
            border-color:{"#a62c38" if abnormal else "#f1a9b1"};
        }}

        .metric-icon {{
            font-size:27px;
            line-height:1;
        }}

        .metric-name {{
            font-size:9px;
            font-weight:900;
            color:{muted};
            margin-top:10px;
            letter-spacing:.3px;
        }}

        .metric-value {{
            font-size:27px;
            font-weight:900;
            color:{text};
            margin-top:8px;
            line-height:1.15;
        }}

        .metric-unit {{
            font-size:10px;
            font-weight:700;
        }}

        .metric-good {{
            color:#159766;
            font-size:9px;
            font-weight:900;
            margin-top:9px;
        }}

        .metric-bad {{
            color:#ff4050;
            font-size:9px;
            font-weight:900;
            margin-top:9px;
        }}

        /* ---------- PANELS ---------- */
        .cm-panel-heading,
        .cm-side-panel,
        .cm-safe-panel,
        .cm-alert-actions,
        .cm-live-footer-panel {{
            background:{card};
            border:1px solid {border};
            border-radius:14px;
            box-shadow:0 5px 18px rgba(20,50,80,.06);
        }}

        .cm-panel-heading {{
            padding:16px 19px 9px;
            border-bottom-left-radius:0;
            border-bottom-right-radius:0;
        }}

        .cm-panel-title {{
            font-size:16px;
            font-weight:900;
            color:{text};
        }}

        .cm-panel-subtitle {{
            font-size:10px;
            color:{muted};
            margin-top:3px;
        }}

        /* The chart sits directly below its heading. */
        .cm-chart-empty {{
            height:405px;
            display:flex;
            align-items:center;
            justify-content:center;
            text-align:center;
            background:{card};
            border:1px solid {border};
            border-top:0;
            color:{muted};
            font-size:13px;
        }}

        /* ---------- QUICK OVERVIEW ---------- */
        .cm-side-panel {{
            padding:18px;
            margin-bottom:14px;
        }}

        .cm-overview-row {{
            display:flex;
            justify-content:space-between;
            align-items:center;
            padding:13px 0;
            border-bottom:1px solid {border};
            color:{muted};
            font-size:10px;
        }}

        .cm-overview-row:last-child {{
            border-bottom:0;
        }}

        .cm-overview-row b {{
            color:{text};
        }}

        .good-text {{
            color:#159766 !important;
        }}

        .cm-safe-panel {{
            text-align:center;
            padding:22px;
        }}

        .cm-safe-icon {{
            font-size:58px;
        }}

        .cm-safe-title {{
            font-size:17px;
            font-weight:900;
            color:#159766;
            margin-top:5px;
        }}

        .cm-safe-text {{
            color:{muted};
            font-size:10px;
            margin-top:4px;
        }}

        /* ---------- ALERT ACTIONS ---------- */
        .cm-alert-actions {{
            padding:20px;
            background:#2a0b10;
            border-color:#9c2936;
        }}

        .cm-alert-title {{
            font-size:20px;
            font-weight:900;
            color:#ff4354;
        }}

        .cm-alert-subtitle {{
            font-size:10px;
            color:#ddb7bd;
            margin-top:4px;
            margin-bottom:15px;
        }}

        .cm-action-row {{
            padding:13px 0;
            color:#d8f5df;
            border-bottom:1px solid #542027;
            font-size:11px;
        }}

        .cm-action-row:last-child {{
            border-bottom:0;
        }}

        .cm-action-row.danger {{
            color:#ff9aa3;
        }}

        .cm-active-title {{
            font-size:16px;
            font-weight:900;
            color:{text};
            margin-top:20px;
            margin-bottom:8px;
        }}

        .cm-active-alert {{
            padding:13px 15px;
            border-radius:10px;
            background:#380b11;
            border:1px solid #741e29;
            color:#ff6570;
            font-size:11px;
            margin-bottom:7px;
        }}

        /* ---------- LIVE INFO ---------- */
        .cm-live-footer-panel {{
            padding:18px 20px;
            margin-top:18px;
        }}

        .cm-live-stats {{
            display:flex;
            gap:30px;
            margin-top:14px;
            color:{muted};
            font-size:10px;
            flex-wrap:wrap;
        }}

        .cm-live-stats b {{
            color:{text};
        }}

        .cm-footer {{
            text-align:center;
            color:{muted};
            font-size:9px;
            margin-top:25px;
        }}

        /* ---------- STREAMLIT LAYOUT ---------- */
        div[data-testid="stHorizontalBlock"] {{
            align-items:stretch;
        }}

        @media (max-width:900px) {{
            .cm-header {{
                flex-direction:column;
                align-items:flex-start;
            }}
            .cm-header-right {{
                flex-wrap:wrap;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def metric_card(icon, name, value, unit, normal=True, normal_text="NORMAL"):
    card_class = "metric-card" if normal else "metric-card metric-card-bad"
    status_class = "metric-good" if normal else "metric-bad"
    symbol = "✓" if normal else "⚠"

    st.markdown(
        f"""
        <div class="{card_class}">
            <div class="metric-icon">{icon}</div>
            <div class="metric-name">{name}</div>
            <div class="metric-value">
                {value}
                <span class="metric-unit">{unit}</span>
            </div>
            <div class="{status_class}">{symbol} {normal_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
