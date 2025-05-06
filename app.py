# some great work by claude (his research notes are included in the repo)

import streamlit as st
import datetime
import random
import uuid

# Page configuration
st.set_page_config(
    page_title="LLM Q&A Session",
    page_icon="💬",
    layout="wide",
)

# Initialize session state variables if they don't exist
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'admin_view' not in st.session_state:
    st.session_state.admin_view = False
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Generate a unique identifier for each user session
if 'user_id' not in st.session_state:
    animal_names = ["Dolphin", "Penguin", "Tiger", "Elephant", "Koala", "Flamingo", "Panda", "Zebra", "Fox", "Owl"]
    colors = ["Red", "Blue", "Green", "Purple", "Golden", "Silver", "Orange", "Teal", "Emerald", "Azure"]
    st.session_state.user_id = f"{random.choice(colors)} {random.choice(animal_names)}"

# Add custom CSS
st.markdown("""
<style>
    .main-header {text-align: center; font-size: 2.5rem; margin-bottom: 20px;}
    .question-card {
        padding: 15px; 
        border-radius: 10px; 
        margin: 10px 0px;
        background-color: #f0f2f6;
        border-left: 5px solid #4b6fff;
    }
    .question-meta {color: #666; font-size: 0.8rem; margin-bottom: 5px;}
    .question-text {font-size: 1.1rem;}
    .admin-header {font-size: 1.5rem; margin: 20px 0px 10px 0px;}
    .pending {background-color: #fff9e6; border-left: 5px solid #ffc107;}
    .approved {background-color: #f0f7f0; border-left: 5px solid #28a745;}
    .highlighted {background-color: #e6f3ff; border-left: 5px solid #007bff;}
    .user-id {font-style: italic; opacity: 0.8;}
    div[data-testid="stVerticalBlock"] {gap: 0rem !important;}
</style>
""", unsafe_allow_html=True)

# Function to add a new question
def add_question(question_text):
    if question_text.strip():
        st.session_state.questions.append({
            "id": len(st.session_state.questions),
            "text": question_text,
            "timestamp": datetime.datetime.now(),
            "status": "pending",
            "user_id": st.session_state.user_id,
            "highlighted": False,
            "votes": 0
        })
        return True
    return False

# Function to toggle admin view
def toggle_admin_view():
    st.session_state.admin_view = not st.session_state.admin_view

# Create header
st.markdown("<h1 class='main-header'>LLM Q&A Session</h1>", unsafe_allow_html=True)

# Create tabs for different functionalities
tab1, tab2 = st.tabs(["Ask Questions", "See Questions"])

# Tab 1: Ask Questions
with tab1:
    st.markdown(f"You are participating as: <span class='user-id'>{st.session_state.user_id}</span>", unsafe_allow_html=True)
    
    with st.form("question_form"):
        question_input = st.text_area("Enter your question:", height=100, 
                                     placeholder="Type your question for the LLMs here... Your identity will remain anonymous.")
        submit_button = st.form_submit_button("Submit Question")
        
        if submit_button:
            if add_question(question_input):
                st.success("Your question has been submitted!")
                st.balloons()
            else:
                st.error("Please enter a question before submitting.")

# Tab 2: See Questions
with tab2:
    # Admin authentication
    admin_col1, admin_col2 = st.columns([3, 1])
    with admin_col1:
        st.markdown("### View submitted questions")
    with admin_col2:
        admin_password = "instructor"  # Simple password for demonstration
        password_input = st.text_input("Admin password:", type="password")
        if password_input == admin_password:
            admin_button = st.button("Toggle Admin View", on_click=toggle_admin_view)
    
    # Filter controls
    filter_options = ["All Questions", "Pending", "Approved", "Highlighted"]
    selected_filter = st.selectbox("Filter questions:", filter_options)
    
    # Display questions based on filter and admin status
    if st.session_state.questions:
        # Sort questions by timestamp (newest first)
        sorted_questions = sorted(st.session_state.questions, key=lambda x: x["timestamp"], reverse=True)
        
        # Apply filters
        filtered_questions = sorted_questions
        if selected_filter == "Pending":
            filtered_questions = [q for q in sorted_questions if q["status"] == "pending"]
        elif selected_filter == "Approved":
            filtered_questions = [q for q in sorted_questions if q["status"] == "approved"]
        elif selected_filter == "Highlighted":
            filtered_questions = [q for q in sorted_questions if q["highlighted"]]
        
        # Display questions
        for q in filtered_questions:
            card_class = "question-card"
            if q["status"] == "pending":
                card_class += " pending"
            elif q["status"] == "approved":
                card_class += " approved"
            if q["highlighted"]:
                card_class += " highlighted"
                
            with st.container():
                st.markdown(f"""
                <div class='{card_class}'>
                    <div class='question-meta'>
                        Asked by {q["user_id"]} • {q["timestamp"].strftime('%I:%M %p')}
                    </div>
                    <div class='question-text'>{q["text"]}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Admin controls
                if st.session_state.admin_view:
                    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
                    
                    with col1:
                        if q["status"] == "pending":
                            if st.button(f"Approve #{q['id']}", key=f"approve_{q['id']}"):
                                q["status"] = "approved"
                                st.experimental_rerun()
                        else:
                            if st.button(f"Pending #{q['id']}", key=f"pending_{q['id']}"):
                                q["status"] = "pending"
                                st.experimental_rerun()
                    
                    with col2:
                        if not q["highlighted"]:
                            if st.button(f"Highlight #{q['id']}", key=f"highlight_{q['id']}"):
                                q["highlighted"] = True
                                st.experimental_rerun()
                        else:
                            if st.button(f"Unhighlight #{q['id']}", key=f"unhighlight_{q['id']}"):
                                q["highlighted"] = False
                                st.experimental_rerun()
                    
                    with col3:
                        if st.button(f"Delete #{q['id']}", key=f"delete_{q['id']}"):
                            st.session_state.questions.remove(q)
                            st.experimental_rerun()
                    
                    with col4:
                        if st.button(f"Pin to Top #{q['id']}", key=f"pin_{q['id']}"):
                            # Move this question to the top by updating timestamp
                            q["timestamp"] = datetime.datetime.now() + datetime.timedelta(days=1)
                            st.experimental_rerun()
                
                # User controls - voting
                if not st.session_state.admin_view:
                    if st.button(f"👍 Vote ({q['votes']})", key=f"vote_{q['id']}"):
                        q["votes"] += 1
                        st.experimental_rerun()
    else:
        st.info("No questions have been submitted yet.")

# Small admin section at the bottom
st.markdown("---")
if st.session_state.admin_view:
    st.markdown("### Admin Controls")
    if st.button("Clear All Questions"):
        st.session_state.questions = []
        st.experimental_rerun()
