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
        if self.conn:
            cursor = self.conn.cursor()
            # Gunakan %s dan self.table_name agar konsisten
            query = f"UPDATE {self.table_name} SET judul = %s, penulis = %s, tahun_terbit = %s WHERE id_buku = %s"
            try:
                cursor.execute(query, (judul, penulis, tahun_terbit, id_buku))
                self.conn.commit()
                print(f"Data buku ID {id_buku} berhasil diperbarui.")
                return True
            except Exception as e:
                print(f"Gagal memperbarui buku: {e}")
                return False
            finally:
                cursor.close()
        return False

    def delete_buku(self, id_buku):
        if self.conn:
            cursor = self.conn.cursor()
            # Gunakan %s dan self.table_name agar konsisten
            query = f"DELETE FROM {self.table_name} WHERE id_buku = %s"
            try:
                cursor.execute(query, (id_buku,))
                self.conn.commit()
                print(f"Data buku ID {id_buku} berhasil dihapus.")
                return True
            except Exception as e:
                print(f"Gagal menghapus buku: {e}")
                return False
            finally:
                cursor.close()
        return False