#!/usr/bin/env python3
"""
Test script para verificar la corrección del filtro de resample
"""
from PIL import Image
import os
import sys

def test_resample_filter():
    """Prueba la función _get_resample_filter corregida"""
    try:
        # Primero intentar el nuevo sistema de PIL (Pillow >= 10.0.0)
        resample_filter = Image.Resampling.LANCZOS
        print("✅ Usando Image.Resampling.LANCZOS")
        return resample_filter
    except AttributeError:
        try:
            # Versiones intermedias de Pillow
            resample_filter = Image.LANCZOS
            print("✅ Usando Image.LANCZOS")
            return resample_filter
        except AttributeError:
            try:
                # Versiones más antiguas
                resample_filter = Image.ANTIALIAS
                print("✅ Usando Image.ANTIALIAS")
                return resample_filter
            except AttributeError:
                # Fallback absoluto para versiones muy antiguas
                resample_filter = 1  # Valor numérico directo
                print("✅ Usando fallback numérico (1)")
                return resample_filter

if __name__ == "__main__":
    print("🔍 Probando corrección del filtro de resample...")
    filter_result = test_resample_filter()
    print(f"📊 Filtro obtenido: {filter_result}")
    
    # Probar redimensionamiento si hay una imagen disponible
    test_images = ["LOGO APP.png", "7.png", "ALENRESULTADOS.png"]
    for img_path in test_images:
        if os.path.exists(img_path):
            try:
                print(f"🖼️ Probando redimensionamiento con {img_path}...")
                img = Image.open(img_path)
                resized = img.resize((50, 50), filter_result)
                print(f"✅ Redimensionamiento exitoso: {img.size} -> (50, 50)")
                break
            except Exception as e:
                print(f"❌ Error redimensionando {img_path}: {e}")
    
    print("🎯 Prueba completada")
