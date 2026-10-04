# model/anggota_model.py
import sqlite3

class AnggotaModel:
    def __init__(self, db_name="perpustakaan.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        # Membuat tabel jika belum ada
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS anggota (
                id_anggota INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                alamat TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def create_anggota(self, nama, alamat):
        query = "INSERT INTO anggota (nama, alamat) VALUES (?, ?)"
        try:
            self.cursor.execute(query, (nama, alamat))
            self.conn.commit()
            print(f"Anggota '{nama}' berhasil ditambahkan.")
            return True
        except Exception as e:
            print(f"Gagal menambahkan anggota: {e}")
            return False

    def read_anggota(self):
        query = "SELECT id_anggota, nama, alamat FROM anggota"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Gagal mengambil data anggota: {e}")
            return []