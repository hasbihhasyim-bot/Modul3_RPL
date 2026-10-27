import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk


class AnggotaView(ctk.CTk):
    """Tampilan (View) data anggota.

    Kelas ini hanya mengurus tampilan: form, tombol, dan tabel.
    Logika tombol (simpan, perbarui, hapus, bersihkan) dan pemanggilan
    AnggotaModel ada di controller/anggota_controller.py (AnggotaController).
    """

    def __init__(self):
        super().__init__()
        # Data asli tiap baris tabel: {id_baris_treeview: (id_anggota, nama, alamat)}
        self._data_baris = {}

        self.title("Sistem Manajemen Perpustakaan - Anggota")
        self.geometry("800x450")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Frame Kiri (Form)
        self.frame_kiri = ctk.CTkFrame(self)
        self.frame_kiri.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kiri, text="Form Data Anggota", font=("Arial", 16, "bold")).pack(pady=15)

        self.entry_nama = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan Nama Anggota")
        self.entry_nama.pack(pady=10, padx=15, fill="x")

        self.entry_alamat = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan Alamat Anggota")
        self.entry_alamat.pack(pady=10, padx=15, fill="x")

        # Tombol: perintahnya (command) dipasang oleh AnggotaController
        self.btn_simpan = ctk.CTkButton(
            self.frame_kiri,
            text="Simpan Data",
            fg_color="green",
        )
        self.btn_simpan.pack(pady=20, padx=15, fill="x")

        self.btn_perbarui = ctk.CTkButton(
            self.frame_kiri,
            text="Perbarui Anggota Terpilih",
        )
        self.btn_perbarui.pack(pady=5, padx=15, fill="x")

        self.btn_hapus = ctk.CTkButton(
            self.frame_kiri,
            text="Hapus Anggota Terpilih",
            fg_color="#b22222",
            hover_color="#8b0000",
        )
        self.btn_hapus.pack(pady=5, padx=15, fill="x")

        self.btn_bersihkan = ctk.CTkButton(
            self.frame_kiri,
            text="Bersihkan Form",
        )
        self.btn_bersihkan.pack(pady=5, padx=15, fill="x")

        # Frame Kanan (Tabel)
        self.frame_kanan = ctk.CTkFrame(self)
        self.frame_kanan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kanan, text="Daftar Anggota Perpustakaan", font=("Arial", 16, "bold")).pack(pady=15)

        kolom = ("id_anggota", "nama", "alamat")
        self.tabel = ttk.Treeview(self.frame_kanan, columns=kolom, show="headings", height=15)

        self.tabel.heading("id_anggota", text="ID")
        self.tabel.heading("nama", text="Nama Anggota")
        self.tabel.heading("alamat", text="Alamat")

        self.tabel.column("id_anggota", width=40, anchor="center")
        self.tabel.column("nama", width=150)
        self.tabel.column("alamat", width=200)

        self.tabel.pack(fill="both", expand=True, padx=15, pady=10)

    # ------------------------------------------------------------------
    # Form
    # ------------------------------------------------------------------
    def ambil_data_form(self):
        """Kembalikan isi form sebagai tuple (nama, alamat) berupa teks."""
        return (
            self.entry_nama.get().strip(),
            self.entry_alamat.get().strip(),
        )

    def isi_form(self, nama, alamat):
        """Isi form dengan data anggota (dipakai saat baris tabel dipilih)."""
        for entry, nilai in (
            (self.entry_nama, nama),
            (self.entry_alamat, alamat),
        ):
            entry.delete(0, "end")
            entry.insert(0, str(nilai))

    def bersihkan_form(self):
        """Kosongkan form dan batalkan pilihan baris pada tabel."""
        self.tabel.selection_remove(self.tabel.selection())
        self.entry_nama.delete(0, "end")
        self.entry_alamat.delete(0, "end")

    # ------------------------------------------------------------------
    # Tabel
    # ------------------------------------------------------------------
    def tampilkan_tabel(self, baris):
        """Ganti seluruh isi tabel dengan `baris` (list of tuple)."""
        for item in self.tabel.get_children():
            self.tabel.delete(item)

        self._data_baris = {}
        for data in baris:
            id_baris = self.tabel.insert("", "end", values=data)
            self._data_baris[id_baris] = tuple(data)

    def ambil_baris_terpilih(self):
        """Kembalikan baris yang sedang dipilih sebagai tuple
        (id_anggota, nama, alamat), atau None jika belum ada yang dipilih."""
        pilihan = self.tabel.selection()
        if not pilihan:
            return None
        return self._data_baris.get(pilihan[0])

    # ------------------------------------------------------------------
    # Dialog pesan
    # ------------------------------------------------------------------
    def tampilkan_info(self, judul, pesan):
        messagebox.showinfo(judul, pesan)

    def tampilkan_peringatan(self, judul, pesan):
        messagebox.showwarning(judul, pesan)

    def tampilkan_error(self, judul, pesan):
        messagebox.showerror(judul, pesan)

    def konfirmasi(self, judul, pesan):
        return messagebox.askyesno(judul, pesan)
