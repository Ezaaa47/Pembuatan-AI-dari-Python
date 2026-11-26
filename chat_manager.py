
import streamlit as st

from config import MAX_HISTORY


def initialize_chat():

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "total_questions" not in st.session_state:
        st.session_state.total_questions = 0


def add_message(role, content):

    st.session_state.messages.append({
        "role": role,
        "content": content
    })

    if role == "user":
        st.session_state.total_questions += 1

    st.session_state.messages = (
        st.session_state.messages[-MAX_HISTORY:]
    )


def get_history():

    history = []

    for message in st.session_state.messages:

        history.append({
            "role": (
                "model"
                if message["role"] == "assistant"
                else "user"
            ),
            "parts": [
                {"text": message["content"]}
            ]
        })

    return history


def clear_chat():

    st.session_state.messages = []
    st.session_state.total_questions = 0
