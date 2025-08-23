#!/usr/bin/env python3
"""
Test script para verificar funcionalidad de scroll con rueda del mouse
Este script verifica que la función configurar_scroll_mouse funcione correctamente
"""

import tkinter as tk
from tkinter import ttk

def configurar_scroll_mouse(canvas, scrollbar=None):
    """
    Configura el scroll con rueda del mouse para un Canvas
    """
    def _on_mousewheel(event):
        try:
            if hasattr(event, 'delta'):
                delta = -1 * (event.delta // 120)
            else:
                if event.num == 4:
                    delta = -1
                elif event.num == 5:
                    delta = 1
                else:
                    delta = 0
        except:
            delta = 0
        
        try:
            canvas.yview_scroll(delta, "units")
        except tk.TclError:
            pass
    
    def _bind_to_mousewheel(event):
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Button-4>", _on_mousewheel)
        canvas.bind_all("<Button-5>", _on_mousewheel)
    
    def _unbind_from_mousewheel(event):
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")
    
    canvas.bind('<Enter>', _bind_to_mousewheel)
    canvas.bind('<Leave>', _unbind_from_mousewheel)
    print("✅ Scroll configurado correctamente")

def test_scroll_functionality():
    """Test básico de funcionalidad de scroll"""
    root = tk.Tk()
    root.title("Test - Scroll con Rueda del Mouse")
    root.geometry("400x300")
    
    # Crear frame principal
    main_frame = tk.Frame(root, bg="#1a1f2e")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Crear canvas con scrollbar
    canvas = tk.Canvas(main_frame, bg="#0f172a", highlightthickness=0)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#0f172a")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Agregar contenido de prueba
    for i in range(50):
        label = tk.Label(scrollable_frame, 
                        text=f"📊 Elemento de prueba #{i+1} - Rueda del mouse para scroll",
                        bg="#1e293b" if i % 2 == 0 else "#0f172a",
                        fg="#e5e7eb",
                        font=("Arial", 10),
                        pady=8)
        label.pack(fill="x", pady=1)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Configurar scroll con rueda del mouse
    configurar_scroll_mouse(canvas, scrollbar)
    
    # Instrucciones
    instructions = tk.Label(root, 
                          text="🖱️ Prueba scrollear con la rueda del mouse sobre el contenido",
                          bg="#2563eb", fg="#ffffff", font=("Arial", 10, "bold"), pady=5)
    instructions.pack(fill="x", side="bottom")
    
    print("🚀 Iniciando test de scroll...")
    print("📝 Mueve la rueda del mouse sobre el contenido para probar")
    root.mainloop()

if __name__ == "__main__":
    test_scroll_functionality()
