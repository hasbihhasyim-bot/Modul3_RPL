# model/anggota_model.py
from config.database import Database
class AnggotaModel:
    def __init__(self, db_name="perpustakaan.db"):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "anggota"

    def get_all_anggota(self):
            if self.conn:
                cursor = self.conn.cursor(dictionary=True)
                query = f"SELECT * FROM {self.table_name}"
                cursor.execute(query)
                result = cursor.fetchall()
                cursor.close()
                return result
            return []

    def create_anggota(self, nama, alamat):
        if self.conn:
            cursor = self.conn.cursor()
            query = f"INSERT INTO {self.table_name} (nama, alamat) VALUES (%s, %s)"
            try:
                cursor.execute(query, (nama, alamat))
                self.conn.commit()
                print(f"Anggota '{nama}' berhasil ditambahkan.")
                return True
            except Exception as e:
                print(f"Gagal menambahkan anggota: {e}")
                return False
            finally:
                cursor.close()
        return False

    def read_anggota(self):
        if self.conn:
            cursor = self.conn.cursor()
            query = f"SELECT id_anggota, nama, alamat FROM {self.table_name}"
            try:
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Gagal mengambil data anggota: {e}")
                return []
            finally:
                cursor.close()
        return []

    def update_anggota(self, id_anggota, nama, alamat):
        if self.conn:
            cursor = self.conn.cursor()
            query = f"UPDATE {self.table_name} SET nama = %s, alamat = %s WHERE id_anggota = %s"
            try:
                cursor.execute(query, (nama, alamat, id_anggota))
                self.conn.commit()
                print(f"Data anggota ID {id_anggota} berhasil diperbarui.")
                return True
            except Exception as e:
                print(f"Gagal memperbarui anggota: {e}")
                return False
            finally:
                cursor.close()
        return False

    def delete_anggota(self, id_anggota):
        if self.conn:
            cursor = self.conn.cursor()
            query = f"DELETE FROM {self.table_name} WHERE id_anggota = %s"
            try:
                cursor.execute(query, (id_anggota,))
                self.conn.commit()
                print(f"Data anggota ID {id_anggota} berhasil dihapus.")
                return True
            except Exception as e:
                print(f"Gagal menghapus anggota: {e}")
                return False
            finally:
                cursor.close()
        return False
