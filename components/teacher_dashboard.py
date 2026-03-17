import streamlit as st
import database.database as db
from datetime import datetime

def render():
    st.markdown("<h1 style='text-align: center;'>👨‍🏫 Teacher Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Manage your class assignments here.</p>", unsafe_allow_html=True)
    
    st.divider()
    
    # Add Assignment Form
    st.markdown("<h2>➕ Add Assignment</h2>", unsafe_allow_html=True)
    with st.form("add_assignment_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            subject = st.text_input("Subject *", placeholder="e.g. DBMS")
            title = st.text_input("Assignment Title *")
        with col2:
            deadline = st.date_input("Deadline *", min_value=datetime.today())
            
        description = st.text_area("Description")
        
        submitted = st.form_submit_button("Create Assignment", use_container_width=True)
        
        if submitted:
            if not subject.strip() or not title.strip():
                st.error("Subject and Title are required fields!")
            else:
                db.add_assignment(
                    subject.strip(), 
                    title.strip(), 
                    description.strip(), 
                    deadline.strftime("%Y-%m-%d")
                )
                st.success(f"Assignment '{title}' added successfully!")
                
    st.divider()
    
    # View and Delete Assignments
    st.markdown("<h2>📋 Current Assignments</h2>", unsafe_allow_html=True)
    df = db.get_all_assignments()
    
    if df.empty:
        st.info("No assignments have been created yet.")
    else:
        # Loop through existing assignments and render them elegantly
        for index, row in df.iterrows():
            with st.container():
                # We wrap each in an animated card container from our global CSS
                st.markdown(f"""
                <div style='padding: 15px; border-radius: 10px; border: 1px solid var(--border-color); margin-bottom: 10px; background-color: var(--secondary-background-color); transition: transform 0.2s;'>
                    <h4>{row['subject']} - {row['title']}</h4>
                    <p style='color: gray; margin-bottom: 5px;'><small><b>Due: {row['deadline']}</b></small></p>
                    <p>{row['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Delete functionality
                if st.button("Delete Assignment", key=f"del_{row['id']}", help=f"Remove {row['title']}"):
                    db.delete_assignment(row['id'])
                    st.rerun()
            st.markdown("<hr style='margin: 10px 0; opacity: 0.2;'>", unsafe_allow_html=True)
