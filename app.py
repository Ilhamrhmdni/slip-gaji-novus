import streamlit as st
from auth import halaman_login, logout
from gaji import halaman_gaji
from karyawan import halaman_kelola_data

# Cek apakah pengguna sudah login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Jika belum login, tampilkan halaman login
if not st.session_state.logged_in:
    from database import init_db  # Load db supaya bisa panggil init_db
    init_db()  # Inisialisasi database sebelum login
    halaman_login()
else:
    # Jika sudah login, tampilkan menu utama
    st.sidebar.title("Navigasi")
    pilihan = st.sidebar.selectbox("Pilih Halaman", ["Slip Gaji", "Kelola Data", "Logout"])

    if pilihan == "Slip Gaji":
        halaman_gaji()
    elif pilihan == "Kelola Data":
        halaman_kelola_data()
    elif pilihan == "Logout":
        logout()
    else:
        st.write("Fitur lainnya akan ditambahkan...")
