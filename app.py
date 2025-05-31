# app.py
import streamlit as st
from auth import halaman_login
from karyawan import halaman_data_karyawan
from gaji import halaman_gaji
from database import init_db

init_db()

st.sidebar.title("MENU UTAMA")
menu = st.sidebar.radio("Pilih Menu", ["USER", "Data Karyawan", "Gaji"])

if menu == "USER":
    halaman_login()
elif menu == "Data Karyawan":
    halaman_data_karyawan()
elif menu == "Gaji":
    halaman_gaji()
