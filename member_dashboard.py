import streamlit as st

def show_member_page():
    st.title("NGO Staff Dashboard")
    # Show some fake stats
    st.bar_chart({"Reports": [5, 10, 2], "Urgency": [2, 8, 4]})
    
    from app import run_emergency_ai
    run_emergency_ai() # Runs the AI search