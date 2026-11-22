
import streamlit as st


def apply_theme(page="Dashboard"):
    themes = {
        "Dashboard": {
            "primary": "#FF354F",
            "glow": "rgba(255, 53, 79, 0.35)"
        },
        "My Notes": {
            "primary": "#A875FF",
            "glow": "rgba(168, 117, 255, 0.35)"
        },
        "Study Planner": {
            "primary": "#785CFF",
            "glow": "rgba(120, 92, 255, 0.35)"
        },
        "Quiz": {
            "primary": "#D45CFF",
            "glow": "rgba(212, 92, 255, 0.35)"
        }
    }

    theme = themes.get(page, themes["Dashboard"])

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    h1, h2, h3, h4 {{
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: -1px;
    }}

    h1 {{
        font-size: 2.8rem !important;
        font-weight: 800 !important;
    }}

    h2 {{
        font-size: 2rem !important;
        font-weight: 700 !important;
    }}

    .stApp {{
        background:
            radial-gradient(circle at 85% 5%, {theme["glow"]}, transparent 28%),
            linear-gradient(135deg, #08080D 0%, #101019 50%, #090910 100%);
        color: #F4F0FF;
    }}

    [data-testid="stSidebar"] {{
        background: #0C0C14;
        border-right: 1px solid #292438;
    }}

    [data-testid="stSidebar"] h1 {{
        color: {theme["primary"]};
        font-size: 1.8rem !important;
    }}
        [data-testid="stSidebar"] div[role="radiogroup"] {{
        gap: 0.5rem;
    }}

    [data-testid="stSidebar"] div[role="radiogroup"] label {{
        background: rgba(255, 255, 255, 0.025);
        border: 1px solid transparent;
        border-radius: 12px;
        padding: 10px 12px;
        transition: all 0.25s ease;
    }}

    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
        background: rgba(255, 255, 255, 0.08);
        border-color: {theme["primary"]};
        transform: translateX(4px);
    }}

    [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {{
        background: linear-gradient(
            100deg,
            {theme["glow"]},
            rgba(255, 255, 255, 0.04)
        );
        border: 1px solid {theme["primary"]};
        box-shadow: 0 0 15px {theme["glow"]};
    }}

    [data-testid="stMetric"] {{
        background: rgba(255,255,255,0.035);
        border: 1px solid #302A40;
        padding: 20px;
        border-radius: 16px;
        transition: all 0.25s ease;
    }}

    [data-testid="stMetric"]:hover {{
        border-color: {theme["primary"]};
        transform: translateY(-4px);
        box-shadow: 0 8px 30px {theme["glow"]};
    }}

    .stButton > button,
    .stFormSubmitButton > button {{
        border: 1px solid {theme["primary"]};
        border-radius: 12px;
        background: linear-gradient(135deg, {theme["primary"]}, #5426A8);
        color: white;
        font-weight: 700;
        transition: all 0.2s ease;
        box-shadow: 0 0 12px {theme["glow"]};
    }}

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {{
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 0 24px {theme["glow"]};
        border-color: white;
        color: white;
    }}

    .stButton > button:active,
    .stFormSubmitButton > button:active {{
        transform: scale(0.96);
    }}

    [data-testid="stExpander"] {{
        background: rgba(255,255,255,0.025);
        border: 1px solid #302A40;
        border-radius: 14px;
    }}

    [data-testid="stMainBlockContainer"] {{
        animation: pageEnter 0.45s ease both;
    }}

    @keyframes pageEnter {{
        from {{ opacity: 0; transform: translateY(12px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    hr {{
        border-color: #302A40;
    }}

    p, label, li {{
        color: #D0CCDC;
    }}
    </style>
    """, unsafe_allow_html=True)
