import streamlit as st
from dotenv import load_dotenv, find_dotenv
import os

# Load env vars from .env file (searching upwards)
load_dotenv(find_dotenv(), override=True)

from src.ui.components import render_sidebar, check_api_key, render_privacy_notice
from src.ui.pages import (
    render_dashboard, render_learning_path, render_lesson_generator,
    render_labs, render_quiz_engine, render_scenarios,
    render_submission, render_settings
)
from src.ui.styles import load_custom_css

# Page Config
st.set_page_config(
    page_title="AI Essentials Trainer",
    page_icon="🎓",
    layout="wide"
)

# Apply Styles
if "theme" not in st.session_state:
    st.session_state.theme = "light"

load_custom_css(st.session_state.theme)
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ""

def main():
    render_privacy_notice()
    
    page = render_sidebar()
    
    # Check for API Key for most pages (except Settings and Dashboard maybe)
    # But Dashboard loads progress which is safe. Lesson Gen needs Key.
    # We'll just check it inside the pages or warn globally.
    if page != "Settings" and not check_api_key():
        st.stop()
        
    if page == "Dashboard":
        render_dashboard()
    elif page == "Learning Path":
        render_learning_path()
    elif page == "Lesson Generator":
        render_lesson_generator()
    elif page == "Labs":
        render_labs()
    elif page == "Quiz Engine":
        render_quiz_engine()
    elif page == "Scenarios":
        render_scenarios()
    elif page == "Submission & Grading":
        render_submission()
    elif page == "Settings":
        render_settings()

if __name__ == "__main__":
    main()
