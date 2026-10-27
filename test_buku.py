# test_buku.py
# Jalankan dengan:  pytest test_buku.py -v
from unittest.mock import MagicMock, patch

from model.buku_model import BukuModel


def test_get_all_buku():
    """get_all_buku() harus mengembalikan semua baris tabel buku (list of dict)."""
    # Data yang seolah-olah dikembalikan oleh database
    data_buku = [
        {"id_buku": 1, "judul": "Rekayasa Perangkat Lunak Lanjutan", "penulis": "Roy Sommerville", "tahun_terbit": 2021},
        {"id_buku": 3, "judul": "Filosofi Teras", "penulis": "Henry Manampiring", "tahun_terbit": 2018},
    ]

    # Koneksi & cursor palsu, sehingga test tidak butuh server MySQL
    cursor_palsu = MagicMock()
    cursor_palsu.fetchall.return_value = data_buku
    koneksi_palsu = MagicMock()
    koneksi_palsu.cursor.return_value = cursor_palsu

    with patch("model.buku_model.Database") as database_palsu:
        database_palsu.return_value.get_connection.return_value = koneksi_palsu

        model = BukuModel()
        hasil = model.get_all_buku()

    # Hasil sama persis dengan data dari database
    assert hasil == data_buku
    # Query yang dijalankan benar dan cursor berbentuk dictionary
    koneksi_palsu.cursor.assert_called_once_with(dictionary=True)
    cursor_palsu.execute.assert_called_once_with("SELECT * FROM buku")
    # Cursor ditutup setelah dipakai
    cursor_palsu.close.assert_called_once()
