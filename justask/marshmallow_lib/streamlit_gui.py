"""
Streamlit GUI for the Marshmallows anonymous questions app.

This module provides the Streamlit interface for the application, using the
core functionality from the marshmallow_lib package.
"""

import streamlit as st
from typing import Dict, Optional, Any, List, Callable
import functools
from .core import MarshmallowManager


class SessionState:
    """Helper class to manage Streamlit session state consistently."""
    
    # Keys used in session state
    MANAGER = "marshmallow_manager"
    ADMIN_VIEW = "admin_view"
    DEBUG_MODE = "debug_mode"
    SORT_OPTION = "sort_option"
    CURRENT_TAB = "current_tab"
    RANDOM_QUESTION = "random_question"
    LAST_SORT_OPTION = "last_sort_option"
    
    @staticmethod
    def initialize_if_missing(key: str, default_value: Any) -> None:
        """
        Initialize a session state value if it doesn't exist.
        
        Args:
            key: Session state key
            default_value: Default value to set
        """
        if key not in st.session_state:
            st.session_state[key] = default_value
    
    @staticmethod
    def initialize_manager(storage_type: str) -> None:
        """
        Initialize the MarshmallowManager in session state.
        
        Args:
            storage_type: Storage type for manager
        """
        if SessionState.MANAGER not in st.session_state:
            st.session_state[SessionState.MANAGER] = MarshmallowManager(storage_type=storage_type)
    
    @staticmethod
    def get_manager() -> MarshmallowManager:
        """Get the MarshmallowManager from session state."""
        return st.session_state[SessionState.MANAGER]
    
    @staticmethod
    def setup_initial_state(storage_type: str) -> None:
        """
        Set up all initial session state values.
        
        Args:
            storage_type: Storage type for manager
        """
        # Initialize manager
        SessionState.initialize_manager(storage_type)
        
        # Initialize UI state
        SessionState.initialize_if_missing(SessionState.ADMIN_VIEW, False)
        SessionState.initialize_if_missing(SessionState.DEBUG_MODE, False)
        SessionState.initialize_if_missing(SessionState.SORT_OPTION, "newest")
        SessionState.initialize_if_missing(SessionState.CURRENT_TAB, 0)
        SessionState.initialize_if_missing(SessionState.RANDOM_QUESTION, None)
        SessionState.initialize_if_missing(SessionState.LAST_SORT_OPTION, "newest")
    
    @staticmethod
    def toggle_admin_view() -> None:
        """Toggle admin view state."""
        st.session_state[SessionState.ADMIN_VIEW] = not st.session_state[SessionState.ADMIN_VIEW]
    
    @staticmethod
    def toggle_debug_mode() -> None:
        """Toggle debug mode state."""
        st.session_state[SessionState.DEBUG_MODE] = not st.session_state[SessionState.DEBUG_MODE]
    
    @staticmethod
    def set_current_tab(tab_index: int) -> None:
        """Set the current active tab."""
        st.session_state[SessionState.CURRENT_TAB] = tab_index
    
    @staticmethod
    def set_sort_option(option: str) -> None:
        """Set the current sort option."""
        st.session_state[SessionState.LAST_SORT_OPTION] = st.session_state[SessionState.SORT_OPTION]
        st.session_state[SessionState.SORT_OPTION] = option
    
    @staticmethod
    def store_random_question(question: Dict) -> None:
        """Store the currently displayed random question."""
        st.session_state[SessionState.RANDOM_QUESTION] = question


def setup_page():
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title="Marshmallows - Anonymous Questions",
        page_icon="🍡",
        layout="wide",
    )
    
    # Add custom CSS
    st.markdown("""
    <style>
        .main-header {text-align: center; font-size: 2.5rem; margin-bottom: 20px; color: #333;}
        .question-card {
            padding: 15px; 
            border-radius: 10px; 
            margin: 10px 0px;
            background-color: #f0f2f6;
            border-left: 5px solid #4b6fff;
        }
        .marshmallow-card {
            padding: 15px; 
            border-radius: 10px; 
            margin: 10px 0px;
            background-color: #4b6fff;
            border-left: 5px solid #ff6ec7;
            color: white;
        }
        .question-meta {color: #ddd; font-size: 0.8rem; margin-bottom: 5px;}
        .question-text {font-size: 1.1rem; color: #333; font-weight: 500;}
        .marshmallow-card .question-text {color: white; font-weight: 500;}
        .admin-header {font-size: 1.5rem; margin: 20px 0px 10px 0px; color: #333;}
        .pending {background-color: #fff9e6; border-left: 5px solid #ffc107; color: #333;}
        .approved {background-color: #f0f7f0; border-left: 5px solid #28a745; color: #333;}
        .highlighted {background-color: #e6f3ff; border-left: 5px solid #007bff; color: #333;}
        .user-id {font-style: italic; opacity: 0.8;}
        div[data-testid="stVerticalBlock"] {gap: 0rem !important;}
        .debug-info {background-color: #f8f9fa; border-left: 5px solid #6c757d; padding: 10px; margin: 5px 0; border-radius: 5px;}
    </style>
    """, unsafe_allow_html=True)


def log_debug_info(message: str):
    """
    Log debug information when debug mode is enabled.
    
    Args:
        message: Debug message to display
    """
    if st.session_state.get(SessionState.DEBUG_MODE, False):
        st.markdown(f"<div class='debug-info'>Debug - {message}</div>", unsafe_allow_html=True)


# Use st.fragment directly without custom decorator
@st.fragment
def add_marshmallow_tab():
    """Render the Add a Marshmallow tab."""
    manager = SessionState.get_manager()
    
    st.markdown(f"You are participating as: <span class='user-id'>{manager.user_id}</span>", unsafe_allow_html=True)
    
    with st.form("question_form"):
        question_input = st.text_area(
            "Enter your anonymous question:", 
            height=100, 
            placeholder="Type your question here... Your identity will remain anonymous."
        )
        submit_button = st.form_submit_button("Submit Marshmallow")
        
        if submit_button:
            if manager.add_question(question_input):
                st.success("Your marshmallow has been tossed into the pile!")
                log_debug_info(f"After add: {manager.questions}")
                st.balloons()
            else:
                st.error("Please enter a question before submitting.")


@st.fragment
def random_marshmallow_tab():
    """Render the Pick a Random Marshmallow tab."""
    manager = SessionState.get_manager()
    
    st.markdown("### Get a random marshmallow question")
    st.write("Click the button below to get a random question someone has submitted anonymously.")
    
    # Debug info
    log_debug_info(f"Session questions: {len(manager.questions)}")
    log_debug_info(f"Questions content: {manager.questions}")
    
    if st.button("Pick a Random Marshmallow"):
        random_question = manager.get_random_question()
        if random_question:
            # Store in session state for voting
            SessionState.store_random_question(random_question)
            
            st.markdown(f"""
            <div class='marshmallow-card'>
                <div class='question-text'>"{random_question["text"]}"</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add voting option for random questions
            if st.button(f"👍 Vote ({random_question['votes']})", key=f"vote_random_{random_question['id']}"):
                manager.vote_for_question(random_question['id'])
                st.rerun()  # Rerun the page
        else:
            st.info("No marshmallows available. Be the first to add one!")


@st.fragment
def display_question(q, is_admin=False):
    """
    Display a single question with its controls.
    
    Args:
        q: Question dictionary
        is_admin: Whether to show admin controls
    """
    manager = SessionState.get_manager()
    
    card_class = "marshmallow-card"
    if is_admin:
        if q["status"] == "pending":
            card_class += " pending"
        elif q["status"] == "approved":
            card_class += " approved"
        if q["highlighted"]:
            card_class += " highlighted"
            
    with st.container():
        st.markdown(f"""
        <div class='{card_class}'>
            <div class='question-text'>"{q["text"]}"</div>
            <div class='question-meta'>
                {q["timestamp"].strftime('%I:%M %p')} • Votes: {q["votes"]}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Admin controls
        if is_admin:
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if q["status"] == "pending":
                    if st.button(f"Approve #{q['id']}", key=f"approve_{q['id']}"):
                        manager.set_question_status(q['id'], "approved")
                        st.rerun()
                else:
                    if st.button(f"Hide #{q['id']}", key=f"hide_{q['id']}"):
                        manager.set_question_status(q['id'], "pending")
                        st.rerun()
            
            with col2:
                if not q["highlighted"]:
                    if st.button(f"Highlight #{q['id']}", key=f"highlight_{q['id']}"):
                        manager.highlight_question(q['id'], True)
                        st.rerun()
                else:
                    if st.button(f"Unhighlight #{q['id']}", key=f"unhighlight_{q['id']}"):
                        manager.highlight_question(q['id'], False)
                        st.rerun()
            
            with col3:
                if st.button(f"Delete #{q['id']}", key=f"delete_{q['id']}"):
                    manager.delete_question(q['id'])
                    st.rerun()
        
        # User controls - voting
        if not is_admin:
            if st.button(f"👍 Vote ({q['votes']})", key=f"vote_{q['id']}"):
                manager.vote_for_question(q['id'])
                st.rerun()


@st.fragment
def all_marshmallows_tab():
    """Render the See All Marshmallows tab."""
    manager = SessionState.get_manager()
    
    # Debug info
    log_debug_info(f"Tab3 Session questions: {len(manager.questions)}")
    log_debug_info(f"Tab3 Questions content: {manager.questions}")
    
    # Admin authentication
    admin_col1, admin_col2 = st.columns([3, 1])
    with admin_col1:
        st.markdown("### All marshmallow questions")
    with admin_col2:
        admin_password = "instructor"  # Simple password for demonstration
        password_input = st.text_input("Admin password:", type="password")
        if password_input == admin_password:
            admin_button = st.button("Toggle Admin View", on_click=SessionState.toggle_admin_view)
    
    # Sort options
    sort_options = {"Newest First": "newest", "Most Voted": "votes", "Random Order": "random"}
    
    # Use callback for sort selection to update session state
    def on_sort_change():
        selected = sort_options[st.session_state.sort_selectbox]
        SessionState.set_sort_option(selected)
    
    # Get current sort option from session state
    current_sort_display = next(k for k, v in sort_options.items() if v == st.session_state.get(SessionState.SORT_OPTION, "newest"))
    
    # Create selectbox with callback
    selected_sort_display = st.selectbox(
        "Sort marshmallows by:", 
        list(sort_options.keys()),
        index=list(sort_options.keys()).index(current_sort_display),
        key="sort_selectbox",
        on_change=on_sort_change
    )
    
    # Get the actual sort option value
    selected_sort = sort_options[selected_sort_display]
    
    # Display questions based on sort and admin status
    if manager.questions:
        # Sort questions
        sorted_questions = manager.get_sorted_questions(selected_sort)
        
        # Display questions
        for q in sorted_questions:
            # Skip pending questions for non-admins
            if q["status"] == "pending" and not st.session_state.get(SessionState.ADMIN_VIEW, False):
                continue
                
            display_question(q, st.session_state.get(SessionState.ADMIN_VIEW, False))
    else:
        st.info("No marshmallows have been added yet. Be the first!")


@st.fragment
def admin_section():
    """Render the admin controls section at the bottom of the page."""
    manager = SessionState.get_manager()
    
    st.markdown("---")
    col1, col2 = st.columns([4, 1])
    
    with col1:
        if st.session_state.get(SessionState.ADMIN_VIEW, False):
            st.markdown("### Admin Controls")
            if st.button("Clear All Marshmallows"):
                manager.clear_all_questions()
                st.rerun()  # Full rerun since this is a major change
    
    with col2:
        # Debug mode toggle with session state callback
        debug_toggle = st.checkbox(
            "Debug Mode", 
            value=st.session_state.get(SessionState.DEBUG_MODE, False),
            key="debug_toggle", 
            on_change=SessionState.toggle_debug_mode
        )


def run_streamlit_app(storage_type: str = "memory"):
    """
    Run the Streamlit GUI application.
    
    Args:
        storage_type: Type of storage to use ("memory" or "file")
    """
    # Setup page layout and styling
    setup_page()
    
    # Initialize session state
    SessionState.setup_initial_state(storage_type)
    
    # Create header
    st.markdown("<h1 class='main-header'>Marshmallows - Anonymous Questions</h1>", unsafe_allow_html=True)
    
    # Create tabs for different functionalities
    tab1, tab2, tab3 = st.tabs(["Add a Marshmallow", "Pick a Random Marshmallow", "See All Marshmallows"])
    
    # Track which tab is selected (can't use on_change with tabs directly)
    if "tabs" in st.session_state:
        SessionState.set_current_tab(st.session_state.tabs)
    
    # Tab 1: Add a Marshmallow (Ask Questions)
    with tab1:
        add_marshmallow_tab()
    
    # Tab 2: Pick a Random Marshmallow
    with tab2:
        random_marshmallow_tab()
    
    # Tab 3: See All Marshmallows
    with tab3:
        all_marshmallows_tab()
    
    # Admin controls at the bottom
    admin_section()