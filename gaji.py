# gaji.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io
from utils import to_rupiah, terbilang

def generate_slip_gaji_pdf(data):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(300, 800, "SLIP GAJI KARYAWAN")

    c.setFont("Helvetica", 11)
    y = 780
    c.drawString(50, y, f"Periode : {data['periode']}")
    y -= 20
    c.drawString(50, y, f"Nama : {data['nama']}")
    y -= 15
    c.drawString(50, y, f"Alamat : {data['alamat']}")
    y -= 15
    c.drawString(50, y, f"No. Telp : {data['telp']}")
    y -= 15
    c.drawString(50, y, f"Divisi : {data['divisi']}")
    y -= 15
    c.drawString(50, y, f"Jabatan : {data['jabatan']}")
    y -= 25
    c.drawString(50, y, "Data Bank")
    y -= 15
    c.drawString(50, y, f"Nama : {data['nama']}")
    y -= 15
    c.drawString(50, y, f"Bank : {data['bank']}")
    y -= 15
    c.drawString(50, y, f"Rekening : {data['rekening']}")
    y -= 30

    c.drawString(50, y, "PENGHASILAN")
    c.drawString(300, y, "POTONGAN")
    y -= 15
    c.drawString(50, y, f"Gaji pokok {to_rupiah(data['gaji_pokok'])}")
    c.drawString(300, y, f"PPh 21 {to_rupiah(data['pph21'])}")
    y -= 15
    c.drawString(50, y, f"Tunjangan kinerja {to_rupiah(data['tunj_kin'])}")
    c.drawString(300, y, f"BPJS Kesehatan {to_rupiah(data['bpjs_kes'])}")
    y -= 15
    c.drawString(50, y, f"Tunjangan makan {to_rupiah(data['tunj_makan'])}")
    c.drawString(300, y, f"BPJS Ketenagakerjaan {to_rupiah(data['bpjs_kerja'])}")
    y -= 15
    c.drawString(50, y, f"Tunjangan Overtime {to_rupiah(data['tunj_lembur'])}")
    c.drawString(300, y, f"Tagihan hutang {to_rupiah(data['hutang1'])}")
    y -= 15
    c.drawString(50, y, f"Tunjangan jabatan {to_rupiah(data['tunj_jabatan'])}")
    c.drawString(300, y, f"Tagihan hutang {to_rupiah(data['hutang2'])}")
    y -= 20

    total_penghasilan = sum([data['gaji_pokok'], data['tunj_kin'], data['tunj_makan'], data['tunj_lembur'], data['tunj_jabatan']])
    total_potongan = sum([data['pph21'], data['bpjs_kes'], data['bpjs_kerja'], data['hutang1'], data['hutang2']])
    total_pembayaran = total_penghasilan - total_potongan

    c.drawString(50, y, f"Total Penghasilan {to_rupiah(total_penghasilan)}")
    c.drawString(300, y, f"Total Potongan {to_rupiah(total_potongan)}")
    y -= 25
    c.drawString(50, y, f"Pembayaran {to_rupiah(total_pembayaran)}")
    y -= 15
    c.drawString(50, y, f"Terbilang : {terbilang(total_pembayaran).capitalize()} rupiah")

    y -= 40
    c.drawString(50, y, "Mengetahui,")
    y -= 15
    c.drawString(50, y, "Septian Kurnia Armando")
    y -= 15
    c.drawString(50, y, "Direktur")

    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
