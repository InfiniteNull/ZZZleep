# ZZZleep — Desktop Calendar, Audio Alarm & Rest Timer

<div align="center">

[![Python 3](https://img.shields.io/badge/Python-3.10+-38bdf8?style=flat-square&logo=python)](https://github.com/InfiniteNull/ZZZleep)
[![License: MIT](https://img.shields.io/badge/License-MIT-334155.svg?style=flat-square)](LICENSE)
[![Version: 1.1.0](https://img.shields.io/badge/Version-1.1.0-10b981?style=flat-square)](version.json)

<br />

<img src="assets/desktop_preview.png" alt="ZZZleep Desktop Application" width="880" />

</div>

> **ZZZleep** adalah aplikasi desktop untuk kalender, alarm audio sintetis, timer Pomodoro, dan pengingat istirahat layar (aturan 20-20-20). Dilengkapi sistem auto-update terintegrasi GitHub, pilihan 5 nada suara harmonis, sakelar istirahat mata, serta dukungan dwibahasa (ID/EN) dan tema Gelap/Terang.

---

## Tampilan Antarmuka (UI Preview)

<div align="center">

### 1. Dashboard Alarm, Jadwal & Pilihan Nada Suara
<img src="assets/desktop_preview.png" alt="Dashboard Alarm" width="820" />

<br />

### 2. Timer Pomodoro & Kontrol Pengingat Istirahat Layar (20-20-20)
<img src="assets/timers_preview.png" alt="Timer Pomodoro & Eye Rest" width="820" />

<br />

### 3. Pengaturan Preferensi, Data JSON & Pembaruan
<img src="assets/vault_preview.png" alt="Data JSON & Pembaruan" width="820" />

</div>

---

## Fitur Utama (v1.1.0)

1. **5 Pilihan Nada Suara Sintetis (Bebas File Eksternal)**
   - Nada dering alarm dihasilkan secara sintetis melalui modul `winsound` pada background thread.
   - Pilihan nada: *Gentle Arpeggio (C-Major)*, *Digital Pulse (880/1760Hz)*, *Harmonic Bell (440Hz)*, *Ascending Chime*, dan *Zen Minimalist (520Hz)*.

2. **Kontrol Sakelar Pengingat Istirahat Layar (20-20-20)**
   - Sakelar ON/OFF untuk menyalakan atau mematikan pengingat istirahat mata.
   - Pilihan interval fleksibel (15m, 20m, 30m, 45m).

3. **Dukungan Dwibahasa Penuh (Indonesian & English)**
   - Tombol pengubah bahasa instan (ID / EN) di header dan tab pengaturan tanpa memerlukan restart aplikasi.

4. **Tema Antarmuka Gelap & Terang (Dark / Light Mode)**
   - Pilihan palet warna Gelap (Dark Slate) dan Terang (Light Slate) yang nyaman untuk berbagai kondisi pencahayaan.

5. **Timer Pomodoro (25/5)**
   - Siklus kerja fokus 25 menit diselingi istirahat 5 menit dengan notifikasi suara.

6. **Sistem Auto-Update Terintegrasi GitHub**
   - Mendeteksi rilis versi baru secara otomatis melalui file manifest `version.json` di repository GitHub.
   - Menampilkan pop-up dialog rilis lengkap dengan perbandingan versi, daftar changelog, dan tombol unduh binary `.exe`.

7. **Penyimpanan Data Lokal JSON**
   - Preferensi, jadwal, dan status tersimpan otomatis di direktori pengguna (`~/.zzzleep_desktop_data.json`).

---

## Struktur Direktori

```text
ZZZleep/
├── assets/
│   ├── desktop_preview.png  # Tangkapan layar UI alarm & dashboard
│   ├── timers_preview.png   # Tangkapan layar UI pomodoro & 20-20-20
│   └── vault_preview.png    # Tangkapan layar UI pengaturan, data & update
├── bin/
│   └── ZZZleep.exe          # Binary mandiri v1.1.0 siap jalan langsung
├── desktop/
│   ├── app.py               # Aplikasi desktop GUI & Auto-Updater engine
│   └── build_exe.py         # Script build PyInstaller
├── version.json             # Manifest versi & changelog untuk auto-update
├── requirements.txt         # Dependensi build
└── README.md                # Dokumentasi
```

---

## Cara Menjalankan & Kompilasi

### 1. Mengunduh Binary Siap Jalan
Unduh langsung file binary [**`bin/ZZZleep.exe`**](https://github.com/InfiniteNull/ZZZleep/raw/main/bin/ZZZleep.exe) dan jalankan langsung pada komputer Windows tanpa memerlukan instalasi Python.

### 2. Menjalankan Langsung dengan Python
```bash
# Clone repository
git clone https://github.com/InfiniteNull/ZZZleep.git
cd ZZZleep

# Jalankan aplikasi
python desktop/app.py
```

### 3. Kompilasi Mandiri via PyInstaller
```bash
# Install dependensi
pip install -r requirements.txt

# Jalankan automated builder
python desktop/build_exe.py
```
Berkas eksekusi mandiri akan dibuat di folder `desktop/dist/ZZZleep.exe`.

---

## Teknologi

- **GUI**: Python 3 & Tkinter (Dark & Light theme styling).
- **Audio Engine**: Modul audio sintetis harmonis (`winsound`).
- **Updater Engine**: Background non-blocking GitHub manifest fetcher (`urllib.request`).
- **Packaging**: PyInstaller (`--noconsole --onefile`).
- **Data**: Local JSON storage engine.

---

## Pengembang

**Rizki Ananda, S.Kom**  
- GitHub: [@InfiniteNull](https://github.com/InfiniteNull)  
- Portfolio: [https://infinitenull.github.io/](https://infinitenull.github.io/)

---

## Lisensi

Proyek ini dilisensikan di bawah lisensi [MIT](LICENSE).
