#!/usr/bin/env python3
"""
ZZZleep Suite — Automated PyInstaller Executable Builder
Author: Rizki Ananda, S.Kom (@InfiniteNull)

Compiles desktop/app.py into a standalone single-file Windows executable (ZZZleep.exe).
"""

import os
import sys
import subprocess

def build():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(script_dir, "app.py")
    dist_dir = os.path.join(script_dir, "dist")

    print("============================================================")
    print("  ZZZleep Suite — Native Windows Executable (.EXE) Builder  ")
    print("============================================================")
    print(f"Source script: {app_path}")

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onefile",
        "--name=ZZZleep",
        app_path
    ]

    print(f"Running command: {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=script_dir)

    if res.returncode == 0:
        exe_path = os.path.join(dist_dir, "ZZZleep.exe")
        print("\n[SUCCESS] Build completed successfully!")
        print(f"Standalone executable created at: {exe_path}")
    else:
        print("\n[ERROR] PyInstaller build failed. Ensure pyinstaller is installed: pip install pyinstaller")

if __name__ == "__main__":
    build()
