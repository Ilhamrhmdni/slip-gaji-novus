import streamlit as st
from reportlab.pdfgen import canvas
import os

def generate_slip(nama, jabatan, gaji_pokok, tunjangan, potongan):
    total = gaji_pokok + tunjangan - potongan
    filename = f"{nama}_slip_gaji.pdf"

    c = canvas.Canvas(filename)
    c.drawString(100, 800, "Slip Gaji")
    c.drawString(100, 780, f"Nama: {nama}")
    c.drawString(100, 760, f"Jabatan: {jabatan}")
    c.drawString(100, 740, f"Gaji Pokok: Rp{gaji_pokok}")
    c.drawString(100, 720, f"Tunjangan: Rp{tunjangan}")
    c.drawString(100, 700, f"Potongan: Rp{potongan}")
    c.drawString(100, 680, f"Total: Rp{total}")
    c.save()

    with open(filename, "rb") as f:
        st.download_button("Download Slip Gaji", f, file_name=filename)

    os.remove(filename)
