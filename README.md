# GitHub Activity Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)

**GitHub Activity Generator** adalah skrip Python sederhana namun *powerful* yang dirancang untuk mengisi grafik kontribusi GitHub Anda dengan riwayat *commit* buatan (fake history). Alat ini memungkinkan Anda untuk membuat profil GitHub terlihat aktif ("hijau") dalam hitungan menit.

> **⚠️ Disclaimer:** Script ini dibuat hanya untuk tujuan edukasi dan kesenangan semata. Keterampilan *coding* yang asli jauh lebih berharga daripada sekadar kotak hijau di profil!

---

## ✨ Fitur Utama

* **Kustomisasi Penuh:** Atur frekuensi *commit* (persentase hari aktif), jumlah maksimal *commit* per hari, dan rentang waktu (hari sebelum/sesudah).
* **Mode Realistis:** Opsi `--no_weekends` agar tidak melakukan *commit* di hari Sabtu & Minggu, sehingga terlihat seperti aktivitas kerja normal.
* **Aman untuk README:** Tersedia skrip `contribute2.py` yang menggunakan file `commits.txt` khusus untuk *log* riwayat aktivitas, sehingga tidak akan menyentuh atau merusak `README.md` proyek.
* **Dukungan Push Otomatis:** Script dapat melakukan *push* otomatis ke repositori jarak jauh menggunakan koneksi yang sudah diatur (seperti SSH).
* **Konfigurasi Identitas:** Bisa mengatur `user.name` dan `user.email` khusus untuk riwayat *commit* ini secara langsung lewat argumen CLI.

---

## 🛠️ Teknologi yang Digunakan

* **Python 3**: Bahasa pemrograman utama untuk menjalankan logika skrip (*randomizer* waktu dan penanganan argumen).
* **Git**: Sistem kontrol versi untuk melakukan inisialisasi, membuat *commit*, dan *push*.
* **Bash/Shell**: Digunakan secara *native* oleh skrip untuk mengeksekusi perintah sistem.

---

## 📋 Prasyarat Instalasi

Sebelum menjalankan script, pastikan lingkungan Anda memenuhi syarat berikut:

1.  **Python 3.x** terinstal di sistem Anda.
2.  **Git** terinstal dan terkonfigurasi dengan benar.
3.  **Koneksi SSH ke GitHub** (Sangat disarankan agar proses *push* berjalan otomatis tanpa perlu memasukkan kata sandi berulang kali).

### 🔑 Cara Setup SSH (Singkat)

Jika Anda belum menghubungkan komputer lokal ke GitHub via SSH, ikuti langkah berikut:

```bash
# 1. Generate SSH key baru (jika belum punya)
ssh-keygen -t ed25519 -C "email-github-anda@example.com"

# 2. Tampilkan public key untuk disalin
cat ~/.ssh/id_ed25519.pub

# 3. Salin output di atas, buka GitHub.com > Settings > SSH and GPG keys > New SSH key
# 4. Paste key tersebut dan simpan.

# 5. Test koneksi
ssh -T git@github.com
# Akan muncul pesan: "Hi username! You've successfully authenticated..."

```

---

## 📂 Susunan Project

* `contribute.py`: Script generator utama yang akan menambahkan *log* aktivitas langsung ke dalam file `README.md`.
* `contribute2.py`: Versi skrip yang lebih canggih dengan sistem *logging* bawaan Python dan menggunakan file `commits.txt` terpisah untuk mendata riwayat *commit*.
* `LICENSE`: Berisi dokumen resmi Lisensi MIT.
* `README.md`: Dokumentasi proyek ini sendiri.

---

## 🚀 Cara Penggunaan

### 1. Clone Repository

Langkah pertama adalah mengunduh repositori ini ke komputer lokal Anda:

```bash
git clone https://github.com/wiraliwirya/GitHub-Activity-Generator
cd GitHub-Activity-Generator

```

### 2. Jalankan Script

Anda dapat menjalankan script `contribute.py` atau `contribute2.py` dengan berbagai argumen melalui terminal.

#### Mode Basic (Default)

Membuat *commit* untuk 365 hari ke belakang dengan pengaturan *default*.

```bash
python contribute2.py --repository=git@github.com:USERNAME/REPO-TARGET.git

```

#### Mode Realistis (Rekomendasi)

Membuat riwayat yang terlihat alami: libur di akhir pekan, frekuensi aktif 60%, dan maksimal 12 *commit* per hari.

```bash
python contribute2.py \
  --repository=git@github.com:USERNAME/REPO-TARGET.git \
  --max_commits=12 \
  --frequency=60 \
  --no_weekends

```

### Daftar Argumen Lengkap

| Argumen | Flag | Deskripsi | Default |
| --- | --- | --- | --- |
| `--repository` | `-r` | Link remote repository GitHub (SSH/HTTPS) | `None` |
| `--no_weekends` | `-nw` | Jangan commit di hari Sabtu/Minggu | `False` |
| `--max_commits` | `-mc` | Maksimal commit per hari (Maksimal batas: 20) | `10` |
| `--frequency` | `-fr` | Persentase hari untuk commit (0-100) | `80` |
| `--user_name` | `-un` | Mengatur `user.name` konfigurasi Git | `None` |
| `--user_email` | `-ue` | Mengatur `user.email` konfigurasi Git | `None` |
| `--days_before` | `-db` | Jumlah hari ke belakang dari hari ini | `365` |
| `--days_after` | `-da` | Jumlah hari ke depan dari hari ini | `0` |

---

## 🤝 Kontribusi

Kontribusi selalu diterima! Jika Anda ingin menambahkan fitur baru atau memperbaiki *bug*:

1. *Fork* repository ini.
2. Buat *branch* fitur baru Anda (`git checkout -b fitur-keren`).
3. Lakukan *commit* pada perubahan Anda (`git commit -m 'Menambahkan fitur keren'`).
4. *Push* ke branch tersebut (`git push origin fitur-keren`).
5. Buat **Pull Request** di GitHub.

---

## 📄 Lisensi

Proyek ini didistribusikan di bawah lisensi **MIT**.
Anda diizinkan secara gratis untuk menggunakan, menyalin, memodifikasi, menggabungkan, menerbitkan, dan mendistribusikan salinan perangkat lunak ini tanpa batasan, asalkan pemberitahuan hak cipta dan izin disertakan dalam semua salinan. Perangkat lunak ini disediakan "APA ADANYA" tanpa jaminan apa pun.

Copyright (c) 2026 **WIRA LIWIRYA**
