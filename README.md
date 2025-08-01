# Scribd Downloader Pro – Unduh Dokumen dengan Cepat dan Otomatis

![ScribdDP - Logo](https://github.com/user-attachments/assets/62a291cd-4853-4a5d-81cb-9f5692e32479)

**Scribd Downloader Pro** adalah alat berbasis command-line yang dirancang untuk mengunduh dokumen dari Scribd secara efisien, andal, dan sepenuhnya otomatis. Dibangun dengan prinsip rekayasa perangkat lunak profesional, proyek ini menawarkan kemudahan penggunaan dan kualitas kode tingkat tinggi, menjadikannya solusi ideal bagi mahasiswa, akademisi, atau siapa saja yang membutuhkan akses cepat ke referensi di Scribd.

## Latar Belakang dan Tujuan

Scribd merupakan salah satu platform populer untuk mengakses dokumen akademik, seperti makalah, buku, dan presentasi. Namun, banyak pengguna, terutama mahasiswa di Indonesia, menghadapi kendala seperti keharusan berlangganan premium atau mengunggah dokumen pribadi untuk mendapatkan akses penuh. Proses ini sering kali merepotkan dan memakan waktu.

**Scribd Downloader Pro** hadir untuk mengatasi masalah tersebut. Berawal dari skrip sederhana, proyek ini telah berkembang menjadi aplikasi matang dengan tujuan utama:

1. **Mempermudah Akses Pendidikan:** Menyediakan cara mudah untuk mengunduh materi referensi tanpa hambatan berlangganan.
2. **Otomatisasi Proses:** Mengubah proses pengunduhan manual menjadi alur kerja otomatis, mulai dari membuka halaman hingga menyimpan dokumen dalam format PDF yang bersih.
3. **Kualitas Perangkat Lunak:** Menerapkan praktik terbaik seperti _Object-Oriented Programming_ (OOP), struktur kode yang terorganisir, dan _logging_ informatif untuk mendukung skalabilitas dan kemudahan pemeliharaan.

## Fitur Unggulan

- **Struktur Kode Profesional:** Menggunakan prinsip OOP untuk memisahkan logika seperti interaksi _browser_, pemrosesan PDF, dan lainnya ke dalam kelas terpisah, memastikan kode mudah dipelihara dan diskalakan.
- **Input Fleksibel:** Mendukung masukan berupa URL Scribd lengkap (misalnya, `/document/...` atau `/embeds/...`) atau hanya ID dokumen.
- **Unduhan Otomatis:** Menggulir halaman secara otomatis untuk memuat semua konten, termasuk elemen yang dimuat secara _lazy-load_, sebelum mengonversinya ke PDF.
- **Penamaan File Cerdas:** Mengambil judul dokumen dari metadata untuk nama file. Jika metadata tidak tersedia, menggunakan nama _fallback_ yang aman.
- **Pembersihan Halaman Kosong:** Secara otomatis menghapus halaman kosong di dokumen hasil unduhan untuk hasil yang lebih rapi. Fitur ini dapat dinonaktifkan dengan opsi `--no-clean`.
- **Kompresi PDF Opsional:** Mengurangi ukuran file PDF menggunakan **Ghostscript** untuk hasil optimal, dengan metode _fallback_ berbasis PyPDF2 jika Ghostscript tidak tersedia.
- **Logging Informatif:** Memberikan _feedback_ jelas di setiap tahap proses. Gunakan opsi `--verbose` atau `-v` untuk log lebih rinci saat _debugging_.

## Prasyarat

Untuk menjalankan Scribd Downloader Pro, Anda memerlukan Python 3.8+ dan beberapa dependensi eksternal. Berikut adalah panduan langkah demi langkah untuk mempersiapkan lingkungan Anda.

### Dependensi Sistem

1. **Google Chrome & ChromeDriver**  
   
   - Pastikan **Google Chrome** terinstal. Cek versinya di `chrome://settings/help`.  
   - Unduh **ChromeDriver** yang sesuai dari [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/).  
   - Tambahkan file `chromedriver` ke direktori yang terdaftar di **PATH** sistem Anda.

2. **Ghostscript (Opsional)**  
   Untuk kompresi PDF terbaik, instal Ghostscript:  
   
   - **Windows:** Unduh dari [situs resmi Ghostscript](https://www.ghostscript.com/releases/gsdnld.html) dan tambahkan direktori `bin` ke PATH.  
   - **Linux (Debian/Ubuntu):**  
     
     ```bash
     sudo apt-get update
     sudo apt-get install ghostscript
     ```
   - **macOS (via Homebrew):**  
     
     ```bash
     brew install ghostscript
     ```

## Instalasi

1. **Kloning Repositori**  
   
   ```bash
   git clone https://github.com/RozhakXD/ScribdDownloaderPro.git
   cd ScribdDownloaderPro
   ```

2. **Buat Lingkungan Virtual (Direkomendasikan)**  
   
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Instal Dependensi Python**  
   
   ```bash
   pip install -r requirements.txt
   ```

## Cara Penggunaan

Jalankan skrip melalui file `main.py` dari terminal dengan sintaks berikut:

```bash
python main.py [URL_ATAU_ID] [OPSI]
```

### Contoh Penggunaan

Berikut adalah contoh perintah untuk menjalankan Scribd Downloader Pro dengan berbagai opsi:

| **Perintah**                                                      | **Deskripsi**                                     | **Kegunaan**                                                  |
| ----------------------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------------------- |
| `python main.py https://id.scribd.com/document/753477899/PPT-PBO` | Mengunduh dokumen menggunakan URL lengkap.        | Cocok untuk pengguna yang memiliki URL dokumen Scribd.        |
| `python main.py 753477899`                                        | Mengunduh dokumen menggunakan ID dokumen.         | Praktis jika hanya memiliki ID dokumen tanpa URL lengkap.     |
| `python main.py 753477899 --compress`                             | Mengunduh dokumen dengan kompresi PDF.            | Mengurangi ukuran file PDF untuk hemat penyimpanan.           |
| `python main.py 753477899 --no-clean`                             | Mengunduh dokumen tanpa menghapus halaman kosong. | Menjaga semua halaman, termasuk yang kosong, jika diperlukan. |
| `python main.py 753477899 --compress -v`                          | Mengunduh dengan kompresi dan log detail.         | Membantu melacak proses untuk debugging jika terjadi masalah. |

Hasil unduhan akan disimpan di direktori `downloads/` dalam format PDF.

## Kontribusi

Kami sangat menyambut kontribusi untuk meningkatkan proyek ini! Jika Anda menemukan bug, memiliki ide fitur baru, atau ingin memperbaiki kode, silakan:  

- Buat _Issue_ untuk melaporkan masalah atau saran.  
- Kirim _Pull Request_ dengan perubahan Anda.  

Pastikan untuk mengikuti pedoman kontribusi di repositori ini.

## Ucapan Terima Kasih

Terima kasih kepada komunitas open-source dan semua kontributor yang telah mendukung pengembangan Scribd Downloader Pro. Proyek ini dibuat dengan semangat untuk memajukan akses pendidikan bagi semua. 💙

## Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE). Lihat file `LICENSE` untuk informasi lebih lanjut.