import streamlit as st

# =====================================
# SIDEBAR
# =====================================

def show_sidebar():

    # SESSION

    if "sidebar_open" not in st.session_state:

        st.session_state.sidebar_open = True

    # TOGGLE

    if st.button(
        "☰",
        key="menu_toggle"
    ):

        st.session_state.sidebar_open = (
            not st.session_state.sidebar_open
        )

    # WIDTH

    if st.session_state.sidebar_open:

        sidebar_width = "280px"
        main_margin = "300px"

    else:

        sidebar_width = "0px"
        main_margin = "20px"

    # CSS

    st.markdown(f"""
    <style>

    /* =====================================
       REMOVE DEFAULT STREAMLIT
    ===================================== */

    section[data-testid="stSidebar"] {{
        display:none;
    }}

    header {{
        visibility:hidden;
    }}

    footer {{
        visibility:hidden;
    }}

    #MainMenu {{
        visibility:hidden;
    }}

    /* =====================================
       PAGE
    ===================================== */

    html, body, .stApp {{

        background:#020617;

        overflow:hidden;

        height:100vh;
    }}

    /* =====================================
       MAIN CONTENT
    ===================================== */

    .main .block-container {{

        margin-left:{main_margin};

        transition:0.3s;

        padding-top:20px;

        padding-right:20px;

        padding-left:20px;

        max-width:100%;

        width:100%;

        overflow:hidden;
    }}

    /* =====================================
       SIDEBAR
    ===================================== */

    .custom-sidebar {{

        position:fixed;

        top:0;

        left:0;

        width:{sidebar_width};

        height:100vh;

        background:#081120;

        transition:0.3s;

        overflow:hidden;

        z-index:9999;

        border-right:1px solid rgba(255,255,255,0.06);

        padding-top:100px;
    }}

    /* =====================================
       SIDEBAR BUTTON
    ===================================== */

    .stButton > button {{

        width:100%;

        background:#111827;

        color:white;

        border:none;

        border-radius:14px;

        padding:14px;

        font-size:16px;

        font-weight:600;

        margin-bottom:12px;
    }}

    .stButton > button:hover {{

        background:#4f46e5;
        color:white;
    }}

    </style>
    """, unsafe_allow_html=True)

    # SIDEBAR HTML

    st.markdown(f"""
    <div class="custom-sidebar">
    </div>
    """, unsafe_allow_html=True)

    # SIDEBAR CONTENT

    if st.session_state.sidebar_open:

        st.markdown("## Navigation")

        if st.button("🏠 Dashboard"):
            st.session_state.page = "dashboard"

        if st.button("📹 Live Traffic"):
            st.session_state.page = "live_traffic"

        if st.button("📈 Prediction"):
            st.session_state.page = "prediction"

        if st.button("🚨 Alerts"):
            st.session_state.page = "alerts"

        if st.button("🤖 AI Assistant"):
            st.session_state.page = "assistant"

        if st.button("📊 Reports"):
            st.session_state.page = "reports"

        if st.button("⚙️ Settings"):
            st.session_state.page = "settings"