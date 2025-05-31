# karyawan.py
import streamlit as st

def halaman_data_karyawan():
    st.title("👥 Input Data Karyawan")

    if not st.session_state.get("logged_in", False):
        st.warning("Silakan login terlebih dahulu.")
        return

    with st.expander("➕ Tambah Data Karyawan"):
        with st.form("form_data_karyawan"):
            nama = st.text_input("Nama")
            alamat = st.text_input("Alamat")
            no_telp = st.text_input("No. Telp")
            divisi = st.text_input("Divisi")
            jabatan = st.text_input("Jabatan")
            email = st.text_input("Email")
            nama_bank = st.text_input("Nama Bank")
            rekening = st.text_input("Rekening")
            alamat_bank = st.text_area("Alamat Bank")

            submitted = st.form_submit_button("Simpan ke Database")
            if submitted:
                from database import save_karyawan
                data = {
                    "nama": nama,
                    "alamat": alamat,
                    "no_telp": no_telp,
                    "divisi": divisi,
                    "jabatan": jabatan,
                    "email": email,
                    "nama_bank": nama_bank,
                    "rekening": rekening,
                    "alamat_bank": alamat_bank
                }
                save_karyawan(data)
                st.success("Data berhasil disimpan ke database!")

    st.markdown("### Daftar Karyawan")
    from database import get_all_karyawan
    data = get_all_karyawan()
    for row in data:
        st.write(f"{row[1]} - {row[2]}")
