# test_model.py
from model.buku_model import BukuModel
from model.anggota_model import AnggotaModel

def test_buku():
    print("--- TESTING BUKU MODEL ---")
    buku = BukuModel()
    
    # Asumsi ID 1 dan 2 sudah ada di database dari proses Create sebelumnya
    # Test Update
    buku.update_buku(1, "Rekayasa Perangkat Lunak Lanjut", "Ian Sommerville", 2021)
    
    # Test Delete
    buku.delete_buku(2)

def test_anggota():
    print("\n--- TESTING ANGGOTA MODEL ---")
    anggota = AnggotaModel()
    
    # Test Create Anggota
    print("Menambahkan anggota baru...")
    anggota.create_anggota("Budi Santoso", "Jl. Merdeka No. 45")
    anggota.create_anggota("Siti Aminah", "Jl. Mawar No. 12")
    
    # Test Read Anggota
    print("\nDaftar Anggota:")
    daftar = anggota.read_anggota()
    for row in daftar:
        print(f"ID: {row[0]}, Nama: {row[1]}, Alamat: {row[2]}")

if __name__ == "__main__":
    test_buku()
    test_anggota()