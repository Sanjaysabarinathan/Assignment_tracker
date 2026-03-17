import streamlit as st
from database.database import init_db
from components import teacher_dashboard, student_dashboard
from utils.helpers import load_css

# Application Setup
st.set_page_config(
    page_title="Assignment Tracker V2",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database
init_db()

# Session State Initialization
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "theme" not in st.session_state:
    st.session_state["theme"] = "Light Mode"

def login():
    st.sidebar.markdown("### 🔐 Teacher Login")
    with st.sidebar.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if username == "admin" and password == "admin123":
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("Invalid username or password.")

def logout():
    st.session_state["logged_in"] = False
    st.rerun()

# Main App Logic
def main():
    # Render Theme early
    load_css(st.session_state["theme"])
    
    st.sidebar.title("📚 Assignment Tracker")
    st.sidebar.markdown("Welcome to the **Assignment Deadline Tracker**.")
    
    # Theme Toggle
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎨 Theme Preference")
    theme = st.sidebar.radio("Select Theme:", ["Light Mode", "Dark Mode"], 
                            index=0 if st.session_state["theme"] == "Light Mode" else 1)
    
    if theme != st.session_state["theme"]:
        st.session_state["theme"] = theme
        st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("👤 Navigation")
    role = st.sidebar.radio("Select View:", ["Student", "Teacher"])
    
    if role == "Teacher":
        if not st.session_state["logged_in"]:
            st.warning("Please login to access teacher dashboard")
            login()
        else:
            if st.sidebar.button("🚪 Logout"):
                logout()
            teacher_dashboard.render()
    else:
        # Student View
        student_dashboard.render()

if __name__ == "__main__":
    main()
