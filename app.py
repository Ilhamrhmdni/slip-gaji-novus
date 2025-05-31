import streamlit as st
from auth import halaman_login, logout
from gaji import halaman_gaji
from karyawan import halaman_kelola_data  # Baru: Kelola Data Karyawan

# Cek apakah pengguna sudah login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Jika belum login, tampilkan halaman login
if not st.session_state.logged_in:
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
