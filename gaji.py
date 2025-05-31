# gaji.py
import streamlit as st
from utils import format_rupiah, terbilang_rupiah

def create_html_content(data):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Slip Gaji - {data['data_pribadi']['Nama']}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
            }}
            h3 {{
                text-align: center;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f4f4f4;
            }}
            .terbilang {{
                margin-top: 20px;
                font-style: italic;
            }}
            .tanda-tangan {{
                margin-top: 40px;
                text-align: right;
            }}
        </style>
    </head>
    <body>
        <h3>SLIP GAJI KARYAWAN</h3>
        <p style="text-align:center;">Periode: {data['periode']}</p>

        <h4>Data Pribadi</h4>
        <ul>
            <li><b>Nama:</b> {data['data_pribadi']['Nama']}</li>
            <li><b>Alamat:</b> {data['data_pribadi']['Alamat']}</li>
            <li><b>No. Telp:</b> {data['data_pribadi']['No. Telp']}</li>
            <li><b>Divisi:</b> {data['data_pribadi']['Divisi']}</li>
            <li><b>Jabatan:</b> {data['data_pribadi']['Jabatan']}</li>
        </ul>

        <h4>Data Bank</h4>
        <ul>
            <li><b>Nama:</b> {data['data_bank']['Nama']}</li>
            <li><b>Bank:</b> {data['data_bank']['Bank']}</li>
            <li><b>Rekening:</b> {data['data_bank']['Rekening']}</li>
            <li><b>Alamat:</b> {data['data_bank']['Alamat']}</li>
            <li><b>Email:</b> {data['data_bank']['Email']}</li>
        </ul>

        <h4>Rincian Gaji</h4>
        <table>
            <tr>
                <th>PENGHASILAN</th>
                <th></th>
                <th>POTONGAN</th>
                <th></th>
            </tr>
            <tr>
                <td>Gaji Pokok</td>
                <td>{format_rupiah(data['gaji_pokok'])}</td>
                <td>PPh 21</td>
                <td>{format_rupiah(data['pph21'])}</td>
            </tr>
            <tr>
                <td>Tunjangan Kinerja</td>
                <td>{format_rupiah(data['tunjangan_kinerja'])}</td>
                <td>BPJS Kesehatan</td>
                <td>{format_rupiah(data['bpjs_kesehatan'])}</td>
            </tr>
            <tr>
                <td>Tunjangan Makan</td>
                <td>{format_rupiah(data['tunjangan_makan'])}</td>
                <td>BPJS Ketenagakerjaan</td>
                <td>{format_rupiah(data['bpjs_ketenagakerjaan'])}</td>
            </tr>
            <tr>
                <td>Total Penghasilan</td>
                <td><strong>{format_rupiah(data['total_penghasilan'])}</strong></td>
                <td>Total Potongan</td>
                <td><strong>{format_rupiah(data['total_potongan'])}</strong></td>
            </tr>
            <tr>
                <td colspan="2"></td>
                <td><strong>Pembayaran</strong></td>
                <td><strong>{format_rupiah(data['pembayaran'])}</strong></td>
            </tr>
        </table>

        <p class="terbilang"><strong>Terbilang:</strong> {terbilang_rupiah(data['pembayaran'])}</p>

        <div class="tanda-tangan">
            Mengetahui,<br><br>
            Septian Kurnia Armando<br>
            Direktur
        </div>
    </body>
    </html>
    """
    return html_content

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

        if st.button("Cetak Slip Gaji (HTML)"):
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

            html_content = create_html_content(data)
            st.download_button(
                label="⬇️ Download HTML",
                data=html_content,
                file_name=f"slip_gaji_{nama}.html",
                mime="text/html"
            )
