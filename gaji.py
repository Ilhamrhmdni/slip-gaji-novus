# gaji.py
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from utils import format_rupiah, terbilang_rupiah

def create_pdf_reportlab(data, nama_file):
    c = canvas.Canvas(nama_file, pagesize=letter)
    width, height = letter  # Ukuran halaman (612 x 792)

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "SLIP GAJI KARYAWAN")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 70, f"Periode: {data['periode']}")

    # Data Pribadi
    y_offset = height - 100
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_offset, "Data Pribadi")
    y_offset -= 20

    c.setFont("Helvetica", 12)
    for key, value in data["data_pribadi"].items():
        c.drawString(50, y_offset, f"{key}: {value}")
        y_offset -= 20

    # Data Bank
    y_offset -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_offset, "Data Bank")
    y_offset -= 20

    c.setFont("Helvetica", 12)
    for key, value in data["data_bank"].items():
        c.drawString(50, y_offset, f"{key}: {value}")
        y_offset -= 20

    # Tabel Penghasilan dan Potongan
    y_offset -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_offset, "Rincian Gaji")
    y_offset -= 20

    c.setFont("Helvetica", 12)
    headers = ["PENGHASILAN", "", "POTONGAN", ""]
    row_height = 15
    col_widths = [150, 100, 150, 100]

    # Gambar header tabel
    x_offset = 50
    for i, header in enumerate(headers):
        c.drawString(x_offset, y_offset, header)
        x_offset += col_widths[i]

    y_offset -= row_height
    x_offset = 50

    # Isi tabel
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
        ("Tagihan Hutang 1", data["tagihan_hutang1"]),
        ("Tagihan Hutang 2", data["tagihan_hutang2"]),
        ("Total Potongan", data["total_potongan"])
    ]

    for i in range(len(penghasilan)):
        c.drawString(x_offset, y_offset, str(penghasilan[i][0]))
        c.drawString(x_offset + col_widths[1], y_offset, format_rupiah(penghasilan[i][1]))
        c.drawString(x_offset + col_widths[2], y_offset, str(potongan[i][0]))
        c.drawString(x_offset + sum(col_widths[:3]), y_offset, format_rupiah(potongan[i][1]))
        y_offset -= row_height

    # Pembayaran
    y_offset -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_offset, "Pembayaran")
    c.setFont("Helvetica", 12)
    c.drawString(200, y_offset, format_rupiah(data["pembayaran"]))

    # Terbilang
    y_offset -= 20
    terbilang = terbilang_rupiah(data["pembayaran"])
    c.drawString(50, y_offset, f"Terbilang: {terbilang}")

    # Tanda tangan
    y_offset -= 40
    c.setFont("Helvetica", 12)
    c.drawString(400, y_offset, "Mengetahui,")
    y_offset -= 20
    c.drawString(400, y_offset, "Septian Kurnia Armando")
    y_offset -= 20
    c.drawString(400, y_offset, "Direktur")

    c.save()

def halaman_gaji():
    st.title("💰 Slip Gaji")

    if not st.session_state.get("logged_in", False):
        st.warning("Silakan login terlebih dahulu.")
        return

    from database import get_all_karyawan
    data_karyawan = get_all_karyawan()
    if not data_karyawan:
        st.info("Belum ada data karyawan.")
        return

    karyawan_dict = {row[1]: row[0] for row in data_karyawan}
    nama_karyawan = st.selectbox("Pilih Nama Karyawan", options=karyawan_dict.keys())

    from database import get_karyawan_by_id
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
        col_penghasilan_kiri, col_penghasilan_kanan = st.columns(2)

        with col_penghasilan_kiri:
            gaji_pokok = st.number_input("Gaji Pokok", min_value=0, value=2_000_000)
            tunjangan_kinerja = st.number_input("Tunjangan Kinerja", min_value=0)
            tunjangan_makan = st.number_input("Tunjangan Makan", min_value=0)
            tunjangan_overtime = st.number_input("Tunjangan Overtime", min_value=0)
            tunjangan_jabatan = st.number_input("Tunjangan Jabatan", min_value=0)

        with col_penghasilan_kanan:
            pph21 = st.number_input("PPh 21", min_value=0)
            bpjs_kesehatan = st.number_input("BPJS Kesehatan", min_value=0)
            bpjs_ketenagakerjaan = st.number_input("BPJS Ketenagakerjaan", min_value=0)
            tagihan_hutang1 = st.number_input("Tagihan Hutang 1", min_value=0)
            tagihan_hutang2 = st.number_input("Tagihan Hutang 2", min_value=0)

        total_penghasilan = gaji_pokok + tunjangan_kinerja + tunjangan_makan + tunjangan_overtime + tunjangan_jabatan
        total_potongan = pph21 + bpjs_kesehatan + bpjs_ketenagakerjaan + tagihan_hutang1 + tagihan_hutang2
        pembayaran = total_penghasilan - total_potongan

        if st.button("Cetak Slip Gaji"):
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
                    "Nama": nama_bank,
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

            pdf_filename = f"slip_gaji_{nama}.pdf"
            create_pdf_reportlab(data, pdf_filename)

            with open(pdf_filename, "rb") as f:
                st.download_button(
                    label="⬇️ Download PDF",
                    data=f.read(),
                    file_name=pdf_filename,
                    mime="application/pdf"
                )
