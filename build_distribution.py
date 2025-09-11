#!/usr/bin/env python3
"""
Script de construcción y distribución para ALENIA GESTION-KONTROL+ v2.3
Genera paquete completo optimizado para distribución comercial
"""

import os
import sys
import subprocess
import shutil
import json
import zipfile
from pathlib import Path
from datetime import datetime

VERSION = "2.3.0"
APP_NAME = "ALENIA-GESTION-KONTROL+"
DIST_NAME = f"{APP_NAME}_v{VERSION}_Complete"

class DistributionBuilder:
    def __init__(self):
        self.root_dir = Path.cwd()
        self.build_dir = self.root_dir / "build_dist"
        self.dist_dir = self.root_dir / "dist_final"
        self.temp_dir = self.root_dir / "temp_build"
        
    def setup_directories(self):
        """Crear directorios de trabajo limpios"""
        print("🧹 Limpiando directorios previos... - build_distribution.py:29")
        
        # Limpiar directorios existentes
        for dir_path in [self.build_dir, self.dist_dir, self.temp_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
            dir_path.mkdir(exist_ok=True)
            
        print("[OK] Directorios de trabajo preparados - build_distribution.py:37")
        
    def verify_dependencies(self):
        """Verificar e instalar dependencias necesarias"""
        print("[CHECK] Verificando dependencias... - build_distribution.py:41")
        
        required_packages = [
            "pyinstaller>=5.0",
            "pillow>=10.0.0",
            "tkcalendar>=1.6.1"
        ]
        
        for package in required_packages:
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                print(f"[ERROR] Error instalando {package} - build_distribution.py:55")
                return False
                
        print("[OK] Dependencias verificadas - build_distribution.py:58")
        return True
        
    def collect_assets(self):
        """Recopilar todos los assets necesarios"""
        print("[ASSETS] Recopilando assets... - build_distribution.py:63")
        
        assets = {
            # Logos principales - CRÍTICOS PARA EL FUNCIONAMIENTO (en raíz)
            "7.png": ".",
            "LOGO APP.png": ".",
            "ALENRESULTADOS.png": ".",
            "screenshot/7.png": ".",
            "screenshot/LOGO_APP.png": ".",
            "screenshot/ALENRESULTADOS.png": ".",
            "screenshot/LOGONOMBRE.png": ".",
            
            # Iconos de botones - CRÍTICOS PARA PANTALLA PRINCIPAL (en raíz)
            "screenshot/iconos/icoNUEVAVENTA.png": ".",
            "screenshot/iconos/icoVENTAS DEL DÍA.png": ".", 
            "screenshot/iconos/icoMenú.png": ".",
            "screenshot/iconos/7.png": ".",
            
            # Screenshots para documentación
            "screenshot/Pantalla principal.png": "screenshot",
            "screenshot/PANTALLA MENU.png": "screenshot", 
            "screenshot/PANTALLA nueva venta.png": "screenshot",
            "screenshot/pantalla ventas del dia.png": "screenshot",
            "screenshot/pantalla IA.png": "screenshot",
            
            # Archivos de configuración
            "modelo_productos.csv": ".",
            "auth.py": ".",
            "session_manager.py": "."
        }
        
        missing_assets = []
        existing_assets = {}
        
        for asset, dest in assets.items():
            asset_path = self.root_dir / asset
            if asset_path.exists():
                existing_assets[asset] = dest
                print(f"[ASSET] ✅ Encontrado: {asset} -> {dest} - build_distribution.py")
            else:
                missing_assets.append(asset)
                
        if missing_assets:
            print(f"[WARNING] Assets faltantes (se omitirán): {missing_assets} - build_distribution.py:101")
            
        print(f"[OK] {len(existing_assets)} assets recopilados - build_distribution.py:103")
        return existing_assets
        
    def build_executable(self, assets):
        """Construir ejecutable optimizado con PyInstaller"""
        print("🔨 Construyendo ejecutable optimizado... - build_distribution.py:108")
        
        # Limpiar directorios previos de PyInstaller
        build_dirs = ["build", "dist", "__pycache__"]
        for dir_name in build_dirs:
            dir_path = self.root_dir / dir_name
            if dir_path.exists():
                try:
                    shutil.rmtree(dir_path)
                    print(f"[CLEAN] Directorio {dir_name} limpiado - build_distribution.py")
                except Exception as e:
                    print(f"[WARNING] No se pudo limpiar {dir_name}: {e} - build_distribution.py")
        
        # Verificar si existe el ícono .ico (preferido) o .png como fallback
        icon_path = None
        icon_candidates = [
            self.root_dir / "screenshot" / "generated-338b7370ef8ace6aaeedd338bea0ffdf433732a4678bf58bde872bec7f175da6.ico",
            self.root_dir / "screenshot" / "7.png",
            self.root_dir / "7.png"
        ]
        
        for candidate in icon_candidates:
            if candidate.exists():
                icon_path = candidate
                break
        
        icon_param = []
        if icon_path:
            icon_param = ["--icon", str(icon_path)]
            print(f"[ICON] ✅ Usando ícono: {icon_path} - build_distribution.py")
        else:
            print("[WARNING] ❌ Ningún ícono encontrado, usando ícono por defecto - build_distribution.py")
        
        # Crear comando PyInstaller directo sin spec file
        cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            "--name=KONTROL-PLUS",
            "--clean",
            "--noconfirm",
            "--optimize=2",
            "--strip"
        ]
        
        # Agregar ícono si está disponible
        cmd.extend(icon_param)
        
        # Agregar assets como data files con rutas corregidas
        for asset, dest in assets.items():
            asset_path = self.root_dir / asset
            if asset_path.exists():
                # Usar punto y coma en Windows para separar origen y destino
                cmd.extend(["--add-data", f"{asset_path};{dest}"])
                print(f"[DATA] ✅ Agregando: {asset} -> {dest} - build_distribution.py")
        
        # Agregar módulos ocultos necesarios
        hidden_imports = [
            "tkinter", "tkinter.ttk", "PIL", "PIL.Image", "PIL.ImageTk",
            "tkcalendar", "json", "csv", "datetime", "uuid", "os", "sys"
        ]
        
        for module in hidden_imports:
            cmd.extend(["--hidden-import", module])
        
        # Excluir módulos innecesarios para reducir tamaño
        excludes = [
            "matplotlib", "numpy", "pandas", "scipy", 
            "PyQt5", "PyQt6", "PySide2", "PySide6", "tkinter.test"
        ]
        
        for module in excludes:
            cmd.extend(["--exclude-module", module])
        
        # Agregar archivo principal
        cmd.append("main.py")
        
        try:
            print(f"[BUILD] 🚀 Ejecutando PyInstaller con {len(assets)} assets... - build_distribution.py")
            
            # Ejecutar con timeout para evitar bloqueos
            result = subprocess.run(
                cmd, 
                cwd=self.root_dir, 
                check=True,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True,
                timeout=600  # 10 minutos máximo
            )
            
            print("[OK] ✅ Ejecutable construido exitosamente - build_distribution.py")
            
            # Verificar que el ejecutable se creó
            exe_path = self.root_dir / "dist" / "KONTROL-PLUS.exe"
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"[OK] 📱 Ejecutable generado: {size_mb:.1f}MB - build_distribution.py")
                print(f"[OK] 🎯 Ícono aplicado: {icon_path.name if icon_path else 'Por defecto'} - build_distribution.py")
                return True
            else:
                print("[ERROR] ❌ Ejecutable no encontrado después del build - build_distribution.py")
                return False
                
        except subprocess.TimeoutExpired:
            print("[ERROR] ⏰ Build timeout - El proceso tomó más de 10 minutos - build_distribution.py")
            return False
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] ❌ Error construyendo ejecutable: - build_distribution.py")
            print(f"Return code: {e.returncode} - build_distribution.py")
            if e.stdout:
                print(f"STDOUT (últimas líneas): - build_distribution.py")
                stdout_lines = e.stdout.strip().split('\n')
                for line in stdout_lines[-10:]:  # Solo últimas 10 líneas
                    print(f"  {line} - build_distribution.py")
            if e.stderr:
                print(f"STDERR (últimas líneas): - build_distribution.py")
                stderr_lines = e.stderr.strip().split('\n')
                for line in stderr_lines[-10:]:  # Solo últimas 10 líneas
                    print(f"  {line} - build_distribution.py")
            return False
        except Exception as e:
            print(f"[ERROR] ❌ Error inesperado: {e} - build_distribution.py")
            return False
            
    def create_installer_package(self):
        """Crear paquete de instalación completo"""
        print("[PACKAGE] Creando paquete de instalación... - build_distribution.py:228")
        
        # Crear estructura del paquete
        package_dir = self.dist_dir / DIST_NAME
        package_dir.mkdir(exist_ok=True)
        
        # Copiar ejecutable
        exe_source = self.root_dir / "dist" / "KONTROL-PLUS.exe"
        exe_dest = package_dir / "KONTROL-PLUS.exe"
        
        if exe_source.exists():
            shutil.copy2(exe_source, exe_dest)
            size_mb = exe_dest.stat().st_size / (1024 * 1024)
            print(f"[OK] Ejecutable copiado: {size_mb:.1f}MB - build_distribution.py:241")
        else:
            print("[ERROR] Ejecutable no encontrado - build_distribution.py:243")
            return False
            
        # Crear documentación de instalación
        self.create_installation_docs(package_dir)
        
        # Copiar archivos auxiliares
        auxiliary_files = [
            "modelo_productos.csv",
            "README.md",
            "GUIA_USUARIO_COMPLETA.html",
            "GUIA_VISUAL_USUARIO.html"
        ]
        
        for file_name in auxiliary_files:
            source = self.root_dir / file_name
            if source.exists():
                shutil.copy2(source, package_dir / file_name)
                
        # Crear directorio de screenshots
        screenshot_dir = package_dir / "Screenshots"
        screenshot_dir.mkdir(exist_ok=True)
        
        screenshot_source = self.root_dir / "screenshot"
        if screenshot_source.exists():
            for screenshot in screenshot_source.glob("*.png"):
                shutil.copy2(screenshot, screenshot_dir / screenshot.name)
                
        print("[OK] Paquete de instalación creado - build_distribution.py:271")
        return True
        
    def create_installation_docs(self, package_dir):
        """Crear documentación de instalación profesional"""
        
        # Archivo LEEME.txt para instalación
        leeme_content = f"""
═══════════════════════════════════════════════════════════════
    [SOFTWARE] ALENIA GESTION-KONTROL+ v{VERSION}
    SOFTWARE PROFESIONAL DE GESTIÓN COMERCIAL
═══════════════════════════════════════════════════════════════

[INSTALACION] INSTALACIÓN RÁPIDA (2 MINUTOS):

1. EJECUTAR
   → Doble clic en "KONTROL-PLUS.exe"
   
2. PRIMERA VEZ
   → Crear usuario administrador
   → Configurar datos básicos
   
3. ¡LISTO!
   → Ya podés empezar a gestionar tu negocio

─────────────────────────────────────────────────────────────────

[NOTAS] NOTAS IMPORTANTES:

[ANTIVIRUS] ANTIVIRUS
   Si Windows Defender o tu antivirus muestra alerta:
   → Es un falso positivo (común con apps empaquetadas)
   → Clic en "Más información" → "Ejecutar de todas formas"
   → Agregar a excepciones para evitar futuras alertas

[REQUISITOS] REQUISITOS DEL SISTEMA
   → Windows 10 o 11 (64-bit)
   → 4GB RAM mínimo (8GB recomendado)
   → 100MB espacio en disco
   → Resolución mínima: 1280x720

[SOPORTE] SOPORTE TÉCNICO
   → WhatsApp: +54 351 6875178
   → Email: alenia.online@gmail.com
   → Respuesta garantizada en 24hs

─────────────────────────────────────────────────────────────────

[CARACTERISTICAS] CARACTERÍSTICAS PRINCIPALES:

[OK] Gestión completa de inventario con alertas automáticas
[OK] Sistema de ventas profesional con múltiples formas de pago
[OK] Ofertas inteligentes (3x2, 2x1, descuentos automáticos)
[OK] Reportes avanzados con exportación a Excel/CSV
[OK] Inteligencia Artificial para optimizar tu negocio
[OK] Carga masiva de productos desde archivos CSV
[OK] Control de usuarios y permisos de acceso
[OK] Cierre de caja automático con balances detallados

[GRATIS] 100% GRATUITO - Sin licencias ni mensualidades

─────────────────────────────────────────────────────────────────

[DOCUMENTACION] DOCUMENTACIÓN INCLUIDA:

[DOC] README.md - Información completa del software
[DOC] GUIA_USUARIO_COMPLETA.html - Manual paso a paso
[DOC] GUIA_VISUAL_USUARIO.html - Tutorial con capturas
[DOC] modelo_productos.csv - Ejemplo para carga masiva

─────────────────────────────────────────────────────────────────

[GRACIAS] ¡Gracias por elegir ALENIA GESTION-KONTROL+!

© 2025 ALENIA - Desarrollado con ❤️ para emprendedores argentinos
"""
        
        with open(package_dir / "LEEME - INSTALACIÓN.txt", "w", encoding="utf-8") as f:
            f.write(leeme_content)
            
        # Crear script de instalación opcional
        install_script = f"""@echo off
title ALENIA GESTION-KONTROL+ v{VERSION} - Instalador
color 0A

echo.
echo ═══════════════════════════════════════════════════════════════
echo     [SOFTWARE] ALENIA GESTION-KONTROL+ v{VERSION}
echo     INSTALADOR INTELIGENTE
echo ═══════════════════════════════════════════════════════════════
echo.

echo [CHECK] Verificando sistema...
echo.

REM Verificar Windows 64-bit
wmic os get osarchitecture | find "64-bit" >nul
if errorlevel 1 (
    echo [ERROR] ERROR: Este software requiere Windows 64-bit
    pause
    exit /b 1
)

echo [OK] Sistema compatible detectado
echo.

echo [SETUP] Creando acceso directo en Escritorio...
set "desktop=%USERPROFILE%\\Desktop"
set "target=%~dp0KONTROL-PLUS.exe"
set "shortcut=%desktop%\\KONTROL+ Gestión.lnk"

powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%shortcut%'); $Shortcut.TargetPath = '%target%'; $shortcut.IconLocation = '%target%'; $Shortcut.Save()"

if exist "%shortcut%" (
    echo [OK] Acceso directo creado en Escritorio
) else (
    echo [WARNING] No se pudo crear acceso directo
)

echo.
echo [QUESTION] ¿Desea ejecutar KONTROL+ ahora? (S/N)
set /p choice=

if /i "%choice%"=="S" (
    echo.
    echo [START] Iniciando KONTROL+...
    start "" "%target%"
) else (
    echo.
    echo [INFO] Puede iniciar KONTROL+ desde:
    echo    → Doble clic en KONTROL-PLUS.exe
    echo    → Acceso directo en Escritorio
)

echo.
echo [OK] Instalación completada exitosamente
echo.
echo [SOPORTE] Soporte técnico: +54 351 6875178
echo [EMAIL] Email: alenia.online@gmail.com
echo.
pause
"""
        
        with open(package_dir / "INSTALAR.bat", "w", encoding="utf-8") as f:
            f.write(install_script)
            
    def create_distribution_zip(self):
        """Crear archivo ZIP final para distribución"""
        print("[ZIP] Creando archivo de distribución... - build_distribution.py:419")
        
        package_dir = self.dist_dir / DIST_NAME
        zip_path = self.dist_dir / f"{DIST_NAME}.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
            for file_path in package_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(package_dir)
                    zipf.write(file_path, arcname)
                    
        zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
        print(f"[OK] Archivo ZIP creado: {zip_size_mb:.1f}MB - build_distribution.py:431")
        
        return zip_path
        
    def generate_checksums(self, zip_path):
        """Generar checksums para verificación de integridad"""
        import hashlib
        
        print("[SECURITY] Generando checksums de seguridad... - build_distribution.py:439")
        
        # Calcular MD5 y SHA256
        with open(zip_path, 'rb') as f:
            content = f.read()
            md5_hash = hashlib.md5(content).hexdigest()
            sha256_hash = hashlib.sha256(content).hexdigest()
            
        # Crear archivo de checksums
        checksum_content = f"""ALENIA GESTION-KONTROL+ v{VERSION} - CHECKSUMS

Archivo: {zip_path.name}
Tamaño: {len(content):,} bytes ({len(content)/(1024*1024):.1f} MB)
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

MD5:    {md5_hash}
SHA256: {sha256_hash}

Verificación:
- Use estos hashes para verificar la integridad del archivo
- Cualquier diferencia indica que el archivo fue modificado
- Para verificar en Windows PowerShell:
  Get-FileHash "{zip_path.name}" -Algorithm SHA256
"""
        
        checksum_file = zip_path.parent / f"{zip_path.stem}_CHECKSUMS.txt"
        with open(checksum_file, 'w', encoding='utf-8') as f:
            f.write(checksum_content)
            
        print("[OK] Checksums generados - build_distribution.py:468")
        return checksum_file
        
    def create_release_notes(self):
        """Crear notas de release actualizadas"""
        print("[RELEASE] Generando notas de release... - build_distribution.py:473")
        
        release_content = f"""# [RELEASE] ALENIA GESTION-KONTROL+ v{VERSION} - RELEASE FINAL

## [FECHA] FECHA DE RELEASE: {datetime.now().strftime('%d de %B de %Y')}

### [DISTRIBUCION] DISTRIBUCIÓN OPTIMIZADA

Esta versión ha sido especialmente optimizada para distribución comercial:

[OK] **Ejecutable optimizado** - Tamaño reducido y mayor estabilidad
[OK] **Instalación automática** - Script de instalación incluido
[OK] **Documentación completa** - Manuales y guías actualizados
[OK] **Checksums de seguridad** - Verificación de integridad incluida
[OK] **Compatibilidad mejorada** - Testing extensivo en Windows 10/11

### [CONTENIDO] CONTENIDO DEL PAQUETE

```
{DIST_NAME}/
├── KONTROL-PLUS.exe           # Aplicación principal
├── INSTALAR.bat               # Instalador automático
├── LEEME - INSTALACIÓN.txt    # Instrucciones rápidas
├── README.md                  # Documentación completa
├── GUIA_USUARIO_COMPLETA.html # Manual interactivo
├── GUIA_VISUAL_USUARIO.html   # Tutorial visual
├── modelo_productos.csv       # Plantilla para importar
└── Screenshots/               # Capturas de pantalla
    ├── Pantalla principal.png
    ├── PANTALLA MENU.png
    ├── PANTALLA nueva venta.png
    ├── pantalla ventas del dia.png
    └── pantalla IA.png
```

### [INSTRUCCIONES] INSTRUCCIONES DE DISTRIBUCIÓN

1. **Descarga**: Descargar {DIST_NAME}.zip
2. **Extracción**: Extraer en ubicación deseada
3. **Instalación**: Ejecutar INSTALAR.bat (opcional)
4. **Uso**: Doble clic en KONTROL-PLUS.exe

### [CARACTERISTICAS] CARACTERÍSTICAS COMERCIALES

- [GRATIS] **100% Gratuito** - Sin licencias ni mensualidades
- [SECURITY] **Datos seguros** - Almacenamiento local
- [OFFLINE] **Sin internet** - Funciona completamente offline
- [EASY] **Fácil instalación** - 2 minutos desde descarga hasta uso
- [SUPPORT] **Soporte incluido** - WhatsApp y email

### [VALOR] VALOR COMERCIAL

Comparado con competencia:
- Ahorro mensual: $123.000 ARS
- Ahorro anual: $1.476.000 ARS
- ROI inmediato: 100%

### [CONTACTO] SOPORTE Y CONTACTO

- **WhatsApp**: +54 351 6875178
- **Email**: alenia.online@gmail.com
- **GitHub**: github.com/vjlale/KONTROL-By-Alenia

---

© 2025 ALENIA - Desarrollado para emprendedores argentinos [ARGENTINA]
"""
        
        release_file = self.dist_dir / f"RELEASE_NOTES_v{VERSION}_FINAL.md"
        with open(release_file, 'w', encoding='utf-8') as f:
            f.write(release_content)
            
        print("[OK] Notas de release generadas - build_distribution.py:545")
        return release_file
        
    def run_build(self):
        """Ejecutar proceso completo de construcción"""
        print(f"[BUILD] Iniciando construcción de {APP_NAME} v{VERSION} - build_distribution.py:550")
        print("= - build_distribution.py:551" * 60)
        
        try:
            # Fase 1: Preparación
            self.setup_directories()
            if not self.verify_dependencies():
                return False
                
            # Fase 2: Recopilación
            assets = self.collect_assets()
            if not assets:
                print("[ERROR] No se encontraron assets necesarios - build_distribution.py:562")
                return False
                
            # Fase 3: Construcción
            if not self.build_executable(assets):
                return False
                
            # Fase 4: Empaquetado
            if not self.create_installer_package():
                return False
                
            # Fase 5: Distribución
            zip_path = self.create_distribution_zip()
            checksum_file = self.generate_checksums(zip_path)
            release_file = self.create_release_notes()
            
            # Resumen final
            print("\n - build_distribution.py:579" + "=" * 60)
            print("[SUCCESS] CONSTRUCCIÓN COMPLETADA EXITOSAMENTE - build_distribution.py:580")
            print("= - build_distribution.py:581" * 60)
            print(f"[PACKAGE] Paquete: {zip_path.name} - build_distribution.py:582")
            print(f"[SIZE] Tamaño: {zip_path.stat().st_size / (1024*1024):.1f}MB - build_distribution.py:583")
            print(f"[CHECKSUMS] Checksums: {checksum_file.name} - build_distribution.py:584")
            print(f"[RELEASE] Release Notes: {release_file.name} - build_distribution.py:585")
            print(f"[LOCATION] Ubicación: {self.dist_dir} - build_distribution.py:586")
            print("\n[READY] ¡Listo para distribución comercial! - build_distribution.py:587")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Error durante la construcción: {e} - build_distribution.py:592")
            return False
            
        finally:
            # Limpiar archivos temporales
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)

def main():
    builder = DistributionBuilder()
    success = builder.run_build()
    
    input(f"\n{'¡BUILD EXITOSO!' if success else 'BUILD FALLÓ'} - Presiona Enter para continuar...")
    return success

if __name__ == "__main__":
    main()