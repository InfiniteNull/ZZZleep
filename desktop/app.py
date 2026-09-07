#!/usr/bin/env python3
"""
ZZZleep — Desktop Calendar, Audio Alarm & Focus Timer (v1.2.0)
Author: Rizki Ananda, S.Kom (@InfiniteNull)
License: MIT
"""

import os
import sys
import json
import time
import math
import random
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
APP_VERSION = "1.2.0"
DATA_FILE = os.path.join(os.path.expanduser("~"), ".zzzleep_desktop_data.json")
UPDATE_MANIFEST_URL = "https://raw.githubusercontent.com/InfiniteNull/ZZZleep/main/version.json"
GITHUB_REPO_URL = "https://github.com/InfiniteNull/ZZZleep"
DIRECT_EXE_URL = "https://github.com/InfiniteNull/ZZZleep/raw/main/bin/ZZZleep.exe"

# Synthesized Harmonic Sound Tones (Frequencies in Hz)
TONES = {
    "gentle": "Arpeggio C-Mayor",
    "retro": "Digital Pulse (880/1760Hz)",
    "bell": "Harmonic Bell (440Hz)",
    "chime": "Ascending Chime (D-A)",
    "zen": "Zen Minimalist (520Hz)"
}

DAY_NAMES = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

# Built-in Indonesian Public Holidays & Joint Leaves (2025 - 2027)
HOLIDAYS_DB = {
    # 2025
    "2025-01-01": "New Year's Day 2025",
    "2025-01-27": "Isra Mi'raj Nabi Muhammad",
    "2025-01-29": "Chinese New Year 2576",
    "2025-03-29": "Hari Raya Nyepi 1947",
    "2025-03-31": "Idul Fitri 1446 H",
    "2025-04-01": "Idul Fitri 1446 H (Day 2)",
    "2025-04-18": "Good Friday",
    "2025-05-01": "International Labor Day",
    "2025-05-12": "Hari Raya Waisak 2569",
    "2025-05-29": "Ascension of Jesus Christ",
    "2025-06-01": "Pancasila Day",
    "2025-06-06": "Idul Adha 1446 H",
    "2025-06-27": "Islamic New Year 1447 H",
    "2025-08-17": "Indonesian Independence Day",
    "2025-09-05": "Maulid Nabi Muhammad SAW",
    "2025-12-25": "Christmas Day",
    # 2026
    "2026-01-01": "New Year's Day 2026",
    "2026-01-16": "Isra Mi'raj Nabi Muhammad",
    "2026-02-17": "Chinese New Year 2577",
    "2026-03-19": "Hari Raya Nyepi 1948",
    "2026-03-20": "Idul Fitri 1447 H",
    "2026-03-21": "Idul Fitri 1447 H (Day 2)",
    "2026-04-03": "Good Friday",
    "2026-05-01": "International Labor Day",
    "2026-05-14": "Ascension of Jesus Christ",
    "2026-05-27": "Idul Adha 1447 H",
    "2026-05-31": "Hari Raya Waisak 2570",
    "2026-06-01": "Pancasila Day",
    "2026-06-16": "Islamic New Year 1448 H",
    "2026-08-17": "Indonesian Independence Day (81st)",
    "2026-08-25": "Maulid Nabi Muhammad SAW",
    "2026-12-25": "Christmas Day",
    # 2027
    "2027-01-01": "New Year's Day 2027",
    "2027-01-05": "Isra Mi'raj Nabi Muhammad",
    "2027-02-06": "Chinese New Year 2578",
    "2027-03-09": "Idul Fitri 1448 H",
    "2027-03-10": "Idul Fitri 1448 H (Day 2)",
    "2027-03-26": "Good Friday",
    "2027-05-01": "International Labor Day",
    "2027-05-06": "Ascension of Jesus Christ",
    "2027-05-17": "Idul Adha 1448 H",
    "2027-05-20": "Hari Raya Waisak 2571",
    "2027-06-01": "Pancasila Day",
    "2027-06-06": "Islamic New Year 1449 H",
    "2027-08-15": "Maulid Nabi Muhammad SAW",
    "2027-08-17": "Indonesian Independence Day",
    "2027-12-25": "Christmas Day"
}

# Theme Color Definitions
THEMES = {
    "dark": {
        "bg": "#090d16",
        "sidebar_bg": "#0f172a",
        "card_bg": "#131c2e",
        "subcard_bg": "#0b1220",
        "ring_bg": "#1e293b",
        "text_primary": "#f8fafc",
        "text_secondary": "#94a3b8",
        "accent": "#0ea5e9",
        "accent_hover": "#0284c7",
        "accent_cyan": "#38bdf8",
        "border": "#1e293b",
        "border_subtle": "#334155",
        "btn_bg": "#1e293b",
        "btn_fg": "#f8fafc",
        "entry_bg": "#0b1220",
        "entry_fg": "#38bdf8",
        "nav_active_bg": "#0ea5e9",
        "nav_active_fg": "#ffffff",
        "nav_inactive_bg": "#0f172a",
        "nav_inactive_fg": "#94a3b8",
        "ring_pomo": "#f43f5e",
        "ring_eye": "#10b981",
        "holiday_bg": "#450a0a",
        "holiday_fg": "#f87171",
        "today_bg": "#0369a1",
        "today_fg": "#ffffff"
    },
    "light": {
        "bg": "#f8fafc",
        "sidebar_bg": "#ffffff",
        "card_bg": "#ffffff",
        "subcard_bg": "#f1f5f9",
        "ring_bg": "#e2e8f0",
        "text_primary": "#0f172a",
        "text_secondary": "#64748b",
        "accent": "#0284c7",
        "accent_hover": "#0369a1",
        "accent_cyan": "#0284c7",
        "border": "#e2e8f0",
        "border_subtle": "#cbd5e1",
        "btn_bg": "#f1f5f9",
        "btn_fg": "#1e293b",
        "entry_bg": "#f8fafc",
        "entry_fg": "#0284c7",
        "nav_active_bg": "#0284c7",
        "nav_active_fg": "#ffffff",
        "nav_inactive_bg": "#ffffff",
        "nav_inactive_fg": "#64748b",
        "ring_pomo": "#e11d48",
        "ring_eye": "#059669",
        "holiday_bg": "#fee2e2",
        "holiday_fg": "#dc2626",
        "today_bg": "#0284c7",
        "today_fg": "#ffffff"
    }
}


class ZZZleepApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} — Desktop Calendar, Alarm & Focus Timer")
        self.root.geometry("1040x650")
        self.root.minsize(860, 560)

        # State Variables
        self.is_mini = False
        self.normal_geom = "1040x650"
        self.current_tab = "alarms"  # "alarms" or "timers"
        self.cal_year = datetime.date.today().year
        self.cal_month = datetime.date.today().month
        self.selected_date = datetime.date.today().strftime("%Y-%m-%d")

        # Load Local Data
        self.load_data()
        self.theme_name = self.data.get("theme", "dark")
        self.colors = THEMES.get(self.theme_name, THEMES["dark"])

        # Pomodoro Engine State
        self.pomo_state = "stopped"  # "running", "paused", "stopped"
        self.pomo_mode = "work"      # "work" (25m) or "break" (5m)
        self.pomo_total_seconds = 25 * 60
        self.pomo_time_left = self.pomo_total_seconds
        self.pomo_last_tick = 0

        # Eye Rest 20-20-20 State
        self.eye_enabled = self.data.get("eye_enabled", True)
        self.eye_interval_min = self.data.get("eye_interval", 20)
        self.eye_time_left = self.eye_interval_min * 60

        # Math Challenge Dialog State
        self.active_math_dialog = None
        self.math_alarm_beeping = False

        # Build UI
        self.setup_styles()
        self.build_gui()

        # Background Daemons
        self.start_clock_thread()
        self.start_alarm_checker()
        self.start_eye_rest_checker()
        self.start_pomo_thread()

        # Background update check (runs quietly)
        threading.Thread(target=self.silent_check_update, daemon=True).start()

    # ==========================================
    # DATA PERSISTENCE & HELPERS
    # ==========================================
    def load_data(self):
        default_data = {
            "alarms": [
                {
                    "id": 1,
                    "time": "07:30",
                    "label": "Morning Standup",
                    "tone": "gentle",
                    "repeat": ["Mon", "Tue", "Wed", "Thu", "Fri"],
                    "enabled": True,
                    "skip_holiday": True,
                    "math_challenge": False
                }
            ],
            "memos": {},
            "pomo_stats": {},
            "theme": "dark",
            "eye_enabled": True,
            "eye_interval": 20,
            "default_tone": "gentle"
        }

        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
                    for k, v in default_data.items():
                        if k not in self.data:
                            self.data[k] = v
            except Exception:
                self.data = default_data
        else:
            self.data = default_data
            self.save_data()

    def save_data(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print("Error saving data:", e)

    def setup_styles(self):
        self.colors = THEMES.get(self.theme_name, THEMES["dark"])
        self.root.configure(bg=self.colors["bg"])

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TCombobox",
                        fieldbackground=self.colors["entry_bg"],
                        background=self.colors["btn_bg"],
                        foreground=self.colors["text_primary"],
                        arrowcolor=self.colors["accent_cyan"],
                        bordercolor=self.colors["border"])

        style.map("TCombobox",
                  fieldbackground=[("readonly", self.colors["entry_bg"])],
                  foreground=[("readonly", self.colors["text_primary"])])

    def toggle_theme(self):
        self.theme_name = "light" if self.theme_name == "dark" else "dark"
        self.data["theme"] = self.theme_name
        self.save_data()
        self.setup_styles()
        self.refresh_ui()

    # ==========================================
    # SOUND SYNTHESIS ENGINE
    # ==========================================
    def play_tone(self, tone_name="gentle"):
        def _play():
            if not HAS_WINSOUND:
                return
            try:
                if tone_name == "gentle":
                    # Arpeggio C-Mayor (C5, E5, G5, C6)
                    for freq, dur in [(523, 140), (659, 140), (784, 140), (1046, 320)]:
                        winsound.Beep(freq, dur)
                        time.sleep(0.04)
                elif tone_name == "retro":
                    # Fast pulse double-beep (880Hz / 1760Hz)
                    winsound.Beep(880, 80)
                    winsound.Beep(1760, 160)
                    time.sleep(0.06)
                    winsound.Beep(1760, 200)
                elif tone_name == "bell":
                    # Bell chime (A4 440Hz -> E5 659Hz)
                    winsound.Beep(440, 220)
                    winsound.Beep(659, 360)
                elif tone_name == "chime":
                    # Ascending notes (D5, F#5, A5)
                    for freq, dur in [(587, 120), (740, 120), (880, 260)]:
                        winsound.Beep(freq, dur)
                        time.sleep(0.03)
                elif tone_name == "zen":
                    # Deep minimal pulse
                    winsound.Beep(520, 480)
                else:
                    winsound.Beep(523, 300)
            except Exception as e:
                print("Sound error:", e)

        threading.Thread(target=_play, daemon=True).start()

    # ==========================================
    # HOLIDAY & CALENDAR UTILITIES
    # ==========================================
    def is_holiday(self, date_obj):
        """Returns (is_holiday_bool, holiday_name_str)"""
        date_str = date_obj.strftime("%Y-%m-%d")
        if date_str in HOLIDAYS_DB:
            return True, HOLIDAYS_DB[date_str]
        # Sundays are standard rest days
        if date_obj.weekday() == 6:
            return True, "Sunday Rest Day"
        return False, ""

    def get_upcoming_holiday(self):
        """Find the earliest upcoming public holiday from today"""
        today = datetime.date.today()
        upcoming = []
        for d_str, name in HOLIDAYS_DB.items():
            try:
                d_obj = datetime.datetime.strptime(d_str, "%Y-%m-%d").date()
                if d_obj >= today:
                    days_diff = (d_obj - today).days
                    upcoming.append((days_diff, d_obj, name))
            except ValueError:
                continue
        upcoming.sort(key=lambda x: x[0])
        if upcoming:
            return upcoming[0]
        return None

    def get_month_long_weekends(self, year, month):
        """Detect any 3+ consecutive rest days in the given month"""
        num_days = calendar.monthrange(year, month)[1]
        rest_days = set()
        for day in range(1, num_days + 1):
            d_obj = datetime.date(year, month, day)
            is_hol, _ = self.is_holiday(d_obj)
            if is_hol or d_obj.weekday() in (5, 6):  # Saturday or Sunday or Holiday
                rest_days.add(day)

        # Find consecutive streaks of 3 or more
        long_weekends = []
        streak = []
        for day in range(1, num_days + 1):
            if day in rest_days:
                streak.append(day)
            else:
                if len(streak) >= 3:
                    long_weekends.append((streak[0], streak[-1], len(streak)))
                streak = []
        if len(streak) >= 3:
            long_weekends.append((streak[0], streak[-1], len(streak)))
        return long_weekends

    # ==========================================
    # GUI LAYOUT & COMPONENT BUILDERS
    # ==========================================
    def build_gui(self):
        # Clear root
        for child in self.root.winfo_children():
            child.destroy()

        self.root.configure(bg=self.colors["bg"])

        # Main Outer Container
        self.main_container = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Top Header Bar
        self.build_header(self.main_container)

        # Content Area with Sidebar
        body_frame = tk.Frame(self.main_container, bg=self.colors["bg"])
        body_frame.pack(fill=tk.BOTH, expand=True)

        # Left Sidebar Navigation
        self.build_sidebar(body_frame)

        # Main Dynamic View Container
        self.content_area = tk.Frame(body_frame, bg=self.colors["bg"], padx=14, pady=10)
        self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Render Active Tab
        self.render_active_tab()

    def build_header(self, parent):
        header = tk.Frame(parent, bg=self.colors["sidebar_bg"], height=52,
                          highlightthickness=1, highlightbackground=self.colors["border"])
        header.pack(side=tk.TOP, fill=tk.X)
        header.pack_propagate(False)

        # Left: Brand & Live Clock
        left_box = tk.Frame(header, bg=self.colors["sidebar_bg"])
        left_box.pack(side=tk.LEFT, padx=16, pady=8)

        brand_lbl = tk.Label(left_box, text=f"⏰ {APP_NAME}", font=("Segoe UI", 12, "bold"),
                             fg=self.colors["accent_cyan"], bg=self.colors["sidebar_bg"])
        brand_lbl.pack(side=tk.LEFT, padx=(0, 14))

        self.clock_lbl = tk.Label(left_box, text="--:--:--", font=("Segoe UI", 11, "bold"),
                                  fg=self.colors["text_primary"], bg=self.colors["sidebar_bg"])
        self.clock_lbl.pack(side=tk.LEFT, padx=(0, 10))

        self.date_lbl = tk.Label(left_box, text="---, -- --- ----", font=("Segoe UI", 9),
                                 fg=self.colors["text_secondary"], bg=self.colors["sidebar_bg"])
        self.date_lbl.pack(side=tk.LEFT)

        # Right: Quick Action Buttons (Mini Widget, Theme Toggle)
        right_box = tk.Frame(header, bg=self.colors["sidebar_bg"])
        right_box.pack(side=tk.RIGHT, padx=14, pady=8)

        # Mini Widget Button
        widget_btn = tk.Button(right_box, text="📌 Mini Widget", font=("Segoe UI", 9, "bold"),
                               bg=self.colors["btn_bg"], fg=self.colors["accent_cyan"],
                               activebackground=self.colors["accent"], activeforeground="#ffffff",
                               relief=tk.FLAT, bd=0, padx=10, pady=3, cursor="hand2",
                               command=self.toggle_mini_widget)
        widget_btn.pack(side=tk.LEFT, padx=4)

        # Theme Switcher
        theme_icon = "☀️ Light" if self.theme_name == "dark" else "🌙 Dark"
        theme_btn = tk.Button(right_box, text=theme_icon, font=("Segoe UI", 9, "bold"),
                              bg=self.colors["btn_bg"], fg=self.colors["text_primary"],
                              activebackground=self.colors["border_subtle"],
                              relief=tk.FLAT, bd=0, padx=10, pady=3, cursor="hand2",
                              command=self.toggle_theme)
        theme_btn.pack(side=tk.LEFT, padx=4)

    def build_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=self.colors["sidebar_bg"], width=190,
                           highlightthickness=1, highlightbackground=self.colors["border"])
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        # Navigation Buttons Box
        nav_box = tk.Frame(sidebar, bg=self.colors["sidebar_bg"])
        nav_box.pack(side=tk.TOP, fill=tk.X, padx=10, pady=16)

        # Tab 1: Alarms & Calendar
        self.btn_nav_alarms = self.create_nav_item(nav_box, "⏰  Alarms & Calendar", "alarms")
        self.btn_nav_alarms.pack(fill=tk.X, pady=3)

        # Tab 2: Focus Timers & Stats
        self.btn_nav_timers = self.create_nav_item(nav_box, "⏱️  Focus Timers & Stats", "timers")
        self.btn_nav_timers.pack(fill=tk.X, pady=3)

        # Bottom Footer: Subtle Status & Version Pill
        footer_box = tk.Frame(sidebar, bg=self.colors["sidebar_bg"])
        footer_box.pack(side=tk.BOTTOM, fill=tk.X, padx=12, pady=12)

        # Holiday Info summary badge
        up_hol = self.get_upcoming_holiday()
        hol_txt = f"🎉 {up_hol[2][:16]} ({up_hol[0]}d)" if up_hol else "✨ No upcoming holiday"
        hol_lbl = tk.Label(footer_box, text=hol_txt, font=("Segoe UI", 8),
                           fg=self.colors["text_secondary"], bg=self.colors["sidebar_bg"],
                           wraplength=160, justify=tk.LEFT)
        hol_lbl.pack(anchor="w", pady=(0, 6))

        # Version & Up to Date pill (clean & small)
        ver_lbl = tk.Label(footer_box, text=f"v{APP_VERSION} • Up to date", font=("Segoe UI", 8),
                           fg=self.colors["accent_cyan"], bg=self.colors["sidebar_bg"])
        ver_lbl.pack(anchor="w")

    def create_nav_item(self, parent, text, key):
        is_active = (self.current_tab == key)
        bg_col = self.colors["nav_active_bg"] if is_active else self.colors["nav_inactive_bg"]
        fg_col = self.colors["nav_active_fg"] if is_active else self.colors["nav_inactive_fg"]

        btn = tk.Button(parent, text=text, font=("Segoe UI", 9, "bold" if is_active else "normal"),
                        bg=bg_col, fg=fg_col,
                        activebackground=self.colors["accent_hover"],
                        activeforeground="#ffffff",
                        relief=tk.FLAT, bd=0, padx=12, pady=8, anchor="w", cursor="hand2",
                        command=lambda k=key: self.switch_nav(k))
        return btn

    def switch_nav(self, key):
        if self.current_tab != key:
            self.current_tab = key
            self.refresh_ui()

    def refresh_ui(self):
        self.build_gui()

    # ==========================================
    # TAB 1: ALARMS & INTERACTIVE CALENDAR
    # ==========================================
    def render_active_tab(self):
        for child in self.content_area.winfo_children():
            child.destroy()

        if self.current_tab == "alarms":
            self.render_alarms_view()
        elif self.current_tab == "timers":
            self.render_timers_view()

    def render_alarms_view(self):
        # 2-Column Grid
        grid_frame = tk.Frame(self.content_area, bg=self.colors["bg"])
        grid_frame.pack(fill=tk.BOTH, expand=True)

        left_col = tk.Frame(grid_frame, bg=self.colors["bg"])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

        right_col = tk.Frame(grid_frame, bg=self.colors["bg"], width=420)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(8, 0))

        # --- LEFT: NEW ALARM FORM & ACTIVE LIST ---
        form_card = tk.Frame(left_col, bg=self.colors["card_bg"],
                             highlightthickness=1, highlightbackground=self.colors["border"], padx=14, pady=12)
        form_card.pack(fill=tk.X, pady=(0, 10))

        lbl_head = tk.Label(form_card, text="ALARM SCHEDULER", font=("Segoe UI", 10, "bold"),
                            fg=self.colors["accent_cyan"], bg=self.colors["card_bg"])
        lbl_head.pack(anchor="w", pady=(0, 8))

        # Dual Spinbox Time Picker with Permanent ':' separator
        time_picker_frame = tk.Frame(form_card, bg=self.colors["card_bg"])
        time_picker_frame.pack(fill=tk.X, pady=(0, 6))

        tk.Label(time_picker_frame, text="Time:", font=("Segoe UI", 9, "bold"),
                 fg=self.colors["text_primary"], bg=self.colors["card_bg"]).pack(side=tk.LEFT, padx=(0, 8))

        self.spin_hour = tk.Spinbox(time_picker_frame, from_=0, to=23, wrap=True, width=3,
                                    format="%02.0f", font=("Segoe UI", 12, "bold"),
                                    bg=self.colors["entry_bg"], fg=self.colors["entry_fg"],
                                    buttonbackground=self.colors["btn_bg"], bd=1, relief=tk.SOLID,
                                    justify=tk.CENTER)
        self.spin_hour.delete(0, "end")
        self.spin_hour.insert(0, "07")
        self.spin_hour.pack(side=tk.LEFT)

        colon_lbl = tk.Label(time_picker_frame, text=" : ", font=("Segoe UI", 14, "bold"),
                             fg=self.colors["accent_cyan"], bg=self.colors["card_bg"])
        colon_lbl.pack(side=tk.LEFT, padx=2)

        self.spin_min = tk.Spinbox(time_picker_frame, from_=0, to=59, wrap=True, width=3,
                                   format="%02.0f", font=("Segoe UI", 12, "bold"),
                                   bg=self.colors["entry_bg"], fg=self.colors["entry_fg"],
                                   buttonbackground=self.colors["btn_bg"], bd=1, relief=tk.SOLID,
                                   justify=tk.CENTER)
        self.spin_min.delete(0, "end")
        self.spin_min.insert(0, "30")
        self.spin_min.pack(side=tk.LEFT)

        # Quick Preset Chips
        presets_frame = tk.Frame(time_picker_frame, bg=self.colors["card_bg"])
        presets_frame.pack(side=tk.RIGHT)
        for t_str in ["06:00", "07:30", "09:00", "22:00"]:
            btn_pre = tk.Button(presets_frame, text=t_str, font=("Segoe UI", 8),
                                bg=self.colors["btn_bg"], fg=self.colors["text_primary"],
                                activebackground=self.colors["accent"], activeforeground="#ffffff",
                                relief=tk.FLAT, bd=0, padx=5, pady=2, cursor="hand2",
                                command=lambda s=t_str: self.apply_preset_time(s))
            btn_pre.pack(side=tk.LEFT, padx=2)

        # Alarm Label Entry
        lbl_box = tk.Frame(form_card, bg=self.colors["card_bg"])
        lbl_box.pack(fill=tk.X, pady=(0, 6))
        tk.Label(lbl_box, text="Label:", font=("Segoe UI", 9),
                 fg=self.colors["text_secondary"], bg=self.colors["card_bg"]).pack(side=tk.LEFT, padx=(0, 8))
        self.entry_label = tk.Entry(lbl_box, font=("Segoe UI", 9),
                                    bg=self.colors["entry_bg"], fg=self.colors["text_primary"],
                                    insertbackground=self.colors["text_primary"],
                                    bd=1, relief=tk.SOLID)
        self.entry_label.insert(0, "Work Standup")
        self.entry_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Tone Selector with Live Preview Button
        tone_box = tk.Frame(form_card, bg=self.colors["card_bg"])
        tone_box.pack(fill=tk.X, pady=(0, 6))
        tk.Label(tone_box, text="Tone:", font=("Segoe UI", 9),
                 fg=self.colors["text_secondary"], bg=self.colors["card_bg"]).pack(side=tk.LEFT, padx=(0, 10))

        self.tone_var = tk.StringVar(value="gentle")
        tone_names_list = list(TONES.keys())
        tone_combo = ttk.Combobox(tone_box, textvariable=self.tone_var, values=tone_names_list,
                                  state="readonly", width=15, font=("Segoe UI", 9))
        tone_combo.pack(side=tk.LEFT, padx=(0, 8))

        test_tone_btn = tk.Button(tone_box, text="🔊 Test", font=("Segoe UI", 8, "bold"),
                                  bg=self.colors["btn_bg"], fg=self.colors["accent_cyan"],
                                  activebackground=self.colors["accent"], activeforeground="#ffffff",
                                  relief=tk.FLAT, bd=0, padx=8, pady=2, cursor="hand2",
                                  command=lambda: self.play_tone(self.tone_var.get()))
        test_tone_btn.pack(side=tk.LEFT)

        # Repeat Days Pills
        days_box = tk.Frame(form_card, bg=self.colors["card_bg"])
        days_box.pack(fill=tk.X, pady=(0, 8))
        tk.Label(days_box, text="Repeat:", font=("Segoe UI", 9),
                 fg=self.colors["text_secondary"], bg=self.colors["card_bg"]).pack(side=tk.LEFT, padx=(0, 6))

        self.repeat_vars = {}
        for d in DAY_NAMES:
            var = tk.BooleanVar(value=(d not in ["Sun", "Sat"]))  # Default Mon-Fri
            self.repeat_vars[d] = var
            chk = tk.Checkbutton(days_box, text=d, variable=var, font=("Segoe UI", 8),
                                 bg=self.colors["card_bg"], fg=self.colors["text_primary"],
                                 activebackground=self.colors["card_bg"],
                                 selectcolor=self.colors["entry_bg"], cursor="hand2")
            chk.pack(side=tk.LEFT, padx=1)

        # Smart Options: Skip Holiday & Math Challenge Checkboxes
        opts_box = tk.Frame(form_card, bg=self.colors["card_bg"])
        opts_box.pack(fill=tk.X, pady=(0, 10))

        self.var_skip_hol = tk.BooleanVar(value=True)
        chk_hol = tk.Checkbutton(opts_box, text="Skip on Public Holidays", variable=self.var_skip_hol,
                                 font=("Segoe UI", 8, "bold"),
                                 bg=self.colors["card_bg"], fg=self.colors["holiday_fg"],
                                 activebackground=self.colors["card_bg"],
                                 selectcolor=self.colors["entry_bg"], cursor="hand2")
        chk_hol.pack(side=tk.LEFT, padx=(0, 12))

        self.var_math_chal = tk.BooleanVar(value=False)
        chk_math = tk.Checkbutton(opts_box, text="Math Challenge to Dismiss", variable=self.var_math_chal,
                                  font=("Segoe UI", 8),
                                  bg=self.colors["card_bg"], fg=self.colors["accent_cyan"],
                                  activebackground=self.colors["card_bg"],
                                  selectcolor=self.colors["entry_bg"], cursor="hand2")
        chk_math.pack(side=tk.LEFT)

        # Add Alarm Button
        add_btn = tk.Button(form_card, text="+ Add Alarm", font=("Segoe UI", 9, "bold"),
                            bg=self.colors["accent"], fg="#ffffff",
                            activebackground=self.colors["accent_hover"], activeforeground="#ffffff",
                            relief=tk.FLAT, bd=0, padx=14, pady=6, cursor="hand2",
                            command=self.add_alarm)
        add_btn.pack(anchor="e")

        # Active Alarms List Card
        list_card = tk.Frame(left_col, bg=self.colors["card_bg"],
                             highlightthickness=1, highlightbackground=self.colors["border"], padx=14, pady=10)
        list_card.pack(fill=tk.BOTH, expand=True)

        lbl_list = tk.Label(list_card, text="ACTIVE ALARMS", font=("Segoe UI", 10, "bold"),
                            fg=self.colors["accent_cyan"], bg=self.colors["card_bg"])
        lbl_list.pack(anchor="w", pady=(0, 6))

        self.alarms_scroll_frame = tk.Frame(list_card, bg=self.colors["card_bg"])
        self.alarms_scroll_frame.pack(fill=tk.BOTH, expand=True)

        self.render_alarms_list()

        # --- RIGHT: INTERACTIVE CALENDAR & HOLIDAYS ---
        cal_card = tk.Frame(right_col, bg=self.colors["card_bg"],
                            highlightthickness=1, highlightbackground=self.colors["border"], padx=14, pady=12)
        cal_card.pack(fill=tk.BOTH, expand=True)

        self.render_calendar_component(cal_card)

    def apply_preset_time(self, t_str):
        h, m = t_str.split(":")
        self.spin_hour.delete(0, "end")
        self.spin_hour.insert(0, h)
        self.spin_min.delete(0, "end")
        self.spin_min.insert(0, m)

    def add_alarm(self):
        try:
            h = int(self.spin_hour.get())
            m = int(self.spin_min.get())
            if not (0 <= h <= 23 and 0 <= m <= 59):
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Time", "Please enter a valid hour (00-23) and minute (00-59).")
            return

        t_str = f"{h:02d}:{m:02d}"
        label = self.entry_label.get().strip() or "Alarm"
        tone = self.tone_var.get()
        repeat = [d for d, v in self.repeat_vars.items() if v.get()]
        if not repeat:
            repeat = list(DAY_NAMES)

        new_item = {
            "id": int(time.time() * 1000),
            "time": t_str,
            "label": label,
            "tone": tone,
            "repeat": repeat,
            "enabled": True,
            "skip_holiday": self.var_skip_hol.get(),
            "math_challenge": self.var_math_chal.get()
        }

        self.data["alarms"].append(new_item)
        self.save_data()
        self.render_alarms_list()

    def render_alarms_list(self):
        for w in self.alarms_scroll_frame.winfo_children():
            w.destroy()

        if not self.data["alarms"]:
            tk.Label(self.alarms_scroll_frame, text="No active alarms configured.",
                     font=("Segoe UI", 9, "italic"),
                     fg=self.colors["text_secondary"], bg=self.colors["card_bg"]).pack(pady=12)
            return

        for al in self.data["alarms"]:
            row = tk.Frame(self.alarms_scroll_frame, bg=self.colors["subcard_bg"],
                           highlightthickness=1, highlightbackground=self.colors["border"],
                           padx=10, pady=6)
            row.pack(fill=tk.X, pady=3)

            # Left: Time & Label
            left_info = tk.Frame(row, bg=self.colors["subcard_bg"])
            left_info.pack(side=tk.LEFT, fill=tk.X, expand=True)

            t_lbl = tk.Label(left_info, text=al["time"], font=("Segoe UI", 11, "bold"),
                             fg=self.colors["accent_cyan"] if al["enabled"] else self.colors["text_secondary"],
                             bg=self.colors["subcard_bg"])
            t_lbl.pack(anchor="w")

            tag_txt = al["label"]
            if al.get("skip_holiday"):
                tag_txt += " • 🏖️ Skip Holiday"
            if al.get("math_challenge"):
                tag_txt += " • 🧠 Math"

            sub_lbl = tk.Label(left_info, text=tag_txt, font=("Segoe UI", 8),
                               fg=self.colors["text_secondary"], bg=self.colors["subcard_bg"])
            sub_lbl.pack(anchor="w")

            # Right: Toggle & Delete
            right_ctrl = tk.Frame(row, bg=self.colors["subcard_bg"])
            right_ctrl.pack(side=tk.RIGHT)

            status_btn = tk.Button(right_ctrl,
                                   text="ACTIVE" if al["enabled"] else "OFF",
                                   font=("Segoe UI", 8, "bold"),
                                   bg=self.colors["ring_eye"] if al["enabled"] else self.colors["btn_bg"],
                                   fg="#ffffff" if al["enabled"] else self.colors["text_secondary"],
                                   relief=tk.FLAT, bd=0, padx=8, pady=2, cursor="hand2",
                                   command=lambda a=al: self.toggle_alarm_status(a))
            status_btn.pack(side=tk.LEFT, padx=3)

            del_btn = tk.Button(right_ctrl, text="✕", font=("Segoe UI", 8, "bold"),
                                bg=self.colors["btn_bg"], fg=self.colors["ring_pomo"],
                                relief=tk.FLAT, bd=0, padx=6, pady=2, cursor="hand2",
                                command=lambda a=al: self.delete_alarm(a))
            del_btn.pack(side=tk.LEFT)

    def toggle_alarm_status(self, alarm_item):
        alarm_item["enabled"] = not alarm_item["enabled"]
        self.save_data()
        self.render_alarms_list()

    def delete_alarm(self, alarm_item):
        self.data["alarms"] = [a for a in self.data["alarms"] if a["id"] != alarm_item["id"]]
        self.save_data()
        self.render_alarms_list()

    # ==========================================
    # CALENDAR, HOLIDAYS & D-DAY COMPONENT
    # ==========================================
    def render_calendar_component(self, parent):
        for w in parent.winfo_children():
            w.destroy()

        # Month Navigation Bar
        nav_cal = tk.Frame(parent, bg=self.colors["card_bg"])
        nav_cal.pack(fill=tk.X, pady=(0, 6))

        month_name = calendar.month_name[self.cal_month]
        lbl_m = tk.Label(nav_cal, text=f"{month_name.upper()} {self.cal_year}", font=("Segoe UI", 10, "bold"),
                         fg=self.colors["accent_cyan"], bg=self.colors["card_bg"])
        lbl_m.pack(side=tk.LEFT)

        nav_btns = tk.Frame(nav_cal, bg=self.colors["card_bg"])
        nav_btns.pack(side=tk.RIGHT)

        btn_prev = tk.Button(nav_btns, text="◀", font=("Segoe UI", 8),
                             bg=self.colors["btn_bg"], fg=self.colors["text_primary"],
                             relief=tk.FLAT, bd=0, padx=6, pady=2, cursor="hand2",
                             command=self.prev_month)
        btn_prev.pack(side=tk.LEFT, padx=2)

        btn_today = tk.Button(nav_btns, text="Today", font=("Segoe UI", 8),
                              bg=self.colors["btn_bg"], fg=self.colors["text_primary"],
                              relief=tk.FLAT, bd=0, padx=6, pady=2, cursor="hand2",
                              command=self.reset_cal_today)
        btn_today.pack(side=tk.LEFT, padx=2)

        btn_next = tk.Button(nav_btns, text="▶", font=("Segoe UI", 8),
                             bg=self.colors["btn_bg"], fg=self.colors["text_primary"],
                             relief=tk.FLAT, bd=0, padx=6, pady=2, cursor="hand2",
                             command=self.next_month)
        btn_next.pack(side=tk.LEFT, padx=2)

        # Long Weekend Banner (if any detected this month)
        lw_list = self.get_month_long_weekends(self.cal_year, self.cal_month)
        if lw_list:
            lw_text = f"🏖️ Long Weekend: {lw_list[0][0]}-{lw_list[0][1]} {month_name[:3]} ({lw_list[0][2]} Days Off)"
            lw_banner = tk.Label(parent, text=lw_text, font=("Segoe UI", 8, "bold"),
                                 bg=self.colors["holiday_bg"], fg=self.colors["holiday_fg"],
                                 padx=6, pady=2)
            lw_banner.pack(fill=tk.X, pady=(0, 6))

        # Day Headers (Sun - Sat)
        grid_container = tk.Frame(parent, bg=self.colors["card_bg"])
        grid_container.pack(fill=tk.BOTH, expand=True)

        for col_idx, d_name in enumerate(DAY_NAMES):
            fg_head = self.colors["holiday_fg"] if d_name == "Sun" else self.colors["text_secondary"]
            lbl_d = tk.Label(grid_container, text=d_name, font=("Segoe UI", 8, "bold"),
                             fg=fg_head, bg=self.colors["card_bg"], width=4)
            lbl_d.grid(row=0, column=col_idx, pady=2, sticky="nsew")

        # Calendar Date Grid Calculation
        cal_matrix = calendar.monthcalendar(self.cal_year, self.cal_month)
        today_obj = datetime.date.today()

        for row_idx, week in enumerate(cal_matrix):
            # Calendar module has weeks starting Monday; we re-align to Sunday:
            # Shift Sunday from index 6 to index 0:
            sunday_first_week = [week[6]] + week[0:6]

            for col_idx, day_num in enumerate(sunday_first_week):
                if day_num == 0:
                    lbl_empty = tk.Label(grid_container, text="", bg=self.colors["card_bg"], width=4)
                    lbl_empty.grid(row=row_idx + 1, column=col_idx, padx=1, pady=1, sticky="nsew")
                else:
                    d_obj = datetime.date(self.cal_year, self.cal_month, day_num)
                    d_str = d_obj.strftime("%Y-%m-%d")
                    is_today = (d_obj == today_obj)
                    is_hol, hol_name = self.is_holiday(d_obj)
                    has_memo = d_str in self.data.get("memos", {})

                    # Color assignment
                    if is_today:
                        bg_d = self.colors["today_bg"]
                        fg_d = self.colors["today_fg"]
                    elif is_hol:
                        bg_d = self.colors["holiday_bg"]
                        fg_d = self.colors["holiday_fg"]
                    else:
                        bg_d = self.colors["subcard_bg"]
                        fg_d = self.colors["text_primary"]

                    day_text = f"{day_num}"
                    if has_memo:
                        day_text += " •"

                    btn_day = tk.Button(grid_container, text=day_text, font=("Segoe UI", 8, "bold" if (is_today or is_hol) else "normal"),
                                        bg=bg_d, fg=fg_d, activebackground=self.colors["accent"], activeforeground="#ffffff",
                                        relief=tk.FLAT, bd=0, padx=2, pady=2, cursor="hand2",
                                        command=lambda ds=d_str, hn=hol_name: self.select_calendar_date(ds, hn))
                    btn_day.grid(row=row_idx + 1, column=col_idx, padx=1, pady=1, sticky="nsew")

        for i in range(7):
            grid_container.columnconfigure(i, weight=1)

        # Selected Date Info & Quick Memo Card (Bottom of Calendar)
        info_frame = tk.Frame(parent, bg=self.colors["subcard_bg"],
                              highlightthickness=1, highlightbackground=self.colors["border"],
                              padx=10, pady=8)
        info_frame.pack(fill=tk.X, pady=(10, 0))

        d_sel_obj = datetime.datetime.strptime(self.selected_date, "%Y-%m-%d").date()
        is_sel_hol, sel_hol_name = self.is_holiday(d_sel_obj)
        memo_txt = self.data.get("memos", {}).get(self.selected_date, "")

        title_sel = d_sel_obj.strftime("%A, %d %B %Y")
        if is_sel_hol:
            title_sel += f" — {sel_hol_name}"

        tk.Label(info_frame, text=title_sel, font=("Segoe UI", 8, "bold"),
                 fg=self.colors["holiday_fg"] if is_sel_hol else self.colors["accent_cyan"],
                 bg=self.colors["subcard_bg"], wraplength=380, justify=tk.LEFT).pack(anchor="w")

        memo_lbl_txt = f"📝 Note: {memo_txt}" if memo_txt else "Click below to add a quick daily note."
        tk.Label(info_frame, text=memo_lbl_txt, font=("Segoe UI", 8),
                 fg=self.colors["text_secondary"], bg=self.colors["subcard_bg"],
                 wraplength=380, justify=tk.LEFT).pack(anchor="w", pady=(2, 4))

        btn_memo = tk.Button(info_frame, text="✏️ Edit Note for Date", font=("Segoe UI", 8),
                             bg=self.colors["btn_bg"], fg=self.colors["text_primary"],
                             relief=tk.FLAT, bd=0, padx=8, pady=2, cursor="hand2",
                             command=self.open_memo_dialog)
        btn_memo.pack(anchor="e")

    def prev_month(self):
        if self.cal_month == 1:
            self.cal_month = 12
            self.cal_year -= 1
        else:
            self.cal_month -= 1
        if self.current_tab == "alarms":
            self.render_alarms_view()

    def next_month(self):
        if self.cal_month == 12:
            self.cal_month = 1
            self.cal_year += 1
        else:
            self.cal_month += 1
        if self.current_tab == "alarms":
            self.render_alarms_view()

    def reset_cal_today(self):
        today = datetime.date.today()
        self.cal_year = today.year
        self.cal_month = today.month
        self.selected_date = today.strftime("%Y-%m-%d")
        if self.current_tab == "alarms":
            self.render_alarms_view()

    def select_calendar_date(self, date_str, holiday_name):
        self.selected_date = date_str
        if self.current_tab == "alarms":
            self.render_alarms_view()

    def open_memo_dialog(self):
        dlg = tk.Toplevel(self.root)
        dlg.title(f"Note — {self.selected_date}")
        dlg.geometry("360x180")
        dlg.configure(bg=self.colors["card_bg"])
        dlg.transient(self.root)
        dlg.grab_set()

        tk.Label(dlg, text=f"Daily Memo for {self.selected_date}:", font=("Segoe UI", 9, "bold"),
                 fg=self.colors["accent_cyan"], bg=self.colors["card_bg"]).pack(padx=14, pady=(14, 6), anchor="w")

        curr_note = self.data.get("memos", {}).get(self.selected_date, "")
        txt_entry = tk.Entry(dlg, font=("Segoe UI", 9), bg=self.colors["entry_bg"],
                             fg=self.colors["text_primary"], insertbackground=self.colors["text_primary"],
                             bd=1, relief=tk.SOLID)
        txt_entry.insert(0, curr_note)
        txt_entry.pack(fill=tk.X, padx=14, pady=6)
        txt_entry.focus_set()

        btn_box = tk.Frame(dlg, bg=self.colors["card_bg"])
        btn_box.pack(fill=tk.X, padx=14, pady=10)

        def save_note():
            val = txt_entry.get().strip()
            if "memos" not in self.data:
                self.data["memos"] = {}
            if val:
                self.data["memos"][self.selected_date] = val
            else:
                self.data["memos"].pop(self.selected_date, None)
            self.save_data()
            dlg.destroy()
            if self.current_tab == "alarms":
                self.render_alarms_view()

        tk.Button(btn_box, text="Save Note", font=("Segoe UI", 9, "bold"),
                  bg=self.colors["accent"], fg="#ffffff", relief=tk.FLAT, bd=0, padx=12, pady=4,
                  command=save_note).pack(side=tk.RIGHT, padx=4)

        tk.Button(btn_box, text="Cancel", font=("Segoe UI", 9),
                  bg=self.colors["btn_bg"], fg=self.colors["text_primary"], relief=tk.FLAT, bd=0, padx=10, pady=4,
                  command=dlg.destroy).pack(side=tk.RIGHT)

    # ==========================================
    # TAB 2: FOCUS TIMERS & WEEKLY ANALYTICS
    # ==========================================
    def render_timers_view(self):
        container = tk.Frame(self.content_area, bg=self.colors["bg"])
        container.pack(fill=tk.BOTH, expand=True)

        # Top Row: Dual Circular Progress Rings (Pomodoro & Eye Rest)
        top_row = tk.Frame(container, bg=self.colors["bg"])
        top_row.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # --- Card 1: Pomodoro 25/5 Timer ---
        pomo_card = tk.Frame(top_row, bg=self.colors["card_bg"],
                             highlightthickness=1, highlightbackground=self.colors["border"], padx=14, pady=12)
        pomo_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

        tk.Label(pomo_card, text="POMODORO FOCUS ENGINE", font=("Segoe UI", 10, "bold"),
                 fg=self.colors["ring_pomo"], bg=self.colors["card_bg"]).pack(anchor="w")

        state_txt = "WORK SESSION (25m)" if self.pomo_mode == "work" else "BREAK REST (5m)"
        tk.Label(pomo_card, text=state_txt, font=("Segoe UI", 8),
                 fg=self.colors["text_secondary"], bg=self.colors["card_bg"]).pack(anchor="w", pady=(0, 6))

        self.pomo_canvas = tk.Canvas(pomo_card, width=170, height=170, bg=self.colors["card_bg"],
                                     highlightthickness=0)
        self.pomo_canvas.pack(pady=4)
        self.draw_circular_progress(self.pomo_canvas, self.pomo_time_left, self.pomo_total_seconds,
                                    self.colors["ring_pomo"], f"{self.pomo_time_left//60:02d}:{self.pomo_time_left%60:02d}")

        # Controls
        ctrl_box = tk.Frame(pomo_card, bg=self.colors["card_bg"])
        ctrl_box.pack(pady=6)

        if self.pomo_state == "running":
            btn_play = tk.Button(ctrl_box, text="⏸ Pause", font=("Segoe UI", 9, "bold"),
                                 bg=self.colors["btn_bg"], fg=self.colors["text_primary"],
                                 relief=tk.FLAT, bd=0, padx=12, pady=4, cursor="hand2",
                                 command=self.pomo_pause)
        else:
            btn_play = tk.Button(ctrl_box, text="▶ Start", font=("Segoe UI", 9, "bold"),
                                 bg=self.colors["accent"], fg="#ffffff",
                                 relief=tk.FLAT, bd=0, padx=12, pady=4, cursor="hand2",
                                 command=self.pomo_start)
        btn_play.pack(side=tk.LEFT, padx=4)

        btn_rst = tk.Button(ctrl_box, text="↺ Reset", font=("Segoe UI", 9),
                            bg=self.colors["btn_bg"], fg=self.colors["text_secondary"],
                            relief=tk.FLAT, bd=0, padx=10, pady=4, cursor="hand2",
                            command=self.pomo_reset)
        btn_rst.pack(side=tk.LEFT, padx=4)

        # --- Card 2: 20-20-20 Eye Rest Reminder ---
        eye_card = tk.Frame(top_row, bg=self.colors["card_bg"],
                            highlightthickness=1, highlightbackground=self.colors["border"], padx=14, pady=12)
        eye_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(6, 0))

        tk.Label(eye_card, text="20-20-20 EYE REST TIMER", font=("Segoe UI", 10, "bold"),
                 fg=self.colors["ring_eye"], bg=self.colors["card_bg"]).pack(anchor="w")

        eye_status_txt = "Active Auto-Reminder" if self.eye_enabled else "Reminder Disabled"
        tk.Label(eye_card, text=eye_status_txt, font=("Segoe UI", 8),
                 fg=self.colors["text_secondary"], bg=self.colors["card_bg"]).pack(anchor="w", pady=(0, 6))

        self.eye_canvas = tk.Canvas(eye_card, width=170, height=170, bg=self.colors["card_bg"],
                                    highlightthickness=0)
        self.eye_canvas.pack(pady=4)
        total_eye_sec = self.eye_interval_min * 60
        self.draw_circular_progress(self.eye_canvas, self.eye_time_left, total_eye_sec,
                                    self.colors["ring_eye"], f"{self.eye_time_left//60:02d}:{self.eye_time_left%60:02d}")

        # Controls & Interval Chips
        eye_ctrl = tk.Frame(eye_card, bg=self.colors["card_bg"])
        eye_ctrl.pack(pady=6)

        btn_toggle_eye = tk.Button(eye_ctrl,
                                   text="🟢 ON" if self.eye_enabled else "🔴 OFF",
                                   font=("Segoe UI", 9, "bold"),
                                   bg=self.colors["ring_eye"] if self.eye_enabled else self.colors["btn_bg"],
                                   fg="#ffffff" if self.eye_enabled else self.colors["text_secondary"],
                                   relief=tk.FLAT, bd=0, padx=10, pady=4, cursor="hand2",
                                   command=self.toggle_eye_rest)
        btn_toggle_eye.pack(side=tk.LEFT, padx=4)

        for iv in [15, 20, 30]:
            btn_iv = tk.Button(eye_ctrl, text=f"{iv}m", font=("Segoe UI", 8),
                               bg=self.colors["accent"] if self.eye_interval_min == iv else self.colors["btn_bg"],
                               fg="#ffffff" if self.eye_interval_min == iv else self.colors["text_primary"],
                               relief=tk.FLAT, bd=0, padx=6, pady=4, cursor="hand2",
                               command=lambda v=iv: self.set_eye_interval(v))
            btn_iv.pack(side=tk.LEFT, padx=2)

        # Bottom Section: Weekly Focus Analytics Bar Chart
        stats_card = tk.Frame(container, bg=self.colors["card_bg"],
                              highlightthickness=1, highlightbackground=self.colors["border"], padx=14, pady=10)
        stats_card.pack(fill=tk.BOTH, expand=True)

        self.render_weekly_focus_chart(stats_card)

    def draw_circular_progress(self, canvas, remaining, total, color, text):
        canvas.delete("all")
        w, h = 170, 170
        pad = 16
        extent = -(360 * (remaining / max(total, 1)))

        # Background track arc
        canvas.create_arc(pad, pad, w - pad, h - pad, start=90, extent=-359.9,
                          style="arc", outline=self.colors["ring_bg"], width=12)

        # Active progress arc
        if extent != 0:
            canvas.create_arc(pad, pad, w - pad, h - pad, start=90, extent=extent,
                              style="arc", outline=color, width=12)

        # Center Text
        canvas.create_text(w / 2, h / 2, text=text, font=("Segoe UI", 18, "bold"),
                           fill=self.colors["text_primary"])

    def render_weekly_focus_chart(self, parent):
        tk.Label(parent, text="WEEKLY FOCUS ANALYTICS", font=("Segoe UI", 10, "bold"),
                 fg=self.colors["accent_cyan"], bg=self.colors["card_bg"]).pack(anchor="w", pady=(0, 4))

        # Calculate current week (Monday to Sunday)
        today = datetime.date.today()
        start_of_week = today - datetime.timedelta(days=today.weekday())  # Monday

        days_data = []
        total_sessions = 0
        pomo_stats = self.data.get("pomo_stats", {})

        for i in range(7):
            d_obj = start_of_week + datetime.timedelta(days=i)
            d_str = d_obj.strftime("%Y-%m-%d")
            cnt = pomo_stats.get(d_str, 0)
            days_data.append((d_obj.strftime("%a"), cnt, d_obj == today))
            total_sessions += cnt

        total_hours = round(total_sessions * 25 / 60, 1)

        # Summary Subtitle
        sub_txt = f"🔥 {total_sessions} Pomodoro Sessions Completed • {total_hours} Focus Hours This Week"
        tk.Label(parent, text=sub_txt, font=("Segoe UI", 8),
                 fg=self.colors["text_secondary"], bg=self.colors["card_bg"]).pack(anchor="w", pady=(0, 6))

        # Canvas Bar Chart
        c_w, c_h = 760, 95
        chart_cv = tk.Canvas(parent, width=c_w, height=c_h, bg=self.colors["card_bg"], highlightthickness=0)
        chart_cv.pack(fill=tk.X, expand=True)

        max_val = max([cnt for _, cnt, _ in days_data] + [6])
        bar_w = 46
        gap = (c_w - (7 * bar_w)) / 8

        for idx, (day_label, count, is_cur) in enumerate(days_data):
            x1 = gap + idx * (bar_w + gap)
            x2 = x1 + bar_w
            bar_h = (count / max_val) * (c_h - 32)
            y1 = (c_h - 22) - bar_h
            y2 = c_h - 22

            # Background bar pillar
            chart_cv.create_rectangle(x1, 10, x2, c_h - 22, fill=self.colors["subcard_bg"], outline="")

            # Filled bar
            bar_color = self.colors["accent"] if is_cur else self.colors["ring_eye"]
            if count > 0:
                chart_cv.create_rectangle(x1, y1, x2, y2, fill=bar_color, outline="")

            # Value label
            chart_cv.create_text((x1 + x2) / 2, y1 - 7 if count > 0 else y2 - 7,
                                 text=f"{count}", font=("Segoe UI", 7, "bold"),
                                 fill=self.colors["text_primary"] if count > 0 else self.colors["text_secondary"])

            # Day label
            chart_cv.create_text((x1 + x2) / 2, c_h - 8, text=day_label,
                                 font=("Segoe UI", 8, "bold" if is_cur else "normal"),
                                 fill=self.colors["accent_cyan"] if is_cur else self.colors["text_secondary"])

    # ==========================================
    # POMODORO & EYE REST LOGIC
    # ==========================================
    def pomo_start(self):
        self.pomo_state = "running"
        self.pomo_last_tick = time.time()
        if self.current_tab == "timers":
            self.render_timers_view()

    def pomo_pause(self):
        self.pomo_state = "paused"
        if self.current_tab == "timers":
            self.render_timers_view()

    def pomo_reset(self):
        self.pomo_state = "stopped"
        self.pomo_mode = "work"
        self.pomo_total_seconds = 25 * 60
        self.pomo_time_left = self.pomo_total_seconds
        if self.current_tab == "timers":
            self.render_timers_view()

    def toggle_eye_rest(self):
        self.eye_enabled = not self.eye_enabled
        self.data["eye_enabled"] = self.eye_enabled
        self.save_data()
        if self.current_tab == "timers":
            self.render_timers_view()

    def set_eye_interval(self, iv):
        self.eye_interval_min = iv
        self.eye_time_left = iv * 60
        self.data["eye_interval"] = iv
        self.save_data()
        if self.current_tab == "timers":
            self.render_timers_view()

    # ==========================================
    # MINI FLOATING WIDGET MODE
    # ==========================================
    def toggle_mini_widget(self):
        self.is_mini = not self.is_mini
        if self.is_mini:
            self.normal_geom = self.root.geometry()
            self.root.geometry("300x100")
            self.root.resizable(False, False)
            self.root.attributes("-topmost", True)
            self.build_mini_widget_gui()
        else:
            self.root.geometry(self.normal_geom or "1040x650")
            self.root.resizable(True, True)
            self.root.attributes("-topmost", False)
            self.build_gui()

    def build_mini_widget_gui(self):
        for w in self.root.winfo_children():
            w.destroy()

        mini_frame = tk.Frame(self.root, bg=self.colors["sidebar_bg"], padx=10, pady=8)
        mini_frame.pack(fill=tk.BOTH, expand=True)

        top_b = tk.Frame(mini_frame, bg=self.colors["sidebar_bg"])
        top_b.pack(fill=tk.X)

        self.mini_clock = tk.Label(top_b, text="--:--:--", font=("Segoe UI", 11, "bold"),
                                   fg=self.colors["text_primary"], bg=self.colors["sidebar_bg"])
        self.mini_clock.pack(side=tk.LEFT)

        rst_btn = tk.Button(top_b, text="⛶ Expand", font=("Segoe UI", 8, "bold"),
                            bg=self.colors["btn_bg"], fg=self.colors["accent_cyan"],
                            relief=tk.FLAT, bd=0, padx=6, pady=1, cursor="hand2",
                            command=self.toggle_mini_widget)
        rst_btn.pack(side=tk.RIGHT)

        # Status row
        self.mini_status = tk.Label(mini_frame, text="🍅 Pomodoro: Ready • ⏰ Alarms Active",
                                    font=("Segoe UI", 8), fg=self.colors["text_secondary"],
                                    bg=self.colors["sidebar_bg"])
        self.mini_status.pack(anchor="w", pady=(4, 0))

    # ==========================================
    # BACKGROUND THREADS & TIMERS
    # ==========================================
    def start_clock_thread(self):
        def _clock():
            while True:
                now = datetime.datetime.now()
                c_str = now.strftime("%H:%M:%S")
                d_str = now.strftime("%A, %d %b %Y")

                try:
                    if hasattr(self, "clock_lbl") and self.clock_lbl.winfo_exists():
                        self.clock_lbl.configure(text=c_str)
                    if hasattr(self, "date_lbl") and self.date_lbl.winfo_exists():
                        self.date_lbl.configure(text=d_str)
                    if hasattr(self, "mini_clock") and self.mini_clock.winfo_exists():
                        self.mini_clock.configure(text=c_str)
                except Exception:
                    pass

                time.sleep(1)

        threading.Thread(target=_clock, daemon=True).start()

    def start_alarm_checker(self):
        def _check():
            last_triggered_min = ""
            while True:
                now = datetime.datetime.now()
                cur_min = now.strftime("%H:%M")
                day_name = now.strftime("%a")  # "Mon", "Tue"...
                today_obj = now.date()

                if cur_min != last_triggered_min and now.second == 0:
                    for al in self.data.get("alarms", []):
                        if al.get("enabled") and al.get("time") == cur_min:
                            repeat = al.get("repeat", [])
                            if day_name in repeat:
                                # Check if skip holiday is active and today is holiday
                                if al.get("skip_holiday"):
                                    is_hol, _ = self.is_holiday(today_obj)
                                    if is_hol:
                                        print(f"Skipping alarm '{al.get('label')}' due to holiday.")
                                        continue

                                last_triggered_min = cur_min
                                self.trigger_alarm(al)
                time.sleep(0.5)

        threading.Thread(target=_check, daemon=True).start()

    def trigger_alarm(self, alarm_item):
        label = alarm_item.get("label", "Alarm")
        tone = alarm_item.get("tone", "gentle")
        has_math = alarm_item.get("math_challenge", False)

        if has_math:
            self.root.after(0, lambda: self.show_math_challenge_alarm(label, tone))
        else:
            self.play_tone(tone)
            self.root.after(0, lambda: messagebox.showinfo("⏰ ZZZleep Alarm", f"🔔 Alarm Triggered!\n\n{label} ({alarm_item.get('time')})"))

    def show_math_challenge_alarm(self, label, tone):
        num1 = random.randint(14, 58)
        num2 = random.randint(17, 49)
        expected = num1 + num2

        dlg = tk.Toplevel(self.root)
        dlg.title("🧠 Math Challenge Alarm")
        dlg.geometry("380x210")
        dlg.configure(bg=self.colors["card_bg"])
        dlg.attributes("-topmost", True)
        dlg.grab_set()

        # Start repeating sound until solved
        self.math_alarm_beeping = True

        def _loop_beep():
            while self.math_alarm_beeping:
                self.play_tone(tone)
                time.sleep(2.0)

        threading.Thread(target=_loop_beep, daemon=True).start()

        tk.Label(dlg, text="⏰ WAKE UP & SOLVE TO DISMISS!", font=("Segoe UI", 10, "bold"),
                 fg=self.colors["ring_pomo"], bg=self.colors["card_bg"]).pack(pady=(14, 4))

        tk.Label(dlg, text=f"Alarm: {label}", font=("Segoe UI", 9),
                 fg=self.colors["text_primary"], bg=self.colors["card_bg"]).pack()

        q_lbl = tk.Label(dlg, text=f"{num1} + {num2} = ?", font=("Segoe UI", 16, "bold"),
                         fg=self.colors["accent_cyan"], bg=self.colors["card_bg"])
        q_lbl.pack(pady=8)

        ans_entry = tk.Entry(dlg, font=("Segoe UI", 12, "bold"), justify=tk.CENTER,
                             bg=self.colors["entry_bg"], fg=self.colors["entry_fg"],
                             bd=1, relief=tk.SOLID)
        ans_entry.pack(padx=20, pady=4)
        ans_entry.focus_set()

        res_lbl = tk.Label(dlg, text="", font=("Segoe UI", 8),
                           fg=self.colors["ring_pomo"], bg=self.colors["card_bg"])
        res_lbl.pack()

        def verify():
            try:
                val = int(ans_entry.get().strip())
                if val == expected:
                    self.math_alarm_beeping = False
                    dlg.destroy()
                    messagebox.showinfo("Alarm Dismissed", "Great job! Have a productive day ahead!")
                else:
                    res_lbl.configure(text=f"Incorrect answer ({val}). Try again!")
                    ans_entry.delete(0, "end")
            except ValueError:
                res_lbl.configure(text="Please enter a valid number.")

        btn_sub = tk.Button(dlg, text="Submit & Dismiss", font=("Segoe UI", 9, "bold"),
                            bg=self.colors["ring_eye"], fg="#ffffff", relief=tk.FLAT, bd=0, padx=14, pady=4,
                            command=verify)
        btn_sub.pack(pady=(4, 10))

        dlg.protocol("WM_DELETE_WINDOW", lambda: None)  # Prevent closing without solving

    def start_eye_rest_checker(self):
        def _eye():
            while True:
                time.sleep(1)
                if self.eye_enabled:
                    self.eye_time_left -= 1
                    if self.eye_time_left <= 0:
                        self.eye_time_left = self.eye_interval_min * 60
                        self.play_tone("zen")
                        self.root.after(0, lambda: messagebox.showinfo(
                            "👀 20-20-20 Eye Rest Reminder",
                            "Look at an object 20 feet (6 meters) away for 20 seconds to relax your eyes."
                        ))

                    if hasattr(self, "eye_canvas") and self.eye_canvas.winfo_exists() and self.current_tab == "timers":
                        total_eye_sec = self.eye_interval_min * 60
                        self.draw_circular_progress(self.eye_canvas, self.eye_time_left, total_eye_sec,
                                                    self.colors["ring_eye"],
                                                    f"{self.eye_time_left//60:02d}:{self.eye_time_left%60:02d}")

        threading.Thread(target=_eye, daemon=True).start()

    def start_pomo_thread(self):
        def _pomo():
            while True:
                time.sleep(0.5)
                if self.pomo_state == "running":
                    now = time.time()
                    elapsed = now - self.pomo_last_tick
                    if elapsed >= 1.0:
                        self.pomo_last_tick = now
                        self.pomo_time_left -= int(elapsed)

                        if self.pomo_time_left <= 0:
                            if self.pomo_mode == "work":
                                # Log completed session to daily stats
                                today_str = datetime.date.today().strftime("%Y-%m-%d")
                                if "pomo_stats" not in self.data:
                                    self.data["pomo_stats"] = {}
                                self.data["pomo_stats"][today_str] = self.data["pomo_stats"].get(today_str, 0) + 1
                                self.save_data()

                                self.pomo_mode = "break"
                                self.pomo_total_seconds = 5 * 60
                                self.pomo_time_left = self.pomo_total_seconds
                                self.play_tone("chime")
                                self.root.after(0, lambda: messagebox.showinfo("🍅 Pomodoro", "Focus Session Complete! Take a 5-minute break."))
                            else:
                                self.pomo_mode = "work"
                                self.pomo_total_seconds = 25 * 60
                                self.pomo_time_left = self.pomo_total_seconds
                                self.play_tone("gentle")
                                self.root.after(0, lambda: messagebox.showinfo("🍅 Pomodoro", "Break Over! Ready for the next focus session?"))

                        # Update UI
                        if hasattr(self, "pomo_canvas") and self.pomo_canvas.winfo_exists() and self.current_tab == "timers":
                            self.draw_circular_progress(self.pomo_canvas, self.pomo_time_left, self.pomo_total_seconds,
                                                        self.colors["ring_pomo"],
                                                        f"{self.pomo_time_left//60:02d}:{self.pomo_time_left%60:02d}")

                        if hasattr(self, "mini_status") and self.mini_status.winfo_exists() and self.is_mini:
                            m_txt = f"🍅 {self.pomo_mode.upper()} {self.pomo_time_left//60:02d}:{self.pomo_time_left%60:02d}"
                            self.mini_status.configure(text=m_txt)

        threading.Thread(target=_pomo, daemon=True).start()

    # ==========================================
    # AUTO-UPDATE SYNCHRONIZATION
    # ==========================================
    def silent_check_update(self):
        try:
            req = urllib.request.Request(UPDATE_MANIFEST_URL, headers={"User-Agent": "ZZZleep-Updater"})
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    latest_ver = data.get("version", "")
                    if latest_ver and latest_ver != APP_VERSION:
                        # Popup update dialog
                        self.root.after(0, lambda: self.show_update_popup(data))
        except Exception:
            pass

    def show_update_popup(self, manifest_data):
        new_ver = manifest_data.get("version", "Latest")
        changelog = manifest_data.get("changelog", [])
        ch_text = "\n• ".join(changelog) if changelog else "Performance optimizations and new features."

        msg = (
            f"A new version of ZZZleep is available!\n\n"
            f"Current Version: v{APP_VERSION}\n"
            f"Latest Version: v{new_ver}\n\n"
            f"Changelog:\n• {ch_text}\n\n"
            f"Would you like to download the updated binary now?"
        )

        if messagebox.askyesno("Update Available", msg):
            download_url = manifest_data.get("download_url", DIRECT_EXE_URL)
            webbrowser.open(download_url)


# ==========================================
# MAIN ENTRY POINT
# ==========================================
def main():
    root = tk.Tk()
    app = ZZZleepApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
