# -*- mode: python ; coding: utf-8 -*-
import os
import pvporcupine
import sys
from pathlib import Path

block_cipher = None

# 获取 pvporcupine 包的安装路径
pv_path = os.path.dirname(pvporcupine.__file__)

# 添加需要打包的数据文件
added_files = [
    ('迈灵迈灵_zh_windows_v3_0_0.ppn', '.'),  # 唤醒词模型
    ('porcupine_params_zh.pv', '.'),  # 中文语言包
]

# 添加 pvporcupine 的资源文件
pv_lib_path = os.path.join(pv_path, 'lib')
pv_resources_path = os.path.join(pv_path, 'resources')

for root, dirs, files in os.walk(pv_path):
    for file in files:
        if file.endswith(('.dll', '.so', '.dylib', '.pv', '.ppn')):
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, pv_path)
            target_path = os.path.join('pvporcupine', rel_path)
            added_files.append((file_path, os.path.dirname(target_path)))

a = Analysis(
    ['wake_word_detector.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=['pvporcupine'],
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
) 