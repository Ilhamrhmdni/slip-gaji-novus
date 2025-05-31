import streamlit as st

def halaman_data_karyawan():
    st.title("👥 Kelola Data Karyawan")

    if not st.session_state.get("logged_in", False):
        st.warning("Silakan login terlebih dahulu.")
        return

    # Bagian Tambah Data Karyawan
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
                # Validasi input
                if not all([nama, alamat, no_telp, divisi, jabatan]):
                    st.error("⚠️ Semua field wajib diisi!")
                else:
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
                    try:
                        save_karyawan(data)
                        st.success("✅ Data berhasil disimpan ke database!")
                    except Exception as e:
                        st.error(f"❌ Gagal menyimpan data: {str(e)}")

    # Bagian Tampilan Data Karyawan
    st.markdown("### 🗂️ Daftar Karyawan")
    from database import get_all_karyawan
    data = get_all_karyawan()
    if data:
        import pandas as pd
        df = pd.DataFrame(data, columns=["ID", "Nama", "Alamat", "No. Telp", "Divisi", "Jabatan", "Email", "Nama Bank", "Rekening", "Alamat Bank"])
        st.dataframe(df)
    else:
        st.info("📁 Belum ada data karyawan.")
