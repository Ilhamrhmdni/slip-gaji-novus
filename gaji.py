# gaji.py

import streamlit as st
from database import get_all_karyawan, get_gaji_by_id, save_or_update_gaji
from utils import format_rupiah

def halaman_gaji():
    st.title("Data Slip Gaji Karyawan")

    data_karyawan = get_all_karyawan()

    if not data_karyawan:
        st.info("Belum ada data karyawan.")
        return

    for id_karyawan, nama, jabatan, divisi in data_karyawan:
        with st.expander(f"{nama} ({divisi} - {jabatan})"):
            st.write(f"**ID:** {id_karyawan}")
            gaji = get_gaji_by_id(id_karyawan)

            with st.form(f"form_gaji_{id_karyawan}", clear_on_submit=False):
                gaji_pokok = st.number_input("Gaji Pokok", min_value=0, value=gaji[0] if gaji else 0)
                tunjangan_kinerja = st.number_input("Tunjangan Kinerja", min_value=0, value=gaji[1] if gaji else 0)
                tunjangan_makan = st.number_input("Tunjangan Makan", min_value=0, value=gaji[2] if gaji else 0)
                tunjangan_overtime = st.number_input("Tunjangan Lembur", min_value=0, value=gaji[3] if gaji else 0)
                tunjangan_jabatan = st.number_input("Tunjangan Jabatan", min_value=0, value=gaji[4] if gaji else 0)
                pph21 = st.number_input("PPH 21", min_value=0, value=gaji[5] if gaji else 0)
                bpjs_kesehatan = st.number_input("BPJS Kesehatan", min_value=0, value=gaji[6] if gaji else 0)
                bpjs_ketenagakerjaan = st.number_input("BPJS Ketenagakerjaan", min_value=0, value=gaji[7] if gaji else 0)
                tagihan_hutang1 = st.number_input("Tagihan Hutang 1", min_value=0, value=gaji[8] if gaji else 0)
                tagihan_hutang2 = st.number_input("Tagihan Hutang 2", min_value=0, value=gaji[9] if gaji else 0)

                submitted = st.form_submit_button("Simpan Slip Gaji")
                if submitted:
                    save_or_update_gaji(id_karyawan, {
                        "gaji_pokok": gaji_pokok,
                        "tunjangan_kinerja": tunjangan_kinerja,
                        "tunjangan_makan": tunjangan_makan,
                        "tunjangan_overtime": tunjangan_overtime,
                        "tunjangan_jabatan": tunjangan_jabatan,
                        "pph21": pph21,
                        "bpjs_kesehatan": bpjs_kesehatan,
                        "bpjs_ketenagakerjaan": bpjs_ketenagakerjaan,
                        "tagihan_hutang1": tagihan_hutang1,
                        "tagihan_hutang2": tagihan_hutang2,
                    })
                    st.success("Data gaji berhasil disimpan.")
