# gaji.py
import streamlit as st
import pdfkit
from utils import format_rupiah, terbilang_rupiah

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

        html_content = f"""
        <h3 style="text-align:center;">SLIP GAJI KARYAWAN</h3>
        <p style="text-align:center;">Periode: {periode}</p>

        <h4>Data Pribadi</h4>
        <ul>
          <li><b>Nama:</b> {nama}</li>
          <li><b>Alamat:</b> {alamat}</li>
          <li><b>No. Telp:</b> {no_telp}</li>
          <li><b>Divisi:</b> {divisi}</li>
          <li><b>Jabatan:</b> {jabatan}</li>
        </ul>

        <h4>Data Bank</h4>
        <ul>
          <li><b>Nama:</b> {nama_bank}</li>
          <li><b>Bank:</b> {nama_bank}</li>
          <li><b>Rekening:</b> {rekening}</li>
          <li><b>Alamat:</b> {alamat_bank}</li>
          <li><b>Email:</b> {email}</li>
        </ul>

        <h4>Rincian Gaji</h4>
        <table border="1" width="100%">
          <tr><th>PENGHASILAN</th><th></th><th>POTONGAN</th><th></th></tr>
          <tr><td>Gaji Pokok</td><td>{format_rupiah(gaji_pokok)}</td><td>PPh 21</td><td>{format_rupiah(pph21)}</td></tr>
          <tr><td>Tunjangan Kinerja</td><td>{format_rupiah(tunjangan_kinerja)}</td><td>BPJS Kesehatan</td><td>{format_rupiah(bpjs_kesehatan)}</td></tr>
          <tr><td>Tunjangan Makan</td><td>{format_rupiah(tunjangan_makan)}</td><td>BPJS Ketenagakerjaan</td><td>{format_rupiah(bpjs_ketenagakerjaan)}</td></tr>
          <tr><td>Total Penghasilan</td><td><strong>{format_rupiah(total_penghasilan)}</strong></td><td>Total Potongan</td><td><strong>{format_rupiah(total_potongan)}</strong></td></tr>
          <tr><td colspan="2"></td><td><strong>Pembayaran</strong></td><td><strong>{format_rupiah(pembayaran)}</strong></td></tr>
        </table>

        <p><strong>Terbilang:</strong> {terbilang_rupiah(pembayaran)}</p>
        <br><p align='right'>Mengetahui, <br><br>Septian Kurnia Armando<br>Direktur</p>
        """

        if st.button("Cetak Slip Gaji"):
            try:
                config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
                pdf = pdfkit.from_string(html_content, False, configuration=config)
                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf,
                    file_name=f"slip_gaji_{nama}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Gagal membuat PDF: {e}")
