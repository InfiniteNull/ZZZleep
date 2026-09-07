# ZZZleep — Offline Desktop Calendar, Audio Alarm & Rest Timer

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-0ea5e9?style=flat-square&logo=github)](https://infinitenull.github.io/ZZZleep/)
[![Windows .EXE](https://img.shields.io/badge/Windows-Standalone%20.EXE-0284c7?style=flat-square&logo=windows)](https://github.com/InfiniteNull/ZZZleep)
[![License: MIT](https://img.shields.io/badge/License-MIT-334155.svg?style=flat-square)](LICENSE)

> **ZZZleep** adalah aplikasi kalender offline, alarm audio, timer Pomodoro, dan pengingat istirahat layar untuk laptop dan PC Windows. Seluruh data tersimpan secara lokal dan generator audio bekerja tanpa ketergantungan file suara eksternal.

---

## Fitur Utama

1. **Kalender & Jadwal Offline**
   - Matriks kalender bulanan dengan penanda jadwal dan agenda kegiatan harian.
   - Tersimpan di penyimpanan lokal (*LocalStorage* pada web atau file JSON pada desktop).

2. **Alarm Audio (Web Audio API & Python winsound)**
   - Nada dering disintesis secara langsung menggunakan osilator audio di browser dan modul `winsound` di Python tanpa membutuhkan file audio eksternal (`.mp3` atau `.wav`).
   - Pilihan nada: Arpeggio C-Mayor, nada digital 880Hz, dan bel harmonis.

3. **Timer Pomodoro (25/5)**
   - Siklus kerja fokus 25 menit dan istirahat 5 menit dengan notifikasi audio.

4. **Pengingat Istirahat Layar (Aturan 20-20-20)**
   - Timer otomatis setiap 20 menit untuk mengistirahatkan mata dengan melihat objek sejauh 6 meter (20 kaki) selama 20 detik guna mencegah ketegangan mata digital.

5. **Pelacak Kebiasaan Harian**
   - Checklist rutinitas harian (target minum air 2L, stretching postur, jam tidur) disertai penghitung *streak*.

6. **Penyimpanan Data Lokal & Backup JSON**
   - Ekspor dan impor data jadwal dan preferensi dalam format JSON standar.

---

## Struktur Direktori

```text
ZZZleep/
├── index.html            # Web client (GitHub Pages)
├── js/
│   └── zzzleep.js  # Audio synthesizer, kalender, timer, dan storage engine
├── desktop/
│   ├── app.py            # Aplikasi native desktop Windows (Tkinter GUI)
│   └── build_exe.py      # Script build PyInstaller untuk membuat ZZZleep.exe
├── requirements.txt      # Dependensi build desktop
└── README.md             # Dokumentasi
```

---

## Cara Menjalankan

### 1. Web Version (Browser)
Akses langsung melalui GitHub Pages: [https://infinitenull.github.io/ZZZleep/](https://infinitenull.github.io/ZZZleep/)

### 2. Desktop Version (Windows Native)
```bash
# Clone repository
git clone https://github.com/InfiniteNull/ZZZleep.git
cd ZZZleep

# Jalankan langsung dengan Python
python desktop/app.py

# Kompilasi menjadi file ZZZleep.exe mandiri
pip install -r requirements.txt
python desktop/build_exe.py
```
File executable mandiri akan tersedia di folder `desktop/dist/ZZZleep.exe`.

---

## Teknologi

- **Web**: HTML5, Tailwind CSS, Vanilla JavaScript (ES6+), Web Audio API, Lucide Icons.
- **Desktop**: Python 3, Tkinter GUI, Windows `winsound` driver, PyInstaller.
- **Storage**: Browser LocalStorage & Local JSON file.

---

## Pengembang

**Rizki Ananda, S.Kom**  
- GitHub: [@InfiniteNull](https://github.com/InfiniteNull)  
- Portfolio: [https://infinitenull.github.io/](https://infinitenull.github.io/)

---

## Lisensi

Proyek ini dilisensikan di bawah lisensi [MIT](LICENSE).
