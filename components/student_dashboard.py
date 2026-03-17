import streamlit as st
import pandas as pd
import database.database as db
from utils.helpers import calculate_days_remaining, get_status_color, render_stat_card

def render():
    st.markdown("<h1 style='text-align: center; color: var(--text-color);'>🎓 Student Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>View all your upcoming deadlines.</p>", unsafe_allow_html=True)
    st.divider()
    
    df = db.get_all_assignments()
    
    if df.empty:
        st.info("No upcoming assignments! 🎉")
        return
        
    # Data Processing
    df['Days Remaining'] = df['deadline'].apply(calculate_days_remaining)
    df['Status'] = df['Days Remaining'].apply(get_status_color)
    
    # Filtering
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 Filters")
    subjects = ["All"] + list(df['subject'].unique())
    selected_subject = st.sidebar.selectbox("Filter by Subject", subjects)
    
    if selected_subject != "All":
        df = df[df['subject'] == selected_subject]
        
    if df.empty:
        st.info(f"No assignments found for {selected_subject}.")
        return

    # Metrics with Animated Custom CSS Cards
    col1, col2, col3 = st.columns(3)
    urgent_count = len(df[(df['Days Remaining'] >= 0) & (df['Days Remaining'] <= 2)])
    overdue_count = len(df[df['Days Remaining'] < 0])
    
    with col1:
        render_stat_card("Total Assignments", len(df), "📝")
    with col2:
        render_stat_card("Urgent (≤ 2 Days)", urgent_count, "⚠️")
    with col3:
        render_stat_card("Overdue", overdue_count, "🚨")

    st.markdown("<br><h2 style='text-align: center;'>⏳ Upcoming Deadlines</h2>", unsafe_allow_html=True)
    
    # Format dataframe for display
    display_df = df[['subject', 'title', 'description', 'deadline', 'Days Remaining', 'Status']].copy()
    display_df.columns = ['Subject', 'Title', 'Description', 'Deadline', 'Days Remaining', 'Status']
    
    # Display styled dataframe
    st.dataframe(
        display_df,
        column_config={
            "Days Remaining": st.column_config.NumberColumn(
                "Days Remaining",
                help="Days until the deadline",
                format="%d days"
            ),
        },
        use_container_width=True,
        hide_index=True
    )
