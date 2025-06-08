import streamlit as st
from auth import login
from gaji import generate_slip

def main():
    st.title("Aplikasi Slip Gaji")

    if login():
        st.success("Login berhasil!")

        nama = st.text_input("Nama Karyawan")
        jabatan = st.text_input("Jabatan")
        gaji_pokok = st.number_input("Gaji Pokok", min_value=0)
        tunjangan = st.number_input("Tunjangan", min_value=0)
        potongan = st.number_input("Potongan", min_value=0)

        if st.button("Generate Slip Gaji"):
            generate_slip(nama, jabatan, gaji_pokok, tunjangan, potongan)
    else:
        st.warning("Silakan login terlebih dahulu.")

if __name__ == "__main__":
    main()
