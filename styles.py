
import streamlit as st


def load_styles():

    st.markdown("""
    <style>

    /* BACKGROUND */
    .stApp {
        background: #100B0D;
        color: #FFFFFF;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: #1A1013;
        border-right: 1px solid #51212A;
    }

    /* TEXT */
    .stApp p,
    .stApp label,
    .stApp li {
        color: #F3F4F6;
    }

    h1, h2, h3, h4 {
        color: #FFFFFF !important;
    }

    /* HERO */
    .hero {
        background: linear-gradient(
            120deg, #1D1013, #581923, #991B1B
        );
        border: 1px solid #A33240;
        border-radius: 22px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 10px 35px #00000055;
    }

    .hero h1 {
        color: white !important;
        font-size: clamp(28px, 5vw, 42px);
        margin: 0 0 10px 0;
    }

    .hero p {
        color: #FECACA !important;
        line-height: 1.7;
    }

    /* CARDS */
    .feature-card {
        background: linear-gradient(
            145deg, #29171B, #171012
        );
        border: 1px solid #652A35;
        border-radius: 18px;
        padding: 22px;
        min-height: 145px;
        transition: 0.25s;
    }

    .feature-card:hover {
        border-color: #EF4444;
        transform: translateY(-4px);
        box-shadow: 0 8px 25px #DC262633;
    }

    .feature-icon {
        font-size: 32px;
    }

    .feature-title {
        color: white;
        font-size: 17px;
        font-weight: bold;
        margin: 10px 0;
    }

    .feature-desc {
        color: #D1D5DB;
        font-size: 13px;
        line-height: 1.6;
    }

    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(
            90deg, #991B1B, #DC2626
        );
        color: white !important;
        border: 1px solid #EF4444;
        border-radius: 12px;
        min-height: 43px;
        font-weight: 600;
    }

    .stButton > button:hover {
        background: #EF4444;
        border-color: #FCA5A5;
    }

    /* INPUT */
    input, textarea,
    [data-baseweb="input"] input {
        background: #25171A !important;
        color: white !important;
        border-color: #71313A !important;
    }

    /* CHAT */
    [data-testid="stChatMessage"] {
        background: #211518;
        border: 1px solid #572630;
        border-radius: 16px;
        padding: 14px;
        margin-bottom: 12px;
    }

    /* METRICS */
    [data-testid="stMetric"] {
        background: #241619;
        border: 1px solid #602B35;
        border-radius: 14px;
        padding: 15px;
    }

    /* STATUS */
    .status {
        background: #17271D;
        border: 1px solid #28613C;
        border-radius: 12px;
        padding: 13px;
        color: #86EFAC;
    }

    /* FOOTER */
    .footer {
        text-align: center;
        color: #BFAEB2;
        padding: 30px 0;
        font-size: 12px;
    }

    /* DIVIDER */
    hr {
        border-color: #54252D;
    }

    </style>
    """, unsafe_allow_html=True)
