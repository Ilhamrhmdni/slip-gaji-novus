# database.py
import sqlite3

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
        (nama, alamat, no_telp, divisi, jabatan, email, nama_bank, rekening, alamat_bank)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data["nama"], data["alamat"], data["no_telp"], data["divisi"],
        data["jabatan"], data["email"], data["nama_bank"], data["rekening"], data["alamat_bank"]
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
