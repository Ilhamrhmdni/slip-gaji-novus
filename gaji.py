import streamlit as st
import sqlite3
from database import get_all_karyawan
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO


def tampilkan_form_gaji(karyawan_id, nama_karyawan):
    st.markdown(f"### Form Slip Gaji untuk {nama_karyawan}")

    gaji_pokok = st.number_input("Gaji Pokok", min_value=0, value=0, step=100000, key=f"gp_{karyawan_id}")
    tunjangan = st.number_input("Tunjangan", min_value=0, value=0, step=100000, key=f"tunj_{karyawan_id}")
    potongan = st.number_input("Potongan", min_value=0, value=0, step=100000, key=f"pot_{karyawan_id}")

    if st.button("💾 Simpan & Download PDF", key=f"simpan_{karyawan_id}"):
        total = gaji_pokok + tunjangan - potongan
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, 800, f"Slip Gaji - {nama_karyawan}")
        c.setFont("Helvetica", 12)
        c.drawString(100, 770, f"Gaji Pokok      : Rp{gaji_pokok:,}")
        c.drawString(100, 750, f"Tunjangan       : Rp{tunjangan:,}")
        c.drawString(100, 730, f"Potongan        : Rp{potongan:,}")
        c.drawString(100, 700, f"Total Diterima  : Rp{total:,}")
        c.line(100, 690, 300, 690)

        c.showPage()
        c.save()

        st.download_button(
            label="📄 Download Slip Gaji PDF",
            data=buffer.getvalue(),
            file_name=f"Slip_Gaji_{nama_karyawan.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )


def halaman_gaji():
    st.title("📋 Daftar Karyawan & Slip Gaji")
    
    data_karyawan = get_all_karyawan()

    if not data_karyawan:
        st.warning("Belum ada data karyawan.")
        return

    # Gunakan session_state untuk melacak karyawan yang dipilih
    if "selected_karyawan_id" not in st.session_state:
        st.session_state.selected_karyawan_id = None

    for id_karyawan, nama in data_karyawan:
        col1, col2 = st.columns([4, 1])
        col1.write(f"**{nama}**")
        if col2.button("📝 Isi Slip Gaji", key=f"btn_{id_karyawan}"):
            st.session_state.selected_karyawan_id = id_karyawan
            st.experimental_rerun()

        # Tampilkan form jika karyawan ini dipilih
        if st.session_state.selected_karyawan_id == id_karyawan:
            tampilkan_form_gaji(id_karyawan, nama)
            st.markdown("---")
