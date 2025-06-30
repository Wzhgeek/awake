# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller configuration file - Offline Wake Word Detection System
"""

import sys
import os
from PyInstaller.utils.hooks import collect_data_files

# Collect pvporcupine data files
porcupine_datas = collect_data_files('pvporcupine')

# Add model files
datas = []
datas.extend(porcupine_datas)

# Add Chinese language model (required)
if os.path.exists('porcupine_params_zh.pv'):
    datas.append(('porcupine_params_zh.pv', '.'))
    print("[INFO] Adding Chinese language model: porcupine_params_zh.pv")

# Wake word model files (check all possible platform versions)
model_files = [
    '迈灵迈灵_zh_windows_v3_0_0.ppn',  # Windows version
]

for model_file in model_files:
    if os.path.exists(model_file):
        datas.append((model_file, '.'))
        print(f"[INFO] Adding wake word model: {model_file}")

block_cipher = None

a = Analysis(
    ['wake_word_detector.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'pvporcupine',
        'pyaudio',
        'struct',
        'threading',
        'time',
        'json',
        'os',
        'sys'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='awake',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
) 