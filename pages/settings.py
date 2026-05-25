import streamlit as st

from config import (
    init_settings,
    get_setting,
    update_setting
)

# =====================================
# SETTINGS PAGE
# =====================================

def show_settings():

    init_settings()

    st.title("⚙ Settings")

    st.write("Manage Smart Traffic AI settings.")

    st.divider()

    # =================================
    # THEME
    # =================================

    st.subheader("🎨 Theme")

    theme = st.selectbox(

        "Select Theme",

        [
            "Dark",
            "Light",
            "Blue"
        ],

        index=[
            "Dark",
            "Light",
            "Blue"
        ].index(
            get_setting("theme")
        )
    )

    update_setting(
        "theme",
        theme
    )

    st.divider()

    # =================================
    # NOTIFICATIONS
    # =================================

    st.subheader("🔔 Notifications")

    notifications = st.toggle(

        "Enable Notifications",

        value=get_setting(
            "notifications"
        )
    )

    update_setting(
        "notifications",
        notifications
    )

    st.divider()

    # =================================
    # AI VOICE
    # =================================

    st.subheader("🎤 AI Voice")

    ai_voice = st.toggle(

        "Enable AI Voice",

        value=get_setting(
            "ai_voice"
        )
    )

    update_setting(
        "ai_voice",
        ai_voice
    )

    st.divider()

    # =================================
    # ANIMATIONS
    # =================================

    st.subheader("✨ Animations")

    animations = st.toggle(

        "Enable Animations",

        value=get_setting(
            "animations"
        )
    )

    update_setting(
        "animations",
        animations
    )

    st.divider()

    # =================================
    # AI MODEL
    # =================================

    st.subheader("🤖 AI Model")

    ai_model = st.selectbox(

        "Select AI Model",

        [
            "llama-3.3-70b-versatile",
            "llama3-8b-8192"
        ],

        index=[
            "llama-3.3-70b-versatile",
            "llama3-8b-8192"
        ].index(
            get_setting("ai_model")
        )
    )

    update_setting(
        "ai_model",
        ai_model
    )

    st.divider()

    st.success(
        "Settings Applied Successfully ✅"
    )