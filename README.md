# ZZZleep — Desktop Calendar, Audio Alarm & Rest Timer

<div align="center">

[![Windows .EXE](https://img.shields.io/badge/Windows-Standalone%20.EXE-0284c7?style=flat-square&logo=windows)](https://github.com/InfiniteNull/ZZZleep)
[![Python 3](https://img.shields.io/badge/Python-3.10+-38bdf8?style=flat-square&logo=python)](https://github.com/InfiniteNull/ZZZleep)
[![License: MIT](https://img.shields.io/badge/License-MIT-334155.svg?style=flat-square)](LICENSE)

<br />

<img src="assets/desktop_preview.png" alt="ZZZleep Desktop Application" width="880" />

</div>

> **ZZZleep** adalah aplikasi desktop native Windows untuk kalender, alarm audio sintetis, timer Pomodoro, dan pengingat istirahat layar (aturan 20-20-20). Seluruh data tersimpan secara lokal dan generator audio bekerja langsung melalui driver Windows tanpa file audio eksternal.

---

## Tampilan Antarmuka (UI Preview)

<div align="center">

### 1. Dashboard Alarm & Jadwal Waktu Lokal
<img src="assets/desktop_preview.png" alt="Dashboard Alarm" width="820" />

<br />

### 2. Timer Pomodoro & Pengingat Istirahat Layar (20-20-20)
<img src="assets/timers_preview.png" alt="Timer Pomodoro & Eye Rest" width="820" />

<br />

### 3. Penyimpanan Data JSON & Backup
<img src="assets/vault_preview.png" alt="Data JSON & Backup" width="820" />

</div>

---

## Fitur Utama

1. **Alarm Audio Sintetis (Bebas File Eksternal)**
   - Nada dering alarm dihasilkan langsung melalui modul `winsound.Beep` pada background thread, tanpa risiko file `.mp3` hilang atau rusak.
   - Pilihan nada: Arpeggio C-Mayor, nada digital 880Hz, dan bel harmonis.

2. **Pengingat Istirahat Layar (Aturan 20-20-20)**
   - Timer otomatis setiap 20 menit untuk mengingatkan pengguna mengalihkan pandangan sejauh 6 meter (20 kaki) selama 20 detik guna mencegah ketegangan mata digital.

3. **Timer Pomodoro (25/5)**
   - Siklus kerja fokus 25 menit diselingi istirahat 5 menit dengan notifikasi suara.

4. **Penyimpanan Data Lokal JSON**
   - Jadwal dan alarm tersimpan otomatis di direktori pengguna (`~/.zzzleep_desktop_data.json`) dan dapat dicadangkan secara manual.

5. **Standalone Windows Executable (.exe)**
   - Dapat dikompilasi menjadi satu file eksekusi mandiri tanpa perlu instalasi Python pada komputer target.

---

## Struktur Direktori

```text
ZZZleep/
├── assets/
│   ├── desktop_preview.png  # Tangkapan layar UI alarm & dashboard
│   ├── timers_preview.png   # Tangkapan layar UI pomodoro & 20-20-20
│   └── vault_preview.png    # Tangkapan layar UI penyimpanan data JSON
├── desktop/
│   ├── app.py               # Aplikasi native desktop Windows (Tkinter GUI)
│   └── build_exe.py         # Script build PyInstaller untuk membuat ZZZleep.exe
├── requirements.txt         # Dependensi build desktop
└── README.md                # Dokumentasi
```

---

## Cara Menjalankan & Build .EXE

### 1. Menjalankan Langsung dengan Python
```bash
# Clone repository
git clone https://github.com/InfiniteNull/ZZZleep.git
cd ZZZleep

# Jalankan aplikasi
python desktop/app.py
```

### 2. Kompilasi Menjadi File ZZZleep.exe Mandiri
```bash
# Install PyInstaller
pip install -r requirements.txt

# Jalankan automated builder
python desktop/build_exe.py
```
File `ZZZleep.exe` akan langsung tersedia di folder `desktop/dist/ZZZleep.exe` dan siap dipindahkan atau dijalankan di PC Windows manapun.

---

## Teknologi

- **GUI**: Python 3 & Tkinter (Dark theme styling).
- **Audio Engine**: Windows native `winsound` driver.
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
