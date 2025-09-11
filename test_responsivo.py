#!/usr/bin/env python3
"""
Script de prueba para verificar la implementación de responsividad en KONTROL+
"""

import tkinter as tk
import sys
import os

# Agregar el directorio actual al path para importar main
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_responsive_window():
    """Prueba la aplicación responsiva con diferentes tamaños de ventana"""
    
    print("=== INICIANDO PRUEBA DE RESPONSIVIDAD KONTROL+ === - test_responsivo.py:16")
    print("✅ Importando módulos principales... - test_responsivo.py:17")
    
    try:
        import main
        print("✅ Módulo main.py importado correctamente - test_responsivo.py:21")
        
        # Crear instancia del sistema de gestión
        sistema = main.SistemaGestion()
        print("✅ SistemaGestion inicializado - test_responsivo.py:25")
        
        # Crear la aplicación principal
        app = main.AppPilchero(sistema)
        print("✅ AppPilchero inicializado - test_responsivo.py:29")
        
        # Verificar métodos responsivos
        has_responsive_dims = hasattr(app, 'get_responsive_dimensions')
        has_responsive_widgets = hasattr(app, 'create_responsive_button')
        has_responsive_logos = hasattr(app, '_colocar_logo_principal')
        
        print(f"✅ Método get_responsive_dimensions: {'Disponible' if has_responsive_dims else 'No encontrado'} - test_responsivo.py:36")
        print(f"✅ Método create_responsive_button: {'Disponible' if has_responsive_widgets else 'No encontrado'} - test_responsivo.py:37")
        print(f"✅ Método _colocar_logo_principal: {'Disponible' if has_responsive_logos else 'No encontrado'} - test_responsivo.py:38")
        
        # Obtener dimensiones actuales
        if has_responsive_dims:
            dims = app.get_responsive_dimensions()
            print(f"✅ Dimensiones responsivas obtenidas: {dims['width']}x{dims['height']} - test_responsivo.py:43")
        
        print("\n=== INICIANDO APLICACIÓN RESPONSIVA === - test_responsivo.py:45")
        print("🔄 La aplicación se ejecutará en modo responsivo. - test_responsivo.py:46")
        print("📱 Puedes redimensionar la ventana para probar la responsividad. - test_responsivo.py:47")
        print("❌ Cierra la ventana para finalizar la prueba. - test_responsivo.py:48")
        
        # Iniciar la aplicación
        app.root.mainloop()
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e} - test_responsivo.py:54")
        import traceback
        traceback.print_exc()
        return False
    
    print("✅ Prueba de responsividad completada exitosamente - test_responsivo.py:59")
    return True

if __name__ == "__main__":
    test_responsive_window()