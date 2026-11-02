from model.buku_model import BukuModel
from views.buku_view import BukuView

# Kolom tahun_terbit bertipe YEAR di MySQL, rentang yang valid: 1901 - 2155.
TAHUN_MIN = 1901
TAHUN_MAX = 2155

# Role yang boleh menambah, memperbarui, dan menghapus data buku.
ROLE_ADMIN = "admin"


def _teks(nilai):
    """Nilai NULL dari database ditampilkan sebagai teks kosong, bukan 'None'."""
    return "" if nilai is None else nilai


class BukuController:
    """Penghubung antara BukuView (tampilan) dan BukuModel (database).

    Controller memasang perintah pada tombol di View, membaca baris yang
    dipilih pengguna pada tabel, lalu meneruskan datanya ke BukuModel.

    `user_role` ("admin" atau "anggota") menentukan hak akses: selain admin,
    form dan tombol simpan/perbarui/hapus dikunci (hanya boleh melihat).
    """

    def __init__(self, model=None, view=None, user_role="anggota"):
        self.user_role = user_role
        self.logout_diminta = False

        self.model = model if model is not None else BukuModel()
        self.view = view if view is not None else BukuView()

        # Menampilkan informasi role pada judul jendela aplikasi
        self.view.title(f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}")

        self._ikat_event()
        self._terapkan_otorisasi()
        self.muat_buku()

    def run(self):
        """Tampilkan jendela aplikasi.

        Mengembalikan True jika jendela ditutup lewat tombol Logout, dan False
        jika ditutup dengan cara lain (misalnya tombol X pada jendela).
        """
        self.view.mainloop()
        return self.logout_diminta

    # ------------------------------------------------------------------
    # Mengikat form, tombol, dan tabel ke fungsi controller
    # ------------------------------------------------------------------
    def _ikat_event(self):
        self.view.btn_simpan.configure(command=self.simpan_buku)
        self.view.btn_perbarui.configure(command=self.perbarui_buku)
        self.view.btn_hapus.configure(command=self.hapus_buku)
        self.view.btn_bersihkan.configure(command=self.view.bersihkan_form)
        self.view.btn_logout.configure(command=self.logout)
        self.view.tabel.bind("<<TreeviewSelect>>", self.pilih_buku)

    # ------------------------------------------------------------------
    # Otorisasi (Role-Based Access Control)
    # ------------------------------------------------------------------
    def _terapkan_otorisasi(self):
        """OTORISASI: jika bukan admin, nonaktifkan form input dan semua tombol manipulasi data."""
        if self.user_role == ROLE_ADMIN:
            return

        self.view.btn_simpan.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
        self.view.btn_perbarui.configure(state="disabled")
        self.view.btn_hapus.configure(state="disabled")
        self.view.entry_judul.configure(state="disabled")
        self.view.entry_penulis.configure(state="disabled")
        self.view.entry_tahun.configure(state="disabled")

    def _izinkan_admin(self, aksi):
        """Proteksi ganda di level Controller: tolak aksi jika pengguna bukan admin."""
        if self.user_role != ROLE_ADMIN:
            self.view.tampilkan_error("Akses Ditolak", f"Anda tidak memiliki izin untuk {aksi} data!")
            return False
        return True

    # ------------------------------------------------------------------
    # Logout
    # ------------------------------------------------------------------
    def logout(self):
        """Tombol 'Logout': tutup jendela perpustakaan. AuthController lalu menampilkan LoginView lagi."""
        self.logout_diminta = True
        self.view.destroy()

    # ------------------------------------------------------------------
    # Tabel
    # ------------------------------------------------------------------
    def muat_buku(self):
        """Ambil semua buku dari model, lalu tampilkan pada tabel."""
        try:
            daftar_buku = self.model.get_all_buku()
        except Exception as error:
            self.view.tampilkan_error("Gagal memuat buku", str(error))
            return

        baris = [
            (
                buku["id_buku"],
                buku["judul"],
                buku["penulis"],
                _teks(buku["tahun_terbit"]),
            )
            for buku in daftar_buku
        ]
        self.view.tampilkan_tabel(baris)

    def pilih_buku(self, event=None):
        """Dipanggil saat pengguna mengklik baris tabel: isi form dengan data baris itu."""
        baris = self.view.ambil_baris_terpilih()
        if baris is None:
            return

        _, judul, penulis, tahun = baris
        self.view.isi_form(judul, penulis, tahun)

    # ------------------------------------------------------------------
    # Form
    # ------------------------------------------------------------------
    def _baca_form(self):
        """Baca dan validasi isi form. Kembalikan (judul, penulis, tahun_terbit) atau None."""
        judul, penulis, tahun = self.view.ambil_data_form()

        if not judul or not penulis or not tahun:
            self.view.tampilkan_peringatan("Data belum lengkap", "Judul, penulis, dan tahun wajib diisi.")
            return None

        try:
            tahun_terbit = int(tahun)
        except ValueError:
            self.view.tampilkan_peringatan("Tahun tidak valid", "Tahun terbit harus berupa angka.")
            return None

        if not TAHUN_MIN <= tahun_terbit <= TAHUN_MAX:
            self.view.tampilkan_peringatan(
                "Tahun tidak valid",
                f"Tahun terbit harus antara {TAHUN_MIN} dan {TAHUN_MAX}.",
            )
            return None

        return judul, penulis, tahun_terbit

    # ------------------------------------------------------------------
    # Tombol
    # ------------------------------------------------------------------
    def simpan_buku(self):
        """Tombol 'Simpan Data': tambah buku baru."""
        if not self._izinkan_admin("menambah"):
            return

        data_buku = self._baca_form()
        if data_buku is None:
            return

        try:
            berhasil = self.model.create_buku(*data_buku)
        except Exception as error:
            self.view.tampilkan_error("Gagal menyimpan buku", str(error))
            return

        if berhasil:
            self.view.tampilkan_info("Berhasil", "Data buku berhasil disimpan.")
            self.view.bersihkan_form()
            self.muat_buku()
        else:
            self.view.tampilkan_error("Gagal menyimpan buku", "Data buku tidak berhasil disimpan.")

    def perbarui_buku(self):
        """Tombol 'Perbarui Buku Terpilih': ubah buku pada baris yang dipilih."""
        if not self._izinkan_admin("memperbarui"):
            return

        baris = self.view.ambil_baris_terpilih()
        if baris is None:
            self.view.tampilkan_peringatan("Pilih buku", "Pilih buku dari tabel yang ingin diperbarui.")
            return

        id_buku = int(baris[0])  # id_buku dari baris tabel yang diklik pengguna

        data_buku = self._baca_form()
        if data_buku is None:
            return

        try:
            berhasil = self.model.update_buku(id_buku, *data_buku)
        except Exception as error:
            self.view.tampilkan_error("Gagal memperbarui buku", str(error))
            return

        if berhasil:
            self.view.tampilkan_info("Berhasil", "Data buku berhasil diperbarui.")
            self.view.bersihkan_form()
            self.muat_buku()
        else:
            self.view.tampilkan_error("Gagal memperbarui buku", "Data buku tidak berhasil diperbarui.")

    def hapus_buku(self):
        """Tombol 'Hapus Buku Terpilih': hapus buku pada baris yang dipilih."""
        if not self._izinkan_admin("menghapus"):
            return

        baris = self.view.ambil_baris_terpilih()
        if baris is None:
            self.view.tampilkan_peringatan("Pilih buku", "Pilih buku dari tabel yang ingin dihapus.")
            return

        id_buku = int(baris[0])  # id_buku dari baris tabel yang diklik pengguna
        judul = baris[1]

        if not self.view.konfirmasi(
            "Konfirmasi",
            f"Hapus buku '{judul}'?\nRiwayat peminjaman buku ini juga akan ikut terhapus.",
        ):
            return

        try:
            berhasil = self.model.delete_buku(id_buku)
        except Exception as error:
            self.view.tampilkan_error("Gagal menghapus buku", str(error))
            return

        if berhasil:
            self.view.tampilkan_info("Berhasil", "Data buku berhasil dihapus.")
            self.view.bersihkan_form()
            self.muat_buku()
        else:
            self.view.tampilkan_error("Gagal menghapus buku", "Data buku tidak berhasil dihapus.")


if __name__ == "__main__":
    # Jalan pintas khusus uji coba tanpa login. Aplikasi sebenarnya dijalankan lewat main.py.
    BukuController(user_role=ROLE_ADMIN).run()
