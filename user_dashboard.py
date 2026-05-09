import streamlit as st

def show_user_page():
    st.title("Volunteer Upload Portal")
    from app import run_data_upload
    
    file = st.file_uploader("Upload Emergency Report (PDF)", type="pdf")
    if file and st.button("Submit Report"):
        run_data_upload(file) # Passes the file to app.py