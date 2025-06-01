# database.py
import sqlite3
import os
from firebase_config import storage, log_backup_event

DB_NAME = "/tmp/karyawan.db"

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
            rekening TEXT
        )
    ''')

    # Tabel Gaji
    c.execute('''
        CREATE TABLE IF NOT EXISTS gaji (
            karyawan_id INTEGER PRIMARY KEY,
            gaji_pokok INTEGER,
            tunjangan_kinerja INTEGER,
            tunjangan_makan INTEGER,
            tunjangan_overtime INTEGER,
            tunjangan_jabatan INTEGER,
            pph21 INTEGER,
            bpjs_kesehatan INTEGER,
            bpjs_ketenagakerjaan INTEGER,
            tagihan_hutang1 INTEGER,
            tagihan_hutang2 INTEGER,
            FOREIGN KEY(karyawan_id) REFERENCES karyawan(id)
        )
    ''')

    # User default
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
    c = conn.cursor()
    c.execute("SELECT id, nama, jabatan, divisi FROM karyawan")
    data = c.fetchall()
    conn.close()
    return data


def save_karyawan(data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO karyawan 
        (nama, alamat, no_telp, divisi, jabatan, email, nama_bank, rekening)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data["nama"], data["alamat"], data["no_telp"], data["divisi"],
        data["jabatan"], data["email"], data["nama_bank"], data["rekening"]
    ))
    conn.commit()
    conn.close()


def get_karyawan_by_id(karyawan_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM karyawan WHERE id=?", (karyawan_id,))
    data = c.fetchone()
    conn.close()
    return data


def get_gaji_by_id(karyawan_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT gaji_pokok, tunjangan_kinerja, tunjangan_makan, tunjangan_overtime,
               tunjangan_jabatan, pph21, bpjs_kesehatan, bpjs_ketenagakerjaan,
               tagihan_hutang1, tagihan_hutang2
        FROM gaji WHERE karyawan_id = ?
    ''', (karyawan_id,))
    data = c.fetchone()
    conn.close()
    return data


def save_or_update_gaji(karyawan_id, data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT 1 FROM gaji WHERE karyawan_id = ?", (karyawan_id,))
    exists = c.fetchone()

    if exists:
        c.execute('''
            UPDATE gaji SET 
                gaji_pokok = ?, tunjangan_kinerja = ?, tunjangan_makan = ?, tunjangan_overtime = ?,
                tunjangan_jabatan = ?, pph21 = ?, bpjs_kesehatan = ?, bpjs_ketenagakerjaan = ?,
                tagihan_hutang1 = ?, tagihan_hutang2 = ?
            WHERE karyawan_id = ?
        ''', (
            data["gaji_pokok"], data["tunjangan_kinerja"], data["tunjangan_makan"], data["tunjangan_overtime"],
            data["tunjangan_jabatan"], data["pph21"], data["bpjs_kesehatan"], data["bpjs_ketenagakerjaan"],
            data["tagihan_hutang1"], data["tagihan_hutang2"], karyawan_id
        ))
    else:
        c.execute('''
            INSERT INTO gaji (
                karyawan_id, gaji_pokok, tunjangan_kinerja, tunjangan_makan, tunjangan_overtime,
                tunjangan_jabatan, pph21, bpjs_kesehatan, bpjs_ketenagakerjaan,
                tagihan_hutang1, tagihan_hutang2
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            karyawan_id, data["gaji_pokok"], data["tunjangan_kinerja"], data["tunjangan_makan"],
            data["tunjangan_overtime"], data["tunjangan_jabatan"], data["pph21"], data["bpjs_kesehatan"],
            data["bpjs_ketenagakerjaan"], data["tagihan_hutang1"], data["tagihan_hutang2"]
        ))

    conn.commit()
    conn.close()


# === 🔥 Fitur Baru: Backup & Restore ke/dari Firebase ===

def backup_database_to_firebase():
    try:
        remote_path = "backups/karyawan.db"
        storage.child(remote_path).put(DB_NAME)
        url = storage.child(remote_path).get_url(None)

        log_backup_event("success", f"Backup berhasil. Link: {url}")
        return True, url
    except Exception as e:
        log_backup_event("failed", str(e))
        return False, str(e)


def restore_database_from_firebase():
    try:
        local_backup = "/tmp/karyawan_backup.db"
        remote_path = "backups/karyawan.db"

        storage.child(remote_path).download(local_backup)

        if os.path.exists(DB_NAME):
            os.remove(DB_NAME)

        os.rename(local_backup, DB_NAME)

        log_backup_event("restore_success", "Database berhasil dipulihkan.")
        return True, "Restore berhasil."
    except Exception as e:
        log_backup_event("restore_failed", str(e))
        return False, str(e)
