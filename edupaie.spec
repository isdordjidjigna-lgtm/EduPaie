# -*- mode: python ; coding: utf-8 -*-
"""Spec PyInstaller pour EduPaie."""
import os
import sys

# Chemins absolus
VENV_DIR = os.path.abspath(os.path.join(os.path.dirname(sys.executable), ".."))
SITE_PACKAGES = os.path.join(VENV_DIR, "Lib", "site-packages")

print(f"[SPEC] Python     : {sys.executable}")
print(f"[SPEC] Site-pack  : {SITE_PACKAGES}")

# Imports obligatoires
hiddenimports = [
    'PySide6', 'PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets',
    'PySide6.QtNetwork', 'PySide6.QtSvg',
    'shiboken6',
    'sqlite3',
    'reportlab', 'reportlab.pdfgen.canvas',
    'reportlab.lib.pagesizes', 'reportlab.lib.units',
]

# Données
datas = [('database/schema.sql', 'database')]
try:
    from PyInstaller.utils.hooks import collect_data_files
    datas += collect_data_files('reportlab')
    datas += collect_data_files('PySide6')
    print(f"[SPEC] Datas collectées : {len(datas)}")
except Exception as e:
    print(f"[SPEC] Erreur collect_data_files : {e}")

a = Analysis(
    ['main.py'],
    pathex=[SITE_PACKAGES],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz, a.scripts, a.binaries, a.datas, [],
    name='EduPaie',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
