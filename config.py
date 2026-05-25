import streamlit as st

# =====================================
# DEFAULT SETTINGS
# =====================================

DEFAULT_SETTINGS = {

    "theme": "Dark",

    "notifications": True,

    "ai_voice": False,

    "animations": True,

    "ai_model": "llama-3.3-70b-versatile"
}

# =====================================
# INIT SETTINGS
# =====================================

def init_settings():

    if "settings" not in st.session_state:

        st.session_state.settings = \
        DEFAULT_SETTINGS.copy()

# =====================================
# GET SETTING
# =====================================

def get_setting(key):

    return st.session_state.settings.get(key)

# =====================================
# UPDATE SETTING
# =====================================

def update_setting(key, value):

    st.session_state.settings[key] = value