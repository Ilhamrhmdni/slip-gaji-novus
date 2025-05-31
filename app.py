import streamlit as st
import sqlite3
import pdfkit
import pandas as pd
from num2words import num2words

# --- Konfigurasi Database ---
DB_NAME = "karyawan.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Tabel Users
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')
    # Tabel Karyawan
    c.execute('''
        CREATE TABLE IF NOT EXISTS karyawan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            alamat TEXT,
            no_telp TEXT,
            divisi TEXT,
            jabatan TEXT,
            email TEXT,
            nama_bank TEXT,
            rekening TEXT,
            alamat_bank TEXT
        )
    ''')
    # Tambahkan user default jika belum ada
    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                  ("admin", "1234", "admin"))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

def get_all_karyawan():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT id, nama, jabatan, divisi FROM karyawan", conn)
    conn.close()
    return df

def save_to_db(data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO karyawan 
        (nama, alamat, no_telp, divisi, jabatan, email, nama_bank, rekening, alamat_bank)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data["nama"], data["alamat"], data["no_telp"], data["divisi"],
        data["jabatan"], data["email"], data["nama_bank"], data["rekening"],
        data["alamat_bank"]
    ))
    conn.commit()
    conn.close()

# --- Fungsi Halaman ---
def halaman_user():
    st.title("🔐 Login Admin")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.role = user[3]
            st.success("Login Berhasil!")
        else:
            st.error("Username atau Password salah")

def halaman_data_karyawan():
    st.title("👥 Data Karyawan")

    if not st.session_state.get("logged_in", False):
        st.warning("Silakan login terlebih dahulu.")
        return

    with st.expander("➕ Tambah Data Karyawan"):
        with st.form("form_data_karyawan"):
            nama = st.text_input("Nama")
            alamat = st.text_input("Alamat")
            no_telp = st.text_input("No. Telp")
            divisi = st.text_input("Divisi")
            jabatan = st.text_input("Jabatan")
            email = st.text_input("Email")
            nama_bank = st.text_input("Nama Bank")
            rekening = st.text_input("Rekening")
            alamat_bank = st.text_area("Alamat Bank")

            submitted = st.form_submit_button("Simpan ke Database")
            if submitted:
                data = {
                    "nama": nama,
                    "alamat": alamat,
                    "no_telp": no_telp,
                    "divisi": divisi,
                    "jabatan": jabatan,
                    "email": email,
                    "nama_bank": nama_bank,
                    "rekening": rekening,
                    "alamat_bank": alamat_bank
                }
                save_to_db(data)
                st.success("Data berhasil disimpan ke database!")

    # Tampilkan daftar karyawan
    st.markdown("### Daftar Karyawan")
    df = get_all_karyawan()
    st.dataframe(df)

def halaman_gaji():
    st.title("💰 Slip Gaji")

    if not st.session_state.get("logged_in", False):
        st.warning("Silakan login terlebih dahulu.")
        return

    # Ambil daftar karyawan dari database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, nama FROM karyawan")
    karyawan_list = c.fetchall()
    conn.close()

    if not karyawan_list:
        st.info("Belum ada data karyawan. Silakan isi data karyawan terlebih dahulu.")
        return

    karyawan_dict = {row[1]: row[0] for row in karyawan_list}
    nama_karyawan = st.selectbox("Pilih Nama Karyawan", options=karyawan_dict.keys())

    # Ambil data karyawan dari database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM karyawan WHERE nama=?", (nama_karyawan,))
    data = c.fetchone()
    conn.close()

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

        total_penghasilan = (
            gaji_pokok + tunjangan_kinerja + tunjangan_makan +
            tunjangan_overtime + tunjangan_jabatan
        )
        total_potongan = (
            pph21 + bpjs_kesehatan + bpjs_ketenagakerjaan +
            tagihan_hutang1 + tagihan_hutang2
        )
        pembayaran = total_penghasilan - total_potongan

        def format_rupiah(angka):
            return f"Rp {angka:,.0f}".replace(",", ".")

        if st.button("Cetak Slip Gaji"):
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
              <tr><td>Tunjangan Overtime</td><td>{format_rupiah(tunjangan_overtime)}</td><td>Tagihan Hutang</td><td>{format_rupiah(tagihan_hutang1)}</td></tr>
              <tr><td>Tunjangan Jabatan</td><td>{format_rupiah(tunjangan_jabatan)}</td><td>Tagihan Hutang</td><td>{format_rupiah(tagihan_hutang2)}</td></tr>
              <tr><td><strong>Total Penghasilan</strong></td><td><strong>{format_rupiah(total_penghasilan)}</strong></td><td><strong>Total Potongan</strong></td><td><strong>{format_rupiah(total_potongan)}</strong></td></tr>
              <tr><td colspan="2"></td><td><strong>Pembayaran</strong></td><td><strong>{format_rupiah(pembayaran)}</strong></td></tr>
            </table>

            <p><strong>Terbilang:</strong> {num2words(pembayaran, lang='id').capitalize()} rupiah</p>
            <br><p align='right'>Mengetahui, <br><br>Septian Kurnia Armando<br>Direktur</p>
            """

            try:
                # Paksa path wkhtmltopdf
                config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

                # Buat PDF
                pdf = pdfkit.from_string(html_content, False, configuration=config)

                # Tombol download
                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf,
                    file_name=f"slip_gaji_{nama}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Gagal membuat PDF: {e}")

# --- Main App Logic ---
def main():
    init_db()
    st.sidebar.title("MENU UTAMA")
    menu = st.sidebar.radio("Pilih Menu", ["USER", "Data Karyawan", "Gaji"])

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if menu == "USER":
        halaman_user()
    elif menu == "Data Karyawan":
        halaman_data_karyawan()
    elif menu == "Gaji":
        halaman_gaji()

if __name__ == "__main__":
    main()
