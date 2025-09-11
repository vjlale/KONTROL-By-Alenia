#!/usr/bin/env python3
"""
Script de validación pre-distribución para ALENIA GESTION-KONTROL+ v2.3
Verifica que todo esté listo para distribución comercial
"""

import os
import sys
import json
import subprocess
from pathlib import Path
import hashlib
from PIL import Image
import ast

class DistributionValidator:
    def __init__(self):
        self.root_dir = Path.cwd()
        self.errors = []
        self.warnings = []
        self.checks_passed = 0
        self.total_checks = 0
        
    def log_error(self, message):
        """Registrar error crítico"""
        self.errors.append(f"❌ ERROR: {message}")
        print(f"❌ ERROR: {message} - validate_distribution.py:27")
        
    def log_warning(self, message):
        """Registrar advertencia"""
        self.warnings.append(f"⚠️  WARNING: {message}")
        print(f"⚠️  WARNING: {message} - validate_distribution.py:32")
        
    def log_success(self, message):
        """Registrar éxito"""
        print(f"✅ {message} - validate_distribution.py:36")
        self.checks_passed += 1
        
    def check_required_files(self):
        """Verificar archivos requeridos para distribución"""
        print("🔍 Verificando archivos requeridos... - validate_distribution.py:41")
        self.total_checks += 1
        
        required_files = {
            # Código fuente
            "main.py": "Archivo principal de la aplicación",
            "auth.py": "Sistema de autenticación", 
            "session_manager.py": "Gestión de sesiones",
            
            # Assets visuales
            "7.png": "Logo principal",
            "LOGO APP.png": "Logo alternativo",
            
            # Documentación
            "README.md": "Documentación principal",
            "MANUAL_DISTRIBUCION.md": "Manual de distribución",
            "modelo_productos.csv": "Plantilla CSV",
            
            # Scripts de construcción
            "build_distribution.py": "Script de construcción",
            "optimize_main.py": "Optimizador de código",
        }
        
        missing_files = []
        for file_path, description in required_files.items():
            if not (self.root_dir / file_path).exists():
                missing_files.append(f"{file_path} ({description})")
                
        if missing_files:
            self.log_error(f"Archivos faltantes: {', '.join(missing_files)}")
            return False
        else:
            self.log_success("Todos los archivos requeridos están presentes")
            return True
            
    def check_code_syntax(self):
        """Verificar sintaxis del código Python"""
        print("🐍 Verificando sintaxis del código... - validate_distribution.py:78")
        self.total_checks += 1
        
        python_files = ["main.py", "auth.py", "session_manager.py"]
        syntax_errors = []
        
        for file_name in python_files:
            file_path = self.root_dir / file_name
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    ast.parse(content)
                except SyntaxError as e:
                    syntax_errors.append(f"{file_name}: {e}")
                    
        if syntax_errors:
            self.log_error(f"Errores de sintaxis: {'; '.join(syntax_errors)}")
            return False
        else:
            self.log_success("Sintaxis de código verificada")
            return True
            
    def check_dependencies(self):
        """Verificar dependencias de Python"""
        print("📦 Verificando dependencias... - validate_distribution.py:103")
        self.total_checks += 1
        
        required_packages = [
            ("PIL", "Pillow"),
            ("tkinter", "tkinter (incluido en Python)"),
            ("json", "json (incluido en Python)"),
            ("datetime", "datetime (incluido en Python)")
        ]
        
        missing_deps = []
        for module_name, package_name in required_packages:
            try:
                __import__(module_name)
            except ImportError:
                missing_deps.append(package_name)
                
        if missing_deps:
            self.log_error(f"Dependencias faltantes: {', '.join(missing_deps)}")
            return False
        else:
            self.log_success("Todas las dependencias están disponibles")
            return True
            
    def check_images(self):
        """Verificar integridad de imágenes"""
        print("🖼️  Verificando integridad de imágenes... - validate_distribution.py:129")
        self.total_checks += 1
        
        # Imágenes en directorio raíz
        image_files = [
            ("7.png", self.root_dir / "7.png"),
            ("LOGO APP.png", self.root_dir / "LOGO APP.png"), 
            ("ALENRESULTADOS.png", self.root_dir / "ALENRESULTADOS.png")
        ]
        
        # Imagen en carpeta screenshot
        logonombre_path = self.root_dir / "screenshot" / "LOGONOMBRE.png"
        if logonombre_path.exists():
            image_files.append(("LOGONOMBRE.png", logonombre_path))
            
        corrupted_images = []
        for image_name, image_path in image_files:
            if image_path.exists():
                try:
                    with Image.open(image_path) as img:
                        img.verify()  # Verificar integridad
                        # Reabrir para verificar tamaño
                        with Image.open(image_path) as img2:
                            width, height = img2.size
                            if width < 10 or height < 10:
                                corrupted_images.append(f"{image_name} (tamaño inválido: {width}x{height})")
                except Exception as e:
                    corrupted_images.append(f"{image_name} ({str(e)})")
            else:
                self.log_warning(f"Imagen opcional no encontrada: {image_name}")
                
        if corrupted_images:
            self.log_error(f"Imágenes corruptas: {', '.join(corrupted_images)}")
            return False
        else:
            self.log_success("Integridad de imágenes verificada")
            return True
            
    def check_pyinstaller(self):
        """Verificar instalación de PyInstaller"""
        print("🔨 Verificando PyInstaller... - validate_distribution.py:169")
        self.total_checks += 1
        
        try:
            result = subprocess.run(["pyinstaller", "--version"], 
                                  capture_output=True, text=True, check=True)
            version = result.stdout.strip()
            self.log_success(f"PyInstaller {version} instalado")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.log_error("PyInstaller no está instalado o no funciona correctamente")
            return False
            
    def check_documentation(self):
        """Verificar completitud de documentación"""
        print("📚 Verificando documentación... - validate_distribution.py:184")
        self.total_checks += 1
        
        doc_checks = []
        
        # Verificar README.md
        readme_path = self.root_dir / "README.md"
        if readme_path.exists():
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
            
            required_sections = [
                "Descripción", "Características", "Instalación", 
                "Requisitos", "Contacto"
            ]
            
            missing_sections = []
            for section in required_sections:
                if section.lower() not in readme_content.lower():
                    missing_sections.append(section)
                    
            if missing_sections:
                doc_checks.append(f"README.md: secciones faltantes ({', '.join(missing_sections)})")
        else:
            doc_checks.append("README.md no encontrado")
            
        # Verificar archivos HTML
        html_files = ["GUIA_USUARIO_COMPLETA.html", "GUIA_VISUAL_USUARIO.html"]
        for html_file in html_files:
            html_path = self.root_dir / html_file
            if not html_path.exists():
                doc_checks.append(f"{html_file} no encontrado")
                
        if doc_checks:
            self.log_warning(f"Problemas en documentación: {'; '.join(doc_checks)}")
            return False
        else:
            self.log_success("Documentación completa y válida")
            return True
            
    def check_csv_template(self):
        """Verificar plantilla CSV"""
        print("📊 Verificando plantilla CSV... - validate_distribution.py:226")
        self.total_checks += 1
        
        csv_path = self.root_dir / "modelo_productos.csv"
        if not csv_path.exists():
            self.log_error("modelo_productos.csv no encontrado")
            return False
            
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                
            # Verificar que tenga las columnas esperadas (flexibilidad en nombres)
            expected_mappings = {
                "marca": ["marca", "marca/proveedor", "proveedor"],
                "descripcion": ["descripcion", "descripción", "producto"],
                "color": ["color", "color/sabor", "sabor"],
                "talle": ["talle", "talle/tamaño", "tamaño", "size"],
                "cantidad": ["cantidad", "stock", "qty"],
                "precio_costo": ["precio_costo", "costo", "precio", "cost"]
            }
            
            columns = [col.strip().lower() for col in first_line.split(',')]
            
            missing_columns = []
            for expected_col, possible_names in expected_mappings.items():
                found = any(possible_name in columns for possible_name in possible_names)
                if not found:
                    missing_columns.append(expected_col)
                    
            if missing_columns:
                self.log_error(f"Columnas faltantes en CSV: {', '.join(missing_columns)}")
                return False
            else:
                self.log_success("Plantilla CSV válida")
                return True
                
        except Exception as e:
            self.log_error(f"Error leyendo CSV: {e}")
            return False
            
    def check_version_consistency(self):
        """Verificar consistencia de versiones"""
        print("🏷️  Verificando consistencia de versiones... - validate_distribution.py:269")
        self.total_checks += 1
        
        version_files = {
            "README.md": r"v(\d+\.\d+)",
            "RELEASE_NOTES_v2.3.md": r"v(\d+\.\d+)",
            "build_distribution.py": r'VERSION = "(\d+\.\d+\.\d+)"'
        }
        
        versions_found = {}
        for file_name, pattern in version_files.items():
            file_path = self.root_dir / file_name
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    import re
                    match = re.search(pattern, content)
                    if match:
                        versions_found[file_name] = match.group(1)
                except Exception as e:
                    self.log_warning(f"Error leyendo versión de {file_name}: {e}")
                    
        # Verificar consistencia
        if len(set(versions_found.values())) > 1:
            self.log_warning(f"Versiones inconsistentes: {versions_found}")
            return False
        else:
            version = list(versions_found.values())[0] if versions_found else "desconocida"
            self.log_success(f"Versión consistente: {version}")
            return True
            
    def check_disk_space(self):
        """Verificar espacio en disco suficiente"""
        print("💾 Verificando espacio en disco... - validate_distribution.py:304")
        self.total_checks += 1
        
        try:
            # Obtener espacio libre (Windows)
            if os.name == 'nt':
                import shutil
                free_bytes = shutil.disk_usage(self.root_dir).free
                free_gb = free_bytes / (1024**3)
                
                if free_gb < 2:  # Mínimo 2GB para el proceso de build
                    self.log_error(f"Espacio insuficiente: {free_gb:.1f}GB (mínimo: 2GB)")
                    return False
                else:
                    self.log_success(f"Espacio en disco suficiente: {free_gb:.1f}GB")
                    return True
            else:
                self.log_warning("Verificación de espacio no disponible en este sistema")
                return True
                
        except Exception as e:
            self.log_warning(f"Error verificando espacio en disco: {e}")
            return True
            
    def generate_pre_build_report(self):
        """Generar reporte pre-build"""
        print("📋 Generando reporte de validación... - validate_distribution.py:330")
        
        report_content = f"""# 📋 REPORTE DE VALIDACIÓN PRE-DISTRIBUCIÓN
## ALENIA GESTION-KONTROL+ v2.3

**Fecha:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Sistema:** {os.name} - {sys.platform}
**Python:** {sys.version.split()[0]}

## 📊 RESUMEN
- **Checks ejecutados:** {self.total_checks}
- **Checks exitosos:** {self.checks_passed}
- **Errores críticos:** {len(self.errors)}
- **Advertencias:** {len(self.warnings)}
- **Estado:** {'✅ LISTO PARA DISTRIBUCIÓN' if len(self.errors) == 0 else '❌ REQUIERE CORRECCIONES'}

## ❌ ERRORES CRÍTICOS
"""
        
        if self.errors:
            for error in self.errors:
                report_content += f"\n{error}"
        else:
            report_content += "\n✅ Sin errores críticos"
            
        report_content += "\n\n## ⚠️ ADVERTENCIAS\n"
        
        if self.warnings:
            for warning in self.warnings:
                report_content += f"\n{warning}"
        else:
            report_content += "\n✅ Sin advertencias"
            
        report_content += f"""

## 🎯 PRÓXIMOS PASOS

{'✅ **LISTO PARA DISTRIBUCIÓN**' if len(self.errors) == 0 else '❌ **CORREGIR ERRORES ANTES DE CONTINUAR**'}

1. {'Ejecutar build_distribution.py' if len(self.errors) == 0 else 'Corregir errores listados arriba'}
2. {'Testear ejecutable generado' if len(self.errors) == 0 else 'Re-ejecutar validate_distribution.py'}
3. {'Distribuir paquete final' if len(self.errors) == 0 else 'Continuar con build cuando esté todo OK'}

## 📞 SOPORTE
Para consultas sobre este reporte: alenia.online@gmail.com

---
© 2025 ALENIA - Reporte generado automáticamente
"""
        
        # Guardar reporte
        report_path = self.root_dir / "VALIDATION_REPORT.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
            
        print(f"📄 Reporte guardado en: {report_path} - validate_distribution.py:385")
        return report_path
        
    def run_validation(self):
        """Ejecutar validación completa"""
        print("🚀 INICIANDO VALIDACIÓN PREDISTRIBUCIÓN - validate_distribution.py:390")
        print("= - validate_distribution.py:391" * 60)
        
        # Ejecutar todos los checks
        validation_methods = [
            self.check_required_files,
            self.check_code_syntax,
            self.check_dependencies,
            self.check_images,
            self.check_pyinstaller,
            self.check_documentation,
            self.check_csv_template,
            self.check_version_consistency,
            self.check_disk_space
        ]
        
        for method in validation_methods:
            try:
                method()
            except Exception as e:
                self.log_error(f"Error en {method.__name__}: {e}")
            print()  # Línea en blanco entre checks
            
        # Generar reporte
        report_path = self.generate_pre_build_report()
        
        # Resumen final
        print("= - validate_distribution.py:417" * 60)
        if len(self.errors) == 0:
            print("🎉 VALIDACIÓN EXITOSA  LISTO PARA DISTRIBUCIÓN - validate_distribution.py:419")
            print(f"✅ {self.checks_passed}/{self.total_checks} checks pasaron - validate_distribution.py:420")
            if self.warnings:
                print(f"⚠️  {len(self.warnings)} advertencias (no críticas) - validate_distribution.py:422")
            print("\n🚀 Próximo paso: Ejecutar build_distribution.py - validate_distribution.py:423")
        else:
            print("❌ VALIDACIÓN FALLÓ  REQUIERE CORRECCIONES - validate_distribution.py:425")
            print(f"❌ {len(self.errors)} errores críticos encontrados - validate_distribution.py:426")
            print(f"⚠️  {len(self.warnings)} advertencias - validate_distribution.py:427")
            print("\n🔧 Corregir errores antes de continuar con la distribución - validate_distribution.py:428")
            
        print(f"📋 Reporte detallado: {report_path} - validate_distribution.py:430")
        
        return len(self.errors) == 0

def main():
    validator = DistributionValidator()
    success = validator.run_validation()
    
    input(f"\n{'✅ VALIDACIÓN EXITOSA' if success else '❌ VALIDACIÓN FALLÓ'} - Presiona Enter para continuar...")
    return success

if __name__ == "__main__":
    main()