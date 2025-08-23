#!/usr/bin/env python3
"""
Script de construcción para KONTROL+ v3.0
Genera ejecutable standalone con PyInstaller
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    print("🚀 Iniciando construcción de KONTROL+ v3.0...")
    
    # Verificar que PyInstaller esté instalado
    try:
        import PyInstaller
        print(f"✅ PyInstaller {PyInstaller.__version__} encontrado")
    except ImportError:
        print("❌ PyInstaller no encontrado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller instalado")
    
    # Verificar archivos necesarios
    required_files = [
        "main.py",
        "auth.py", 
        "7.png",
        "screenshot/ALENRESULTADOS.png",
        "screenshot/LOGO_APP.png",
        "screenshot/LOGONOMBRE.png",
        "screenshot/iconos/icoNUEVAVENTA.png",
        "screenshot/iconos/icoVENTAS DEL DÍA.png",
        "screenshot/iconos/icoMenú.png"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Archivos faltantes: {missing_files}")
        return False
    
    print("✅ Todos los archivos necesarios encontrados")
    
    # Limpiar build anterior
    build_dirs = ["build", "dist", "__pycache__"]
    for dir_name in build_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🗑️  Limpiado directorio {dir_name}")
    
    # Comando PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",                    # Ejecutable único
        "--windowed",                   # Sin consola
        "--name=KONTROL+",              # Nombre del ejecutable
        "--icon=7.png",                 # Icono del ejecutable
        "--add-data=7.png;.",           # Incluir logo principal
        "--add-data=screenshot/ALENRESULTADOS.png;.", # Incluir logo panel IA
        "--add-data=screenshot/LOGO_APP.png;.",    # Incluir logo app
        "--add-data=screenshot/LOGONOMBRE.png;.",  # Incluir logo pequeño (si se usa en otras pantallas)
        "--add-data=screenshot/iconos/icoNUEVAVENTA.png;.", # Icono nueva venta
        "--add-data=screenshot/iconos/icoVENTAS DEL DÍA.png;.", # Icono ventas del día
        "--add-data=screenshot/iconos/icoMenú.png;.",       # Icono menú
        "--add-data=auth.py;.",         # Incluir módulo auth
        "--distpath=dist",              # Directorio de salida
        "--workpath=build",             # Directorio temporal
        "--specpath=.",                 # Ubicación del .spec
        "--clean",                      # Limpiar cache
        "main.py"                       # Archivo principal
    ]
    
    print(f"🔨 Ejecutando: {' '.join(cmd)}")
    
    try:
        # Ejecutar PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Compilación exitosa!")
        
        # Verificar que el ejecutable se creó
        exe_path = Path("dist/KONTROL+.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"🎉 Ejecutable creado: {exe_path}")
            print(f"📦 Tamaño: {size_mb:.1f} MB")
            
            # Crear directorio de distribución
            dist_dir = Path("KONTROL+_v3.0_Release")
            if dist_dir.exists():
                shutil.rmtree(dist_dir)
            dist_dir.mkdir()
            
            # Copiar ejecutable y archivos necesarios
            shutil.copy2(exe_path, dist_dir / "KONTROL+.exe")
            
            # Crear README de distribución
            readme_content = """# KONTROL+ v3.0 - Software de Gestión
By Alen.iA

## Instalación
1. Ejecutar KONTROL+.exe
2. En el primer inicio, crear usuario administrador
3. ¡Listo para usar!

## Características v3.0
- Gestión completa de inventario
- Sistema de ventas integrado
- Reportes y análisis inteligente
- Control de usuarios y permisos
- Interfaz moderna y profesional

## Soporte
Para soporte técnico contactar a Alen.iA

---
KONTROL+ - RESULTADOS CON INTELIGENCIA
"""
            
            with open(dist_dir / "README.txt", "w", encoding="utf-8") as f:
                f.write(readme_content)
            
            print(f"📁 Paquete de distribución creado: {dist_dir}")
            print("✅ ¡Construcción completada exitosamente!")
            return True
            
        else:
            print("❌ El ejecutable no se creó correctamente")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en la compilación:")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False

if __name__ == "__main__":
    success = main()
    input("\nPresiona Enter para continuar..." if success else "\nPresiona Enter para salir...")
