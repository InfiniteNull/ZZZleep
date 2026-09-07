# ⏰ ZZZleep Suite — Smart Offline Desktop Calendar, Precision Alarm & Routine Guardian

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-0ea5e9?style=for-the-badge&logo=github)](https://infinitenull.github.io/ZZZleep/)
[![Windows .EXE](https://img.shields.io/badge/Windows-Standalone%20.EXE-0284c7?style=for-the-badge&logo=windows)](https://github.com/InfiniteNull/ZZZleep)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Zero Telemetry](https://img.shields.io/badge/Privacy-100%25%20Offline%20Vault-10b981?style=for-the-badge)](https://github.com/InfiniteNull/ZZZleep)

> **ZZZleep Suite** adalah ekosistem manajemen waktu, kalender offline presisi, dan alarm audio cerdas yang dirancang khusus untuk meningkatkan produktivitas, menjaga kesehatan mata, dan mendisiplinkan ritme sirkadian kerja di laptop/PC tanpa ketergantungan koneksi internet dan tanpa pengumpulan data pihak ketiga (*Zero Telemetry*).

---

## 🌟 Fitur Utama (Core Highlights)

### 1. 📅 Interactive Offline Calendar & Event Scheduler
- Kalender bulanan interaktif dengan navigasi cepat, indikator hari ini, dan penanda jadwal visual.
- Penjadwalan aktivitas harian, deadline, dan agenda rutin yang tersimpan 100% aman di penyimpanan lokal (*Local Storage / JSON Vault*).

### 2. ⏰ Precision Multi-Alarm & Harmonic Audio Synthesizer
- Pengaturan alarm jam, menit, label aktivitas, dan pemilihan hari berulang (Senin–Minggu).
- **Web Audio API & Native Winsound Synthesizer**: Tidak membutuhkan berkas audio eksternal (`.mp3` atau `.wav`). Nada dering disintesis secara matematis secara *real-time* (C-Major Gentle Arpeggio, 880Hz Retro Beep, Harmonic Bell, Ambient Meditation Sine Pad).

### 3. 🍅 Pomodoro Focus Timer & 20-20-20 Screen Rest Guardian
- **Pomodoro Timer**: Siklus kerja fokus 25 menit dan jeda relaksasi 5 menit.
- **Aturan 20-20-20**: Pengingat otomatis setiap 20 menit menatap monitor untuk mengalihkan pandangan sejauh 6 meter (20 kaki) selama 20 detik guna mencegah ketegangan mata digital (*Digital Eye Strain*).

### 4. 📊 Daily Habit Tracker & Streak Analytics
- Pemantauan kebiasaan sehat harian (minum air 2L, peregangan postur, jam tidur teratur).
- Perhitungan *streak* otomatis dan persentase konsistensi mingguan.

### 5. 🔒 Zero-Telemetry Offline Data Vault
- Tidak ada data, kebiasaan, atau jadwal Anda yang dikirim ke server (*100% Privacy Preserved*).
- Fitur ekspor dan impor cadangan data lokal (*JSON One-Click Backup/Restore*).

---

## 💻 Dual-Deployment Architecture

ZZZleep Suite hadir dalam 2 bentuk implementasi:

```
ZZZleep/
├── index.html                # Web Suite PWA / GitHub Pages Client
├── js/
│   └── zzzleep-suite.js      # Pure Vanilla JS Suite (Audio Synthesizer, Calendar, Timers)
├── desktop/
│   ├── app.py                # Standalone Native Windows Desktop Application (Tkinter GUI)
│   └── build_exe.py          # Automated PyInstaller Windows .EXE Builder
├── requirements.txt          # Desktop Build Dependencies
└── README.md                 # Documentation
```

### 1. Web Application (GitHub Pages)
Buka langsung melalui peramban: [https://infinitenull.github.io/ZZZleep/](https://infinitenull.github.io/ZZZleep/)

### 2. Native Windows Application (.EXE)
Jalankan aplikasi desktop mandiri di Windows:
```bash
# Clone repositori
git clone https://github.com/InfiniteNull/ZZZleep.git
cd ZZZleep

# Jalankan langsung dengan Python
python desktop/app.py

# Kompilasi menjadi ZZZleep.exe mandiri
pip install -r requirements.txt
python desktop/build_exe.py
```
Hasil berkas eksekusi `.exe` akan langsung berada di folder `desktop/dist/ZZZleep.exe`.

---

## 🎨 Teknologi yang Digunakan

- **Frontend Web**: HTML5, Tailwind CSS, Vanilla JavaScript (ES6+), Web Audio API Oscillator Nodes, Lucide Icons.
- **Desktop Application**: Python 3, Tkinter GUI, Threading Engine, Windows `winsound` Driver, PyInstaller.
- **Arsitektur Data**: Local Storage API & Standalone JSON File System.

---

## 👨‍💻 Pengembang (Author)

**Rizki Ananda, S.Kom**  
- GitHub: [@InfiniteNull](https://github.com/InfiniteNull)
- Portfolio Hub: [https://infinitenull.github.io/](https://infinitenull.github.io/)

---

## 📜 Lisensi

Proyek ini dilisensikan di bawah lisensi [MIT](LICENSE).
