# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['CardioView.py'],
    pathex=[],
    binaries=[],
    datas=[('Logo.png', '.')],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='CardioView',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='Logo_icon.ico',
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

icon_path = 'Logo_icon.ico'
desktop_icon = [("CardioView", icon_path, '.')]

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas + desktop_icon,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='CardioView',
)
