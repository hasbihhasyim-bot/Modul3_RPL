import tkinter.messagebox as messagebox

from model.user_model import UserModel
from views.login_view import LoginView
from controller.buku_controller import BukuController


class AuthController:
    """Mengatur alur autentikasi aplikasi.

    Alur: jendela Login -> (login berhasil) jendela utama Perpustakaan
    -> (tombol Logout) kembali ke jendela Login.
    """

    def __init__(self, model=None):
        self.model = model if model is not None else UserModel()
        self._buka_login()

    def _buka_login(self):
        """Buat jendela Login baru dan pasang perintah pada tombol Masuk."""
        self.user = None
        self.view = LoginView()
        self.view.btn_login.configure(command=self.proses_login)

    def proses_login(self):
        username = self.view.entry_username.get()
        password = self.view.entry_password.get()

        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan Password wajib diisi!")
            return

        user = self.model.autentikasi(username, password)

        if user:
            messagebox.showinfo("Login Berhasil", f"Selamat datang, {user['username']} ({user['role']})!")
            self.user = user
            # Tutup jendela Login. mainloop Login berakhir, lalu run() membuka jendela utama.
            self.view.destroy()
        else:
            messagebox.showerror("Login Gagal", "Username atau Password salah!")

    def run(self):
        while True:
            self.view.mainloop()  # tampilkan jendela Login

            if self.user is None:
                break  # jendela Login ditutup tanpa login -> aplikasi selesai

            # Buka jendela utama Perpustakaan dengan mengirimkan role pengguna
            app_utama = BukuController(user_role=self.user["role"])
            logout = app_utama.run()

            if not logout:
                break  # jendela utama ditutup (bukan lewat Logout) -> aplikasi selesai

            self._buka_login()  # Logout -> kembali ke jendela Login
