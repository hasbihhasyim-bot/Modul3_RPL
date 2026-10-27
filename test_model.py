# test_model.py
import argparse

from model.buku_model import BukuModel
from model.anggota_model import AnggotaModel

def test_buku():
    print("--- TESTING BUKU MODEL ---")
    buku = BukuModel()
    
    # Test Update
    #buku.update_buku(1, "Rekayasa Perangkat Lunak Lanjutan", "Roy Sommerville", 2021)
    
    # Test Delete
    #buku.delete_buku(2)

    # Daftar buku terbaru
    print("\nDaftar Buku Terbaru:")
    buku_baru = buku.read_buku()
    for row in buku_baru:
        print(f"ID: {row[0]}, Judul: {row[1]}, Penulis: {row[2]}, Tahun: {row[3]}")

def test_anggota():
    print("\n--- TESTING ANGGOTA MODEL ---")
    anggota = AnggotaModel()
    
    # Test Create Anggota
    print("Menambahkan anggota baru...")
    #anggota.create_anggota("Andi Anggita", "Jl. Sentosa No. 40")
    #anggota.create_anggota("Lani Amalia", "Jl. Anggrek No. 10")

    # Test Read Anggota
    print("\nDaftar Anggota:")
    daftar = anggota.read_anggota()
    for row in daftar:
        print(f"ID: {row[0]}, Nama: {row[1]}, Alamat: {row[2]}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gui",
        nargs="?",
        const="buku",
        choices=["buku", "anggota"],
        help="Jalankan antarmuka grafis (buku atau anggota). Default: buku.",
    )
    args = parser.parse_args()

    if args.gui == "anggota":
        from controller.anggota_controller import AnggotaController

        AnggotaController().run()
    elif args.gui == "buku":
        from controller.buku_controller import BukuController

        BukuController().run()
    else:
        test_buku()
        test_anggota()