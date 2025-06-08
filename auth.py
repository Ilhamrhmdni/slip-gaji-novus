import streamlit as st

def login():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin":
            return True
        else:
            st.error("Username/password salah")
    return False
