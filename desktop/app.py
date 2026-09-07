#!/usr/bin/env python3
"""
ZZZleep Desktop — Offline Calendar, Audio Alarm & Rest Timer
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
import tkinter as tk
from tkinter import ttk, messagebox

# Windows Sound Support
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

# Application Meta
APP_NAME = "ZZZleep Desktop"
APP_VERSION = "1.0.0"
DATA_FILE = os.path.join(os.path.expanduser("~"), ".zzzleep_desktop_data.json")

DEFAULT_DATA = {
    "alarms": [
        {"id": "alarm-1", "title": "Bangun Pagi & Rutinitas", "time": "06:00", "enabled": True, "days": [1, 2, 3, 4, 5], "tone": "gentle"},
        {"id": "alarm-2", "title": "Evaluasi & Tutup Laptop", "time": "22:30", "enabled": True, "days": [1, 2, 3, 4, 5, 6, 0], "tone": "acoustic"}
    ],
    "habits": [
        {"id": "h-1", "name": "Minum Air Putih 2L", "target": 1, "unit": "Target Harian", "completedDays": []},
        {"id": "h-2", "name": "Stretching & Postur Tubuh", "target": 1, "unit": "Target Harian", "completedDays": []}
    ],
    "settings": {
        "soundVolume": 80,
        "soundTone": "gentle",
        "eyeRestEnabled": True,
        "eyeRestIntervalMin": 20
    }
}


def play_audio_tone(tone_type="gentle"):
    """Synthesizes pure offline harmonic beeps using native winsound."""
    if not HAS_WINSOUND:
        return

    def _beep_worker():
        try:
            if tone_type == "gentle":
                # C Major Arpeggio: C5 (523Hz), E5 (659Hz), G5 (784Hz), C6 (1046Hz)
                notes = [523, 659, 784, 1046]
                for freq in notes:
                    winsound.Beep(freq, 220)
                    time.sleep(0.04)
            elif tone_type == "retro":
                # Double high-pitch beep
                for _ in range(3):
                    winsound.Beep(880, 150)
                    time.sleep(0.08)
                    winsound.Beep(1760, 180)
                    time.sleep(0.1)
            elif tone_type == "acoustic":
                # Harmonic Bell
                winsound.Beep(440, 300)
                time.sleep(0.05)
                winsound.Beep(880, 450)
            else:
                winsound.Beep(600, 300)
        except Exception as e:
            print(f"Audio playback error: {e}")

    thread = threading.Thread(target=_beep_worker, daemon=True)
    thread.start()


class ZzzleepDesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} v{APP_VERSION} — 100% Offline")
        self.root.geometry("880x640")
        self.root.minsize(780, 560)
        self.root.configure(bg="#0f172a")

        self.data = self.load_data()
        self.pomodoro_seconds_left = 25 * 60
        self.pomodoro_is_running = False
        self.eye_rest_seconds_left = self.data.get("settings", {}).get("eyeRestIntervalMin", 20) * 60
        self.eye_rest_is_running = True
        self.active_alarm_ringing = False

        self.setup_styles()
        self.build_ui()
        self.start_background_timer()

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
        self.style.configure("Card.TLabel", background=card_bg, foreground=text_white, font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", background=bg_dark, foreground="#38bdf8", font=("Segoe UI", 16, "bold"))
        self.style.configure("Clock.TLabel", background="#1e293b", foreground="#38bdf8", font=("Consolas", 28, "bold"))

    def build_ui(self):
        header_frame = tk.Frame(self.root, bg="#1e293b", height=60)
        header_frame.pack(fill="x", side="top")

        brand_lbl = tk.Label(header_frame, text="⏰ ZZZleep Desktop", font=("Segoe UI", 13, "bold"), fg="#38bdf8", bg="#1e293b")
        brand_lbl.pack(side="left", padx=16, pady=12)

        badge_lbl = tk.Label(header_frame, text="OFFLINE", font=("Segoe UI", 8, "bold"), fg="#0284c7", bg="#0f172a", padx=8, pady=3)
        badge_lbl.pack(side="left", padx=4)

        self.top_clock_lbl = tk.Label(header_frame, text="--:--:--", font=("Consolas", 12, "bold"), fg="#f8fafc", bg="#1e293b")
        self.top_clock_lbl.pack(side="right", padx=16)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=12, pady=12)

        # Tab 1: Alarms & Schedule
        tab_alarms = ttk.Frame(notebook)
        notebook.add(tab_alarms, text="  ⏰ Alarm & Jadwal  ")
        self.build_alarms_tab(tab_alarms)

        # Tab 2: Pomodoro & Eye Rest
        tab_timers = ttk.Frame(notebook)
        notebook.add(tab_timers, text="  🍅 Pomodoro & Istirahat Layar  ")
        self.build_timers_tab(tab_timers)

        # Tab 3: Habits & Data Vault
        tab_vault = ttk.Frame(notebook)
        notebook.add(tab_vault, text="  📊 Kebiasaan & Backup  ")
        self.build_vault_tab(tab_vault)

    def build_alarms_tab(self, parent):
        container = tk.Frame(parent, bg="#0f172a")
        container.pack(fill="both", expand=True, padx=8, pady=8)

        # Left Column: Clock & Form
        left_col = tk.Frame(container, bg="#1e293b", width=320)
        left_col.pack(side="left", fill="y", padx=6, pady=6)
        left_col.pack_propagate(False)

        tk.Label(left_col, text="WAKTU LOKAL (OFFLINE)", font=("Segoe UI", 8, "bold"), fg="#94a3b8", bg="#1e293b").pack(anchor="w", padx=16, pady=(16, 2))
        self.main_clock_lbl = tk.Label(left_col, text="00:00:00", font=("Consolas", 26, "bold"), fg="#38bdf8", bg="#1e293b")
        self.main_clock_lbl.pack(anchor="w", padx=16)
        self.main_date_lbl = tk.Label(left_col, text="Loading date...", font=("Segoe UI", 10), fg="#94a3b8", bg="#1e293b")
        self.main_date_lbl.pack(anchor="w", padx=16, pady=(0, 16))

        tk.Frame(left_col, height=1, bg="#334155").pack(fill="x", padx=16, pady=8)

        tk.Label(left_col, text="Tambah Alarm Baru", font=("Segoe UI", 11, "bold"), fg="#f8fafc", bg="#1e293b").pack(anchor="w", padx=16, pady=4)

        time_frame = tk.Frame(left_col, bg="#1e293b")
        time_frame.pack(anchor="w", padx=16, pady=4, fill="x")
        tk.Label(time_frame, text="Jam (HH:MM):", font=("Segoe UI", 9), fg="#94a3b8", bg="#1e293b").pack(anchor="w")
        self.entry_alarm_time = tk.Entry(time_frame, font=("Consolas", 12), bg="#0f172a", fg="#38bdf8", insertbackground="#38bdf8", relief="flat")
        self.entry_alarm_time.insert(0, "07:00")
        self.entry_alarm_time.pack(fill="x", pady=2, ipady=4)

        title_frame = tk.Frame(left_col, bg="#1e293b")
        title_frame.pack(anchor="w", padx=16, pady=4, fill="x")
        tk.Label(title_frame, text="Keterangan / Label:", font=("Segoe UI", 9), fg="#94a3b8", bg="#1e293b").pack(anchor="w")
        self.entry_alarm_title = tk.Entry(title_frame, font=("Segoe UI", 10), bg="#0f172a", fg="#f8fafc", insertbackground="#38bdf8", relief="flat")
        self.entry_alarm_title.insert(0, "Fokus Kerja Pagi")
        self.entry_alarm_title.pack(fill="x", pady=2, ipady=4)

        btn_add = tk.Button(left_col, text="+ Pasang Alarm", font=("Segoe UI", 10, "bold"), bg="#0284c7", fg="white", activebackground="#0369a1", activeforeground="white", relief="flat", command=self.add_alarm)
        btn_add.pack(fill="x", padx=16, pady=12, ipady=6)

        btn_test = tk.Button(left_col, text="🔊 Uji Suara Harmoni (Offline)", font=("Segoe UI", 9), bg="#334155", fg="#f8fafc", relief="flat", command=lambda: play_audio_tone("gentle"))
        btn_test.pack(fill="x", padx=16, pady=4, ipady=4)

        # Right Column: List of Alarms
        right_col = tk.Frame(container, bg="#1e293b")
        right_col.pack(side="right", fill="both", expand=True, padx=6, pady=6)

        header_list = tk.Frame(right_col, bg="#1e293b")
        header_list.pack(fill="x", padx=16, pady=12)
        tk.Label(header_list, text="Daftar Alarm & Pengingat Aktif", font=("Segoe UI", 12, "bold"), fg="#f8fafc", bg="#1e293b").pack(side="left")

        self.alarms_list_frame = tk.Frame(right_col, bg="#1e293b")
        self.alarms_list_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        self.refresh_alarms_list()

    def refresh_alarms_list(self):
        for widget in self.alarms_list_frame.winfo_children():
            widget.destroy()

        alarms = self.data.get("alarms", [])
        if not alarms:
            tk.Label(self.alarms_list_frame, text="Belum ada alarm aktif. Tambahkan melalui form di samping.", fg="#64748b", bg="#1e293b", font=("Segoe UI", 10, "italic")).pack(pady=40)
            return

        for alarm in alarms:
            card = tk.Frame(self.alarms_list_frame, bg="#0f172a", relief="flat", bd=1)
            card.pack(fill="x", pady=4, padx=2)

            left = tk.Frame(card, bg="#0f172a")
            left.pack(side="left", padx=12, pady=10)

            time_lbl = tk.Label(left, text=alarm["time"], font=("Consolas", 18, "bold"), fg="#38bdf8" if alarm.get("enabled", True) else "#64748b", bg="#0f172a")
            time_lbl.pack(anchor="w")

            title_lbl = tk.Label(left, text=alarm.get("title", "Alarm"), font=("Segoe UI", 10, "bold"), fg="#f8fafc" if alarm.get("enabled", True) else "#64748b", bg="#0f172a")
            title_lbl.pack(anchor="w")

            right = tk.Frame(card, bg="#0f172a")
            right.pack(side="right", padx=12, pady=10)

            status_text = "AKTIF" if alarm.get("enabled", True) else "NONAKTIF"
            status_bg = "#059669" if alarm.get("enabled", True) else "#475569"
            toggle_btn = tk.Button(right, text=status_text, font=("Segoe UI", 8, "bold"), bg=status_bg, fg="white", relief="flat", padx=8, pady=2, command=lambda a=alarm: self.toggle_alarm(a))
            toggle_btn.pack(side="left", padx=4)

            del_btn = tk.Button(right, text="✕ Hapus", font=("Segoe UI", 8), bg="#dc2626", fg="white", relief="flat", padx=6, pady=2, command=lambda a_id=alarm["id"]: self.delete_alarm(a_id))
            del_btn.pack(side="left", padx=4)

    def add_alarm(self):
        t_str = self.entry_alarm_time.get().strip()
        title = self.entry_alarm_title.get().strip() or "Alarm Pengingat"

        try:
            parts = t_str.split(":")
            h = int(parts[0])
            m = int(parts[1])
            if not (0 <= h < 24 and 0 <= m < 60):
                raise ValueError
            valid_time = f"{h:02d}:{m:02d}"
        except Exception:
            messagebox.showerror("Format Waktu Salah", "Silakan masukkan waktu dalam format HH:MM (contoh: 07:30 atau 21:00).")
            return

        new_alarm = {
            "id": f"alarm-{int(time.time()*1000)}",
            "title": title,
            "time": valid_time,
            "enabled": True,
            "days": [0, 1, 2, 3, 4, 5, 6],
            "tone": "gentle"
        }

        self.data["alarms"].append(new_alarm)
        self.save_data()
        self.refresh_alarms_list()
        messagebox.showinfo("Alarm Terpasang", f"Alarm '{title}' berhasil dipasang pada pukul {valid_time}.")

    def toggle_alarm(self, alarm):
        alarm["enabled"] = not alarm.get("enabled", True)
        self.save_data()
        self.refresh_alarms_list()

    def delete_alarm(self, alarm_id):
        self.data["alarms"] = [a for a in self.data.get("alarms", []) if a.get("id") != alarm_id]
        self.save_data()
        self.refresh_alarms_list()

    def build_timers_tab(self, parent):
        container = tk.Frame(parent, bg="#0f172a")
        container.pack(fill="both", expand=True, padx=8, pady=8)

        # Pomodoro Card
        pomo_card = tk.Frame(container, bg="#1e293b")
        pomo_card.pack(side="left", fill="both", expand=True, padx=6, pady=6)

        tk.Label(pomo_card, text="🍅 POMODORO FOCUS TIMER", font=("Segoe UI", 12, "bold"), fg="#f43f5e", bg="#1e293b").pack(pady=(20, 8))
        self.pomo_clock_lbl = tk.Label(pomo_card, text="25:00", font=("Consolas", 40, "bold"), fg="#f8fafc", bg="#1e293b")
        self.pomo_clock_lbl.pack(pady=10)

        pomo_btn_frame = tk.Frame(pomo_card, bg="#1e293b")
        pomo_btn_frame.pack(pady=12)

        self.btn_pomo_toggle = tk.Button(pomo_btn_frame, text="Mulai Sesi (25m)", font=("Segoe UI", 10, "bold"), bg="#f43f5e", fg="white", relief="flat", padx=14, pady=6, command=self.toggle_pomodoro)
        self.btn_pomo_toggle.pack(side="left", padx=6)

        btn_pomo_reset = tk.Button(pomo_btn_frame, text="Reset", font=("Segoe UI", 10), bg="#334155", fg="#f8fafc", relief="flat", padx=10, pady=6, command=self.reset_pomodoro)
        btn_pomo_reset.pack(side="left", padx=6)

        desc1 = "Siklus kerja 25 menit diselingi istirahat 5 menit\\nmeningkatkan fokus tanpa kelelahan mental."
        tk.Label(pomo_card, text="Siklus kerja 25 menit diselingi istirahat 5 menit\nmeningkatkan fokus tanpa kelelahan mental.", font=("Segoe UI", 9), fg="#94a3b8", bg="#1e293b", justify="center").pack(pady=16)

        # Eye Rest Card
        eye_card = tk.Frame(container, bg="#1e293b")
        eye_card.pack(side="right", fill="both", expand=True, padx=6, pady=6)

        tk.Label(eye_card, text="👁️ ATURAN ISTIRAHAT MATA 20-20-20", font=("Segoe UI", 12, "bold"), fg="#10b981", bg="#1e293b").pack(pady=(20, 8))
        self.eye_clock_lbl = tk.Label(eye_card, text="20:00", font=("Consolas", 40, "bold"), fg="#f8fafc", bg="#1e293b")
        self.eye_clock_lbl.pack(pady=10)

        eye_btn_frame = tk.Frame(eye_card, bg="#1e293b")
        eye_btn_frame.pack(pady=12)

        btn_eye_reset = tk.Button(eye_btn_frame, text="Reset Interval (20m)", font=("Segoe UI", 10, "bold"), bg="#10b981", fg="white", relief="flat", padx=14, pady=6, command=self.reset_eye_rest)
        btn_eye_reset.pack(side="left", padx=6)

        tk.Label(eye_card, text="Setiap 20 menit menatap layar laptop/PC,\npandang objek sejauh 20 kaki (6 meter) selama 20 detik\nuntuk mencegah ketegangan mata (Digital Eye Strain).", font=("Segoe UI", 9), fg="#94a3b8", bg="#1e293b", justify="center").pack(pady=16)

    def toggle_pomodoro(self):
        self.pomodoro_is_running = not self.pomodoro_is_running
        if self.pomodoro_is_running:
            self.btn_pomo_toggle.config(text="Jeda Sesi", bg="#d97706")
        else:
            self.btn_pomo_toggle.config(text="Lanjutkan Sesi", bg="#f43f5e")

    def reset_pomodoro(self):
        self.pomodoro_is_running = False
        self.pomodoro_seconds_left = 25 * 60
        self.btn_pomo_toggle.config(text="Mulai Sesi (25m)", bg="#f43f5e")
        self.pomo_clock_lbl.config(text="25:00")

    def reset_eye_rest(self):
        self.eye_rest_seconds_left = 20 * 60
        self.eye_clock_lbl.config(text="20:00")

    def build_vault_tab(self, parent):
        container = tk.Frame(parent, bg="#0f172a")
        container.pack(fill="both", expand=True, padx=8, pady=8)

        card = tk.Frame(container, bg="#1e293b")
        card.pack(fill="both", expand=True, padx=6, pady=6)

        tk.Label(card, text="📁 PENYIMPANAN DATA LOKAL (JSON)", font=("Segoe UI", 13, "bold"), fg="#38bdf8", bg="#1e293b").pack(anchor="w", padx=20, pady=(20, 4))
        tk.Label(card, text=f"Lokasi Berkas Lokal: {DATA_FILE}", font=("Consolas", 9), fg="#94a3b8", bg="#1e293b").pack(anchor="w", padx=20, pady=(0, 16))

        info_text = (
            "Karakteristik Aplikasi:\n"
            "1. Seluruh data disimpan secara lokal pada perangkat Anda dalam format JSON.\n"
            "2. Nada alarm dihasilkan langsung melalui driver audio Windows (winsound) tanpa file audio eksternal.\n"
            "3. Berkas data dapat dicadangkan atau dipindahkan secara manual kapan saja."
        )
        tk.Label(card, text=info_text, font=("Segoe UI", 10), fg="#e2e8f0", bg="#1e293b", justify="left").pack(anchor="w", padx=20, pady=8)

        btn_box = tk.Frame(card, bg="#1e293b")
        btn_box.pack(anchor="w", padx=20, pady=20)

        btn_open_file = tk.Button(btn_box, text="Buka Folder Data Lokal", font=("Segoe UI", 9, "bold"), bg="#0284c7", fg="white", relief="flat", padx=12, pady=6, command=lambda: os.system(f'explorer /select,"{DATA_FILE}"'))
        btn_open_file.pack(side="left", padx=(0, 8))

        btn_save_now = tk.Button(btn_box, text="Paksa Simpan JSON Sekarang", font=("Segoe UI", 9), bg="#334155", fg="#f8fafc", relief="flat", padx=12, pady=6, command=self.save_data)
        btn_save_now.pack(side="left", padx=8)

    def start_background_timer(self):
        def _loop():
            last_checked_minute = ""
            while True:
                now = datetime.datetime.now()
                time_str = now.strftime("%H:%M:%S")
                hm_str = now.strftime("%H:%M")
                date_str = now.strftime("%A, %d %B %Y")

                try:
                    self.top_clock_lbl.config(text=time_str)
                    self.main_clock_lbl.config(text=time_str)
                    self.main_date_lbl.config(text=date_str)
                except Exception:
                    pass

                if hm_str != last_checked_minute:
                    last_checked_minute = hm_str
                    day_idx = (now.weekday() + 1) % 7

                    for alarm in self.data.get("alarms", []):
                        if alarm.get("enabled", True) and alarm.get("time") == hm_str:
                            days = alarm.get("days", [0, 1, 2, 3, 4, 5, 6])
                            if day_idx in days:
                                self.trigger_alarm(alarm)

                if self.pomodoro_is_running and self.pomodoro_seconds_left > 0:
                    self.pomodoro_seconds_left -= 1
                    m = self.pomodoro_seconds_left // 60
                    s = self.pomodoro_seconds_left % 60
                    try:
                        self.pomo_clock_lbl.config(text=f"{m:02d}:{s:02d}")
                    except Exception:
                        pass
                    if self.pomodoro_seconds_left == 0:
                        self.pomodoro_is_running = False
                        play_audio_tone("retro")
                        messagebox.showinfo("Pomodoro Selesai!", "Sesi fokus 25 menit telah selesai! Ambil istirahat sejenak 5 menit.")

                if self.eye_rest_is_running and self.eye_rest_seconds_left > 0:
                    self.eye_rest_seconds_left -= 1
                    m = self.eye_rest_seconds_left // 60
                    s = self.eye_rest_seconds_left % 60
                    try:
                        self.eye_clock_lbl.config(text=f"{m:02d}:{s:02d}")
                    except Exception:
                        pass
                    if self.eye_rest_seconds_left == 0:
                        self.eye_rest_seconds_left = 20 * 60
                        play_audio_tone("acoustic")
                        messagebox.showinfo("Istirahatkan Mata (20-20-20)", "Waktunya jeda 20 detik! Alihkan pandangan ke objek sejauh 6 meter (20 kaki).")

                time.sleep(1)

        t = threading.Thread(target=_loop, daemon=True)
        t.start()

    def trigger_alarm(self, alarm):
        play_audio_tone(alarm.get("tone", "gentle"))
        self.root.deiconify()
        self.root.lift()
        messagebox.showwarning("⏰ ALARM BERBUNYI!", f"Pukul: {alarm.get('time')}\n{alarm.get('title')}")


def main():
    root = tk.Tk()
    app = ZzzleepDesktopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
