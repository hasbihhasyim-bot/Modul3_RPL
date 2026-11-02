# test/test_auth.py
# Jalankan dari folder root proyek dengan:  pytest test/test_auth.py -v
import hashlib
import os
import sys
from unittest.mock import MagicMock, patch

# Agar `from model...` dan `from controller...` ditemukan walau test ada di folder test/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.user_model import UserModel
from controller.buku_controller import BukuController


# ----------------------------------------------------------------------
# Alat bantu
# ----------------------------------------------------------------------
def buat_user_model():
    """UserModel dengan koneksi & cursor palsu (tanpa server MySQL)."""
    cursor_palsu = MagicMock()
    koneksi_palsu = MagicMock()
    koneksi_palsu.cursor.return_value = cursor_palsu

    with patch("model.user_model.Database") as database_palsu:
        database_palsu.return_value.get_connection.return_value = koneksi_palsu
        model = UserModel()

    return model, koneksi_palsu, cursor_palsu


def buat_controller(role):
    """BukuController dengan model & view palsu (tanpa MySQL dan tanpa jendela GUI)."""
    model_palsu = MagicMock()
    model_palsu.get_all_buku.return_value = []
    view_palsu = MagicMock()
    controller = BukuController(model=model_palsu, view=view_palsu, user_role=role)
    return controller, model_palsu, view_palsu


def widget_yang_dikunci(view):
    """Nama widget yang pernah di-configure(state="disabled")."""
    nama_widget = ["btn_simpan", "btn_perbarui", "btn_hapus", "btn_bersihkan", "btn_logout",
                   "entry_judul", "entry_penulis", "entry_tahun"]
    dikunci = set()
    for nama in nama_widget:
        for panggilan in getattr(view, nama).configure.call_args_list:
            if panggilan.kwargs.get("state") == "disabled":
                dikunci.add(nama)
    return dikunci


# ----------------------------------------------------------------------
# Hashing & autentikasi (UserModel)
# ----------------------------------------------------------------------
def test_hash_password_sha256():
    hasil = UserModel.hash_password("admin123")

    assert hasil == hashlib.sha256(b"admin123").hexdigest()
    # Nilai yang sama dengan SHA2('admin123', 256) di MySQL
    assert hasil == "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9"
    assert len(hasil) == 64
    assert hasil != "admin123"
    assert UserModel.hash_password("user123") != hasil


def test_autentikasi_berhasil_mengembalikan_role():
    model, _, cursor = buat_user_model()
    cursor.fetchone.return_value = {"id_user": 1, "username": "petugas", "role": "admin"}

    user = model.autentikasi("petugas", "admin123")

    assert user == {"id_user": 1, "username": "petugas", "role": "admin"}
    query, params = cursor.execute.call_args.args
    assert "%s" in query                                    # parameterized query
    assert params == ("petugas", UserModel.hash_password("admin123"))
    assert "admin123" not in params                         # password tidak dikirim sebagai plain text
    cursor.close.assert_called_once()


def test_autentikasi_gagal_mengembalikan_none():
    model, _, cursor = buat_user_model()
    cursor.fetchone.return_value = None

    assert model.autentikasi("petugas", "salah") is None


def test_autentikasi_kebal_sql_injection():
    model, _, cursor = buat_user_model()
    cursor.fetchone.return_value = None
    serangan = "' OR '1'='1"

    model.autentikasi(serangan, serangan)

    query, params = cursor.execute.call_args.args
    assert serangan not in query        # input pengguna tidak disisipkan ke teks SQL
    assert params[0] == serangan        # melainkan dikirim sebagai parameter


# ----------------------------------------------------------------------
# TUGAS 1: register_user
# ----------------------------------------------------------------------
def test_register_user_hash_password_sebelum_disimpan():
    model, koneksi, cursor = buat_user_model()

    berhasil = model.register_user("budi", "rahasia123", "anggota")

    assert berhasil is True
    query, params = cursor.execute.call_args.args
    assert query.startswith("INSERT INTO users")
    assert params == ("budi", hashlib.sha256(b"rahasia123").hexdigest(), "anggota")
    assert "rahasia123" not in params
    koneksi.commit.assert_called_once()
    cursor.close.assert_called_once()


def test_register_user_role_tidak_valid_ditolak():
    model, koneksi, cursor = buat_user_model()

    assert model.register_user("budi", "rahasia123", "superadmin") is False
    cursor.execute.assert_not_called()
    koneksi.commit.assert_not_called()


def test_register_user_input_kosong_ditolak():
    model, _, cursor = buat_user_model()

    assert model.register_user("", "rahasia123", "anggota") is False
    assert model.register_user("budi", "", "anggota") is False
    cursor.execute.assert_not_called()


def test_register_user_username_sudah_dipakai():
    model, koneksi, cursor = buat_user_model()
    cursor.execute.side_effect = Exception("Duplicate entry 'budi' for key 'users.username'")

    assert model.register_user("budi", "rahasia123", "anggota") is False
    koneksi.commit.assert_not_called()
    cursor.close.assert_called_once()


# ----------------------------------------------------------------------
# Otorisasi role (BukuController)
# ----------------------------------------------------------------------
def test_anggota_form_dan_tombol_manipulasi_terkunci():
    _, _, view = buat_controller("anggota")

    # TUGAS 2: Simpan, Perbarui, dan Hapus terkunci. Form input juga terkunci.
    assert widget_yang_dikunci(view) == {
        "btn_simpan", "btn_perbarui", "btn_hapus",
        "entry_judul", "entry_penulis", "entry_tahun",
    }
    # Logout dan Bersihkan Form tidak boleh ikut terkunci
    assert "btn_logout" not in widget_yang_dikunci(view)


def test_admin_tidak_ada_yang_terkunci():
    _, _, view = buat_controller("admin")

    assert widget_yang_dikunci(view) == set()


def test_judul_jendela_menampilkan_role():
    _, _, view = buat_controller("anggota")

    view.title.assert_called_with("Sistem Manajemen Perpustakaan - Mode: ANGGOTA")


def test_anggota_ditolak_di_level_controller():
    controller, model, view = buat_controller("anggota")

    controller.simpan_buku()
    controller.perbarui_buku()
    controller.hapus_buku()

    model.create_buku.assert_not_called()
    model.update_buku.assert_not_called()
    model.delete_buku.assert_not_called()
    assert view.tampilkan_error.call_count == 3
    assert view.tampilkan_error.call_args.args[0] == "Akses Ditolak"


def test_admin_boleh_simpan_perbarui_hapus():
    controller, model, view = buat_controller("admin")
    view.ambil_data_form.return_value = ("Laut Bercerita", "Leila S. Chudori", "2017")
    view.ambil_baris_terpilih.return_value = (5, "Judul Lama", "Penulis Lama", 2000)
    view.konfirmasi.return_value = True
    model.create_buku.return_value = True
    model.update_buku.return_value = True
    model.delete_buku.return_value = True

    controller.simpan_buku()
    controller.perbarui_buku()
    controller.hapus_buku()

    model.create_buku.assert_called_once_with("Laut Bercerita", "Leila S. Chudori", 2017)
    model.update_buku.assert_called_once_with(5, "Laut Bercerita", "Leila S. Chudori", 2017)
    model.delete_buku.assert_called_once_with(5)


# ----------------------------------------------------------------------
# TUGAS 3: Logout
# ----------------------------------------------------------------------
def test_tombol_logout_terhubung_ke_controller():
    controller, _, view = buat_controller("admin")

    view.btn_logout.configure.assert_any_call(command=controller.logout)


def test_logout_menutup_jendela_dan_run_mengembalikan_true():
    controller, _, view = buat_controller("anggota")

    controller.logout()

    view.destroy.assert_called_once()
    assert controller.run() is True


def test_run_tanpa_logout_mengembalikan_false():
    controller, _, view = buat_controller("admin")

    assert controller.run() is False
    view.mainloop.assert_called_once()
