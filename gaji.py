import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from utils import format_rupiah, terbilang_rupiah
from error_handling import log_exception, show_user_error
from PIL import Image
import os
import re
from database import get_all_karyawan, get_karyawan_by_id, get_gaji_by_id
import zipfile

def convert_png_to_rgb(input_path, output_path, bg_color=(255, 255, 255)):
    try:
        img = Image.open(input_path)
        if img.mode in ('RGBA', 'LA'):
            background = Image.new("RGB", img.size, bg_color)
            background.paste(img, mask=img.split()[3])
            background.save(output_path, 'PNG')
        else:
            img.convert("RGB").save(output_path, 'PNG')
    except Exception as e:
        log_exception(e, f"Gagal konversi PNG {input_path}")

def create_pdf_reportlab(data, nama_file):
    try:
        c = canvas.Canvas(nama_file, pagesize=letter)
        width, height = letter
        y_offset = height - 180

        # Header
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, height - 50, "SLIP GAJI KARYAWAN")
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 70, f"Periode: {data['periode']}")

        # Logo
        logo_path = "novus_logo.png"
        logo_rgb_path = "novus_logo_rgb.png"
        convert_png_to_rgb(logo_path, logo_rgb_path)

        if os.path.exists(logo_rgb_path):
            c.drawImage(logo_rgb_path, 450, height - 60, width=100, height=50)
        else:
            c.drawString(450, height - 60, "[Logo tidak ditemukan]")

        # Alamat kantor
        c.setFont("Helvetica", 10)
        c.drawString(450, height - 100, "NOVUS Stream Lab")
        c.drawString(450, height - 115, "Jl. Wijaya Kusuma No. 1 Munggut Kec. Wungu")
        c.drawString(450, height - 130, "Kab. Malang Jawa Timur 63181")
        c.drawString(450, height - 145, "Email: novustreamlab@gmail.com")

        # Data Pribadi
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y_offset, "Data Pribadi")
        y_offset -= 20
        c.setFont("Helvetica", 10)
        for key, value in data["data_pribadi"].items():
            c.drawString(50, y_offset, f"{key}: {value}")
            y_offset -= 15

        # Data Bank
        y_offset -= 20
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y_offset, "Data Bank")
        y_offset -= 20
        c.setFont("Helvetica", 10)
        for key, value in data["data_bank"].items():
            c.drawString(50, y_offset, f"{key}: {value}")
            y_offset -= 15

        # Tabel penghasilan & potongan
        y_offset -= 30
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y_offset, "PENGHASILAN")
        c.drawString(300, y_offset, "POTONGAN")
        y_offset -= 20

        headers = ["Gaji Pokok", "Rp", "PPh 21", "Rp"]
        row_height = 15
        col_widths = [150, 50, 150, 50]

        x_offset = 50
        for i, header in enumerate(headers):
            c.drawString(x_offset, y_offset, header)
            x_offset += col_widths[i]

        y_offset -= row_height
        x_offset = 50

        penghasilan = [
            ("Gaji Pokok", data["gaji_pokok"]),
            ("Tunjangan Kinerja", data["tunjangan_kinerja"]),
            ("Tunjangan Makan", data["tunjangan_makan"]),
            ("Tunjangan Overtime", data["tunjangan_overtime"]),
            ("Tunjangan Jabatan", data["tunjangan_jabatan"]),
            ("Total Penghasilan", data["total_penghasilan"])
        ]

        potongan = [
            ("PPh 21", data["pph21"]),
            ("BPJS Kesehatan", data["bpjs_kesehatan"]),
            ("BPJS Ketenagakerjaan", data["bpjs_ketenagakerjaan"]),
            ("Tagihan Hutang", data["tagihan_hutang1"]),
            ("Tagihan Hutang", data["tagihan_hutang2"]),
            ("Total Potongan", data["total_potongan"])
        ]

        for i in range(len(penghasilan)):
            c.drawString(x_offset, y_offset, str(penghasilan[i][0]))
            c.drawString(x_offset + col_widths[1], y_offset, format_rupiah(penghasilan[i][1]))
            c.drawString(x_offset + sum(col_widths[:2]), y_offset, str(potongan[i][0]))
            c.drawString(x_offset + sum(col_widths[:3]), y_offset, format_rupiah(potongan[i][1]))
            y_offset -= row_height

        # Pembayaran
        y_offset -= 20
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y_offset, "Pembayaran")
        c.drawString(300, y_offset, format_rupiah(data["pembayaran"]))

        # Terbilang
        y_offset -= 20
        terbilang = terbilang_rupiah(data["pembayaran"])
        c.drawString(50, y_offset, f"Terbilang: {terbilang}")

        # Tanda tangan
        y_offset -= 40
        c.setFont("Helvetica", 10)
        c.drawString(400, y_offset, "Mengetahui,")

        signature_path = "signature.png"
        signature_rgb_path = "signature_rgb.png"
        convert_png_to_rgb(signature_path, signature_rgb_path)

        if os.path.exists(signature_rgb_path):
            c.drawImage(signature_rgb_path, 450, y_offset - 50, width=50, height=50)
        else:
            c.drawString(450, y_offset - 50, "[Ttd tidak ditemukan]")

        c.drawString(400, y_offset - 70, "Septian Kurnia Armando")
        c.drawString(400, y_offset - 85, "Direktur")

        c.save()

        # Bersihkan file konversi sementara
        for f in [logo_rgb_path, signature_rgb_path]:
            if os.path.exists(f):
                os.remove(f)

    except Exception as e:
        log_exception(e, "Gagal membuat PDF slip gaji")
        raise

def halaman_gaji():
    st.title("💰 Slip Gaji")

    if not st.session_state.get("logged_in", False):
        st.warning("Silakan login terlebih dahulu.")
        return

    st.subheader("Cetak Slip Gaji Massal")
    periode = st.text_input("Periode", value="Januari 2025")

    if st.button("📦 Cetak Semua Slip Gaji"):
        try:
            karyawan_list = get_all_karyawan()
            if not karyawan_list:
                st.info("Tidak ada data karyawan.")
                return

            with zipfile.ZipFile("slip_massal.zip", "w") as zipf:
                for id_karyawan, nama, jabatan, divisi in karyawan_list:
                    data_kar = get_karyawan_by_id(id_karyawan)
                    data_gaji = get_gaji_by_id(id_karyawan)

                    if not data_kar or not data_gaji:
                        continue  # Lewatkan jika ada data yang tidak lengkap

                    _, nama, alamat, no_telp, divisi, jabatan, email, nama_bank, rekening, alamat_bank = data_kar
                    (
                        gaji_pokok, tunjangan_kinerja, tunjangan_makan, tunjangan_overtime,
                        tunjangan_jabatan, pph21, bpjs_kesehatan, bpjs_ketenagakerjaan,
                        tagihan_hutang1, tagihan_hutang2
                    ) = data_gaji

                    total_penghasilan = gaji_pokok + tunjangan_kinerja + tunjangan_makan + tunjangan_overtime + tunjangan_jabatan
                    total_potongan = pph21 + bpjs_kesehatan + bpjs_ketenagakerjaan + tagihan_hutang1 + tagihan_hutang2
                    pembayaran = total_penghasilan - total_potongan

                    slip_data = {
                        "periode": periode,
                        "data_pribadi": {
                            "Nama": nama,
                            "Alamat": alamat,
                            "No. Telp": no_telp,
                            "Divisi": divisi,
                            "Jabatan": jabatan
                        },
                        "data_bank": {
                            "Nama": nama,
                            "Bank": nama_bank,
                            "Rekening": rekening,
                            "Alamat": alamat_bank,
                            "Email": email
                        },
                        "gaji_pokok": gaji_pokok,
                        "tunjangan_kinerja": tunjangan_kinerja,
                        "tunjangan_makan": tunjangan_makan,
                        "tunjangan_overtime": tunjangan_overtime,
                        "tunjangan_jabatan": tunjangan_jabatan,
                        "total_penghasilan": total_penghasilan,
                        "pph21": pph21,
                        "bpjs_kesehatan": bpjs_kesehatan,
                        "bpjs_ketenagakerjaan": bpjs_ketenagakerjaan,
                        "tagihan_hutang1": tagihan_hutang1,
                        "tagihan_hutang2": tagihan_hutang2,
                        "total_potongan": total_potongan,
                        "pembayaran": pembayaran
                    }

                    nama_sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', nama)
                    pdf_name = f"slip_gaji_{nama_sanitized}.pdf"
                    create_pdf_reportlab(slip_data, pdf_name)
                    zipf.write(pdf_name)
                    os.remove(pdf_name)

            with open("slip_massal.zip", "rb") as f:
                st.download_button("⬇️ Download Slip Massal (ZIP)", f.read(), "slip_massal.zip")

        except Exception as e:
            log_exception(e, "Gagal membuat slip massal")
            show_user_error("Terjadi kesalahan saat membuat slip massal.")

