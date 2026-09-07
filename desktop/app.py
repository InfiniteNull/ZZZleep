#!/usr/bin/env python3
"""
ZZZleep — Desktop Calendar, Audio Alarm & Rest Timer
Author: Rizki Ananda, S.Kom (@InfiniteNull)
License: MIT
"""

import os
import sys
import json
import time
import math
import threading
import datetime
import urllib.request
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox

# Windows Sound Support
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

# Application Meta & Update Config
APP_NAME = "ZZZleep"
APP_VERSION = "1.0.0"
DATA_FILE = os.path.join(os.path.expanduser("~"), ".zzzleep_desktop_data.json")
UPDATE_MANIFEST_URL = "https://raw.githubusercontent.com/InfiniteNull/ZZZleep/main/version.json"
GITHUB_REPO_URL = "https://github.com/InfiniteNull/ZZZleep"

DEFAULT_DATA = {
    "alarms": [
        {"id": "alarm-1", "title": "Bangun Pagi & Stretching", "time": "06:00", "enabled": True, "days": [1, 2, 3, 4, 5], "tone": "gentle"},
        {"id": "alarm-2", "title": "Istirahat Siang & Makan", "time": "12:00", "enabled": True, "days": [1, 2, 3, 4, 5], "tone": "retro"},
        {"id": "alarm-3", "title": "Tutup Laptop & Persiapan Tidur", "time": "22:30", "enabled": True, "days": [0, 1, 2, 3, 4, 5, 6], "tone": "acoustic"}
    ],
    "habits": [
        {"id": "h-1", "name": "Minum Air Putih 2L", "target": 1, "completedDays": [1, 2, 3, 4, 5]},
        {"id": "h-2", "name": "Stretching & Postur Tubuh", "target": 1, "completedDays": [1, 2, 3]},
        {"id": "h-3", "name": "Jeda Layar 20-20-20 Rutin", "target": 1, "completedDays": [1, 2, 3, 4]}
    ],
    "settings": {
        "soundTone": "gentle",
        "eyeRestIntervalMin": 20
    }
}


def parse_version(v_str):
    """Parses semver string into comparable tuple."""
    try:
        clean = str(v_str).strip().lstrip('v')
        return tuple(int(x) for x in clean.split('.'))
    except Exception:
        return (0, 0, 0)


def play_audio_tone(tone_type="gentle"):
    """Synthesizes harmonic beeps using native winsound."""
    if not HAS_WINSOUND:
        return

    def _beep_worker():
        try:
            if tone_type == "gentle":
                # Arpeggio C-Mayor: C5 (523Hz), E5 (659Hz), G5 (784Hz), C6 (1046Hz)
                notes = [523, 659, 784, 1046]
                for freq in notes:
                    winsound.Beep(freq, 200)
                    time.sleep(0.04)
            elif tone_type == "retro":
                for _ in range(2):
                    winsound.Beep(880, 150)
                    time.sleep(0.06)
                    winsound.Beep(1760, 180)
                    time.sleep(0.08)
            elif tone_type == "acoustic":
                winsound.Beep(440, 250)
                time.sleep(0.05)
                winsound.Beep(880, 400)
            else:
                winsound.Beep(600, 300)
        except Exception:
            pass

    t = threading.Thread(target=_beep_worker, daemon=True)
    t.start()


class ZzzleepDesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("920x660")
        self.root.minsize(840, 580)
        self.root.configure(bg="#0f172a")

        self.data = self.load_data()
        self.pomodoro_seconds_left = 25 * 60
        self.pomodoro_is_running = False
        self.eye_rest_seconds_left = self.data.get("settings", {}).get("eyeRestIntervalMin", 20) * 60
        self.eye_rest_is_running = True

        self.setup_styles()
        self.build_ui()
        self.start_background_timer()

        # Background update check on launch (silent)
        self.root.after(2000, lambda: self.check_for_updates_async(silent=True))

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return DEFAULT_DATA.copy()
        return DEFAULT_DATA.copy()

    def save_data(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Failed to save data: {e}")

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        bg_dark = "#0f172a"
        card_bg = "#1e293b"
        accent = "#0284c7"
        text_white = "#f8fafc"
        text_muted = "#94a3b8"

        self.style.configure("TNotebook", background=bg_dark, borderwidth=0)
        self.style.configure("TNotebook.Tab", background="#1e293b", foreground=text_muted, padding=[16, 8], font=("Segoe UI", 10, "bold"))
        self.style.map("TNotebook.Tab",
                       background=[("selected", "#0284c7")],
                       foreground=[("selected", "#ffffff")])

        self.style.configure("TFrame", background=bg_dark)
        self.style.configure("Card.TFrame", background=card_bg, relief="flat")
        self.style.configure("TLabel", background=bg_dark, foreground=text_white, font=("Segoe UI", 10))

    def build_ui(self):
        # Header Bar
        header = tk.Frame(self.root, bg="#1e293b", height=56)
        header.pack(fill="x", side="top")

        brand = tk.Label(header, text="⏰ ZZZleep", font=("Segoe UI", 13, "bold"), fg="#38bdf8", bg="#1e293b")
        brand.pack(side="left", padx=16, pady=12)

        self.top_clock = tk.Label(header, text="--:--:--", font=("Consolas", 12, "bold"), fg="#f8fafc", bg="#1e293b")
        self.top_clock.pack(side="right", padx=16)

        # Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=10)

        # Tab 1: Alarms
        tab_alarms = ttk.Frame(self.notebook)
        self.notebook.add(tab_alarms, text="  ⏰ Alarm & Jadwal  ")
        self.build_alarms_tab(tab_alarms)

        # Tab 2: Timers
        tab_timers = ttk.Frame(self.notebook)
        self.notebook.add(tab_timers, text="  🍅 Pomodoro & Istirahat Layar  ")
        self.build_timers_tab(tab_timers)

        # Tab 3: Habits, Data & Updates
        tab_vault = ttk.Frame(self.notebook)
        self.notebook.add(tab_vault, text="  📁 Data JSON & Pembaruan  ")
        self.build_vault_tab(tab_vault)

    def build_alarms_tab(self, parent):
        container = tk.Frame(parent, bg="#0f172a")
        container.pack(fill="both", expand=True, padx=6, pady=6)

        # Left Column (Clock & Add Form)
        left = tk.Frame(container, bg="#1e293b", width=310)
        left.pack(side="left", fill="y", padx=6, pady=6)
        left.pack_propagate(False)

        tk.Label(left, text="WAKTU LOKAL", font=("Segoe UI", 8, "bold"), fg="#64748b", bg="#1e293b").pack(anchor="w", padx=16, pady=(16, 2))
        self.clock_lbl = tk.Label(left, text="00:00:00", font=("Consolas", 26, "bold"), fg="#38bdf8", bg="#1e293b")
        self.clock_lbl.pack(anchor="w", padx=16)
        self.date_lbl = tk.Label(left, text="Loading...", font=("Segoe UI", 10), fg="#94a3b8", bg="#1e293b")
        self.date_lbl.pack(anchor="w", padx=16, pady=(0, 14))

        tk.Frame(left, height=1, bg="#334155").pack(fill="x", padx=16, pady=6)

        tk.Label(left, text="Tambah Alarm Baru", font=("Segoe UI", 11, "bold"), fg="#f8fafc", bg="#1e293b").pack(anchor="w", padx=16, pady=4)

        # Time Input
        tk.Label(left, text="Jam (HH:MM):", font=("Segoe UI", 9), fg="#94a3b8", bg="#1e293b").pack(anchor="w", padx=16, pady=(6, 2))
        self.entry_time = tk.Entry(left, font=("Consolas", 12), bg="#0f172a", fg="#38bdf8", insertbackground="#38bdf8", relief="flat")
        self.entry_time.insert(0, "07:30")
        self.entry_time.pack(fill="x", padx=16, ipady=4)

        # Title Input
        tk.Label(left, text="Keterangan / Label:", font=("Segoe UI", 9), fg="#94a3b8", bg="#1e293b").pack(anchor="w", padx=16, pady=(8, 2))
        self.entry_title = tk.Entry(left, font=("Segoe UI", 10), bg="#0f172a", fg="#f8fafc", insertbackground="#38bdf8", relief="flat")
        self.entry_title.insert(0, "Mulai Kerja Pagi")
        self.entry_title.pack(fill="x", padx=16, ipady=4)

        # Buttons
        btn_add = tk.Button(left, text="+ Pasang Alarm", font=("Segoe UI", 10, "bold"), bg="#0284c7", fg="white", activebackground="#0369a1", activeforeground="white", relief="flat", command=self.add_alarm)
        btn_add.pack(fill="x", padx=16, pady=(16, 6), ipady=5)

        btn_test = tk.Button(left, text="🔊 Uji Suara Harmonis", font=("Segoe UI", 9), bg="#334155", fg="#f8fafc", relief="flat", command=lambda: play_audio_tone("gentle"))
        btn_test.pack(fill="x", padx=16, pady=4, ipady=4)

        # Right Column (List of Alarms)
        right = tk.Frame(container, bg="#1e293b")
        right.pack(side="right", fill="both", expand=True, padx=6, pady=6)

        header_r = tk.Frame(right, bg="#1e293b")
        header_r.pack(fill="x", padx=16, pady=12)
        tk.Label(header_r, text="Daftar Alarm Aktif", font=("Segoe UI", 12, "bold"), fg="#f8fafc", bg="#1e293b").pack(side="left")

        self.alarms_frame = tk.Frame(right, bg="#1e293b")
        self.alarms_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        self.refresh_alarms()

    def refresh_alarms(self):
        for w in self.alarms_frame.winfo_children():
            w.destroy()

        alarms = self.data.get("alarms", [])
        if not alarms:
            tk.Label(self.alarms_frame, text="Belum ada alarm aktif.", fg="#64748b", bg="#1e293b", font=("Segoe UI", 10, "italic")).pack(pady=30)
            return

        for a in alarms:
            card = tk.Frame(self.alarms_frame, bg="#0f172a", relief="flat", bd=1)
            card.pack(fill="x", pady=4)

            left_box = tk.Frame(card, bg="#0f172a")
            left_box.pack(side="left", padx=12, pady=10)

            time_col = "#38bdf8" if a.get("enabled", True) else "#64748b"
            tk.Label(left_box, text=a["time"], font=("Consolas", 18, "bold"), fg=time_col, bg="#0f172a").pack(anchor="w")
            tk.Label(left_box, text=a.get("title", "Alarm"), font=("Segoe UI", 10, "bold"), fg="#f8fafc" if a.get("enabled", True) else "#64748b", bg="#0f172a").pack(anchor="w")

            right_box = tk.Frame(card, bg="#0f172a")
            right_box.pack(side="right", padx=12, pady=10)

            st_text = "AKTIF" if a.get("enabled", True) else "NONAKTIF"
            st_bg = "#059669" if a.get("enabled", True) else "#475569"
            t_btn = tk.Button(right_box, text=st_text, font=("Segoe UI", 8, "bold"), bg=st_bg, fg="white", relief="flat", padx=8, pady=2, command=lambda item=a: self.toggle_alarm(item))
            t_btn.pack(side="left", padx=4)

            d_btn = tk.Button(right_box, text="✕", font=("Segoe UI", 8, "bold"), bg="#dc2626", fg="white", relief="flat", padx=6, pady=2, command=lambda a_id=a["id"]: self.delete_alarm(a_id))
            d_btn.pack(side="left", padx=4)

    def add_alarm(self):
        t_str = self.entry_time.get().strip()
        title = self.entry_title.get().strip() or "Alarm"

        try:
            parts = t_str.split(":")
            h, m = int(parts[0]), int(parts[1])
            if not (0 <= h < 24 and 0 <= m < 60):
                raise ValueError
            valid_time = f"{h:02d}:{m:02d}"
        except Exception:
            messagebox.showerror("Format Salah", "Masukkan format HH:MM (contoh: 07:30).")
            return

        new_a = {
            "id": f"alarm-{int(time.time()*1000)}",
            "title": title,
            "time": valid_time,
            "enabled": True,
            "days": [0, 1, 2, 3, 4, 5, 6],
            "tone": "gentle"
        }
        self.data["alarms"].append(new_a)
        self.save_data()
        self.refresh_alarms()

    def toggle_alarm(self, a):
        a["enabled"] = not a.get("enabled", True)
        self.save_data()
        self.refresh_alarms()

    def delete_alarm(self, a_id):
        self.data["alarms"] = [a for a in self.data.get("alarms", []) if a.get("id") != a_id]
        self.save_data()
        self.refresh_alarms()

    def build_timers_tab(self, parent):
        container = tk.Frame(parent, bg="#0f172a")
        container.pack(fill="both", expand=True, padx=6, pady=6)

        # Pomodoro Card
        pomo = tk.Frame(container, bg="#1e293b")
        pomo.pack(side="left", fill="both", expand=True, padx=6, pady=6)

        tk.Label(pomo, text="🍅 POMODORO FOCUS TIMER", font=("Segoe UI", 12, "bold"), fg="#f43f5e", bg="#1e293b").pack(pady=(20, 10))
        self.pomo_clock = tk.Label(pomo, text="25:00", font=("Consolas", 42, "bold"), fg="#f8fafc", bg="#1e293b")
        self.pomo_clock.pack(pady=10)

        pomo_btns = tk.Frame(pomo, bg="#1e293b")
        pomo_btns.pack(pady=12)

        self.btn_pomo = tk.Button(pomo_btns, text="Mulai Sesi (25m)", font=("Segoe UI", 10, "bold"), bg="#f43f5e", fg="white", relief="flat", padx=14, pady=6, command=self.toggle_pomodoro)
        self.btn_pomo.pack(side="left", padx=6)

        btn_pomo_r = tk.Button(pomo_btns, text="Reset", font=("Segoe UI", 10), bg="#334155", fg="#f8fafc", relief="flat", padx=10, pady=6, command=self.reset_pomodoro)
        btn_pomo_r.pack(side="left", padx=6)

        tk.Label(pomo, text="Siklus kerja fokus 25 menit diselingi istirahat 5 menit\nuntuk menjaga konsentrasi kerja.", font=("Segoe UI", 9), fg="#94a3b8", bg="#1e293b", justify="center").pack(pady=16)

        # Eye Rest Card
        eye = tk.Frame(container, bg="#1e293b")
        eye.pack(side="right", fill="both", expand=True, padx=6, pady=6)

        tk.Label(eye, text="👁️ PENGINGAT ISTIRAHAT MATA (20-20-20)", font=("Segoe UI", 12, "bold"), fg="#10b981", bg="#1e293b").pack(pady=(20, 10))
        self.eye_clock = tk.Label(eye, text="20:00", font=("Consolas", 42, "bold"), fg="#f8fafc", bg="#1e293b")
        self.eye_clock.pack(pady=10)

        eye_btns = tk.Frame(eye, bg="#1e293b")
        eye_btns.pack(pady=12)

        btn_eye_r = tk.Button(eye_btns, text="Reset Interval (20m)", font=("Segoe UI", 10, "bold"), bg="#10b981", fg="white", relief="flat", padx=14, pady=6, command=self.reset_eye_rest)
        btn_eye_r.pack(side="left", padx=6)

        tk.Label(eye, text="Setiap 20 menit menatap layar monitor laptop/PC,\npandang objek sejauh 20 kaki (6 meter) selama 20 detik\nguna mencegah ketegangan mata digital.", font=("Segoe UI", 9), fg="#94a3b8", bg="#1e293b", justify="center").pack(pady=16)

    def toggle_pomodoro(self):
        self.pomodoro_is_running = not self.pomodoro_is_running
        if self.pomodoro_is_running:
            self.btn_pomo.config(text="Jeda Sesi", bg="#d97706")
        else:
            self.btn_pomo.config(text="Lanjutkan Sesi", bg="#f43f5e")

    def reset_pomodoro(self):
        self.pomodoro_is_running = False
        self.pomodoro_seconds_left = 25 * 60
        self.btn_pomo.config(text="Mulai Sesi (25m)", bg="#f43f5e")
        self.pomo_clock.config(text="25:00")

    def reset_eye_rest(self):
        self.eye_rest_seconds_left = 20 * 60
        self.eye_clock.config(text="20:00")

    def build_vault_tab(self, parent):
        container = tk.Frame(parent, bg="#0f172a")
        container.pack(fill="both", expand=True, padx=6, pady=6)

        # 1. Local Storage Card
        card = tk.Frame(container, bg="#1e293b")
        card.pack(fill="x", padx=6, pady=(6, 8))

        tk.Label(card, text="📁 PENYIMPANAN DATA LOKAL (JSON)", font=("Segoe UI", 12, "bold"), fg="#38bdf8", bg="#1e293b").pack(anchor="w", padx=20, pady=(16, 4))
        tk.Label(card, text=f"Lokasi File: {DATA_FILE}", font=("Consolas", 9), fg="#94a3b8", bg="#1e293b").pack(anchor="w", padx=20, pady=(0, 10))

        info_text = (
            "Karakteristik Aplikasi:\n"
            "1. Seluruh data preferensi & jadwal tersimpan secara lokal dalam format JSON.\n"
            "2. Generator nada alarm dihasilkan secara sintetis menggunakan modul audio bawaan.\n"
            "3. Berkas basis data dapat dicadangkan atau dipindahkan secara manual kapan saja."
        )
        tk.Label(card, text=info_text, font=("Segoe UI", 9), fg="#e2e8f0", bg="#1e293b", justify="left").pack(anchor="w", padx=20, pady=4)

        btn_box = tk.Frame(card, bg="#1e293b")
        btn_box.pack(anchor="w", padx=20, pady=(12, 16))

        btn_open = tk.Button(btn_box, text="Buka Folder Data", font=("Segoe UI", 9, "bold"), bg="#0284c7", fg="white", relief="flat", padx=12, pady=5, command=lambda: os.system(f'explorer /select,"{DATA_FILE}"'))
        btn_open.pack(side="left", padx=(0, 8))

        btn_save = tk.Button(btn_box, text="Simpan JSON Sekarang", font=("Segoe UI", 9), bg="#334155", fg="#f8fafc", relief="flat", padx=12, pady=5, command=self.save_data)
        btn_save.pack(side="left", padx=8)

        # 2. Update & Version Sync Card
        up_card = tk.Frame(container, bg="#1e293b")
        up_card.pack(fill="both", expand=True, padx=6, pady=(0, 6))

        tk.Label(up_card, text="🔄 SINKRONISASI & PEMBARUAN VERSI", font=("Segoe UI", 12, "bold"), fg="#10b981", bg="#1e293b").pack(anchor="w", padx=20, pady=(16, 4))
        
        up_meta = tk.Frame(up_card, bg="#1e293b")
        up_meta.pack(fill="x", padx=20, pady=4)
        
        tk.Label(up_meta, text=f"Versi Aplikasi Saat Ini: v{APP_VERSION}", font=("Segoe UI", 10, "bold"), fg="#f8fafc", bg="#1e293b").pack(side="left")
        
        self.lbl_update_status = tk.Label(up_meta, text="● Siap memeriksa pembaruan", font=("Segoe UI", 9), fg="#94a3b8", bg="#1e293b")
        self.lbl_update_status.pack(side="left", padx=14)

        up_desc = (
            "Sistem Auto-Update terhubung langsung dengan manifest versi di repository GitHub.\n"
            "Ketika versi baru dirilis, aplikasi akan menampilkan pop-up detail changelog dan opsi unduh."
        )
        tk.Label(up_card, text=up_desc, font=("Segoe UI", 9), fg="#94a3b8", bg="#1e293b", justify="left").pack(anchor="w", padx=20, pady=6)

        up_btn_box = tk.Frame(up_card, bg="#1e293b")
        up_btn_box.pack(anchor="w", padx=20, pady=(8, 16))

        self.btn_check_update = tk.Button(up_btn_box, text="🔄 Periksa Pembaruan Sekarang", font=("Segoe UI", 9, "bold"), bg="#059669", fg="white", activebackground="#047857", activeforeground="white", relief="flat", padx=14, pady=6, command=lambda: self.check_for_updates_async(silent=False))
        self.btn_check_update.pack(side="left", padx=(0, 8))

        btn_repo = tk.Button(up_btn_box, text="🌐 Buka GitHub Repository", font=("Segoe UI", 9), bg="#334155", fg="#f8fafc", relief="flat", padx=12, pady=6, command=lambda: webbrowser.open(GITHUB_REPO_URL))
        btn_repo.pack(side="left", padx=8)

    def check_for_updates_async(self, silent=True):
        """Asynchronously checks version.json from GitHub."""
        if hasattr(self, 'lbl_update_status'):
            self.lbl_update_status.config(text="⏳ Memeriksa ke GitHub...", fg="#38bdf8")

        def _worker():
            try:
                req = urllib.request.Request(
                    UPDATE_MANIFEST_URL,
                    headers={"User-Agent": f"ZZZleep-Desktop/{APP_VERSION}"}
                )
                with urllib.request.urlopen(req, timeout=6) as resp:
                    if resp.status == 200:
                        raw = resp.read().decode('utf-8')
                        data = json.loads(raw)
                        remote_ver = data.get("version", "1.0.0")
                        
                        if parse_version(remote_ver) > parse_version(APP_VERSION):
                            self.root.after(0, lambda: self.on_update_found(data))
                        else:
                            self.root.after(0, lambda: self.on_update_up_to_date(remote_ver, silent))
                        return
            except Exception as e:
                self.root.after(0, lambda: self.on_update_error(str(e), silent))

        t = threading.Thread(target=_worker, daemon=True)
        t.start()

    def on_update_found(self, data):
        new_ver = data.get("version", "1.0.0")
        if hasattr(self, 'lbl_update_status'):
            self.lbl_update_status.config(text=f"✨ Versi baru v{new_ver} tersedia!", fg="#10b981")
        self.show_update_dialog(data)

    def on_update_up_to_date(self, remote_ver, silent):
        if hasattr(self, 'lbl_update_status'):
            self.lbl_update_status.config(text=f"✓ Versi sudah paling mutakhir (v{APP_VERSION})", fg="#10b981")
        if not silent:
            messagebox.showinfo("Pembaruan Versi", f"Aplikasi ZZZleep sudah berada pada versi paling mutakhir (v{APP_VERSION}).")

    def on_update_error(self, err_msg, silent):
        if hasattr(self, 'lbl_update_status'):
            self.lbl_update_status.config(text="● Mode offline / server tidak terjangkau", fg="#94a3b8")
        if not silent:
            messagebox.showwarning("Koneksi Pembaruan", "Tidak dapat menghubungi server GitHub. Periksa koneksi internet Anda.")

    def show_update_dialog(self, data):
        """Displays a modern dark-themed modal popup with update details and changelog."""
        new_ver = data.get("version", "1.0.0")
        rel_date = data.get("release_date", "")
        changelog = data.get("changelog", [])
        dl_url = data.get("download_url", GITHUB_REPO_URL)

        dialog = tk.Toplevel(self.root)
        dialog.title("Pembaruan ZZZleep Tersedia")
        dialog.geometry("540x480")
        dialog.minsize(500, 440)
        dialog.configure(bg="#0f172a")
        dialog.transient(self.root)
        dialog.grab_set()

        # Center relative to root window
        dialog.update_idletasks()
        rx = self.root.winfo_x()
        ry = self.root.winfo_y()
        rw = self.root.winfo_width()
        rh = self.root.winfo_height()
        dx = rx + (rw - 540) // 2
        dy = ry + (rh - 480) // 2
        dialog.geometry(f"+{max(0, dx)}+{max(0, dy)}")

        # Header Box
        hdr = tk.Frame(dialog, bg="#1e293b")
        hdr.pack(fill="x")

        tk.Label(hdr, text="🚀", font=("Segoe UI Emoji", 20), bg="#1e293b").pack(side="left", padx=(20, 10), pady=16)
        h_info = tk.Frame(hdr, bg="#1e293b")
        h_info.pack(side="left", fill="y", pady=14)

        tk.Label(h_info, text="Pembaruan Baru Tersedia!", font=("Segoe UI", 12, "bold"), fg="#38bdf8", bg="#1e293b").pack(anchor="w")
        sub_text = f"Versi v{new_ver} telah dirilis ({rel_date})" if rel_date else f"Versi v{new_ver} telah dirilis"
        tk.Label(h_info, text=sub_text, font=("Segoe UI", 9), fg="#94a3b8", bg="#1e293b").pack(anchor="w")

        # Body
        body = tk.Frame(dialog, bg="#0f172a")
        body.pack(fill="both", expand=True, padx=20, pady=14)

        # Version Comparison Badge
        v_box = tk.Frame(body, bg="#1e293b", padx=14, pady=10)
        v_box.pack(fill="x", pady=(0, 12))

        tk.Label(v_box, text=f"Versi Anda: v{APP_VERSION}", font=("Segoe UI", 9, "bold"), fg="#94a3b8", bg="#1e293b").pack(side="left")
        tk.Label(v_box, text="  ➔  ", font=("Segoe UI", 10, "bold"), fg="#38bdf8", bg="#1e293b").pack(side="left")
        tk.Label(v_box, text=f"Versi Terbaru: v{new_ver}", font=("Segoe UI", 9, "bold"), fg="#10b981", bg="#1e293b").pack(side="left")

        # Changelog Header
        tk.Label(body, text="Apa saja yang baru pada versi ini:", font=("Segoe UI", 10, "bold"), fg="#f8fafc", bg="#0f172a").pack(anchor="w", pady=(0, 6))

        # Changelog List Container
        cl_box = tk.Frame(body, bg="#1e293b", padx=14, pady=12)
        cl_box.pack(fill="both", expand=True)

        if changelog:
            for item in changelog:
                row = tk.Frame(cl_box, bg="#1e293b")
                row.pack(fill="x", anchor="w", pady=3)
                tk.Label(row, text="•", font=("Segoe UI", 10, "bold"), fg="#38bdf8", bg="#1e293b").pack(side="left", anchor="n", padx=(0, 8))
                tk.Label(row, text=item, font=("Segoe UI", 9), fg="#e2e8f0", bg="#1e293b", wraplength=430, justify="left").pack(side="left", fill="x", expand=True)
        else:
            tk.Label(cl_box, text="Peningkatan performa dan pembaruan sistem.", font=("Segoe UI", 9, "italic"), fg="#94a3b8", bg="#1e293b").pack(anchor="w")

        # Footer Actions
        ftr = tk.Frame(dialog, bg="#1e293b", padx=16, pady=14)
        ftr.pack(fill="x", side="bottom")

        def _do_update():
            webbrowser.open(dl_url)
            dialog.destroy()

        btn_update = tk.Button(ftr, text="⬇ Unduh Pembaruan", font=("Segoe UI", 9, "bold"), bg="#0284c7", fg="white", activebackground="#0369a1", activeforeground="white", relief="flat", padx=16, pady=6, command=_do_update)
        btn_update.pack(side="right", padx=(8, 0))

        btn_gh = tk.Button(ftr, text="🌐 Lihat di GitHub", font=("Segoe UI", 9), bg="#334155", fg="#f8fafc", relief="flat", padx=12, pady=6, command=lambda: webbrowser.open(GITHUB_REPO_URL))
        btn_gh.pack(side="right", padx=6)

        btn_cancel = tk.Button(ftr, text="Nanti Saja", font=("Segoe UI", 9), bg="#1e293b", fg="#94a3b8", relief="flat", padx=12, pady=6, command=dialog.destroy)
        btn_cancel.pack(side="left")

    def start_background_timer(self):
        def _loop():
            last_min = ""
            while True:
                now = datetime.datetime.now()
                t_str = now.strftime("%H:%M:%S")
                hm_str = now.strftime("%H:%M")
                d_str = now.strftime("%A, %d %B %Y")

                try:
                    self.top_clock.config(text=t_str)
                    self.clock_lbl.config(text=t_str)
                    self.date_lbl.config(text=d_str)
                except Exception:
                    pass

                if hm_str != last_min:
                    last_min = hm_str
                    day_idx = (now.weekday() + 1) % 7
                    for a in self.data.get("alarms", []):
                        if a.get("enabled", True) and a.get("time") == hm_str:
                            days = a.get("days", [0, 1, 2, 3, 4, 5, 6])
                            if day_idx in days:
                                play_audio_tone(a.get("tone", "gentle"))
                                try:
                                    self.root.deiconify()
                                    self.root.lift()
                                    self.root.focus_force()
                                except Exception:
                                    pass

                if self.pomodoro_is_running and self.pomodoro_seconds_left > 0:
                    self.pomodoro_seconds_left -= 1
                    m = self.pomodoro_seconds_left // 60
                    s = self.pomodoro_seconds_left % 60
                    try:
                        self.pomo_clock.config(text=f"{m:02d}:{s:02d}")
                    except Exception:
                        pass
                    if self.pomodoro_seconds_left == 0:
                        self.pomodoro_is_running = False
                        play_audio_tone("retro")

                if self.eye_rest_is_running and self.eye_rest_seconds_left > 0:
                    self.eye_rest_seconds_left -= 1
                    m = self.eye_rest_seconds_left // 60
                    s = self.eye_rest_seconds_left % 60
                    try:
                        self.eye_clock.config(text=f"{m:02d}:{s:02d}")
                    except Exception:
                        pass
                    if self.eye_rest_seconds_left == 0:
                        self.eye_rest_seconds_left = 20 * 60
                        play_audio_tone("acoustic")

                time.sleep(1)

        t = threading.Thread(target=_loop, daemon=True)
        t.start()


def main():
    root = tk.Tk()
    app = ZzzleepDesktopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
