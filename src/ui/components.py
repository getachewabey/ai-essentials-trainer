import streamlit as st
import os

def render_sidebar():
    with st.sidebar:
        st.title("AI Essentials Trainer")
        
        if "current_page" not in st.session_state:
            st.session_state.current_page = "Dashboard"
            
        # Map page names to indices
        pages = [
            "Dashboard",
            "Learning Path",
            "Lesson Generator",
            "Labs",
            "Quiz Engine",
            "Scenarios",
            "Submission & Grading",
            "Settings"
        ]
        
        try:
            current_index = pages.index(st.session_state.get("current_page", "Dashboard"))
        except ValueError:
            current_index = 0
            
        page = st.radio("Navigation", pages, index=current_index)
        
        # Update session state when radio changes
        if page != st.session_state.get("current_page"):
            st.session_state.current_page = page
            st.rerun()
        
        # Theme Toggle
        st.markdown("---")
        is_dark = st.session_state.get("theme", "light") == "dark"
        dark_mode = st.toggle("Dark Mode", value=is_dark)
        
        new_theme = "dark" if dark_mode else "light"
        if new_theme != st.session_state.get("theme", "light"):
            st.session_state.theme = new_theme
            st.rerun()

        st.markdown("---")
        if not os.getenv("OPENAI_API_KEY") and not st.session_state.get("openai_api_key"):
            st.error("🔑 API Key Missing")
        
        return page

def check_api_key():
    if os.getenv("OPENAI_API_KEY"):
        return True
    
    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = ""
    
    if not st.session_state.openai_api_key:
        st.warning("Please configure your OpenAI API Key in Settings or .env")
        return False
    return True

def render_privacy_notice():
    if not st.session_state.get("privacy_accepted", False):
        st.info("🔒 **Privacy Notice**: Avoid submitting sensitive PII. Submissions are processed by AI.")

def display_streaming_content(placeholder, content: str):
    """Updates a placeholder with accumulated content"""
    placeholder.markdown(content)
