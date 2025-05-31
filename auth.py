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
            st.session_state.role = user[3]  # Simpan peran (role) user
            st.success("Login Berhasil!")
            st.rerun()  # Muat ulang agar form login hilang
        else:
            st.error("Username atau Password salah")

def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.info("Anda telah logout.")
    st.rerun()
