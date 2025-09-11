#!/usr/bin/env python3
# Test script para verificar que los iconos se cargan correctamente

from PIL import Image, ImageTk
import os
import tkinter as tk

def test_iconos():
    """Prueba la carga de iconos"""
    iconos = [
        'screenshot/iconos/icoNUEVAVENTA.png',
        'screenshot/iconos/icoVENTAS DEL DÍA.png', 
        'screenshot/iconos/icoMenú.png'
    ]
    
    print("=== TEST DE ICONOS ===")
    
    for icono_path in iconos:
        print(f"\nProbando: {icono_path}")
        try:
            # Verificar existencia
            if not os.path.exists(icono_path):
                print(f"  ❌ Archivo no encontrado: {icono_path}")
                continue
            
            # Cargar imagen
            img = Image.open(icono_path).convert("RGBA")
            print(f"  ✅ Imagen cargada: {img.size} pixels, modo: {img.mode}")
            
            # Redimensionar
            img_resized = img.resize((32, 32), Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.LANCZOS)
            print(f"  ✅ Redimensionada a: {img_resized.size}")
            
            # Verificar que se puede convertir a PhotoImage (requiere ventana Tk)
            root = tk.Tk()
            root.withdraw()  # Ocultar ventana
            img_tk = ImageTk.PhotoImage(img_resized)
            print(f"  ✅ Convertida a PhotoImage: {type(img_tk)}")
            root.destroy()
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n=== FIN TEST ===")

if __name__ == "__main__":
    test_iconos()