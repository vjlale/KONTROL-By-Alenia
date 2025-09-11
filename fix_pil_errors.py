#!/usr/bin/env python3
"""
Script para corregir errores de PIL/Pillow en main.py
Reemplaza referencias obsoletas de Image.LANCZOS y Image.ANTIALIAS
"""

import re

def fix_pil_references(file_path):
    """Corrige las referencias de PIL en el archivo"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Patrón para detectar referencias problemáticas
    patterns_to_fix = [
        # Caso 1: Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS
        (
            r'Image\.LANCZOS if hasattr\(Image, [\'"]LANCZOS[\'"].\) else Image\.ANTIALIAS',
            '_get_resample_filter()'
        ),
        
        # Caso 2: Image.ANTIALIAS directo
        (
            r'Image\.ANTIALIAS(?!\w)',
            '_get_resample_filter()'
        ),
        
        # Caso 3: Image.LANCZOS directo
        (
            r'Image\.LANCZOS(?!\w)',
            '_get_resample_filter()'
        )
    ]
    
    # Aplicar reemplazos
    for pattern, replacement in patterns_to_fix:
        content = re.sub(pattern, replacement, content)
    
    # Agregar función helper al inicio de la clase
    helper_function = '''
    def _get_resample_filter(self):
        """Obtiene el filtro de resampling compatible con la versión de Pillow"""
        try:
            return Image.Resampling.LANCZOS
        except AttributeError:
            try:
                return Image.LANCZOS
            except AttributeError:
                try:
                    return Image.ANTIALIAS
                except AttributeError:
                    # Fallback para versiones muy antiguas
                    return 1  # PIL.Image.ANTIALIAS value
'''
    
    # Buscar el inicio de la clase AppPilchero y agregar la función
    class_pattern = r'(class AppPilchero.*?:\s*\n)'
    if re.search(class_pattern, content):
        content = re.sub(class_pattern, r'\1' + helper_function + '\n', content)
    
    # Escribir archivo corregido
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Correcciones de PIL aplicadas exitosamente")

if __name__ == "__main__":
    fix_pil_references("main.py")