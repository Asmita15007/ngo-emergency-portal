import streamlit as st

st.set_page_config(page_title="NGO Emergency Portal", layout="wide")

# Initialize User Database
if 'user_db' not in st.session_state:
    st.session_state['user_db'] = {"admin@ngo.org": {"pass": "admin123", "role": "member"}}

if 'role' not in st.session_state:
    st.session_state['role'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None

if st.session_state['role'] is None:
    st.title("🏥 NGO Emergency Portal")
    email = st.text_input("Email", key="auth_email")
    pw = st.text_input("Password", type="password", key="auth_pw")
    
    if st.button("Enter Portal"):
        if email in st.session_state['user_db']:
            if st.session_state['user_db'][email]["pass"] == pw:
                st.session_state['role'] = st.session_state['user_db'][email]["role"]
                st.session_state['username'] = email
                st.rerun()
            else:
                st.error("Wrong password")
        else:
            # Auto-register new users
            st.session_state['user_db'][email] = {"pass": pw, "role": "user"}
            st.session_state['role'] = "user"
            st.session_state['username'] = email
            st.rerun()

elif st.session_state['role'] == "member":
    from member_dashboard import show_member_page
    show_member_page()
else:
    from user_dashboard import show_user_page
    show_user_page()

if st.session_state['role']:
    if st.sidebar.button("Logout"):
        st.session_state['role'] = None
        st.rerun()