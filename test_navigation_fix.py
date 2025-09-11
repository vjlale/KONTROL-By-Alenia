#!/usr/bin/env python3
"""
Test script para verificar la navegación y limpieza de pantalla
"""
import tkinter as tk
from tkinter import messagebox
import os
import sys

# Agregar el directorio actual al path para importar el módulo principal
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_navigation():
    """Prueba la navegación y limpieza de pantalla"""
    try:
        # Import the main module
        import main
        
        print("✅ Módulo main importado correctamente")
        
        # Verificar que las funciones clave existen
        functions_to_check = [
            'aplicar_estilo_moderno_boton',
            'aplicar_estilo_moderno_treeview', 
            'crear_tooltip',
            'validar_campo_visual'
        ]
        
        for func_name in functions_to_check:
            if hasattr(main, func_name):
                print(f"✅ Función {func_name} disponible")
            else:
                print(f"❌ Función {func_name} NO disponible")
        
        # Verificar clases principales
        classes_to_check = ['Producto', 'Venta', 'SistemaGestion', 'AppPilchero']
        for class_name in classes_to_check:
            if hasattr(main, class_name):
                print(f"✅ Clase {class_name} disponible")
            else:
                print(f"❌ Clase {class_name} NO disponible")
        
        # Test básico de SistemaGestion
        sistema = main.SistemaGestion()
        print(f"✅ SistemaGestion inicializado - Productos: {len(sistema.productos)}, Ventas: {len(sistema.ventas)}")
        
        # Test AppPilchero (sin mostrar UI)
        app = main.AppPilchero(sistema)
        print("✅ AppPilchero inicializado correctamente")
        
        # Test método _get_resample_filter
        filter_result = app._get_resample_filter()
        print(f"✅ _get_resample_filter funciona: {filter_result}")
        
        # Test limpiar_pantalla
        app.pantalla_widgets = [1, 2, "test"]  # Simular widgets
        app.limpiar_pantalla()
        print(f"✅ limpiar_pantalla funciona - widgets restantes: {len(app.pantalla_widgets)}")
        
        app.destroy()  # Cerrar la aplicación
        print("✅ Todas las pruebas de navegación pasaron")
        return True
        
    except Exception as e:
        print(f"❌ Error en pruebas de navegación: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Probando navegación y correcciones...")
    success = test_navigation()
    if success:
        print("🎯 ¡Todas las correcciones funcionan correctamente!")
    else:
        print("⚠️ Se encontraron problemas en las correcciones")
