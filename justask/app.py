import streamlit as st
import datetime
import random
import uuid

# Page configuration
st.set_page_config(
    page_title="Marshmallows - Anonymous Questions",
    page_icon="🍡",
    layout="wide",
)

# Initialize session state variables if they don't exist
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'admin_view' not in st.session_state:
    st.session_state.admin_view = False
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'viewed_questions' not in st.session_state:
    st.session_state.viewed_questions = set()
if 'debug_mode' not in st.session_state:
    st.session_state.debug_mode = False

# Generate a unique identifier for each user session
if 'user_id' not in st.session_state:
    animal_names = ["Dolphin", "Penguin", "Tiger", "Elephant", "Koala", "Flamingo", "Panda", "Zebra", "Fox", "Owl"]
    colors = ["Red", "Blue", "Green", "Purple", "Golden", "Silver", "Orange", "Teal", "Emerald", "Azure"]
    st.session_state.user_id = f"{random.choice(colors)} {random.choice(animal_names)}"

# Function to toggle debug mode
def toggle_debug_mode():
    st.session_state.debug_mode = not st.session_state.debug_mode

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

# Function to add a new question
def add_question(question_text):
    if question_text.strip():
        st.session_state.questions.append({
            "id": len(st.session_state.questions),
            "text": question_text,
            "timestamp": datetime.datetime.now(),
            "status": "approved",  # All questions are immediately approved
            "user_id": st.session_state.user_id,
            "highlighted": False,
            "votes": 0
        })
        return True
    return False

# Function to toggle admin view
def toggle_admin_view():
    st.session_state.admin_view = not st.session_state.admin_view

# Function to get a random question
def get_random_question():
    approved_questions = [q for q in st.session_state.questions if q["status"] == "approved"]
    if not approved_questions:
        return None
    
    # Filter out recently viewed questions unless all have been viewed
    unviewed = [q for q in approved_questions if q["id"] not in st.session_state.viewed_questions]
    if not unviewed and approved_questions:
        # Reset viewed questions if all have been seen
        st.session_state.viewed_questions = set()
        unviewed = approved_questions
    
    if unviewed:
        question = random.choice(unviewed)
        st.session_state.viewed_questions.add(question["id"])
        return question
    return None

# Create header
st.markdown("<h1 class='main-header'>Marshmallows - Anonymous Questions</h1>", unsafe_allow_html=True)

# Create tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["Add a Marshmallow", "Pick a Random Marshmallow", "See All Marshmallows"])

# Tab 1: Add a Marshmallow (Ask Questions)
with tab1:
    st.markdown(f"You are participating as: <span class='user-id'>{st.session_state.user_id}</span>", unsafe_allow_html=True)
    
    with st.form("question_form"):
        question_input = st.text_area("Enter your anonymous question:", height=100, 
                                     placeholder="Type your question here... Your identity will remain anonymous.")
        submit_button = st.form_submit_button("Submit Marshmallow")
        
        if submit_button:
            if add_question(question_input):
                st.success("Your marshmallow has been tossed into the pile!")
                if st.session_state.debug_mode:
                    st.markdown(f"<div class='debug-info'>Debug - After add: {st.session_state.questions}</div>", unsafe_allow_html=True)
                st.balloons()
            else:
                st.error("Please enter a question before submitting.")

# Tab 2: Pick a Random Marshmallow
with tab2:
    st.markdown("### Get a random marshmallow question")
    st.write("Click the button below to get a random question someone has submitted anonymously.")

    # Debug info
    if st.session_state.debug_mode:
        st.markdown(f"<div class='debug-info'>Debug - Session questions: {len(st.session_state.questions)}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='debug-info'>Debug - Questions content: {st.session_state.questions}</div>", unsafe_allow_html=True)

    if st.button("Pick a Random Marshmallow"):
        random_question = get_random_question()
        if random_question:
            st.markdown(f"""
            <div class='marshmallow-card'>
                <div class='question-text'>"{random_question["text"]}"</div>
            </div>
            """, unsafe_allow_html=True)

            # Add voting option for random questions
            if st.button(f"👍 Vote ({random_question['votes']})", key=f"vote_random_{random_question['id']}"):
                random_question["votes"] += 1
                st.rerun()
        else:
            st.info("No marshmallows available. Be the first to add one!")

# Tab 3: See All Marshmallows
with tab3:
    # Debug info
    if st.session_state.debug_mode:
        st.markdown(f"<div class='debug-info'>Debug - Tab3 Session questions: {len(st.session_state.questions)}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='debug-info'>Debug - Tab3 Questions content: {st.session_state.questions}</div>", unsafe_allow_html=True)

    # Admin authentication
    admin_col1, admin_col2 = st.columns([3, 1])
    with admin_col1:
        st.markdown("### All marshmallow questions")
    with admin_col2:
        admin_password = "instructor"  # Simple password for demonstration
        password_input = st.text_input("Admin password:", type="password")
        if password_input == admin_password:
            admin_button = st.button("Toggle Admin View", on_click=toggle_admin_view)
    
    # Sort options
    sort_options = ["Newest First", "Most Voted", "Random Order"]
    selected_sort = st.selectbox("Sort marshmallows by:", sort_options)
    
    # Display questions based on sort and admin status
    if st.session_state.questions:
        # Sort questions
        if selected_sort == "Newest First":
            sorted_questions = sorted(st.session_state.questions, key=lambda x: x["timestamp"], reverse=True)
        elif selected_sort == "Most Voted":
            sorted_questions = sorted(st.session_state.questions, key=lambda x: x["votes"], reverse=True)
        elif selected_sort == "Random Order":
            sorted_questions = st.session_state.questions.copy()
            random.shuffle(sorted_questions)
        
        # Display questions
        for q in sorted_questions:
            card_class = "marshmallow-card"
            if st.session_state.admin_view:
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
                if st.session_state.admin_view:
                    col1, col2, col3 = st.columns([1, 1, 1])
                    
                    with col1:
                        if q["status"] == "pending":
                            if st.button(f"Approve #{q['id']}", key=f"approve_{q['id']}"):
                                q["status"] = "approved"
                                st.rerun()
                        else:
                            if st.button(f"Hide #{q['id']}", key=f"hide_{q['id']}"):
                                q["status"] = "pending"
                                st.rerun()
                    
                    with col2:
                        if not q["highlighted"]:
                            if st.button(f"Highlight #{q['id']}", key=f"highlight_{q['id']}"):
                                q["highlighted"] = True
                                st.rerun()
                        else:
                            if st.button(f"Unhighlight #{q['id']}", key=f"unhighlight_{q['id']}"):
                                q["highlighted"] = False
                                st.rerun()
                    
                    with col3:
                        if st.button(f"Delete #{q['id']}", key=f"delete_{q['id']}"):
                            st.session_state.questions.remove(q)
                            st.rerun()
                
                # User controls - voting
                if not st.session_state.admin_view:
                    if st.button(f"👍 Vote ({q['votes']})", key=f"vote_{q['id']}"):
                        q["votes"] += 1
                        st.rerun()
    else:
        st.info("No marshmallows have been added yet. Be the first!")

# Small admin section at the bottom
st.markdown("---")
col1, col2 = st.columns([4, 1])

with col1:
    if st.session_state.admin_view:
        st.markdown("### Admin Controls")
        if st.button("Clear All Marshmallows"):
            st.session_state.questions = []
            st.rerun()

with col2:
    # Debug mode toggle
    debug_toggle = st.checkbox("Debug Mode", value=st.session_state.debug_mode, key="debug_toggle", on_change=toggle_debug_mode)