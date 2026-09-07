#!/usr/bin/env python3
"""
ZZZleep — Desktop Calendar, Audio Alarm & Rest Timer (v1.1.0)
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
APP_VERSION = "1.1.0"
DATA_FILE = os.path.join(os.path.expanduser("~"), ".zzzleep_desktop_data.json")
UPDATE_MANIFEST_URL = "https://raw.githubusercontent.com/InfiniteNull/ZZZleep/main/version.json"
GITHUB_REPO_URL = "https://github.com/InfiniteNull/ZZZleep"
DIRECT_EXE_URL = "https://github.com/InfiniteNull/ZZZleep/raw/main/bin/ZZZleep.exe"

# Available Synthesized Sound Tones
TONES = {
    "gentle": "Arpeggio C-Mayor (Lembut / Gentle)",
    "retro": "Digital Pulse (880Hz / 1760Hz)",
    "bell": "Harmonic Bell (Resonansi 440Hz)",
    "chime": "Ascending Chime (Melodi Naik)",
    "zen": "Zen Minimalist (520Hz Akustik)"
}

# Theme Color Definitions
THEMES = {
    "dark": {
        "bg": "#0f172a",
        "card_bg": "#1e293b",
        "subcard_bg": "#0f172a",
        "header_bg": "#1e293b",
        "text_primary": "#f8fafc",
        "text_secondary": "#94a3b8",
        "accent": "#0284c7",
        "accent_hover": "#0369a1",
        "accent_cyan": "#38bdf8",
        "border": "#334155",
        "btn_bg": "#334155",
        "btn_fg": "#f8fafc",
        "entry_bg": "#0f172a",
        "entry_fg": "#38bdf8",
        "tab_active_bg": "#0284c7",
        "tab_active_fg": "#ffffff",
        "tab_inactive_bg": "#1e293b",
        "tab_inactive_fg": "#94a3b8"
    },
    "light": {
        "bg": "#f8fafc",
        "card_bg": "#ffffff",
        "subcard_bg": "#f1f5f9",
        "header_bg": "#ffffff",
        "text_primary": "#0f172a",
        "text_secondary": "#64748b",
        "accent": "#0284c7",
        "accent_hover": "#0369a1",
        "accent_cyan": "#0284c7",
        "border": "#e2e8f0",
        "btn_bg": "#e2e8f0",
        "btn_fg": "#1e293b",
        "entry_bg": "#f1f5f9",
        "entry_fg": "#0284c7",
        "tab_active_bg": "#0284c7",
        "tab_active_fg": "#ffffff",
        "tab_inactive_bg": "#e2e8f0",
        "tab_inactive_fg": "#64748b"
    }
}

# Bilingual Translations Dictionary
I18N = {
    "id": {
        "app_title": "ZZZleep — Desktop Calendar & Audio Alarm",
        "brand": "⏰ ZZZleep",
        "local_time": "WAKTU LOKAL",
        "tab_alarms": "  ⏰ Alarm & Jadwal  ",
        "tab_timers": "  🍅 Pomodoro & Istirahat Layar  ",
        "tab_settings": "  ⚙️ Pengaturan & Pembaruan  ",
        "new_alarm": "Tambah Alarm Baru",
        "time_label": "Jam (HH:MM):",
        "title_label": "Keterangan / Label:",
        "tone_label": "Pilihan Nada Suara:",
        "btn_add_alarm": "+ Pasang Alarm",
        "btn_test_tone": "🔊 Uji Suara",
        "active_alarms": "Daftar Alarm Aktif",
        "no_alarms": "Belum ada alarm aktif.",
        "btn_active": "AKTIF",
        "btn_inactive": "NONAKTIF",
        "pomo_title": "🍅 POMODORO FOCUS TIMER",
        "btn_pomo_start": "Mulai Sesi (25m)",
        "btn_pomo_pause": "Jeda Sesi",
        "btn_pomo_resume": "Lanjutkan Sesi",
        "btn_pomo_reset": "Reset",
        "pomo_desc": "Siklus kerja fokus 25 menit diselingi istirahat 5 menit untuk menjaga konsentrasi kerja.",
        "eye_title": "👁️ PENGINGAT ISTIRAHAT MATA (20-20-20)",
        "eye_toggle_on": "Status: AKTIF (Mengingatkan Setiap Interval)",
        "eye_toggle_off": "Status: NONAKTIF (Pengingat Dimatikan)",
        "btn_eye_on": "🟢 Pengingat Aktif",
        "btn_eye_off": "🔴 Pengingat Nonaktif",
        "eye_interval_lbl": "Interval Istirahat:",
        "btn_eye_reset": "Reset Interval",
        "eye_desc": "Setiap 20 menit menatap layar monitor laptop/PC, pandang objek sejauh 6 meter (20 kaki) selama 20 detik guna mencegah ketegangan mata digital.",
        "settings_heading": "⚙️ PREFERENSI SUARA & SISTEM",
        "default_tone": "Nada Alarm Utama:",
        "app_language": "Bahasa Antarmuka:",
        "app_theme": "Tema Tampilan:",
        "theme_dark": "🌙 Mode Gelap (Dark)",
        "theme_light": "☀️ Mode Terang (Light)",
        "storage_heading": "📁 PENYIMPANAN DATA LOKAL (JSON)",
        "storage_info": (
            "1. Seluruh data preferensi & jadwal tersimpan secara lokal dalam format JSON.\n"
            "2. Generator nada alarm dihasilkan secara sintetis menggunakan modul audio bawaan.\n"
            "3. Berkas basis data dapat dicadangkan atau dipindahkan secara manual kapan saja."
        ),
        "btn_open_folder": "Buka Folder Data",
        "btn_save_json": "Simpan JSON Sekarang",
        "update_heading": "🔄 SINKRONISASI & PEMBARUAN VERSI",
        "current_ver": "Versi Aplikasi Saat Ini:",
        "btn_check_update": "🔄 Periksa Pembaruan Sekarang",
        "btn_open_repo": "🌐 Buka GitHub Repository",
        "status_ready": "● Siap memeriksa pembaruan",
        "status_checking": "⏳ Memeriksa ke GitHub...",
        "status_latest": "✓ Versi sudah paling mutakhir (v1.1.0)",
        "status_new_avail": "✨ Versi baru tersedia!",
        "status_offline": "● Mode offline / server tidak terjangkau",
        "format_err": "Masukkan format HH:MM yang valid (contoh: 07:30).",
        "saved_ok": "Pengaturan & data berhasil disimpan ke file lokal.",
        "up_to_date_msg": "Aplikasi ZZZleep sudah berada pada versi paling mutakhir (v1.1.0).",
        "conn_err_msg": "Tidak dapat menghubungi server GitHub. Periksa koneksi internet Anda."
    },
    "en": {
        "app_title": "ZZZleep — Desktop Calendar & Audio Alarm",
        "brand": "⏰ ZZZleep",
        "local_time": "LOCAL TIME",
        "tab_alarms": "  ⏰ Alarms & Schedule  ",
        "tab_timers": "  🍅 Pomodoro & Screen Rest  ",
        "tab_settings": "  ⚙️ Settings & Updates  ",
        "new_alarm": "Add New Alarm",
        "time_label": "Time (HH:MM):",
        "title_label": "Label / Description:",
        "tone_label": "Audio Tone Selection:",
        "btn_add_alarm": "+ Set Alarm",
        "btn_test_tone": "🔊 Test Tone",
        "active_alarms": "Active Alarms List",
        "no_alarms": "No active alarms yet.",
        "btn_active": "ACTIVE",
        "btn_inactive": "INACTIVE",
        "pomo_title": "🍅 POMODORO FOCUS TIMER",
        "btn_pomo_start": "Start Session (25m)",
        "btn_pomo_pause": "Pause Session",
        "btn_pomo_resume": "Resume Session",
        "btn_pomo_reset": "Reset",
        "pomo_desc": "25-minute focused work cycles followed by 5-minute breaks to maintain productivity.",
        "eye_title": "👁️ SCREEN REST REMINDER (20-20-20)",
        "eye_toggle_on": "Status: ACTIVE (Alerts Every Interval)",
        "eye_toggle_off": "Status: INACTIVE (Reminders Disabled)",
        "btn_eye_on": "🟢 Reminder Active",
        "btn_eye_off": "🔴 Reminder Inactive",
        "eye_interval_lbl": "Rest Interval:",
        "btn_eye_reset": "Reset Interval",
        "eye_desc": "Every 20 minutes looking at screens, look at an object 20 feet (6 meters) away for 20 seconds to prevent digital eye strain.",
        "settings_heading": "⚙️ AUDIO & SYSTEM PREFERENCES",
        "default_tone": "Default Alarm Tone:",
        "app_language": "Interface Language:",
        "app_theme": "UI Theme:",
        "theme_dark": "🌙 Dark Mode",
        "theme_light": "☀️ Light Mode",
        "storage_heading": "📁 LOCAL DATA STORAGE (JSON)",
        "storage_info": (
            "1. All preferences & schedules are stored locally in JSON format.\n"
            "2. Alarms are synthesized without external audio file dependencies.\n"
            "3. Data files can be backed up manually anytime."
        ),
        "btn_open_folder": "Open Data Folder",
        "btn_save_json": "Save JSON Now",
        "update_heading": "🔄 VERSION SYNC & UPDATES",
        "current_ver": "Current App Version:",
        "btn_check_update": "🔄 Check for Updates Now",
        "btn_open_repo": "🌐 Open GitHub Repository",
        "status_ready": "● Ready to check updates",
        "status_checking": "⏳ Checking GitHub...",
        "status_latest": "✓ App is up to date (v1.1.0)",
        "status_new_avail": "✨ New version available!",
        "status_offline": "● Offline mode / server unreachable",
        "format_err": "Please enter a valid HH:MM time format (e.g. 07:30).",
        "saved_ok": "Preferences & data saved to local file successfully.",
        "up_to_date_msg": "ZZZleep is already at the latest version (v1.1.0).",
        "conn_err_msg": "Unable to connect to GitHub. Please check your internet connection."
    }
}

DEFAULT_DATA = {
    "alarms": [
        {"id": "alarm-1", "title": "Bangun Pagi & Stretching", "time": "06:00", "enabled": True, "days": [1, 2, 3, 4, 5], "tone": "gentle"},
        {"id": "alarm-2", "title": "Istirahat Siang & Makan", "time": "12:00", "enabled": True, "days": [1, 2, 3, 4, 5], "tone": "retro"},
        {"id": "alarm-3", "title": "Tutup Laptop & Persiapan Tidur", "time": "22:30", "enabled": True, "days": [0, 1, 2, 3, 4, 5, 6], "tone": "bell"}
    ],
    "habits": [
        {"id": "h-1", "name": "Minum Air Putih 2L", "target": 1, "completedDays": [1, 2, 3, 4, 5]},
        {"id": "h-2", "name": "Stretching & Postur Tubuh", "target": 1, "completedDays": [1, 2, 3]},
        {"id": "h-3", "name": "Jeda Layar 20-20-20 Rutin", "target": 1, "completedDays": [1, 2, 3, 4]}
    ],
    "settings": {
        "soundTone": "gentle",
        "eyeRestEnabled": True,
        "eyeRestIntervalMin": 20,
        "language": "id",
        "theme": "dark"
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
    """Synthesizes rich harmonic beeps using native winsound."""
    if not HAS_WINSOUND:
        return

    def _beep_worker():
        try:
            if tone_type == "gentle":
                # Arpeggio C-Mayor: C5 (523Hz), E5 (659Hz), G5 (784Hz), C6 (1046Hz)
                notes = [523, 659, 784, 1046]
                for freq in notes:
                    winsound.Beep(freq, 180)
                    time.sleep(0.03)
            elif tone_type == "retro":
                for _ in range(2):
                    winsound.Beep(880, 120)
                    time.sleep(0.04)
                    winsound.Beep(1760, 160)
                    time.sleep(0.06)
            elif tone_type == "bell":
                winsound.Beep(440, 200)
                time.sleep(0.03)
                winsound.Beep(880, 350)
                time.sleep(0.03)
                winsound.Beep(1320, 200)
            elif tone_type == "chime":
                notes = [587, 659, 698, 784, 880]
                for freq in notes:
                    winsound.Beep(freq, 130)
                    time.sleep(0.02)
            elif tone_type == "zen":
                winsound.Beep(520, 220)
                time.sleep(0.05)
                winsound.Beep(520, 220)
                time.sleep(0.05)
                winsound.Beep(650, 400)
            else:
                winsound.Beep(600, 300)
        except Exception:
            pass

    t = threading.Thread(target=_beep_worker, daemon=True)
    t.start()


class ZzzleepDesktopApp:
    def __init__(self, root):
        self.root = root
        self.data = self.load_data()

        # State Variables
        settings = self.data.get("settings", {})
        self.current_lang = settings.get("language", "id")
        self.current_theme = settings.get("theme", "dark")
        self.current_tone = settings.get("soundTone", "gentle")
        self.eye_rest_enabled = settings.get("eyeRestEnabled", True)
        self.eye_interval_min = settings.get("eyeRestIntervalMin", 20)

        self.pomodoro_seconds_left = 25 * 60
        self.pomodoro_is_running = False
        self.eye_rest_seconds_left = self.eye_interval_min * 60

        # UI Setup
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("940x680")
        self.root.minsize(860, 600)

        self.apply_theme_styles()
        self.build_ui()
        self.start_background_timer()

        # Check for updates in background 2 seconds after launch
        self.root.after(2000, lambda: self.check_for_updates_async(silent=True))

    def t(self, key):
        """Helper to get translated string for current language."""
        return I18N.get(self.current_lang, I18N["id"]).get(key, key)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    d = json.load(f)
                    # Merge with default structure
                    if "settings" not in d:
                        d["settings"] = DEFAULT_DATA["settings"].copy()
                    return d
            except Exception:
                return DEFAULT_DATA.copy()
        return DEFAULT_DATA.copy()

    def save_data(self):
        try:
            self.data["settings"]["language"] = self.current_lang
            self.data["settings"]["theme"] = self.current_theme
            self.data["settings"]["soundTone"] = self.current_tone
            self.data["settings"]["eyeRestEnabled"] = self.eye_rest_enabled
            self.data["settings"]["eyeRestIntervalMin"] = self.eye_interval_min

            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Failed to save data: {e}")

    def apply_theme_styles(self):
        """Configures ttk styles matching current theme palette."""
        th = THEMES[self.current_theme]
        self.root.configure(bg=th["bg"])

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure("TNotebook", background=th["bg"], borderwidth=0)
        self.style.configure("TNotebook.Tab", background=th["tab_inactive_bg"], foreground=th["tab_inactive_fg"], padding=[16, 8], font=("Segoe UI", 10, "bold"))
        self.style.map("TNotebook.Tab",
                       background=[("selected", th["tab_active_bg"])],
                       foreground=[("selected", th["tab_active_fg"])])

        self.style.configure("TFrame", background=th["bg"])
        self.style.configure("Card.TFrame", background=th["card_bg"], relief="flat")
        self.style.configure("TLabel", background=th["bg"], foreground=th["text_primary"], font=("Segoe UI", 10))

    def toggle_language(self):
        self.current_lang = "en" if self.current_lang == "id" else "id"
        self.save_data()
        self.rebuild_full_ui()

    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.save_data()
        self.apply_theme_styles()
        self.rebuild_full_ui()

    def rebuild_full_ui(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.build_ui()

    def build_ui(self):
        th = THEMES[self.current_theme]

        # Top Header Bar
        header = tk.Frame(self.root, bg=th["header_bg"], height=58, highlightthickness=1, highlightbackground=th["border"])
        header.pack(fill="x", side="top")

        # Brand & Version
        brand_box = tk.Frame(header, bg=th["header_bg"])
        brand_box.pack(side="left", padx=16, pady=10)

        tk.Label(brand_box, text=self.t("brand"), font=("Segoe UI", 13, "bold"), fg=th["accent_cyan"], bg=th["header_bg"]).pack(side="left")
        tk.Label(brand_box, text=f"v{APP_VERSION}", font=("Consolas", 9, "bold"), fg=th["text_secondary"], bg=th["subcard_bg"], padx=6, pady=2).pack(side="left", padx=8)

        # Header Right Controls (Theme, Language, Clock)
        ctrl_box = tk.Frame(header, bg=th["header_bg"])
        ctrl_box.pack(side="right", padx=16)

        # Language Toggle Button
        lang_text = "🌐 ID" if self.current_lang == "id" else "🌐 EN"
        btn_lang = tk.Button(ctrl_box, text=lang_text, font=("Segoe UI", 9, "bold"), bg=th["btn_bg"], fg=th["text_primary"], activebackground=th["accent"], activeforeground="white", relief="flat", padx=8, pady=3, command=self.toggle_language)
        btn_lang.pack(side="left", padx=4)

        # Theme Toggle Button
        theme_icon = "🌙" if self.current_theme == "dark" else "☀️"
        btn_theme = tk.Button(ctrl_box, text=theme_icon, font=("Segoe UI", 9, "bold"), bg=th["btn_bg"], fg=th["text_primary"], activebackground=th["accent"], activeforeground="white", relief="flat", padx=8, pady=3, command=self.toggle_theme)
        btn_theme.pack(side="left", padx=4)

        # Top Clock
        self.top_clock = tk.Label(ctrl_box, text="--:--:--", font=("Consolas", 12, "bold"), fg=th["text_primary"], bg=th["header_bg"])
        self.top_clock.pack(side="left", padx=(10, 0))

        # Main Notebook Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=10)

        # Tab 1: Alarms
        tab_alarms = ttk.Frame(self.notebook)
        self.notebook.add(tab_alarms, text=self.t("tab_alarms"))
        self.build_alarms_tab(tab_alarms)

        # Tab 2: Timers & Eye Rest
        tab_timers = ttk.Frame(self.notebook)
        self.notebook.add(tab_timers, text=self.t("tab_timers"))
        self.build_timers_tab(tab_timers)

        # Tab 3: Settings, Data & Updates
        tab_settings = ttk.Frame(self.notebook)
        self.notebook.add(tab_settings, text=self.t("tab_settings"))
        self.build_settings_tab(tab_settings)

    def build_alarms_tab(self, parent):
        th = THEMES[self.current_theme]
        container = tk.Frame(parent, bg=th["bg"])
        container.pack(fill="both", expand=True, padx=6, pady=6)

        # Left Column (Clock & Add Form)
        left = tk.Frame(container, bg=th["card_bg"], width=330, highlightthickness=1, highlightbackground=th["border"])
        left.pack(side="left", fill="y", padx=6, pady=6)
        left.pack_propagate(False)

        tk.Label(left, text=self.t("local_time"), font=("Segoe UI", 8, "bold"), fg=th["text_secondary"], bg=th["card_bg"]).pack(anchor="w", padx=16, pady=(16, 2))
        self.clock_lbl = tk.Label(left, text="00:00:00", font=("Consolas", 26, "bold"), fg=th["accent_cyan"], bg=th["card_bg"])
        self.clock_lbl.pack(anchor="w", padx=16)
        self.date_lbl = tk.Label(left, text="Loading...", font=("Segoe UI", 10), fg=th["text_secondary"], bg=th["card_bg"])
        self.date_lbl.pack(anchor="w", padx=16, pady=(0, 14))

        tk.Frame(left, height=1, bg=th["border"]).pack(fill="x", padx=16, pady=4)

        tk.Label(left, text=self.t("new_alarm"), font=("Segoe UI", 11, "bold"), fg=th["text_primary"], bg=th["card_bg"]).pack(anchor="w", padx=16, pady=(8, 4))

        # Time Input
        tk.Label(left, text=self.t("time_label"), font=("Segoe UI", 9), fg=th["text_secondary"], bg=th["card_bg"]).pack(anchor="w", padx=16, pady=(4, 2))
        self.entry_time = tk.Entry(left, font=("Consolas", 12), bg=th["entry_bg"], fg=th["entry_fg"], insertbackground=th["entry_fg"], relief="flat", highlightthickness=1, highlightbackground=th["border"])
        self.entry_time.insert(0, "07:30")
        self.entry_time.pack(fill="x", padx=16, ipady=4)

        # Title Input
        tk.Label(left, text=self.t("title_label"), font=("Segoe UI", 9), fg=th["text_secondary"], bg=th["card_bg"]).pack(anchor="w", padx=16, pady=(6, 2))
        self.entry_title = tk.Entry(left, font=("Segoe UI", 10), bg=th["entry_bg"], fg=th["text_primary"], insertbackground=th["entry_fg"], relief="flat", highlightthickness=1, highlightbackground=th["border"])
        self.entry_title.insert(0, "Mulai Kerja Pagi" if self.current_lang == "id" else "Morning Deep Work")
        self.entry_title.pack(fill="x", padx=16, ipady=4)

        # Sound Tone Selector
        tk.Label(left, text=self.t("tone_label"), font=("Segoe UI", 9), fg=th["text_secondary"], bg=th["card_bg"]).pack(anchor="w", padx=16, pady=(6, 2))
        
        self.var_alarm_tone = tk.StringVar(value=self.current_tone)
        tone_box = tk.Frame(left, bg=th["card_bg"])
        tone_box.pack(fill="x", padx=16)

        tone_options = list(TONES.keys())
        self.combo_tone = ttk.Combobox(tone_box, textvariable=self.var_alarm_tone, values=tone_options, state="readonly", font=("Segoe UI", 9))
        self.combo_tone.pack(side="left", fill="x", expand=True)

        btn_test_mini = tk.Button(tone_box, text="🔊", font=("Segoe UI", 9, "bold"), bg=th["btn_bg"], fg=th["text_primary"], relief="flat", padx=6, command=lambda: play_audio_tone(self.var_alarm_tone.get()))
        btn_test_mini.pack(side="right", padx=(4, 0))

        # Buttons
        btn_add = tk.Button(left, text=self.t("btn_add_alarm"), font=("Segoe UI", 10, "bold"), bg=th["accent"], fg="white", activebackground=th["accent_hover"], activeforeground="white", relief="flat", command=self.add_alarm)
        btn_add.pack(fill="x", padx=16, pady=(16, 6), ipady=5)

        # Right Column (List of Alarms)
        right = tk.Frame(container, bg=th["card_bg"], highlightthickness=1, highlightbackground=th["border"])
        right.pack(side="right", fill="both", expand=True, padx=6, pady=6)

        header_r = tk.Frame(right, bg=th["card_bg"])
        header_r.pack(fill="x", padx=16, pady=12)
        tk.Label(header_r, text=self.t("active_alarms"), font=("Segoe UI", 12, "bold"), fg=th["text_primary"], bg=th["card_bg"]).pack(side="left")

        self.alarms_frame = tk.Frame(right, bg=th["card_bg"])
        self.alarms_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        self.refresh_alarms()

    def refresh_alarms(self):
        th = THEMES[self.current_theme]
        for w in self.alarms_frame.winfo_children():
            w.destroy()

        alarms = self.data.get("alarms", [])
        if not alarms:
            tk.Label(self.alarms_frame, text=self.t("no_alarms"), fg=th["text_secondary"], bg=th["card_bg"], font=("Segoe UI", 10, "italic")).pack(pady=30)
            return

        for a in alarms:
            card = tk.Frame(self.alarms_frame, bg=th["subcard_bg"], relief="flat", highlightthickness=1, highlightbackground=th["border"])
            card.pack(fill="x", pady=4)

            left_box = tk.Frame(card, bg=th["subcard_bg"])
            left_box.pack(side="left", padx=12, pady=8)

            time_col = th["accent_cyan"] if a.get("enabled", True) else th["text_secondary"]
            tk.Label(left_box, text=a["time"], font=("Consolas", 18, "bold"), fg=time_col, bg=th["subcard_bg"]).pack(anchor="w")
            
            label_text = a.get("title", "Alarm")
            tone_name = a.get("tone", "gentle")
            tk.Label(left_box, text=f"{label_text}  •  🎵 {tone_name}", font=("Segoe UI", 9, "bold" if a.get("enabled", True) else "normal"), fg=th["text_primary"] if a.get("enabled", True) else th["text_secondary"], bg=th["subcard_bg"]).pack(anchor="w")

            right_box = tk.Frame(card, bg=th["subcard_bg"])
            right_box.pack(side="right", padx=12, pady=8)

            st_text = self.t("btn_active") if a.get("enabled", True) else self.t("btn_inactive")
            st_bg = "#059669" if a.get("enabled", True) else "#64748b"
            t_btn = tk.Button(right_box, text=st_text, font=("Segoe UI", 8, "bold"), bg=st_bg, fg="white", relief="flat", padx=8, pady=3, command=lambda item=a: self.toggle_alarm(item))
            t_btn.pack(side="left", padx=4)

            btn_test_alarm = tk.Button(right_box, text="🔊", font=("Segoe UI", 8, "bold"), bg=th["btn_bg"], fg=th["text_primary"], relief="flat", padx=6, pady=3, command=lambda item=a: play_audio_tone(item.get("tone", "gentle")))
            btn_test_alarm.pack(side="left", padx=4)

            d_btn = tk.Button(right_box, text="✕", font=("Segoe UI", 8, "bold"), bg="#dc2626", fg="white", relief="flat", padx=6, pady=3, command=lambda a_id=a["id"]: self.delete_alarm(a_id))
            d_btn.pack(side="left", padx=4)

    def add_alarm(self):
        t_str = self.entry_time.get().strip()
        title = self.entry_title.get().strip() or "Alarm"
        tone = self.var_alarm_tone.get()

        try:
            parts = t_str.split(":")
            h, m = int(parts[0]), int(parts[1])
            if not (0 <= h < 24 and 0 <= m < 60):
                raise ValueError
            valid_time = f"{h:02d}:{m:02d}"
        except Exception:
            messagebox.showerror("Format Error", self.t("format_err"))
            return

        new_a = {
            "id": f"alarm-{int(time.time()*1000)}",
            "title": title,
            "time": valid_time,
            "enabled": True,
            "days": [0, 1, 2, 3, 4, 5, 6],
            "tone": tone
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
        th = THEMES[self.current_theme]
        container = tk.Frame(parent, bg=th["bg"])
        container.pack(fill="both", expand=True, padx=6, pady=6)

        # Left: Pomodoro Card
        pomo = tk.Frame(container, bg=th["card_bg"], highlightthickness=1, highlightbackground=th["border"])
        pomo.pack(side="left", fill="both", expand=True, padx=6, pady=6)

        tk.Label(pomo, text=self.t("pomo_title"), font=("Segoe UI", 12, "bold"), fg="#f43f5e", bg=th["card_bg"]).pack(pady=(20, 10))
        self.pomo_clock = tk.Label(pomo, text="25:00", font=("Consolas", 42, "bold"), fg=th["text_primary"], bg=th["card_bg"])
        self.pomo_clock.pack(pady=10)

        pomo_btns = tk.Frame(pomo, bg=th["card_bg"])
        pomo_btns.pack(pady=12)

        self.btn_pomo = tk.Button(pomo_btns, text=self.t("btn_pomo_start"), font=("Segoe UI", 10, "bold"), bg="#f43f5e", fg="white", relief="flat", padx=14, pady=6, command=self.toggle_pomodoro)
        self.btn_pomo.pack(side="left", padx=6)

        btn_pomo_r = tk.Button(pomo_btns, text=self.t("btn_pomo_reset"), font=("Segoe UI", 10), bg=th["btn_bg"], fg=th["text_primary"], relief="flat", padx=10, pady=6, command=self.reset_pomodoro)
        btn_pomo_r.pack(side="left", padx=6)

        tk.Label(pomo, text=self.t("pomo_desc"), font=("Segoe UI", 9), fg=th["text_secondary"], bg=th["card_bg"], justify="center", wraplength=320).pack(pady=16)

        # Right: Eye Rest Card (With Toggle & Interval Selector)
        eye = tk.Frame(container, bg=th["card_bg"], highlightthickness=1, highlightbackground=th["border"])
        eye.pack(side="right", fill="both", expand=True, padx=6, pady=6)

        tk.Label(eye, text=self.t("eye_title"), font=("Segoe UI", 12, "bold"), fg="#10b981", bg=th["card_bg"]).pack(pady=(20, 8))
        
        # Status Label
        st_txt = self.t("eye_toggle_on") if self.eye_rest_enabled else self.t("eye_toggle_off")
        st_fg = "#10b981" if self.eye_rest_enabled else "#ef4444"
        self.lbl_eye_status = tk.Label(eye, text=st_txt, font=("Segoe UI", 9, "bold"), fg=st_fg, bg=th["card_bg"])
        self.lbl_eye_status.pack(pady=(0, 4))

        self.eye_clock = tk.Label(eye, text=f"{self.eye_interval_min:02d}:00", font=("Consolas", 42, "bold"), fg=th["text_primary"] if self.eye_rest_enabled else th["text_secondary"], bg=th["card_bg"])
        self.eye_clock.pack(pady=6)

        eye_btns = tk.Frame(eye, bg=th["card_bg"])
        eye_btns.pack(pady=10)

        # ON/OFF Toggle Button
        toggle_btn_txt = self.t("btn_eye_on") if self.eye_rest_enabled else self.t("btn_eye_off")
        toggle_btn_bg = "#10b981" if self.eye_rest_enabled else "#64748b"
        self.btn_eye_toggle = tk.Button(eye_btns, text=toggle_btn_txt, font=("Segoe UI", 10, "bold"), bg=toggle_btn_bg, fg="white", relief="flat", padx=12, pady=6, command=self.toggle_eye_rest_enabled)
        self.btn_eye_toggle.pack(side="left", padx=4)

        btn_eye_r = tk.Button(eye_btns, text=self.t("btn_eye_reset"), font=("Segoe UI", 10), bg=th["btn_bg"], fg=th["text_primary"], relief="flat", padx=10, pady=6, command=self.reset_eye_rest)
        btn_eye_r.pack(side="left", padx=4)

        # Interval Options
        interval_frame = tk.Frame(eye, bg=th["card_bg"])
        interval_frame.pack(pady=6)
        tk.Label(interval_frame, text=self.t("eye_interval_lbl"), font=("Segoe UI", 9), fg=th["text_secondary"], bg=th["card_bg"]).pack(side="left", padx=4)

        for mins in [15, 20, 30, 45]:
            act = (mins == self.eye_interval_min)
            b_bg = th["accent"] if act else th["btn_bg"]
            b_fg = "white" if act else th["text_primary"]
            btn_int = tk.Button(interval_frame, text=f"{mins}m", font=("Segoe UI", 8, "bold" if act else "normal"), bg=b_bg, fg=b_fg, relief="flat", padx=6, pady=2, command=lambda m=mins: self.set_eye_interval(m))
            btn_int.pack(side="left", padx=2)

        tk.Label(eye, text=self.t("eye_desc"), font=("Segoe UI", 9), fg=th["text_secondary"], bg=th["card_bg"], justify="center", wraplength=340).pack(pady=14)

    def toggle_pomodoro(self):
        self.pomodoro_is_running = not self.pomodoro_is_running
        if self.pomodoro_is_running:
            self.btn_pomo.config(text=self.t("btn_pomo_pause"), bg="#d97706")
        else:
            self.btn_pomo.config(text=self.t("btn_pomo_resume"), bg="#f43f5e")

    def reset_pomodoro(self):
        self.pomodoro_is_running = False
        self.pomodoro_seconds_left = 25 * 60
        self.btn_pomo.config(text=self.t("btn_pomo_start"), bg="#f43f5e")
        self.pomo_clock.config(text="25:00")

    def toggle_eye_rest_enabled(self):
        self.eye_rest_enabled = not self.eye_rest_enabled
        self.save_data()
        th = THEMES[self.current_theme]
        
        st_txt = self.t("eye_toggle_on") if self.eye_rest_enabled else self.t("eye_toggle_off")
        st_fg = "#10b981" if self.eye_rest_enabled else "#ef4444"
        self.lbl_eye_status.config(text=st_txt, fg=st_fg)

        toggle_btn_txt = self.t("btn_eye_on") if self.eye_rest_enabled else self.t("btn_eye_off")
        toggle_btn_bg = "#10b981" if self.eye_rest_enabled else "#64748b"
        self.btn_eye_toggle.config(text=toggle_btn_txt, bg=toggle_btn_bg)

        self.eye_clock.config(fg=th["text_primary"] if self.eye_rest_enabled else th["text_secondary"])

    def set_eye_interval(self, mins):
        self.eye_interval_min = mins
        self.eye_rest_seconds_left = mins * 60
        self.save_data()
        self.rebuild_full_ui()

    def reset_eye_rest(self):
        self.eye_rest_seconds_left = self.eye_interval_min * 60
        self.eye_clock.config(text=f"{self.eye_interval_min:02d}:00")

    def build_settings_tab(self, parent):
        th = THEMES[self.current_theme]
        container = tk.Frame(parent, bg=th["bg"])
        container.pack(fill="both", expand=True, padx=6, pady=6)

        # 1. Preferences Card
        pref_card = tk.Frame(container, bg=th["card_bg"], highlightthickness=1, highlightbackground=th["border"])
        pref_card.pack(fill="x", padx=6, pady=(0, 8))

        tk.Label(pref_card, text=self.t("settings_heading"), font=("Segoe UI", 12, "bold"), fg=th["accent_cyan"], bg=th["card_bg"]).pack(anchor="w", padx=20, pady=(14, 8))

        pref_grid = tk.Frame(pref_card, bg=th["card_bg"])
        pref_grid.pack(fill="x", padx=20, pady=(0, 14))

        # Default Tone Selector
        tk.Label(pref_grid, text=self.t("default_tone"), font=("Segoe UI", 9, "bold"), fg=th["text_primary"], bg=th["card_bg"]).grid(row=0, column=0, sticky="w", pady=6)
        
        self.var_def_tone = tk.StringVar(value=self.current_tone)
        combo_def = ttk.Combobox(pref_grid, textvariable=self.var_def_tone, values=list(TONES.keys()), state="readonly", font=("Segoe UI", 9), width=18)
        combo_def.grid(row=0, column=1, sticky="w", padx=10, pady=6)
        combo_def.bind("<<ComboboxSelected>>", lambda e: self.on_change_default_tone())

        btn_test_def = tk.Button(pref_grid, text="🔊 " + self.t("btn_test_tone"), font=("Segoe UI", 9), bg=th["btn_bg"], fg=th["text_primary"], relief="flat", padx=10, command=lambda: play_audio_tone(self.var_def_tone.get()))
        btn_test_def.grid(row=0, column=2, sticky="w", padx=4, pady=6)

        # Language Selector
        tk.Label(pref_grid, text=self.t("app_language"), font=("Segoe UI", 9, "bold"), fg=th["text_primary"], bg=th["card_bg"]).grid(row=1, column=0, sticky="w", pady=6)
        
        lang_box = tk.Frame(pref_grid, bg=th["card_bg"])
        lang_box.grid(row=1, column=1, sticky="w", padx=10, pady=6)

        btn_l_id = tk.Button(lang_box, text="Bahasa Indonesia", font=("Segoe UI", 8, "bold" if self.current_lang == "id" else "normal"), bg=th["accent"] if self.current_lang == "id" else th["btn_bg"], fg="white" if self.current_lang == "id" else th["text_primary"], relief="flat", padx=8, pady=2, command=lambda: self.set_language("id"))
        btn_l_id.pack(side="left", padx=(0, 4))

        btn_l_en = tk.Button(lang_box, text="English", font=("Segoe UI", 8, "bold" if self.current_lang == "en" else "normal"), bg=th["accent"] if self.current_lang == "en" else th["btn_bg"], fg="white" if self.current_lang == "en" else th["text_primary"], relief="flat", padx=8, pady=2, command=lambda: self.set_language("en"))
        btn_l_en.pack(side="left")

        # Theme Selector
        tk.Label(pref_grid, text=self.t("app_theme"), font=("Segoe UI", 9, "bold"), fg=th["text_primary"], bg=th["card_bg"]).grid(row=2, column=0, sticky="w", pady=6)
        
        thm_box = tk.Frame(pref_grid, bg=th["card_bg"])
        thm_box.grid(row=2, column=1, sticky="w", padx=10, pady=6)

        btn_th_dark = tk.Button(thm_box, text=self.t("theme_dark"), font=("Segoe UI", 8, "bold" if self.current_theme == "dark" else "normal"), bg=th["accent"] if self.current_theme == "dark" else th["btn_bg"], fg="white" if self.current_theme == "dark" else th["text_primary"], relief="flat", padx=8, pady=2, command=lambda: self.set_theme("dark"))
        btn_th_dark.pack(side="left", padx=(0, 4))

        btn_th_light = tk.Button(thm_box, text=self.t("theme_light"), font=("Segoe UI", 8, "bold" if self.current_theme == "light" else "normal"), bg=th["accent"] if self.current_theme == "light" else th["btn_bg"], fg="white" if self.current_theme == "light" else th["text_primary"], relief="flat", padx=8, pady=2, command=lambda: self.set_theme("light"))
        btn_th_light.pack(side="left")

        # 2. Local Storage Card
        card = tk.Frame(container, bg=th["card_bg"], highlightthickness=1, highlightbackground=th["border"])
        card.pack(fill="x", padx=6, pady=(0, 8))

        tk.Label(card, text=self.t("storage_heading"), font=("Segoe UI", 12, "bold"), fg=th["accent_cyan"], bg=th["card_bg"]).pack(anchor="w", padx=20, pady=(12, 2))
        tk.Label(card, text=f"File: {DATA_FILE}", font=("Consolas", 9), fg=th["text_secondary"], bg=th["card_bg"]).pack(anchor="w", padx=20, pady=(0, 6))

        tk.Label(card, text=self.t("storage_info"), font=("Segoe UI", 9), fg=th["text_primary"], bg=th["card_bg"], justify="left").pack(anchor="w", padx=20, pady=2)

        btn_box = tk.Frame(card, bg=th["card_bg"])
        btn_box.pack(anchor="w", padx=20, pady=(8, 14))

        btn_open = tk.Button(btn_box, text=self.t("btn_open_folder"), font=("Segoe UI", 9, "bold"), bg=th["accent"], fg="white", relief="flat", padx=12, pady=5, command=lambda: os.system(f'explorer /select,"{DATA_FILE}"'))
        btn_open.pack(side="left", padx=(0, 8))

        btn_save = tk.Button(btn_box, text=self.t("btn_save_json"), font=("Segoe UI", 9), bg=th["btn_bg"], fg=th["text_primary"], relief="flat", padx=12, pady=5, command=self.save_data_with_feedback)
        btn_save.pack(side="left", padx=8)

        # 3. Update & Version Sync Card
        up_card = tk.Frame(container, bg=th["card_bg"], highlightthickness=1, highlightbackground=th["border"])
        up_card.pack(fill="both", expand=True, padx=6, pady=(0, 6))

        tk.Label(up_card, text=self.t("update_heading"), font=("Segoe UI", 12, "bold"), fg="#10b981", bg=th["card_bg"]).pack(anchor="w", padx=20, pady=(12, 2))
        
        up_meta = tk.Frame(up_card, bg=th["card_bg"])
        up_meta.pack(fill="x", padx=20, pady=4)
        
        tk.Label(up_meta, text=f"{self.t('current_ver')} v{APP_VERSION}", font=("Segoe UI", 10, "bold"), fg=th["text_primary"], bg=th["card_bg"]).pack(side="left")
        
        self.lbl_update_status = tk.Label(up_meta, text=self.t("status_ready"), font=("Segoe UI", 9), fg=th["text_secondary"], bg=th["card_bg"])
        self.lbl_update_status.pack(side="left", padx=14)

        up_btn_box = tk.Frame(up_card, bg=th["card_bg"])
        up_btn_box.pack(anchor="w", padx=20, pady=(8, 14))

        self.btn_check_update = tk.Button(up_btn_box, text=self.t("btn_check_update"), font=("Segoe UI", 9, "bold"), bg="#059669", fg="white", activebackground="#047857", activeforeground="white", relief="flat", padx=14, pady=6, command=lambda: self.check_for_updates_async(silent=False))
        self.btn_check_update.pack(side="left", padx=(0, 8))

        btn_repo = tk.Button(up_btn_box, text=self.t("btn_open_repo"), font=("Segoe UI", 9), bg=th["btn_bg"], fg=th["text_primary"], relief="flat", padx=12, pady=6, command=lambda: webbrowser.open(GITHUB_REPO_URL))
        btn_repo.pack(side="left", padx=8)

    def on_change_default_tone(self):
        self.current_tone = self.var_def_tone.get()
        self.save_data()

    def set_language(self, lang):
        self.current_lang = lang
        self.save_data()
        self.rebuild_full_ui()

    def set_theme(self, th_name):
        self.current_theme = th_name
        self.save_data()
        self.apply_theme_styles()
        self.rebuild_full_ui()

    def save_data_with_feedback(self):
        self.save_data()
        messagebox.showinfo("ZZZleep", self.t("saved_ok"))

    def check_for_updates_async(self, silent=True):
        """Asynchronously checks version.json from GitHub."""
        if hasattr(self, 'lbl_update_status'):
            self.lbl_update_status.config(text=self.t("status_checking"), fg="#38bdf8")

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
                        remote_ver = data.get("version", "1.1.0")
                        
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
        new_ver = data.get("version", "1.1.0")
        if hasattr(self, 'lbl_update_status'):
            self.lbl_update_status.config(text=f"{self.t('status_new_avail')} (v{new_ver})", fg="#10b981")
        self.show_update_dialog(data)

    def on_update_up_to_date(self, remote_ver, silent):
        if hasattr(self, 'lbl_update_status'):
            self.lbl_update_status.config(text=self.t("status_latest"), fg="#10b981")
        if not silent:
            messagebox.showinfo("Pembaruan Versi", self.t("up_to_date_msg"))

    def on_update_error(self, err_msg, silent):
        if hasattr(self, 'lbl_update_status'):
            self.lbl_update_status.config(text=self.t("status_offline"), fg="#94a3b8")
        if not silent:
            messagebox.showwarning("Koneksi Pembaruan", self.t("conn_err_msg"))

    def show_update_dialog(self, data):
        """Displays a modern modal popup with update details and changelog."""
        new_ver = data.get("version", "1.1.0")
        rel_date = data.get("release_date", "")
        changelog = data.get("changelog", [])
        dl_url = data.get("download_url", DIRECT_EXE_URL)

        th = THEMES[self.current_theme]
        dialog = tk.Toplevel(self.root)
        dialog.title("Pembaruan ZZZleep Tersedia" if self.current_lang == "id" else "ZZZleep Update Available")
        dialog.geometry("540x490")
        dialog.minsize(500, 450)
        dialog.configure(bg=th["bg"])
        dialog.transient(self.root)
        dialog.grab_set()

        # Center relative to root window
        dialog.update_idletasks()
        rx = self.root.winfo_x()
        ry = self.root.winfo_y()
        rw = self.root.winfo_width()
        rh = self.root.winfo_height()
        dx = rx + (rw - 540) // 2
        dy = ry + (rh - 490) // 2
        dialog.geometry(f"+{max(0, dx)}+{max(0, dy)}")

        # Header Box
        hdr = tk.Frame(dialog, bg=th["card_bg"], highlightthickness=1, highlightbackground=th["border"])
        hdr.pack(fill="x")

        tk.Label(hdr, text="🚀", font=("Segoe UI Emoji", 20), bg=th["card_bg"]).pack(side="left", padx=(20, 10), pady=16)
        h_info = tk.Frame(hdr, bg=th["card_bg"])
        h_info.pack(side="left", fill="y", pady=14)

        title_text = "Pembaruan Baru Tersedia!" if self.current_lang == "id" else "New Version Available!"
        tk.Label(h_info, text=title_text, font=("Segoe UI", 12, "bold"), fg=th["accent_cyan"], bg=th["card_bg"]).pack(anchor="w")
        sub_text = f"Versi v{new_ver} telah dirilis ({rel_date})" if self.current_lang == "id" else f"Version v{new_ver} released ({rel_date})"
        tk.Label(h_info, text=sub_text, font=("Segoe UI", 9), fg=th["text_secondary"], bg=th["card_bg"]).pack(anchor="w")

        # Body
        body = tk.Frame(dialog, bg=th["bg"])
        body.pack(fill="both", expand=True, padx=20, pady=14)

        # Version Comparison Badge
        v_box = tk.Frame(body, bg=th["card_bg"], padx=14, pady=10, highlightthickness=1, highlightbackground=th["border"])
        v_box.pack(fill="x", pady=(0, 12))

        cur_lbl = f"Versi Anda: v{APP_VERSION}" if self.current_lang == "id" else f"Your Version: v{APP_VERSION}"
        new_lbl = f"Versi Terbaru: v{new_ver}" if self.current_lang == "id" else f"Latest Version: v{new_ver}"
        tk.Label(v_box, text=cur_lbl, font=("Segoe UI", 9, "bold"), fg=th["text_secondary"], bg=th["card_bg"]).pack(side="left")
        tk.Label(v_box, text="  ➔  ", font=("Segoe UI", 10, "bold"), fg=th["accent_cyan"], bg=th["card_bg"]).pack(side="left")
        tk.Label(v_box, text=new_lbl, font=("Segoe UI", 9, "bold"), fg="#10b981", bg=th["card_bg"]).pack(side="left")

        # Changelog Header
        cl_head = "Apa saja yang baru pada versi ini:" if self.current_lang == "id" else "What's new in this update:"
        tk.Label(body, text=cl_head, font=("Segoe UI", 10, "bold"), fg=th["text_primary"], bg=th["bg"]).pack(anchor="w", pady=(0, 6))

        # Changelog List Container
        cl_box = tk.Frame(body, bg=th["card_bg"], padx=14, pady=12, highlightthickness=1, highlightbackground=th["border"])
        cl_box.pack(fill="both", expand=True)

        if changelog:
            for item in changelog:
                row = tk.Frame(cl_box, bg=th["card_bg"])
                row.pack(fill="x", anchor="w", pady=3)
                tk.Label(row, text="•", font=("Segoe UI", 10, "bold"), fg=th["accent_cyan"], bg=th["card_bg"]).pack(side="left", anchor="n", padx=(0, 8))
                tk.Label(row, text=item, font=("Segoe UI", 9), fg=th["text_primary"], bg=th["card_bg"], wraplength=430, justify="left").pack(side="left", fill="x", expand=True)
        else:
            tk.Label(cl_box, text="Peningkatan stabilitas dan fitur baru.", font=("Segoe UI", 9, "italic"), fg=th["text_secondary"], bg=th["card_bg"]).pack(anchor="w")

        # Footer Actions
        ftr = tk.Frame(dialog, bg=th["card_bg"], padx=16, pady=14, highlightthickness=1, highlightbackground=th["border"])
        ftr.pack(fill="x", side="bottom")

        def _do_update():
            webbrowser.open(dl_url)
            dialog.destroy()

        btn_up_txt = "⬇ Unduh Pembaruan" if self.current_lang == "id" else "⬇ Download Update"
        btn_update = tk.Button(ftr, text=btn_up_txt, font=("Segoe UI", 9, "bold"), bg=th["accent"], fg="white", activebackground=th["accent_hover"], activeforeground="white", relief="flat", padx=16, pady=6, command=_do_update)
        btn_update.pack(side="right", padx=(8, 0))

        btn_gh_txt = "🌐 Lihat di GitHub" if self.current_lang == "id" else "🌐 View on GitHub"
        btn_gh = tk.Button(ftr, text=btn_gh_txt, font=("Segoe UI", 9), bg=th["btn_bg"], fg=th["text_primary"], relief="flat", padx=12, pady=6, command=lambda: webbrowser.open(GITHUB_REPO_URL))
        btn_gh.pack(side="right", padx=6)

        btn_can_txt = "Nanti Saja" if self.current_lang == "id" else "Later"
        btn_cancel = tk.Button(ftr, text=btn_can_txt, font=("Segoe UI", 9), bg=th["card_bg"], fg=th["text_secondary"], relief="flat", padx=12, pady=6, command=dialog.destroy)
        btn_cancel.pack(side="left")

    def start_background_timer(self):
        def _loop():
            last_min = ""
            while True:
                now = datetime.datetime.now()
                t_str = now.strftime("%H:%M:%S")
                hm_str = now.strftime("%H:%M")
                
                # Bilingual Date Formatter
                if self.current_lang == "id":
                    days_id = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
                    months_id = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    d_str = f"{days_id[now.weekday()]}, {now.day} {months_id[now.month-1]} {now.year}"
                else:
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
                                play_audio_tone(a.get("tone", self.current_tone))
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
                        play_audio_tone(self.current_tone)

                if self.eye_rest_enabled and self.eye_rest_seconds_left > 0:
                    self.eye_rest_seconds_left -= 1
                    m = self.eye_rest_seconds_left // 60
                    s = self.eye_rest_seconds_left % 60
                    try:
                        self.eye_clock.config(text=f"{m:02d}:{s:02d}")
                    except Exception:
                        pass
                    if self.eye_rest_seconds_left == 0:
                        self.eye_rest_seconds_left = self.eye_interval_min * 60
                        play_audio_tone("bell")

                time.sleep(1)

        t = threading.Thread(target=_loop, daemon=True)
        t.start()


def main():
    root = tk.Tk()
    app = ZzzleepDesktopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
