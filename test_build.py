#!/usr/bin/env python3
"""
Script de prueba para verificar PyInstaller
"""

import sys
import subprocess
from pathlib import Path

def test_pyinstaller():
    """Probar PyInstaller con un archivo simple"""
    print("🔨 Testando PyInstaller...")
    
    # Crear archivo spec simple
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.building.build_main import Analysis, PYZ, EXE

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=['tkinter', 'PIL'],
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
    name='KONTROL-PLUS-TEST',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None
)
'''
    
    # Escribir spec file
    spec_file = Path("test_kontrol.spec")
    with open(spec_file, "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    # Ejecutar PyInstaller
    cmd = ["pyinstaller", "--clean", "--noconfirm", str(spec_file)]
    
    try:
        result = subprocess.run(cmd, check=True, text=True, 
                              capture_output=True, timeout=300)
        print("✅ PyInstaller ejecutado exitosamente")
        print(f"Salida: {result.stdout[:500]}...")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en PyInstaller:")
        print(f"Error: {e.stderr[:500]}...")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Timeout en PyInstaller")
        return False

if __name__ == "__main__":
    print("🚀 Test de construcción simplificado")
    success = test_pyinstaller()
    print(f"Resultado: {'ÉXITO' if success else 'FALLÓ'}")
