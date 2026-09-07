/**
 * zzzleep-suite.js — ZZZleep Suite: Smart Offline Desktop Calendar, Precision Alarm & Routine Guardian
 * Flagship Project 4:
 * - Interactive Monthly Calendar Matrix & Priority Agenda Planner
 * - Real-Time Precision Alarm Station with Web Audio Synthesizer (Zero External Dependencies)
 * - Pomodoro Focus & Rest Cycle Engine
 * - Sleep Hygiene, Bedtime Tracker & 20-20-20 Eye-Rest Guardian
 * - Daily Habit Routine Checklist & Streak Analytics
 * - 100% Offline Local Privacy Vault (JSON Import/Export)
 * - Native Windows Desktop .EXE Source & Integration Guide
 * 
 * Lead Developer & Core Architect: Rizki Ananda, S.Kom (@InfiniteNull)
 * 100% Client-Side & Zero-Telemetry Architecture.
 */

(function () {
  'use strict';

  // =========================================================================
  // LOCAL STORAGE & STATE MANAGEMENT
  // =========================================================================
  const STORAGE_KEY = 'zzzleep_app_data_v1';

  function getInitialState() {
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    const todayStr = `${yyyy}-${mm}-${dd}`;

    return {
      currentTab: 'calendar', // 'calendar', 'alarm', 'pomodoro', 'sleep', 'habits', 'backup', 'desktop'
      selectedDate: todayStr,
      calendarMonth: today.getMonth(),
      calendarYear: today.getFullYear(),
      
      // Alarms
      alarms: [
        { id: 1, time: '06:30', title: 'Wakeup & Morning Stretch', sound: 'gentle', enabled: true, category: 'wake', repeat: ['Mon','Tue','Wed','Thu','Fri'] },
        { id: 2, time: '12:00', title: 'Lunch & Screen-Time Break', sound: 'synth', enabled: true, category: 'health', repeat: ['Mon','Tue','Wed','Thu','Fri'] },
        { id: 3, time: '17:30', title: 'Daily Code Commit & Sync', sound: 'digital', enabled: true, category: 'work', repeat: ['Mon','Tue','Wed','Thu','Fri'] },
        { id: 4, time: '22:30', title: 'Sleep Preparation & Offline Mode', sound: 'bell', enabled: true, category: 'sleep', repeat: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'] }
      ],

      // Calendar Events
      events: [
        { id: 101, date: todayStr, time: '09:00', title: 'Standup Sprint Review & Architecture Sync', category: 'work', priority: 'high', notes: 'Review backend deployment and clean code review.' },
        { id: 102, date: todayStr, time: '14:30', title: 'Vulnerability Assessment & Code Audit', category: 'work', priority: 'high', notes: 'Inspect zero-day risks and dependency updates.' },
        { id: 103, date: todayStr, time: '20:00', title: 'Independent Study & Algorithm Practice', category: 'study', priority: 'medium', notes: 'Solve dynamic programming problems.' }
      ],

      // Pomodoro Engine
      pomodoro: {
        mode: 'work', // 'work', 'shortBreak', 'longBreak'
        workDuration: 25,
        shortBreakDuration: 5,
        longBreakDuration: 15,
        secondsLeft: 25 * 60,
        isRunning: false,
        completedSessions: 4
      },

      // Sleep & Eye Health
      sleepHealth: {
        bedtime: '22:30',
        wakeTime: '06:30',
        waterGlasses: 5,
        waterGoal: 8,
        eyeRestActive: true,
        eyeRestInterval: 20, // 20 minutes rule
        eyeRestSecondsLeft: 20 * 60,
        eyeRestRunning: true
      },

      // Habits
      habits: [
        { id: 1, title: 'Minum 2L Air / Hydration Goal', icon: 'droplet', streak: 12, completedToday: true },
        { id: 2, title: '20-20-20 Eye-Rest Breaks', icon: 'eye', streak: 8, completedToday: true },
        { id: 3, title: 'Clean Code Git Commit Daily', icon: 'git-commit', streak: 24, completedToday: true },
        { id: 4, title: 'Tidur Tepat Waktu (7-8 Jam)', icon: 'moon', streak: 6, completedToday: false },
        { id: 5, title: 'Stretching & Posture Reset', icon: 'activity', streak: 9, completedToday: true }
      ]
    };
  }

  function loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        return { ...getInitialState(), ...parsed };
      }
    } catch (e) {
      console.warn('Failed to load ZZZleep storage, fallback to initial state', e);
    }
    return getInitialState();
  }

  function saveState() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (e) {
      console.error('Failed to save ZZZleep state', e);
    }
  }

  let state = loadState();

  // =========================================================================
  // WEB AUDIO SYNTHESIZER ENGINE (100% Offline & Pure JS)
  // =========================================================================
  let audioCtx = null;

  function getAudioContext() {
    if (!audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        audioCtx = new AudioContext();
      }
    }
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
    return audioCtx;
  }

  function playSynthSound(type) {
    const ctx = getAudioContext();
    if (!ctx) return;

    const now = ctx.currentTime;

    if (type === 'digital') {
      // Retro 3-beep alarm
      [0, 0.15, 0.3].forEach((delay) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'square';
        osc.frequency.setValueAtTime(880, now + delay);
        gain.gain.setValueAtTime(0.15, now + delay);
        gain.gain.exponentialRampToValueAtTime(0.001, now + delay + 0.1);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now + delay);
        osc.stop(now + delay + 0.1);
      });
    } else if (type === 'gentle') {
      // Acoustic arpeggio (C5 -> E5 -> G5 -> B5)
      const freqs = [523.25, 659.25, 783.99, 987.77];
      freqs.forEach((f, idx) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(f, now + idx * 0.12);
        gain.gain.setValueAtTime(0, now + idx * 0.12);
        gain.gain.linearRampToValueAtTime(0.2, now + idx * 0.12 + 0.05);
        gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.12 + 0.8);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now + idx * 0.12);
        osc.stop(now + idx * 0.12 + 0.8);
      });
    } else if (type === 'bell') {
      // Harmonic church bell strike
      const fundamental = 440;
      [1, 2.76, 5.4, 8.9].forEach((harmonic, idx) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(fundamental * harmonic, now);
        const amp = 0.2 / (idx + 1);
        gain.gain.setValueAtTime(amp, now);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + 1.6);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 1.6);
      });
    } else if (type === 'synth') {
      // Ambient warm synth pad
      const chords = [349.23, 440.0, 523.25, 659.25]; // Fmaj7
      chords.forEach((f) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(f, now);
        gain.gain.setValueAtTime(0.08, now);
        gain.gain.linearRampToValueAtTime(0.12, now + 0.2);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 1.2);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 1.2);
      });
    } else {
      // Short friendly ping
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(1046.5, now); // C6
      gain.gain.setValueAtTime(0.2, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.4);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.4);
    }
  }

  // =========================================================================
  // REAL-TIME ALARM DISPATCHER & INTERVAL WORKER
  // =========================================================================
  let lastCheckedMinute = '';
  let activeAlarmSoundInterval = null;

  function initAlarmWorker() {
    setInterval(() => {
      const now = new Date();
      const hh = String(now.getHours()).padStart(2, '0');
      const mm = String(now.getMinutes()).padStart(2, '0');
      const ss = String(now.getSeconds()).padStart(2, '0');
      const currentHHMM = `${hh}:${mm}`;

      // Update digital clocks if present on screen
      const liveClockEl = document.getElementById('zzzLiveClockDisplay');
      if (liveClockEl) {
        liveClockEl.textContent = `${currentHHMM}:${ss}`;
      }

      // Check alarms once per minute at second 00
      if (currentHHMM !== lastCheckedMinute && ss === '00') {
        lastCheckedMinute = currentHHMM;
        checkAlarmsForTrigger(currentHHMM, now);
      }

      // Pomodoro ticking
      if (state.pomodoro.isRunning && state.pomodoro.secondsLeft > 0) {
        state.pomodoro.secondsLeft--;
        updatePomodoroUiLive();
        if (state.pomodoro.secondsLeft === 0) {
          handlePomodoroPhaseComplete();
        }
      }

      // Eye rest ticking
      if (state.sleepHealth.eyeRestRunning && state.sleepHealth.eyeRestSecondsLeft > 0) {
        state.sleepHealth.eyeRestSecondsLeft--;
        updateEyeRestUiLive();
        if (state.sleepHealth.eyeRestSecondsLeft === 0) {
          triggerEyeRestAlert();
          state.sleepHealth.eyeRestSecondsLeft = state.sleepHealth.eyeRestInterval * 60;
        }
      }

    }, 1000);
  }

  function checkAlarmsForTrigger(hhmm, dateObj) {
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const currentDay = days[dateObj.getDay()];

    state.alarms.forEach(al => {
      if (al.enabled && al.time === hhmm) {
        if (!al.repeat || al.repeat.length === 0 || al.repeat.includes(currentDay)) {
          triggerAlarmModal(al);
        }
      }
    });
  }

  function triggerAlarmModal(alarm) {
    const isEn = window.currentLang === 'en';

    // Play synthesized sound
    playSynthSound(alarm.sound || 'digital');
    if (activeAlarmSoundInterval) clearInterval(activeAlarmSoundInterval);
    activeAlarmSoundInterval = setInterval(() => {
      playSynthSound(alarm.sound || 'digital');
    }, 2500);

    // Native Notification if supported
    if ("Notification" in window && Notification.permission === "granted") {
      new Notification(`⏰ ZZZleep Alarm: ${alarm.title}`, {
        body: isEn ? `Time: ${alarm.time} — Stay mindful and organized.` : `Waktu: ${alarm.time} — Pengingat jadwal laptop Anda.`,
        icon: 'https://infinitenull.github.io/favicon.ico'
      });
    }

    const modal = document.getElementById('zzzGlobalModal');
    const card = document.getElementById('zzzGlobalModalCard');
    if (!modal || !card) return;

    card.innerHTML = `
      <div class="p-6 sm:p-8 text-center space-y-6 bg-slate-900 text-white rounded-2xl border border-sky-500/50 shadow-2xl relative overflow-hidden animate-bounce-short">
        <div class="absolute -top-12 -right-12 w-40 h-40 bg-sky-500/10 rounded-full blur-3xl pointer-events-none"></div>
        
        <div class="w-16 h-16 rounded-2xl bg-sky-500/20 text-sky-400 mx-auto flex items-center justify-center ring-4 ring-sky-500/30 animate-pulse">
          <i data-lucide="bell-ring" class="w-8 h-8"></i>
        </div>

        <div class="space-y-2">
          <span class="px-3 py-1 rounded-full text-[10px] font-mono font-bold bg-sky-500/20 text-sky-300 border border-sky-500/40 uppercase">
            ${isEn ? 'ACTIVE ALARM TRIGGERED' : 'ALARM BERBUNYI'}
          </span>
          <h3 class="text-2xl sm:text-3xl font-extrabold tracking-tight">${alarm.title}</h3>
          <p class="text-3xl font-mono font-bold text-sky-400">${alarm.time}</p>
        </div>

        <div class="flex flex-wrap items-center justify-center gap-3 pt-2">
          <button id="btnAlarmSnooze5" class="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition flex items-center gap-1.5">
            <i data-lucide="clock" class="w-4 h-4"></i>
            <span>${isEn ? 'Snooze 5 Min' : 'Tunda 5 Menit'}</span>
          </button>
          <button id="btnAlarmDismiss" class="px-6 py-2.5 rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold text-xs transition shadow-lg shadow-sky-500/25 flex items-center gap-1.5">
            <i data-lucide="check-circle" class="w-4 h-4"></i>
            <span>${isEn ? 'Dismiss Alarm' : 'Matikan Alarm'}</span>
          </button>
        </div>
      </div>
    `;

    modal.classList.remove('hidden');
    if (window.lucide) lucide.createIcons();

    card.querySelector('#btnAlarmDismiss').addEventListener('click', () => {
      if (activeAlarmSoundInterval) clearInterval(activeAlarmSoundInterval);
      modal.classList.add('hidden');
    });

    card.querySelector('#btnAlarmSnooze5').addEventListener('click', () => {
      if (activeAlarmSoundInterval) clearInterval(activeAlarmSoundInterval);
      modal.classList.add('hidden');
      snoozeAlarmMinutes(alarm, 5);
    });
  }

  function snoozeAlarmMinutes(alarm, mins) {
    const now = new Date();
    now.setMinutes(now.getMinutes() + mins);
    const hh = String(now.getHours()).padStart(2, '0');
    const mm = String(now.getMinutes()).padStart(2, '0');
    const snoozeTime = `${hh}:${mm}`;

    state.alarms.push({
      id: Date.now(),
      time: snoozeTime,
      title: `(Snooze) ${alarm.title}`,
      sound: alarm.sound,
      enabled: true,
      category: alarm.category,
      repeat: []
    });
    saveState();
    reRenderActiveView();
  }

  function triggerEyeRestAlert() {
    const isEn = window.currentLang === 'en';
    playSynthSound('gentle');

    if ("Notification" in window && Notification.permission === "granted") {
      new Notification(isEn ? "👁️ 20-20-20 Eye-Rest Time!" : "👁️ Istirahat Mata 20 Detik!", {
        body: isEn ? "Look at something 20 feet away for 20 seconds to prevent screen fatigue." : "Alihkan pandangan sejauh 6 meter selama 20 detik untuk mencegah kelelahan mata.",
        icon: 'https://infinitenull.github.io/favicon.ico'
      });
    }
  }

  // Request Notification permission
  window.zzzRequestNotificationPermission = function() {
    if ("Notification" in window) {
      Notification.requestPermission().then(permission => {
        const isEn = window.currentLang === 'en';
        if (permission === 'granted') {
          playSynthSound('chime');
          alert(isEn ? "Windows notification permission granted!" : "Izin notifikasi Windows berhasil diaktifkan!");
        }
      });
    }
  };

  // =========================================================================
  // MASTER RENDER CONTAINER
  // =========================================================================
  window.renderZzzleepSuite = function (container) {
    const isEn = window.currentLang === 'en';

    const totalAlarms = state.alarms.length;
    const activeAlarmsCount = state.alarms.filter(a => a.enabled).length;
    const totalEvents = state.events.length;
    const completedHabits = state.habits.filter(h => h.completedToday).length;

    container.innerHTML = `
      <div class="space-y-6">
        
        <!-- Header Showcase Banner -->
        <div class="p-5 sm:p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col lg:flex-row lg:items-center justify-between gap-5 transition-colors">
          <div class="space-y-1.5 max-w-3xl">
            <div class="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full text-[11px] font-mono font-semibold bg-sky-50 dark:bg-sky-950/60 text-sky-700 dark:text-sky-300 border border-sky-200 dark:border-sky-800">
              <span class="w-2 h-2 rounded-full bg-sky-500 animate-pulse"></span>
              <span>ZZZleep Suite Core • 100% Offline & Private Local Engine</span>
            </div>
            <h2 class="text-xl sm:text-2xl font-extrabold tracking-tight text-slate-900 dark:text-white flex items-center gap-2.5">
              <span>${isEn ? "Smart Desktop Calendar, Precision Alarm & Routine Guardian" : "Kalender Desktop Pintar, Alarm Audio & Pengingat Rutinitas"}</span>
            </h2>
            <p class="text-xs sm:text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
              ${isEn
                ? "Autonomous desktop time-management suite designed for laptops & PCs. Features offline monthly agenda matrix, realtime synthesizer audio alarms, Pomodoro focus cycles, 20-20-20 eye health protector, daily habit streak logs, and standalone Windows .EXE packaging."
                : "Aplikasi pengatur waktu & produktivitas desktop mandiri untuk laptop dan PC. Dilengkapi kalender agenda offline, alarm audio synthesizer realtime, timer pomodoro, pelindung kesehatan mata 20-20-20, pencatat kebiasaan harian, serta dukungan build aplikasi Windows .EXE mandiri."}
            </p>
          </div>

          <div class="flex flex-wrap items-center gap-2.5 shrink-0 font-mono">
            <!-- Digital Clock Display Card -->
            <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 flex items-center gap-3">
              <i data-lucide="clock" class="w-5 h-5 text-sky-500"></i>
              <div>
                <div class="text-[9px] text-slate-400 uppercase tracking-widest">${isEn ? "LIVE TIME" : "WAKTU SISTEM"}</div>
                <div id="zzzLiveClockDisplay" class="text-base font-bold text-slate-900 dark:text-white tracking-wider">--:--:--</div>
              </div>
            </div>

            <button onclick="window.zzzRequestNotificationPermission()" class="px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 font-semibold text-xs flex items-center gap-2 transition border border-slate-200 dark:border-slate-700 shadow-sm" title="${isEn ? "Enable Windows Toast Notifications" : "Aktifkan Notifikasi Banner Windows"}">
              <i data-lucide="bell" class="w-4 h-4 text-sky-600 dark:text-sky-400"></i>
              <span>${isEn ? "Allow Alerts" : "Izin Notifikasi"}</span>
            </button>
          </div>
        </div>

        <!-- Executive Metrics Bar -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3.5">
          
          <div class="p-4 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-1 transition-colors">
            <div class="flex items-center justify-between text-slate-500 dark:text-slate-400 text-xs">
              <span>${isEn ? "Active Alarms" : "Alarm Aktif"}</span>
              <i data-lucide="alarm-clock" class="w-4 h-4 text-sky-500"></i>
            </div>
            <div class="text-xl font-bold font-mono text-slate-900 dark:text-white">${activeAlarmsCount} <span class="text-xs font-sans font-normal text-slate-500">/ ${totalAlarms}</span></div>
            <div class="text-[10px] text-emerald-600 dark:text-emerald-400 font-medium">${isEn ? "Realtime Synth Engine Ready" : "Audio Synth Siap Berbunyi"}</div>
          </div>

          <div class="p-4 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-1 transition-colors">
            <div class="flex items-center justify-between text-slate-500 dark:text-slate-400 text-xs">
              <span>${isEn ? "Scheduled Agendas" : "Agenda Terjadwal"}</span>
              <i data-lucide="calendar" class="w-4 h-4 text-purple-500"></i>
            </div>
            <div class="text-xl font-bold font-mono text-slate-900 dark:text-white">${totalEvents} <span class="text-xs font-sans font-normal text-slate-500">${isEn ? "Items" : "Acara"}</span></div>
            <div class="text-[10px] text-purple-600 dark:text-purple-400 font-medium">${isEn ? "Priority Matrix Tracked" : "Tersinkron di Kalender"}</div>
          </div>

          <div class="p-4 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-1 transition-colors">
            <div class="flex items-center justify-between text-slate-500 dark:text-slate-400 text-xs">
              <span>${isEn ? "Daily Habit Score" : "Kebiasaan Hari Ini"}</span>
              <i data-lucide="check-check" class="w-4 h-4 text-emerald-500"></i>
            </div>
            <div class="text-xl font-bold font-mono text-slate-900 dark:text-white">${completedHabits} <span class="text-xs font-sans font-normal text-slate-500">/ ${state.habits.length}</span></div>
            <div class="text-[10px] text-emerald-600 dark:text-emerald-400 font-medium">${Math.round((completedHabits / state.habits.length) * 100)}% ${isEn ? "Completed" : "Tercapai"}</div>
          </div>

          <div class="p-4 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-1 transition-colors">
            <div class="flex items-center justify-between text-slate-500 dark:text-slate-400 text-xs">
              <span>${isEn ? "Hydration & Eye-Rest" : "Kesehatan Layar"}</span>
              <i data-lucide="eye" class="w-4 h-4 text-amber-500"></i>
            </div>
            <div class="text-xl font-bold font-mono text-slate-900 dark:text-white">${state.sleepHealth.waterGlasses} <span class="text-xs font-sans font-normal text-slate-500">/ 8 ${isEn ? "Glasses" : "Gelas"}</span></div>
            <div class="text-[10px] text-amber-600 dark:text-amber-400 font-medium">${isEn ? "20-20-20 Rule Active" : "Aturan 20-20-20 Aktif"}</div>
          </div>

        </div>

        <!-- Tab Navigation (7 Segments) -->
        <div class="flex items-center gap-1.5 border-b border-slate-200 dark:border-slate-800 overflow-x-auto pb-px scrollbar-none" id="zzzSubTabs">
          <button data-tab="calendar" class="zzz-tab-link ${state.currentTab === 'calendar' ? 'active' : ''} px-3.5 py-2.5 text-xs font-semibold rounded-t-xl transition flex items-center gap-1.5 shrink-0">
            <i data-lucide="calendar" class="w-4 h-4"></i>
            <span>${isEn ? "1. Calendar Matrix" : "1. Kalender Agenda"}</span>
          </button>
          <button data-tab="alarm" class="zzz-tab-link ${state.currentTab === 'alarm' ? 'active' : ''} px-3.5 py-2.5 text-xs font-semibold rounded-t-xl transition flex items-center gap-1.5 shrink-0">
            <i data-lucide="alarm-clock" class="w-4 h-4"></i>
            <span>${isEn ? "2. Alarm Station" : "2. Stasiun Alarm"}</span>
          </button>
          <button data-tab="pomodoro" class="zzz-tab-link ${state.currentTab === 'pomodoro' ? 'active' : ''} px-3.5 py-2.5 text-xs font-semibold rounded-t-xl transition flex items-center gap-1.5 shrink-0">
            <i data-lucide="timer" class="w-4 h-4"></i>
            <span>${isEn ? "3. Pomodoro Focus" : "3. Pomodoro Fokus"}</span>
          </button>
          <button data-tab="sleep" class="zzz-tab-link ${state.currentTab === 'sleep' ? 'active' : ''} px-3.5 py-2.5 text-xs font-semibold rounded-t-xl transition flex items-center gap-1.5 shrink-0">
            <i data-lucide="moon" class="w-4 h-4"></i>
            <span>${isEn ? "4. Eye-Rest & Sleep" : "4. Istirahat & Tidur"}</span>
          </button>
          <button data-tab="habits" class="zzz-tab-link ${state.currentTab === 'habits' ? 'active' : ''} px-3.5 py-2.5 text-xs font-semibold rounded-t-xl transition flex items-center gap-1.5 shrink-0">
            <i data-lucide="sparkles" class="w-4 h-4"></i>
            <span>${isEn ? "5. Daily Routines" : "5. Rutinitas Harian"}</span>
          </button>
          <button data-tab="backup" class="zzz-tab-link ${state.currentTab === 'backup' ? 'active' : ''} px-3.5 py-2.5 text-xs font-semibold rounded-t-xl transition flex items-center gap-1.5 shrink-0">
            <i data-lucide="shield-check" class="w-4 h-4"></i>
            <span>${isEn ? "6. Privacy Vault" : "6. Backup & Privasi"}</span>
          </button>
          <button data-tab="desktop" class="zzz-tab-link ${state.currentTab === 'desktop' ? 'active' : ''} px-3.5 py-2.5 text-xs font-semibold rounded-t-xl transition flex items-center gap-1.5 shrink-0">
            <i data-lucide="monitor" class="w-4 h-4"></i>
            <span>${isEn ? "7. Windows .EXE" : "7. Aplikasi Windows .EXE"}</span>
          </button>
        </div>

        <!-- Active Tab Container -->
        <div id="zzzTabPanel" class="min-h-[460px]"></div>

        <!-- Global In-App Modal Container -->
        <div id="zzzGlobalModal" class="fixed inset-0 z-50 hidden bg-slate-950/70 backdrop-blur-sm flex items-center justify-center p-3 sm:p-6 overflow-y-auto">
          <div id="zzzGlobalModalCard" class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden transition-all">
            <!-- Dynamic modal content -->
          </div>
        </div>

      </div>
    `;

    // Tab switcher events
    container.querySelectorAll('.zzz-tab-link').forEach(btn => {
      btn.addEventListener('click', () => {
        state.currentTab = btn.dataset.tab;
        container.querySelectorAll('.zzz-tab-link').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        renderActiveTab();
      });
    });

    renderActiveTab();
    if (window.lucide) lucide.createIcons();
  };

  function reRenderActiveView() {
    const root = document.getElementById('zzzleepSuiteRoot');
    if (root && typeof window.renderZzzleepSuite === 'function') {
      window.renderZzzleepSuite(root);
    }
  }

  function renderActiveTab() {
    const panel = document.getElementById('zzzTabPanel');
    if (!panel) return;

    if (state.currentTab === 'calendar') renderCalendarTab(panel);
    else if (state.currentTab === 'alarm') renderAlarmTab(panel);
    else if (state.currentTab === 'pomodoro') renderPomodoroTab(panel);
    else if (state.currentTab === 'sleep') renderSleepHealthTab(panel);
    else if (state.currentTab === 'habits') renderHabitsTab(panel);
    else if (state.currentTab === 'backup') renderBackupTab(panel);
    else if (state.currentTab === 'desktop') renderDesktopExeTab(panel);

    if (window.lucide) lucide.createIcons();
  }

  // =========================================================================
  // TAB 1: SMART CALENDAR & AGENDA MATRIX
  // =========================================================================
  function renderCalendarTab(container) {
    const isEn = window.currentLang === 'en';
    const monthNamesId = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'];
    const monthNamesEn = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    const curMonthName = isEn ? monthNamesEn[state.calendarMonth] : monthNamesId[state.calendarMonth];

    const firstDayIndex = new Date(state.calendarYear, state.calendarMonth, 1).getDay();
    const daysInMonth = new Date(state.calendarYear, state.calendarMonth + 1, 0).getDate();

    const selectedEvents = state.events.filter(e => e.date === state.selectedDate);

    container.innerHTML = `
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <!-- Left Column: Interactive Month Grid (7 cols) -->
        <div class="lg:col-span-7 bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
            <div class="flex items-center gap-2">
              <i data-lucide="calendar-days" class="w-5 h-5 text-sky-500"></i>
              <h3 class="font-bold text-sm text-slate-900 dark:text-white">
                ${curMonthName} ${state.calendarYear}
              </h3>
            </div>
            
            <div class="flex items-center gap-1">
              <button id="btnPrevMonth" class="p-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 transition">
                <i data-lucide="chevron-left" class="w-4 h-4"></i>
              </button>
              <button id="btnTodayMonth" class="px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 font-mono text-xs font-semibold transition">
                ${isEn ? 'Today' : 'Hari Ini'}
              </button>
              <button id="btnNextMonth" class="p-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 transition">
                <i data-lucide="chevron-right" class="w-4 h-4"></i>
              </button>
            </div>
          </div>

          <!-- Day Headers -->
          <div class="grid grid-cols-7 gap-1 text-center font-mono text-[11px] font-bold text-slate-400">
            <div>${isEn ? 'Sun' : 'Min'}</div>
            <div>${isEn ? 'Mon' : 'Sen'}</div>
            <div>${isEn ? 'Tue' : 'Sel'}</div>
            <div>${isEn ? 'Wed' : 'Rab'}</div>
            <div>${isEn ? 'Thu' : 'Kam'}</div>
            <div>${isEn ? 'Fri' : 'Jum'}</div>
            <div>${isEn ? 'Sat' : 'Sab'}</div>
          </div>

          <!-- Month Matrix Days -->
          <div class="grid grid-cols-7 gap-1.5 text-xs font-mono" id="calendarDaysGrid">
            ${Array(firstDayIndex).fill('').map(() => `<div class="p-2 min-h-[44px] rounded-lg bg-slate-50/50 dark:bg-slate-950/20 border border-transparent"></div>`).join('')}
            ${Array.from({ length: daysInMonth }, (_, i) => {
              const dayNum = i + 1;
              const dateStr = `${state.calendarYear}-${String(state.calendarMonth + 1).padStart(2, '0')}-${String(dayNum).padStart(2, '0')}`;
              const isSelected = dateStr === state.selectedDate;
              const hasEvents = state.events.some(e => e.date === dateStr);
              const eventCount = state.events.filter(e => e.date === dateStr).length;

              return `
                <button data-date="${dateStr}" class="zzz-cal-day-btn p-2 min-h-[50px] rounded-xl border transition flex flex-col justify-between items-center text-left ${
                  isSelected 
                    ? 'bg-sky-50 dark:bg-sky-950/60 border-sky-500 font-bold text-sky-700 dark:text-sky-300 ring-2 ring-sky-500/20 shadow-sm' 
                    : 'bg-slate-50 dark:bg-slate-950/60 border-slate-200/80 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700'
                }">
                  <span class="text-xs">${dayNum}</span>
                  ${hasEvents ? `<span class="w-1.5 h-1.5 rounded-full bg-sky-500 mt-1" title="${eventCount} ${isEn ? 'agendas' : 'agenda'}"></span>` : '<span class="w-1.5 h-1.5"></span>'}
                </button>
              `;
            }).join('')}
          </div>
        </div>

        <!-- Right Column: Agenda Details for Selected Date (5 cols) -->
        <div class="lg:col-span-5 space-y-4">
          <div class="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
            
            <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
              <div>
                <span class="text-[10px] font-mono text-slate-400 uppercase tracking-wider">${isEn ? "SELECTED AGENDA" : "AGENDA TERPILIH"}</span>
                <h4 class="font-bold text-sm text-slate-900 dark:text-white font-mono">${state.selectedDate}</h4>
              </div>
              
              <button id="btnOpenAddEventModal" class="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 dark:bg-slate-100 dark:hover:bg-white text-white dark:text-slate-900 text-xs font-semibold flex items-center gap-1.5 transition shadow-sm">
                <i data-lucide="plus" class="w-3.5 h-3.5"></i>
                <span>${isEn ? "Add Event" : "Tambah Acara"}</span>
              </button>
            </div>

            <!-- List of events on this date -->
            <div class="space-y-2.5 max-h-[360px] overflow-y-auto pr-1" id="agendaEventsList">
              ${selectedEvents.length > 0 ? selectedEvents.map(e => `
                <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 space-y-1.5 text-xs">
                  <div class="flex items-start justify-between gap-2">
                    <div class="font-bold text-slate-900 dark:text-white text-xs">${e.title}</div>
                    <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase ${
                      e.priority === 'high' ? 'bg-rose-100 dark:bg-rose-950 text-rose-700 dark:text-rose-300' :
                      e.priority === 'medium' ? 'bg-amber-100 dark:bg-amber-950 text-amber-700 dark:text-amber-300' :
                      'bg-emerald-100 dark:bg-emerald-950 text-emerald-700 dark:text-emerald-300'
                    }">
                      ${e.priority}
                    </span>
                  </div>

                  <div class="flex items-center gap-3 text-[11px] font-mono text-slate-500">
                    <span class="flex items-center gap-1"><i data-lucide="clock" class="w-3 h-3 text-sky-500"></i> ${e.time}</span>
                    <span class="capitalize">• ${e.category}</span>
                  </div>

                  ${e.notes ? `<p class="text-slate-600 dark:text-slate-400 text-[11px] pt-1 border-t border-slate-200/50 dark:border-slate-800/50">${e.notes}</p>` : ''}
                  
                  <div class="flex justify-end pt-1">
                    <button onclick="window.zzzDeleteEvent(${e.id})" class="text-[10px] text-rose-500 hover:underline font-mono">
                      ${isEn ? 'Delete' : 'Hapus'}
                    </button>
                  </div>
                </div>
              `).join('') : `
                <div class="p-8 text-center text-slate-400 text-xs space-y-1">
                  <i data-lucide="calendar-x" class="w-8 h-8 mx-auto text-slate-300 dark:text-slate-700"></i>
                  <p>${isEn ? 'No agendas scheduled for this date.' : 'Belum ada agenda pada tanggal ini.'}</p>
                </div>
              `}
            </div>

          </div>
        </div>

      </div>
    `;

    // Calendar navigation listeners
    container.querySelector('#btnPrevMonth').addEventListener('click', () => {
      state.calendarMonth--;
      if (state.calendarMonth < 0) {
        state.calendarMonth = 11;
        state.calendarYear--;
      }
      renderCalendarTab(container);
    });

    container.querySelector('#btnNextMonth').addEventListener('click', () => {
      state.calendarMonth++;
      if (state.calendarMonth > 11) {
        state.calendarMonth = 0;
        state.calendarYear++;
      }
      renderCalendarTab(container);
    });

    container.querySelector('#btnTodayMonth').addEventListener('click', () => {
      const now = new Date();
      state.calendarMonth = now.getMonth();
      state.calendarYear = now.getFullYear();
      const yyyy = now.getFullYear();
      const mm = String(now.getMonth() + 1).padStart(2, '0');
      const dd = String(now.getDate()).padStart(2, '0');
      state.selectedDate = `${yyyy}-${mm}-${dd}`;
      renderCalendarTab(container);
    });

    container.querySelectorAll('.zzz-cal-day-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        state.selectedDate = btn.dataset.date;
        renderCalendarTab(container);
      });
    });

    container.querySelector('#btnOpenAddEventModal').addEventListener('click', () => {
      openAddEventModal();
    });
  }

  function openAddEventModal() {
    const isEn = window.currentLang === 'en';
    const modal = document.getElementById('zzzGlobalModal');
    const card = document.getElementById('zzzGlobalModalCard');
    if (!modal || !card) return;

    card.innerHTML = `
      <div class="p-6 space-y-4 text-slate-900 dark:text-white">
        <div class="border-b border-slate-200 dark:border-slate-800 pb-3 flex items-center justify-between">
          <h3 class="font-bold text-sm flex items-center gap-2">
            <i data-lucide="calendar-plus" class="w-4 h-4 text-sky-500"></i>
            <span>${isEn ? 'Add New Calendar Agenda' : 'Tambah Agenda Kalender'}</span>
          </h3>
          <button onclick="document.getElementById('zzzGlobalModal').classList.add('hidden')" class="text-slate-400 hover:text-slate-600">
            <i data-lucide="x" class="w-4 h-4"></i>
          </button>
        </div>

        <form id="formAddCalendarEvent" class="space-y-3 text-xs">
          <div>
            <label class="block font-medium mb-1">${isEn ? 'Agenda Title:' : 'Judul Agenda:'}</label>
            <input type="text" id="inpEvTitle" required placeholder="${isEn ? 'e.g. Project Code Audit' : 'Contoh: Rapat Evaluasi Proyek'}" class="w-full px-3 py-2 rounded-lg bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-xs focus:ring-1 focus:ring-sky-500 focus:outline-none" />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-medium mb-1">${isEn ? 'Date:' : 'Tanggal:'}</label>
              <input type="date" id="inpEvDate" value="${state.selectedDate}" required class="w-full px-3 py-2 rounded-lg bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 font-mono text-xs focus:ring-1 focus:ring-sky-500 focus:outline-none" />
            </div>
            <div>
              <label class="block font-medium mb-1">${isEn ? 'Time (HH:MM):' : 'Waktu (HH:MM):'}</label>
              <input type="time" id="inpEvTime" value="09:00" required class="w-full px-3 py-2 rounded-lg bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 font-mono text-xs focus:ring-1 focus:ring-sky-500 focus:outline-none" />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-medium mb-1">${isEn ? 'Category:' : 'Kategori:'}</label>
              <select id="inpEvCat" class="w-full px-3 py-2 rounded-lg bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-xs focus:ring-1 focus:ring-sky-500 focus:outline-none">
                <option value="work">💼 Work / Coding</option>
                <option value="study">📚 Study & Research</option>
                <option value="health">💊 Health & Rest</option>
                <option value="personal">⭐ Personal Goal</option>
              </select>
            </div>
            <div>
              <label class="block font-medium mb-1">${isEn ? 'Priority Urgency:' : 'Tingkat Urgensi:'}</label>
              <select id="inpEvPri" class="w-full px-3 py-2 rounded-lg bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-xs focus:ring-1 focus:ring-sky-500 focus:outline-none">
                <option value="high">🔴 High Urgency</option>
                <option value="medium" selected>🟡 Medium</option>
                <option value="low">🟢 Low</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block font-medium mb-1">${isEn ? 'Notes / Description:' : 'Catatan Tambahan:'}</label>
            <textarea id="inpEvNotes" rows="2" placeholder="${isEn ? 'Optional details...' : 'Detail catatan agenda...'}" class="w-full px-3 py-2 rounded-lg bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-xs focus:ring-1 focus:ring-sky-500 focus:outline-none"></textarea>
          </div>

          <div class="pt-3 border-t border-slate-200 dark:border-slate-800 flex justify-end gap-2">
            <button type="button" onclick="document.getElementById('zzzGlobalModal').classList.add('hidden')" class="px-3.5 py-1.5 rounded-lg text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800 transition">${isEn ? 'Cancel' : 'Batal'}</button>
            <button type="submit" class="px-4 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 dark:bg-slate-100 dark:hover:bg-white text-white dark:text-slate-900 font-semibold transition shadow-sm">${isEn ? 'Save Event' : 'Simpan Agenda'}</button>
          </div>
        </form>
      </div>
    `;

    modal.classList.remove('hidden');
    if (window.lucide) lucide.createIcons();

    card.querySelector('#formAddCalendarEvent').addEventListener('submit', (e) => {
      e.preventDefault();
      const title = card.querySelector('#inpEvTitle').value.trim();
      const date = card.querySelector('#inpEvDate').value;
      const time = card.querySelector('#inpEvTime').value;
      const category = card.querySelector('#inpEvCat').value;
      const priority = card.querySelector('#inpEvPri').value;
      const notes = card.querySelector('#inpEvNotes').value.trim();

      state.events.push({ id: Date.now(), title, date, time, category, priority, notes });
      state.selectedDate = date;
      saveState();
      modal.classList.add('hidden');
      reRenderActiveView();
      playSynthSound('chime');
    });
  }

  window.zzzDeleteEvent = function(id) {
    state.events = state.events.filter(e => e.id !== id);
    saveState();
    reRenderActiveView();
  };

  // =========================================================================
  // TAB 2: PRECISION ALARM & WAKEUP STATION
  // =========================================================================
  function renderAlarmTab(container) {
    const isEn = window.currentLang === 'en';

    container.innerHTML = `
      <div class="space-y-6">
        
        <div class="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div class="space-y-1">
            <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <i data-lucide="alarm-clock" class="w-5 h-5 text-sky-500"></i>
              <span>${isEn ? "Precision Desktop Alarms & Audio Chimes" : "Stasiun Alarm Presisi & Audio Chimes"}</span>
            </h3>
            <p class="text-xs text-slate-500">${isEn ? "Offline Web Audio synthesizer triggers instant alarms and Windows notifications without internet." : "Synthesizer audio offline langsung membunyikan alarm dan notifikasi laptop tanpa koneksi internet."}</p>
          </div>

          <button id="btnOpenAddAlarmModal" class="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 dark:bg-slate-100 dark:hover:bg-white text-white dark:text-slate-900 text-xs font-semibold flex items-center gap-2 transition shadow-sm shrink-0">
            <i data-lucide="plus" class="w-4 h-4"></i>
            <span>${isEn ? "Set New Alarm" : "Buat Alarm Baru"}</span>
          </button>
        </div>

        <!-- Alarm Cards Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          ${state.alarms.map(a => `
            <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-3 transition">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-xl flex items-center justify-center ${a.enabled ? 'bg-sky-500/10 text-sky-600 dark:text-sky-400' : 'bg-slate-100 dark:bg-slate-800 text-slate-400'}">
                    <i data-lucide="${a.category === 'sleep' ? 'moon' : (a.category === 'wake' ? 'sunrise' : 'clock')}" class="w-5 h-5"></i>
                  </div>
                  <div>
                    <h4 class="font-bold text-sm text-slate-900 dark:text-white">${a.title}</h4>
                    <div class="flex items-center gap-2 text-[11px] font-mono text-slate-400">
                      <span>Sound: ${a.sound}</span>
                      <button onclick="window.zzzPreviewSound('${a.sound}')" class="text-sky-500 hover:underline font-semibold text-[10px]">
                        ▶ ${isEn ? 'Preview' : 'Tes Suara'}
                      </button>
                    </div>
                  </div>
                </div>

                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" ${a.enabled ? 'checked' : ''} onchange="window.zzzToggleAlarm(${a.id})" class="sr-only peer">
                  <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer dark:bg-slate-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-sky-600"></div>
                </label>
              </div>

              <div class="flex items-baseline justify-between pt-2 border-t border-slate-100 dark:border-slate-800 font-mono">
                <span class="text-3xl font-extrabold text-slate-900 dark:text-white tracking-wider">${a.time}</span>
                <button onclick="window.zzzDeleteAlarm(${a.id})" class="text-xs text-rose-500 hover:underline">
                  ${isEn ? 'Remove' : 'Hapus'}
                </button>
              </div>
            </div>
          `).join('')}
        </div>

      </div>
    `;

    container.querySelector('#btnOpenAddAlarmModal').addEventListener('click', () => {
      openAddAlarmModal();
    });
  }

  function openAddAlarmModal() {
    const isEn = window.currentLang === 'en';
    const modal = document.getElementById('zzzGlobalModal');
    const card = document.getElementById('zzzGlobalModalCard');
    if (!modal || !card) return;

    card.innerHTML = `
      <div class="p-6 space-y-4 text-slate-900 dark:text-white">
        <div class="border-b border-slate-200 dark:border-slate-800 pb-3 flex items-center justify-between">
          <h3 class="font-bold text-sm flex items-center gap-2">
            <i data-lucide="alarm-clock-plus" class="w-4 h-4 text-sky-500"></i>
            <span>${isEn ? 'Set New Precision Alarm' : 'Atur Alarm Baru'}</span>
          </h3>
          <button onclick="document.getElementById('zzzGlobalModal').classList.add('hidden')" class="text-slate-400 hover:text-slate-600">
            <i data-lucide="x" class="w-4 h-4"></i>
          </button>
        </div>

        <form id="formAddAlarm" class="space-y-3 text-xs">
          <div>
            <label class="block font-medium mb-1">${isEn ? 'Alarm Label:' : 'Label Alarm:'}</label>
            <input type="text" id="inpAlTitle" required placeholder="${isEn ? 'e.g. Afternoon Coding Sprint' : 'Contoh: Istirahat Menatap Layar'}" class="w-full px-3 py-2 rounded-lg bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-xs focus:ring-1 focus:ring-sky-500 focus:outline-none" />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-medium mb-1">${isEn ? 'Alarm Time (HH:MM):' : 'Waktu Alarm (HH:MM):'}</label>
              <input type="time" id="inpAlTime" required value="08:00" class="w-full px-3 py-2 rounded-lg bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 font-mono text-sm focus:ring-1 focus:ring-sky-500 focus:outline-none" />
            </div>
            <div>
              <label class="block font-medium mb-1">${isEn ? 'Audio Chime Sound:' : 'Pilihan Suara Alarm:'}</label>
              <select id="inpAlSound" class="w-full px-3 py-2 rounded-lg bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-xs focus:ring-1 focus:ring-sky-500 focus:outline-none">
                <option value="digital">📟 Digital Beep (Retro 880Hz)</option>
                <option value="gentle">🌿 Gentle Chime (C5 Chord)</option>
                <option value="bell">🔔 Acoustic Bell Strike</option>
                <option value="synth">✨ Ambient Synth Wave</option>
              </select>
            </div>
          </div>

          <div class="pt-3 border-t border-slate-200 dark:border-slate-800 flex justify-end gap-2">
            <button type="button" onclick="document.getElementById('zzzGlobalModal').classList.add('hidden')" class="px-3.5 py-1.5 rounded-lg text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800 transition">${isEn ? 'Cancel' : 'Batal'}</button>
            <button type="submit" class="px-4 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 dark:bg-slate-100 dark:hover:bg-white text-white dark:text-slate-900 font-semibold transition shadow-sm">${isEn ? 'Save Alarm' : 'Simpan Alarm'}</button>
          </div>
        </form>
      </div>
    `;

    modal.classList.remove('hidden');
    if (window.lucide) lucide.createIcons();

    card.querySelector('#formAddAlarm').addEventListener('submit', (e) => {
      e.preventDefault();
      const title = card.querySelector('#inpAlTitle').value.trim();
      const time = card.querySelector('#inpAlTime').value;
      const sound = card.querySelector('#inpAlSound').value;

      state.alarms.push({ id: Date.now(), title, time, sound, enabled: true, category: 'work', repeat: [] });
      saveState();
      modal.classList.add('hidden');
      reRenderActiveView();
      playSynthSound(sound);
    });
  }

  window.zzzToggleAlarm = function(id) {
    const a = state.alarms.find(x => x.id === id);
    if (a) {
      a.enabled = !a.enabled;
      saveState();
    }
  };

  window.zzzDeleteAlarm = function(id) {
    state.alarms = state.alarms.filter(x => x.id !== id);
    saveState();
    reRenderActiveView();
  };

  window.zzzPreviewSound = function(soundType) {
    playSynthSound(soundType);
  };

  // =========================================================================
  // TAB 3: POMODORO FOCUS & BREAK ENGINE
  // =========================================================================
  function renderPomodoroTab(container) {
    const isEn = window.currentLang === 'en';
    const p = state.pomodoro;
    const mins = Math.floor(p.secondsLeft / 60);
    const secs = p.secondsLeft % 60;
    const timeFormatted = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

    container.innerHTML = `
      <div class="max-w-2xl mx-auto space-y-6">
        
        <div class="p-8 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm text-center space-y-6">
          
          <!-- Mode Switcher Tabs -->
          <div class="inline-flex p-1 rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs font-mono font-semibold">
            <button onclick="window.zzzSetPomodoroMode('work')" class="px-4 py-2 rounded-lg transition ${p.mode === 'work' ? 'bg-white dark:bg-slate-900 text-slate-900 dark:text-white shadow-sm' : 'text-slate-500 hover:text-slate-900 dark:hover:text-white'}">
              🎯 ${isEn ? 'Work (25m)' : 'Fokus (25m)'}
            </button>
            <button onclick="window.zzzSetPomodoroMode('shortBreak')" class="px-4 py-2 rounded-lg transition ${p.mode === 'shortBreak' ? 'bg-white dark:bg-slate-900 text-slate-900 dark:text-white shadow-sm' : 'text-slate-500 hover:text-slate-900 dark:hover:text-white'}">
              ☕ ${isEn ? 'Short Break (5m)' : 'Rehat (5m)'}
            </button>
            <button onclick="window.zzzSetPomodoroMode('longBreak')" class="px-4 py-2 rounded-lg transition ${p.mode === 'longBreak' ? 'bg-white dark:bg-slate-900 text-slate-900 dark:text-white shadow-sm' : 'text-slate-500 hover:text-slate-900 dark:hover:text-white'}">
              🌿 ${isEn ? 'Long Break (15m)' : 'Istirahat (15m)'}
            </button>
          </div>

          <!-- Big Countdown Clock Display -->
          <div class="space-y-2">
            <div id="pomodoroTimerDisplay" class="text-6xl sm:text-7xl font-mono font-extrabold text-slate-900 dark:text-white tracking-widest">
              ${timeFormatted}
            </div>
            <p class="text-xs text-slate-500 font-mono">
              ${p.mode === 'work' ? (isEn ? 'Deep work interval — Avoid multitasking.' : 'Sesi fokus mendalam — Hindari distraksi.') : (isEn ? 'Rest your eyes and stretch.' : 'Istirahatkan mata dan regangkan badan.')}
            </p>
          </div>

          <!-- Action Controls -->
          <div class="flex items-center justify-center gap-3">
            <button onclick="window.zzzTogglePomodoro()" class="px-6 py-3 rounded-xl ${p.isRunning ? 'bg-amber-500 hover:bg-amber-400 text-slate-950' : 'bg-sky-600 hover:bg-sky-500 text-white'} font-bold text-sm transition shadow-lg flex items-center gap-2">
              <i data-lucide="${p.isRunning ? 'pause' : 'play'}" class="w-4 h-4"></i>
              <span>${p.isRunning ? (isEn ? 'Pause Timer' : 'Jeda Timer') : (isEn ? 'Start Focus' : 'Mulai Fokus')}</span>
            </button>
            <button onclick="window.zzzResetPomodoro()" class="p-3 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 transition" title="Reset">
              <i data-lucide="rotate-ccw" class="w-4 h-4"></i>
            </button>
          </div>

          <!-- Completed sessions stats -->
          <div class="pt-4 border-t border-slate-100 dark:border-slate-800 flex justify-center items-center gap-6 font-mono text-xs text-slate-500">
            <span>${isEn ? 'Completed Focus Sessions:' : 'Sesi Fokus Selesai:'} <strong class="text-sky-500 font-bold">${p.completedSessions}</strong></span>
          </div>

        </div>

      </div>
    `;
  }

  function updatePomodoroUiLive() {
    const el = document.getElementById('pomodoroTimerDisplay');
    if (el) {
      const mins = Math.floor(state.pomodoro.secondsLeft / 60);
      const secs = state.pomodoro.secondsLeft % 60;
      el.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    }
  }

  function handlePomodoroPhaseComplete() {
    playSynthSound('gentle');
    state.pomodoro.isRunning = false;
    if (state.pomodoro.mode === 'work') {
      state.pomodoro.completedSessions++;
      state.pomodoro.mode = 'shortBreak';
      state.pomodoro.secondsLeft = state.pomodoro.shortBreakDuration * 60;
    } else {
      state.pomodoro.mode = 'work';
      state.pomodoro.secondsLeft = state.pomodoro.workDuration * 60;
    }
    saveState();
    reRenderActiveView();
  }

  window.zzzSetPomodoroMode = function(m) {
    state.pomodoro.mode = m;
    state.pomodoro.isRunning = false;
    if (m === 'work') state.pomodoro.secondsLeft = state.pomodoro.workDuration * 60;
    else if (m === 'shortBreak') state.pomodoro.secondsLeft = state.pomodoro.shortBreakDuration * 60;
    else if (m === 'longBreak') state.pomodoro.secondsLeft = state.pomodoro.longBreakDuration * 60;
    saveState();
    reRenderActiveView();
  };

  window.zzzTogglePomodoro = function() {
    state.pomodoro.isRunning = !state.pomodoro.isRunning;
    saveState();
    reRenderActiveView();
  };

  window.zzzResetPomodoro = function() {
    state.pomodoro.isRunning = false;
    window.zzzSetPomodoroMode(state.pomodoro.mode);
  };

  // =========================================================================
  // TAB 4: SLEEP HYGIENE & EYE-REST GUARDIAN
  // =========================================================================
  function renderSleepHealthTab(container) {
    const isEn = window.currentLang === 'en';
    const sh = state.sleepHealth;
    const eyeMins = Math.floor(sh.eyeRestSecondsLeft / 60);
    const eyeSecs = sh.eyeRestSecondsLeft % 60;

    container.innerHTML = `
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        <!-- Eye Strain Protection Card -->
        <div class="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-2">
              <i data-lucide="eye" class="w-5 h-5 text-sky-500"></i>
              <span>${isEn ? "20-20-20 Eye-Rest Guardian" : "Pelindung Kelelahan Mata 20-20-20"}</span>
            </h3>
            <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-sky-100 dark:bg-sky-950 text-sky-800 dark:text-sky-300">
              ${sh.eyeRestRunning ? (isEn ? 'ACTIVE' : 'AKTIF') : (isEn ? 'PAUSED' : 'JEDA')}
            </span>
          </div>

          <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            ${isEn 
              ? "Every 20 minutes spent using a screen, look at something 20 feet (6 meters) away for 20 seconds to prevent digital eye strain."
              : "Setiap 20 menit menatap layar laptop, alihkan pandangan sejauh 6 meter selama 20 detik untuk mencegah mata lelah dan kering."}
          </p>

          <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-center space-y-1">
            <div class="text-xs font-mono text-slate-400">${isEn ? "NEXT REST BREAK IN:" : "ISTIRAHAT MATA BERIKUTNYA:"}</div>
            <div id="eyeRestDisplay" class="text-3xl font-mono font-extrabold text-sky-600 dark:text-sky-400">
              ${String(eyeMins).padStart(2, '0')}:${String(eyeSecs).padStart(2, '0')}
            </div>
          </div>

          <div class="flex justify-center gap-2 pt-2">
            <button onclick="window.zzzToggleEyeRest()" class="px-4 py-2 rounded-lg bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 text-xs font-semibold border border-slate-200 dark:border-slate-700 transition">
              ${sh.eyeRestRunning ? (isEn ? 'Pause Timer' : 'Jeda Timer') : (isEn ? 'Resume' : 'Lanjutkan')}
            </button>
            <button onclick="window.zzzResetEyeRest()" class="px-4 py-2 rounded-lg bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 text-xs font-semibold border border-slate-200 dark:border-slate-700 transition">
              ${isEn ? 'Reset 20m' : 'Reset 20 Menit'}
            </button>
          </div>
        </div>

        <!-- Daily Hydration Tracker -->
        <div class="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-2">
              <i data-lucide="droplet" class="w-5 h-5 text-sky-500"></i>
              <span>${isEn ? "Daily Hydration Goal (8 Glasses)" : "Target Minum Air Harian (8 Gelas)"}</span>
            </h3>
            <span class="font-mono font-bold text-xs text-sky-600 dark:text-sky-400">${sh.waterGlasses} / ${sh.waterGoal}</span>
          </div>

          <p class="text-xs text-slate-600 dark:text-slate-400">
            ${isEn ? "Track daily water intake while coding/working to maintain mental sharpness and focus." : "Pantau asupan air harian saat bekerja di depan laptop agar tetap fokus dan terhidrasi."}
          </p>

          <!-- 8 Water Glasses Grid -->
          <div class="grid grid-cols-4 gap-2.5 pt-2">
            ${Array.from({ length: sh.waterGoal }, (_, i) => {
              const filled = i < sh.waterGlasses;
              return `
                <button onclick="window.zzzSetWaterGlasses(${i + 1})" class="p-3 rounded-xl border transition flex flex-col items-center gap-1 ${
                  filled 
                    ? 'bg-sky-500 text-white border-sky-600 shadow-sm' 
                    : 'bg-slate-50 dark:bg-slate-950 text-slate-400 border-slate-200 dark:border-slate-800 hover:border-sky-400'
                }">
                  <i data-lucide="droplet" class="w-5 h-5"></i>
                  <span class="text-[10px] font-mono">#${i + 1}</span>
                </button>
              `;
            }).join('')}
          </div>

          <div class="flex justify-end pt-2">
            <button onclick="window.zzzSetWaterGlasses(0)" class="text-xs text-slate-400 hover:underline font-mono">
              ${isEn ? 'Reset Glasses' : 'Reset Gelas'}
            </button>
          </div>
        </div>

      </div>
    `;
  }

  function updateEyeRestUiLive() {
    const el = document.getElementById('eyeRestDisplay');
    if (el) {
      const eyeMins = Math.floor(state.sleepHealth.eyeRestSecondsLeft / 60);
      const eyeSecs = state.sleepHealth.eyeRestSecondsLeft % 60;
      el.textContent = `${String(eyeMins).padStart(2, '0')}:${String(eyeSecs).padStart(2, '0')}`;
    }
  }

  window.zzzToggleEyeRest = function() {
    state.sleepHealth.eyeRestRunning = !state.sleepHealth.eyeRestRunning;
    saveState();
    reRenderActiveView();
  };

  window.zzzResetEyeRest = function() {
    state.sleepHealth.eyeRestSecondsLeft = state.sleepHealth.eyeRestInterval * 60;
    saveState();
    reRenderActiveView();
  };

  window.zzzSetWaterGlasses = function(count) {
    state.sleepHealth.waterGlasses = count;
    saveState();
    reRenderActiveView();
    if (count > 0) playSynthSound('chime');
  };

  // =========================================================================
  // TAB 5: DAILY HABITS & ROUTINE CHECKLIST
  // =========================================================================
  function renderHabitsTab(container) {
    const isEn = window.currentLang === 'en';

    container.innerHTML = `
      <div class="space-y-6">
        
        <div class="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div class="space-y-1">
            <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <i data-lucide="sparkles" class="w-5 h-5 text-sky-500"></i>
              <span>${isEn ? "Daily Routine & Habit Streak Tracker" : "Pencatat Rutinitas & Habit Streak Harian"}</span>
            </h3>
            <p class="text-xs text-slate-500">${isEn ? "Build disciplined engineering and health habits with offline streak tracking." : "Bangun disiplin kerja dan kesehatan dengan pencatatan streak kebiasaan harian secara offline."}</p>
          </div>

          <button id="btnOpenAddHabitModal" class="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 dark:bg-slate-100 dark:hover:bg-white text-white dark:text-slate-900 text-xs font-semibold flex items-center gap-2 transition shadow-sm shrink-0">
            <i data-lucide="plus" class="w-4 h-4"></i>
            <span>${isEn ? "Add Habit" : "Tambah Kebiasaan"}</span>
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          ${state.habits.map(h => `
            <div class="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm flex items-center justify-between gap-3 transition">
              <div class="flex items-center gap-3">
                <button onclick="window.zzzToggleHabit(${h.id})" class="w-8 h-8 rounded-xl flex items-center justify-center transition ${
                  h.completedToday 
                    ? 'bg-emerald-500 text-white shadow-sm ring-2 ring-emerald-500/20' 
                    : 'bg-slate-100 dark:bg-slate-800 text-slate-400 hover:border-emerald-400'
                }">
                  <i data-lucide="${h.completedToday ? 'check' : 'circle'}" class="w-4 h-4"></i>
                </button>
                <div>
                  <h4 class="font-bold text-xs text-slate-900 dark:text-white ${h.completedToday ? 'line-through text-slate-400' : ''}">${h.title}</h4>
                  <span class="text-[11px] font-mono text-amber-500 font-semibold flex items-center gap-1">
                    🔥 ${h.streak} ${isEn ? 'days streak' : 'hari streak'}
                  </span>
                </div>
              </div>

              <button onclick="window.zzzDeleteHabit(${h.id})" class="text-slate-400 hover:text-rose-500 p-1">
                <i data-lucide="trash-2" class="w-4 h-4"></i>
              </button>
            </div>
          `).join('')}
        </div>

      </div>
    `;

    container.querySelector('#btnOpenAddHabitModal').addEventListener('click', () => {
      openAddHabitModal();
    });
  }

  function openAddHabitModal() {
    const isEn = window.currentLang === 'en';
    const modal = document.getElementById('zzzGlobalModal');
    const card = document.getElementById('zzzGlobalModalCard');
    if (!modal || !card) return;

    card.innerHTML = `
      <div class="p-6 space-y-4 text-slate-900 dark:text-white">
        <div class="border-b border-slate-200 dark:border-slate-800 pb-3 flex items-center justify-between">
          <h3 class="font-bold text-sm flex items-center gap-2">
            <i data-lucide="sparkles" class="w-4 h-4 text-sky-500"></i>
            <span>${isEn ? 'Add Daily Habit' : 'Tambah Kebiasaan Harian'}</span>
          </h3>
          <button onclick="document.getElementById('zzzGlobalModal').classList.add('hidden')" class="text-slate-400 hover:text-slate-600">
            <i data-lucide="x" class="w-4 h-4"></i>
          </button>
        </div>

        <form id="formAddHabit" class="space-y-3 text-xs">
          <div>
            <label class="block font-medium mb-1">${isEn ? 'Habit Description:' : 'Nama Kebiasaan:'}</label>
            <input type="text" id="inpHabitTitle" required placeholder="${isEn ? 'e.g. 15 Mins Code Refactor' : 'Contoh: Olahraga Ringan 15 Menit'}" class="w-full px-3 py-2 rounded-lg bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-xs focus:ring-1 focus:ring-sky-500 focus:outline-none" />
          </div>

          <div class="pt-3 border-t border-slate-200 dark:border-slate-800 flex justify-end gap-2">
            <button type="button" onclick="document.getElementById('zzzGlobalModal').classList.add('hidden')" class="px-3.5 py-1.5 rounded-lg text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800 transition">${isEn ? 'Cancel' : 'Batal'}</button>
            <button type="submit" class="px-4 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 dark:bg-slate-100 dark:hover:bg-white text-white dark:text-slate-900 font-semibold transition shadow-sm">${isEn ? 'Add Habit' : 'Simpan'}</button>
          </div>
        </form>
      </div>
    `;

    modal.classList.remove('hidden');
    if (window.lucide) lucide.createIcons();

    card.querySelector('#formAddHabit').addEventListener('submit', (e) => {
      e.preventDefault();
      const title = card.querySelector('#inpHabitTitle').value.trim();
      state.habits.push({ id: Date.now(), title, icon: 'check', streak: 1, completedToday: false });
      saveState();
      modal.classList.add('hidden');
      reRenderActiveView();
      playSynthSound('chime');
    });
  }

  window.zzzToggleHabit = function(id) {
    const h = state.habits.find(x => x.id === id);
    if (h) {
      h.completedToday = !h.completedToday;
      if (h.completedToday) {
        h.streak++;
        playSynthSound('chime');
      } else {
        h.streak = Math.max(0, h.streak - 1);
      }
      saveState();
      reRenderActiveView();
    }
  };

  window.zzzDeleteHabit = function(id) {
    state.habits = state.habits.filter(x => x.id !== id);
    saveState();
    reRenderActiveView();
  };

  // =========================================================================
  // TAB 6: LOCAL PRIVACY VAULT & JSON BACKUP
  // =========================================================================
  function renderBackupTab(container) {
    const isEn = window.currentLang === 'en';

    container.innerHTML = `
      <div class="max-w-3xl mx-auto space-y-6">
        
        <div class="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-5">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
              <i data-lucide="shield-check" class="w-6 h-6"></i>
            </div>
            <div>
              <h3 class="font-bold text-base text-slate-900 dark:text-white">
                ${isEn ? "100% Offline Privacy Vault & Data Export" : "Brankas Privasi 100% Offline & Ekspor Data"}
              </h3>
              <p class="text-xs text-slate-500">
                ${isEn ? "Your schedules, alarms, and personal habits never leave this laptop. Zero analytics, zero cloud tracking." : "Data jadwal, alarm, dan rutinitas tidak pernah dikirim ke internet. Bebas pelacakan cloud."}
              </p>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
            
            <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 space-y-3">
              <h4 class="font-bold text-xs text-slate-900 dark:text-white flex items-center gap-1.5">
                <i data-lucide="download" class="w-4 h-4 text-sky-500"></i>
                <span>${isEn ? "Export Backup JSON" : "Cadangkan Data (JSON)"}</span>
              </h4>
              <p class="text-[11px] text-slate-500">
                ${isEn ? "Download complete offline backup file of all your alarms, calendar agendas, and habit streaks." : "Unduh file cadangan lengkap berisi semua alarm, jadwal kalender, dan habit streak."}
              </p>
              <button onclick="window.zzzExportJson()" class="w-full py-2 rounded-lg bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs transition shadow-sm">
                ${isEn ? "Download Backup JSON" : "Unduh File Backup"}
              </button>
            </div>

            <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 space-y-3">
              <h4 class="font-bold text-xs text-slate-900 dark:text-white flex items-center gap-1.5">
                <i data-lucide="upload" class="w-4 h-4 text-purple-500"></i>
                <span>${isEn ? "Restore / Import Backup" : "Pulihkan Cadangan (Restore)"}</span>
              </h4>
              <p class="text-[11px] text-slate-500">
                ${isEn ? "Import a previously exported JSON backup file to instantly restore your data." : "Impor file JSON cadangan untuk memulihkan seluruh pengaturan jadwal Anda."}
              </p>
              <label class="block w-full py-2 rounded-lg bg-slate-900 hover:bg-slate-800 dark:bg-slate-100 dark:hover:bg-white text-white dark:text-slate-900 font-semibold text-xs text-center cursor-pointer transition shadow-sm">
                <span>${isEn ? "Select JSON File" : "Pilih File JSON"}</span>
                <input type="file" accept=".json" onchange="window.zzzImportJson(event)" class="hidden" />
              </label>
            </div>

          </div>

          <div class="pt-4 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-xs font-mono">
            <span class="text-slate-400">${isEn ? "Need clean demo state?" : "Ingin mereset ke data awal?"}</span>
            <button onclick="window.zzzResetDemoData()" class="text-rose-500 hover:underline">
              ${isEn ? "Reset Demo State" : "Reset Data Bawaan"}
            </button>
          </div>
        </div>

      </div>
    `;
  }

  window.zzzExportJson = function() {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(state, null, 2));
    const dlAnchor = document.createElement('a');
    dlAnchor.setAttribute("href", dataStr);
    dlAnchor.setAttribute("download", `zzzleep_backup_${new Date().toISOString().slice(0,10)}.json`);
    document.body.appendChild(dlAnchor);
    dlAnchor.click();
    dlAnchor.remove();
  };

  window.zzzImportJson = function(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
      try {
        const imported = JSON.parse(e.target.result);
        state = { ...getInitialState(), ...imported };
        saveState();
        reRenderActiveView();
        alert(window.currentLang === 'en' ? "Data restored successfully!" : "Data berhasil dipulihkan!");
      } catch (err) {
        alert(window.currentLang === 'en' ? "Invalid JSON file!" : "Format file JSON tidak valid!");
      }
    };
    reader.readAsText(file);
  };

  window.zzzResetDemoData = function() {
    const isEn = window.currentLang === 'en';
    if (confirm(isEn ? "Reset all ZZZleep data to initial state?" : "Reset semua data ZZZleep ke kondisi awal?")) {
      localStorage.removeItem(STORAGE_KEY);
      state = getInitialState();
      saveState();
      reRenderActiveView();
    }
  };

  // =========================================================================
  // TAB 7: NATIVE WINDOWS .EXE & SOURCE CODE
  // =========================================================================
  function renderDesktopExeTab(container) {
    const isEn = window.currentLang === 'en';

    container.innerHTML = `
      <div class="space-y-6">
        
        <div class="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="font-bold text-base text-slate-900 dark:text-white flex items-center gap-2">
              <i data-lucide="monitor" class="w-5 h-5 text-sky-500"></i>
              <span>${isEn ? "Standalone Native Windows Desktop Application (.EXE)" : "Aplikasi Desktop Native Windows Standalone (.EXE)"}</span>
            </h3>
            <span class="px-2.5 py-0.5 rounded text-[10px] font-mono font-bold bg-sky-100 dark:bg-sky-950 text-sky-800 dark:text-sky-300">
              Python 3 • PyInstaller Ready
            </span>
          </div>

          <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            ${isEn
              ? "ZZZleep Suite includes a production-grade Python desktop client located in the <code>desktop/</code> directory. It runs natively in the Windows System Tray, monitors alarms in the background even when browser is closed, and triggers native Windows notifications."
              : "ZZZleep Suite menyertakan klien desktop Python native di folder <code>desktop/</code>. Aplikasi ini berjalan di latar belakang (System Tray Windows), mengecek alarm saat browser ditutup, dan memunculkan banner notifikasi Windows asli."}
          </p>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 font-mono text-xs pt-2">
            <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800">
              <div class="text-[10px] text-slate-400 uppercase">SYSTEM TRAY</div>
              <div class="font-bold text-slate-800 dark:text-slate-200">Background Daemon</div>
            </div>
            <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800">
              <div class="text-[10px] text-slate-400 uppercase">OFFLINE AUDIO</div>
              <div class="font-bold text-slate-800 dark:text-slate-200">Winsound / Local Chimes</div>
            </div>
            <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800">
              <div class="text-[10px] text-slate-400 uppercase">BUILD TARGET</div>
              <div class="font-bold text-slate-800 dark:text-slate-200">ZZZleep.exe (Single File)</div>
            </div>
          </div>
        </div>

        <!-- How to build executable instructions -->
        <div class="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h4 class="font-bold text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400 font-mono">
            ${isEn ? "Terminal Commands to Build ZZZleep.exe" : "Perintah Terminal Untuk Build ZZZleep.exe"}
          </h4>

          <pre class="bg-slate-950 text-slate-100 p-4 rounded-xl text-xs font-mono overflow-x-auto leading-relaxed border border-slate-800 shadow-inner"><code># 1. Masuk ke direktori desktop
cd "desktop"

# 2. Install dependensi PyInstaller (jika belum terpasang)
pip install -r requirements.txt

# 3. Jalankan script build otomatis
python build_exe.py

# Hasil file executable akan otomatis terbit di folder dist/ZZZleep.exe</code></pre>
        </div>

      </div>
    `;
  }

  // Initialize background alarm checking
  initAlarmWorker();

})();
