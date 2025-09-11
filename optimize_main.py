#!/usr/bin/env python3
"""
Script de optimización para main.py antes de la distribución
Completa métodos stub y optimiza el código para producción
"""

import re
import ast
from pathlib import Path

class MainOptimizer:
    def __init__(self, main_file_path="main.py"):
        self.main_file = Path(main_file_path)
        self.optimized_file = Path("main_optimized.py")
        
    def read_main_file(self):
        """Leer el archivo main.py"""
        with open(self.main_file, 'r', encoding='utf-8') as f:
            return f.read()
            
    def find_stub_methods(self, content):
        """Encontrar métodos stub que necesitan implementación"""
        # Patrones para encontrar métodos vacíos o con solo pass/...
        stub_patterns = [
            r'def\s+(\w+)\s*\([^)]*\):\s*\n\s*(pass|\.\.\.|\s*$)',
            r'def\s+(\w+)\s*\([^)]*\):\s*\n\s*"""[^"]*"""\s*\n\s*(pass|\.\.\.|\s*$)',
            r'def\s+(\w+)\s*\([^)]*\):\s*\n\s*#[^\n]*\n\s*(pass|\.\.\.|\s*$)'
        ]
        
        stub_methods = []
        for pattern in stub_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                method_name = match.group(1)
                if method_name not in [m[0] for m in stub_methods]:
                    stub_methods.append((method_name, match.start(), match.end()))
                    
        return stub_methods
        
    def complete_stub_methods(self, content):
        """Completar métodos stub con implementaciones básicas"""
        print("🔧 Completando métodos stub...")
        
        # Implementaciones para métodos comunes
        implementations = {
            "on_enter": """    def on_enter(self, e):
        \"\"\"Efecto hover al entrar\"\"\"
        try:
            e.widget.config(bg=color_hover)
        except:
            pass""",
            
            "on_leave": """    def on_leave(self, e):
        \"\"\"Efecto hover al salir\"\"\"
        try:
            e.widget.config(bg=color_normal)
        except:
            pass""",
            
            "_get_resample_filter": """    def _get_resample_filter(self):
        \"\"\"Obtener filtro de resampling compatible\"\"\"
        try:
            from PIL import Image
            return getattr(Image, 'LANCZOS', Image.ANTIALIAS)
        except:
            return 1""",
            
            "mostrar_inventario": """    def mostrar_inventario(self):
        \"\"\"Mostrar pantalla de inventario\"\"\"
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        self._chip_volver(self.mostrar_menu_principal)
        self._pantalla_inventario(self.canvas_bg)""",
            
            "limpiar_pantalla": """    def limpiar_pantalla(self):
        \"\"\"Limpiar todos los widgets de la pantalla\"\"\"
        if hasattr(self, 'pantalla_widgets'):
            for widget in self.pantalla_widgets:
                try:
                    widget.destroy()
                except:
                    pass
            self.pantalla_widgets.clear()
        else:
            self.pantalla_widgets = []""",
            
            "mostrar_menu_principal": """    def mostrar_menu_principal(self):
        \"\"\"Mostrar menú principal\"\"\"
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=True)
        self.crear_widgets()""",
            
            "mostrar_menu_secundario": """    def mostrar_menu_secundario(self):
        \"\"\"Mostrar menú secundario de gestión\"\"\"
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        self._chip_volver(self.mostrar_menu_principal)
        # Crear botones del menú secundario aquí
        pass""",
        }
        
        # Buscar métodos stub y reemplazarlos
        for method_name, start, end in self.find_stub_methods(content):
            if method_name in implementations:
                # Reemplazar implementación stub
                before = content[:start]
                after = content[end:]
                content = before + implementations[method_name] + after
                print(f"  ✅ Completado: {method_name}")
            else:
                print(f"  ⚠️  Sin implementación para: {method_name}")
                
        return content
        
    def add_missing_imports(self, content):
        """Agregar imports faltantes"""
        print("📦 Verificando imports...")
        
        required_imports = [
            "import tkinter as tk",
            "import tkinter.font as tkfont",
            "from tkinter import messagebox, filedialog",
            "import os",
            "import sys", 
            "import json",
            "import csv",
            "import datetime",
            "import uuid",
            "from pathlib import Path",
            "from PIL import Image, ImageTk"
        ]
        
        # Verificar qué imports faltan
        missing_imports = []
        for imp in required_imports:
            if imp not in content:
                missing_imports.append(imp)
                
        if missing_imports:
            # Agregar imports al inicio del archivo
            import_section = "\n".join(missing_imports) + "\n\n"
            
            # Encontrar donde insertar los imports (después del docstring si existe)
            if '"""' in content[:500]:
                # Hay docstring, insertar después
                end_docstring = content.find('"""', content.find('"""') + 3) + 3
                content = content[:end_docstring] + "\n\n" + import_section + content[end_docstring:]
            else:
                # No hay docstring, insertar al inicio
                content = import_section + content
                
            print(f"  ✅ Agregados {len(missing_imports)} imports faltantes")
            
        return content
        
    def optimize_code_structure(self, content):
        """Optimizar estructura del código"""
        print("⚡ Optimizando estructura del código...")
        
        # Eliminar líneas de debug innecesarias para producción
        debug_patterns = [
            r'print\(f?"\[DEBUG\][^"]*"\)',
            r'print\(f?"[^"]*DEBUG[^"]*"\)',
        ]
        
        for pattern in debug_patterns:
            content = re.sub(pattern, '# Debug removed for production', content, flags=re.MULTILINE)
            
        # Optimizar imports duplicados
        import_lines = []
        other_lines = []
        in_imports = True
        
        for line in content.split('\n'):
            if line.strip().startswith(('import ', 'from ')) and in_imports:
                if line not in import_lines:
                    import_lines.append(line)
            else:
                if line.strip() and not line.startswith('#'):
                    in_imports = False
                other_lines.append(line)
                
        # Reorganizar imports
        organized_imports = sorted(set(import_lines))
        content = '\n'.join(organized_imports) + '\n\n' + '\n'.join(other_lines)
        
        print("  ✅ Código optimizado")
        return content
        
    def add_production_config(self, content):
        """Agregar configuración para producción"""
        print("🏭 Agregando configuración de producción...")
        
        # Configuración para ejecutable empaquetado
        production_config = '''
# ============================================================================
# CONFIGURACIÓN PARA PRODUCCIÓN - AUTO GENERADO
# ============================================================================

import sys
import os
from pathlib import Path

# Detectar si estamos ejecutando desde PyInstaller
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # Ejecutándose como ejecutable
    RUNNING_AS_EXE = True
    BASE_PATH = Path(sys._MEIPASS)
    DATA_PATH = Path(sys.executable).parent
else:
    # Ejecutándose como script
    RUNNING_AS_EXE = False
    BASE_PATH = Path(__file__).parent
    DATA_PATH = BASE_PATH

# Rutas de archivos de datos
PRODUCTOS_FILE = DATA_PATH / "productos.json"
VENTAS_FILE = DATA_PATH / "ventas.json"
GASTOS_FILE = DATA_PATH / "gastos.json"
USUARIOS_FILE = DATA_PATH / "usuarios.json"

# Función para obtener ruta de recursos
def get_resource_path(relative_path):
    """Obtener ruta absoluta a recurso, compatible con PyInstaller"""
    try:
        if RUNNING_AS_EXE:
            return BASE_PATH / relative_path
        else:
            return BASE_PATH / relative_path
    except Exception:
        return Path(relative_path)

# Configurar logging para producción
import logging
logging.basicConfig(
    level=logging.WARNING,  # Solo warnings y errores en producción
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(DATA_PATH / 'kontrol.log'),
        logging.StreamHandler()
    ]
)

'''
        
        # Insertar configuración después de los imports
        import_end = content.find('\n\n# Paleta moderna')
        if import_end == -1:
            import_end = content.find('\n\nCOLOR_GRADIENTE_1')
            
        if import_end != -1:
            content = content[:import_end] + production_config + content[import_end:]
        else:
            content = production_config + content
            
        print("  ✅ Configuración de producción agregada")
        return content
        
    def optimize_main(self):
        """Proceso completo de optimización"""
        print("🚀 Iniciando optimización de main.py para distribución")
        print("=" * 60)
        
        try:
            # Leer archivo original
            content = self.read_main_file()
            print(f"📖 Archivo original leído: {len(content)} caracteres")
            
            # Aplicar optimizaciones
            content = self.add_missing_imports(content)
            content = self.complete_stub_methods(content)
            content = self.add_production_config(content)
            content = self.optimize_code_structure(content)
            
            # Escribir archivo optimizado
            with open(self.optimized_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"💾 Archivo optimizado guardado: {self.optimized_file}")
            print(f"📊 Tamaño final: {len(content)} caracteres")
            
            # Verificar sintaxis
            try:
                ast.parse(content)
                print("✅ Sintaxis verificada correctamente")
            except SyntaxError as e:
                print(f"❌ Error de sintaxis: {e}")
                return False
                
            print("\n🎉 Optimización completada exitosamente")
            return True
            
        except Exception as e:
            print(f"❌ Error durante la optimización: {e}")
            return False

def main():
    optimizer = MainOptimizer()
    success = optimizer.optimize_main()
    
    if success:
        print("\n✅ main.py optimizado para distribución")
        print("📝 Usa main_optimized.py para el build final")
    else:
        print("\n❌ Error en la optimización")
        
    input("\nPresiona Enter para continuar...")
    return success

if __name__ == "__main__":
    main()