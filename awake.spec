# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller配置文件 - 离线唤醒词检测系统
"""

import sys
import os
from PyInstaller.utils.hooks import collect_data_files

# 收集pvporcupine的数据文件
porcupine_datas = collect_data_files('pvporcupine')

# 添加模型文件
datas = []
datas.extend(porcupine_datas)

# 添加中文语言模型（必需）
if os.path.exists('porcupine_params_zh.pv'):
    datas.append(('porcupine_params_zh.pv', '.'))
    print("添加中文语言模型: porcupine_params_zh.pv")

# 唤醒词模型文件（检查所有可能的平台版本）
model_files = [
    '迈灵迈灵_zh_windows_v3_0_0.ppn',  # Windows版本
    '迈灵迈灵_zh_linux_v3_0_0.ppn',    # Linux版本
    '迈灵迈灵_zh_mac_v3_0_0.ppn',      # Mac版本
]

for model_file in model_files:
    if os.path.exists(model_file):
        datas.append((model_file, '.'))
        print(f"添加模型文件: {model_file}")

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