# auth.py
import streamlit as st

def halaman_login():
    st.title("🔐 Login Admin")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        from database import login_user
        user = login_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.role = user[3]
            st.success("Login Berhasil!")
        else:
            st.error("Username atau Password salah")
