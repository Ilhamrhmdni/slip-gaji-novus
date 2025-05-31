import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from utils import format_rupiah, terbilang_rupiah
from error_handling import log_exception, show_user_error
from PIL import Image
import os
import re
import tempfile


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
        y_offset = height - 100

        # Header
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, y_offset, "SLIP GAJI KARYAWAN")
        y_offset -= 20
        c.setFont("Helvetica", 12)
        c.drawString(50, y_offset, f"Periode: {data['periode']}")
        y_offset -= 40

        # Logo
        logo_path = "novus_logo.png"
        logo_rgb_path = "novus_logo_rgb.png"
        convert_png_to_rgb(logo_path, logo_rgb_path)
        if os.path.exists(logo_rgb_path):
            c.drawImage(logo_rgb_path, 450, y_offset + 30, width=100, height=50)

        # Alamat Perusahaan
        c.setFont("Helvetica", 10)
        c.drawString(450, y_offset + 20, "NOVUS Stream Lab")
        c.drawString(450, y_offset + 5, "Jl. Wijaya Kusuma No. 1 Munggut")
        c.drawString(450, y_offset - 10, "Kec. Wungu, Kab. Malang")
        c.drawString(450, y_offset - 25, "Jawa Timur 63181")
        c.drawString(450, y_offset - 40, "Email: novustreamlab@gmail.com")

        y_offset -= 60

        # Data Pribadi & Data Bank
        col_width = 200
        row_height = 15

        # Data Pribadi
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y_offset, "Data Pribadi")
        y_offset -= 20
        c.setFont("Helvetica", 10)
        for key, value in data["data_pribadi"].items():
            c.drawString(50, y_offset, f"{key}: {value}")
            y_offset -= row_height
        y_offset -= 10

        # Data Bank
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y_offset, "Data Bank")
        y_offset -= 20
        c.setFont("Helvetica", 10)
        for key, value in data["data_bank"].items():
            c.drawString(50, y_offset, f"{key}: {value}")
            y_offset -= row_height
        y_offset -= 30

        # Tabel Penghasilan & Potongan
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_offset, "PENGHASILAN")
        c.drawString(300, y_offset, "POTONGAN")
        y_offset -= 20

        row_height = 15
        col_penghasilan_x = 50
        col_penghasilan_nilai_x = 200
        col_potongan_x = 300
        col_potongan_nilai_x = 450

        penghasilan = [
            ("Gaji Pokok", data["gaji_pokok"]),
            ("Tunjangan Kinerja", data["tunjangan_kinerja"]),
            ("Tunjangan Makan", data["tunjangan_makan"]),
            ("Tunjangan Overtime", data["tunjangan_overtime"]),
            ("Tunjangan Jabatan", data["tunjangan_jabatan"]),
            ("Total Penghasilan", data["total_penghasilan"]),
        ]
        potongan = [
            ("PPh 21", data["pph21"]),
            ("BPJS Kesehatan", data["bpjs_kesehatan"]),
            ("BPJS Ketenagakerjaan", data["bpjs_ketenagakerjaan"]),
            ("Tagihan Hutang", data["tagihan_hutang1"]),
            ("Tagihan Hutang", data["tagihan_hutang2"]),
            ("Total Potongan", data["total_potongan"]),
        ]

        for i in range(len(penghasilan)):
            c.setFont("Helvetica", 10)
            c.drawString(col_penghasilan_x, y_offset, str(penghasilan[i][0]))
            c.drawString(col_penghasilan_nilai_x, y_offset, format_rupiah(penghasilan[i][1]))

            c.drawString(col_potongan_x, y_offset, str(potongan[i][0]))
            c.drawString(col_potongan_nilai_x, y_offset, format_rupiah(potongan[i][1]))

            y_offset -= row_height

        # Pembayaran
        y_offset -= 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_offset, "Pembayaran:")
        c.drawString(200, y_offset, format_rupiah(data["pembayaran"]))
        y_offset -= 20
        c.setFont("Helvetica", 10)
        c.drawString(50, y_offset, f"Terbilang: {terbilang_rupiah(data['pembayaran'])}")

        # Tanda Tangan
        y_offset -= 60
        c.setFont("Helvetica", 10)
        c.drawString(400, y_offset, "Mengetahui,")

        signature_path = "signature.png"
        signature_rgb_path = "signature_rgb.png"
        convert_png_to_rgb(signature_path, signature_rgb_path)

        if os.path.exists(signature_rgb_path):
            c.drawImage(signature_rgb_path, 450, y_offset - 50, width=50, height=50)
        else:
            c.drawString(450, y_offset - 50, "[TTD tidak ditemukan]")

        y_offset -= 70
        c.drawString(400, y_offset, "Septian Kurnia Armando")
        c.drawString(400, y_offset - 15, "Direktur")

        c.save()

        # Hapus file sementara
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

    from database import get_all_karyawan, get_karyawan_by_id

    try:
        data_karyawan = get_all_karyawan()
        if not data_karyawan:
            st.info("Belum ada data karyawan.")
            return

        karyawan_dict = {row[1]: row[0] for row in data_karyawan}
        nama_karyawan = st.selectbox("Pilih Nama Karyawan", options=karyawan_dict.keys())
        data = get_karyawan_by_id(karyawan_dict[nama_karyawan])

        if data:
            _, nama, alamat, no_telp, divisi, jabatan, email, nama_bank, rekening, alamat_bank = data
            col1, col2 = st.columns(2)

            with col1:
                st.text_input("Nama", value=nama, key="g_nama")
                st.text_input("Alamat", value=alamat, key="g_alamat")
                st.text_input("No. Telp", value=no_telp, key="g_no_telp")
                st.text_input("Divisi", value=divisi, key="g_divisi")
                st.text_input("Jabatan", value=jabatan, key="g_jabatan")
                st.text_input("Email", value=email, key="g_email")

            with col2:
                st.text_input("Nama Bank", value=nama_bank, key="g_nama_bank")
                st.text_input("Rekening", value=rekening, key="g_rekening")
                st.text_area("Alamat Bank", value=alamat_bank, key="g_alamat_bank", height=150)
                periode = st.text_input("Periode", value="Januari 2025")

            st.header("Penghasilan")
            col_kiri, col_kanan = st.columns(2)

            with col_kiri:
                gaji_pokok = st.number_input("Gaji Pokok", min_value=0, value=2_000_000)
                tunjangan_kinerja = st.number_input("Tunjangan Kinerja", min_value=0)
                tunjangan_makan = st.number_input("Tunjangan Makan", min_value=0)
                tunjangan_overtime = st.number_input("Tunjangan Overtime", min_value=0)
                tunjangan_jabatan = st.number_input("Tunjangan Jabatan", min_value=0)

            with col_kanan:
                pph21 = st.number_input("PPh 21", min_value=0)
                bpjs_kesehatan = st.number_input("BPJS Kesehatan", min_value=0)
                bpjs_ketenagakerjaan = st.number_input("BPJS Ketenagakerjaan", min_value=0)
                tagihan_hutang1 = st.number_input("Tagihan Hutang 1", min_value=0)
                tagihan_hutang2 = st.number_input("Tagihan Hutang 2", min_value=0)

            total_penghasilan = gaji_pokok + tunjangan_kinerja + tunjangan_makan + tunjangan_overtime + tunjangan_jabatan
            total_potongan = pph21 + bpjs_kesehatan + bpjs_ketenagakerjaan + tagihan_hutang1 + tagihan_hutang2
            pembayaran = total_penghasilan - total_potongan

            if pembayaran < 0:
                st.warning("⚠️ Total potongan lebih besar dari penghasilan!")

            if st.button("Cetak Slip Gaji"):
                try:
                    data = {
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
                    pdf_filename = f"slip_gaji_{nama_sanitized}.pdf"

                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                        create_pdf_reportlab(data, tmpfile.name)
                        tmpfile.seek(0)
                        st.download_button("⬇️ Download PDF", tmpfile.read(), file_name=pdf_filename, mime="application/pdf")
                    os.remove(tmpfile.name)

                except Exception as e:
                    log_exception(e, "Gagal membuat dan mengunduh slip gaji")
                    show_user_error("Gagal membuat slip gaji. Silakan periksa kembali data Anda.")

    except Exception as e:
        log_exception(e, "Kesalahan halaman_gaji")
        show_user_error("Terjadi kesalahan saat memuat data. Silakan coba lagi.")
