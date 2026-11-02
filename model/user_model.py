import hashlib

from config.database import Database

# Nilai yang diizinkan pada kolom role (sama dengan ENUM di tabel users)
ROLE_VALID = ("admin", "anggota")


class UserModel:
    """Model pengguna: hashing kata sandi, autentikasi, dan pendaftaran akun."""

    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "users"

    @staticmethod
    def hash_password(password):
        # Mengubah plain text password menjadi hash SHA-256
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def autentikasi(self, username, password):
        """Verifikasi username + password. Kembalikan dict user (dengan role) atau None."""
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            password_hash = self.hash_password(password)

            # Parameterized Query untuk mencegah SQL Injection
            query = f"SELECT id_user, username, role FROM {self.table_name} WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password_hash))
            user = cursor.fetchone()
            cursor.close()
            return user
        return None

    def register_user(self, username, password, role="anggota"):
        """Daftarkan akun baru. Password otomatis di-hash SHA-256 sebelum disimpan ke tabel users.

        Mengembalikan True jika berhasil. Mengembalikan False jika username/password kosong,
        role tidak dikenal, username sudah dipakai, atau koneksi database tidak tersedia.
        """
        if not username or not password:
            print("Gagal mendaftarkan user: username dan password wajib diisi.")
            return False

        if role not in ROLE_VALID:
            print(f"Gagal mendaftarkan user: role '{role}' tidak dikenal (pilih: {', '.join(ROLE_VALID)}).")
            return False

        if self.conn:
            cursor = self.conn.cursor()
            password_hash = self.hash_password(password)
            query = f"INSERT INTO {self.table_name} (username, password, role) VALUES (%s, %s, %s)"
            try:
                cursor.execute(query, (username, password_hash, role))
                self.conn.commit()
                print(f"User '{username}' ({role}) berhasil didaftarkan.")
                return True
            except Exception as e:
                print(f"Gagal mendaftarkan user: {e}")
                return False
            finally:
                cursor.close()
        return False
