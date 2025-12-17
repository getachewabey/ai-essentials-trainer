import streamlit as st

def load_custom_css(theme="light"):
    # Define themes
    themes = {
        "light": {
            "bg_color": "#ffffff",
            "text_color": "#333333",
            "card_bg": "#ffffff",
            "border_color": "#f0f0f0",
            "sidebar_bg": "#f8f9fa",
            "input_bg": "#ffffff"
        },
        "dark": {
            "bg_color": "#0e1117",
            "text_color": "#fafafa",
            "card_bg": "#262730",
            "border_color": "#3d404a",
            "sidebar_bg": "#262730",
            "input_bg": "#3d404a"
        }
    }
    
    current = themes.get(theme, themes["light"])

    st.markdown(f"""
        <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        :root {{
            --bg-color: {current['bg_color']};
            --text-color: {current['text_color']};
            --card-bg: {current['card_bg']};
            --border-color: {current['border_color']};
            --sidebar-bg: {current['sidebar_bg']};
            --input-bg: {current['input_bg']};
        }}

        /* Global Font */
        /* Global Font */
        html, body, [class*="css"]  {{
            font-family: 'Inter', sans-serif;
            color: var(--text-color);
        }}
        
        /* App Container Background */
        .stApp {{
            background-color: var(--bg-color);
            color: var(--text-color);
        }}

        /* Text Elements & Labels */
        p, label, .stMarkdown, .stText {{
            color: var(--text-color) !important;
        }}

        /* Inputs & Selectboxes */
        .stTextInput input, .stSelectbox, .stNumberInput input, .stTextArea textarea, div[data-baseweb="select"] {{
            background-color: var(--input-bg) !important;
            color: var(--text-color) !important;
            border-color: var(--border-color) !important;
        }}
        
        /* Dropdown Menu Items */
        ul[data-testid="stSelectboxVirtualDropdown"] li {{
            background-color: var(--card-bg) !important;
            color: var(--text-color) !important;
        }}

        /* Radio Buttons & Checkboxes */
        div[role="radiogroup"] label {{
            color: var(--text-color) !important;
        }}

        /* Gradient Background for Headers */
        h1, h2, h3 {{
            background: -webkit-linear-gradient(45deg, #FF4B4B, #FF914D);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }}

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {{
            background-color: var(--sidebar-bg);
        }}
        
        section[data-testid="stSidebar"] * {{
            color: var(--text-color) !important; # Force sidebar text
        }}

        /* Custom Button Styling */
        .stButton button {{
            background: linear-gradient(90deg, #FF4B4B 0%, #FF9068 100%);
            color: white !important;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
        }}

        .stButton button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3);
        }}
        
        .stButton button p {{
            color: white !important; /* Ensure button text stays white */
        }}

        /* Expander Styling */
        .streamlit-expanderHeader {{
            border-radius: 8px;
            background-color: var(--card_bg);
            border: 1px solid var(--border-color);
            color: var(--text-color);
        }}
        
        /* Metric Cards */
        div[data-testid="stMetricValue"] {{
            font-size: 2rem;
            color: #FF4B4B !important;
        }}

        /* Success/Info Alerts */
        .stAlert {{
            border-radius: 8px;
        }}
        
        /* Custom "Card" helper class for markdown */
        .custom-card {{
            padding: 1.5rem;
            border-radius: 12px;
            background-color: var(--card-bg);
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border: 1px solid var(--border-color);
            margin-bottom: 1rem;
            color: var(--text-color);
        }}
        </style>
    """, unsafe_allow_html=True)

def card_start():
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)

def card_end():
    st.markdown('</div>', unsafe_allow_html=True)
