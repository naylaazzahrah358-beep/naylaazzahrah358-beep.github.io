"""
=============================================================================
Nama Project : mencraft.id
Deskripsi    : Aplikasi sederhana untuk mempermudah pemesanan bucket.
               Dibuat menggunakan Python sebagai proyek belajar membuat aplikasi.
Fitur Utama  :
  1. Pilih Bucket  - Memilih jenis bucket yang tersedia beserta harga.
  2. Tambah Pesanan - Menambahkan bucket ke daftar pesanan & jumlahnya.
  3. Kelola Pesanan - Mengubah atau menghapus pesanan dalam daftar.
  4. Checkout      - Menyelesaikan transaksi & simpan ke file JSON.
=============================================================================
"""

import json
import os
from datetime import datetime

# Database Daftar Produk Bucket yang Tersedia
KATALOG_BUCKET = {
    1: {"nama": "Bucket Bunga Mawar (Fresh/Artificial)", "harga": 75000, "kategori": "Bunga"},
    2: {"nama": "Bucket Snack & Cokelat Premium", "harga": 50000, "kategori": "Snack"},
    3: {"nama": "Bucket Uang Tarik Eksklusif (10 Lembar)", "harga": 120000, "kategori": "Uang"},
    4: {"nama": "Bucket Boneka Wisuda + Selempang Nama", "harga": 85000, "kategori": "Wisuda"},
    5: {"nama": "Bucket Hijab Segi Empat + Bros Cantik", "harga": 65000, "kategori": "Hijab"},
    6: {"nama": "Bucket Custom Special Request", "harga": 100000, "kategori": "Custom"}
}

FILE_DATABASE = "riwayat_pesanan.json"


def bersihkan_layar():
    """Membersihkan tampilan terminal/console"""
    os.system('cls' if os.name == 'nt' else 'clear')


def garis_pembatas(simbol="=", panjang=60):
    print(simbol * panjang)


def format_rupiah(angka):
    """Format angka integer menjadi format mata uang Rupiah (IDR)"""
    return f"Rp {angka:,.0f}".replace(",", ".")


def tampilkan_header():
    garis_pembatas("=")
    print("                 M E N C R A F T . I D                 ")
    print("           'The Perfect Gift at any Time'             ")
    print("      Aplikasi Pemesanan Bucket Praktis & Cepat       ")
    garis_pembatas("=")


def fitur_1_pilih_bucket():
    """Fitur 1: Memilih jenis bucket yang tersedia beserta harga melalui menu pilihan."""
    bersihkan_layar()
    tampilkan_header()
    print("\n📦 [FITUR 1: KATALOG & DAFTAR PILIHAN BUCKET]\n")
    print(f"{'No':<4} | {'Jenis Bucket':<40} | {'Harga':<12}")
    garis_pembatas("-")
    for nomor, item in KATALOG_BUCKET.items():
        print(f"{nomor:<4} | {item['nama']:<40} | {format_rupiah(item['harga']):<12}")
    garis_pembatas("-")
    input("\nTekan [Enter] untuk kembali ke menu utama...")


def fitur_2_tambah_pesanan(daftar_pesanan):
    """Fitur 2: Menambahkan bucket ke daftar pesanan dan menentukan jumlah yang ingin dipesan."""
    while True:
        bersihkan_layar()
        tampilkan_header()
        print("\n🛒 [FITUR 2: TAMBAH PESANAN BUCKET]\n")
        print(f"{'No':<4} | {'Jenis Bucket':<40} | {'Harga':<12}")
        garis_pembatas("-")
        for nomor, item in KATALOG_BUCKET.items():
            print(f"{nomor:<4} | {item['nama']:<40} | {format_rupiah(item['harga']):<12}")
        garis_pembatas("-")

        try:
            pilihan = int(input("\nPilih nomor bucket yang ingin dipesan (1-6) [0 untuk Batal]: "))
            if pilihan == 0:
                print("Kembali ke menu utama.")
                break
            
            if pilihan not in KATALOG_BUCKET:
                print("⚠️ Nomor bucket tidak valid! Silakan pilih sesuai daftar.")
                input("Tekan [Enter] untuk coba lagi...")
                continue

            jumlah = int(input(f"Masukkan jumlah bucket '{KATALOG_BUCKET[pilihan]['nama']}' : "))
            if jumlah <= 0:
                print("⚠️ Jumlah pesanan minimal 1!")
                input("Tekan [Enter] untuk coba lagi...")
                continue

            catatan = input("Catatan tambahan (warna wrapping / kartu ucapan) [Opsional]: ").strip()
            if not catatan:
                catatan = "Standar"

            bucket_terpilih = KATALOG_BUCKET[pilihan]
            subtotal = bucket_terpilih["harga"] * jumlah

            item_ditemukan = False
            for pesanan in daftar_pesanan:
                if pesanan["id_bucket"] == pilihan and pesanan["catatan"] == catatan:
                    pesanan["jumlah"] += jumlah
                    pesanan["subtotal"] += subtotal
                    item_ditemukan = True
                    break

            if not item_ditemukan:
                daftar_pesanan.append({
                    "id_bucket": pilihan,
                    "nama_bucket": bucket_terpilih["nama"],
                    "harga_satuan": bucket_terpilih["harga"],
                    "jumlah": jumlah,
                    "catatan": catatan,
                    "subtotal": subtotal
                })

            print(f"\n✅ Berhasil menambahkan {jumlah}x '{bucket_terpilih['nama']}' ke keranjang!")
            
            lagi = input("\nTambah pesanan lainnya? (y/t): ").strip().lower()
            if lagi != 'y':
                break

        except ValueError:
            print("⚠️ Input harus berupa angka valid!")
            input("Tekan [Enter] untuk coba lagi...")


def fitur_3_kelola_pesanan(daftar_pesanan):
    """Fitur 3: Mengubah atau menghapus pesanan yang sudah dimasukkan ke dalam daftar."""
    while True:
        bersihkan_layar()
        tampilkan_header()
        print("\n📋 [FITUR 3: KELOLA DAFTAR PESANAN KERANJANG]\n")

        if not daftar_pesanan:
            print("ℹ️ Keranjang pesanan Anda masih kosong!")
            input("\nTekan [Enter] untuk kembali ke menu utama...")
            return

        total_harga = 0
        print(f"{'No':<3} | {'Item Bucket':<32} | {'Qty':<4} | {'Harga Satuan':<12} | {'Subtotal':<12}")
        garis_pembatas("-")
        for i, item in enumerate(daftar_pesanan, start=1):
            total_harga += item["subtotal"]
            print(f"{i:<3} | {item['nama_bucket'][:32]:<32} | {item['jumlah']:<4} | {format_rupiah(item['harga_satuan']):<12} | {format_rupiah(item['subtotal']):<12}")
            if item["catatan"] != "Standar":
                print(f"    └─ Catatan: {item['catatan']}")
        garis_pembatas("-")
        print(f"TOTAL SEMENTARA : {format_rupiah(total_harga)}")
        garis_pembatas("=")

        print("\nOpsi Pengelolaan:")
        print("[1] Ubah Jumlah Pesanan")
        print("[2] Hapus Salah Satu Item")
        print("[3] Kosongkan Seluruh Keranjang")
        print("[0] Selesai / Kembali ke Menu Utama")

        pilihan = input("\nPilih aksi (0-3): ").strip()

        if pilihan == '0':
            break

        elif pilihan == '1':
            try:
                nomor_item = int(input("\nMasukkan nomor urut item yang ingin diubah jumlahnya: "))
                if 1 <= nomor_item <= len(daftar_pesanan):
                    item = daftar_pesanan[nomor_item - 1]
                    jumlah_baru = int(input(f"Masukkan jumlah baru untuk '{item['nama_bucket']}' (saat ini: {item['jumlah']}): "))
                    if jumlah_baru > 0:
                        item["jumlah"] = jumlah_baru
                        item["subtotal"] = item["harga_satuan"] * jumlah_baru
                        print("✅ Jumlah pesanan berhasil diperbarui!")
                    elif jumlah_baru == 0:
                        del daftar_pesanan[nomor_item - 1]
                        print("✅ Item dihapus karena jumlah diubah menjadi 0.")
                    else:
                        print("⚠️ Jumlah tidak valid.")
                else:
                    print("⚠️ Nomor urut tidak ditemukan!")
            except ValueError:
                print("⚠️ Masukkan angka yang valid.")
            input("Tekan [Enter] untuk melanjutkan...")

        elif pilihan == '2':
            try:
                nomor_item = int(input("\nMasukkan nomor urut item yang ingin dihapus: "))
                if 1 <= nomor_item <= len(daftar_pesanan):
                    item_terhapus = daftar_pesanan.pop(nomor_item - 1)
                    print(f"✅ Item '{item_terhapus['nama_bucket']}' berhasil dihapus dari keranjang.")
                else:
                    print("⚠️ Nomor urut tidak ditemukan!")
            except ValueError:
                print("⚠️ Masukkan angka yang valid.")
            input("Tekan [Enter] untuk melanjutkan...")

        elif pilihan == '3':
            konfirmasi = input("\nApakah Anda yakin ingin mengosongkan seluruh keranjang? (y/t): ").strip().lower()
            if konfirmasi == 'y':
                daftar_pesanan.clear()
                print("✅ Keranjang berhasil dikosongkan.")
                input("Tekan [Enter] untuk kembali...")
                break
        else:
            print("⚠️ Pilihan tidak valid!")
            input("Tekan [Enter] untuk coba lagi...")


def fitur_4_checkout(daftar_pesanan):
    """Fitur 4: Menyelesaikan transaksi dan menyimpan riwayat pesanan ke dalam file JSON."""
    bersihkan_layar()
    tampilkan_header()
    print("\n💳 [FITUR 4: CHECKOUT & STRUK TRANSAKSI]\n")

    if not daftar_pesanan:
        print("⚠️ Keranjang Anda masih kosong! Tambahkan pesanan terlebih dahulu.")
        input("\nTekan [Enter] untuk kembali ke menu utama...")
        return

    print("Silakan lengkapi data pemesan:")
    nama_pemesan = input("Nama Lengkap Pemesan    : ").strip()
    while not nama_pemesan:
        nama_pemesan = input("Nama tidak boleh kosong! Masukkan nama: ").strip()

    nomor_hp = input("Nomor Telepon / WhatsApp: ").strip()
    alamat = input("Alamat / Opsi Antar     : ").strip()
    if not alamat:
        alamat = "Ambil di Toko (Self Pick-up)"

    total_pembayaran = sum(item["subtotal"] for item in daftar_pesanan)
    waktu_transaksi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    id_transaksi = f"MC-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Tampilkan Struk Pembayaran
    bersihkan_layar()
    tampilkan_header()
    print(f"\n🧾 STRUK PEMESANAN RESMI: {id_transaksi}")
    print(f"Waktu Transaksi : {waktu_transaksi}")
    print(f"Nama Pemesan    : {nama_pemesan}")
    print(f"Kontak WhatsApp : {nomor_hp}")
    print(f"Alamat / Opsi   : {alamat}")
    garis_pembatas("-")
    print(f"{'No':<3} | {'Item Bucket':<30} | {'Qty':<4} | {'Subtotal':<12}")
    garis_pembatas("-")
    for i, item in enumerate(daftar_pesanan, start=1):
        print(f"{i:<3} | {item['nama_bucket'][:30]:<30} | {item['jumlah']:<4} | {format_rupiah(item['subtotal']):<12}")
    garis_pembatas("-")
    print(f"TOTAL TAGIHAN   : {format_rupiah(total_pembayaran)}")
    garis_pembatas("=")

    konfirmasi = input("\nKonfirmasi dan selesaikan pesanan? (y/t): ").strip().lower()
    if konfirmasi != 'y':
        print("Transaksi dibatalkan. Pesanan tetap berada di keranjang.")
        input("Tekan [Enter] untuk kembali...")
        return

    data_transaksi = {
        "id_transaksi": id_transaksi,
        "waktu": waktu_transaksi,
        "pemesan": {
            "nama": nama_pemesan,
            "telepon": nomor_hp,
            "alamat": alamat
        },
        "item_pesanan": list(daftar_pesanan),
        "total_pembayaran": total_pembayaran,
        "status": "Selesai / Lunas"
    }

    riwayat = []
    if os.path.exists(FILE_DATABASE):
        try:
            with open(FILE_DATABASE, "r", encoding="utf-8") as file:
                riwayat = json.load(file)
        except Exception:
            riwayat = []

    riwayat.append(data_transaksi)

    try:
        with open(FILE_DATABASE, "w", encoding="utf-8") as file:
            json.dump(riwayat, file, indent=4, ensure_ascii=False)
        print(f"\n🎉 Terima kasih, {nama_pemesan}! Pesanan Anda berhasil dicatat.")
        print(f"📁 Riwayat transaksi telah tersimpan ke dalam file: '{FILE_DATABASE}'")
        daftar_pesanan.clear()
    except Exception as e:
        print(f"\n⚠️ Terjadi kesalahan saat menyimpan file JSON: {e}")

    input("\nTekan [Enter] untuk kembali ke menu utama...")


def lihat_riwayat_json():
    """Melihat seluruh log transaksi dari file JSON"""
    bersihkan_layar()
    tampilkan_header()
    print("\n📂 [RIWAYAT TRANSAKSI JSON]\n")

    if not os.path.exists(FILE_DATABASE):
        print("ℹ️ Belum ada file riwayat transaksi.")
        input("\nTekan [Enter] untuk kembali...")
        return

    try:
        with open(FILE_DATABASE, "r", encoding="utf-8") as file:
            riwayat = json.load(file)

        if not riwayat:
            print("ℹ️ Riwayat transaksi kosong.")
        else:
            print(f"Total Transaksi Tersimpan: {len(riwayat)} transaksi\n")
            for i, data in enumerate(riwayat, start=1):
                print(f"[{i}] ID: {data['id_transaksi']} | Waktu: {data['waktu']}")
                print(f"    Pemesan: {data['pemesan']['nama']} ({data['pemesan']['telepon']})")
                print(f"    Total  : {format_rupiah(data['total_pembayaran'])}")
                print(f"    Item   : {', '.join([f'{it['jumlah']}x {it['nama_bucket']}' for it in data['item_pesanan']])}")
                garis_pembatas("-")
    except Exception as e:
        print(f"⚠️ Gagal membaca data riwayat: {e}")

    input("\nTekan [Enter] untuk kembali...")


def main():
    """Fungsi utama program mencraft.id"""
    daftar_pesanan = []

    while True:
        bersihkan_layar()
        tampilkan_header()
        jumlah_keranjang = sum(item["jumlah"] for item in daftar_pesanan)
        print(f"\n🛒 Keranjang Aktif: {jumlah_keranjang} item ({len(daftar_pesanan)} jenis bucket)")
        print("\nMENU UTAMA MENCRAFT.ID:")
        print("1. Pilih Bucket      (Lihat Katalog & Harga)")
        print("2. Tambah Pesanan    (Masukkan ke Keranjang)")
        print("3. Kelola Pesanan    (Edit / Hapus Item)")
        print("4. Checkout          (Bayar & Simpan ke JSON)")
        print("5. Lihat File JSON   (Riwayat Transaksi)")
        print("0. Keluar Aplikasi")
        garis_pembatas("-")

        pilihan = input("Pilih menu [0-5]: ").strip()

        if pilihan == '1':
            fitur_1_pilih_bucket()
        elif pilihan == '2':
            fitur_2_tambah_pesanan(daftar_pesanan)
        elif pilihan == '3':
            fitur_3_kelola_pesanan(daftar_pesanan)
        elif pilihan == '4':
            fitur_4_checkout(daftar_pesanan)
        elif pilihan == '5':
            lihat_riwayat_json()
        elif pilihan == '0':
            bersihkan_layar()
            tampilkan_header()
            print("\nTerima kasih telah menggunakan aplikasi mencraft.id!")
            print("'The Perfect Gift at any Time' ✨\n")
            break
        else:
            print("⚠️ Pilihan tidak valid! Silakan pilih nomor 0-5.")
            input("Tekan [Enter] untuk coba lagi...")


if __name__ == "__main__":
    main()
