#!/usr/bin/env python3
# Script de lanzamiento mejorado para KONTROL+

import sys
import os

print("=== KONTROL+ - Iniciando aplicación ===")
print(f"Python version: {sys.version}")
print(f"Directorio actual: {os.getcwd()}")

# Verificar iconos
iconos = [
    'screenshot/iconos/icoNUEVAVENTA.png',
    'screenshot/iconos/icoVENTAS DEL DÍA.png', 
    'screenshot/iconos/icoMenú.png'
]

print("\n--- Verificando iconos ---")
for icono in iconos:
    if os.path.exists(icono):
        size = os.path.getsize(icono)
        print(f"✅ {icono} ({size} bytes)")
    else:
        print(f"❌ {icono} - NO ENCONTRADO")

print("\n--- Iniciando aplicación principal ---")

# Importar y ejecutar la aplicación
try:
    from main import AppPilchero, SistemaGestion
    
    print("✅ Módulos importados correctamente")
    
    # Crear sistema y aplicación
    sistema = SistemaGestion()
    app = AppPilchero(sistema)
    
    print("✅ Aplicación inicializada")
    print("🚀 Ejecutando interfaz gráfica...")
    
    # Ejecutar el loop principal
    app.mainloop()
    
except Exception as e:
    print(f"❌ Error ejecutando aplicación: {e}")
    import traceback
    traceback.print_exc()