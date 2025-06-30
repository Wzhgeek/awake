# -*- mode: python ; coding: utf-8 -*-
import os
import pvporcupine
import platform
import sys
from pathlib import Path

block_cipher = None

# 获取pvporcupine库的路径
pvporcupine_path = os.path.dirname(pvporcupine.__file__)

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

a = Analysis(
    ['wake_word_detector.py'],
    pathex=[current_dir],
    binaries=[
        # 添加Porcupine动态库
        (os.path.join(pvporcupine_path, 'lib', 'windows', 'amd64', 'libpv_porcupine.dll'), 'pvporcupine/lib/windows/amd64'),
    ],
    datas=[
        # 添加自定义唤醒词模型
        (os.path.join(current_dir, '迈灵迈灵_zh_windows_v3_0_0.ppn'), '.'),
        # 添加中文基础模型
        (os.path.join(current_dir, 'porcupine_params_zh.pv'), '.'),
        # 添加pvporcupine的资源文件
        (os.path.join(pvporcupine_path, 'lib', 'common', '*'), 'pvporcupine/lib/common'),
        (os.path.join(pvporcupine_path, 'resources', '*'), 'pvporcupine/resources'),
    ],
    hiddenimports=[
        'pyaudio',
        'pvporcupine',
        'struct',
        'json',
        'pathlib'
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
    name='wake_word_detector',
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
    icon='NONE'
) 