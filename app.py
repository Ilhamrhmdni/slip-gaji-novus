import streamlit as st
from gaji import generate_slip_gaji_pdf

st.set_page_config(page_title="Slip Gaji - Novus", layout="centered")
st.title("SLIP GAJI - NOVUS STREAM LAB")

with st.form("slip_form"):
    st.subheader("Data Karyawan")
    nama = st.text_input("Nama", "ILHAM RAHMAD DANI")
    alamat = st.text_input("Alamat", "Lampung")
    telp = st.text_input("No. Telp", "082179698342")
    divisi = st.text_input("Divisi", "Operator")
    jabatan = st.text_input("Jabatan", "Karyawan")

    st.subheader("Data Bank")
    bank = st.text_input("Bank", "BRI")
    rekening = st.text_input("No. Rekening", "013001114447503")

    st.subheader("Periode & Komponen Gaji")
    periode = st.text_input("Periode", "Januari 2025")
    gaji_pokok = st.number_input("Gaji Pokok", value=2000000)
    tunj_kin = st.number_input("Tunjangan Kinerja", value=0)
    tunj_makan = st.number_input("Tunjangan Makan", value=0)
    tunj_lembur = st.number_input("Tunjangan Overtime", value=0)
    tunj_jabatan = st.number_input("Tunjangan Jabatan", value=0)
    pph21 = st.number_input("PPh 21", value=0)
    bpjs_kes = st.number_input("BPJS Kesehatan", value=0)
    bpjs_kerja = st.number_input("BPJS Ketenagakerjaan", value=0)
    hutang1 = st.number_input("Tagihan Hutang 1", value=0)
    hutang2 = st.number_input("Tagihan Hutang 2", value=0)

    submitted = st.form_submit_button("Generate Slip Gaji")

if submitted:
    data = {
        'nama': nama,
        'alamat': alamat,
        'telp': telp,
        'divisi': divisi,
        'jabatan': jabatan,
        'bank': bank,
        'rekening': rekening,
        'periode': periode,
        'gaji_pokok': gaji_pokok,
        'tunj_kin': tunj_kin,
        'tunj_makan': tunj_makan,
        'tunj_lembur': tunj_lembur,
        'tunj_jabatan': tunj_jabatan,
        'pph21': pph21,
        'bpjs_kes': bpjs_kes,
        'bpjs_kerja': bpjs_kerja,
        'hutang1': hutang1,
        'hutang2': hutang2,
    }

    pdf = generate_slip_gaji_pdf(data)
    st.success("Slip gaji berhasil dibuat.")
    st.download_button("Download Slip Gaji", data=pdf, file_name=f"Slip Gaji {nama}.pdf", mime="application/pdf")
