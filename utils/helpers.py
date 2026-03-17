import streamlit as st
from datetime import datetime

def calculate_days_remaining(deadline_str):
    """Calculates days remaining from today to the given deadline."""
    if not deadline_str:
        return 0
    
    try:
        deadline_date = datetime.strptime(str(deadline_str), "%Y-%m-%d").date()
        today = datetime.now().date()
        days_remaining = (deadline_date - today).days
        return days_remaining
    except ValueError:
        return 0

def get_status_color(days_remaining):
    """Returns a color indicator based on days remaining."""
    if days_remaining < 0:
        return "🔴 Overdue"
    elif days_remaining == 0:
        return "🔴 Today"
    elif days_remaining <= 2:
        return "🟠 Urgent (≤2 days)"
    else:
        return "🟢 Normal"

def load_css(theme="Light Mode"):
    """Injects custom CSS based on the selected theme, including animations."""
    
    # Base CSS with animations
    base_css = """
    <style>
        /* Fade-in Animation for the whole page */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .stApp {
            animation: fadeIn 0.8s ease-out;
        }

        /* Animated Statistics Cards */
        .stat-card {
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            margin-bottom: 20px;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        }
        
        .stat-value {
            font-size: 36px;
            font-weight: bold;
            margin: 10px 0;
        }
        
        .stat-label {
            font-size: 16px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Smooth table loading */
        [data-testid="stDataFrame"] {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }
        [data-testid="stDataFrame"]:hover {
            box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        }
    """
    
    # Theme specific CSS
    if theme == "Dark Mode":
        theme_css = """
        /* Dark Theme Variables */
        .stat-card {
            background: linear-gradient(145deg, #1e1e24, #2a2a32);
            border: 1px solid #3a3a45;
            color: #ffffff;
        }
        .stat-value { color: #f0f0f5; }
        .stat-label { color: #aaaaaa; }
        
        /* Force dark text on specific elements to look better */
        h1, h2, h3, h4, h5, h6, p, span {
            color: #f0f0f5;
        }
        </style>
        """
    else:
        theme_css = """
        /* Light Theme Variables */
        .stat-card {
            background: linear-gradient(145deg, #ffffff, #f0f2f6);
            border: 1px solid #e0e4eb;
            color: #31333f;
        }
        .stat-value { color: #1f2129; }
        .stat-label { color: #555555; }
        </style>
        """
        
    st.markdown(base_css + theme_css, unsafe_allow_html=True)

def render_stat_card(label, value, icon=""):
    """Renders a modern animated generic statistics card."""
    card_html = f"""
    <div class="stat-card">
        <div class="stat-value">{icon} {value}</div>
        <div class="stat-label">{label}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
