"""Standalone EXE build automation script for StorageManager Pro."""

import os
import sys
import subprocess
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
SPEC_FILE = ROOT_DIR / "StorageManagerPro.spec"
DIST_DIR = ROOT_DIR / "dist"
BUILD_DIR = ROOT_DIR / "build"
ASSETS_DIR = ROOT_DIR / "storage_manager" / "assets"
ICON_FILE = ASSETS_DIR / "app_icon.ico"


def build_exe():
    print("==================================================")
    print("   StorageManager Pro - Windows EXE Build Suite   ")
    print("==================================================")

    # 1. Verify Icon exists
    if not ICON_FILE.exists():
        print(f"Icon not found at {ICON_FILE}. Generating icon...")
        from storage_manager.assets.generate_icon import generate_app_icon
        generate_app_icon(ICON_FILE)

    # Terminate any running StorageManagerPro.exe instances before rebuilding
    try:
        subprocess.run(["taskkill", "/F", "/IM", "StorageManagerPro.exe"], capture_output=True)
    except Exception:
        pass

    # 2. Clean previous build artifacts
    if DIST_DIR.exists():
        print("Cleaning previous dist directory...")
        shutil.rmtree(DIST_DIR, ignore_errors=True)

    if BUILD_DIR.exists():
        print("Cleaning previous build directory...")
        shutil.rmtree(BUILD_DIR, ignore_errors=True)

    # 3. Execute PyInstaller
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "--noconfirm",
        str(SPEC_FILE),
    ]

    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=str(ROOT_DIR))

    if result.returncode != 0:
        print("\n[ERROR] PyInstaller build failed!")
        sys.exit(result.returncode)

    exe_path = DIST_DIR / "StorageManagerPro.exe"
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print("\n==================================================")
        print("  BUILD SUCCESSFUL! Standalone Executable Ready   ")
        print("==================================================")
        print(f"Path: {exe_path}")
        print(f"Size: {size_mb:.2f} MB")
        print("Target: Windows 11 / 10 64-bit (Admin UAC Elevation Enabled)")
    else:
        print(f"\n[WARNING] Build finished but {exe_path} was not found.")


if __name__ == "__main__":
    build_exe()

