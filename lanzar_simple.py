#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Script de lanzamiento simple para KONTROL+

import sys
import os

print("=== KONTROL+ - Iniciando aplicacion ===")
print(f"Python version: {sys.version}")
print(f"Directorio actual: {os.getcwd()}")

# Verificar iconos
iconos = [
    'screenshot/iconos/icoNUEVAVENTA.png',
    'screenshot/iconos/icoVENTAS DEL DIA.png', 
    'screenshot/iconos/icoMenu.png'
]

print("\n--- Verificando iconos ---")
for icono in iconos:
    if os.path.exists(icono):
        size = os.path.getsize(icono)
        print(f"OK {icono} ({size} bytes)")
    else:
        print(f"ERROR {icono} - NO ENCONTRADO")

# Importar y ejecutar la aplicación
try:
    print("\n--- Iniciando aplicacion principal ---")
    from main import AppPilchero, SistemaGestion
    
    print("OK Modulos importados correctamente")
    
    # Crear sistema y aplicación
    sistema = SistemaGestion()
    app = AppPilchero(sistema)
    
    print("OK Aplicacion inicializada")
    print("Ejecutando interfaz grafica...")
    
    # Ejecutar el loop principal
    app.mainloop()
    
except Exception as e:
    print(f"ERROR ejecutando aplicacion: {e}")
    import traceback
    traceback.print_exc()