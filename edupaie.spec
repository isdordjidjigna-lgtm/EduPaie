# -*- mode: python ; coding: utf-8 -*-
"""Spec PyInstaller pour EduPaie."""
from PyInstaller.utils.hooks import collect_data_files

# Imports obligatoires
hiddenimports = [
    'PySide6', 'PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets',
    'PySide6.QtNetwork', 'PySide6.QtSvg',
    'shiboken6',
    'sqlite3',
    'reportlab', 'reportlab.pdfgen.canvas',
    'reportlab.lib.pagesizes', 'reportlab.lib.units',
]

# Données à inclure dans le .exe
datas = [
    ('database/schema.sql', 'database'),
    ('edupaie.db', '.'),
]
datas += collect_data_files('reportlab')
datas += collect_data_files('PySide6')

# Modules à exclure (réduit la taille du .exe)
excludes = [
    'matplotlib', 'scipy', 'pandas',
    'PySide6.QtWebEngineCore', 'PySide6.QtWebEngineWidgets',
    'PySide6.Qt3DCore', 'PySide6.Qt3DRender',
    'PySide6.QtMultimedia', 'PySide6.QtMultimediaWidgets',
    'PySide6.QtQuick', 'PySide6.QtQml',
    'PySide6.QtCharts', 'PySide6.QtDataVisualization',
    'tkinter', 'unittest', 'test', 'pydoc',
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
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