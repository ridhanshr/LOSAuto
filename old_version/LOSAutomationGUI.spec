# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# Collect everything from src directory
datas = []
binaries = []
hiddenimports = [
    'pyodbc', 
    'faker', 
    'openpyxl', 
    'selenium', 
    'PIL', 
    'tkinter',
    'multiprocessing'
]

# Ensure src is collected
tmp_ret = collect_all('src')
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]

# Add drivers
# We use datas here to just copy the exe files into the dist folder structure if needed, 
# but usually they are better kept external or handled by the code path.
# However, the user's drivers/ folder is in the root.
datas.append(('drivers/*', 'drivers'))

a = Analysis(
    ['run.py'],
    pathex=[os.getcwd()],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='LOSAutomationGUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False, # Set to False for windowed app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
