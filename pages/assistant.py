import os
import streamlit as st

from groq import Groq
from dotenv import load_dotenv

# ======================================
# LOAD ENV
# ======================================

load_dotenv()

# ======================================
# GROQ CLIENT
# ======================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ======================================
# MAIN FUNCTION
# ======================================

def show_traffic_ai():

    # ==================================
    # PAGE TITLE
    # ==================================

    st.title("🤖 Traffic AI Assistant")

    st.write(
        "Ask anything about traffic, roads, CCTV, accidents and smart city AI systems."
    )

    st.write("")

    # ==================================
    # CHAT HISTORY
    # ==================================

    if "messages" not in st.session_state:

        st.session_state.messages = []

    # ==================================
    # SHOW OLD CHATS
    # ==================================

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):

            st.markdown(msg["content"])

    # ==================================
    # USER INPUT
    # ==================================

    user_input = st.chat_input(
        "Ask Traffic AI..."
    )

    # ==================================
    # WHEN USER SENDS MESSAGE
    # ==================================

    if user_input:

        # ------------------------------
        # SAVE USER MESSAGE
        # ------------------------------

        st.session_state.messages.append({

            "role": "user",

            "content": user_input

        })

        # ------------------------------
        # SHOW USER MESSAGE
        # RIGHT SIDE
        # ------------------------------

        with st.chat_message("user"):

            st.markdown(user_input)

        # ------------------------------
        # AI RESPONSE
        # ------------------------------

        try:

            completion = client.chat.completions.create(

                model="llama-3.3-70b-versatile",

                messages=[

                    {
                        "role": "system",

                        "content":
                        """
                        You are Smart Traffic AI.

                        Answer only traffic related questions.

                        Help with:
                        - traffic congestion
                        - smart traffic systems
                        - road safety
                        - accidents
                        - CCTV monitoring
                        - AI traffic control
                        - smart cities

                        Talk like professional AI assistant.
                        """
                    },

                    {
                        "role": "user",

                        "content": user_input
                    }
                ],

                temperature=0.7,

                max_tokens=500
            )

            response = \
            completion.choices[0].message.content

        except Exception as e:

            response = f"Error: {e}"

        # ------------------------------
        # SAVE AI MESSAGE
        # ------------------------------

        st.session_state.messages.append({

            "role": "assistant",

            "content": response

        })

        # ------------------------------
        # SHOW AI MESSAGE
        # LEFT SIDE
        # ------------------------------

        with st.chat_message("assistant"):

            st.markdown(response)