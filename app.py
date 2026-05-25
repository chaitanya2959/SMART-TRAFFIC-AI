##############################################
import streamlit as st
import pandas as pd
import numpy as np
 


# ---------------- IMPORT PAGES ----------------

from pages.dashboard import show_dashboard
from pages.alerts import show_alerts
from pages.assistant import show_traffic_ai
from pages.prediction import show_prediction
from pages.settings import show_settings
from pages.reports import show_reports
from pages.live_traffic import show_live_traffic

from config import (
    init_settings,
    get_setting
)
# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="SMART TRAFFIC AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_settings()

# ---------------- CSS ----------------

with open("assets/style.css") as f:

    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )
# ---------------- HIDE DEFAULT STREAMLIT ----------------

st.markdown("""
<style>

[data-testid="stSidebarNav"] {
    display: none;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ---------------- 

if "page" not in st.session_state:
    st.session_state.page = "dashboard"

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("🚦 SMART TRAFFIC AI")

    st.markdown("---")

    if st.button("🏠 Dashboard", use_container_width=True):
        st.session_state.page = "dashboard"
    
    if st.button("📹 Live Traffic", use_container_width=True):
        st.session_state.page = "live_traffic"

    if st.button("📈 Prediction", use_container_width=True):
        st.session_state.page = "prediction"

    if st.button("🚨 Alerts", use_container_width=True):
        st.session_state.page = "alerts"

    if st.button("🤖 Assistant", use_container_width=True):
        st.session_state.page = "assistant"

    if st.button("📊 Reports", use_container_width=True):
        st.session_state.page = "reports"

    if st.button("⚙️ Settings", use_container_width=True):
        st.session_state.page = "settings"

# ---------------- PAGE ROUTING ----------------

if st.session_state.page == "dashboard":

    show_dashboard()

elif st.session_state.page == "live_traffic":

    show_live_traffic()

elif st.session_state.page == "prediction":

    show_prediction()

elif st.session_state.page == "alerts":

    show_alerts()

elif st.session_state.page == "assistant":

    show_traffic_ai()

elif st.session_state.page == "reports":

    show_reports()

elif st.session_state.page == "settings":

    show_settings()