from config.database import Database

class BukuModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "buku"

    def get_all_buku(self):
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        return []

    def create_buku(self, judul, penulis, tahun_terbit):
        if self.conn:
            cursor = self.conn.cursor()
            query = f"INSERT INTO {self.table_name} (judul, penulis, tahun_terbit) VALUES (%s, %s, %s)"
            val = (judul, penulis, tahun_terbit)
            cursor.execute(query, val)
            self.conn.commit()
            cursor.close()
            return True
        return False

    def update_buku(self, id_buku, judul, penulis, tahun_terbit):
        query = "UPDATE buku SET judul = ?, penulis = ?, tahun_terbit = ? WHERE id_buku = ?"
        try:
            self.cursor.execute(query, (judul, penulis, tahun_terbit, id_buku))
            self.conn.commit()
            print(f"Data buku ID {id_buku} berhasil diperbarui.")
            return True
        except Exception as e:
            print(f"Gagal memperbarui buku: {e}")
            return False

    def delete_buku(self, id_buku):
        query = "DELETE FROM buku WHERE id_buku = ?"
        try:
            self.cursor.execute(query, (id_buku,))
            self.conn.commit()
            print(f"Data buku ID {id_buku} berhasil dihapus.")
            return True
        except Exception as e:
            print(f"Gagal menghapus buku: {e}")
            return False