import customtkinter as ctk


class LoginView(ctk.CTk):
    """Tampilan (View) jendela Login.

    Kelas ini hanya mengurus tampilan. Perintah tombol "Masuk" dipasang oleh
    AuthController (controller/auth_controller.py).
    """

    def __init__(self):
        super().__init__()
        self.title("Login - Sistem Perpustakaan")
        self.geometry("360x320")
        self.resizable(False, False)

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(self.frame, text="LOGIN SISTEM", font=("Arial", 18, "bold")).pack(pady=(20, 15))

        self.entry_username = ctk.CTkEntry(self.frame, placeholder_text="Username")
        self.entry_username.pack(pady=10, padx=20, fill="x")

        # Parameter show="*" menyembunyikan karakter password
        self.entry_password = ctk.CTkEntry(self.frame, placeholder_text="Password", show="*")
        self.entry_password.pack(pady=10, padx=20, fill="x")

        self.btn_login = ctk.CTkButton(self.frame, text="Masuk", fg_color="blue")
        self.btn_login.pack(pady=20, padx=20, fill="x")
