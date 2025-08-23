## Mejoras visuales propuestas (main.py)

Este documento lista los cambios sugeridos para modernizar la UI (Tkinter) de Alen.iA Gestión, indicando dónde aplicarlos en `main.py` y brindando fragmentos listos para pegar.

---

### Cambios críticos inmediatos

- Combobox (texto invisible): corrige el color del texto (tenía 8 dígitos)

```python
# En aplicar_estilo_moderno_combobox
style.configure("Moderno.TCombobox",
                fieldbackground="#ffffff",
                background="#ffffff",
                foreground="#333333",  # ← antes estaba "#33333300"
                borderwidth=3,
                relief="solid",
                focuscolor=COLOR_CIAN,
                selectbackground=COLOR_CIAN,
                selectforeground="#0c0b0b",
                font=("Montserrat", 12))
```

- Logo secundario (ruta estable): usa el archivo existente `7.png` (evita inconsistencias entre mayúsculas/minúsculas)

```python
# En _colocar_logo_secundarias
logo_path = "7.png"
# Si empaquetas con PyInstaller, resuelve el path desde sys._MEIPASS si corresponde
```

---

### Paleta moderna (modo oscuro)

Sustituye las constantes de color del inicio del archivo por esta paleta moderna, sobria y consistente:

```python
# Paleta moderna (modo oscuro)
COLOR_GRADIENTE_1 = "#0f172a"
COLOR_GRADIENTE_2 = "#111827"
COLOR_CIAN = "#e5e7eb"        # Texto principal claro
COLOR_AZUL = "#0f172a"
COLOR_FONDO = COLOR_AZUL
COLOR_BOTON = "#4f46e5"       # Indigo
COLOR_BOTON_SECUNDARIO = "#6b7280"
COLOR_TOTAL_IVA_BG = "#1f2937"   # Panels grises
COLOR_LABEL_VENTA_BG = "#1f2937"
COLOR_ENTRY_VENTA_BG = "#ffffff"
COLOR_BOTON_TEXTO = "#ffffff"
COLOR_TEXTO = "#e5e7eb"
COLOR_ENTRADA = "#111827"
COLOR_BOTON_HOVER = "#4338ca"     # Indigo hover

# Botones por tipo
COLOR_BOTON_MODERNO = "#4f46e5"         # primario
COLOR_BOTON_HOVER_MODERNO = "#4338ca"
COLOR_BOTON_SUCCESS = "#10b981"         # verde moderno
COLOR_BOTON_WARNING = "#f59e0b"         # naranja moderno
COLOR_BOTON_DANGER = "#ef4444"          # rojo moderno
COLOR_BOTON_SECONDARY = "#6b7280"       # gris moderno
```

Impacto: mejora la legibilidad, reduce saturación y unifica el look & feel.

---

### Treeview “moderno” (cabecera, filas, selección)

Reemplaza `aplicar_estilo_moderno_treeview` por esta versión (tema `clam`, altura de fila, header plano, selección indigo):

```python
def aplicar_estilo_moderno_treeview(tree):
    try:
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("Moderno.Treeview",
                        background="#ffffff",
                        foreground="#111827",
                        fieldbackground="#ffffff",
                        borderwidth=0,
                        font=("Montserrat", 10),
                        rowheight=28)

        style.configure("Moderno.Treeview.Heading",
                        background="#1f2937",
                        foreground="#ffffff",
                        relief="flat",
                        font=("Montserrat", 10, "bold"))

        style.map("Moderno.Treeview",
                  background=[('selected', "#4f46e5")],
                  foreground=[('selected', '#ffffff')])

        tree.configure(style="Moderno.Treeview")
    except Exception as e:
        print(f"[DEBUG] Error aplicando estilo a treeview: {e}")
```

Opcional: reduce columnas visibles y aumenta anchos para menos ruido visual.

---

### Tooltip limpio (oscuro, sin borde verde)

Moderniza el método `show` de `Tooltip` para un estilo sutil y legible:

```python
def show(self):
    if self.tooltip_window:
        return

    x, y, _, _ = self.widget.bbox("insert") if hasattr(self.widget, 'bbox') else (0, 0, 0, 0)
    x += self.widget.winfo_rootx() + 16
    y += self.widget.winfo_rooty() + 16

    self.tooltip_window = tk.Toplevel(self.widget)
    self.tooltip_window.wm_overrideredirect(True)
    self.tooltip_window.wm_geometry(f"+{x}+{y}")

    frame = tk.Frame(self.tooltip_window, background="#0b1220", borderwidth=1, relief="solid")
    frame.pack()

    label = tk.Label(frame, text=self.text, justify="left",
                     background="#0b1220", foreground="#e5e7eb",
                     font=("Montserrat", 9), padx=10, pady=6)
    label.pack()
```

---

### Barra superior reutilizable (título + volver)

Crea una barra estándar y úsala en todas las pantallas para cohesión visual.

```python
def _barra_superior(self, titulo, on_volver):
    bar = tk.Frame(self.canvas_bg, bg="#0b1220")
    self.canvas_bg.create_window(640, 60, window=bar, width=1180, height=50, anchor="center")

    lbl = tk.Label(bar, text=titulo, font=("Montserrat", 14, "bold"), bg="#0b1220", fg="#e5e7eb")
    lbl.place(x=20, y=12)

    btn_volver = tk.Button(bar, text="← Volver", font=("Montserrat", 11, "bold"),
                           bg="#374151", fg="#ffffff", bd=0, relief="flat",
                           cursor="hand2", command=on_volver)
    btn_volver.place(x=1060, y=8, width=100, height=34)
    aplicar_estilo_moderno_boton(btn_volver, "secundario", hover_efecto=True)

# Ejemplo de uso al inicio de cada pantalla
self._barra_superior("VENTAS DEL DÍA", self.mostrar_menu_principal)
```

---

### Ajustes rápidos por pantalla

- Venta: sube el tamaño del título a 16–18; unifica paneles "TOTAL" e "IVA" con `COLOR_TOTAL_IVA_BG`; mantiene `aplicar_estilo_moderno_entry` en entradas.
- Ventas del día: coloca título con `_barra_superior`; mantiene el label de total con fondo gris oscuro.
- Alta producto / Actualizar precio: organiza entradas en dos columnas con `grid` dentro de un `Frame` para mejor alineación (opcional gradual); aplica `aplicar_estilo_moderno_entry` a todos los `Entry`.
- Inventario: usa tags para resaltar bajo stock (ej. `stock <= 5` → fondo tenue/rojo claro en la fila).

Ejemplo para resaltar bajo stock:

```python
tree.tag_configure('lowstock', background='#fee2e2')
# Al insertar filas
tag = 'lowstock' if p.cantidad <= 5 else ''
tree.insert("", "end", values=(...), tags=(tag,))
```

---

### Opcionales (≈1 hora)

- Migrar gradualmente a `ttk.Button` con estilos nombrados.

```python
style = ttk.Style(); style.theme_use('clam')
style.configure('Primary.TButton', background='#4f46e5', foreground='#ffffff', font=("Montserrat", 12, "bold"), padding=10)
style.map('Primary.TButton', background=[('active', '#4338ca')])

btn = ttk.Button(parent, text="Aceptar", style='Primary.TButton', command=...)
```

- Modo claro/oscuro: define 2 paletas y un toggle en la barra superior que reasigne constantes y reconstruya la pantalla actual.
- Ordenamiento por columna en `Treeview`: enlaza el header para ordenar asc/desc.
- Reemplazar emojis por íconos PNG si empaquetas (mejor legibilidad cross-OS).

---

### Rendimiento y consistencia

- Gradiente de fondo: generar una sola imagen con `Pillow` y dibujarla como `PhotoImage` (menos CPU que cientos de rectángulos).
- Tipografía: si no está instalada Montserrat, usa fallback a `Segoe UI`.

```python
import tkinter.font as tkfont
FUENTE_BASE = ("Montserrat", 12) if "Montserrat" in tkfont.families() else ("Segoe UI", 12)
```

---

### Checklist de aplicación

- [ ] Corregir `foreground` en `aplicar_estilo_moderno_combobox`
- [ ] Cambiar ruta a `7.png` en `_colocar_logo_secundarias`
- [ ] Sustituir paleta de colores en el bloque de constantes
- [ ] Reemplazar `aplicar_estilo_moderno_treeview`
- [ ] Actualizar `Tooltip.show`
- [ ] Añadir `_barra_superior` y usarla en cada pantalla
- [ ] Ajustar título y paneles de totales en Venta
- [ ] Resaltar bajo stock en Inventario (tags)
- [ ] (Opcional) Migrar botones a `ttk.Button` con estilos
- [ ] (Opcional) Toggle modo claro/oscuro
- [ ] (Opcional) Optimizar gradiente con `Pillow`


