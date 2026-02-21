# GitHub Activity Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)

**GitHub Activity Generator** adalah skrip Python sederhana namun *powerful* yang dirancang untuk mengisi grafik kontribusi GitHub Anda dengan riwayat *commit* buatan (fake history). Alat ini memungkinkan Anda untuk membuat profil GitHub terlihat aktif ("hijau") dalam hitungan menit.

> **⚠️ Disclaimer:** Script ini dibuat hanya untuk tujuan edukasi dan kesenangan semata. Keterampilan *coding* yang asli jauh lebih berharga daripada sekadar kotak hijau di profil!

---

## ✨ Fitur Utama

Berdasarkan kode sumber `contribute.py` dan dokumentasi asli, berikut adalah fitur utamanya:

* **Kustomisasi Penuh:** Atur frekuensi *commit* (persentase hari aktif), jumlah maksimal *commit* per hari, dan rentang waktu (hari sebelum/sesudah).
* **Mode Realistis:** Opsi `--no_weekends` agar tidak melakukan *commit* di hari Sabtu & Minggu, sehingga terlihat seperti aktivitas kerja normal.
* **Dukungan SSH Otomatis:** Script dapat melakukan *push* otomatis ke repositori jarak jauh menggunakan SSH key.
* **Optimasi Termux:** Ringan dan kompatibel dijalankan di lingkungan Termux (Android) maupun VPS.
* **Konfigurasi Identitas:** Bisa mengatur `user.name` dan `user.email` khusus untuk riwayat *commit* ini secara langsung lewat argumen.

---

## 🛠️ Teknologi yang Digunakan

* **Python 3**: Bahasa pemrograman utama untuk logika skrip.
* **Git**: Sistem kontrol versi untuk membuat *commit* dan *push*.
* **Bash/Shell**: Digunakan untuk eksekusi perintah sistem.

---

## 📋 Prasyarat Instalasi

Sebelum menjalankan script, pastikan lingkungan Anda memenuhi syarat berikut:

1.  **Python 3.x** terinstal.
2.  **Git** terinstal dan terkonfigurasi.
3.  **Koneksi SSH ke GitHub** (Sangat Disarankan agar tidak perlu memasukkan password berulang kali).

### Cara Setup SSH (Singkat)
```bash
# Generate key baru (jika belum punya)
ssh-keygen -t ed25519 -C "email-anda@example.com"

# Salin public key ke GitHub (Settings > SSH Keys)
cat ~/.ssh/id_ed25519.pub

# Test koneksi
ssh -T git@github.com

```

---

## 📂 Susunan Project

```text
.
├── contribute.py       # Script utama (logika generator)
├── LICENSE             # Lisensi MIT
└── README.md           # Dokumentasi proyek

```

---

## 🚀 Cara Penggunaan

### 1. Clone Repository

```bash
git clone https://github.com/wiraliwirya/GitHub-Activity-Generator
cd GitHub-Activity-Generator

```

### 2. Jalankan Script

Anda dapat menjalankan script `contribute.py` dengan berbagai argumen.

#### A. Mode Basic (Default)

Membuat *commit* untuk 365 hari ke belakang dengan pengaturan default.

```bash
python contribute.py --repository=git@github.com:USERNAME/REPO-TARGET.git

```

#### B. Mode Realistis (Rekomendasi)

Membuat riwayat yang terlihat alami: libur di akhir pekan, frekuensi 60%, maksimal 12 commit/hari.

```bash
python contribute.py \
  --repository=git@github.com:USERNAME/REPO-TARGET.git \
  --max_commits=12 \
  --frequency=60 \
  --no_weekends

```

#### C. Kustomisasi Lanjutan

Mengatur nama user git secara spesifik dan rentang hari yang lebih lama.

```bash
python contribute.py \
  --repository=git@github.com:USERNAME/REPO-TARGET.git \
  --user_name="Wira Liwirya" \
  --days_before=500 \
  --days_after=10

```

### Daftar Argumen Lengkap

| Argumen | Flag | Deskripsi | Default |
| --- | --- | --- | --- |
| `--repository` | `-r` | Link remote repository (SSH/HTTPS) | `None` |
| `--no_weekends` | `-nw` | Jangan commit di Sabtu/Minggu | `False` |
| `--max_commits` | `-mc` | Maksimal commit per hari | `10` |
| `--frequency` | `-fr` | Persentase hari untuk commit (0-100) | `80` |
| `--user_name` | `-un` | Git config user.name | `None` |
| `--user_email` | `-ue` | Git config user.email | `None` |
| `--days_before` | `-db` | Jumlah hari ke belakang dari sekarang | `365` |
| `--days_after` | `-da` | Jumlah hari ke depan dari sekarang | `0` |

*(Informasi argumen diambil dari fungsi `arguments` di `contribute.py`)*

---

## 🤝 Kontribusi

Kontribusi selalu diterima! Jika Anda ingin menambahkan fitur baru atau memperbaiki *bug*:

1. *Fork* repository ini.
2. Buat *branch* fitur baru (`git checkout -b fitur-keren`).
3. *Commit* perubahan Anda (`git commit -m 'Menambahkan fitur keren'`).
4. *Push* ke branch tersebut (`git push origin fitur-keren`).
5. Buat **Pull Request**.

---

## 📄 Lisensi

Proyek ini didistribusikan di bawah lisensi **MIT**. Lihat file [LICENSE](https://www.google.com/search?q=LICENSE) untuk detail lebih lanjut.

Copyright (c) 2026 **WIRA LIWIRYA**
