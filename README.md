# StorageManager Pro 🚀
### Native Windows Desktop Storage Optimization & NTFS Junction Suite

**StorageManager Pro** is a high-performance native Windows desktop application engineered in Python 3.12+ and PySide6. It is specifically architected to liberate gigabytes of storage from space-constrained Windows system drives (C:) by moving bulky user data, application caches, software, and AI models to secondary drives (D:, E:, F:, etc.) while preserving 100% application transparency using native **NTFS Junctions (Directory Reparse Points)**.

---

## 🌟 Key Features

1. **Dashboard Overview**
   - Real-time disk telemetry for System Drive C: and all mounted storage volumes.
   - Live KPI tracking: Total storage saved via junctions, aggregate AppData size, and active healthy junctions.
   - Comprehensive operation journal and activity audit history backed by SQLite WAL mode.

2. **AppData Manager**
   - Deep scanning across `AppData\Local`, `AppData\Roaming`, and `AppData\LocalLow`.
   - Granular directory size calculations and file counting.
   - Safety compatibility assessment: `Safe`, `Process Running`, `Protected System`, `Already Relocated`.
   - Never moves the entire AppData root; guarantees folder-by-folder isolation.
   - 1-click verified relocation and instant rollback to C: drive.

3. **Software Manager**
   - 64-bit and 32-bit Windows Registry inspection across HKLM and HKCU.
   - App-specific relocation for user-installed software and independent tools.
   - Native management of Windows default software installation targets (`ProgramFilesDir` / `ProgramFilesDir (x86)`).
   - Clear architectural distinction: explains that installation preferences guide new installers and do not modify existing programs.

4. **Cache & Temporary Files Manager**
   - Discovers and cleans Windows System Temp and User Temp with safe locked-file skipping.
   - Detects developer package caches: Python pip, uv, Node.js npm, pnpm global store, Yarn, NuGet.
   - Detects browser caches: Google Chrome, Microsoft Edge, Brave Browser.
   - Relocates supported package stores to secondary drives.

5. **Developer Tools Manager**
   - 1-click relocation for heavyweight VS Code extensions (`.vscode/extensions`).
   - Relocation for Cursor editor extensions and global npm CLI tools.
   - Project artifacts scanner: scans workspaces for heavy `node_modules`, `.venv`, and `target` build directories.

6. **AI Models & Checkpoints Manager**
   - Hugging Face cache (`HF_HOME` / `~/.cache/huggingface`).
   - Ollama models (`OLLAMA_MODELS` / `~/.ollama/models`).
   - LM Studio models (`~/.cache/lm-studio/models`).
   - PyTorch Hub checkpoints (`~/.cache/torch/hub`).
   - Antigravity agent data context.
   - Custom model directory selector.
   - Dual relocation strategies: transparent NTFS Junctions or permanent Windows user environment variables.

7. **Downloads & User Library Folders**
   - Relocates Windows Known Folders: Downloads, Documents, Desktop, Videos, Music, Pictures.
   - Relocates any custom user folder.

8. **Drive & Filesystem Health Manager**
   - Physical and logical partition inspection.
   - Filesystem verification: validates NTFS / ReFS before allowing junction operations (protects against FAT32/exFAT incompatibility).
   - Recommends optimal destination drive based on free capacity.

9. **Safety Engine & Rollback Engine (Core Architecture)**
   - **Pre-flight Checks**: Administrator privileges, destination free space (+10% margin + 500MB headroom), destination collision check.
   - **Process Detection**: Identifies running processes holding open file locks or binary references using `psutil` and native Win32 APIs.
   - **Transactional Atomic Swap**:
     1. Copies data to target destination.
     2. Verifies destination byte count and file count match source.
     3. Renames source to a temporary rollback backup (`.__sm_temp_<timestamp>`).
     4. Creates NTFS Junction pointing to destination.
     5. Verifies junction resolution and readability.
     6. Only cleans up temporary backup after full verification passes.
     7. Instant rollback on any failure.
   - **Simulation Mode (Dry Run)**: Tests validation and logs operations without touching disk.

10. **Backup & Broken Junction Diagnostics**
    - 1-click restoration of any relocated folder back to C:.
    - Automatically diagnoses detached drives, missing target folders, and broken reparse points.
    - Cleans up leftover temporary backups from interrupted power cycles.

---

## 🛠️ Technology Stack

| Layer | Component | Purpose |
|---|---|---|
| **GUI Framework** | PySide6 (Qt 6.12+) | Native Windows desktop UI, Fluent dark theme, QThread async workers |
| **Database** | SQLite3 (WAL mode) | Persistent settings, operation journals, relocated item tracking |
| **System Telemetry** | psutil | Volume metrics, partition enumeration, process lock detection |
| **Windows API** | pywin32 & ctypes | Reparse points, volume info, Known Folders, registry manipulation |
| **Filesystem** | pathlib, shutil, os | Safe chunked file streaming, directory tree verification |
| **Packaging** | PyInstaller 6.22+ | Standalone 64-bit Windows executable (`StorageManagerPro.exe`) |

---

## 📁 Project Architecture

```
StorageManagerPro/
├── run.py                          # Launcher script
├── build_exe.py                    # Standalone PyInstaller build script
├── StorageManagerPro.spec          # PyInstaller packaging configuration
├── version_info.txt                # Windows PE executable version resource
├── requirements.txt                # Python dependencies
├── README.md                       # Comprehensive technical documentation
├── storage_manager/
│   ├── __init__.py
│   ├── main.py                     # Application entry point
│   ├── config/
│   │   ├── constants.py            # System paths, color palette, protected directories
│   │   └── settings.py             # AppSettings dataclass & SettingsManager
│   ├── database/
│   │   ├── models.py               # Data models (DriveInfo, RelocatedItem, etc.)
│   │   └── db_manager.py           # SQLite operations journal and settings storage
│   ├── core/
│   │   ├── windows_api.py          # Native Win32 API calls & process lock detection
│   │   ├── junction_manager.py     # mklink /J creation, resolution, safe removal
│   │   ├── safety_engine.py        # Pre-flight validation, disk space, protected paths
│   │   ├── relocation_engine.py    # Atomic transactional migration pipeline
│   │   ├── backup_engine.py        # Rollback engine and broken junction diagnosis
│   │   ├── drive_scanner.py        # Storage volume and filesystem inspection
│   │   ├── appdata_scanner.py      # AppData Local/Roaming/LocalLow directory scanner
│   │   ├── software_scanner.py     # Registry installed software and default dirs
│   │   ├── cache_manager.py        # Temporary files and package manager caches
│   │   ├── developer_manager.py    # VS Code, npm, pnpm, and project artifacts scanner
│   │   ├── ai_model_manager.py     # Hugging Face, Ollama, ComfyUI model directories
│   │   └── downloads_manager.py    # Windows Known Folders (Downloads, Desktop, etc.)
│   ├── services/
│   │   ├── logger_service.py       # Multi-target logging (file, console, UI)
│   │   └── worker_threads.py       # PySide6 QThread background workers
│   ├── ui/
│   │   ├── main_window.py          # Main application window & page router
│   │   ├── style.py                # Fluent dark theme stylesheet & formatting helpers
│   │   ├── dashboard.py            # Overview dashboard
│   │   ├── appdata_page.py         # AppData Manager
│   │   ├── software_page.py        # Software Manager
│   │   ├── cache_page.py           # Cache Manager
│   │   ├── developer_page.py       # Developer Tools
│   │   ├── ai_models_page.py       # AI Models Manager
│   │   ├── downloads_page.py       # Downloads Manager
│   │   ├── drive_page.py           # Drive Manager
│   │   ├── backup_page.py          # Backup & Restore
│   │   ├── settings_page.py        # Application Settings
│   │   └── components/
│   │       ├── sidebar.py          # Modern dark sidebar with icons & active states
│   │       ├── metric_card.py      # Hero drive bars, mini drive cards, KPI widgets
│   │       └── dialogs.py          # Confirmation, progress, and process dialogs
│   └── assets/
│       ├── app_icon.ico            # High-resolution multi-frame application icon
│       └── generate_icon.py        # Programmatic icon generator
└── tests/
    ├── test_core_engines.py        # Windows API, Junctions, Safety, Relocation tests
    ├── test_extended_managers.py   # Drive, Software, Cache, DevTools, AI model tests
    └── test_ui_pages.py            # Headless UI tests for all 10 pages
```

---

## 🚀 Running StorageManager Pro

### 1. From Python Source
```powershell
# Navigate to the project root
cd d:\Projects\StorageManagerPro

# Install required dependencies
pip install -r requirements.txt

# Launch application
python run.py
```

### 2. Building Standalone Windows Executable (.exe)
```powershell
python build_exe.py
```
Output executable will be generated at:
`d:\Projects\StorageManagerPro\dist\StorageManagerPro.exe`

---

## 🔒 Safety Guarantees

1. **Original Data Preservation**: Original data is NEVER removed until the full directory copy is verified for byte and file count integrity, and the NTFS junction has been created and verified to resolve to the target folder.
2. **Safe Junction Removal**: Deleting or restoring an NTFS junction uses `os.rmdir()` / `RemoveDirectoryW` which exclusively removes the reparse link and never deletes the target files.
3. **Blacklisted System Folders**: `C:\Windows`, `C:\Program Files\WindowsApps`, system boot files, and entire AppData roots are strictly protected and blocked from relocation.
4. **Filesystem Validation**: Non-NTFS partitions (FAT32, exFAT) are automatically detected and blocked from creating junctions.
5. **Dry Run Simulation**: Allows users to preview every operation without modifying disk state.

