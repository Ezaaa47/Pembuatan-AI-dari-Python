
import streamlit as st

from config import APP_NAME, APP_VERSION


def render_header():

    st.markdown("""
    <div class="hero">
        <h1>Smart Daily Assistant ✨</h1>
        <p>
            Your Personal AI Assistant.
            Teman pintar untuk belajar, bekerja,
            dan membantu aktivitas sehari-hari.
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_feature_card(icon, title, description):

    st.markdown(f"""
    <div class="feature-card">
        <div class="feature-icon">{icon}</div>
        <div class="feature-title">{title}</div>
        <div class="feature-desc">{description}</div>
    </div>
    """, unsafe_allow_html=True)


def render_footer():

    st.markdown(f"""
    <div class="footer">
        🤖 {APP_NAME}
        <br>
        Version {APP_VERSION}
        <br><br>
        Powered by Python, Streamlit & Google Gemini AI
        <br>
        © 2026 Smart Daily Assistant
    </div>
    """, unsafe_allow_html=True)
