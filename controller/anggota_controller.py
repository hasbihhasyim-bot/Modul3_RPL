from model.anggota_model import AnggotaModel
from views.anggota_view import AnggotaView


def _teks(nilai):
    """Nilai NULL dari database ditampilkan sebagai teks kosong, bukan 'None'."""
    return "" if nilai is None else nilai


class AnggotaController:
    """Penghubung antara AnggotaView (tampilan) dan AnggotaModel (database).

    Controller memasang perintah pada tombol di View, membaca baris yang
    dipilih pengguna pada tabel, lalu meneruskan datanya ke AnggotaModel.
    """

    def __init__(self, model=None, view=None):
        self.model = model if model is not None else AnggotaModel()
        self.view = view if view is not None else AnggotaView()

        self._ikat_event()
        self.muat_anggota()

    def run(self):
        """Tampilkan jendela aplikasi."""
        self.view.mainloop()

    # ------------------------------------------------------------------
    # Mengikat form, tombol, dan tabel ke fungsi controller
    # ------------------------------------------------------------------
    def _ikat_event(self):
        self.view.btn_simpan.configure(command=self.simpan_anggota)
        self.view.btn_perbarui.configure(command=self.perbarui_anggota)
        self.view.btn_hapus.configure(command=self.hapus_anggota)
        self.view.btn_bersihkan.configure(command=self.view.bersihkan_form)
        self.view.tabel.bind("<<TreeviewSelect>>", self.pilih_anggota)

    # ------------------------------------------------------------------
    # Tabel
    # ------------------------------------------------------------------
    def muat_anggota(self):
        """Ambil semua anggota dari model, lalu tampilkan pada tabel."""
        try:
            daftar_anggota = self.model.get_all_anggota()
        except Exception as error:
            self.view.tampilkan_error("Gagal memuat anggota", str(error))
            return

        baris = [
            (
                anggota["id_anggota"],
                anggota["nama"],
                _teks(anggota["alamat"]),
            )
            for anggota in daftar_anggota
        ]
        self.view.tampilkan_tabel(baris)

    def pilih_anggota(self, event=None):
        """Dipanggil saat pengguna mengklik baris tabel: isi form dengan data baris itu."""
        baris = self.view.ambil_baris_terpilih()
        if baris is None:
            return

        _, nama, alamat = baris
        self.view.isi_form(nama, alamat)

    # ------------------------------------------------------------------
    # Form
    # ------------------------------------------------------------------
    def _baca_form(self):
        """Baca dan validasi isi form. Kembalikan (nama, alamat) atau None."""
        nama, alamat = self.view.ambil_data_form()

        if not nama or not alamat:
            self.view.tampilkan_peringatan("Data belum lengkap", "Nama dan alamat wajib diisi.")
            return None

        return nama, alamat

    # ------------------------------------------------------------------
    # Tombol
    # ------------------------------------------------------------------
    def simpan_anggota(self):
        """Tombol 'Simpan Data': tambah anggota baru."""
        data_anggota = self._baca_form()
        if data_anggota is None:
            return

        try:
            berhasil = self.model.create_anggota(*data_anggota)
        except Exception as error:
            self.view.tampilkan_error("Gagal menyimpan anggota", str(error))
            return

        if berhasil:
            self.view.tampilkan_info("Berhasil", "Data anggota berhasil disimpan.")
            self.view.bersihkan_form()
            self.muat_anggota()
        else:
            self.view.tampilkan_error("Gagal menyimpan anggota", "Data anggota tidak berhasil disimpan.")

    def perbarui_anggota(self):
        """Tombol 'Perbarui Anggota Terpilih': ubah anggota pada baris yang dipilih."""
        baris = self.view.ambil_baris_terpilih()
        if baris is None:
            self.view.tampilkan_peringatan("Pilih anggota", "Pilih anggota dari tabel yang ingin diperbarui.")
            return

        id_anggota = int(baris[0])  # id_anggota dari baris tabel yang diklik pengguna

        data_anggota = self._baca_form()
        if data_anggota is None:
            return

        try:
            berhasil = self.model.update_anggota(id_anggota, *data_anggota)
        except Exception as error:
            self.view.tampilkan_error("Gagal memperbarui anggota", str(error))
            return

        if berhasil:
            self.view.tampilkan_info("Berhasil", "Data anggota berhasil diperbarui.")
            self.view.bersihkan_form()
            self.muat_anggota()
        else:
            self.view.tampilkan_error("Gagal memperbarui anggota", "Data anggota tidak berhasil diperbarui.")

    def hapus_anggota(self):
        """Tombol 'Hapus Anggota Terpilih': hapus anggota pada baris yang dipilih."""
        baris = self.view.ambil_baris_terpilih()
        if baris is None:
            self.view.tampilkan_peringatan("Pilih anggota", "Pilih anggota dari tabel yang ingin dihapus.")
            return

        id_anggota = int(baris[0])  # id_anggota dari baris tabel yang diklik pengguna
        nama = baris[1]

        if not self.view.konfirmasi("Konfirmasi", f"Hapus anggota '{nama}'?"):
            return

        try:
            berhasil = self.model.delete_anggota(id_anggota)
        except Exception as error:
            self.view.tampilkan_error("Gagal menghapus anggota", str(error))
            return

        if berhasil:
            self.view.tampilkan_info("Berhasil", "Data anggota berhasil dihapus.")
            self.view.bersihkan_form()
            self.muat_anggota()
        else:
            self.view.tampilkan_error(
                "Gagal menghapus anggota",
                "Data anggota tidak berhasil dihapus.\n"
                "Anggota yang masih tercatat pada data peminjaman tidak dapat dihapus.",
            )


if __name__ == "__main__":
    AnggotaController().run()
