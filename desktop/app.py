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
import calendar
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
    "gentle": "Arpeggio C-Mayor",
    "retro": "Digital Pulse (880/1760Hz)",
    "bell": "Harmonic Bell (440Hz)",
    "chime": "Ascending Chime (D-A)",
    "zen": "Zen Minimalist (520Hz)"
}

# Day Names
DAY_NAMES_ID = ["Min", "Sen", "Sel", "Rab", "Kam", "Jum", "Sab"]
DAY_NAMES_EN = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

# Theme Color Definitions
THEMES = {
    "dark": {
        "bg": "#0b0f19",
        "sidebar_bg": "#0f172a",
        "card_bg": "#1e293b",
        "subcard_bg": "#111827",
        "ring_bg": "#334155",
        "text_primary": "#f8fafc",
        "text_secondary": "#94a3b8",
        "accent": "#0284c7",
        "accent_hover": "#0369a1",
        "accent_cyan": "#38bdf8",
        "border": "#1e293b",
        "border_subtle": "#334155",
        "btn_bg": "#334155",
        "btn_fg": "#f8fafc",
        "entry_bg": "#0f172a",
        "entry_fg": "#38bdf8",
        "nav_active_bg": "#0284c7",
        "nav_active_fg": "#ffffff",
        "nav_inactive_bg": "#0f172a",
        "nav_inactive_fg": "#94a3b8",
        "ring_pomo": "#f43f5e",
        "ring_eye": "#10b981"
    },
    "light": {
        "bg": "#f1f5f9",
        "sidebar_bg": "#ffffff",
        "card_bg": "#ffffff",
        "subcard_bg": "#f8fafc",
        "ring_bg": "#e2e8f0",
        "text_primary": "#0f172a",
        "text_secondary": "#64748b",
        "accent": "#0284c7",
        "accent_hover": "#0369a1",
        "accent_cyan": "#0284c7",
        "border": "#e2e8f0",
        "border_subtle": "#cbd5e1",
        "btn_bg": "#e2e8f0",
        "btn_fg": "#1e293b",
        "entry_bg": "#f8fafc",
        "entry_fg": "#0284c7",
        "nav_active_bg": "#0284c7",
        "nav_active_fg": "#ffffff",
        "nav_inactive_bg": "#ffffff",
        "nav_inactive_fg": "#64748b",
        "ring_pomo": "#e11d48",
        "ring_eye": "#059669"
    }
}

# Bilingual Translations Dictionary
I18N = {
    "id": {
        "app_title": "ZZZleep — Desktop Calendar & Audio Alarm",
        "brand": "⏰ ZZZleep",
        "nav_alarms": "⏰  Alarm & Jadwal",
        "nav_timers": "🍅  Timer & Layar",
        "nav_settings": "⚙️  Pengaturan & Data",
        "nav_hub": "🌐  Hub Portofolio",
        "local_time": "WAKTU LOKAL",
        "monthly_calendar": "KALENDER BULANAN",
        "new_alarm": "Tambah Alarm Baru",
        "time_picker": "Waktu Alarm (Jam : Menit):",
        "quick_presets": "Waktu Cepat:",
        "title_label": "Keterangan / Label:",
        "tone_label": "Nada Dering:",
        "repeat_days": "Ulangi Hari:",
        "btn_add_alarm": "+ Pasang Alarm",
        "btn_test_tone": "🔊 Uji Suara",
        "active_alarms": "Daftar Alarm Aktif",
        "no_alarms": "Belum ada alarm. Buat alarm baru di sebelah kiri.",
        "btn_active": "AKTIF",
        "btn_inactive": "NONAKTIF",
        "pomo_title": "POMODORO FOCUS TIMER",
        "pomo_state_work": "SESI FOKUS KERJA",
        "pomo_state_break": "SESI ISTIRAHAT",
        "btn_pomo_start": "▶ Mulai Sesi",
        "btn_pomo_pause": "⏸ Jeda",
        "btn_pomo_resume": "▶ Lanjut",
        "btn_pomo_reset": "↺ Reset",
        "pomo_desc": "25 menit fokus kerja diselingi 5 menit istirahat untuk menjaga kesegaran berpikir.",
        "eye_title": "PENGINGAT MATA 20-20-20",
        "eye_toggle_on": "🟢 Pengingat Aktif",
        "eye_toggle_off": "🔴 Pengingat Nonaktif",
        "eye_interval_lbl": "Interval:",
        "btn_eye_reset": "↺ Reset",
        "eye_desc": "Tiap 20 menit menatap layar, pandang objek sejauh 6 meter selama 20 detik guna mencegah mata lelah.",
        "settings_heading": "⚙️ PREFERENSI SUARA & TAMPILAN",
        "default_tone": "Nada Alarm Utama:",
        "app_language": "Bahasa Antarmuka:",
        "app_theme": "Tema Tampilan:",
        "theme_dark": "🌙 Mode Gelap (Dark)",
        "theme_light": "☀️ Mode Terang (Light)",
        "storage_heading": "📁 PENYIMPANAN DATA LOKAL (JSON)",
        "storage_info": (
            "1. Seluruh jadwal dan preferensi tersimpan secara lokal dalam format JSON.\n"
            "2. Nada alarm disintesis mandiri tanpa dependensi file eksternal.\n"
            "3. Berkas data dapat dicadangkan atau dipindahkan secara manual kapan saja."
        ),
        "btn_open_folder": "Buka Folder Data",
        "btn_save_json": "Simpan JSON Sekarang",
        "update_heading": "🔄 SINKRONISASI & PEMBARUAN VERSI",
        "current_ver": "Versi Saat Ini:",
        "btn_check_update": "🔄 Periksa Pembaruan",
        "btn_open_repo": "🌐 Buka GitHub Repository",
        "status_ready": "● Siap memeriksa pembaruan",
        "status_checking": "⏳ Memeriksa ke GitHub...",
        "status_latest": "✓ Versi sudah paling mutakhir (v1.1.0)",
        "status_new_avail": "✨ Versi baru tersedia!",
        "status_offline": "● Mode offline / server tidak terjangkau",
        "format_err": "Masukkan jam (00-23) dan menit (00-59) yang valid.",
        "saved_ok": "Pengaturan berhasil disimpan ke berkas lokal.",
        "up_to_date_msg": "Aplikasi ZZZleep sudah berada pada versi paling mutakhir (v1.1.0).",
        "conn_err_msg": "Tidak dapat menghubungi server GitHub. Periksa koneksi internet Anda."
    },
    "en": {
        "app_title": "ZZZleep — Desktop Calendar & Audio Alarm",
        "brand": "⏰ ZZZleep",
        "nav_alarms": "⏰  Alarms & Schedule",
        "nav_timers": "🍅  Focus & Screen Rest",
        "nav_settings": "⚙️  Settings & Data",
        "nav_hub": "🌐  Portfolio Hub",
        "local_time": "LOCAL TIME",
        "monthly_calendar": "MONTHLY CALENDAR",
        "new_alarm": "Add New Alarm",
        "time_picker": "Alarm Time (Hour : Minute):",
        "quick_presets": "Quick Times:",
        "title_label": "Label / Description:",
        "tone_label": "Sound Tone:",
        "repeat_days": "Repeat Days:",
        "btn_add_alarm": "+ Set Alarm",
        "btn_test_tone": "🔊 Test Tone",
        "active_alarms": "Active Alarms List",
        "no_alarms": "No active alarms yet. Create one on the left.",
        "btn_active": "ACTIVE",
        "btn_inactive": "INACTIVE",
        "pomo_title": "POMODORO FOCUS TIMER",
        "pomo_state_work": "FOCUS WORK SESSION",
        "pomo_state_break": "REST BREAK SESSION",
        "btn_pomo_start": "▶ Start Session",
        "btn_pomo_pause": "⏸ Pause",
        "btn_pomo_resume": "▶ Resume",
        "btn_pomo_reset": "↺ Reset",
        "pomo_desc": "25-minute focused work cycles followed by 5-minute breaks to maintain productivity.",
        "eye_title": "20-20-20 SCREEN REST",
        "eye_toggle_on": "🟢 Reminder Active",
        "eye_toggle_off": "🔴 Reminder Disabled",
        "eye_interval_lbl": "Interval:",
        "btn_eye_reset": "↺ Reset",
        "eye_desc": "Every 20 minutes looking at screens, look at an object 20 feet away for 20 seconds.",
        "settings_heading": "⚙️ AUDIO & THEME PREFERENCES",
        "default_tone": "Default Alarm Tone:",
        "app_language": "Interface Language:",
        "app_theme": "UI Theme:",
        "theme_dark": "🌙 Dark Mode",
        "theme_light": "☀️ Light Mode",
        "storage_heading": "📁 LOCAL DATA STORAGE (JSON)",
        "storage_info": (
            "1. All schedules & preferences are stored locally in JSON format.\n"
            "2. Alarms are synthesized without external audio file dependencies.\n"
            "3. Data files can be backed up or transferred manually anytime."
        ),
        "btn_open_folder": "Open Data Folder",
        "btn_save_json": "Save JSON Now",
        "update_heading": "🔄 VERSION SYNC & UPDATES",
        "current_ver": "Current Version:",
        "btn_check_update": "🔄 Check for Updates",
        "btn_open_repo": "🌐 Open GitHub Repository",
        "status_ready": "● Ready to check updates",
        "status_checking": "⏳ Checking GitHub...",
        "status_latest": "✓ App is up to date (v1.1.0)",
        "status_new_avail": "✨ New version available!",
        "status_offline": "● Offline mode / server unreachable",
        "format_err": "Please enter valid hours (00-23) and minutes (00-59).",
        "saved_ok": "Preferences saved to local file successfully.",
        "up_to_date_msg": "ZZZleep is already at the latest version (v1.1.0).",
        "conn_err_msg": "Unable to connect to GitHub. Please check your internet connection."
    }
}

DEFAULT_DATA = {
    "alarms": [
        {"id": "alarm-1", "title": "Bangun Pagi & Stretching", "time": "06:00", "enabled": True, "days": [1, 2, 3, 4, 5], "tone": "gentle"},
        {"id": "alarm-2", "title": "Istirahat Siang & Makan", "time": "12:00", "enabled": True, "days": [1, 2, 3, 4, 5], "tone": "retro"},
        {"id": "alarm-3", "title": "Tutup Laptop & Istirahat", "time": "22:30", "enabled": True, "days": [0, 1, 2, 3, 4, 5, 6], "tone": "bell"}
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

        self.current_nav = "alarms"  # "alarms", "timers", "settings"
        self.selected_form_days = [0, 1, 2, 3, 4, 5, 6]

        self.pomodoro_total_sec = 25 * 60
        self.pomodoro_seconds_left = 25 * 60
        self.pomodoro_is_running = False
        self.pomodoro_is_break = False

        self.eye_rest_total_sec = self.eye_interval_min * 60
        self.eye_rest_seconds_left = self.eye_interval_min * 60

        # UI Setup
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("980x680")
        self.root.minsize(920, 620)

        self.build_main_shell()
        self.start_background_timer()

        # Check for updates in background 2s after launch
        self.root.after(2000, lambda: self.check_for_updates_async(silent=True))

    def t(self, key):
        return I18N.get(self.current_lang, I18N["id"]).get(key, key)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    d = json.load(f)
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

    def switch_nav(self, nav_key):
        self.current_nav = nav_key
        self.render_content_view()
        self.update_sidebar_buttons()

    def toggle_language(self):
        self.current_lang = "en" if self.current_lang == "id" else "id"
        self.save_data()
        self.rebuild_ui()

    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.save_data()
        self.rebuild_ui()

    def rebuild_ui(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.build_main_shell()

    def build_main_shell(self):
        th = THEMES[self.current_theme]
        self.root.configure(bg=th["bg"])

        # Main horizontal container
        self.shell_frame = tk.Frame(self.root, bg=th["bg"])
        self.shell_frame.pack(fill="both", expand=True)

        # 1. Left Sidebar
        self.sidebar = tk.Frame(self.shell_frame, bg=th["sidebar_bg"], width=230, highlightthickness=1, highlightbackground=th["border"])
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Sidebar Header (Brand)
        brand_frame = tk.Frame(self.sidebar, bg=th["sidebar_bg"])
        brand_frame.pack(fill="x", padx=16, pady=(18, 20))

        tk.Label(brand_frame, text=self.t("brand"), font=("Segoe UI", 15, "bold"), fg=th["accent_cyan"], bg=th["sidebar_bg"]).pack(side="left")
        tk.Label(brand_frame, text=f"v{APP_VERSION}", font=("Consolas", 8, "bold"), fg=th["text_secondary"], bg=th["subcard_bg"], padx=6, pady=2).pack(side="left", padx=8)

        # Navigation Menu Buttons
        self.nav_btns = {}
        nav_items = [
            ("alarms", self.t("nav_alarms")),
            ("timers", self.t("nav_timers")),
            ("settings", self.t("nav_settings")),
        ]

        menu_box = tk.Frame(self.sidebar, bg=th["sidebar_bg"])
        menu_box.pack(fill="x", padx=10, pady=4)

        for key, label in nav_items:
            btn = tk.Button(
                menu_box,
                text=label,
                font=("Segoe UI", 10, "bold"),
                anchor="w",
                relief="flat",
                padx=14,
                pady=10,
                cursor="hand2",
                command=lambda k=key: self.switch_nav(k)
            )
            btn.pack(fill="x", pady=3)
            self.nav_btns[key] = btn

        # Sidebar Bottom Controls (Language, Theme, Hub)
        bot_box = tk.Frame(self.sidebar, bg=th["sidebar_bg"])
        bot_box.pack(side="bottom", fill="x", padx=14, pady=16)

        # Quick Theme & Lang Row
        toggle_row = tk.Frame(bot_box, bg=th["sidebar_bg"])
        toggle_row.pack(fill="x", pady=(0, 10))

        lang_label = "🌐 ID" if self.current_lang == "id" else "🌐 EN"
        btn_lang = tk.Button(toggle_row, text=lang_label, font=("Segoe UI", 8, "bold"), bg=th["btn_bg"], fg=th["btn_fg"], relief="flat", padx=10, pady=5, cursor="hand2", command=self.toggle_language)
        btn_lang.pack(side="left", expand=True, fill="x", padx=(0, 4))

        theme_label = "🌙 Dark" if self.current_theme == "dark" else "☀️ Light"
        btn_theme = tk.Button(toggle_row, text=theme_label, font=("Segoe UI", 8, "bold"), bg=th["btn_bg"], fg=th["btn_fg"], relief="flat", padx=10, pady=5, cursor="hand2", command=self.toggle_theme)
        btn_theme.pack(side="right", expand=True, fill="x", padx=(4, 0))

        # Hub Link
        btn_hub = tk.Button(bot_box, text=self.t("nav_hub") + " ↗", font=("Segoe UI", 8), bg=th["sidebar_bg"], fg=th["text_secondary"], activeforeground=th["accent_cyan"], relief="flat", cursor="hand2", command=lambda: webbrowser.open("https://infinitenull.github.io/"))
        btn_hub.pack(fill="x")

        # 2. Right Content Area
        self.content_area = tk.Frame(self.shell_frame, bg=th["bg"])
        self.content_area.pack(side="right", fill="both", expand=True, padx=16, pady=16)

        self.update_sidebar_buttons()
        self.render_content_view()

    def update_sidebar_buttons(self):
        th = THEMES[self.current_theme]
        for key, btn in self.nav_btns.items():
            if key == self.current_nav:
                btn.config(bg=th["nav_active_bg"], fg=th["nav_active_fg"], activebackground=th["accent_hover"], activeforeground="white")
            else:
                btn.config(bg=th["nav_inactive_bg"], fg=th["nav_inactive_fg"], activebackground=th["btn_bg"], activeforeground=th["text_primary"])

    def render_content_view(self):
        for w in self.content_area.winfo_children():
            w.destroy()

        if self.current_nav == "alarms":
            self.build_alarms_view(self.content_area)
        elif self.current_nav == "timers":
            self.build_timers_view(self.content_area)
        elif self.current_nav == "settings":
            self.build_settings_view(self.content_area)

    # =========================================================================
    # VIEW 1: ALARMS & MONTHLY CALENDAR
    # =========================================================================
    def build_alarms_view(self, parent):
        th = THEMES[self.current_theme]

        # Top Bar: Big Local Clock & Active Alarms Status
        top_bar = tk.Frame(parent, bg=th["card_bg"], highlightthickness=1, highlightbackground=th["border"])
        top_bar.pack(fill="x", pady=(0, 12))

        # Left Top: Digital Clock & Date
        clock_box = tk.Frame(top_bar, bg=th["card_bg"])
        clock_box.pack(side="left", padx=16, pady=10)

        self.clock_lbl = tk.Label(clock_box, text="00:00:00", font=("Consolas", 22, "bold"), fg=th["accent_cyan"], bg=th["card_bg"])
        self.clock_lbl.pack(anchor="w")
        self.date_lbl = tk.Label(clock_box, text="Loading date...", font=("Segoe UI", 9), fg=th["text_secondary"], bg=th["card_bg"])
        self.date_lbl.pack(anchor="w")

        # Right Top: Alarm Status Pill
        active_count = len([a for a in self.data.get("alarms", []) if a.get("enabled", True)])
        pill_txt = f"🔔 {active_count} Alarm Aktif" if self.current_lang == "id" else f"🔔 {active_count} Alarms Active"
        tk.Label(top_bar, text=pill_txt, font=("Segoe UI", 9, "bold"), fg="#10b981", bg=th["subcard_bg"], padx=12, pady=6).pack(side="right", padx=16)

        # Dual Column Layout
        cols = tk.Frame(parent, bg=th["bg"])
        cols.pack(fill="both", expand=True)

        # Left Column: Add Alarm Form (Width ~340px)
        left_col = tk.Frame(cols, bg=th["card_bg"], width=350, highlightthickness=1, highlightbackground=th["border"])
        left_col.pack(side="left", fill="both", padx=(0, 10))
        left_col.pack_propagate(False)

        tk.Label(left_col, text=self.t("new_alarm"), font=("Segoe UI", 11, "bold"), fg=th["text_primary"], bg=th["card_bg"]).pack(anchor="w", padx=16, pady=(14, 6))

        # --- Dual Spinbox Time Picker (NO ACCIDENTAL DELETING COLON) ---
        tk.Label(left_col, text=self.t("time_picker"), font=("Segoe UI", 9, "bold"), fg=th["text_secondary"], bg=th["card_bg"]).pack(anchor="w", padx=16, pady=(4, 4))
        
        picker_box = tk.Frame(left_col, bg=th["card_bg"])
        picker_box.pack(anchor="w", padx=16, pady=(0, 6))

        # Hour Spinbox
        self.spin_hour = tk.Spinbox(picker_box, from_=0, to=23, format="%02.0f", width=3, font=("Consolas", 16, "bold"), justify="center", bg=th["entry_bg"], fg=th["entry_fg"], relief="flat", highlightthickness=1, highlightbackground=th["border_subtle"])
        self.spin_hour.delete(0, "end")
        self.spin_hour.insert(0, "07")
        self.spin_hour.pack(side="left")

        # Fixed Permanent Colon
        tk.Label(picker_box, text=" : ", font=("Consolas", 18, "bold"), fg=th["accent_cyan"], bg=th["card_bg"]).pack(side="left", padx=4)

        # Minute Spinbox
        self.spin_min = tk.Spinbox(picker_box, from_=0, to=59, format="%02.0f", width=3, font=("Consolas", 16, "bold"), justify="center", bg=th["entry_bg"], fg=th["entry_fg"], relief="flat", highlightthickness=1, highlightbackground=th["border_subtle"])
        self.spin_min.delete(0, "end")
        self.spin_min.insert(0, "30")
        self.spin_min.pack(side="left")

        # Quick Preset Buttons Row
        preset_row = tk.Frame(left_col, bg=th["card_bg"])
        preset_row.pack(anchor="w", padx=16, pady=(0, 10))
        for p_h, p_m in [("06", "00"), ("08", "00"), ("12", "00"), ("22", "30")]:
            btn_p = tk.Button(preset_row, text=f"{p_h}:{p_m}", font=("Consolas", 8), bg=th["btn_bg"], fg=th["btn_fg"], relief="flat", padx=6, pady=2, cursor="hand2", command=lambda h=p_h, m=p_m: self.set_picker_time(h, m))
            btn_p.pack(side="left", padx=(0, 4))

        # Label Entry
        tk.Label(left_col, text=self.t("title_label"), font=("Segoe UI", 9), fg=th["text_secondary"], bg=th["card_bg"]).pack(anchor="w", padx=16, pady=(2, 2))
        self.entry_title = tk.Entry(left_col, font=("Segoe UI", 10), bg=th["entry_bg"], fg=th["text_primary"], insertbackground=th["entry_fg"], relief="flat", highlightthickness=1, highlightbackground=th["border_subtle"])
        self.entry_title.insert(0, "Mulai Kerja Pagi" if self.current_lang == "id" else "Morning Deep Work")
        self.entry_title.pack(fill="x", padx=16, ipady=4)

        # Tone Selector with Test Button
        tk.Label(left_col, text=self.t("tone_label"), font=("Segoe UI", 9), fg=th["text_secondary"], bg=th["card_bg"]).pack(anchor="w", padx=16, pady=(8, 2))
        tone_box = tk.Frame(left_col, bg=th["card_bg"])
        tone_box.pack(fill="x", padx=16)

        self.var_alarm_tone = tk.StringVar(value=self.current_tone)
        self.combo_tone = ttk.Combobox(tone_box, textvariable=self.var_alarm_tone, values=list(TONES.keys()), state="readonly", font=("Segoe UI", 9))
        self.combo_tone.pack(side="left", fill="x", expand=True)

        btn_test = tk.Button(tone_box, text="🔊", font=("Segoe UI", 9), bg=th["btn_bg"], fg=th["btn_fg"], relief="flat", padx=8, cursor="hand2", command=lambda: play_audio_tone(self.var_alarm_tone.get()))
        btn_test.pack(side="right", padx=(4, 0))

        # Day Pills Selector (Sun - Sat)
        tk.Label(left_col, text=self.t("repeat_days"), font=("Segoe UI", 9), fg=th["text_secondary"], bg=th["card_bg"]).pack(anchor="w", padx=16, pady=(8, 4))
        day_pills_row = tk.Frame(left_col, bg=th["card_bg"])
        day_pills_row.pack(anchor="w", padx=16)

        day_labels = DAY_NAMES_ID if self.current_lang == "id" else DAY_NAMES_EN
        self.day_buttons = []
        for i in range(7):
            d_btn = tk.Button(
                day_pills_row,
                text=day_labels[i],
                font=("Segoe UI", 7, "bold"),
                width=3,
                bg=th["accent"] if i in self.selected_form_days else th["btn_bg"],
                fg="white" if i in self.selected_form_days else th["text_secondary"],
                relief="flat",
                cursor="hand2",
                command=lambda day_idx=i: self.toggle_form_day(day_idx)
            )
            d_btn.pack(side="left", padx=1)
            self.day_buttons.append(d_btn)

        # Submit Button
        btn_add = tk.Button(left_col, text=self.t("btn_add_alarm"), font=("Segoe UI", 10, "bold"), bg=th["accent"], fg="white", activebackground=th["accent_hover"], activeforeground="white", relief="flat", cursor="hand2", command=self.add_alarm_from_picker)
        btn_add.pack(fill="x", padx=16, pady=(16, 12), ipady=5)

        # Right Column: Mini Calendar (Top) + Alarms List (Bottom)
        right_col = tk.Frame(cols, bg=th["bg"])
        right_col.pack(side="right", fill="both", expand=True)

        # Mini Calendar Card (Height ~170px)
        cal_card = tk.Frame(right_col, bg=th["card_bg"], highlightthickness=1, highlightbackground=th["border"])
        cal_card.pack(fill="x", pady=(0, 10))
        self.build_mini_calendar(cal_card)

        # Alarms List Card (Remaining height)
        list_card = tk.Frame(right_col, bg=th["card_bg"], highlightthickness=1, highlightbackground=th["border"])
        list_card.pack(fill="both", expand=True)

        tk.Label(list_card, text=self.t("active_alarms"), font=("Segoe UI", 11, "bold"), fg=th["text_primary"], bg=th["card_bg"]).pack(anchor="w", padx=16, pady=(12, 6))

        self.alarms_frame = tk.Frame(list_card, bg=th["card_bg"])
        self.alarms_frame.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        self.refresh_alarms_list()

    def set_picker_time(self, h, m):
        self.spin_hour.delete(0, "end")
        self.spin_hour.insert(0, h)
        self.spin_min.delete(0, "end")
        self.spin_min.insert(0, m)

    def toggle_form_day(self, day_idx):
        th = THEMES[self.current_theme]
        if day_idx in self.selected_form_days:
            if len(self.selected_form_days) > 1:
                self.selected_form_days.remove(day_idx)
        else:
            self.selected_form_days.append(day_idx)
            self.selected_form_days.sort()

        for i, btn in enumerate(self.day_buttons):
            if i in self.selected_form_days:
                btn.config(bg=th["accent"], fg="white")
            else:
                btn.config(bg=th["btn_bg"], fg=th["text_secondary"])

    def build_mini_calendar(self, parent):
        th = THEMES[self.current_theme]
        now = datetime.datetime.now()
        year, month = now.year, now.month
        
        cal_hdr = tk.Frame(parent, bg=th["card_bg"])
        cal_hdr.pack(fill="x", padx=14, pady=(8, 4))

        month_name = now.strftime("%B %Y")
        tk.Label(cal_hdr, text=f"📅 {month_name.upper()}", font=("Segoe UI", 9, "bold"), fg=th["accent_cyan"], bg=th["card_bg"]).pack(side="left")
        tk.Label(cal_hdr, text=f"Hari Ini: {now.day}", font=("Segoe UI", 8), fg=th["text_secondary"], bg=th["card_bg"]).pack(side="right")

        # Calendar Grid Table
        grid_frame = tk.Frame(parent, bg=th["card_bg"])
        grid_frame.pack(fill="x", padx=14, pady=(0, 8))

        day_headers = DAY_NAMES_ID if self.current_lang == "id" else DAY_NAMES_EN
        for col_idx, d_name in enumerate(day_headers):
            tk.Label(grid_frame, text=d_name, font=("Segoe UI", 8, "bold"), fg=th["text_secondary"], bg=th["card_bg"], width=4).grid(row=0, column=col_idx, padx=2, pady=1)

        # Sunday first indexing
        cal = calendar.Calendar(firstweekday=6)
        month_days = cal.monthdayscalendar(year, month)

        for r_idx, week in enumerate(month_days):
            for c_idx, day_num in enumerate(week):
                if day_num == 0:
                    lbl = tk.Label(grid_frame, text="", bg=th["card_bg"], width=4)
                else:
                    is_today = (day_num == now.day)
                    bg_col = th["accent"] if is_today else th["subcard_bg"]
                    fg_col = "white" if is_today else th["text_primary"]
                    lbl = tk.Label(grid_frame, text=str(day_num), font=("Segoe UI", 8, "bold" if is_today else "normal"), bg=bg_col, fg=fg_col, width=4, pady=1)
                lbl.grid(row=r_idx + 1, column=c_idx, padx=2, pady=1)

    def refresh_alarms_list(self):
        th = THEMES[self.current_theme]
        for w in self.alarms_frame.winfo_children():
            w.destroy()

        alarms = self.data.get("alarms", [])
        if not alarms:
            tk.Label(self.alarms_frame, text=self.t("no_alarms"), fg=th["text_secondary"], bg=th["card_bg"], font=("Segoe UI", 9, "italic")).pack(pady=20)
            return

        day_labels = DAY_NAMES_ID if self.current_lang == "id" else DAY_NAMES_EN

        for a in alarms:
            card = tk.Frame(self.alarms_frame, bg=th["subcard_bg"], relief="flat", highlightthickness=1, highlightbackground=th["border_subtle"])
            card.pack(fill="x", pady=3)

            # Left: Time & Info
            left_box = tk.Frame(card, bg=th["subcard_bg"])
            left_box.pack(side="left", padx=12, pady=6)

            time_col = th["accent_cyan"] if a.get("enabled", True) else th["text_secondary"]
            tk.Label(left_box, text=a["time"], font=("Consolas", 17, "bold"), fg=time_col, bg=th["subcard_bg"]).pack(anchor="w")

            # Day Chips sub-row
            chips_row = tk.Frame(left_box, bg=th["subcard_bg"])
            chips_row.pack(anchor="w", pady=(2, 0))
            tk.Label(chips_row, text=a.get("title", "Alarm"), font=("Segoe UI", 9, "bold"), fg=th["text_primary"] if a.get("enabled", True) else th["text_secondary"], bg=th["subcard_bg"]).pack(side="left", padx=(0, 6))

            for d_i in range(7):
                in_days = d_i in a.get("days", [0, 1, 2, 3, 4, 5, 6])
                d_fg = th["accent_cyan"] if (in_days and a.get("enabled", True)) else th["border_subtle"]
                tk.Label(chips_row, text=day_labels[d_i][0], font=("Consolas", 7, "bold"), fg=d_fg, bg=th["subcard_bg"]).pack(side="left", padx=1)

            # Right: Action Buttons
            right_box = tk.Frame(card, bg=th["subcard_bg"])
            right_box.pack(side="right", padx=12, pady=6)

            st_text = self.t("btn_active") if a.get("enabled", True) else self.t("btn_inactive")
            st_bg = "#059669" if a.get("enabled", True) else "#64748b"
            t_btn = tk.Button(right_box, text=st_text, font=("Segoe UI", 8, "bold"), bg=st_bg, fg="white", relief="flat", padx=8, pady=2, cursor="hand2", command=lambda item=a: self.toggle_alarm(item))
            t_btn.pack(side="left", padx=3)

            btn_test = tk.Button(right_box, text="🔊", font=("Segoe UI", 8), bg=th["btn_bg"], fg=th["btn_fg"], relief="flat", padx=6, pady=2, cursor="hand2", command=lambda item=a: play_audio_tone(item.get("tone", "gentle")))
            btn_test.pack(side="left", padx=3)

            d_btn = tk.Button(right_box, text="✕", font=("Segoe UI", 8, "bold"), bg="#dc2626", fg="white", relief="flat", padx=6, pady=2, cursor="hand2", command=lambda a_id=a["id"]: self.delete_alarm(a_id))
            d_btn.pack(side="left", padx=3)

    def add_alarm_from_picker(self):
        try:
            h = int(self.spin_hour.get())
            m = int(self.spin_min.get())
            if not (0 <= h < 24 and 0 <= m < 60):
                raise ValueError
            valid_time = f"{h:02d}:{m:02d}"
        except Exception:
            messagebox.showerror("Error", self.t("format_err"))
            return

        title = self.entry_title.get().strip() or "Alarm"
        tone = self.var_alarm_tone.get()

        new_a = {
            "id": f"alarm-{int(time.time()*1000)}",
            "title": title,
            "time": valid_time,
            "enabled": True,
            "days": list(self.selected_form_days),
            "tone": tone
        }
        self.data["alarms"].append(new_a)
        self.save_data()
        self.refresh_alarms_list()

    def toggle_alarm(self, a):
        a["enabled"] = not a.get("enabled", True)
        self.save_data()
        self.refresh_alarms_list()

    def delete_alarm(self, a_id):
        self.data["alarms"] = [a for a in self.data.get("alarms", []) if a.get("id") != a_id]
        self.save_data()
        self.refresh_alarms_list()

    # =========================================================================
    # VIEW 2: FOCUS TIMERS & CIRCULAR PROGRESS RINGS
    # =========================================================================
    def build_timers_view(self, parent):
        th = THEMES[self.current_theme]

        cards_row = tk.Frame(parent, bg=th["bg"])
        cards_row.pack(fill="both", expand=True)

        # 1. Left Card: Pomodoro Circular Timer
        pomo_card = tk.Frame(cards_row, bg=th["card_bg"], highlightthickness=1, highlightbackground=th["border"])
        pomo_card.pack(side="left", fill="both", expand=True, padx=(0, 8))

        tk.Label(pomo_card, text=self.t("pomo_title"), font=("Segoe UI", 12, "bold"), fg=th["ring_pomo"], bg=th["card_bg"]).pack(pady=(16, 2))
        
        state_txt = self.t("pomo_state_work") if not self.pomodoro_is_break else self.t("pomo_state_break")
        self.lbl_pomo_state = tk.Label(pomo_card, text=state_txt, font=("Segoe UI", 8, "bold"), fg=th["text_secondary"], bg=th["card_bg"])
        self.lbl_pomo_state.pack(pady=(0, 6))

        # Circular Canvas
        self.canvas_pomo = tk.Canvas(pomo_card, width=200, height=200, bg=th["card_bg"], highlightthickness=0)
        self.canvas_pomo.pack(pady=4)

        # Action Buttons
        pomo_btns = tk.Frame(pomo_card, bg=th["card_bg"])
        pomo_btns.pack(pady=10)

        self.btn_pomo = tk.Button(pomo_btns, text=self.t("btn_pomo_start"), font=("Segoe UI", 9, "bold"), bg=th["ring_pomo"], fg="white", relief="flat", padx=14, pady=6, cursor="hand2", command=self.toggle_pomodoro)
        self.btn_pomo.pack(side="left", padx=4)

        btn_pomo_r = tk.Button(pomo_btns, text=self.t("btn_pomo_reset"), font=("Segoe UI", 9), bg=th["btn_bg"], fg=th["btn_fg"], relief="flat", padx=10, pady=6, cursor="hand2", command=self.reset_pomodoro)
        btn_pomo_r.pack(side="left", padx=4)

        tk.Label(pomo_card, text=self.t("pomo_desc"), font=("Segoe UI", 8), fg=th["text_secondary"], bg=th["card_bg"], justify="center", wraplength=280).pack(pady=(4, 12))

        # 2. Right Card: 20-20-20 Eye Rest Circular Timer
        eye_card = tk.Frame(cards_row, bg=th["card_bg"], highlightthickness=1, highlightbackground=th["border"])
        eye_card.pack(side="right", fill="both", expand=True, padx=(8, 0))

        tk.Label(eye_card, text=self.t("eye_title"), font=("Segoe UI", 12, "bold"), fg=th["ring_eye"], bg=th["card_bg"]).pack(pady=(16, 2))

        # Toggle Switch Row
        st_txt = self.t("eye_toggle_on") if self.eye_rest_enabled else self.t("eye_toggle_off")
        st_bg = "#10b981" if self.eye_rest_enabled else "#64748b"
        self.btn_eye_toggle = tk.Button(eye_card, text=st_txt, font=("Segoe UI", 8, "bold"), bg=st_bg, fg="white", relief="flat", padx=10, pady=2, cursor="hand2", command=self.toggle_eye_rest_enabled)
        self.btn_eye_toggle.pack(pady=(0, 6))

        # Circular Canvas
        self.canvas_eye = tk.Canvas(eye_card, width=200, height=200, bg=th["card_bg"], highlightthickness=0)
        self.canvas_eye.pack(pady=4)

        # Interval Options Row
        int_row = tk.Frame(eye_card, bg=th["card_bg"])
        int_row.pack(pady=4)
        tk.Label(int_row, text=self.t("eye_interval_lbl"), font=("Segoe UI", 8), fg=th["text_secondary"], bg=th["card_bg"]).pack(side="left", padx=4)

        for mins in [15, 20, 30, 45]:
            act = (mins == self.eye_interval_min)
            b_bg = th["accent"] if act else th["btn_bg"]
            b_fg = "white" if act else th["btn_fg"]
            b_int = tk.Button(int_row, text=f"{mins}m", font=("Segoe UI", 8, "bold" if act else "normal"), bg=b_bg, fg=b_fg, relief="flat", padx=6, pady=2, cursor="hand2", command=lambda m=mins: self.set_eye_interval(m))
            b_int.pack(side="left", padx=2)

        btn_eye_r = tk.Button(eye_card, text=self.t("btn_eye_reset"), font=("Segoe UI", 8), bg=th["btn_bg"], fg=th["btn_fg"], relief="flat", padx=10, pady=4, cursor="hand2", command=self.reset_eye_rest)
        btn_eye_r.pack(pady=4)

        tk.Label(eye_card, text=self.t("eye_desc"), font=("Segoe UI", 8), fg=th["text_secondary"], bg=th["card_bg"], justify="center", wraplength=280).pack(pady=(2, 12))

        self.update_timer_rings()

    def update_timer_rings(self):
        if not hasattr(self, 'canvas_pomo') or not self.canvas_pomo.winfo_exists():
            return

        th = THEMES[self.current_theme]
        
        # 1. Draw Pomodoro Ring
        self.canvas_pomo.delete("all")
        p_pct = 1.0 - (self.pomodoro_seconds_left / max(1, self.pomodoro_total_sec))
        self.draw_circular_arc(self.canvas_pomo, 200, 200, p_pct, th["ring_pomo"], th["ring_bg"])
        
        m_p = self.pomodoro_seconds_left // 60
        s_p = self.pomodoro_seconds_left % 60
        self.canvas_pomo.create_text(100, 100, text=f"{m_p:02d}:{s_p:02d}", font=("Consolas", 28, "bold"), fill=th["text_primary"])

        # 2. Draw Eye Rest Ring
        self.canvas_eye.delete("all")
        e_pct = 1.0 - (self.eye_rest_seconds_left / max(1, self.eye_rest_total_sec))
        ring_col = th["ring_eye"] if self.eye_rest_enabled else th["border_subtle"]
        self.draw_circular_arc(self.canvas_eye, 200, 200, e_pct if self.eye_rest_enabled else 0.0, ring_col, th["ring_bg"])
        
        m_e = self.eye_rest_seconds_left // 60
        s_e = self.eye_rest_seconds_left % 60
        txt_col = th["text_primary"] if self.eye_rest_enabled else th["text_secondary"]
        self.canvas_eye.create_text(100, 100, text=f"{m_e:02d}:{s_e:02d}", font=("Consolas", 28, "bold"), fill=txt_col)

    def draw_circular_arc(self, canvas, w, h, progress_pct, arc_color, track_color):
        pad = 18
        width_ring = 12
        # Background full circle track
        canvas.create_oval(pad, pad, w - pad, h - pad, outline=track_color, width=width_ring)
        # Active progress arc
        if progress_pct > 0:
            extent = -359.9 * min(1.0, max(0.0, progress_pct))
            canvas.create_arc(pad, pad, w - pad, h - pad, start=90, extent=extent, outline=arc_color, width=width_ring, style="arc")

    def toggle_pomodoro(self):
        self.pomodoro_is_running = not self.pomodoro_is_running
        if self.pomodoro_is_running:
            self.btn_pomo.config(text=self.t("btn_pomo_pause"), bg="#d97706")
        else:
            self.btn_pomo.config(text=self.t("btn_pomo_resume"), bg=THEMES[self.current_theme]["ring_pomo"])

    def reset_pomodoro(self):
        self.pomodoro_is_running = False
        self.pomodoro_is_break = False
        self.pomodoro_total_sec = 25 * 60
        self.pomodoro_seconds_left = 25 * 60
        self.btn_pomo.config(text=self.t("btn_pomo_start"), bg=THEMES[self.current_theme]["ring_pomo"])
        self.lbl_pomo_state.config(text=self.t("pomo_state_work"))
        self.update_timer_rings()

    def toggle_eye_rest_enabled(self):
        self.eye_rest_enabled = not self.eye_rest_enabled
        self.save_data()
        st_txt = self.t("eye_toggle_on") if self.eye_rest_enabled else self.t("eye_toggle_off")
        st_bg = "#10b981" if self.eye_rest_enabled else "#64748b"
        self.btn_eye_toggle.config(text=st_txt, bg=st_bg)
        self.update_timer_rings()

    def set_eye_interval(self, mins):
        self.eye_interval_min = mins
        self.eye_rest_total_sec = mins * 60
        self.eye_rest_seconds_left = mins * 60
        self.save_data()
        self.render_content_view()

    def reset_eye_rest(self):
        self.eye_rest_seconds_left = self.eye_interval_min * 60
        self.update_timer_rings()

    # =========================================================================
    # VIEW 3: SETTINGS, DATA & UPDATES
    # =========================================================================
    def build_settings_view(self, parent):
        th = THEMES[self.current_theme]

        # 1. Preferences Card
        pref_card = tk.Frame(parent, bg=th["card_bg"], highlightthickness=1, highlightbackground=th["border"])
        pref_card.pack(fill="x", pady=(0, 10))

        tk.Label(pref_card, text=self.t("settings_heading"), font=("Segoe UI", 11, "bold"), fg=th["accent_cyan"], bg=th["card_bg"]).pack(anchor="w", padx=16, pady=(12, 6))

        grid_p = tk.Frame(pref_card, bg=th["card_bg"])
        grid_p.pack(fill="x", padx=16, pady=(0, 12))

        # Default Tone
        tk.Label(grid_p, text=self.t("default_tone"), font=("Segoe UI", 9, "bold"), fg=th["text_primary"], bg=th["card_bg"]).grid(row=0, column=0, sticky="w", pady=4)
        self.var_def_tone = tk.StringVar(value=self.current_tone)
        combo_def = ttk.Combobox(grid_p, textvariable=self.var_def_tone, values=list(TONES.keys()), state="readonly", font=("Segoe UI", 9), width=18)
        combo_def.grid(row=0, column=1, sticky="w", padx=10, pady=4)
        combo_def.bind("<<ComboboxSelected>>", lambda e: self.on_change_default_tone())

        btn_test_def = tk.Button(grid_p, text="🔊 " + self.t("btn_test_tone"), font=("Segoe UI", 8), bg=th["btn_bg"], fg=th["btn_fg"], relief="flat", padx=8, cursor="hand2", command=lambda: play_audio_tone(self.var_def_tone.get()))
        btn_test_def.grid(row=0, column=2, sticky="w", padx=4, pady=4)

        # Language
        tk.Label(grid_p, text=self.t("app_language"), font=("Segoe UI", 9, "bold"), fg=th["text_primary"], bg=th["card_bg"]).grid(row=1, column=0, sticky="w", pady=6)
        lang_box = tk.Frame(grid_p, bg=th["card_bg"])
        lang_box.grid(row=1, column=1, sticky="w", padx=10, pady=6)

        btn_l_id = tk.Button(lang_box, text="Bahasa Indonesia", font=("Segoe UI", 8, "bold" if self.current_lang == "id" else "normal"), bg=th["accent"] if self.current_lang == "id" else th["btn_bg"], fg="white" if self.current_lang == "id" else th["btn_fg"], relief="flat", padx=8, pady=2, cursor="hand2", command=lambda: self.set_language("id"))
        btn_l_id.pack(side="left", padx=(0, 4))

        btn_l_en = tk.Button(lang_box, text="English", font=("Segoe UI", 8, "bold" if self.current_lang == "en" else "normal"), bg=th["accent"] if self.current_lang == "en" else th["btn_bg"], fg="white" if self.current_lang == "en" else th["btn_fg"], relief="flat", padx=8, pady=2, cursor="hand2", command=lambda: self.set_language("en"))
        btn_l_en.pack(side="left")

        # Theme
        tk.Label(grid_p, text=self.t("app_theme"), font=("Segoe UI", 9, "bold"), fg=th["text_primary"], bg=th["card_bg"]).grid(row=2, column=0, sticky="w", pady=6)
        thm_box = tk.Frame(grid_p, bg=th["card_bg"])
        thm_box.grid(row=2, column=1, sticky="w", padx=10, pady=6)

        btn_th_dark = tk.Button(thm_box, text=self.t("theme_dark"), font=("Segoe UI", 8, "bold" if self.current_theme == "dark" else "normal"), bg=th["accent"] if self.current_theme == "dark" else th["btn_bg"], fg="white" if self.current_theme == "dark" else th["btn_fg"], relief="flat", padx=8, pady=2, cursor="hand2", command=lambda: self.set_theme("dark"))
        btn_th_dark.pack(side="left", padx=(0, 4))

        btn_th_light = tk.Button(thm_box, text=self.t("theme_light"), font=("Segoe UI", 8, "bold" if self.current_theme == "light" else "normal"), bg=th["accent"] if self.current_theme == "light" else th["btn_bg"], fg="white" if self.current_theme == "light" else th["btn_fg"], relief="flat", padx=8, pady=2, cursor="hand2", command=lambda: self.set_theme("light"))
        btn_th_light.pack(side="left")

        # 2. Local Storage Card
        card = tk.Frame(parent, bg=th["card_bg"], highlightthickness=1, highlightbackground=th["border"])
        card.pack(fill="x", pady=(0, 10))

        tk.Label(card, text=self.t("storage_heading"), font=("Segoe UI", 11, "bold"), fg=th["accent_cyan"], bg=th["card_bg"]).pack(anchor="w", padx=16, pady=(12, 2))
        tk.Label(card, text=f"File: {DATA_FILE}", font=("Consolas", 8), fg=th["text_secondary"], bg=th["card_bg"]).pack(anchor="w", padx=16, pady=(0, 4))
        tk.Label(card, text=self.t("storage_info"), font=("Segoe UI", 8), fg=th["text_primary"], bg=th["card_bg"], justify="left").pack(anchor="w", padx=16, pady=2)

        btn_box = tk.Frame(card, bg=th["card_bg"])
        btn_box.pack(anchor="w", padx=16, pady=(6, 12))

        btn_open = tk.Button(btn_box, text=self.t("btn_open_folder"), font=("Segoe UI", 8, "bold"), bg=th["accent"], fg="white", relief="flat", padx=10, pady=4, cursor="hand2", command=lambda: os.system(f'explorer /select,"{DATA_FILE}"'))
        btn_open.pack(side="left", padx=(0, 6))

        btn_save = tk.Button(btn_box, text=self.t("btn_save_json"), font=("Segoe UI", 8), bg=th["btn_bg"], fg=th["btn_fg"], relief="flat", padx=10, pady=4, cursor="hand2", command=self.save_data_with_feedback)
        btn_save.pack(side="left")

        # 3. Update & Version Sync Card
        up_card = tk.Frame(parent, bg=th["card_bg"], highlightthickness=1, highlightbackground=th["border"])
        up_card.pack(fill="both", expand=True)

        tk.Label(up_card, text=self.t("update_heading"), font=("Segoe UI", 11, "bold"), fg="#10b981", bg=th["card_bg"]).pack(anchor="w", padx=16, pady=(12, 2))
        
        up_meta = tk.Frame(up_card, bg=th["card_bg"])
        up_meta.pack(fill="x", padx=16, pady=4)
        
        tk.Label(up_meta, text=f"{self.t('current_ver')} v{APP_VERSION}", font=("Segoe UI", 9, "bold"), fg=th["text_primary"], bg=th["card_bg"]).pack(side="left")
        self.lbl_update_status = tk.Label(up_meta, text=self.t("status_ready"), font=("Segoe UI", 8), fg=th["text_secondary"], bg=th["card_bg"])
        self.lbl_update_status.pack(side="left", padx=12)

        up_btn_box = tk.Frame(up_card, bg=th["card_bg"])
        up_btn_box.pack(anchor="w", padx=16, pady=(6, 12))

        self.btn_check_update = tk.Button(up_btn_box, text=self.t("btn_check_update"), font=("Segoe UI", 8, "bold"), bg="#059669", fg="white", activebackground="#047857", activeforeground="white", relief="flat", padx=12, pady=5, cursor="hand2", command=lambda: self.check_for_updates_async(silent=False))
        self.btn_check_update.pack(side="left", padx=(0, 6))

        btn_repo = tk.Button(up_btn_box, text=self.t("btn_open_repo"), font=("Segoe UI", 8), bg=th["btn_bg"], fg=th["btn_fg"], relief="flat", padx=10, pady=5, cursor="hand2", command=lambda: webbrowser.open(GITHUB_REPO_URL))
        btn_repo.pack(side="left")

    def on_change_default_tone(self):
        self.current_tone = self.var_def_tone.get()
        self.save_data()

    def set_language(self, lang):
        self.current_lang = lang
        self.save_data()
        self.rebuild_ui()

    def set_theme(self, th_name):
        self.current_theme = th_name
        self.save_data()
        self.rebuild_ui()

    def save_data_with_feedback(self):
        self.save_data()
        messagebox.showinfo("ZZZleep", self.t("saved_ok"))

    def check_for_updates_async(self, silent=True):
        if hasattr(self, 'lbl_update_status') and self.lbl_update_status.winfo_exists():
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
        if hasattr(self, 'lbl_update_status') and self.lbl_update_status.winfo_exists():
            self.lbl_update_status.config(text=f"{self.t('status_new_avail')} (v{new_ver})", fg="#10b981")
        self.show_update_dialog(data)

    def on_update_up_to_date(self, remote_ver, silent):
        if hasattr(self, 'lbl_update_status') and self.lbl_update_status.winfo_exists():
            self.lbl_update_status.config(text=self.t("status_latest"), fg="#10b981")
        if not silent:
            messagebox.showinfo("Pembaruan Versi", self.t("up_to_date_msg"))

    def on_update_error(self, err_msg, silent):
        if hasattr(self, 'lbl_update_status') and self.lbl_update_status.winfo_exists():
            self.lbl_update_status.config(text=self.t("status_offline"), fg="#94a3b8")
        if not silent:
            messagebox.showwarning("Koneksi Pembaruan", self.t("conn_err_msg"))

    def show_update_dialog(self, data):
        new_ver = data.get("version", "1.1.0")
        rel_date = data.get("release_date", "")
        changelog = data.get("changelog", [])
        dl_url = data.get("download_url", DIRECT_EXE_URL)

        th = THEMES[self.current_theme]
        dialog = tk.Toplevel(self.root)
        dialog.title("Pembaruan ZZZleep Tersedia" if self.current_lang == "id" else "ZZZleep Update Available")
        dialog.geometry("540x480")
        dialog.minsize(500, 440)
        dialog.configure(bg=th["bg"])
        dialog.transient(self.root)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        rx, ry = self.root.winfo_x(), self.root.winfo_y()
        rw, rh = self.root.winfo_width(), self.root.winfo_height()
        dx = rx + (rw - 540) // 2
        dy = ry + (rh - 480) // 2
        dialog.geometry(f"+{max(0, dx)}+{max(0, dy)}")

        hdr = tk.Frame(dialog, bg=th["card_bg"], highlightthickness=1, highlightbackground=th["border"])
        hdr.pack(fill="x")

        tk.Label(hdr, text="🚀", font=("Segoe UI Emoji", 20), bg=th["card_bg"]).pack(side="left", padx=(18, 8), pady=14)
        h_info = tk.Frame(hdr, bg=th["card_bg"])
        h_info.pack(side="left", fill="y", pady=12)

        title_text = "Pembaruan Baru Tersedia!" if self.current_lang == "id" else "New Version Available!"
        tk.Label(h_info, text=title_text, font=("Segoe UI", 12, "bold"), fg=th["accent_cyan"], bg=th["card_bg"]).pack(anchor="w")
        sub_text = f"Versi v{new_ver} telah dirilis ({rel_date})" if self.current_lang == "id" else f"Version v{new_ver} released ({rel_date})"
        tk.Label(h_info, text=sub_text, font=("Segoe UI", 8), fg=th["text_secondary"], bg=th["card_bg"]).pack(anchor="w")

        body = tk.Frame(dialog, bg=th["bg"])
        body.pack(fill="both", expand=True, padx=18, pady=12)

        v_box = tk.Frame(body, bg=th["card_bg"], padx=12, pady=8, highlightthickness=1, highlightbackground=th["border"])
        v_box.pack(fill="x", pady=(0, 10))

        cur_lbl = f"Versi Anda: v{APP_VERSION}" if self.current_lang == "id" else f"Your Version: v{APP_VERSION}"
        new_lbl = f"Versi Terbaru: v{new_ver}" if self.current_lang == "id" else f"Latest Version: v{new_ver}"
        tk.Label(v_box, text=cur_lbl, font=("Segoe UI", 9, "bold"), fg=th["text_secondary"], bg=th["card_bg"]).pack(side="left")
        tk.Label(v_box, text="  ➔  ", font=("Segoe UI", 9, "bold"), fg=th["accent_cyan"], bg=th["card_bg"]).pack(side="left")
        tk.Label(v_box, text=new_lbl, font=("Segoe UI", 9, "bold"), fg="#10b981", bg=th["card_bg"]).pack(side="left")

        cl_head = "Apa saja yang baru pada versi ini:" if self.current_lang == "id" else "What's new in this update:"
        tk.Label(body, text=cl_head, font=("Segoe UI", 9, "bold"), fg=th["text_primary"], bg=th["bg"]).pack(anchor="w", pady=(0, 4))

        cl_box = tk.Frame(body, bg=th["card_bg"], padx=12, pady=8, highlightthickness=1, highlightbackground=th["border"])
        cl_box.pack(fill="both", expand=True)

        for item in changelog:
            row = tk.Frame(cl_box, bg=th["card_bg"])
            row.pack(fill="x", anchor="w", pady=2)
            tk.Label(row, text="•", font=("Segoe UI", 9, "bold"), fg=th["accent_cyan"], bg=th["card_bg"]).pack(side="left", anchor="n", padx=(0, 6))
            tk.Label(row, text=item, font=("Segoe UI", 8), fg=th["text_primary"], bg=th["card_bg"], wraplength=440, justify="left").pack(side="left", fill="x", expand=True)

        ftr = tk.Frame(dialog, bg=th["card_bg"], padx=14, pady=12, highlightthickness=1, highlightbackground=th["border"])
        ftr.pack(fill="x", side="bottom")

        def _do_update():
            webbrowser.open(dl_url)
            dialog.destroy()

        btn_up_txt = "⬇ Unduh Pembaruan" if self.current_lang == "id" else "⬇ Download Update"
        btn_update = tk.Button(ftr, text=btn_up_txt, font=("Segoe UI", 9, "bold"), bg=th["accent"], fg="white", activebackground=th["accent_hover"], activeforeground="white", relief="flat", padx=14, pady=5, cursor="hand2", command=_do_update)
        btn_update.pack(side="right", padx=(6, 0))

        btn_gh_txt = "🌐 GitHub"
        btn_gh = tk.Button(ftr, text=btn_gh_txt, font=("Segoe UI", 8), bg=th["btn_bg"], fg=th["btn_fg"], relief="flat", padx=10, pady=5, cursor="hand2", command=lambda: webbrowser.open(GITHUB_REPO_URL))
        btn_gh.pack(side="right", padx=4)

        btn_can_txt = "Nanti Saja" if self.current_lang == "id" else "Later"
        btn_cancel = tk.Button(ftr, text=btn_can_txt, font=("Segoe UI", 8), bg=th["card_bg"], fg=th["text_secondary"], relief="flat", padx=10, pady=5, cursor="hand2", command=dialog.destroy)
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
                    if hasattr(self, 'clock_lbl') and self.clock_lbl.winfo_exists():
                        self.clock_lbl.config(text=t_str)
                    if hasattr(self, 'date_lbl') and self.date_lbl.winfo_exists():
                        self.date_lbl.config(text=d_str)
                except Exception:
                    pass

                # Alarm Trigger
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

                # Pomodoro Tick
                if self.pomodoro_is_running and self.pomodoro_seconds_left > 0:
                    self.pomodoro_seconds_left -= 1
                    if self.pomodoro_seconds_left == 0:
                        self.pomodoro_is_break = not self.pomodoro_is_break
                        self.pomodoro_total_sec = (5 * 60) if self.pomodoro_is_break else (25 * 60)
                        self.pomodoro_seconds_left = self.pomodoro_total_sec
                        play_audio_tone(self.current_tone)
                        try:
                            st_lbl = self.t("pomo_state_break") if self.pomodoro_is_break else self.t("pomo_state_work")
                            if hasattr(self, 'lbl_pomo_state') and self.lbl_pomo_state.winfo_exists():
                                self.lbl_pomo_state.config(text=st_lbl)
                        except Exception:
                            pass

                # Eye Rest Tick
                if self.eye_rest_enabled and self.eye_rest_seconds_left > 0:
                    self.eye_rest_seconds_left -= 1
                    if self.eye_rest_seconds_left == 0:
                        self.eye_rest_seconds_left = self.eye_interval_min * 60
                        play_audio_tone("bell")
                        try:
                            self.root.deiconify()
                            self.root.lift()
                        except Exception:
                            pass

                # Update Timer Canvas Rings if on timers tab
                try:
                    if self.current_nav == "timers":
                        self.root.after(0, self.update_timer_rings)
                except Exception:
                    pass

                time.sleep(1)

        t = threading.Thread(target=_loop, daemon=True)
        t.start()


def main():
    root = tk.Tk()
    app = ZzzleepDesktopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
