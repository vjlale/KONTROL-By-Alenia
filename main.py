import datetime
import sys
from typing import List, Dict, Optional
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import csv
import tkinter.font as tkfont
from auth import AuthManager
from session_manager import SessionManager

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
COLOR_BOTON_SUCCESS = "#03985a"         # verde moderno
COLOR_BOTON_WARNING = "#f59e0b"         # naranja moderno
COLOR_BOTON_DANGER = "#ef4444"          # rojo moderno
COLOR_BOTON_SECONDARY = "#6b7280"       # gris moderno

try:
    FUENTE_BASE = ("Montserrat", 12) if "Montserrat" in tkfont.families() else ("Segoe UI", 12)
except Exception:
    FUENTE_BASE = ("Segoe UI", 12)

def aplicar_estilo_moderno_boton(boton, tipo="primario", hover_efecto=True):
    """
    Aplica estilo moderno a un botón con bordes redondeados y efectos
    Args:
        boton: El widget Button a estilizar
        tipo: "primario", "secundario", "success", "warning", "danger"
        hover_efecto: Si aplicar efectos hover
    """
    # Definir colores según el tipo
    colores = {
        "primario": (COLOR_BOTON_MODERNO, COLOR_BOTON_HOVER_MODERNO),
        "secundario": (COLOR_BOTON_SECONDARY, "#4b5563"),
        "success": (COLOR_BOTON_SUCCESS, "#047857"),
        "warning": (COLOR_BOTON_WARNING, "#b45309"),
        "danger": (COLOR_BOTON_DANGER, "#b91c1c")
    }
    
    color_normal, color_hover = colores.get(tipo, colores["primario"])
    
    # Configurar el botón con estilo moderno
    boton.config(
        bg=color_normal,
        fg="#ffffff",
        bd=2,
        relief="solid",
        cursor="hand2",
        activebackground=color_hover,
        activeforeground="#ffffff",
        highlightthickness=0,
        padx=15,
        pady=8
    )
    
    if hover_efecto:
        # Efectos hover mejorados
        def on_enter(e):
            boton.config(
                bg=color_hover, 
                relief="raised", 
                bd=3,
                font=(boton.cget("font").split()[0] if hasattr(boton.cget("font"), 'split') else "Montserrat", 
                      int(boton.cget("font").split()[1]) if hasattr(boton.cget("font"), 'split') and len(boton.cget("font").split()) > 1 else 12, 
                      "bold")
            )
        
        def on_leave(e):
            boton.config(
                bg=color_normal, 
                relief="solid", 
                bd=2,
                font=(boton.cget("font").split()[0] if hasattr(boton.cget("font"), 'split') else "Montserrat", 
                      int(boton.cget("font").split()[1]) if hasattr(boton.cget("font"), 'split') and len(boton.cget("font").split()) > 1 else 12, 
                      "bold")
            )
        
        boton.bind("<Enter>", on_enter)
        boton.bind("<Leave>", on_leave)

def aplicar_estilo_moderno_entry(entry):
    """Aplica estilo moderno a un Entry"""
    entry.config(
        bd=2,
        relief="solid",
        highlightthickness=1,
        highlightcolor=COLOR_CIAN,
        highlightbackground="#cccccc",
        font=("Montserrat", 10),
        fg="#333333"
    )

def aplicar_estilo_moderno_label(label, tipo="normal"):
    """Aplica estilo moderno a un Label"""
    if tipo == "titulo":
        label.config(
            font=("Montserrat", 18, "bold"),
            fg=COLOR_CIAN,
            relief="flat",
            bd=0
        )
    elif tipo == "subtitulo":
        label.config(
            font=("Montserrat", 14, "bold"),
            fg=COLOR_TEXTO,
            relief="flat",
            bd=0
        )
    else:
        label.config(
            font=("Montserrat", 12),
            fg=COLOR_TEXTO,
            relief="flat",
            bd=0
        )

def aplicar_estilo_moderno_combobox(combo):
    """Aplica estilo moderno a un Combobox"""
    try:
        # Configuración para ttk.Combobox
        style = ttk.Style()
        
        # Crear un estilo personalizado para el combobox
        style.theme_use('default')
        
        # Estilo para el Combobox (campo de entrada)
        style.configure("Moderno.TCombobox",
                       fieldbackground="#ffffff",
                       background="#ffffff",
                       foreground="#333333",
                       borderwidth=3,
                       relief="solid",
                       focuscolor=COLOR_CIAN,
                       selectbackground=COLOR_CIAN,
                       selectforeground="#0c0b0b",
                       font=("Montserrat", 12))
        
        # Estilo para el botón dropdown
        style.configure("Moderno.TCombobox",
                       arrowcolor=COLOR_BOTON_MODERNO,
                       borderwidth=3,
                       relief="solid")
        
        # Aplicar el estilo al combobox
        combo.configure(style="Moderno.TCombobox")
        
        # Configuración adicional directa
        combo.configure(font=("Montserrat", 10))
        
    except Exception as e:
        # Fallback si hay problemas con el estilo
        print(f"[DEBUG] Error aplicando estilo a combobox: {e} - main.py:171")
        combo.configure(font=("Montserrat", 10))

def aplicar_estilo_moderno_treeview(tree):
    try:
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("Moderno.Treeview",
                        background="#1f2937",
                        foreground="#e5e7eb",
                        fieldbackground="#1f2937",
                        borderwidth=0,
                        font=("Montserrat", 12),
                        rowheight=28)

        style.configure("Moderno.Treeview.Heading",
                        background="#2563eb",
                        foreground="#ffffff",
                        relief="flat",
                        font=("Montserrat", 11, "bold"))

        style.map("Moderno.Treeview",
                  background=[('selected', "#4f46e5")],
                  foreground=[('selected', '#ffffff')])

        tree.configure(style="Moderno.Treeview")

        # Estilo visible para scrollbars verticales en fondo oscuro
        try:
            base_layout = style.layout('Vertical.TScrollbar')
            style.layout('Moderno.Vertical.TScrollbar', base_layout)
        except Exception:
            pass
        # Colores grises profesionales para mayor neutralidad
        style.configure('Moderno.Vertical.TScrollbar',
                        troughcolor="#1f2937",   # canal gris oscuro
                        background="#9ca3af",    # thumb gris medio
                        bordercolor="#374151",
                        lightcolor="#6b7280",
                        darkcolor="#4b5563",
                        arrowsize=14)
        style.map('Moderno.Vertical.TScrollbar',
                  background=[('active', '#b0b7c3'), ('!disabled', '#9ca3af')])
    except Exception as e:
        print(f"[DEBUG] Error aplicando estilo a treeview: {e} - main.py:199")

class Tooltip:
    """Clase para crear tooltips informativos modernos"""
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window = None
        self.id = None
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        self.widget.bind("<Motion>", self.on_motion)

    def on_enter(self, event=None):
        self.schedule()

    def on_leave(self, event=None):
        self.unschedule()
        self.hide()

    def on_motion(self, event=None):
        self.unschedule()
        self.schedule()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.delay, self.show)

    def unschedule(self):
        if self.id:
            self.widget.after_cancel(self.id)
        self.id = None

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

    def hide(self):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

def crear_tooltip(widget, texto):
    """Función helper para crear tooltips fácilmente"""
    return Tooltip(widget, texto)

def agregar_icono_a_boton(boton, ruta_icono, tamaño=(24, 24)):
    """
    Agrega un ícono PNG a un botón existente
    Args:
        boton: El widget Button al que agregar el ícono
        ruta_icono: Ruta al archivo PNG del ícono
        tamaño: Tupla (ancho, alto) para redimensionar el ícono
    Returns:
        True si se agregó exitosamente, False en caso contrario
    """
    try:
        from PIL import Image, ImageTk
        import os, sys
        
        # Manejo de rutas para ejecutable y desarrollo
        if hasattr(sys, '_MEIPASS'):
            # En ejecutable compilado, buscar en el directorio base
            icono_path = os.path.join(sys._MEIPASS, os.path.basename(ruta_icono))
        else:
            # En desarrollo, usar ruta completa
            icono_path = ruta_icono
            
        if not os.path.exists(icono_path):
            print(f"[DEBUG] Ícono no encontrado: {icono_path} - main.py:283")
            return False
            
        # Cargar y redimensionar el ícono
        icono_img = Image.open(icono_path).convert("RGBA")
        icono_resized = icono_img.resize(tamaño, Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS)
        icono_tk = ImageTk.PhotoImage(icono_resized)
        
        # Configurar el botón con el ícono
        boton.config(image=icono_tk, compound="left")  # compound="left" pone el ícono a la izquierda del texto
        
        # Guardar referencia para evitar que sea eliminado por el garbage collector
        if not hasattr(boton, '_iconos'):
            boton._iconos = []
        boton._iconos.append(icono_tk)
        
        print(f"[DEBUG] Ícono agregado exitosamente: {ruta_icono} - main.py:299")
        return True
        
    except Exception as e:
        print(f"[DEBUG] Error agregando ícono {ruta_icono}: {e} - main.py:303")
        return False

def validar_campo_visual(entry, es_valido, mensaje_error=""):
    """Aplica validación visual a un campo Entry"""
    if es_valido:
        entry.config(highlightcolor="#01A807", highlightbackground="#4CAF50", bd=2)
        # Quitar cualquier tooltip de error existente
        if hasattr(entry, '_tooltip_error'):
            entry._tooltip_error.hide()
    else:
        entry.config(highlightcolor="#f44336", highlightbackground="#f44336", bd=2)
        # Agregar tooltip de error si hay mensaje
        if mensaje_error:
            if not hasattr(entry, '_tooltip_error'):
                entry._tooltip_error = crear_tooltip(entry, mensaje_error)
            else:
                entry._tooltip_error.text = mensaje_error

def aplicar_animacion_hover_mejorada(widget, color_normal, color_hover):
    """Aplica animación de hover mejorada con transición suave"""
    def on_enter(e):
        widget.config(bg=color_hover)
        # Efecto de "elevación" visual
        widget.config(relief="raised", bd=3)
    
    def on_leave(e):
        widget.config(bg=color_normal)
        widget.config(relief="solid", bd=2)
    
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

def configurar_scroll_mouse(canvas, scrollbar=None):
    """
    Configura el scroll con rueda del mouse para un Canvas
    Args:
        canvas: El widget Canvas al que aplicar el scroll
        scrollbar: El scrollbar asociado (opcional)
    """
    def _on_mousewheel(event):
        # Determinar la dirección del scroll (compatible con Windows y Linux)
        try:
            if hasattr(event, 'delta'):
                # Windows: event.delta es positivo para scroll arriba, negativo para abajo
                delta = -1 * (event.delta // 120)  # Normalizar para Windows
            else:
                # Linux: event.num es 4 para arriba, 5 para abajo
                if event.num == 4:
                    delta = -1
                elif event.num == 5:
                    delta = 1
                else:
                    delta = 0
        except:
            delta = 0
        
        # Aplicar scroll al canvas solo si hay contenido que scrollear
        try:
            canvas.yview_scroll(delta, "units")
        except tk.TclError:
            pass  # Ignorar errores si no hay contenido scrolleable
    
    def _bind_to_mousewheel(event):
        # Activar scroll cuando el mouse entra en el área
        canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows
        canvas.bind_all("<Button-4>", _on_mousewheel)    # Linux scroll up
        canvas.bind_all("<Button-5>", _on_mousewheel)    # Linux scroll down
    
    def _unbind_from_mousewheel(event):
        # Desactivar scroll cuando el mouse sale del área
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")
    
    # Bind events para activar/desactivar scroll según posición del mouse
    canvas.bind('<Enter>', _bind_to_mousewheel)
    canvas.bind('<Leave>', _unbind_from_mousewheel)
    
    print(f"[DEBUG] Scroll con rueda del mouse configurado para canvas: {canvas} - main.py:382")
    
    # También vincular a todos los widgets hijos del canvas para mejor experiencia
    def bind_recursive(widget):
        try:
            widget.bind('<Enter>', _bind_to_mousewheel)
            widget.bind('<Leave>', _unbind_from_mousewheel)
            for child in widget.winfo_children():
                bind_recursive(child)
        except:
            pass  # Ignorar errores en widgets que no soportan bind

    # Enlazar también a los widgets hijos del canvas para asegurar el scroll en contenidos embebidos
    bind_recursive(canvas)

class Producto:
    def __init__(self, marca: str, descripcion: str, color: str, talle: str, cantidad: int, precio_costo: float, porcentaje_venta: float = 50, porcentaje_amigo: float = 20, oferta: dict = {}):
        self.marca = marca
        self.descripcion = descripcion
        self.color = color
        self.talle = talle
        self.cantidad = cantidad
        self.precio_costo = precio_costo
        self.porcentaje_venta = porcentaje_venta
        self.porcentaje_amigo = porcentaje_amigo
        self.oferta = oferta if oferta is not None else {}
        self.precio_venta = self.calcular_precio_venta()
        self.precio_amigo = self.calcular_precio_amigo()

    def calcular_precio_venta(self):
        return round(self.precio_costo * (1 + self.porcentaje_venta / 100), 2)

    def calcular_precio_amigo(self):
        return round(self.precio_costo * (1 + self.porcentaje_amigo / 100), 2)

    def actualizar_precio_costo(self, nuevo_precio):
        self.precio_costo = nuevo_precio
        self.precio_venta = self.calcular_precio_venta()
        self.precio_amigo = self.calcular_precio_amigo()

class Venta:
    def __init__(self, descripcion: str, items: list, fecha: datetime.date, forma_pago: str = "EFECTIVO", vendedor: str = None):
        self.descripcion = descripcion
        self.items = items  # lista de dicts: {producto, cantidad, precio}
        self.fecha = fecha
        self.forma_pago = forma_pago
        self.vendedor = vendedor if vendedor else "Sin especificar"

class Gasto:
    def __init__(self, monto: float, motivo: str, fecha: datetime.date, usuario: str = None):
        self.monto = monto
        self.motivo = motivo
        self.fecha = fecha
        self.usuario = usuario if usuario else "Sin especificar"
        self.timestamp = datetime.datetime.now()

class SistemaGestion:
    def __init__(self):
        self.productos: List[Producto] = []
        self.ventas: List[Venta] = []
        self.gastos: List[Gasto] = []
        self.cargar_datos()

    def cargar_datos(self):
        if os.path.exists("productos.json"):
            with open("productos.json", "r", encoding="utf-8") as f:
                productos = json.load(f)
                for p in productos:
                    self.productos.append(Producto(
                        p.get("marca", ""),
                        p["descripcion"], p["color"], p["talle"], p["cantidad"], p["precio_costo"], p.get("porcentaje_venta", 50), p.get("porcentaje_amigo", 20)
                    ))
        if os.path.exists("ventas.json"):
            with open("ventas.json", "r", encoding="utf-8") as f:
                ventas = json.load(f)
                for v in ventas:
                    items = []
                    for item in v["items"]:
                        prod = self.buscar_producto(item.get("marca", ""), item["producto"], item["color"], item["talle"])  # Marca ahora se guarda; fallback sin marca
                        if not prod:
                            for p in self.productos:
                                if p.descripcion == item["producto"] and p.color == item["color"] and p.talle == item["talle"]:
                                    prod = p
                                    break
                        if prod:
                            items.append({
                                "producto": prod,
                                "cantidad": item["cantidad"],
                                "precio": item["precio"]
                            })
                    self.ventas.append(Venta(
                        v["descripcion"], items, datetime.datetime.strptime(v["fecha"], "%Y-%m-%d").date(), 
                        v.get("forma_pago", "EFECTIVO")
                    ))
        
        # Cargar gastos
        if os.path.exists("gastos.json"):
            with open("gastos.json", "r", encoding="utf-8") as f:
                gastos = json.load(f)
                for g in gastos:
                    self.gastos.append(Gasto(
                        monto=g["monto"],
                        motivo=g["motivo"],
                        fecha=datetime.datetime.strptime(g["fecha"], "%Y-%m-%d").date(),
                        usuario=g.get("usuario", "Sin especificar")
                    ))

    def guardar_productos(self):
        with open("productos.json", "w", encoding="utf-8") as f:
            json.dump([
                {
                    "marca": p.marca,
                    "descripcion": p.descripcion,
                    "color": p.color,
                    "talle": p.talle,
                    "cantidad": p.cantidad,
                    "precio_costo": p.precio_costo,
                    "porcentaje_venta": p.porcentaje_venta,
                    "porcentaje_amigo": p.porcentaje_amigo
                } for p in self.productos
            ], f, ensure_ascii=False, indent=2)

    def guardar_ventas(self):
        with open("ventas.json", "w", encoding="utf-8") as f:
            json.dump([
                {
                    "descripcion": v.descripcion,
                    "items": [
                        {
                            "producto": item["producto"].descripcion,
                            "marca": item["producto"].marca,
                            "color": item["producto"].color,
                            "talle": item["producto"].talle,
                            "cantidad": item["cantidad"],
                            "precio": item["precio"]
                        } for item in v.items
                    ],
                    "fecha": v.fecha.strftime("%Y-%m-%d"),
                    "forma_pago": getattr(v, 'forma_pago', 'EFECTIVO'),
                    "vendedor": getattr(v, 'vendedor', 'Sin especificar')
                } for v in self.ventas
            ], f, ensure_ascii=False, indent=2)

    def guardar_gastos(self):
        """Guarda gastos en gastos.json"""
        with open("gastos.json", "w", encoding="utf-8") as f:
            json.dump([
                {
                    "monto": g.monto,
                    "motivo": g.motivo,
                    "fecha": g.fecha.strftime("%Y-%m-%d"),
                    "usuario": g.usuario,
                    "timestamp": g.timestamp.isoformat()
                } for g in self.gastos
            ], f, ensure_ascii=False, indent=2)

    def agregar_producto(self, marca, descripcion, color, talle, cantidad, precio_costo, porcentaje_venta=50, porcentaje_amigo=20):
        prod = Producto(marca, descripcion, color, talle, cantidad, precio_costo, porcentaje_venta, porcentaje_amigo)
        self.productos.append(prod)
        self.guardar_productos()

    def registrar_venta(self, descripcion, items, fecha, forma_pago="EFECTIVO", vendedor: str = None):
        # items: lista de tuplas (producto, cantidad, precio)
        for producto, cantidad, _ in items:
            if producto.cantidad < cantidad:
                return False
        for producto, cantidad, _ in items:
            producto.cantidad -= cantidad
        venta_items = [{"producto": p, "cantidad": c, "precio": pr} for p, c, pr in items]
        venta = Venta(descripcion, venta_items, fecha, forma_pago, vendedor=vendedor)
        self.ventas.append(venta)
        self.guardar_productos()
        self.guardar_ventas()
        return True

    def agregar_gasto(self, monto: float, motivo: str, fecha: datetime.date, usuario: str = None):
        """Agrega un nuevo gasto"""
        print(f"[DEBUG] SistemaGestion.agregar_gasto llamado: monto={monto}, motivo='{motivo}', fecha={fecha}, usuario='{usuario}'  agregar_gasto - main.py:559")
        gasto = Gasto(monto, motivo, fecha, usuario)
        self.gastos.append(gasto)
        print(f"[DEBUG] Gasto agregado. Total gastos en memoria: {len(self.gastos)}  agregar_gasto - main.py:562")
        self.guardar_gastos()
        print("[DEBUG] Gastos guardados en archivo  agregar_gasto - main.py:564")
        return True

    def obtener_gastos_fecha(self, fecha: datetime.date):
        """Obtiene gastos de una fecha específica"""
        gastos_fecha = [g for g in self.gastos if g.fecha == fecha]
        print(f"[DEBUG] obtener_gastos_fecha para {fecha}: encontrados {len(gastos_fecha)} gastos de {len(self.gastos)} totales  obtener_gastos_fecha - main.py:570")
        return gastos_fecha

    def obtener_gastos_periodo(self, fecha_desde: datetime.date, fecha_hasta: datetime.date):
        """Obtiene gastos en un período"""
        return [g for g in self.gastos if fecha_desde <= g.fecha <= fecha_hasta]

    def eliminar_gasto(self, gasto_index: int):
        """Elimina un gasto por índice"""
        if 0 <= gasto_index < len(self.gastos):
            del self.gastos[gasto_index]
            self.guardar_gastos()
            return True
        return False

    def buscar_producto(self, marca, descripcion, color, talle):
        for p in self.productos:
            if p.marca == marca and p.descripcion == descripcion and p.color == color and p.talle == talle:
                return p
        return None

    def cierre_caja(self, fecha):
        return [v for v in self.ventas if v.fecha == fecha]

    def archivar_ventas_dia(self, fecha):
        """Archiva las ventas del día en un archivo histórico y las elimina del día actual"""
        ventas_dia = self.cierre_caja(fecha)
        
        if not ventas_dia:
            return False
        
        # Crear archivo histórico si no existe
        archivo_historico = f"ventas_historico_{fecha.strftime('%Y')}.json"
        historico = []
        
        if os.path.exists(archivo_historico):
            with open(archivo_historico, "r", encoding="utf-8") as f:
                historico = json.load(f)
        
        # Agregar ventas del día al histórico
        for v in ventas_dia:
            historico.append({
                "descripcion": v.descripcion,
                "items": [
                    {
                        "producto": item["producto"].descripcion,
                        "marca": item["producto"].marca,
                        "color": item["producto"].color,
                        "talle": item["producto"].talle,
                        "cantidad": item["cantidad"],
                        "precio": item["precio"]
                    } for item in v.items
                ],
                "fecha": v.fecha.strftime("%Y-%m-%d"),
                "forma_pago": getattr(v, 'forma_pago', 'EFECTIVO'),
                "vendedor": getattr(v, 'vendedor', 'Sin especificar'),
                "cerrado": True
            })
        
        # Guardar histórico actualizado
        with open(archivo_historico, "w", encoding="utf-8") as f:
            json.dump(historico, f, ensure_ascii=False, indent=2)
        
        # Eliminar ventas del día del archivo actual
        self.ventas = [v for v in self.ventas if v.fecha != fecha]
        self.guardar_ventas()
        
        return True

    def archivar_gastos_dia(self, fecha):
        """Archiva gastos del día al histórico anual"""
        gastos_dia = self.obtener_gastos_fecha(fecha)
        if not gastos_dia:
            return
        
        archivo_historico = f"gastos_historico_{fecha.year}.json"
        historico = {}
        
        if os.path.exists(archivo_historico):
            with open(archivo_historico, "r", encoding="utf-8") as f:
                historico = json.load(f)
        
        fecha_str = fecha.strftime("%Y-%m-%d")
        historico[fecha_str] = {
            "gastos": [
                {
                    "monto": g.monto,
                    "motivo": g.motivo,
                    "usuario": g.usuario,
                    "timestamp": g.timestamp.isoformat()
                } for g in gastos_dia
            ],
            "total_gastos": sum(g.monto for g in gastos_dia)
        }
        
        with open(archivo_historico, "w", encoding="utf-8") as f:
            json.dump(historico, f, ensure_ascii=False, indent=2)
        
        # Remover gastos del día actual
        self.gastos = [g for g in self.gastos if g.fecha != fecha]
        self.guardar_gastos()

    def reporte_ventas(self, desde, hasta):
        return [v for v in self.ventas if desde <= v.fecha <= hasta]

    def reporte_ventas_por_marca(self, desde, hasta, marca):
        ventas = [v for v in self.ventas if desde <= v.fecha <= hasta]
        ventas_marca = []
        for v in ventas:
            for item in v.items:
                if hasattr(item['producto'], 'marca') and item['producto'].marca == marca:
                    ventas_marca.append({
                        'fecha': v.fecha,
                        'descripcion': v.descripcion,
                        'producto': item['producto'],
                        'cantidad': item['cantidad'],
                        'precio': item['precio']
                    })
        return ventas_marca

    def inventario_actual(self):
        return self.productos

    def actualizar_precio_producto(self, marca, descripcion, color, talle, nuevo_precio):
        prod = self.buscar_producto(marca, descripcion, color, talle)
        if prod:
            prod.actualizar_precio_costo(nuevo_precio)
            self.guardar_productos()
            return True
        return False

    def eliminar_producto(self, marca, descripcion, color, talle):
        self.productos = [p for p in self.productos if not (p.marca == marca and p.descripcion == descripcion and p.color == color and p.talle == talle)]
        self.guardar_productos()

    def eliminar_productos_masivo(self, lista_claves):
        # lista_claves: lista de tuplas (marca, descripcion, color, talle)
        self.productos = [p for p in self.productos if (p.marca, p.descripcion, p.color, p.talle) not in lista_claves]
        self.guardar_productos()

    def sugerencias_reposicion(self, umbral_stock=5, dias_analisis=30):
        """
        Devuelve una lista de productos que deberían reponerse según ventas recientes y stock bajo.
        - umbral_stock: stock mínimo recomendado
        - dias_analisis: días hacia atrás para analizar ventas
        """
        import datetime
        hoy = datetime.date.today()
        ventas_recientes = [v for v in self.ventas if (hoy - v.fecha).days <= dias_analisis]
        conteo = {}
        for v in ventas_recientes:
            for item in v.items:
                prod = item['producto']
                clave = (prod.marca, prod.descripcion, prod.color, prod.talle)
                conteo[clave] = conteo.get(clave, 0) + item['cantidad']
        sugerencias = []
        for p in self.productos:
            clave = (p.marca, p.descripcion, p.color, p.talle)
            ventas = conteo.get(clave, 0)
            if p.cantidad <= umbral_stock and ventas > 0:
                sugerencias.append({
                    'producto': p,
                    'stock': p.cantidad,
                    'vendidos': ventas
                })
        # Ordenar por más vendidos y menos stock
        sugerencias.sort(key=lambda x: (x['stock'], -x['vendidos']))
        return sugerencias

class AppPilchero(tk.Tk):
    def mostrar_venta(self):
        print("[DEBUG] mostrar_venta() llamado  restaurado - main.py:741")
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        self._chip_volver(self.mostrar_menu_principal)
        self._pantalla_venta(self.canvas_bg)

    def mostrar_ventas_dia(self):
        print("[DEBUG] mostrar_ventas_dia() llamado  restaurado - main.py:748")
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        self._chip_volver(self.mostrar_menu_principal)
        self._pantalla_ventas_dia(self.canvas_bg)
    def mostrar_actualizar_precio(self):
        print("[DEBUG] mostrar_actualizar_precio() redirigido a Inventario - main.py:754")
        # Compatibilidad hacia atrás: redirige al Inventario para modificar productos y precios
        self.mostrar_inventario()
    def __init__(self, sistema, session: SessionManager = None):
        print("[DEBUG] Iniciando AppPilchero.__init__ - main.py:758")
        super().__init__()
        self.sistema = sistema
        self.session = session
        self.title("KONTROL+ - Software de gestión By Alen.iA")
        self.geometry("1280x720")
        self.resizable(False, False)
        self.configure(bg=COLOR_FONDO)
        print("[DEBUG] Llamando a crear_widgets() desde __init__ - main.py:766")
        self.crear_widgets()

    def crear_widgets(self):
        print("[DEBUG] Entrando en crear_widgets() - main.py:770")
        self.canvas_bg = tk.Canvas(self, width=1280, height=720, highlightthickness=0, bd=0)
        self.canvas_bg.place(x=0, y=0, relwidth=1, relheight=1)
        # Crear el fondo con etiquetas para poder identificarlo y preservarlo
        for i in range(0, 720, 2):
            color = self._interpolar_color(COLOR_GRADIENTE_1, COLOR_GRADIENTE_2, i/720)
            self.canvas_bg.create_rectangle(0, i, 1280, i+2, outline="", fill=color, tags="fondo_{}".format(i))
        self.canvas_bg.lower("all")
        self.pantalla_widgets = []
        self.mostrar_menu_principal()

    def _colocar_logo(self, pantalla_principal=True):
        # Elimina logo anterior si existe
        if hasattr(self, 'logo_canvas_id') and self.logo_canvas_id:
            self.canvas_bg.delete(self.logo_canvas_id)
            self.logo_canvas_id = None
        
        if pantalla_principal:
            # PANTALLA PRINCIPAL: Usar LOGO APP.png (SIN MODIFICAR)
            import sys, os
            if hasattr(sys, '_MEIPASS'):
                logo_path = os.path.join(sys._MEIPASS, "LOGO_APP.png") # type: ignore
            else:
                logo_path = "screenshot/LOGO_APP.png"
            try:
                from PIL import Image, ImageTk
                logo_img = Image.open(logo_path).convert("RGBA")
                orig_w, orig_h = logo_img.size
                self.update_idletasks()  # Forzar update para obtener tamaño real
                w = self.winfo_width() or 1200
                h = self.winfo_height() or 1000
                max_w = int(w * 0.65)
                max_h = int(h * 0.42)
                # Mantener proporción
                scale = min(max_w / orig_w, max_h / orig_h)
                new_w = int(orig_w * scale)
                new_h = int(orig_h * scale)
                logo_img = logo_img.resize((new_w, new_h), Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS) # type: ignore
                self.logo_tk = ImageTk.PhotoImage(logo_img)
                pos_x = w // 2
                pos_y = int(h * 0.08)
                self.logo_canvas_id = self.canvas_bg.create_image(pos_x, pos_y, image=self.logo_tk, anchor="n")
                self.canvas_bg.tag_raise(self.logo_canvas_id)
            except Exception as e:
                print(f"[DEBUG] Error cargando logo principal: {e} - Ruta: {logo_path}")
                self.logo_canvas_id = self.canvas_bg.create_text(self.winfo_width()//2, 40, text="[LOGO]", font=("Orbitron", 32, "bold"), fill=COLOR_CIAN, anchor="n")
        else:
            # PANTALLAS SECUNDARIAS: Usar 7.PNG con transparencia y centrado
            self._colocar_logo_secundarias()

    def _colocar_logo_secundarias(self):
        """Coloca el logo 7.PNG en pantallas secundarias con transparencia y centrado"""
        try:
            from PIL import Image, ImageTk
            import os, sys
            logo_path = os.path.join(sys._MEIPASS, "7.png") if hasattr(sys, "_MEIPASS") else "7.png"
            
            if os.path.exists(logo_path):
                # Cargar imagen con transparencia
                logo_img = Image.open(logo_path).convert("RGBA")
                
                # Redimensionar el logo manteniendo proporción (reducido 10% adicional: 170 * 0.9 = 153)
                logo_width = 153  # Reducido un 10% adicional desde 170
                logo_height = int(logo_img.height * (logo_width / logo_img.width))
                
                # Si es muy alto, ajustar por altura máxima
                if logo_height > 76:  # Reducido proporcionalmente (85 * 0.9)
                    logo_height = 115  # Reducido desde 128 (128 * 0.9)
                    logo_width = int(logo_img.width * (logo_height / logo_img.height))
                
                # Redimensionar con alta calidad (compatibilidad con versiones de Pillow)
                try:
                    resample_filter = Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS
                except Exception:
                    resample_filter = Image.ANTIALIAS
                logo_resized = logo_img.resize((logo_width, logo_height), resample_filter)
                
                # Convertir a PhotoImage manteniendo transparencia
                self.logo_tk_secundaria = ImageTk.PhotoImage(logo_resized)
                
                # Colocar en el canvas centrado en la parte superior (subido 3mm ≈ 8px)
                self.logo_canvas_id = self.canvas_bg.create_image(
                    640, 12,  # Centrado horizontalmente, margen superior reducido (subido 8px)
                    image=self.logo_tk_secundaria, 
                    anchor="n"
                )
                
                # Asegurar que el logo esté al frente
                self.canvas_bg.tag_raise(self.logo_canvas_id)
                
            else:
                # Fallback si no encuentra el archivo
                print(f"[DEBUG] Logo 7.png no encontrado en: {logo_path}")
                self.logo_canvas_id = self.canvas_bg.create_text(
                    640, 30, 
                    text="ALEN.IA", 
                    font=("Orbitron", 20, "bold"), 
                    fill=COLOR_CIAN, 
                    anchor="n"
                )
                
        except Exception as e:
            print(f"[INFO] Error al cargar logo 7.PNG en pantalla secundaria: {e} - main.py:870")
            # Fallback texto
            self.logo_canvas_id = self.canvas_bg.create_text(
                640, 30, 
                text="ALEN.IA", 
                font=("Orbitron", 20, "bold"), 
                fill=COLOR_CIAN, 
                anchor="n"
            )

    def _colocar_logo_panel_ia(self):
        """Coloca el logo ALENRESULTADOS.PNG específicamente para el Panel IA"""
        try:
            from PIL import Image, ImageTk
            import os, sys
            logo_path = os.path.join(sys._MEIPASS, "ALENRESULTADOS.png") if hasattr(sys, "_MEIPASS") else "ALENRESULTADOS.png"
            
            if os.path.exists(logo_path):
                # Cargar imagen con transparencia
                logo_img = Image.open(logo_path).convert("RGBA")
                
                # Redimensionar el logo manteniendo proporción (tamaño profesional para Panel IA)
                logo_width = 200  # Tamaño apropiado para el panel IA
                logo_height = int(logo_img.height * (logo_width / logo_img.width))
                
                # Si es muy alto, ajustar por altura máxima
                if logo_height > 100:
                    logo_height = 100
                    logo_width = int(logo_img.width * (logo_height / logo_img.height))
                
                # Redimensionar con alta calidad
                try:
                    resample_filter = Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS
                except Exception:
                    resample_filter = Image.ANTIALIAS
                logo_resized = logo_img.resize((logo_width, logo_height), resample_filter)
                
                # Convertir a PhotoImage manteniendo transparencia
                self.logo_tk_panel_ia = ImageTk.PhotoImage(logo_resized)
                
                # Colocar en el canvas centrado en la parte superior
                self.logo_canvas_id = self.canvas_bg.create_image(
                    640, 20,  # Centrado horizontalmente, margen superior
                    image=self.logo_tk_panel_ia, 
                    anchor="n"
                )
                
                # Asegurar que el logo esté al frente
                self.canvas_bg.tag_raise(self.logo_canvas_id)
            else:
                # Fallback: usar texto si no existe ALENRESULTADOS.png
                print(f"[DEBUG] No se encontró ALENRESULTADOS.png - main.py:921")
                self.logo_canvas_id = self.canvas_bg.create_text(640, 60, text="ALENIA RESULTADOS", font=("Montserrat", 18, "bold"), fill="#00a316", anchor="center")
                
        except Exception as e:
            print(f"[DEBUG] Error cargando logo Panel IA: {e} - main.py:925")
            # Fallback texto si no se puede cargar la imagen
            self.logo_canvas_id = self.canvas_bg.create_text(640, 60, text="ALENIA RESULTADOS", font=("Montserrat", 18, "bold"), fill="#00a316", anchor="center")

    def _interpolar_color(self, color1, color2, t): # type: ignore
        # Interpola dos colores hex en t (0-1)
        c1 = tuple(int(color1[i:i+2], 16) for i in (1, 3, 5))
        c2 = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))
        c = tuple(int(c1[j] + (c2[j] - c1[j]) * t) for j in range(3))
        return f'#{c[0]:02x}{c[1]:02x}{c[2]:02x}'

    # Métodos stub para evitar errores si no existen
    def mostrar_inventario(self): # type: ignore
        print("[DEBUG] mostrar_inventario() llamado - main.py:938")
        if not self.require_role(["admin"]):
            return
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        self._chip_volver(self.mostrar_menu_secundario)
        self._chip_logout()
        self._pantalla_inventario(self.canvas_bg)

    def limpiar_pantalla(self):
        # Elimina todos los widgets de la pantalla y limpia referencias
        for w in getattr(self, 'pantalla_widgets', []):
            try:
                w.destroy()
            except Exception:
                pass
        self.pantalla_widgets = []
        
        # Elimina solo el logo si existe
        if hasattr(self, 'logo_canvas_id') and self.logo_canvas_id:
            self.canvas_bg.delete(self.logo_canvas_id)
            self.logo_canvas_id = None
        
        # Guarda las referencias de los rectángulos del fondo (gradiente)
        fondo = []
        for i in range(0, 720, 2):
            rect_id = self.canvas_bg.find_withtag("fondo_{}".format(i))
            if rect_id:
                fondo.extend(rect_id)
        
        # Elimina todos los elementos canvas excepto el fondo
        for item in self.canvas_bg.find_all():
            if item not in fondo:
                self.canvas_bg.delete(item)
                
        # Redibuja el gradiente si es necesario
        if not fondo:
            for i in range(0, 720, 2):
                color = self._interpolar_color(COLOR_GRADIENTE_1, COLOR_GRADIENTE_2, i/720)
                rect_id = self.canvas_bg.create_rectangle(0, i, 1280, i+2, outline="", fill=color, tags="fondo_{}".format(i))
        
        # Asegura que el gradiente siempre esté al fondo
        self.canvas_bg.lower("all")

    def mostrar_menu_principal(self):
        print("[DEBUG] mostrar_menu_principal() llamado - main.py:981")
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=True)
        
        # Botones con tooltips informativos
        btns_data = [
            ("💰 Venta", self.mostrar_venta, "Registrar nueva venta - Agregar productos al carrito y procesar pagos"),
            ("📊 Ventas del Día", self.mostrar_ventas_dia, "Ver resumen de ventas del día actual - Control de ingresos diarios"),
            ("⚙️ Menú Gestión", self.mostrar_menu_secundario, "Acceder a herramientas de gestión - Productos, precios e inventario"),
        ]
        
        btn_w, btn_h = 360, 68
        sep_y, sep_h = 20, 350
        y0 = 250
        
        for i, (txt, cmd, tooltip) in enumerate(btns_data):
            b = tk.Button(self.canvas_bg, text=txt, font=("Montserrat", 15, "bold"), 
                         bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, bd=0, relief="flat", 
                         activebackground="#7c5eff", activeforeground=COLOR_BOTON_TEXTO, 
                         cursor="hand2", command=cmd)
            
            # Aplicar estilo moderno
            aplicar_estilo_moderno_boton(b, "primario", hover_efecto=True)
            
            # Agregar tooltip informativo
            crear_tooltip(b, tooltip)
            
            win = self.canvas_bg.create_window(650, y0+i*(btn_h+sep_y), window=b, width=btn_w, height=btn_h, anchor="n")
            
            # Crear efecto de sombra sutil
            try:
                # Simular sombra con un rectángulo de fondo
                self.canvas_bg.create_rectangle(
                    650 - btn_w//2 + 3, y0+i*(btn_h+sep_y) + 3, 
                    650 + btn_w//2 + 3, y0+i*(btn_h+sep_y) + btn_h + 3,
                    fill="#00000020", outline="", width=0, tags="sombra_boton"
                )
                # Mover la sombra detrás del botón
                self.canvas_bg.tag_lower("sombra_boton")
            except:
                pass
            
            self.pantalla_widgets.append(b)

    def mostrar_menu_secundario(self):
        print("[DEBUG] mostrar_menu_secundario() llamado - main.py:1026")
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        self._chip_logout()
        
        # Título del menú (ajustado para el nuevo logo)
        lbl_titulo = tk.Label(self.canvas_bg, text="MENÚ ", font=("Montserrat", 20, "bold"), 
                             bg=COLOR_FONDO, fg=COLOR_CIAN)
        aplicar_estilo_moderno_label(lbl_titulo, "titulo")
        self.canvas_bg.create_window(1160, 80, window=lbl_titulo, anchor="center")  # Ajustado para el logo

        # --- NUEVA DISTRIBUCIÓN EN DOS COLUMNAS ---
        # Configuración de botones y layout dinámico (sin tocar logos ni botones Volver)
        self.update_idletasks()
        canvas_w = self.winfo_width() or 1280
        canvas_h = self.winfo_height() or 720

        btn_w, btn_h = 320, 70
        font_btn = ("Montserrat", 18, "bold")
        sep_y = 28

        # Posiciones de columnas centradas y con margen lateral
        gap_x = max(100, int(canvas_w * 0.09375))  # ≈120 px en 1280
        col1_x = canvas_w//2 - (btn_w//2 + gap_x//2)
        col2_x = canvas_w//2 + (btn_w//2 + gap_x//2)

        # Punto de inicio vertical por debajo del logo secundario
        try:
            logo_h = self.logo_tk_secundaria.height()
        except Exception:
            logo_h = 0
        y0 = max(180, 12 + logo_h + 48)

        # Botones columna izquierda
        col1 = [
            ("Agregar Producto", self.mostrar_alta_producto, "#e89c2c", "Dar de alta nuevos productos - Configurar marca, descripción, precios y stock"),
            ("Carga Masiva", self.carga_masiva_productos, "#e89c2c", "Importar productos desde archivo CSV - Carga rápida de múltiples productos"),
            ("Modificar Producto", self.mostrar_inventario, "#e89c2c", "Modificar productos y precios desde Inventario"),
        ]
        # Ocultar columna izquierda completa para vendedores (solo ADMIN)
        if not (self.session and self.session.is_admin()):
            col1 = []
        # Botones columna derecha
        col2 = [
            ("Ver Inventario", self.mostrar_inventario, "primario", "Consultar inventario actual - Stock, precios y datos de productos"),
            ("Reportes", self.mostrar_reportes, "primario", "Generar reportes de ventas - Análisis por fechas, productos y formas de pago"),
        ]
        # Mostrar extras solo para admin
        if self.session and self.session.is_admin():
            col2.append(("Crear Ofertas", self.mostrar_crear_ofertas, "primario", "Gestionar ofertas y promociones - Descuentos y ofertas especiales"))
            col2.append(("Gestión de Usuarios", self.mostrar_gestion_usuarios, "primario", "Administrar usuarios: crear, activar/desactivar, cambiar roles y contraseñas"))
        else:
            # Si no es admin, remover 'Ver Inventario'
            col2 = [item for item in col2 if item[0] != "Ver Inventario"]

        # Crear botones columna izquierda (naranja)
        for i, (txt, cmd, tipo, tooltip) in enumerate(col1):
            b = tk.Button(self.canvas_bg, text=txt, font=font_btn,
                         bg="#e89c2c", fg="#ffffff", bd=0, relief="flat",
                         cursor="hand2", command=cmd)
            # Forzar color naranja y tipo primario para efectos
            aplicar_estilo_moderno_boton(b, "warning", hover_efecto=True)
            crear_tooltip(b, tooltip)
            y = y0 + i * (btn_h + sep_y)
            self.canvas_bg.create_window(col1_x, y, window=b, width=btn_w, height=btn_h, anchor="center")
            # Sombra
            try:
                self.canvas_bg.create_rectangle(
                    col1_x - btn_w//2 + 2, y - btn_h//2 + 2,
                    col1_x + btn_w//2 + 2, y + btn_h//2 + 2,
                    fill="#00000015", outline="", width=0, tags="sombra_menu")
                self.canvas_bg.tag_lower("sombra_menu")
            except:
                pass
            self.pantalla_widgets.append(b)

        # Crear botones columna derecha (color primario)
        for i, (txt, cmd, tipo, tooltip) in enumerate(col2):
            b = tk.Button(self.canvas_bg, text=txt, font=font_btn,
                         bg=COLOR_BOTON, fg="#ffffff", bd=0, relief="flat",
                         cursor="hand2", command=cmd)
            aplicar_estilo_moderno_boton(b, tipo, hover_efecto=True)
            crear_tooltip(b, tooltip)
            y = y0 + i * (btn_h + sep_y)
            self.canvas_bg.create_window(col2_x, y, window=b, width=btn_w, height=btn_h, anchor="center")
            # Sombra
            try:
                self.canvas_bg.create_rectangle(
                    col2_x - btn_w//2 + 2, y - btn_h//2 + 2,
                    col2_x + btn_w//2 + 2, y + btn_h//2 + 2,
                    fill="#00000015", outline="", width=0, tags="sombra_menu")
                self.canvas_bg.tag_lower("sombra_menu")
            except:
                pass
            self.pantalla_widgets.append(b)

        # --- BOTÓN PANEL INTELIGENTE DE Alen.iA ---
        btn_ia = tk.Button(
            self.canvas_bg,
            text="PANEL INTELIGENTE DE Alen.iA",
            font=font_btn,
            bg=COLOR_BOTON_SUCCESS,
            fg="#ffffff",
            bd=0,
            relief="flat",
            cursor="hand2",
            command=self.mostrar_centro_ia
        )
        aplicar_estilo_moderno_boton(btn_ia, "success", hover_efecto=True)
        crear_tooltip(btn_ia, "Centro de inteligencia artificial - Análisis predictivo y sugerencias")
        y_ia = y0 + max(len(col1), len(col2)) * (btn_h + sep_y) + 20
        self.canvas_bg.create_window((col1_x + col2_x)//2, y_ia, window=btn_ia, width=col2_x-col1_x+btn_w, height=btn_h, anchor="center")
        # Sombra para el botón IA
        try:
            self.canvas_bg.create_rectangle(
                (col1_x + col2_x)//2 - (col2_x-col1_x+btn_w)//2 + 2, y_ia - btn_h//2 + 2,
                (col1_x + col2_x)//2 + (col2_x-col1_x+btn_w)//2 + 2, y_ia + btn_h//2 + 2,
                fill="#00000015", outline="", width=0, tags="sombra_menu")
            self.canvas_bg.tag_lower("sombra_menu")
        except:
            pass
        self.pantalla_widgets.append(btn_ia)

        # Barra superior estándar con título y volver
        # Usar chip de Volver también aquí si aplica (no bloquea logo)
        self._chip_volver(self.mostrar_menu_principal)
        self.pantalla_widgets.extend([lbl_titulo])

    def mostrar_centro_ia(self):
        """Centro de Inteligencia Artificial - Versión Optimizada Visual"""
        print("[DEBUG] mostrar_centro_ia() OPTIMIZADO VISUAL llamado - main.py:1153")
        self.limpiar_pantalla()
        
        # Usar logo especial para Panel IA (ALENRESULTADOS.png)
        if hasattr(self, 'logo_canvas_id') and self.logo_canvas_id:
            self.canvas_bg.delete(self.logo_canvas_id)
            self.logo_canvas_id = None
        self._colocar_logo_panel_ia()
        
        widgets = []
        
        # --- HEADER PRINCIPAL MODERNO ---
        # Crear gradiente de fondo para el header
        header_frame = tk.Frame(self.canvas_bg, bg="#062091", relief="flat", bd=0)
        self.canvas_bg.create_window(640, 90, window=header_frame, width=1240, height=90, anchor="center")
        
        # --- PANEL DE NAVEGACIÓN MODERNO ---
        frame_nav = tk.Frame(self.canvas_bg, bg="#1a3d75", relief="flat", bd=1)
        self.canvas_bg.create_window(640, 160, window=frame_nav, width=1120, height=100, anchor="center")
        
        # Agregar sombra visual al panel de navegación
        shadow_frame = tk.Frame(self.canvas_bg, bg="#1a3d75", relief="flat", bd=0)
        self.canvas_bg.create_window(642, 162, window=shadow_frame, width=1122, height=72, anchor="center")
        self.canvas_bg.tag_lower(shadow_frame)
        
        # Variable para controlar la vista activa
        self.vista_ia_activa = tk.StringVar(value="dashboard")
        
        # Botones de navegación con diseño moderno y espaciado mejorado
        nav_buttons = [
            ("📊 Dashboard", "dashboard", "#00B4D8", "#0077B6"),
            ("📦 Reposición", "reposicion", "#38A169", "#2F855A"),
            ("💰 Precios", "precios", "#F6AD55", "#ED8936"),
            ("📈 Análisis", "analisis", "#9F7AEA", "#805AD5"),
            ("📤 Exportar", "exportar", "#718096", "#4A5568"),
            ("🔄 Actualizar", "actualizar", "#3182CE", "#2C5282")
        ]
        
        x_start = 40
        button_width = 180
        button_spacing = 180
        
        for i, (text, action, bg_color, hover_color) in enumerate(nav_buttons):
            x_pos = x_start + (i * button_spacing)
            
            if action == "exportar":
                command = self._exportar_centro_ia
            elif action == "actualizar":
                command = self._actualizar_centro_ia
            else:
                command = lambda a=action: self._cambiar_vista_ia(a)
            
            btn = tk.Button(frame_nav, 
                           text=text, 
                           font=("Montserrat", 11, "bold"), 
                           bg=bg_color, 
                           fg="#ffffff", 
                           bd=0, 
                           relief="flat", 
                           cursor="hand2",
                           command=command,
                           pady=8,
                           padx=12)
            btn.place(x=x_pos, y=18, width=button_width, height=35)
            
            # Efectos hover mejorados
            def on_enter(e, btn=btn, color=hover_color):
                btn.config(bg=color, relief="raised", bd=1)
            def on_leave(e, btn=btn, color=bg_color):
                btn.config(bg=color, relief="flat", bd=0)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
        
        # --- ÁREA DE CONTENIDO DINÁMICO CON MEJOR ESPACIADO ---
        content_frame = tk.Frame(self.canvas_bg, bg="#0f172a", relief="flat", bd=1)
        self.canvas_bg.create_window(640, 480, window=content_frame, width=1200, height=560, anchor="center")
        
        # Frame interno para contenido con padding
        self.frame_contenido_ia = tk.Frame(content_frame, bg=COLOR_FONDO)
        self.frame_contenido_ia.place(x=10, y=10, width=1180, height=540)
        
        # Cargar vista inicial
        self._cambiar_vista_ia("dashboard")
        
        # Chip volver con posición optimizada
        self._chip_volver(self.mostrar_menu_secundario, x=1150, y=25)
        
        widgets.extend([header_frame, shadow_frame, frame_nav, content_frame])
        self.pantalla_widgets.extend(widgets)

    def mostrar_cierre_caja(self):
        print("[DEBUG] mostrar_cierre_caja() llamado - main.py:1245")
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        self._chip_volver(self.mostrar_menu_principal)
        self._pantalla_cierre_caja(self.canvas_bg)

    def mostrar_alta_producto(self):
        print("[DEBUG] mostrar_alta_producto() llamado - main.py:1252")
        if not self.require_role(["admin"]):
            return
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        self._chip_volver(self.mostrar_menu_secundario)
        self._chip_logout()
        self._pantalla_alta_producto(self.canvas_bg)

    def mostrar_menu_principal(self):
        print("[DEBUG] mostrar_menu_principal() llamado - main.py:1262")
        self.limpiar_pantalla()
        self._chip_logout()
        # Colocar logo reutilizando el método estándar (maneja rutas y empaquetado)
        self._colocar_logo(pantalla_principal=True)

        # --- BOTONES PRINCIPALES ---
        # Colores exactos de la imagen
        COLOR_VERDE = "#00a316"
        COLOR_PURPURA = "#5000a3"
        COLOR_NARANJA = "#05509e"
        COLOR_GRIS = "#163d5a"

        # Medidas y posiciones dinámicas para aprovechar el espacio sin superponer elementos
        self.update_idletasks()
        canvas_w = self.winfo_width() or 1280
        canvas_h = self.winfo_height() or 720

        # Ubicación vertical de los botones: inmediatamente debajo del logo existente
        try:
            logo_top_y = pos_y  # definido arriba al colocar el logo
            logo_h = self.logo_tk.height()
        except Exception:
            logo_top_y = 70
            logo_h = 0
        btn_y = max(int(logo_top_y + logo_h + 30), int(canvas_h * 0.35))
        # Bajar fila de botones 2.5 cm (~95 px)
        btn_y += 95

        btn_w = 350  # mantenemos tamaños para respetar identidad visual
        btn_h = 150

        # Márgenes y separación horizontales calculados para centrar y no pegarse a los bordes
        margin_x = max(60, int(canvas_w * 0.066))  # ≈85 px en 1280
        offset = btn_w + int((canvas_w - (2 * margin_x + 3 * btn_w)) / 2)
        center_x = canvas_w // 2
        left_x = center_x - offset
        mid_x = center_x
        right_x = center_x + offset

        # NUEVA VENTA (izquierda)
        btn_nueva_venta = tk.Button(self.canvas_bg, text="NUEVA\nVENTA", font=("Montserrat", 26, "bold"),
                                    bg=COLOR_PURPURA, fg="#ffffff", bd=0, relief="flat", cursor="hand2", 
                                    command=self.mostrar_venta, activebackground=COLOR_PURPURA  , activeforeground="#ffffff")
        aplicar_estilo_moderno_boton(btn_nueva_venta, "primario", hover_efecto=True)
        btn_nueva_venta.config(bg=COLOR_PURPURA, activebackground="#0ea866")
        self.canvas_bg.create_window(left_x, btn_y, window=btn_nueva_venta, width=btn_w, height=btn_h, anchor="n")

        # VENTAS  (centro) DEL DÍA (centro abajo) 
        btn_ventas_dia = tk.Button(self.canvas_bg, text="VENTAS\nDEL DÍA", font=("Montserrat", 26, "bold"),
                                   bg=COLOR_NARANJA, fg="#ffffff", bd=0, relief="flat", cursor="hand2", 
                                   command=self.mostrar_ventas_dia, activebackground=COLOR_NARANJA, activeforeground="#ffffff")
        aplicar_estilo_moderno_boton(btn_ventas_dia, "warning", hover_efecto=True)
        btn_ventas_dia.config(bg=COLOR_NARANJA, activebackground="#c97b20")
        self.canvas_bg.create_window(mid_x, btn_y, window=btn_ventas_dia, width=btn_w, height=btn_h, anchor="n")

        # MENÚ (derecha)
        btn_menu = tk.Button(self.canvas_bg, text="MENÚ", font=("Montserrat", 26, "bold"),
                             bg=COLOR_GRIS, fg="#ffffff", bd=0, relief="flat", cursor="hand2", 
                             command=self.mostrar_menu_secundario, activebackground=COLOR_GRIS, activeforeground="#ffffff")
        aplicar_estilo_moderno_boton(btn_menu, "secundario", hover_efecto=True)
        btn_menu.config(bg=COLOR_GRIS, activebackground="#555555")
        self.canvas_bg.create_window(right_x, btn_y, window=btn_menu, width=btn_w, height=btn_h, anchor="n")

        # Sombra moderna sutil para cada botón (elevación)
        try:
            for x_center, _btn in [(left_x, btn_nueva_venta), (mid_x, btn_ventas_dia), (right_x, btn_menu)]:
                for i in range(3):
                    offset_i = 3 + i*2
                    opacity = 25 - i*5  # Disminuye opacidad gradualmente
                    if opacity > 0:
                        sombra_actual = f"#000000{opacity:02x}"
                    else:
                        sombra_actual = "#00000000"
                    self.canvas_bg.create_rectangle(
                        x_center - btn_w//2 + offset_i,
                        btn_y + offset_i,
                        x_center + btn_w//2 + offset_i,
                        btn_y + btn_h + offset_i,
                        fill=sombra_actual, outline="", width=1, 
                        tags="sombra_boton"
                    )
            self.canvas_bg.tag_lower("sombra_boton")
        except Exception as e:
            print(f"Error al crear sombra: {e} - main.py:1368")

        # Tooltips
        crear_tooltip(btn_nueva_venta, "Registrar nueva venta - Agregar productos al carrito y procesar pagos")
        crear_tooltip(btn_ventas_dia, "Ver resumen de ventas del día actual - Control de ingresos diarios")
        crear_tooltip(btn_menu, "Acceder a herramientas de gestión - Productos, precios e inventario")

        # Agregar íconos reales a los botones principales (si existen archivos PNG)
        agregar_icono_a_boton(btn_nueva_venta, "screenshot/iconos/icoNUEVAVENTA.png", (105, 105))
        agregar_icono_a_boton(btn_ventas_dia, "screenshot/iconos/icoVENTAS DEL DÍA.png", (95, 95))
        agregar_icono_a_boton(btn_menu, "screenshot/iconos/icoMenú.png", (95, 95))

        self.pantalla_widgets.extend([btn_nueva_venta, btn_ventas_dia, btn_menu])

        # --- LOGO PEQUEÑO Y TEXTO DE VERSIÓN EN ESQUINA INFERIOR DERECHA ---
        try:
            from PIL import Image, ImageTk
            import os, sys
            
            # Buscar ALENRESULTADOS.png con manejo de rutas para ejecutable
            if hasattr(sys, '_MEIPASS'):
                logo_chico_path = os.path.join(sys._MEIPASS, "ALENRESULTADOS.png")
            else:
                logo_chico_path = "screenshot/ALENRESULTADOS.png"
            
            if os.path.exists(logo_chico_path):
                logo_chico_img = Image.open(logo_chico_path).convert("RGBA")
                # Mantener proporción del logo chico: fijar altura y escalar ancho
                orig_w, orig_h = logo_chico_img.size
                target_h = 38
                target_w = int(orig_w * (target_h / orig_h))
                try:
                    resample_filter = Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS
                except Exception:
                    resample_filter = Image.ANTIALIAS
                logo_chico_img = logo_chico_img.resize((target_w, target_h), resample_filter)
                self.logo_chico_tk = ImageTk.PhotoImage(logo_chico_img)
                self.logo_chico_canvas_id = self.canvas_bg.create_image(1152, 705, image=self.logo_chico_tk, anchor="sw")
            else:
                print(f"[DEBUG] Logo chico no encontrado: {logo_chico_path}")
                self.logo_chico_canvas_id = self.canvas_bg.create_text(1152, 690, text="[LOGO]", font=("Montserrat", 10, "bold"), fill="#19c37d", anchor="sw")
        except Exception as e:
            print(f"[DEBUG] Error cargando logo chico: {e}")
            self.logo_chico_canvas_id = self.canvas_bg.create_text(1152, 690, text="[LOGO]", font=("Montserrat", 10, "bold"), fill="#19c37d", anchor="sw")

        self.version_text_id = self.canvas_bg.create_text(10, 710, text="Versión: 3.0 / Un servicio de Alen.iA / RESULTADOS CON INTELIGENCIA", anchor="sw", font=("Montserrat", 12, "bold"), fill="#ffffff")
        
        # No es necesario agregar más widgets, ya se agregaron los botones principales anteriormente

    def formato_moneda(self, valor):
        try:
            if isinstance(valor, str):
                cleaned = valor.replace("$", "").replace(".", "").replace(",", ".").strip()
                valor_num = float(cleaned) if cleaned else 0.0
            else:
                valor_num = float(valor)
        except Exception:
            return "$0"
        entero = int(round(valor_num))
        signo = "-" if entero < 0 else ""
        miles = f"{abs(entero):,}".replace(",", ".")
        return f"{signo}${miles}"

    def _norm_pago(self, s: str) -> str:
        try:
            mapa = str.maketrans({"Á":"A","É":"E","Í":"I","Ó":"O","Ú":"U","á":"A","é":"E","í":"I","ó":"O","ú":"U"})
            return (s or "").translate(mapa).upper().strip()
        except Exception:
            return (s or "").upper().strip()

    # Pantallas adaptadas para navegación interna
    def _pantalla_venta(self, parent):
        """Pantalla de ventas optimizada con diseño moderno y profesional"""
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        
        # === BOTÓN VOLVER ESPECÍFICO PARA NUEVA VENTA ===
        btn_volver_venta = tk.Button(self.canvas_bg, text="← VOLVER", font=("Montserrat", 12, "bold"),
                                    bg=COLOR_BOTON_DANGER, fg="#ffffff", bd=2, relief="raised",
                                    cursor="hand2", command=self.mostrar_menu_principal, pady=8, padx=15)
        aplicar_estilo_moderno_boton(btn_volver_venta, "danger", hover_efecto=True)
        crear_tooltip(btn_volver_venta, "Volver al menú principal")
        
        # Posicionar en esquina superior izquierda, debajo del logo
        btn_volver_id = self.canvas_bg.create_window(40, 20, window=btn_volver_venta, width=120, height=40, anchor="nw")
        self.canvas_bg.tag_raise(btn_volver_id)
        self.pantalla_widgets.extend([btn_volver_venta, btn_volver_id])
        
        widgets = []
        carrito = []
        productos = self.sistema.inventario_actual()
        opciones = [f"{p.marca} | {p.descripcion} | {p.color} | {p.talle} | Stock: {p.cantidad}" for p in productos]
        precios = {f"{p.marca} | {p.descripcion} | {p.color} | {p.talle} | Stock: {p.cantidad}": p.precio_venta for p in productos}
        productos_dict = {f"{p.marca} | {p.descripcion} | {p.color} | {p.talle} | Stock: {p.cantidad}": p for p in productos}
        
        # === TÍTULO PRINCIPAL ===
        titulo_frame = tk.Frame(self.canvas_bg, bg=COLOR_FONDO)
        self.canvas_bg.create_window(158, 120, window=titulo_frame, anchor="center")
        
        lbl_titulo_principal = tk.Label(titulo_frame, text="NUEVA VENTA", 
                                       font=("Montserrat", 24, "bold"), bg=COLOR_FONDO, fg="#00c9df")
        lbl_titulo_principal.pack()
        
        # === PANEL DE ENTRADA DE DATOS (IZQUIERDA) ===
        panel_entrada = tk.Frame(self.canvas_bg, bg="#1a3d75", bd=2, relief="solid")
        self.canvas_bg.create_window(40, 140, window=panel_entrada, width=580, height=420, anchor="nw")
        
        # Marco decorativo para el panel
        marco_entrada = tk.Frame(panel_entrada, bg="#00c9df", height=4)
        marco_entrada.pack(fill="x", pady=(0, 10))
        
        # Título del panel
        lbl_titulo_entrada = tk.Label(panel_entrada, text="1° CARGÁ EL PRODUCTO ", 
                                     font=("Montserrat", 16, "bold"), bg="#1a3d75", fg="#e5e7eb")
        lbl_titulo_entrada.pack(pady=(10, 15))
        
        # === PRODUCTO SELECTOR ===
        frame_producto = tk.Frame(panel_entrada, bg="#1a3d75")
        frame_producto.pack(fill="x", padx=20, pady=(0, 15))
        
        lbl_prod = tk.Label(frame_producto, text="Producto:", font=("Montserrat", 14, "bold"), 
                           bg="#1a3d75", fg="#e5e7eb")
        lbl_prod.pack(anchor="w", pady=(0, 5))
        
        producto_var = tk.StringVar()
        combo = ttk.Combobox(frame_producto, textvariable=producto_var, values=opciones, 
                            font=("Montserrat", 11), state="normal", height=8)
        aplicar_estilo_moderno_combobox(combo)
        crear_tooltip(combo, "🔍 Escriba para buscar productos\n• Dropdown se abre automáticamente con sugerencias\n• Siga escribiendo para filtrar más\n• Haga clic para seleccionar el producto deseado\n• Enter: Seleccionar primer resultado • Escape: Limpiar")
        combo.pack(fill="x", ipady=6)
        
        # Sistema de sugerencias optimizado - Mantiene el foco en el campo
        def on_keyrelease(event):
            """Filtrado inteligente SIN perder el foco - Permite escribir continuamente"""
            # Evitar procesar teclas de navegación y control
            if event.keysym in ["Return", "Tab", "Up", "Down", "Left", "Right", "Home", "End", 
                               "Page_Up", "Page_Down", "Control_L", "Control_R", "Alt_L", "Alt_R",
                               "Shift_L", "Shift_R", "Caps_Lock", "Escape"]:
                return
            
            value = combo.get().lower().strip()
            
            # Si el campo está vacío, mostrar todas las opciones
            if not value:
                combo['values'] = opciones
                return
            
            # Filtrar productos que coincidan con la búsqueda
            # Busca en marca, descripción, color y talle
            filtered = []
            for opcion in opciones:
                opcion_lower = opcion.lower()
                # Coincidencia exacta tiene prioridad
                if value in opcion_lower:
                    filtered.append(opcion)
            
            # SOLO actualizar las opciones disponibles
            combo['values'] = filtered if filtered else opciones
            
            # NO generar eventos que abran dropdown - el usuario puede usar Alt+Down si necesita
        
        # Manejar selección del dropdown
        def on_combobox_select(event):
            """Cuando el usuario selecciona un producto del dropdown"""
            seleccion = combo.get()
            if seleccion and seleccion in productos_dict:
                # Cargar precio automáticamente al seleccionar
                set_precio_venta()
                # Enfocar el siguiente campo (cantidad)
                ent_cantidad.focus_set()
                print(f"[DEBUG] Producto seleccionado: {seleccion}  on_combobox_select - main.py:1518")
        
        # Navegación con teclado mejorada
        def on_key_press(event):
            """Manejo de teclas especiales en el combobox"""
            if event.keysym == "Return":
                # Enter: seleccionar el primer resultado si hay coincidencias
                current_values = combo['values']
                if current_values and len(current_values) > 0:
                    combo.set(current_values[0])
                    on_combobox_select(event)
                return "break"
            elif event.keysym == "Escape":
                # Escape: limpiar búsqueda
                combo.set("")
                combo['values'] = opciones
                return "break"
        
        # Vincular eventos
        combo.bind('<KeyRelease>', on_keyrelease)
        combo.bind('<<ComboboxSelected>>', on_combobox_select)
        combo.bind('<KeyPress>', on_key_press)
        
        # === FILA CANTIDAD Y PRECIO ===
        frame_cantidad_precio = tk.Frame(panel_entrada, bg="#1a3d75")
        frame_cantidad_precio.pack(fill="x", padx=20, pady=(0, 15))
        
        # Cantidad (Izquierda)
        frame_cantidad = tk.Frame(frame_cantidad_precio, bg="#1a3d75")
        frame_cantidad.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        lbl_cant = tk.Label(frame_cantidad, text="Cantidad:", font=("Montserrat", 14, "bold"), 
                           bg="#1a3d75", fg="#e5e7eb")
        lbl_cant.pack(anchor="w", pady=(0, 5))
        
        ent_cantidad = tk.Entry(frame_cantidad, font=("Montserrat", 16), bg="#ffffff", 
                               fg="#000000", bd=2, relief="solid", justify="center")
        aplicar_estilo_moderno_entry(ent_cantidad)
        crear_tooltip(ent_cantidad, "Ingrese la cantidad de productos a vender")
        ent_cantidad.pack(fill="x", ipady=6)
        
        # Precio (Derecha)
        frame_precio = tk.Frame(frame_cantidad_precio, bg="#1a3d75")
        frame_precio.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        lbl_precio = tk.Label(frame_precio, text="Precio:", font=("Montserrat", 14, "bold"), 
                             bg="#1a3d75", fg="#e5e7eb")
        lbl_precio.pack(anchor="w", pady=(0, 5))
        
        precio_var = tk.StringVar()
        ent_precio = tk.Entry(frame_precio, textvariable=precio_var, font=("Montserrat", 12), 
                             bg="#ffffff", fg="#000000", bd=2, relief="solid", justify="center")
        aplicar_estilo_moderno_entry(ent_precio)
        crear_tooltip(ent_precio, "Precio unitario del producto (3 decimales) - Se completa automáticamente")
        ent_precio.pack(fill="x", ipady=6)
        
        # === FORMA DE PAGO ===
        frame_pago = tk.Frame(panel_entrada, bg="#1a3d75")
        frame_pago.pack(fill="x", padx=20, pady=(0, 20))
        
        lbl_forma_pago = tk.Label(frame_pago, text="💳 Forma de Pago:", font=("Montserrat", 14, "bold"), 
                                 bg="#1a3d75", fg="#e5e7eb")
        lbl_forma_pago.pack(anchor="w", pady=(0, 5))
        
        forma_pago_var = tk.StringVar(value="EFECTIVO")
        combo_forma_pago = ttk.Combobox(frame_pago, textvariable=forma_pago_var, 
                                       values=["EFECTIVO", "DÉBITO", "CRÉDITO", "TRANSFERENCIA", "QR", "OTROS"], 
                                       font=("Montserrat", 11), state="readonly")
        aplicar_estilo_moderno_combobox(combo_forma_pago)
        crear_tooltip(combo_forma_pago, "Seleccione la forma de pago para la venta")
        combo_forma_pago.pack(fill="x", ipady=6)
        
        # === BOTÓN AGREGAR ===
        frame_boton_agregar = tk.Frame(panel_entrada, bg="#1e293b")
        frame_boton_agregar.pack(fill="x", padx=20, pady=(10, 20))
        
        btn_agregar = tk.Button(frame_boton_agregar, text="2° AGREGÁ AL CARRITO", 
                               font=("Montserrat", 14, "bold"), bg=COLOR_BOTON_MODERNO, fg="#ffffff", 
                               bd=0, relief="flat", cursor="hand2", pady=12)
        aplicar_estilo_moderno_boton(btn_agregar, "primario", hover_efecto=True)
        crear_tooltip(btn_agregar, "Agregar el producto seleccionado al carrito de compras")
        btn_agregar.pack(fill="x")
        
        # === PANEL DEL CARRITO (DERECHA) ===
        panel_carrito = tk.Frame(self.canvas_bg, bg="#1a3d75", bd=2, relief="solid")
        self.canvas_bg.create_window(640, 140, window=panel_carrito, width=600, height=420, anchor="nw")
        
        # Marco decorativo para el carrito
        marco_carrito = tk.Frame(panel_carrito, bg="#00c9df", height=4)
        marco_carrito.pack(fill="x", pady=(0, 10))
        
        # Título del carrito
        lbl_titulo_carrito = tk.Label(panel_carrito, text="🛒 CARRITO DE COMPRAS", 
                                     font=("Montserrat", 16, "bold"), bg="#1a3d75", fg="#e5e7eb")
        lbl_titulo_carrito.pack(pady=(10, 15))
        
        # === TABLA DEL CARRITO ===
        frame_tabla = tk.Frame(panel_carrito, bg="#1e293b")
        frame_tabla.pack(fill="both", expand=True, padx=15, pady=(0, 4))
        
        # Configuración de la tabla
        col_widths = [280, 100, 60, 120]
        carrito_tree = ttk.Treeview(frame_tabla, columns=("Producto", "Precio", "Cant.", "Subtotal"), show="headings", height=8)
        aplicar_estilo_moderno_treeview(carrito_tree)
        habilitar_ordenamiento_treeview(carrito_tree)
        
        # Configurar encabezados y columnas
        headers = ["Producto (Marca | Desc. | Color | Talle)", "Precio Unit.", "Cant.", "Subtotal"]
        for col, ancho, header in zip(carrito_tree["columns"], col_widths, headers):
            carrito_tree.heading(col, text=header, anchor="center")
            carrito_tree.column(col, width=ancho, anchor="center")
        
        # Scrollbar vertical para la tabla
        scrollbar_v = ttk.Scrollbar(frame_tabla, orient="vertical", command=carrito_tree.yview)
        carrito_tree.configure(yscrollcommand=scrollbar_v.set)
        
        # Posicionamiento de tabla y scrollbar
        carrito_tree.pack(side="left", fill="both", expand=True)
        scrollbar_v.pack(side="right", fill="y")
        
        # === BOTONES DE ACCIÓN DEL CARRITO ===
        frame_botones_carrito = tk.Frame(panel_carrito, bg="#260e9b", relief="ridge", bd=2, height=60)
        frame_botones_carrito.pack(fill="x", padx=15, pady=(10, 15))
        frame_botones_carrito.pack_propagate(False)  # Mantener altura fija
        
        btn_eliminar_carrito = tk.Button(frame_botones_carrito, text="🗑️ELIMINAR", 
                                        font=("Montserrat", 14, "bold"), bg=COLOR_BOTON_DANGER, fg="#ffffff", 
                                        bd=2, relief="raised", cursor="hand2", pady=8, padx=20)
        aplicar_estilo_moderno_boton(btn_eliminar_carrito, "danger", hover_efecto=True)
        crear_tooltip(btn_eliminar_carrito, "Eliminar el producto seleccionado del carrito")
        btn_eliminar_carrito.pack(side="left", padx=(10, 10), pady=8, fill="y")
        
        btn_limpiar_carrito = tk.Button(frame_botones_carrito, text="🧹LIMPIAR", 
                                       font=("Montserrat", 14, "bold"), bg=COLOR_BOTON_WARNING, fg="#ffffff", 
                                       bd=2, relief="raised", cursor="hand2", pady=8, padx=20)
        aplicar_estilo_moderno_boton(btn_limpiar_carrito, "warning", hover_efecto=True)
        crear_tooltip(btn_limpiar_carrito, "Limpiar todos los productos del carrito")
        btn_limpiar_carrito.pack(side="right", padx=(10, 10), pady=8, fill="y")
        
        # === PANEL DE TOTALES Y FINALIZACIÓN ===
        panel_totales = tk.Frame(self.canvas_bg, bg="#250576", bd=3, relief="solid")
        self.canvas_bg.create_window(640, 640, window=panel_totales, width=1200, height=120, anchor="center")
        
        # Marco superior decorativo
        marco_totales = tk.Frame(panel_totales, bg=COLOR_BOTON_SUCCESS, height=6)
        marco_totales.pack(fill="x")
        
        # Container principal de totales
        container_totales = tk.Frame(panel_totales, bg="#250576")
        container_totales.pack(fill="both", expand=True, pady=15)
        
        # Variables para totales
        total_var = tk.StringVar(value=f"TOTAL: {self.formato_moneda(0)}")
        iva_var = tk.StringVar(value=f"IVA (21%): {self.formato_moneda(0)}")
        
        # === INFORMACIÓN DE TOTALES (IZQUIERDA) ===
        frame_info_totales = tk.Frame(container_totales, bg="#250576")
        frame_info_totales.pack(side="left", fill="y", padx=(30, 0))
        
        # Panel IVA
        lbl_iva = tk.Label(frame_info_totales, textvariable=iva_var, font=("Montserrat", 14, "bold"), 
                          bg="#374151", fg="#ffffff", relief="flat", bd=0, padx=20, pady=7)
        lbl_iva.pack(anchor="w", pady=(0, 10))
        
        # Panel TOTAL
        lbl_total = tk.Label(frame_info_totales, textvariable=total_var, font=("Montserrat", 18, "bold"), 
                           bg="#008327", fg="#ffffff", relief="flat", bd=0, padx=25, pady=12)
        lbl_total.pack(anchor="w")
        

        # === BOTÓN FINALIZAR VENTA (DERECHA) ===
        frame_finalizar = tk.Frame(container_totales, bg="#250576")
        frame_finalizar.pack(side="right", fill="y", padx=(0, 30))
        
        btn_finalizar = tk.Button(frame_finalizar, text="✅ FINALIZAR VENTA", 
                                 font=("Montserrat", 16, "bold"), bg=COLOR_BOTON_SUCCESS, fg="#ffffff", 
                                 bd=0, relief="flat", cursor="hand2", pady=20, padx=40)
        aplicar_estilo_moderno_boton(btn_finalizar, "success", hover_efecto=True)
        crear_tooltip(btn_finalizar, "Procesar la venta y registrar en el sistema")
        btn_finalizar.pack(expand=True)

        # === FUNCIONES DE VALIDACIÓN Y LÓGICA ===
        def validar_cantidad(event=None):
            try:
                valor = ent_cantidad.get()
                if valor == "":
                    validar_campo_visual(ent_cantidad, True)
                    return
                cantidad = int(valor)
                if cantidad > 0:
                    validar_campo_visual(ent_cantidad, True)
                else:
                    validar_campo_visual(ent_cantidad, False, "La cantidad debe ser mayor a 0")
            except ValueError:
                validar_campo_visual(ent_cantidad, False, "Ingrese un número válido")
        
        def validar_precio(event=None):
            try:
                valor = precio_var.get()
                if valor == "":
                    validar_campo_visual(ent_precio, True)
                    return
                precio = float(valor)
                if precio > 0:
                    validar_campo_visual(ent_precio, True)
                    # Normalizar sin decimales para visual
                    precio_var.set(str(int(round(precio))))
                else:
                    validar_campo_visual(ent_precio, False, "El precio debe ser mayor a 0")
            except ValueError:
                validar_campo_visual(ent_precio, False, "Ingrese un precio válido")
        
        def set_precio_venta(event=None):
            """Carga automáticamente el precio cuando se selecciona un producto"""
            seleccion = producto_var.get().strip()
            print(f"[DEBUG] set_precio_venta llamado para: '{seleccion}'  set_precio_venta - main.py:1733")
            
            if not seleccion:
                precio_var.set("")
                return
            
            if seleccion in productos_dict:
                producto = productos_dict[seleccion]
                print(f"[DEBUG] Producto encontrado: {producto.marca} {producto.descripcion}  Stock: {producto.cantidad}  set_precio_venta - main.py:1741")
                
                # Verificar stock disponible
                if producto.cantidad <= 0:
                    precio_var.set("SIN STOCK")
                    ent_precio.config(fg="#ef4444")  # Rojo para sin stock
                    messagebox.showwarning("Sin Stock", f"El producto '{producto.descripcion}' no tiene stock disponible.")
                    return
                else:
                    ent_precio.config(fg="#000000")  # Negro normal
                
                # Calcular precio con ofertas
                precio_final = producto.precio_venta
                mensaje_oferta = ""
                
                if producto.oferta and producto.oferta.get('tipo'):
                    print(f"[DEBUG] Oferta encontrada: {producto.oferta}  set_precio_venta - main.py:1757")
                    if producto.oferta['tipo'] == 'porcentaje':
                        descuento = float(producto.oferta['valor'])
                        precio_final = producto.precio_venta * (1 - descuento / 100)
                        mensaje_oferta = f" ({descuento}% OFF)"
                    elif producto.oferta['tipo'] == 'precio_manual':
                        precio_final = float(producto.oferta['valor'])
                        mensaje_oferta = " (OFERTA)"
                    elif producto.oferta['tipo'] == 'cantidad':
                        mensaje_oferta = f" ({producto.oferta['valor']})"
                
                # Mostrar precio formateado
                precio_mostrar = f"{precio_final:.0f}"
                precio_var.set(precio_mostrar)
                
                # Actualizar tooltip con información del producto
                info_producto = f"Stock: {producto.cantidad} | Precio: ${precio_final:.0f}{mensaje_oferta}"
                crear_tooltip(ent_precio, info_producto)
                
                print(f"[DEBUG] Precio cargado: {precio_mostrar}{mensaje_oferta}  set_precio_venta - main.py:1776")
            else:
                print(f"[DEBUG] Producto no encontrado en diccionario  set_precio_venta - main.py:1778")
                precio_var.set("")
                
        def actualizar_totales():
            """Actualiza los totales del carrito"""
            total = sum(item[3] for item in carrito)
            total_iva = sum(item[4] for item in carrito)
            total_var.set(f"TOTAL: {self.formato_moneda(total)}")
            iva_var.set(f"IVA (21%): {self.formato_moneda(total_iva)}")

        def eliminar_del_carrito():
            seleccion = carrito_tree.selection()
            if not seleccion:
                messagebox.showwarning("Eliminar", "Seleccione un producto del carrito para eliminar.")
                return
            for item in seleccion:
                idx = carrito_tree.index(item)
                carrito_tree.delete(item)
                del carrito[idx]
            actualizar_totales()
            
        def limpiar_carrito():
            """Limpia todo el carrito"""
            if carrito:
                resultado = messagebox.askyesno("Limpiar Carrito", "¿Está seguro de que desea limpiar todo el carrito?")
                if resultado:
                    carrito.clear()
                    for item in carrito_tree.get_children():
                        carrito_tree.delete(item)
                    actualizar_totales()

        def agregar_al_carrito():
            try:
                seleccion = producto_var.get()
                if not seleccion:
                    raise ValueError("Debe seleccionar un producto.")
                producto = productos_dict[seleccion]
                cantidad = int(ent_cantidad.get())
                if cantidad <= 0:
                    raise ValueError("La cantidad debe ser mayor a 0.")
                if producto.cantidad < cantidad:
                    raise ValueError(f"Stock insuficiente. Disponible: {producto.cantidad}")
                
                precio_unitario = float(precio_var.get())
                
                # Aplicar lógica de ofertas por cantidad (ej: 3x2)
                cantidad_a_cobrar = cantidad
                mensaje_oferta = ""
                if producto.oferta and producto.oferta.get('tipo') == 'cantidad':
                    oferta_str = producto.oferta['valor']  # ej: "3X2"
                    try:
                        if 'X' in oferta_str.upper():
                            partes = oferta_str.upper().split('X')
                            compra, paga = int(partes[0]), int(partes[1])
                            # Calcular cuántos grupos de oferta aplican
                            grupos_oferta = cantidad // compra
                            resto = cantidad % compra
                            cantidad_a_cobrar = (grupos_oferta * paga) + resto
                            if grupos_oferta > 0:
                                mensaje_oferta = f" (Oferta {oferta_str})"
                    except:
                        pass  # Si no se puede parsear, usar cantidad normal
                
                sub_total = precio_unitario * cantidad_a_cobrar
                iva = sub_total * 0.21
                carrito.append((producto, cantidad, precio_unitario, sub_total, iva))
                
                # Mostrar en la tabla con nombre optimizado incluyendo marca
                producto_nombre = f"{producto.marca} | {producto.descripcion[:12]}... | {producto.color} | {producto.talle}"
                if len(f"{producto.marca} | {producto.descripcion} | {producto.color} | {producto.talle}") <= 45:
                    producto_nombre = f"{producto.marca} | {producto.descripcion} | {producto.color} | {producto.talle}"
                
                # Mostrar precio con formato consistente
                precio_mostrar = f"{self.formato_moneda(precio_unitario)}{mensaje_oferta}"
                
                carrito_tree.insert("", "end", values=(
                    producto_nombre,
                    precio_mostrar, 
                    cantidad, 
                    self.formato_moneda(sub_total)
                ))
                
                # Limpiar campos
                producto_var.set("")
                ent_cantidad.delete(0, tk.END)
                precio_var.set("")
                
                # Actualizar totales
                actualizar_totales()
                
                # Feedback visual
                btn_agregar.config(bg="#059669", text="✅ AGREGADO")
                self.after(800, lambda: btn_agregar.config(bg=COLOR_BOTON_MODERNO, text="🛒 AGREGAR AL CARRITO"))
                
            except ValueError as ve:
                messagebox.showerror("Error de Validación", str(ve))
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {e}")
        
        def registrar_venta_final():
            if not carrito:
                messagebox.showerror("Carrito Vacío", "Agregue productos al carrito antes de finalizar la venta.")
                return
                
            nro_venta = len(self.sistema.ventas) + 1
            nro_venta_str = str(nro_venta).zfill(5)
            descripcion = f"Venta N° {nro_venta_str}"
            forma_pago = forma_pago_var.get()
            
            # Confirmación antes de procesar
            total_venta = sum(item[3] for item in carrito)
            resultado = messagebox.askyesno("Confirmar Venta", 
                                          f"¿Confirmar venta por {self.formato_moneda(total_venta)}?\n"
                                          f"Forma de pago: {forma_pago}")
            if not resultado:
                return
                
            exito = self.sistema.registrar_venta(descripcion, [(p, c, pu) for p, c, pu, st, iva in carrito], 
                                               datetime.date.today(), forma_pago, vendedor=(self.session.username if hasattr(self, 'session') and self.session else None))
            if not exito:
                messagebox.showerror("Error de Stock", "No se pudo registrar la venta. Verifique el stock disponible.")
                return
                
            messagebox.showinfo("Venta Exitosa", f"✅ Venta N° {nro_venta_str} registrada exitosamente\n"
                                               f"Total: {self.formato_moneda(total_venta)}\n"
                                               f"Stock actualizado automáticamente")
            self.mostrar_menu_principal()
        
        # === BIND DE EVENTOS ===
        ent_cantidad.bind('<KeyRelease>', validar_cantidad)
        ent_precio.bind('<KeyRelease>', validar_precio)
        # Los eventos del combo están configurados en la función optimizada de sugerencias
        
        # === ASIGNAR COMANDOS A BOTONES ===
        btn_agregar.config(command=agregar_al_carrito)
        btn_eliminar_carrito.config(command=eliminar_del_carrito)
        btn_limpiar_carrito.config(command=limpiar_carrito)
        btn_finalizar.config(command=registrar_venta_final)

        # Atajos de teclado
        self.bind_all('<Control-Return>', lambda e: registrar_venta_final())
        ent_precio.bind('<Return>', lambda e: agregar_al_carrito())
        ent_cantidad.bind('<Return>', lambda e: agregar_al_carrito())
        
        # === REGISTRAR WIDGETS ===
        widgets.extend([titulo_frame, panel_entrada, panel_carrito, panel_totales,
                       lbl_prod, combo, lbl_cant, ent_cantidad, lbl_precio, ent_precio, 
                       lbl_forma_pago, combo_forma_pago, btn_agregar,
                       carrito_tree, scrollbar_v, frame_botones_carrito, 
                       btn_eliminar_carrito, btn_limpiar_carrito,
                       lbl_iva, lbl_total, btn_finalizar])
        self.pantalla_widgets.extend(widgets)

    def _pantalla_ventas_dia(self, parent):
        widgets = []
        hoy = datetime.date.today()
        ventas_hoy = self.sistema.cierre_caja(hoy)
        
        # Marco principal de la tabla con estilo profesional
        tabla_frame = tk.Frame(self.canvas_bg, bg="#0a0f1a", relief="flat", bd=0, height=450)
        self.canvas_bg.create_window(340, 375, window=tabla_frame, width=650, height=450, anchor="center")
        tabla_frame.pack_propagate(False)  # Mantener altura fija
        
        # Marco interno con diseño profesional - BORDE SUTIL
        marco_interno = tk.Frame(tabla_frame, bg="#1a1f2e", relief="solid", bd=1)
        marco_interno.pack(fill="both", expand=True, padx=3, pady=3)
        marco_interno.config(highlightbackground="#3b82f6", highlightcolor="#3b82f6", highlightthickness=2)
        
        # Header con título y separador elegante
        header_label = tk.Label(marco_interno, text="📊 VENTAS DEL DÍA", 
                              font=("Montserrat", 18, "bold"), 
                              bg="#1a1f2e", fg="#60a5fa", pady=15)
        header_label.pack(fill="x")
        
        # Línea separadora elegante
        separador = tk.Frame(marco_interno, bg="#3b82f6", height=2)
        separador.pack(fill="x", padx=15, pady=(0, 10))
        
        # Contenedor de la tabla
        tabla_container = tk.Frame(marco_interno, bg="#1a1f2e")
        tabla_container.pack(fill="both", expand=True, padx=15, pady=(5, 20))
        
        # Headers de columnas con estilo corporativo
        header_row = tk.Frame(tabla_container, bg="#2563eb", relief="flat", bd=0)
        header_row.pack(fill="x", pady=(0, 5))
        
        headers_config = [("Nro Venta", 12), ("Forma de Pago", 15), ("Detalle Artículos", 35), ("Total Venta", 12)]
        for i, (header_text, width) in enumerate(headers_config):
            lbl_header = tk.Label(header_row, text=header_text, 
                                 font=("Montserrat", 12, "bold"), 
                                 bg="#2563eb", fg="#ffffff", 
                                 width=width, pady=8)
            lbl_header.pack(side="left", padx=1)
        
        # Frame scrollable para las filas de datos
        scroll_frame = tk.Frame(tabla_container, bg="#1a1f2e")
        scroll_frame.pack(fill="both", expand=True)
        
        # Canvas y scrollbar para scroll vertical
        canvas_tabla = tk.Canvas(scroll_frame, bg="#1a1f2e", highlightthickness=0)
        scrollbar_tabla = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas_tabla.yview)
        scrollable_frame = tk.Frame(canvas_tabla, bg="#1a1f2e")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas_tabla.configure(scrollregion=canvas_tabla.bbox("all"))
        )
        
        canvas_tabla.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas_tabla.configure(yscrollcommand=scrollbar_tabla.set)
        
        canvas_tabla.pack(side="left", fill="both", expand=True)
        scrollbar_tabla.pack(side="right", fill="y")
        
        # Configurar scroll con rueda del mouse para la tabla de ventas
        configurar_scroll_mouse(canvas_tabla, scrollbar_tabla)
        
        # Definir venta_items_map para mapear cada fila a su detalle
        venta_items_map = {}

        # Función para obtener color del texto según el tipo de dato
        def obtener_color_por_tipo(valor, tipo_dato):
            if tipo_dato == "monto":
                return "#93c5fd"  # Azul claro para montos
            else:
                return "#e5e7eb"  # Color estándar
        
        # Llenar datos con filas alternadas
        for idx, v in enumerate(ventas_hoy):
            detalle = ", ".join([f"{item['producto'].marca} {item['producto'].descripcion}({item['producto'].color}/{item['producto'].talle}) x{item['cantidad']} @{self.formato_moneda(item['precio'])}" for item in v.items])
            total = sum(item['cantidad'] * item['precio'] for item in v.items)
            forma_pago = getattr(v, 'forma_pago', 'EFECTIVO')
            
            # Color alternado para las filas
            bg_color = "#1e293b" if idx % 2 == 0 else "#0f172a"
            
            row_frame = tk.Frame(scrollable_frame, bg=bg_color, relief="flat", bd=0)
            row_frame.pack(fill="x", pady=1)
            
            valores_config = [
                (v.descripcion, 12, "texto"),
                (forma_pago, 15, "texto"), 
                (detalle[:40] + "..." if len(detalle) > 40 else detalle, 35, "texto"),
                (self.formato_moneda(total), 12, "monto")
            ]
            
            for i, (valor, width, tipo_dato) in enumerate(valores_config):
                text_color = obtener_color_por_tipo(valor, tipo_dato)
                lbl_valor = tk.Label(row_frame, text=valor, 
                                   font=("Montserrat", 11), 
                                   bg=bg_color, fg=text_color, 
                                   width=width, pady=6)
                lbl_valor.pack(side="left", padx=1)
            
            # Guardar mapeo para detalle completo
            venta_items_map[row_frame] = detalle
            
            # Bind para mostrar detalle al hacer clic
            def crear_click_handler(detalle_completo):
                def mostrar_detalle(event):
                    top = tk.Toplevel(self)
                    top.title("Detalle de venta")
                    top.geometry("800x300")
                    top.configure(bg="#0a0f1a")
                    
                    # Marco con el mismo estilo
                    marco_detalle = tk.Frame(top, bg="#1a1f2e", relief="solid", bd=1)
                    marco_detalle.pack(fill="both", expand=True, padx=10, pady=10)
                    marco_detalle.config(highlightbackground="#3b82f6", highlightcolor="#3b82f6", highlightthickness=2)
                    
                    # Título
                    lbl_titulo_detalle = tk.Label(marco_detalle, text="🔍 DETALLE COMPLETO DE LA VENTA", 
                                                font=("Montserrat", 16, "bold"), 
                                                bg="#1a1f2e", fg="#60a5fa", pady=10)
                    lbl_titulo_detalle.pack(fill="x")
                    
                    # Separador
                    sep_detalle = tk.Frame(marco_detalle, bg="#3b82f6", height=2)
                    sep_detalle.pack(fill="x", padx=15, pady=(0, 10))
                    
                    # Texto con scroll
                    txt = tk.Text(marco_detalle, wrap="word", bg="#0f172a", fg="#e5e7eb",
                                font=("Montserrat", 10), padx=15, pady=10)
                    txt.pack(fill="both", expand=True, padx=15, pady=(0, 15))
                    txt.insert("1.0", detalle_completo)
                    txt.config(state="disabled")
                    
                return mostrar_detalle
            
            for widget in row_frame.winfo_children():
                widget.bind("<Button-1>", crear_click_handler(detalle))
            for widget in row_frame.winfo_children():
                widget.bind("<Button-1>", crear_click_handler(detalle))
        
        # Total ventas centrado debajo de la tabla
        total_general = sum(sum(item['cantidad'] * item['precio'] for item in v.items) for v in ventas_hoy)
        lbl_total = tk.Label(self.canvas_bg, text=f"Total ventas: {self.formato_moneda(total_general)}", 
                           font=("Montserrat", 14, "bold"), bg= COLOR_BOTON_SUCCESS, fg="#ffffff", 
                           relief="flat", bd=0, padx=20, pady=10)
        self.canvas_bg.create_window(350, 655, window=lbl_total, anchor="center")

        # === PANEL DE GASTOS ===
        gastos_widgets = self._crear_panel_gastos()
        widgets.extend(gastos_widgets)
        
        # Botón cierre de caja centrado (ajustado para nueva posición)
        btn_cierre = tk.Button(self.canvas_bg, text="CIERRE DE CAJA", font=("Montserrat", 14, "bold"), 
                              bg="#dd0707", fg="#ffffff", bd=0, relief="flat", 
                              command=self.realizar_cierre_caja, cursor="hand2")
        self.canvas_bg.create_window(990, 660, window=btn_cierre, width=220, height=50, anchor="center")
        
        widgets.extend([tabla_frame, lbl_total, btn_cierre])
        self.pantalla_widgets.extend(widgets)

    def _crear_panel_gastos(self):
        """Crea el panel de gastos del día"""
        print("[DEBUG] Iniciando creación del panel de gastos  _crear_panel_gastos - main.py:2094")
        widgets = []
        hoy = datetime.date.today()
        gastos_hoy = self.sistema.obtener_gastos_fecha(hoy)
        print(f"[DEBUG] Gastos encontrados para hoy ({hoy}): {len(gastos_hoy)} gastos  _crear_panel_gastos - main.py:2098")
        
        # Frame principal del panel (usando Frame en lugar de crear directamente en canvas)
        gastos_frame = tk.Frame(self.canvas_bg, bg="#1a3d75", relief="solid", bd=1)
        self.canvas_bg.create_window(940, 375, window=gastos_frame, width=520, height=450, anchor="center")
        
        # Header del panel
        header_frame = tk.Frame(gastos_frame, bg="#1A3D75", height=30)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Título con ícono
        lbl_titulo = tk.Label(header_frame, text="GASTOS Y PAGOS", 
                             font=("Montserrat", 12, "bold"), 
                             bg="#1A3D75", fg="#ffffff")
        lbl_titulo.pack(side="left", padx=10, pady=5)
        
        # Botón colapsar/expandir
        self.gastos_expandido = tk.BooleanVar(value=True)
        self.btn_toggle_gastos = tk.Button(header_frame, text="[-]", 
                              font=("Montserrat", 10, "bold"),
                              bg="#4f46e5", fg="#ffffff", bd=0, width=3,
                              command=self._toggle_gastos_panel)
        self.btn_toggle_gastos.pack(side="right", padx=10, pady=2)
        
        # Contenido del panel
        self.content_gastos = tk.Frame(gastos_frame, bg="#1a3d75")
        self.content_gastos.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Frame superior: Formulario de entrada
        entrada_frame = tk.Frame(self.content_gastos, bg="#1a3d75")
        entrada_frame.pack(fill="x", pady=(0, 5))
        
        # Campo Monto
        tk.Label(entrada_frame, text="Monto:", font=("Montserrat", 12, "bold"),
                bg="#1a3d75", fg="#ffffff").pack(side="left", padx=(0, 5))
        
        self.ent_gasto_monto = tk.Entry(entrada_frame, font=("Montserrat", 10),
                                       bg="#ffffff", fg="#0026FF", width=12)
        aplicar_estilo_moderno_entry(self.ent_gasto_monto)
        self.ent_gasto_monto.pack(side="left", padx=(0, 10))
        
        # Campo Motivo
        tk.Label(entrada_frame, text="Motivo:", font=("Montserrat", 12, "bold"),
                bg="#1a3d75", fg="#ffffff").pack(side="left", padx=(0, 5))

        self.ent_gasto_motivo = tk.Entry(entrada_frame, font=("Montserrat", 10),
                                        bg="#ffffff", fg="#0026FF", width=25)
        aplicar_estilo_moderno_entry(self.ent_gasto_motivo)
        self.ent_gasto_motivo.pack(side="left", padx=(0, 10))
        
        # Botón Agregar
        btn_agregar_gasto = tk.Button(entrada_frame, text="+",
                               font=("Montserrat", 16, "bold"),
                               bg=COLOR_BOTON_SUCCESS, fg="#ffffff",
                               command=self._agregar_gasto_dia, cursor="hand2")
        aplicar_estilo_moderno_boton(btn_agregar_gasto, "success", True)
        btn_agregar_gasto.pack(side="left", padx=(5, 0))
        
        # Frame inferior: Lista de gastos y total
        lista_frame = tk.Frame(self.content_gastos, bg="#1a3d75")
        lista_frame.pack(fill="both", expand=True)
        
        # Título de la lista
        tk.Label(lista_frame, text="Gastos del día:", 
                font=("Montserrat", 11, "bold"),
                bg="#1a3d75", fg="#ffffff").pack(anchor="w", pady=(0, 3))
        
        # Frame scrollable para la lista de gastos
        self.frame_lista_gastos = tk.Frame(lista_frame, bg="#1e293b", relief="sunken", bd=1)
        self.frame_lista_gastos.pack(fill="both", expand=True, pady=(0, 5))
        
        # Crear scrollbar para la lista
        scrollbar_gastos = tk.Scrollbar(self.frame_lista_gastos, bg="#4a5568")
        scrollbar_gastos.pack(side="right", fill="y")
        
        # Canvas para scroll
        self.canvas_gastos = tk.Canvas(self.frame_lista_gastos, bg="#1e293b", 
                                      yscrollcommand=scrollbar_gastos.set,
                                      highlightthickness=0)
        self.canvas_gastos.pack(side="left", fill="both", expand=True)
        scrollbar_gastos.config(command=self.canvas_gastos.yview)
        
        # Configurar scroll con rueda del mouse para el panel de gastos
        configurar_scroll_mouse(self.canvas_gastos, scrollbar_gastos)
        
        # Frame interno para los elementos de gasto
        self.inner_frame_gastos = tk.Frame(self.canvas_gastos, bg="#0090e4")
        self.canvas_gastos.create_window((0, 0), window=self.inner_frame_gastos, anchor="nw")
        
        # Cargar gastos iniciales
        self._actualizar_lista_gastos()
        
        # Configurar scroll region
        self.inner_frame_gastos.update_idletasks()
        self.canvas_gastos.configure(scrollregion=self.canvas_gastos.bbox("all"))
        
        # Total de gastos
        total_gastos = sum(g.monto for g in gastos_hoy)
        self.lbl_total_gastos = tk.Label(lista_frame, 
                                        text=f"Total Gastos del Día: {self.formato_moneda(total_gastos)}",
                                        font=("Montserrat", 10, "bold"),
                                        bg="#f7770e", fg="#ffffff", pady=3)
        self.lbl_total_gastos.pack(fill="x", pady=(2, 0))
        
        widgets.extend([gastos_frame, self.ent_gasto_monto, self.ent_gasto_motivo, 
                       btn_agregar_gasto, self.lbl_total_gastos])
        
        return widgets

    def _toggle_gastos_panel(self):
        """Colapsa/expande el panel de gastos"""
        if self.gastos_expandido.get():
            self.content_gastos.pack_forget()
            self.btn_toggle_gastos.config(text="[+]")
            self.gastos_expandido.set(False)
        else:
            self.content_gastos.pack(fill="both", expand=True, padx=10, pady=5)
            self.btn_toggle_gastos.config(text="[-]")
            self.gastos_expandido.set(True)

    def _agregar_gasto_dia(self):
        """Agrega un gasto del día"""
        try:
            monto_str = self.ent_gasto_monto.get().strip()
            motivo = self.ent_gasto_motivo.get().strip()
            
            if not monto_str or not motivo:
                messagebox.showerror("Error", "Debe completar monto y motivo")
                return
        
            # Convertir monto (aceptar tanto punto como coma)
            monto_str = monto_str.replace(",", ".")
            monto = float(monto_str)
            if monto <= 0:
                messagebox.showerror("Error", "El monto debe ser mayor a 0")
                return
            
            # Agregar al sistema (usuario temporal hasta integrar autenticación)
            usuario = "Usuario Sistema"  # Temporal - posteriormente se integrará con sistema de autenticación
            exito = self.sistema.agregar_gasto(monto, motivo, datetime.date.today(), usuario)
            
            if exito:
                # Limpiar campos
                self.ent_gasto_monto.delete(0, tk.END)
                self.ent_gasto_motivo.delete(0, tk.END)
                
                # Actualizar panel
                self._actualizar_panel_gastos()
                
                messagebox.showinfo("Éxito", f"Gasto agregado correctamente: {self.formato_moneda(monto)} - {motivo}")
            else:
                messagebox.showerror("Error", "No se pudo agregar el gasto")
            
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado al agregar gasto: {str(e)}")
            print(f"[DEBUG] Error en _agregar_gasto_dia: {e} - main.py:2256")

    def _actualizar_lista_gastos(self):
        """Actualiza la lista visual de gastos con formato vertical"""
        print("[DEBUG] Actualizando lista visual de gastos - main.py:2260")
        
        # Limpiar frame de gastos
        for widget in self.inner_frame_gastos.winfo_children():
            widget.destroy()
            
        hoy = datetime.date.today()
        gastos_hoy = self.sistema.obtener_gastos_fecha(hoy)
        
        if gastos_hoy:
            for i, gasto in enumerate(gastos_hoy):
                # Frame individual para cada gasto
                gasto_frame = tk.Frame(self.inner_frame_gastos, bg="#2d3748", relief="solid", bd=1)
                gasto_frame.pack(fill="x", padx=2, pady=1)
                
                # Texto del gasto
                gasto_texto = f"💸 {self.formato_moneda(gasto.monto)} - {gasto.motivo}"
                if hasattr(gasto, 'timestamp'):
                    hora = gasto.timestamp.strftime("%H:%M")
                    gasto_texto += f" ({hora})"
                
                lbl_gasto = tk.Label(gasto_frame, text=gasto_texto,
                                   font=("Montserrat", 9), 
                                   bg="#2d3748", fg="#e5e7eb",
                                   anchor="w", padx=5, pady=2)
                lbl_gasto.pack(fill="x")
        else:
            # Mensaje cuando no hay gastos
            lbl_sin_gastos = tk.Label(self.inner_frame_gastos, 
                                     text="📝 Sin gastos registrados hoy",
                                     font=("Montserrat", 10, "italic"), 
                                     bg="#1e293b", fg="#94a3b8",
                                     pady=10)
            lbl_sin_gastos.pack(fill="x")
        
        # Actualizar scroll region
        self.inner_frame_gastos.update_idletasks()
        self.canvas_gastos.configure(scrollregion=self.canvas_gastos.bbox("all"))

    def _actualizar_panel_gastos(self):
        """Actualiza la información del panel de gastos"""
        print("[DEBUG] Iniciando actualización del panel de gastos  _actualizar_panel_gastos - main.py:2301")
        hoy = datetime.date.today()
        gastos_hoy = self.sistema.obtener_gastos_fecha(hoy)
        print(f"[DEBUG] Gastos encontrados para actualizar: {len(gastos_hoy)}  _actualizar_panel_gastos - main.py:2304")
        
        # Actualizar lista visual de gastos
        if hasattr(self, 'inner_frame_gastos'):
            self._actualizar_lista_gastos()
            print("[DEBUG] Lista visual de gastos actualizada - main.py:2309")
        
        # Actualizar total
        total_gastos = sum(g.monto for g in gastos_hoy)
        if hasattr(self, 'lbl_total_gastos'):
            total_text = f"Total Gastos del Día: {self.formato_moneda(total_gastos)}"
            self.lbl_total_gastos.config(text=total_text)
            print(f"[DEBUG] Label de total actualizado: {total_text}  _actualizar_panel_gastos - main.py:2316")
        else:
            print("[DEBUG] ERROR: lbl_total_gastos no existe  _actualizar_panel_gastos - main.py:2318")

    def realizar_cierre_caja(self):
        """Realiza el cierre de caja del día y muestra informe avanzado"""
        hoy = datetime.date.today()
        ventas_hoy = self.sistema.cierre_caja(hoy)
        gastos_hoy = self.sistema.obtener_gastos_fecha(hoy)
        
        # Mostrar ventana de cierre avanzado (incluso si no hay ventas, puede haber gastos)
        self.mostrar_cierre_avanzado()

    def mostrar_ventana_descarga_csv(self, ventas_hoy, fecha):
        """Muestra ventana de confirmación para descarga de CSV"""
        ventana = tk.Toplevel(self)
        ventana.title("Cierre de Caja")
        ventana.geometry("450x300")
        ventana.configure(bg=COLOR_FONDO)
        ventana.resizable(False, False)
        
        # Crear gradiente de fondo
        canvas = tk.Canvas(ventana, width=450, height=300, highlightthickness=0, bd=0)
        canvas.pack(fill="both", expand=True)
        for i in range(0, 300, 2):
            color = self._interpolar_color(COLOR_GRADIENTE_1, COLOR_GRADIENTE_2, i/300)
            canvas.create_rectangle(0, i, 450, i+2, outline="", fill=color)
        
        # Título
        lbl_titulo = tk.Label(canvas, text="QUERES DESCARGAR TU RESUMEN HOY??", 
                             font=("Montserrat", 16, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO)
        canvas.create_window(225, 60, window=lbl_titulo, anchor="center")
        
        # Texto explicativo
        lbl_explicacion = tk.Label(canvas, text="Tus ventas quedan guardadas acá.\nDisponibles cuando quieras!", 
                                  font=("Montserrat", 12), bg=COLOR_FONDO, fg=COLOR_TEXTO, justify="center")
        canvas.create_window(225, 180, window=lbl_explicacion, anchor="center")
        
        # Botones SI / NO
        def descargar_si():
            self.generar_csv_cierre(ventas_hoy, fecha)
            # ARCHIVAR VENTAS Y GASTOS DEL DÍA
            self.sistema.archivar_ventas_dia(fecha)
            self.sistema.archivar_gastos_dia(fecha)
            ventana.destroy()
            # Refrescar pantalla ventas del día
            self.mostrar_ventas_dia()
            
        def descargar_no():
            # ARCHIVAR VENTAS Y GASTOS DEL DÍA AUNQUE NO DESCARGUE CSV
            self.sistema.archivar_ventas_dia(fecha)
            self.sistema.archivar_gastos_dia(fecha)
            messagebox.showinfo("Cierre de Caja", "Cierre de caja realizado. Las ventas y gastos han sido archivados correctamente.")
            ventana.destroy()
            # Refrescar pantalla ventas del día
            self.mostrar_ventas_dia()
        
        btn_si = tk.Button(canvas, text="SÍ", font=("Montserrat", 14, "bold"), 
                          bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, bd=0, relief="flat", 
                          command=descargar_si, cursor="hand2")
        canvas.create_window(150, 240, window=btn_si, width=100, height=40, anchor="center")
        
        btn_no = tk.Button(canvas, text="NO", font=("Montserrat", 14, "bold"), 
                          bg="#666666", fg=COLOR_BOTON_TEXTO, bd=0, relief="flat", 
                          command=descargar_no, cursor="hand2")
        canvas.create_window(300, 240, window=btn_no, width=100, height=40, anchor="center")
        
        # Centrar ventana
        ventana.transient(self)
        ventana.grab_set()
        
    def generar_csv_cierre(self, ventas_hoy, fecha):
        """Genera archivo CSV con el resumen del día"""
        
        # Calcular totales por forma de pago
        totales_forma_pago = {}
        total_general = 0
        detalle_ventas = []
        
        for venta in ventas_hoy:
            forma_pago = getattr(venta, 'forma_pago', 'EFECTIVO')
            total_venta = sum(item['cantidad'] * item['precio'] for item in venta.items)
            total_general += total_venta
            
            if forma_pago not in totales_forma_pago:
                totales_forma_pago[forma_pago] = 0
            totales_forma_pago[forma_pago] += total_venta
            
            # Detalle de cada venta
            for item in venta.items:
                detalle_ventas.append({
                    'Fecha': fecha.strftime("%Y-%m-%d"),
                    'Nro ventata': venta.descripcion,
                    'Forma de Pago': forma_pago,
                    'Producto': item['producto'].descripcion,
                    'Marca': item['producto'].marca,
                    'Color': item['producto'].color,
                    'Talle': item['producto'].talle,
                    'Cantidad': item['cantidad'],
                    'Precio Unitario': item['precio'],
                    'Subtotal': item['cantidad'] * item['precio']
                })
        
        # Pedir ubicación de guardado
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile=f"Cierre_Caja_{fecha.strftime('%Y-%m-%d')}.csv"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Encabezado del resumen
                    writer.writerow(['RESUMEN CIERRE DE CAJA'])
                    writer.writerow(['Fecha:', fecha.strftime("%Y-%m-%d")])
                    writer.writerow([''])
                    
                    # Totales por forma de pago
                    writer.writerow(['TOTALES POR FORMA DE PAGO'])
                    for forma_pago, total in totales_forma_pago.items():
                        writer.writerow([forma_pago, self.formato_moneda(total)])
                    writer.writerow([''])
                    writer.writerow(['TOTAL GENERAL', self.formato_moneda(total_general)])
                    writer.writerow([''])
                    writer.writerow([''])
                    
                    # Detalle de ventas
                    writer.writerow(['DETALLE DE VENTAS'])
                    if detalle_ventas:
                        fieldnames = detalle_ventas[0].keys()
                        dict_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        dict_writer.writeheader()
                        dict_writer.writerows(detalle_ventas)
                
                messagebox.showinfo("Descarga Exitosa", f"Archivo guardado en:\n{filename}\n\nCierre de caja realizado correctamente.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar el archivo:\n{e}")
        else:
            messagebox.showinfo("Cierre de Caja", "Cierre de caja realizado. Las ventas han sido guardadas correctamente.")

    def calcular_metricas_cierre(self, fecha):
        """Calcula todas las métricas para el cierre del día"""
        
        # Obtener datos del día
        ventas_hoy = self.sistema.cierre_caja(fecha)
        gastos_hoy = self.sistema.obtener_gastos_fecha(fecha)
        
        # Métricas básicas
        cantidad_ventas = len(ventas_hoy)
        productos_vendidos = sum(sum(item['cantidad'] for item in v.items) for v in ventas_hoy)
        monto_total_ventas = sum(sum(item['cantidad'] * item['precio'] for item in v.items) for v in ventas_hoy)
        monto_total_gastos = sum(g.monto for g in gastos_hoy)
        monto_total_iva = monto_total_ventas * 0.21
        
        # Métricas calculadas
        promedio_venta = monto_total_ventas / cantidad_ventas if cantidad_ventas > 0 else 0
        monto_facturado = monto_total_ventas - monto_total_gastos
        
        # Producto más vendido
        conteo_productos = {}
        for venta in ventas_hoy:
            for item in venta.items:
                producto = item['producto']
                key = f"{producto.descripcion} {producto.color} {producto.talle}"
                conteo_productos[key] = conteo_productos.get(key, 0) + item['cantidad']
        
        producto_mas_vendido = max(conteo_productos.items(), key=lambda x: x[1]) if conteo_productos else ("N/A", 0)
        
        # Balance ganancia (ventas - costos - gastos)
        costo_total_productos = 0
        for venta in ventas_hoy:
            for item in venta.items:
                costo_total_productos += item['producto'].precio_costo * item['cantidad']
        
        balance_ganancia = monto_total_ventas - costo_total_productos - monto_total_gastos
        
        # Métricas adicionales
        margen_bruto = (balance_ganancia / monto_total_ventas * 100) if monto_total_ventas > 0 else 0
        roi_dia = (balance_ganancia / costo_total_productos * 100) if costo_total_productos > 0 else 0
        
        # Eficiencia operativa
        eficiencia = "Alta" if balance_ganancia > monto_total_ventas * 0.4 else "Media" if balance_ganancia > monto_total_ventas * 0.2 else "Baja"
        
        return {
            'cantidad_ventas': cantidad_ventas,
            'productos_vendidos': productos_vendidos,
            'producto_mas_vendido': producto_mas_vendido,
            'monto_total_ventas': monto_total_ventas,
            'monto_total_gastos': monto_total_gastos,
            'monto_total_iva': monto_total_iva,
            'promedio_venta': promedio_venta,
            'monto_facturado': monto_facturado,
            'balance_ganancia': balance_ganancia,
            'margen_bruto': margen_bruto,
            'roi_dia': roi_dia,
            'costo_total_productos': costo_total_productos,
            'eficiencia_operativa': eficiencia,
            'ventas_detalle': ventas_hoy,
            'gastos_detalle': gastos_hoy,
            'fecha': fecha
        }

    def mostrar_cierre_avanzado(self):
        """Muestra la ventana de cierre avanzado con métricas completas"""
        
        fecha_hoy = datetime.date.today()
        metricas = self.calcular_metricas_cierre(fecha_hoy)
        
        # Crear ventana modal
        ventana_cierre = tk.Toplevel(self)
        ventana_cierre.title("📊 Informe de Cierre Diario - ALENIA GESTIÓN KONTROL+")
        ventana_cierre.geometry("1100x700")
        ventana_cierre.configure(bg="#0f172a")
        ventana_cierre.resizable(False, False)
        ventana_cierre.transient(self)
        ventana_cierre.grab_set()
        
        # Centrar ventana
        ventana_cierre.geometry("+{}+{}".format(
            (ventana_cierre.winfo_screenwidth() // 2) - 450,
            (ventana_cierre.winfo_screenheight() // 2) - 350
        ))
        
        # Crear canvas con scroll
        canvas_cierre = tk.Canvas(ventana_cierre, bg="#1a3d75", highlightthickness=0)
        scrollbar_cierre = ttk.Scrollbar(ventana_cierre, orient="vertical", command=canvas_cierre.yview)
        frame_contenido = tk.Frame(canvas_cierre, bg="#1a3d75")
        
        canvas_cierre.configure(yscrollcommand=scrollbar_cierre.set)
        canvas_cierre.pack(side="left", fill="both", expand=True)
        scrollbar_cierre.pack(side="right", fill="y")
        configurar_scroll_mouse(canvas_cierre, scrollbar_cierre)
        
        canvas_window = canvas_cierre.create_window((0, 0), window=frame_contenido, anchor="nw")
        
        # Header principal
        self._crear_header_cierre(frame_contenido, fecha_hoy)
        
        # SECCIÓN CENTRAL: Frame horizontal para DESGLOSE DETALLADO (60%) + CONTROL DE CAJA (40%)
        seccion_central_frame = tk.Frame(frame_contenido, bg="#0f172a")
        seccion_central_frame.pack(fill="x", padx=20, pady=10)
        
        # Frame izquierdo para DESGLOSE DETALLADO (60% del ancho)
        desglose_container = tk.Frame(seccion_central_frame, bg="#0f172a")
        desglose_container.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Frame derecho para CONTROL DE CAJA (40% del ancho) 
        control_container = tk.Frame(seccion_central_frame, bg="#0f172a", width=300)
        control_container.pack(side="right", fill="y", padx=(10, 0))
        control_container.pack_propagate(False)  # Mantener el ancho fijo
        
        # 1. DESGLOSE DETALLADO (izquierda - 60%)
        self._crear_desglose_detallado(desglose_container, metricas)
        
        # 2. CONTROL DE CAJA (derecha superior - 40%)
        self._crear_control_caja(control_container, metricas)
        
        # 3. MÉTODOS DE PAGO (debajo de desglose, formato 2x2)
        self._crear_metodos_pago(desglose_container, metricas)
        
        # 4. BOTONES DE ACCIÓN (derecha, debajo de control de caja)
        self._crear_botones_cierre(control_container, metricas, ventana_cierre)
        
        # 5. MÉTRICAS DE VENTAS Y BALANCE EMPRESARIAL (abajo del todo)
        self._crear_metricas_y_balance_horizontal(frame_contenido, metricas)
        
        # Configurar scroll
        frame_contenido.update_idletasks()
        canvas_cierre.configure(scrollregion=canvas_cierre.bbox("all"))
        
        def configurar_scroll(event):
            canvas_cierre.configure(scrollregion=canvas_cierre.bbox("all"))
            canvas_width = event.width
            canvas_cierre.itemconfig(canvas_window, width=canvas_width)
        
        canvas_cierre.bind('<Configure>', configurar_scroll)

    def _crear_header_cierre(self, parent, fecha):
        """Crea el header del informe de cierre con diseño moderno y efectos glow"""
        # Frame principal con gradiente y borde glow
        header_frame = tk.Frame(parent, bg="#0a0f1a", relief="flat", bd=0)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Marco interno con efecto glow
        marco_interno = tk.Frame(header_frame, bg="#1a1f2e", relief="flat", bd=0)
        marco_interno.pack(fill="x", padx=2, pady=2)
        
        # Borde glow superior
        borde_glow = tk.Frame(marco_interno, bg="#00c9df", height=3)
        borde_glow.pack(fill="x", pady=(0, 15))
        
        # Contenedor del contenido con layout horizontal para título y fecha
        contenido_frame = tk.Frame(marco_interno, bg="#1a1f2e")
        contenido_frame.pack(fill="x", padx=20, pady=15)
        
        # Frame para el título (centrado)
        titulo_frame = tk.Frame(contenido_frame, bg="#1a1f2e")
        titulo_frame.pack(anchor="center")
        
        # Título principal con efecto neon (centrado)
        lbl_titulo = tk.Label(titulo_frame, text=f"📊 INFORME DE CIERRE {fecha.strftime('%d/%m/%Y')}", 
                             font=("Montserrat", 22, "bold"), 
                             bg="#1a1f2e", fg="#00c9df")
        lbl_titulo.pack()
        
        # Línea decorativa
        linea_decorativa = tk.Frame(contenido_frame, bg="#00c9df", height=2)
        linea_decorativa.pack(fill="x", pady=(10, 10))
        


    def _crear_metricas_ventas(self, parent, metricas):
        """Crea la sección de métricas de ventas"""
        # Frame contenedor
        ventas_frame = tk.Frame(parent, bg="#0f172a")
        ventas_frame.pack(fill="x", padx=20, pady=5)
        
        # Marco izquierdo - Métricas Ventas
        marco_ventas = tk.Frame(ventas_frame, bg="#1f2937", relief="solid", bd=1)
        marco_ventas.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Header
        header_ventas = tk.Label(marco_ventas, text="📈 MÉTRICAS VENTAS", 
                                font=("Montserrat", 14, "bold"), 
                                bg="#4f46e5", fg="#ffffff", pady=8)
        header_ventas.pack(fill="x")
        
        # Métricas
        metricas_ventas = [
            ("Cantidad de Ventas:", f"{metricas['cantidad_ventas']}"),
            ("Productos Vendidos:", f"{metricas['productos_vendidos']}"),
            ("Producto Más Vendido:", f"{metricas['producto_mas_vendido'][0]}\n({metricas['producto_mas_vendido'][1]} uds)")
        ]
        
        for etiqueta, valor in metricas_ventas:
            frame_metrica = tk.Frame(marco_ventas, bg="#1f2937")
            frame_metrica.pack(fill="x", padx=15, pady=5)
            
            lbl_etiqueta = tk.Label(frame_metrica, text=etiqueta, 
                                   font=("Montserrat", 10, "bold"), 
                                   bg="#1f2937", fg="#e5e7eb")
            lbl_etiqueta.pack(anchor="w")
            
            lbl_valor = tk.Label(frame_metrica, text=valor, 
                                font=("Montserrat", 11), 
                                bg="#1f2937", fg="#ffffff")
            lbl_valor.pack(anchor="w", padx=(10, 0))

    def _crear_metricas_financieras(self, parent, metricas):
        """Crea la sección de métricas financieras"""
        # Marco derecho - Métricas Financieras
        marco_financiero = tk.Frame(parent.master.children[list(parent.master.children.keys())[-1]], bg="#1f2937", relief="solid", bd=1)
        marco_financiero.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Header
        header_financiero = tk.Label(marco_financiero, text="💰 MÉTRICAS FINANCIERAS", 
                                    font=("Montserrat", 14, "bold"), 
                                    bg="#059669", fg="#ffffff", pady=8)
        header_financiero.pack(fill="x")
        
        # Métricas financieras
        metricas_financieras = [
            ("Monto Total Ventas:", self.formato_moneda(metricas['monto_total_ventas'])),
            ("Monto Total Gastos:", self.formato_moneda(metricas['monto_total_gastos'])),
            ("Monto Total IVA:", self.formato_moneda(metricas['monto_total_iva'])),
            ("Promedio por Venta:", self.formato_moneda(metricas['promedio_venta']))
        ]
        
        for etiqueta, valor in metricas_financieras:
            frame_metrica = tk.Frame(marco_financiero, bg="#1f2937")
            frame_metrica.pack(fill="x", padx=15, pady=5)
            
            lbl_etiqueta = tk.Label(frame_metrica, text=etiqueta, 
                                   font=("Montserrat", 10, "bold"), 
                                   bg="#1f2937", fg="#e5e7eb")
            lbl_etiqueta.pack(anchor="w")
            
            lbl_valor = tk.Label(frame_metrica, text=valor, 
                                font=("Montserrat", 11), 
                                bg="#1f2937", fg="#ffffff")
            lbl_valor.pack(anchor="w", padx=(10, 0))

    def _crear_balance_empresarial(self, parent, metricas):
        """Crea la sección de balance empresarial"""
        balance_frame = tk.Frame(parent, bg="#1f2937", relief="solid", bd=1)
        balance_frame.pack(fill="y", padx=20, pady=10)
        
        # Header
        header_balance = tk.Label(balance_frame, text="💼 BALANCE EMPRESARIAL", 
                                 font=("Montserrat", 16, "bold"), 
                                 bg="#f59e0b", fg="#000000", pady=10)
        header_balance.pack(fill="x")
        
        # Métricas principales
        monto_facturado_frame = tk.Frame(balance_frame, bg="#1f2937")
        monto_facturado_frame.pack(fill="x", padx=20, pady=10)
        
        lbl_facturado = tk.Label(monto_facturado_frame, 
                                text=f"Monto Facturado del Día: {self.formato_moneda(metricas['monto_facturado'])} (Ventas - Gastos)", 
                                font=("Montserrat", 12, "bold"), 
                                bg="#1f2937", fg="#ffffff")
        lbl_facturado.pack(anchor="w")
        
        lbl_ganancia = tk.Label(monto_facturado_frame, 
                               text=f"Balance Ganancia Real: {self.formato_moneda(metricas['balance_ganancia'])} (Ventas - Costos - Gastos)", 
                               font=("Montserrat", 12, "bold"), 
                               bg="#1f2937", fg="#ffffff")
        lbl_ganancia.pack(anchor="w", pady=(5, 0))
        
        # Indicadores en tres columnas
        indicadores_frame = tk.Frame(balance_frame, bg="#1f2937")
        indicadores_frame.pack(fill="x", padx=20, pady=10)
        
        # Margen Bruto
        margen_frame = tk.Frame(indicadores_frame, bg="#374151", relief="solid", bd=1)
        margen_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        lbl_margen_titulo = tk.Label(margen_frame, text="Margen Bruto:", 
                                    font=("Montserrat", 10, "bold"), 
                                    bg="#374151", fg="#e5e7eb")
        lbl_margen_titulo.pack(pady=(8, 2))
        
        lbl_margen_valor = tk.Label(margen_frame, text=f"{metricas['margen_bruto']:.1f}%", 
                                   font=("Montserrat", 14, "bold"), 
                                   bg="#374151", fg="#ffffff")
        lbl_margen_valor.pack(pady=(0, 8))
        
        # ROI del Día
        roi_frame = tk.Frame(indicadores_frame, bg="#374151", relief="solid", bd=1)
        roi_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        lbl_roi_titulo = tk.Label(roi_frame, text="ROI del Día:", 
                                 font=("Montserrat", 10, "bold"), 
                                 bg="#374151", fg="#e5e7eb")
        lbl_roi_titulo.pack(pady=(8, 2))
        
        lbl_roi_valor = tk.Label(roi_frame, text=f"{metricas['roi_dia']:.1f}%", 
                                font=("Montserrat", 14, "bold"), 
                                bg="#374151", fg="#ffffff")
        lbl_roi_valor.pack(pady=(0, 8))
        
        # Eficiencia Operativa
        eficiencia_frame = tk.Frame(indicadores_frame, bg="#374151", relief="solid", bd=1)
        eficiencia_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        lbl_eficiencia_titulo = tk.Label(eficiencia_frame, text="Eficiencia Operativa:", 
                                        font=("Montserrat", 10, "bold"), 
                                        bg="#374151", fg="#e5e7eb")
        lbl_eficiencia_titulo.pack(pady=(8, 2))
        
        # Color de eficiencia según valor
        color_eficiencia = "#059669" if metricas['eficiencia_operativa'] == "Alta" else "#f59e0b" if metricas['eficiencia_operativa'] == "Media" else "#ef4444"
        
        lbl_eficiencia_valor = tk.Label(eficiencia_frame, text=metricas['eficiencia_operativa'], 
                                       font=("Montserrat", 14, "bold"), 
                                       bg="#374151", fg=color_eficiencia)
        lbl_eficiencia_valor.pack(pady=(0, 8))

    def _crear_desglose_detallado(self, parent, metricas):
        """Crea la sección de desglose detallado con diseño moderno"""
        # Frame principal con fondo oscuro - ALTURA OPTIMIZADA
        desglose_frame = tk.Frame(parent, bg="#0a0f1a", relief="flat", bd=0, height=350)
        desglose_frame.pack(fill="both", expand=True, padx=20, pady=10)
        desglose_frame.pack_propagate(False)  # Mantener altura fija
        
        # Marco interno con diseño profesional - BORDE SUTIL
        marco_interno = tk.Frame(desglose_frame, bg="#1a1f2e", relief="solid", bd=1)
        marco_interno.pack(fill="both", expand=True, padx=3, pady=3)
        marco_interno.config(highlightbackground="#3b82f6", highlightcolor="#3b82f6", highlightthickness=2)
        
        # Header con efecto neon mejorado
        header_desglose = tk.Label(marco_interno, text="📊 DESGLOSE DETALLADO", 
                                  font=("Montserrat", 18, "bold"), 
                                  bg="#1a1f2e", fg="#60a5fa", pady=15)
        header_desglose.pack(fill="x")
        
        # Línea separadora elegante
        separador = tk.Frame(marco_interno, bg="#3b82f6", height=2)
        separador.pack(fill="x", padx=15, pady=(0, 10))
        
        # Top 5 productos más vendidos
        if metricas['ventas_detalle']:
            # Calcular top productos
            productos_vendidos = {}
            for venta in metricas['ventas_detalle']:
                for item in venta.items:
                    key = f"{item['producto'].descripcion} {item['producto'].color} {item['producto'].talle}"
                    if key not in productos_vendidos:
                        productos_vendidos[key] = {
                            'cantidad': 0,
                            'total_vendido': 0,
                            'costo_total': 0,
                            'producto': item['producto']
                        }
                    productos_vendidos[key]['cantidad'] += item['cantidad']
                    productos_vendidos[key]['total_vendido'] += item['cantidad'] * item['precio']
                    productos_vendidos[key]['costo_total'] += item['cantidad'] * item['producto'].precio_costo
            
            # Ordenar por cantidad vendida
            top_productos = sorted(productos_vendidos.items(), key=lambda x: x[1]['cantidad'], reverse=True)[:5]
            
            if top_productos:
                tabla_frame = tk.Frame(marco_interno, bg="#1a1f2e")
                tabla_frame.pack(fill="both", expand=True, padx=15, pady=(5, 20))
                
                # Headers de tabla con estilo moderno y profesional
                headers = ["Producto", "Cant.", "Vendido", "Costo", "Margen"]
                header_row = tk.Frame(tabla_frame, bg="#2563eb", relief="flat", bd=0)
                header_row.pack(fill="x", pady=(0, 5))
                
                for i, header in enumerate(headers):
                    width = [30, 8, 15, 15, 10][i]
                    lbl_header = tk.Label(header_row, text=header, 
                                         font=("Montserrat", 12, "bold"), 
                                         bg="#2563eb", fg="#ffffff", width=width, pady=8)
                    lbl_header.pack(side="left", padx=1)
                
                # Filas de datos con alternancia de colores profesional
                for idx, (nombre, datos) in enumerate(top_productos):
                    margen = ((datos['total_vendido'] - datos['costo_total']) / datos['total_vendido'] * 100) if datos['total_vendido'] > 0 else 0
                    
                    # Color alternado para las filas
                    bg_color = "#1e293b" if idx % 2 == 0 else "#0f172a"
                    
                    row_frame = tk.Frame(tabla_frame, bg=bg_color, relief="flat", bd=0)
                    row_frame.pack(fill="x", pady=1)
                    
                    valores = [
                        nombre[:28] + "..." if len(nombre) > 28 else nombre,
                        str(datos['cantidad']),
                        self.formato_moneda(datos['total_vendido']),
                        self.formato_moneda(datos['costo_total']),
                        f"{margen:.1f}%"
                    ]
                    
                    for i, valor in enumerate(valores):
                        width = [30, 8, 15, 15, 10][i]
                        # Color del texto según el tipo de dato
                        text_color = "#e5e7eb"
                        if i == 4:  # Margen
                            text_color = "#10b981" if margen > 30 else "#f59e0b" if margen > 15 else "#ef4444"
                        elif i in [2, 3]:  # Montos
                            text_color = "#93c5fd"
                            
                        lbl_valor = tk.Label(row_frame, text=valor, 
                                           font=("Montserrat", 11), 
                                           bg=bg_color, fg=text_color, width=width, pady=6)
                        lbl_valor.pack(side="left", padx=1)
        else:
            lbl_sin_datos = tk.Label(marco_interno, text="No hay ventas para mostrar desglose detallado", 
                                    font=("Montserrat", 14, "bold"), 
                                    bg="#1a1f2e", fg="#e5e7eb")
            lbl_sin_datos.pack(expand=True, pady=50)

    def _crear_control_caja(self, parent, metricas):
        """Crea la sección de control de caja con diseño moderno y efectos glow"""
        # Frame principal con fondo oscuro - ALTURA REDUCIDA PARA TRES BLOQUES
        control_frame = tk.Frame(parent, bg="#0a0f1a", relief="flat", bd=0, height=280)
        control_frame.pack(fill="both", expand=True, padx=30, pady=5)
        control_frame.pack_propagate(False)  # Mantener altura fija
        
        # Marco interno con glow
        marco_interno = tk.Frame(control_frame, bg="#1a1f2e", relief="solid", bd=1, highlightbackground="#3b82f6", highlightcolor="#3b82f6", highlightthickness=2)
        marco_interno.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Header con efecto neon - REDUCIR TAMAÑO
        header_control = tk.Label(marco_interno, text="💰 CONTROL DE CAJA", 
                                 font=("Montserrat", 15, "bold"), 
                                 bg="#1a1f2e", fg="#60a5fa", pady=3)
        header_control.pack(fill="x")
        separador_control = tk.Frame(marco_interno, bg="#3b82f6", height=2)
        separador_control.pack(fill="x", padx=15, pady=(0, 10))
        
        # Contenedor principal vertical (3 bloques apilados) - MENOS PADDING
        contenedor_control = tk.Frame(marco_interno, bg="#1a1f2e")
        contenedor_control.pack(fill="both", expand=True, padx=8, pady=(5, 5))
        
        # INGRESOS (superior) - Verde - ALTURA FIJA
        facturacion_frame = tk.Frame(contenedor_control, bg="#03985a", relief="flat", bd=0, height=70)
        facturacion_frame.pack(fill="x", pady=(0, 3))
        facturacion_frame.pack_propagate(False)
        
        # Efecto glow para ingresos
        facturacion_glow = tk.Frame(facturacion_frame, bg="#00ff88", height=2)
        facturacion_glow.pack(fill="x")
        
        lbl_facturacion_titulo = tk.Label(facturacion_frame, text="📈 INGRESOS", 
                                         font=("Montserrat", 12, "bold"), 
                                         bg="#03985a", fg="#ffffff", pady=3)
        lbl_facturacion_titulo.pack(fill="x")
        
        lbl_facturacion_monto = tk.Label(facturacion_frame, 
                                        text=self.formato_moneda(metricas['monto_total_ventas']), 
                                        font=("Montserrat", 18, "bold"), 
                                        bg="#03985a", fg="#ffffff")
        lbl_facturacion_monto.pack(pady=(2, 5))
        
        # GASTOS (medio) - Rojo - ALTURA FIJA
        gastos_frame = tk.Frame(contenedor_control, bg="#ef4444", relief="flat", bd=0, height=70)
        gastos_frame.pack(fill="x", pady=3)
        gastos_frame.pack_propagate(False)
        
        # Efecto glow para gastos
        gastos_glow = tk.Frame(gastos_frame, bg="#ff6b6b", height=2)
        gastos_glow.pack(fill="x")
        
        lbl_gastos_titulo = tk.Label(gastos_frame, text="💸 GASTOS", 
                                    font=("Montserrat", 12, "bold"), 
                                    bg="#ef4444", fg="#ffffff", pady=3)
        lbl_gastos_titulo.pack(fill="x")
        
        lbl_gastos_monto = tk.Label(gastos_frame, 
                                   text=self.formato_moneda(metricas['monto_total_gastos']), 
                                   font=("Montserrat", 18, "bold"), 
                                   bg="#ef4444", fg="#ffffff")
        lbl_gastos_monto.pack(pady=(2, 5))
        
        # TOTAL EN CAJA (inferior) - Naranja destacado - ALTURA FIJA
        balance_frame = tk.Frame(contenedor_control, bg="#f59e0b", relief="flat", bd=0, height=70)
        balance_frame.pack(fill="x", pady=(3, 0))
        balance_frame.pack_propagate(False)
        
        # Efecto glow para total en caja más prominente
        balance_glow = tk.Frame(balance_frame, bg="#ffd93d", height=2)
        balance_glow.pack(fill="x")
        
        lbl_balance_titulo = tk.Label(balance_frame, text="💼 TOTAL EN CAJA", 
                                     font=("Montserrat", 12, "bold"), 
                                     bg="#f59e0b", fg="#000000", pady=3)
        lbl_balance_titulo.pack(fill="x")
        
        lbl_balance_monto = tk.Label(balance_frame, 
                                    text=self.formato_moneda(metricas['monto_facturado']), 
                                    font=("Montserrat", 18, "bold"), 
                                    bg="#f59e0b", fg="#000000")
        lbl_balance_monto.pack(pady=(2, 5))

    def _crear_metodos_pago(self, parent, metricas):
        """Crea la sección de métodos de pago con diseño moderno"""
        # Frame principal con fondo oscuro
        metodos_frame = tk.Frame(parent, bg="#0a0f1a", relief="flat", bd=0)
        metodos_frame.pack(fill="x", padx=20, pady=10)
        
        # Marco interno con borde highlight
        marco_interno = tk.Frame(metodos_frame, bg="#1a1f2e", relief="solid", bd=1, highlightbackground="#3b82f6", highlightcolor="#3b82f6", highlightthickness=2)
        marco_interno.pack(fill="x", padx=3, pady=3)
        
        # Header con efecto neon
        header_metodos = tk.Label(marco_interno, text="💳 MÉTODOS DE PAGO", 
                                 font=("Montserrat", 18, "bold"), 
                                 bg="#1a1f2e", fg="#60a5fa", pady=15)
        header_metodos.pack(fill="x")
        separador_metodos = tk.Frame(marco_interno, bg="#3b82f6", height=2)
        separador_metodos.pack(fill="x", padx=15, pady=(0, 10))
        
        # Contenedor de métodos en grilla 2x2
        contenedor_metodos = tk.Frame(marco_interno, bg="#1a1f2e")
        contenedor_metodos.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        
        # Calcular métodos de pago
        metodos_pago = {}
        for venta in metricas['ventas_detalle']:
            forma_pago = getattr(venta, 'forma_pago', 'EFECTIVO')
            if forma_pago not in metodos_pago:
                metodos_pago[forma_pago] = 0
            metodos_pago[forma_pago] += sum(item['cantidad'] * item['precio'] for item in venta.items)
        
        # Crear widgets para cada método con estilo botón moderno en grilla 2x2
        colores_metodos = {
            'EFECTIVO': '#059669',
            'DÉBITO': '#4f46e5', 
            'CRÉDITO': '#f59e0b',
            'TRANSFERENCIA': '#8b5cf6',
            'QR': '#06b6d4',
            'OTROS': '#6b7280'
        }
        
        # Ordenar métodos para consistencia visual
        metodos_items = list(metodos_pago.items())
        for idx, (metodo, monto) in enumerate(metodos_items):
            color = colores_metodos.get(metodo, '#6b7280')
            row = idx // 2
            col = idx % 2
            
            # Frame del método con efecto glow
            metodo_frame = tk.Frame(contenedor_metodos, bg=color, relief="flat", bd=0)
            metodo_frame.grid(row=row, column=col, sticky="nsew", padx=6, pady=6)
            
            # Configurar pesos de la grilla
            contenedor_metodos.grid_rowconfigure(row, weight=1)
            contenedor_metodos.grid_columnconfigure(col, weight=1)
            
            # Efecto glow superior
            glow_frame = tk.Frame(metodo_frame, bg="#ffffff", height=2)
            glow_frame.pack(fill="x")
            
            lbl_metodo = tk.Label(metodo_frame, text=metodo, 
                                 font=("Montserrat", 14, "bold"), 
                                 bg=color, fg="#ffffff", pady=10)
            lbl_metodo.pack(fill="x")
            
            lbl_monto = tk.Label(metodo_frame, text=self.formato_moneda(monto), 
                                font=("Montserrat", 16, "bold"), 
                                bg=color, fg="#ffffff")
            lbl_monto.pack(pady=(0, 10))

    def _crear_metricas_y_balance_horizontal(self, parent, metricas):
        """Crea las métricas de ventas y balance empresarial en layout horizontal con estilo botón moderno"""
        # Frame contenedor principal
        metricas_balance_frame = tk.Frame(parent, bg="#0a0f1a")
        metricas_balance_frame.pack(fill="x", padx=20, pady=10)
        
        # MÉTRICAS DE VENTAS (izquierda) - Estilo botón moderno
        metricas_frame = tk.Frame(metricas_balance_frame, bg="#0a0f1a", relief="flat", bd=0)
        metricas_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Marco interno con glow
        marco_metricas = tk.Frame(metricas_frame, bg="#1a1f2e", relief="flat", bd=0)
        marco_metricas.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Header métricas con efecto neon
        header_metricas = tk.Label(marco_metricas, text="📈 MÉTRICAS DE VENTAS", 
                                  font=("Montserrat", 16, "bold"), 
                                  bg="#1a1f2e", fg="#00c9df", pady=12)
        header_metricas.pack(fill="x")
        
        # Contenedor de métricas
        contenedor_metricas = tk.Frame(marco_metricas, bg="#1a1f2e")
        contenedor_metricas.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Métricas de ventas en estilo botón
        metricas_ventas = [
            ("Cantidad de Ventas:", f"{metricas['cantidad_ventas']}", "#4f46e5"),
            ("Productos Vendidos:", f"{metricas['productos_vendidos']}", "#059669"),
            ("Producto Más Vendido:", f"{metricas['producto_mas_vendido'][0]}\n({metricas['producto_mas_vendido'][1]} uds)", "#f59e0b"),
            ("Promedio por Venta:", self.formato_moneda(metricas['promedio_venta']), "#8b5cf6")
        ]
        
        for etiqueta, valor, color in metricas_ventas:
            # Frame del botón métrica
            boton_metrica = tk.Frame(contenedor_metricas, bg=color, relief="flat", bd=0)
            boton_metrica.pack(fill="x", pady=3)
            
            # Efecto glow superior
            glow_frame = tk.Frame(boton_metrica, bg="#ffffff", height=1)
            glow_frame.pack(fill="x")
            
            # Contenido del botón
            contenido_boton = tk.Frame(boton_metrica, bg=color)
            contenido_boton.pack(fill="x", padx=12, pady=8)
            
            lbl_etiqueta = tk.Label(contenido_boton, text=etiqueta, 
                                   font=("Montserrat", 11, "bold"), 
                                   bg=color, fg="#ffffff")
            lbl_etiqueta.pack(anchor="w")
            
            lbl_valor = tk.Label(contenido_boton, text=valor, 
                                font=("Montserrat", 14, "bold"), 
                                bg=color, fg="#ffffff")
            lbl_valor.pack(anchor="w", pady=(2, 0))
        
        # BALANCE EMPRESARIAL (derecha) - Solo 3 métricas en estilo botón
        balance_frame = tk.Frame(metricas_balance_frame, bg="#0a0f1a", relief="flat", bd=0)
        balance_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Marco interno con glow
        marco_balance = tk.Frame(balance_frame, bg="#1a1f2e", relief="flat", bd=0)
        marco_balance.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Header balance con efecto neon
        header_balance = tk.Label(marco_balance, text="💼 BALANCE EMPRESARIAL", 
                                 font=("Montserrat", 16, "bold"), 
                                 bg="#1a1f2e", fg="#00c9df", pady=12)
        header_balance.pack(fill="x")
        
        # Contenedor de balance
        contenedor_balance = tk.Frame(marco_balance, bg="#1a1f2e")
        contenedor_balance.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Solo 3 métricas principales en estilo botón
        balance_metricas = [
            ("Margen Bruto:", f"{metricas['margen_bruto']:.1f}%", "#059669"),
            ("ROI del Día:", f"{metricas['roi_dia']:.1f}%", "#4f46e5"),
            ("Eficiencia Operativa:", metricas['eficiencia_operativa'], "#f59e0b")
        ]
        
        for etiqueta, valor, color in balance_metricas:
            # Frame del botón balance
            boton_balance = tk.Frame(contenedor_balance, bg=color, relief="flat", bd=0)
            boton_balance.pack(fill="x", pady=3)
            
            # Efecto glow superior
            glow_frame = tk.Frame(boton_balance, bg="#ffffff", height=1)
            glow_frame.pack(fill="x")
            
            # Contenido del botón
            contenido_boton = tk.Frame(boton_balance, bg=color)
            contenido_boton.pack(fill="x", padx=12, pady=8)
            
            lbl_etiqueta = tk.Label(contenido_boton, text=etiqueta, 
                                   font=("Montserrat", 11, "bold"), 
                                   bg=color, fg="#ffffff")
            lbl_etiqueta.pack(anchor="w")
            
            # Color especial para eficiencia operativa
            if "Eficiencia" in etiqueta:
                color_eficiencia = "#059669" if valor == "Alta" else "#f59e0b" if valor == "Media" else "#ef4444"
                lbl_valor = tk.Label(contenido_boton, text=valor, 
                                    font=("Montserrat", 14, "bold"), 
                                    bg=color, fg=color_eficiencia)
            else:
                lbl_valor = tk.Label(contenido_boton, text=valor, 
                                    font=("Montserrat", 14, "bold"), 
                                    bg=color, fg="#ffffff")
            lbl_valor.pack(anchor="w", pady=(2, 0))

    def _crear_botones_cierre(self, parent, metricas, ventana):
        """Crea los botones de acción del cierre con diseño moderno"""
        # Frame principal con fondo oscuro
        botones_frame = tk.Frame(parent, bg="#0a0f1a", relief="flat", bd=0)
        botones_frame.pack(fill="x", padx=20, pady=10)
        
        # Marco interno con borde highlight, estilo consistente
        marco_botones = tk.Frame(botones_frame, bg="#1a1f2e", relief="solid", bd=1, highlightbackground="#3b82f6", highlightcolor="#3b82f6", highlightthickness=2)
        marco_botones.pack(fill="x", padx=3, pady=3)
        
        # Header con separador
        header_botones = tk.Label(marco_botones, text="⚙️ ACCIONES", 
                                 font=("Montserrat", 15, "bold"), 
                                 bg="#1a1f2e", fg="#60a5fa", pady=8)
        header_botones.pack(fill="x")
        sep_botones = tk.Frame(marco_botones, bg="#3b82f6", height=2)
        sep_botones.pack(fill="x", padx=15, pady=(0, 10))
        
        # Contenedor de botones en columna
        contenedor_botones = tk.Frame(marco_botones, bg="#1a1f2e")
        contenedor_botones.pack(fill="x", padx=15, pady=10)
        
        # Botón Cerrar Caja - Destacado
        btn_cerrar = tk.Button(contenedor_botones, text="🚀 CERRAR CAJA", 
                              font=("Montserrat", 13, "bold"), 
                              bg="#ef4444", fg="#ffffff", 
                              command=lambda: self.confirmar_cierre_caja(ventana, metricas),
                              cursor="hand2", width=22, height=2, relief="flat", bd=0)
        aplicar_estilo_moderno_boton(btn_cerrar, "danger", True)
        btn_cerrar.pack(fill="x", pady=(0, 10))
        
        # Botón Descargar PDF 
        btn_pdf = tk.Button(contenedor_botones, text="📄 DESCARGAR PDF", 
                           font=("Montserrat", 12, "bold"), 
                           bg="#4f46e5", fg="#ffffff", 
                           command=lambda: self.generar_pdf_cierre(metricas),
                           cursor="hand2", width=22, height=2, relief="flat", bd=0)
        aplicar_estilo_moderno_boton(btn_pdf, "primario", True)
        btn_pdf.pack(fill="x", pady=6)
        
        # Botón Ver Histórico
        btn_historico = tk.Button(contenedor_botones, text="📊 VER HISTÓRICO", 
                                 font=("Montserrat", 12, "bold"), 
                                 bg="#6b7280", fg="#ffffff", 
                                 command=self.mostrar_reportes,
                                 cursor="hand2", width=22, height=2, relief="flat", bd=0)
        aplicar_estilo_moderno_boton(btn_historico, "secundario", True)
        btn_historico.pack(fill="x", pady=6)

    def confirmar_cierre_caja(self, ventana, metricas):
        """Confirma y ejecuta el cierre de caja"""
        resultado = messagebox.askyesno("Confirmar Cierre de Caja", 
                                       "¿Está seguro de cerrar la caja?\n\n" +
                                       "Esta acción archivará todas las ventas y gastos del día.\n" +
                                       "No se podrá deshacer.")
        
        if resultado:
            fecha = metricas['fecha']
            # Archivar ventas y gastos
            self.sistema.archivar_ventas_dia(fecha)
            self.sistema.archivar_gastos_dia(fecha)
            
            messagebox.showinfo("Cierre Completado", 
                               f"✅ Cierre de caja realizado exitosamente\n\n" +
                               f"Fecha: {fecha.strftime('%d/%m/%Y')}\n" +
                               f"Ventas archivadas: {metricas['cantidad_ventas']}\n" +
                               f"Gastos archivados: {len(metricas['gastos_detalle'])}")
            
            ventana.destroy()
            self.mostrar_ventas_dia()  # Refrescar pantalla

    def generar_pdf_cierre(self, metricas):
        """Genera PDF profesional del informe de cierre"""
        
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.units import inch
            
            # Nombre del archivo
            fecha = metricas['fecha']
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                initialfile=f"informe_cierre_{fecha.strftime('%Y%m%d')}_{datetime.datetime.now().strftime('%H%M%S')}.pdf"
            )
            
            if not filename:
                return None
            
            # Crear documento
            doc = SimpleDocTemplate(filename, pagesize=A4, topMargin=0.5*inch)
            story = []
            styles = getSampleStyleSheet()
            
            # Estilo personalizado para título
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                textColor=colors.HexColor('#0f172a'),
                alignment=1  # Centrado
            )
            
            # Estilo para subtítulos
            subtitle_style = ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Heading2'],
                fontSize=16,
                spaceAfter=20,
                textColor=colors.HexColor('#4f46e5'),
                alignment=0
            )
            
            # Título principal
            story.append(Paragraph("📊 INFORME DE CIERRE DIARIO", title_style))
            story.append(Paragraph("ALENIA GESTIÓN KONTROL+", styles['Normal']))
            story.append(Paragraph(f"Fecha: {fecha.strftime('%d/%m/%Y')}", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # === RESUMEN EJECUTIVO ===
            story.append(Paragraph("💼 RESUMEN EJECUTIVO", subtitle_style))
            
            resumen_data = [
                ['MÉTRICA', 'VALOR', 'INTERPRETACIÓN'],
                ['Cantidad de Ventas', str(metricas['cantidad_ventas']), 'Transacciones del día'],
                ['Productos Vendidos', str(metricas['productos_vendidos']), 'Unidades comercializadas'],
                ['Monto Total Ventas', self.formato_moneda(metricas['monto_total_ventas']), 'Ingresos brutos'],
                ['Monto Total Gastos', self.formato_moneda(metricas['monto_total_gastos']), 'Egresos operativos'],
                ['Balance Ganancia', self.formato_moneda(metricas['balance_ganancia']), 'Ganancia neta real'],
                ['Margen Bruto', f"{metricas['margen_bruto']:.1f}%", self._interpretar_margen(metricas['margen_bruto'])],
                ['ROI del Día', f"{metricas['roi_dia']:.1f}%", self._interpretar_roi(metricas['roi_dia'])],
                ['Eficiencia Operativa', metricas['eficiencia_operativa'], 'Rendimiento general']
            ]
            
            tabla_resumen = Table(resumen_data, colWidths=[2.5*inch, 1.5*inch, 2*inch])
            tabla_resumen.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4f46e5')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9)
            ]))
            
            story.append(tabla_resumen)
            story.append(Spacer(1, 20))
            
            # === ANÁLISIS FINANCIERO ===
            story.append(Paragraph("💰 ANÁLISIS FINANCIERO DETALLADO", subtitle_style))
            
            analisis_data = [
                ['CONCEPTO', 'MONTO', 'PORCENTAJE'],
                ['Ventas Totales', self.formato_moneda(metricas['monto_total_ventas']), '100.0%'],
                ['(-) Costos de Productos', self.formato_moneda(metricas['costo_total_productos']), f"{(metricas['costo_total_productos']/metricas['monto_total_ventas']*100):.1f}%" if metricas['monto_total_ventas'] > 0 else '0.0%'],
                ['(-) Gastos Operativos', self.formato_moneda(metricas['monto_total_gastos']), f"{(metricas['monto_total_gastos']/metricas['monto_total_ventas']*100):.1f}%" if metricas['monto_total_ventas'] > 0 else '0.0%'],
                ['(=) Ganancia Neta', self.formato_moneda(metricas['balance_ganancia']), f"{metricas['margen_bruto']:.1f}%"],
                ['IVA Incluido (21%)', self.formato_moneda(metricas['monto_total_iva']), '21.0%']
            ]
            
            tabla_analisis = Table(analisis_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
            tabla_analisis.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (0, 4), colors.lightgrey),
                ('BACKGROUND', (0, 4), (-1, 4), colors.HexColor('#f0f9ff')),  # Destacar ganancia neta
                ('FONTNAME', (0, 4), (-1, 4), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9)
            ]))
            
            story.append(tabla_analisis)
            story.append(Spacer(1, 20))
            
            # === PRODUCTOS MÁS VENDIDOS ===
            if metricas['ventas_detalle']:
                story.append(Paragraph("🏆 TOP PRODUCTOS DEL DÍA", subtitle_style))
                
                # Calcular top productos
                productos_vendidos = {}
                for venta in metricas['ventas_detalle']:
                    for item in venta.items:
                        key = f"{item['producto'].descripcion} {item['producto'].color} {item['producto'].talle}"
                        if key not in productos_vendidos:
                            productos_vendidos[key] = {
                                'cantidad': 0,
                                'total_vendido': 0,
                                'costo_total': 0
                            }
                        productos_vendidos[key]['cantidad'] += item['cantidad']
                        productos_vendidos[key]['total_vendido'] += item['cantidad'] * item['precio']
                        productos_vendidos[key]['costo_total'] += item['cantidad'] * item['producto'].precio_costo
                
                # Ordenar y tomar top 5
                top_productos = sorted(productos_vendidos.items(), key=lambda x: x[1]['cantidad'], reverse=True)[:5]
                
                if top_productos:
                    productos_data = [['PRODUCTO', 'CANTIDAD', 'VENDIDO', 'MARGEN']]
                    
                    for nombre, datos in top_productos:
                        margen = ((datos['total_vendido'] - datos['costo_total']) / datos['total_vendido'] * 100) if datos['total_vendido'] > 0 else 0
                        productos_data.append([
                            nombre[:35] + "..." if len(nombre) > 35 else nombre,
                            str(datos['cantidad']),
                            self.formato_moneda(datos['total_vendido']),
                            f"{margen:.1f}%"
                        ])
                    
                    tabla_productos = Table(productos_data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
                    tabla_productos.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f59e0b')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.lightcyan),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('FONTSIZE', (0, 1), (-1, -1), 9)
                    ]))
                    
                    story.append(tabla_productos)
                    story.append(Spacer(1, 20))
            
            # === GASTOS DEL DÍA ===
            if metricas['gastos_detalle']:
                story.append(Paragraph("GASTOS Y PAGOS", subtitle_style))
                
                gastos_data = [['MOTIVO', 'MONTO', 'USUARIO']]
                for gasto in metricas['gastos_detalle']:
                    gastos_data.append([
                        gasto.motivo[:40] + "..." if len(gasto.motivo) > 40 else gasto.motivo,
                        self.formato_moneda(gasto.monto),
                        gasto.usuario
                    ])
                
                # Agregar total
                gastos_data.append(['TOTAL GASTOS', self.formato_moneda(metricas['monto_total_gastos']), ''])
                
                tabla_gastos = Table(gastos_data, colWidths=[3*inch, 2*inch, 1*inch])
                tabla_gastos.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ef4444')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BACKGROUND', (0, 1), (0, -2), colors.mistyrose),
                    ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#fee2e2')),  # Destacar total
                    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 9)
                ]))
                
                story.append(tabla_gastos)
                story.append(Spacer(1, 20))
            
            # === RECOMENDACIONES ===
            story.append(Paragraph("🎯 RECOMENDACIONES ESTRATÉGICAS", subtitle_style))
            
            recomendaciones = self._generar_recomendaciones(metricas)
            for recomendacion in recomendaciones:
                story.append(Paragraph(f"• {recomendacion}", styles['Normal']))
                story.append(Spacer(1, 5))
            
            story.append(Spacer(1, 20))
            
            # Footer
            story.append(Paragraph("---", styles['Normal']))
            story.append(Paragraph(f"Reporte generado el {datetime.datetime.now().strftime('%d/%m/%Y a las %H:%M:%S')}", styles['Normal']))
            story.append(Paragraph("ALENIA GESTIÓN KONTROL+ v2.4 - Sistema de Gestión Inteligente", styles['Normal']))
            
            # Construir PDF
            doc.build(story)
            
            messagebox.showinfo("PDF Generado", f"✅ Informe PDF generado exitosamente\n\nArchivo guardado en:\n{filename}")
            return filename
            
        except ImportError:
            messagebox.showwarning("Dependencia Faltante", 
                                 "Para generar PDF necesita instalar ReportLab:\n\n" +
                                 "pip install reportlab\n\n" +
                                 "¿Desea instalar automáticamente?")
            return None
        except Exception as e:
            messagebox.showerror("Error PDF", f"Error al generar PDF:\n\n{e}")
            return None

    def _interpretar_margen(self, margen):
        """Interpreta el margen bruto"""
        if margen > 50:
            return "Excelente"
        elif margen > 30:
            return "Bueno"
        elif margen > 10:
            return "Regular"
        else:
            return "Bajo"

    def _interpretar_roi(self, roi):
        """Interpreta el ROI"""
        if roi > 200:
            return "Excelente"
        elif roi > 100:
            return "Bueno"
        elif roi > 50:
            return "Regular"
        else:
            return "Bajo"

    def _generar_recomendaciones(self, metricas):
        """Genera recomendaciones estratégicas basadas en las métricas"""
        recomendaciones = []
        
        # Análisis de ventas
        if metricas['cantidad_ventas'] == 0:
            recomendaciones.append("No se registraron ventas hoy. Considere estrategias de promoción y marketing.")
        elif metricas['cantidad_ventas'] < 5:
            recomendaciones.append("Pocas ventas registradas. Evalúe horarios de mayor afluencia y productos estrella.")
        
        # Análisis de margen
        if metricas['margen_bruto'] < 30:
            recomendaciones.append("Margen bruto bajo. Revise precios de venta y costos de productos.")
        elif metricas['margen_bruto'] > 60:
            recomendaciones.append("Excelente margen bruto. Mantenga esta estrategia de precios.")
        
        # Análisis de gastos
        if metricas['monto_total_gastos'] > metricas['monto_total_ventas'] * 0.3:
            recomendaciones.append("Gastos operativos elevados. Revise y optimice los costos fijos.")
        
        # Análisis de eficiencia
        if metricas['eficiencia_operativa'] == "Baja":
            recomendaciones.append("Eficiencia operativa baja. Enfoque en productos de mayor rotación.")
        elif metricas['eficiencia_operativa'] == "Alta":
            recomendaciones.append("Excelente eficiencia operativa. Considere expandir el inventario exitoso.")
        
        # Análisis de producto estrella
        if metricas['producto_mas_vendido'][1] > 5:
            recomendaciones.append(f"El producto '{metricas['producto_mas_vendido'][0]}' es muy popular. Asegure stock suficiente.")
        
        # Recomendación general si no hay específicas
        if not recomendaciones:
            recomendaciones.append("Rendimiento estable. Continúe monitoreando las métricas diariamente.")
            recomendaciones.append("Considere implementar promociones para incrementar las ventas.")
        
        return recomendaciones

    # FUNCIONES FALTANTES PARA LOS BOTONES DEL MENÚ
    def carga_masiva_productos(self):
        if not self.require_role(["admin"]):
            return
        import tkinter.filedialog as fd
        from tkinter import messagebox
        import csv
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        self._chip_volver(self.mostrar_menu_secundario)
        self._chip_logout()
        lbl_info = tk.Label(self.canvas_bg, text="Carga masiva de productos desde archivo CSV", font=("Montserrat", 15, "bold"), bg=COLOR_FONDO, fg=COLOR_CIAN)
        self.canvas_bg.create_window(640, 150, window=lbl_info, anchor="n")  # Ajustado para el logo
        def descargar_modelo():
            modelo = "marca,descripcion,color,talle,cantidad,precio_costo,porcentaje_venta,porcentaje_amigo\nNike,Remera,Rojo,M,10,1000,50,20\n"
            ruta = fd.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Guardar archivo modelo")
            if ruta:
                with open(ruta, "w", encoding="utf-8") as f:
                    f.write(modelo)
                messagebox.showinfo("Archivo guardado", f"Archivo modelo guardado en:\n{ruta}")
        def parse_cantidad(val):
            if val == "-":
                return 0
            if val == "" or val is None:
                raise ValueError("Hay campos numéricos vacíos. Complete o coloque '-' para cero.")
            s = str(val).strip()
            neg = s.startswith("-")
            # Eliminar símbolos, separadores y espacios
            s = s.replace("$", "").replace("%", "").replace(" ", "").replace(".", "").replace(",", "")
            if not s.isdigit():
                raise ValueError(f"Cantidad inválida: {val}")
            n = int(s)
            return -n if neg else n

        def parse_precio(val):
            if val == "-":
                return 0.0
            if val == "" or val is None:
                raise ValueError("Hay campos numéricos vacíos. Complete o coloque '-' para cero.")
            s = str(val).strip().replace(" ", "").replace("$", "")
            # Si hay coma, se asume notación latam: '.' miles, ',' decimal
            if "," in s:
                s = s.replace(".", "").replace(",", ".")
            else:
                # Sin coma: tratar '.' como separador de miles para precios
                s = s.replace(".", "")
            return float(s) if s else 0.0

        def parse_porcentaje(val):
            if val == "-":
                return 0.0
            if val == "" or val is None:
                raise ValueError("Hay campos numéricos vacíos. Complete o coloque '-' para cero.")
            s = str(val).strip().replace("%", "").replace(" ", "")
            # Aceptar tanto '50,5' como '50.5'
            if "," in s and "." in s:
                # Interpretar '.' como miles y ',' como decimal
                s = s.replace(".", "").replace(",", ".")
            elif "," in s:
                s = s.replace(",", ".")
            # else: '.' ya es decimal
            return float(s) if s else 0.0
        def cargar_csv():
            ruta = fd.askopenfilename(filetypes=[("CSV files", "*.csv")], title="Seleccionar archivo CSV")
            if not ruta:
                return
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    requeridos = ["marca", "descripcion", "color", "talle", "cantidad", "precio_costo", "porcentaje_venta", "porcentaje_amigo"]
                    nuevos = []
                    for row in reader:
                        if not all(k in row for k in requeridos):
                            raise ValueError("El archivo no tiene todas las columnas requeridas.")
                        nuevos.append((
                            row["marca"],
                            row["descripcion"],
                            row["color"],
                            row["talle"],
                            parse_cantidad(row["cantidad"]),
                            parse_precio(row["precio_costo"]),
                            parse_porcentaje(row["porcentaje_venta"]),
                            parse_porcentaje(row["porcentaje_amigo"])
                        ))
                # Insertar en memoria y guardar una sola vez
                for args in nuevos:
                    self.sistema.productos.append(Producto(*args))
                self.sistema.guardar_productos()
                messagebox.showinfo("Éxito", f"Productos cargados correctamente: {len(nuevos)} ítems.")
                self.mostrar_menu_secundario()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")
        btn_descargar = tk.Button(self.canvas_bg, text="⬇️ Descargar archivo modelo CSV", font=("Montserrat", 12, "bold"), bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, bd=0, relief="flat", command=descargar_modelo)
        self.canvas_bg.create_window(640, 220, window=btn_descargar, width=320, height=40, anchor="n")  # Ajustado
        btn_cargar = tk.Button(self.canvas_bg, text="📁 Seleccionar y cargar archivo CSV", font=("Montserrat", 12, "bold"), bg="#4CAF50", fg="#ffffff", bd=0, relief="flat", command=cargar_csv)
        self.canvas_bg.create_window(640, 280, window=btn_cargar, width=320, height=40, anchor="n")  # Ajustado
        self.pantalla_widgets.extend([lbl_info, btn_descargar, btn_cargar])

    def mostrar_reportes(self):
        """Pantalla de reportes con diseño moderno y filtros avanzados"""
        print("[DEBUG] mostrar_reportes() llamado - main.py:3554")
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        self._chip_volver(self.mostrar_menu_secundario)
        self._chip_logout()
        
        # Variable global para almacenar datos filtrados
        global datos_filtrados_actuales
        datos_filtrados_actuales = None
        
        widgets = []
        
        # === HEADER MODERNO ===
        header_frame = tk.Frame(self.canvas_bg, bg="#0f172a", height=40)
        self.canvas_bg.create_window(640, 30, window=header_frame, width=600, height=80, anchor="center")
        
        lbl_titulo = tk.Label(header_frame, text="📊 REPORTES Y ANÁLISIS", 
                             font=("Montserrat", 18, "bold"), bg="#0f172a", fg="#00ff88")
        lbl_titulo.pack(pady=5)
        
        # === PANEL DE FILTROS AVANZADOS MODERNO ===
        filters_frame = tk.Frame(self.canvas_bg, bg="#0a0f1a", relief="flat", bd=0)
        self.canvas_bg.create_window(640, 120, window=filters_frame, width=900, height=135, anchor="center")
        
        # Marco interno con borde highlight
        marco_filtros = tk.Frame(filters_frame, bg="#1a1f2e", relief="solid", bd=1, highlightbackground="#3b82f6", highlightcolor="#3b82f6", highlightthickness=2)
        marco_filtros.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Header compacto
        header_filtros = tk.Label(marco_filtros, text="🔍 FILTROS DE BÚSQUEDA AVANZADA", 
                                 font=("Montserrat", 14, "bold"), 
                                 bg="#1a1f2e", fg="#60a5fa", pady=6)
        header_filtros.pack(fill="x")
        
        # Contenedor principal de filtros
        filters_container = tk.Frame(marco_filtros, bg="#1a1f2e")
        filters_container.pack(fill="x", padx=12, pady=(2, 6))
        
        # === FILTROS EN LÍNEA HORIZONTAL ===
        filtros_linea = tk.Frame(filters_container, bg="#1a1f2e")
        filtros_linea.pack(fill="x", pady=(0, 5))
        
        # FECHA DESDE - Diseño moderno
        desde_container = tk.Frame(filtros_linea, bg="#1a1f2e")
        desde_container.pack(side="left", padx=(0, 5))
        
        lbl_desde = tk.Label(desde_container, text="📅 Desde:", 
                            font=("Montserrat", 12, "bold"), 
                            bg="#1a1f2e", fg="#e5e7eb")
        lbl_desde.pack(anchor="w", pady=(0, 5))
        
        # Frame del input desde con glow
        input_desde_frame = tk.Frame(desde_container, bg="#374151", relief="flat", bd=0)
        input_desde_frame.pack(fill="x")
        
        ent_desde = tk.Entry(input_desde_frame, font=("Montserrat", 12), 
                            bg="#ffffff", fg="#000000", 
                            bd=0, relief="flat", width=12, justify="center")
        ent_desde.pack(side="left", padx=8, pady=6)
        ent_desde.insert(0, "2000-01-01")
        
        # Botón calendario desde con efecto glow
        btn_cal_desde = tk.Button(input_desde_frame, text="📅", 
                                 font=("Montserrat", 12, "bold"), 
                                 bg="#4f46e5", fg="#ffffff", 
                                 bd=0, relief="flat", cursor="hand2",
                                 width=3, height=1)
        btn_cal_desde.pack(side="right", padx=2, pady=2)
        
        # FECHA HASTA - Diseño moderno
        hasta_container = tk.Frame(filtros_linea, bg="#1a1f2e")
        hasta_container.pack(side="left", padx=(0, 15))
        
        lbl_hasta = tk.Label(hasta_container, text="📅 Hasta:", 
                            font=("Montserrat", 12, "bold"), 
                            bg="#1a1f2e", fg="#e5e7eb")
        lbl_hasta.pack(anchor="w", pady=(0, 5))
        
        # Frame del input hasta con glow
        input_hasta_frame = tk.Frame(hasta_container, bg="#374151", relief="flat", bd=0)
        input_hasta_frame.pack(fill="x")
        
        ent_hasta = tk.Entry(input_hasta_frame, font=("Montserrat", 12), 
                            bg="#ffffff", fg="#000000", 
                            bd=0, relief="flat", width=12, justify="center")
        ent_hasta.pack(side="left", padx=8, pady=6)
        ent_hasta.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
        
        # Botón calendario hasta con efecto glow
        btn_cal_hasta = tk.Button(input_hasta_frame, text="📅", 
                                 font=("Montserrat", 12, "bold"), 
                                 bg="#4f46e5", fg="#ffffff", 
                                 bd=0, relief="flat", cursor="hand2",
                                 width=3, height=1)
        btn_cal_hasta.pack(side="right", padx=2, pady=2)
        
        # FILTRO FORMA DE PAGO
        pago_container = tk.Frame(filtros_linea, bg="#1a1f2e")
        pago_container.pack(side="left", padx=(0, 15))
        
        lbl_pago = tk.Label(pago_container, text="💳 Pago:", 
                           font=("Montserrat", 12, "bold"), 
                           bg="#1a1f2e", fg="#e5e7eb")
        lbl_pago.pack(anchor="w", pady=(0, 5))
        
        combo_forma_pago = ttk.Combobox(pago_container, 
                                       values=["TODAS", "EFECTIVO", "DÉBITO", "CRÉDITO", "TRANSFERENCIA", "QR", "OTROS"], 
                                       font=("Montserrat", 11), state="readonly", width=12)
        aplicar_estilo_moderno_combobox(combo_forma_pago)
        combo_forma_pago.set("TODAS")
        combo_forma_pago.pack()
        
        # FILTRO MARCA
        marca_container = tk.Frame(filtros_linea, bg="#1a1f2e")
        marca_container.pack(side="left", padx=(0, 15))
        
        lbl_marca = tk.Label(marca_container, text="🏷️ Marca:", 
                            font=("Montserrat", 12, "bold"), 
                            bg="#1a1f2e", fg="#e5e7eb")
        lbl_marca.pack(anchor="w", pady=(0, 5))
        
        marcas = list(set([p.marca for p in self.sistema.productos if p.marca]))
        marcas.insert(0, "TODAS")
        combo_marca = ttk.Combobox(marca_container, values=marcas, 
                                  font=("Montserrat", 11), state="readonly", width=15)
        aplicar_estilo_moderno_combobox(combo_marca)
        combo_marca.set("TODAS")
        combo_marca.pack()
        
        # FILTRO VENDEDOR
        vendedor_container = tk.Frame(filtros_linea, bg="#1a1f2e")
        vendedor_container.pack(side="left", padx=(0, 15))
        
        lbl_vendedor = tk.Label(vendedor_container, text="👤 Vendedor:", 
                               font=("Montserrat", 12, "bold"), 
                               bg="#1a1f2e", fg="#e5e7eb")
        lbl_vendedor.pack(anchor="w", pady=(0, 5))
        
        vendedores = list(set([getattr(v, 'vendedor', 'Sin especificar') for v in self.sistema.ventas]))
        # Incluir vendedores históricos también
        for año in range(2000, datetime.date.today().year + 1):
            archivo_historico = f"ventas_historico_{año}.json"
            if os.path.exists(archivo_historico):
                try:
                    with open(archivo_historico, "r", encoding="utf-8") as f:
                        datos_h = json.load(f)
                        for vhist in datos_h:
                            vendedores.append(vhist.get('vendedor', 'Sin especificar'))
                except Exception:
                    pass
        vendedores = sorted(list(set(vendedores)))
        vendedores.insert(0, "TODOS")
        combo_vendedor = ttk.Combobox(vendedor_container, values=vendedores, 
                                     font=("Montserrat", 11), state="readonly", width=15)
        aplicar_estilo_moderno_combobox(combo_vendedor)
        combo_vendedor.set("TODOS")
        combo_vendedor.pack()
        
        # === FUNCIONES DE CALENDARIO MEJORADAS ===
        def abrir_calendario_desde():
            """Abre calendario directamente en la fecha actual"""
            try:
                from tkcalendar import DateEntry
                
                # Crear ventana de calendario moderna
                cal_window = tk.Toplevel()
                cal_window.title("📅 Seleccionar Fecha Desde")
                cal_window.geometry("450x300")
                cal_window.configure(bg="#1a1f2e")
                cal_window.resizable(False, False)
                
                # Centrar ventana
                cal_window.transient(self.canvas_bg.winfo_toplevel())
                cal_window.grab_set()
                
                # Obtener fecha actual o fecha en el campo
                try:
                    fecha_actual = datetime.datetime.strptime(ent_desde.get(), "%Y-%m-%d").date()
                except:
                    fecha_actual = datetime.date.today()
                
                # Frame principal del calendario
                cal_frame = tk.Frame(cal_window, bg="#1a1f2e")
                cal_frame.pack(fill="both", expand=True, padx=20, pady=20)
                
                # Título del calendario
                lbl_titulo = tk.Label(cal_frame, text="Seleccione la fecha desde", 
                                     font=("Montserrat", 14, "bold"), 
                                     bg="#1a1f2e", fg="#00c9df")
                lbl_titulo.pack(pady=(0, 15))
                
                # Calendario con estilo moderno
                cal = DateEntry(cal_frame, width=15, background='#4f46e5',
                               foreground='white', borderwidth=0, 
                               date_pattern='yyyy-mm-dd',
                               year=fecha_actual.year, month=fecha_actual.month, day=fecha_actual.day,
                               font=("Montserrat", 12))
                cal.pack(pady=(0, 20))
                
                # Botones de acción
                botones_frame = tk.Frame(cal_frame, bg="#1a1f2e")
                botones_frame.pack(fill="x")
                
                def seleccionar_fecha():
                    ent_desde.delete(0, tk.END)
                    ent_desde.insert(0, cal.get())
                    cal_window.destroy()
                
                def fecha_hoy():
                    ent_desde.delete(0, tk.END)
                    ent_desde.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
                    cal_window.destroy()
                
                # Botón seleccionar
                btn_seleccionar = tk.Button(botones_frame, text="✅ Seleccionar", 
                                           font=("Montserrat", 11, "bold"),
                                           bg="#4f46e5", fg="#ffffff", 
                                           command=seleccionar_fecha,
                                           relief="flat", bd=0, padx=15, pady=8)
                btn_seleccionar.pack(side="left", padx=(0, 10))
                
                # Botón fecha hoy
                btn_hoy = tk.Button(botones_frame, text="📅 Hoy", 
                                   font=("Montserrat", 11, "bold"),
                                   bg="#059669", fg="#ffffff", 
                                   command=fecha_hoy,
                                   relief="flat", bd=0, padx=15, pady=8)
                btn_hoy.pack(side="left", padx=(0, 10))
                
                # Botón cancelar
                btn_cancelar = tk.Button(botones_frame, text="❌ Cancelar", 
                                        font=("Montserrat", 11, "bold"),
                                        bg="#ef4444", fg="#ffffff", 
                                        command=cal_window.destroy,
                                        relief="flat", bd=0, padx=15, pady=8)
                btn_cancelar.pack(side="right")
                
            except ImportError:
                messagebox.showinfo("Información", 
                                   "Para usar el calendario, instale: pip install tkcalendar\n"
                                   "Por ahora, ingrese la fecha manualmente (YYYY-MM-DD)")
        
        def abrir_calendario_hasta():
            """Abre calendario directamente en la fecha actual"""
            try:
                from tkcalendar import DateEntry
                
                # Crear ventana de calendario moderna
                cal_window = tk.Toplevel()
                cal_window.title("📅 Seleccionar Fecha Hasta")
                cal_window.geometry("450x300")
                cal_window.configure(bg="#1a1f2e")
                cal_window.resizable(False, False)
                
                # Centrar ventana
                cal_window.transient(self.canvas_bg.winfo_toplevel())
                cal_window.grab_set()
                
                # Obtener fecha actual o fecha en el campo
                try:
                    fecha_actual = datetime.datetime.strptime(ent_hasta.get(), "%Y-%m-%d").date()
                except:
                    fecha_actual = datetime.date.today()
                
                # Frame principal del calendario
                cal_frame = tk.Frame(cal_window, bg="#1a1f2e")
                cal_frame.pack(fill="both", expand=True, padx=20, pady=20)
                
                # Título del calendario
                lbl_titulo = tk.Label(cal_frame, text="Seleccione la fecha hasta", 
                                     font=("Montserrat", 14, "bold"), 
                                     bg="#1a1f2e", fg="#00c9df")
                lbl_titulo.pack(pady=(0, 15))
                
                # Calendario con estilo moderno
                cal = DateEntry(cal_frame, width=15, background='#4f46e5',
                               foreground='white', borderwidth=0, 
                               date_pattern='yyyy-mm-dd',
                               year=fecha_actual.year, month=fecha_actual.month, day=fecha_actual.day,
                               font=("Montserrat", 12))
                cal.pack(pady=(0, 20))
                
                # Botones de acción
                botones_frame = tk.Frame(cal_frame, bg="#1a1f2e")
                botones_frame.pack(fill="x")
                
                def seleccionar_fecha():
                    ent_hasta.delete(0, tk.END)
                    ent_hasta.insert(0, cal.get())
                    cal_window.destroy()
                
                def fecha_hoy():
                    ent_hasta.delete(0, tk.END)
                    ent_hasta.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
                    cal_window.destroy()
                
                # Botón seleccionar
                btn_seleccionar = tk.Button(botones_frame, text="✅ Seleccionar", 
                                           font=("Montserrat", 11, "bold"),
                                           bg="#4f46e5", fg="#ffffff", 
                                           command=seleccionar_fecha,
                                           relief="flat", bd=0, padx=15, pady=8)
                btn_seleccionar.pack(side="left", padx=(0, 10))
                
                # Botón fecha hoy
                btn_hoy = tk.Button(botones_frame, text="📅 Hoy", 
                                   font=("Montserrat", 11, "bold"),
                                   bg="#059669", fg="#ffffff", 
                                   command=fecha_hoy,
                                   relief="flat", bd=0, padx=15, pady=8)
                btn_hoy.pack(side="left", padx=(0, 10))
                
                # Botón cancelar
                btn_cancelar = tk.Button(botones_frame, text="❌ Cancelar", 
                                        font=("Montserrat", 11, "bold"),
                                        bg="#ef4444", fg="#ffffff", 
                                        command=cal_window.destroy,
                                        relief="flat", bd=0, padx=15, pady=8)
                btn_cancelar.pack(side="right")
                
            except ImportError:
                messagebox.showinfo("Información", 
                                   "Para usar el calendario, instale: pip install tkcalendar\n"
                                   "Por ahora, ingrese la fecha manualmente (YYYY-MM-DD)")
        
        # Asignar comandos a los botones
        btn_cal_desde.config(command=abrir_calendario_desde)
        btn_cal_hasta.config(command=abrir_calendario_hasta)
        

        
        # === BOTONES DE ACCIÓN MODERNOS ===
        acciones_container = tk.Frame(self.canvas_bg, bg="#0a0f1a")
        self.canvas_bg.create_window(640, 220, window=acciones_container, width=900, height=70, anchor="center")
        
        marco_acciones = tk.Frame(acciones_container, bg="#1a1f2e", relief="solid", bd=1, highlightbackground="#3b82f6", highlightcolor="#3b82f6", highlightthickness=2)
        marco_acciones.pack(fill="both", expand=True, padx=3, pady=3)
        
        actions_frame = tk.Frame(marco_acciones, bg="#1a1f2e")
        actions_frame.pack(fill="x", padx=12, pady=6)
        
        # Botón FILTRAR con efecto glow
        btn_filtrar = tk.Button(actions_frame, text="🔍 FILTRAR", 
                               font=("Montserrat", 12, "bold"), 
                               bg="#4f46e5", fg="#ffffff", 
                               bd=0, relief="flat", padx=20, pady=8, cursor="hand2")
        aplicar_estilo_moderno_boton(btn_filtrar, "primario", hover_efecto=True)
        btn_filtrar.pack(side="left", padx=(0, 12))
        
        # Botón VER DESGLOSE con efecto glow
        btn_desglose = tk.Button(actions_frame, text="📊 VER DESGLOSE", 
                                font=("Montserrat", 12, "bold"), 
                                bg="#f59e0b", fg="#ffffff", 
                                bd=0, relief="flat", padx=20, pady=8, cursor="hand2")
        aplicar_estilo_moderno_boton(btn_desglose, "warning", hover_efecto=True)
        btn_desglose.pack(side="left", padx=(0, 12))
        
        # Botón DESCARGAR PDF con efecto glow
        btn_pdf = tk.Button(actions_frame, text="📄 DESCARGAR PDF", 
                           font=("Montserrat", 12, "bold"), 
                           bg="#8b5cf6", fg="#ffffff", 
                           bd=0, relief="flat", padx=20, pady=8, cursor="hand2")
        aplicar_estilo_moderno_boton(btn_pdf, "secundario", hover_efecto=True)
        btn_pdf.pack(side="left", padx=(0, 12))
        
        # Botón EXPORTAR CSV con efecto glow
        btn_exportar = tk.Button(actions_frame, text="📁 EXPORTAR CSV", 
                                font=("Montserrat", 12, "bold"), 
                                bg="#059669", fg="#ffffff", 
                                bd=0, relief="flat", padx=20, pady=8, cursor="hand2")
        aplicar_estilo_moderno_boton(btn_exportar, "success", hover_efecto=True)
        btn_exportar.pack(side="left")
        
        # === CONTENEDOR PRINCIPAL PARA TABLA Y ESTADÍSTICAS ===
        main_content_frame = tk.Frame(self.canvas_bg, bg="#0f172a")
        self.canvas_bg.create_window(640, 450, window=main_content_frame, width=1180, height=350, anchor="center")
        
        # === TABLA DE VENTAS (60% del ancho) ===
        table_frame = tk.Frame(main_content_frame, bg="#0a0f1a")
        table_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        marco_tabla = tk.Frame(table_frame, bg="#1a1f2e", relief="solid", bd=1, highlightbackground="#3b82f6", highlightcolor="#3b82f6", highlightthickness=2)
        marco_tabla.pack(fill="both", expand=True, padx=2, pady=2)

        header_tabla = tk.Label(marco_tabla, text="📋 DETALLE DE VENTAS", font=("Montserrat", 14, "bold"), bg="#1a1f2e", fg="#60a5fa", pady=4)
        header_tabla.pack(fill="x")

        tabla_container = tk.Frame(marco_tabla, bg="#1a1f2e")
        tabla_container.pack(fill="both", expand=True, padx=8, pady=4)

        columns = ("fecha", "total", "pago", "items", "detalle")
        tree_ventas = ttk.Treeview(tabla_container, columns=columns, show="headings", height=10)
        aplicar_estilo_moderno_treeview(tree_ventas)

        tree_ventas.heading("fecha", text="Fecha")
        tree_ventas.heading("total", text="Total")
        tree_ventas.heading("pago", text="Forma Pago")
        tree_ventas.heading("items", text="# Items")
        tree_ventas.heading("detalle", text="Detalle de Productos")

        tree_ventas.column("fecha", width=120, anchor="center")
        tree_ventas.column("total", width=120, anchor="center")
        tree_ventas.column("pago", width=140, anchor="center")
        tree_ventas.column("items", width=80, anchor="center")
        tree_ventas.column("detalle", width=400, anchor="center")

        scrollbar_v = ttk.Scrollbar(tabla_container, orient="vertical", command=tree_ventas.yview)
        tree_ventas.configure(yscrollcommand=scrollbar_v.set)

        tree_ventas.pack(side="left", fill="both", expand=True)
        scrollbar_v.pack(side="right", fill="y")

        habilitar_ordenamiento_treeview(tree_ventas)

        # === TARJETAS DE ESTADÍSTICAS (40% del ancho, formato 2x2) ===
        stats_container = tk.Frame(main_content_frame, bg="#0f172a")
        stats_container.pack(side="right", fill="both", expand=True)
        
        # Fila 1: Tarjeta 1 y 2
        row1_frame = tk.Frame(stats_container, bg="#0f172a")
        row1_frame.pack(fill="x", pady=(0, 3))
        
        # Tarjeta Total Ventas
        card1 = tk.Frame(row1_frame, bg="#1e293b", relief="raised", bd=2)
        card1.pack(side="left", fill="both", expand=True, padx=(0, 3))
        
        tk.Label(card1, text="💰", font=("Montserrat", 18), bg="#1e293b", fg="#00ff88").pack(pady=(5, 0))
        lbl_total_ventas = tk.Label(card1, text=self.formato_moneda(0), font=("Montserrat", 12, "bold"), 
                                   bg="#1e293b", fg="#ffffff")
        lbl_total_ventas.pack()
        tk.Label(card1, text="Total Ventas", font=("Montserrat", 8), bg="#1e293b", fg="#94a3b8").pack()
        
        # Tarjeta Cantidad Ventas
        card2 = tk.Frame(row1_frame, bg="#1e293b", relief="raised", bd=2)
        card2.pack(side="right", fill="both", expand=True, padx=(3, 0))
        
        tk.Label(card2, text="🛒", font=("Montserrat", 18), bg="#1e293b", fg="#4f46e5").pack(pady=(5, 0))
        lbl_cant_ventas = tk.Label(card2, text="0", font=("Montserrat", 12, "bold"), 
                                  bg="#1e293b", fg="#ffffff")
        lbl_cant_ventas.pack()
        tk.Label(card2, text="Ventas Realizadas", font=("Montserrat", 8), bg="#1e293b", fg="#94a3b8").pack()
        
        # Fila 2: Tarjeta 3 y 4
        row2_frame = tk.Frame(stats_container, bg="#0f172a")
        row2_frame.pack(fill="x", pady=(3, 0))
        
        # Tarjeta Productos Vendidos
        card3 = tk.Frame(row2_frame, bg="#1e293b", relief="raised", bd=2)
        card3.pack(side="left", fill="both", expand=True, padx=(0, 3))
        
        tk.Label(card3, text="📦", font=("Montserrat", 18), bg="#1e293b", fg="#f59e0b").pack(pady=(5, 0))
        lbl_productos_vendidos = tk.Label(card3, text="0", font=("Montserrat", 12, "bold"), 
                                         bg="#1e293b", fg="#ffffff")
        lbl_productos_vendidos.pack()
        tk.Label(card3, text="Productos Vendidos", font=("Montserrat", 8), bg="#1e293b", fg="#94a3b8").pack()
        
        # Tarjeta Promedio por Venta
        card4 = tk.Frame(row2_frame, bg="#1e293b", relief="raised", bd=2)
        card4.pack(side="right", fill="both", expand=True, padx=(3, 0))
        
        tk.Label(card4, text="📈", font=("Montserrat", 18), bg="#1e293b", fg="#ef4444").pack(pady=(5, 0))
        lbl_promedio = tk.Label(card4, text=self.formato_moneda(0), font=("Montserrat", 12, "bold"), 
                               bg="#1e293b", fg="#ffffff")
        lbl_promedio.pack()
        tk.Label(card4, text="Promedio por Venta", font=("Montserrat", 8), bg="#1e293b", fg="#94a3b8").pack()

        venta_items_map = {}
        
        # === PANEL DE RESUMEN ===
        summary_frame = tk.Frame(self.canvas_bg, bg="#1a3d75", relief="raised", bd=2)
        self.canvas_bg.create_window(640, 670, window=summary_frame, width=1180, height=60, anchor="center")
        
        lbl_total_periodo = tk.Label(summary_frame, text=f"Total del Período: {self.formato_moneda(0)}", 
                                    font=("Montserrat", 16, "bold"), bg="#1a3d75", fg="#00ff88")
        lbl_total_periodo.pack(pady=15)
        
        def actualizar_estadisticas(ventas_filtradas):
            """Actualiza las tarjetas de estadísticas"""
            total_dinero = sum(v.total for v in ventas_filtradas)
            cantidad_ventas = len(ventas_filtradas)
            productos_vendidos = sum(sum(item['cantidad'] for item in v.items) for v in ventas_filtradas)
            promedio = total_dinero / cantidad_ventas if cantidad_ventas > 0 else 0
            
            lbl_total_ventas.config(text=self.formato_moneda(total_dinero))
            lbl_cant_ventas.config(text=str(cantidad_ventas))
            lbl_productos_vendidos.config(text=str(productos_vendidos))
            lbl_promedio.config(text=self.formato_moneda(promedio))
            lbl_total_periodo.config(text=f"Total del Período: {self.formato_moneda(total_dinero)}")
        
        def filtrar_ventas():
            """Filtra las ventas según los criterios seleccionados e incluye ventas históricas"""
            global datos_filtrados_actuales
            try:
                # Obtener valores de los filtros
                fecha_desde_str = ent_desde.get().strip()
                fecha_hasta_str = ent_hasta.get().strip()
                forma_pago_filtro = combo_forma_pago.get()
                marca_filtro = combo_marca.get()
                vendedor_filtro = combo_vendedor.get()
                
                # Convertir fechas
                fecha_desde = datetime.datetime.strptime(fecha_desde_str, "%Y-%m-%d").date()
                fecha_hasta = datetime.datetime.strptime(fecha_hasta_str, "%Y-%m-%d").date()
                
                # Limpiar tabla
                for item in tree_ventas.get_children():
                    tree_ventas.delete(item)
                
                ventas_filtradas = []
                
                # 1) Ventas actuales (memoria)
                ventas_periodo = self.sistema.reporte_ventas(fecha_desde, fecha_hasta)
                for venta in ventas_periodo:
                    # Filtros por forma de pago y vendedor
                    if forma_pago_filtro != "TODAS" and self._norm_pago(getattr(venta, 'forma_pago', 'EFECTIVO')) != self._norm_pago(forma_pago_filtro):
                        continue
                    if vendedor_filtro != "TODOS" and getattr(venta, 'vendedor', '') != vendedor_filtro:
                        continue
                    # Filtro por marca: debe existir al menos un item con esa marca
                    if marca_filtro != "TODAS" and not any(item['producto'].marca == marca_filtro for item in venta.items):
                        continue
                    ventas_filtradas.append(venta)
                    # Mostrar en tabla y almacenar detalle por venta
                    total_venta = getattr(venta, 'total', sum(it['cantidad'] * it['precio'] for it in venta.items))
                    productos_str = ", ".join([f"{it['producto'].marca} {it['producto'].descripcion} {it['producto'].color}/{it['producto'].talle} x{it['cantidad']} @{self.formato_moneda(it['precio'])}" for it in venta.items])
                    if len(productos_str) > 120:
                        productos_str = productos_str[:117] + "..."
                    cliente = getattr(venta, 'cliente', 'Sin especificar')
                    iid = tree_ventas.insert("", "end", values=(
                        venta.fecha.strftime("%Y-%m-%d"),
                        self.formato_moneda(total_venta),
                        getattr(venta, 'forma_pago', 'EFECTIVO'),
                        f"{len(venta.items)}",
                        productos_str
                    ))
                    venta_items_map[iid] = productos_str
                
                # 2) Ventas históricas (archivadas por año)
                ventas_historicas_en_rango = []
                for año in range(fecha_desde.year, fecha_hasta.year + 1):
                    archivo_historico = f"ventas_historico_{año}.json"
                    if not os.path.exists(archivo_historico):
                        continue
                    try:
                        with open(archivo_historico, "r", encoding="utf-8") as f:
                            datos_historicos = json.load(f)
                            for venta_data in datos_historicos:
                                fecha_venta = datetime.datetime.strptime(venta_data['fecha'], "%Y-%m-%d").date()
                                if not (fecha_desde <= fecha_venta <= fecha_hasta):
                                    continue
                                # Filtros históricos (forma de pago, marca y vendedor)
                                if forma_pago_filtro != "TODAS" and self._norm_pago(venta_data.get('forma_pago', 'EFECTIVO')) != self._norm_pago(forma_pago_filtro):
                                    continue
                                if vendedor_filtro != "TODOS" and venta_data.get('vendedor', 'Sin especificar') != vendedor_filtro:
                                    continue
                                if marca_filtro != "TODAS":
                                    if not any(item.get('marca', '') == marca_filtro for item in venta_data['items']):
                                        continue
                                ventas_historicas_en_rango.append(venta_data)
                    except Exception:
                        continue
                
                # Pintar ventas históricas en la tabla y acumular en ventas_filtradas-like para estadísticas
                total_dinero_hist = 0
                for vhist in ventas_historicas_en_rango:
                    total_venta_hist = sum(item['cantidad'] * item['precio'] for item in vhist['items'])
                    total_dinero_hist += total_venta_hist
                    productos_str = ", ".join([f"{it.get('marca','')} {it.get('producto','')} {it.get('color','')}/{it.get('talle','')} x{it.get('cantidad',0)} @{self.formato_moneda(it.get('precio',0))}" for it in vhist['items']])
                    if len(productos_str) > 120:
                        productos_str = productos_str[:117] + "..."
                    iid = tree_ventas.insert("", "end", values=(
                        vhist['fecha'],
                        self.formato_moneda(total_venta_hist),
                        vhist.get('forma_pago', 'EFECTIVO'),
                        f"{len(vhist['items'])}",
                        productos_str
                    ))
                    venta_items_map[iid] = productos_str
                
                # Actualizar estadísticas unificando actuales + histórico
                total_dinero_actual = sum(getattr(v, 'total', sum(it['cantidad'] * it['precio'] for it in v.items)) for v in ventas_filtradas)
                total_dinero = total_dinero_actual + total_dinero_hist
                cantidad_ventas = len(ventas_filtradas) + len(ventas_historicas_en_rango)
                productos_vendidos = sum(sum(item['cantidad'] for item in v.items) for v in ventas_filtradas) + \
                                     sum(sum(item['cantidad'] for item in vhist['items']) for vhist in ventas_historicas_en_rango)
                promedio = total_dinero / cantidad_ventas if cantidad_ventas > 0 else 0
                lbl_total_ventas.config(text=self.formato_moneda(total_dinero))
                lbl_cant_ventas.config(text=str(cantidad_ventas))
                lbl_productos_vendidos.config(text=str(productos_vendidos))
                lbl_promedio.config(text=self.formato_moneda(promedio))
                lbl_total_periodo.config(text=f"Total del Período: {self.formato_moneda(total_dinero)}")
                
                # Actualizar datos_filtrados_actuales para PDF y desglose
                datos_filtrados_actuales = {
                    'ventas_actuales': ventas_filtradas,
                    'ventas_historicas': ventas_historicas_en_rango,
                    'fecha_desde': fecha_desde,
                    'fecha_hasta': fecha_hasta,
                    'total_dinero': total_dinero,
                    'cantidad_ventas': cantidad_ventas,
                    'productos_vendidos': productos_vendidos,
                    'promedio': promedio
                }
                
                messagebox.showinfo("Éxito", f"Se encontraron {cantidad_ventas} ventas en el período seleccionado (incluye histórico)")
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")
            except Exception as e:
                messagebox.showerror("Error", f"Error al filtrar ventas: {e}")
        
        def exportar_reporte():
            """Exporta el reporte a CSV"""
            try:
                if not tree_ventas.get_children():
                    messagebox.showwarning("Advertencia", "No hay datos para exportar. Primero filtre las ventas.")
                    return
                
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                nombre_archivo = f"reporte_ventas_{timestamp}.csv"
                
                with open(nombre_archivo, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    
                    # Escribir encabezados
                    writer.writerow(['Fecha', 'Total', 'Forma Pago', 'Productos', 'Cliente'])
                    
                    # Escribir datos
                    for child in tree_ventas.get_children():
                        values = tree_ventas.item(child)['values']
                        writer.writerow(values)
                
                messagebox.showinfo("Exportación Exitosa", f"Reporte exportado como: {nombre_archivo}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar: {e}")
        
        def mostrar_desglose_detallado():
            """Muestra el desglose detallado de las ventas filtradas"""
            if not hasattr(globals(), 'datos_filtrados_actuales') or not datos_filtrados_actuales:
                messagebox.showwarning("Sin Datos", "Primero debe filtrar las ventas para ver el desglose detallado.")
                return
            
            datos = datos_filtrados_actuales
            
            # Crear ventana de desglose
            ventana_desglose = tk.Toplevel(self)
            ventana_desglose.title("📊 Desglose Detallado de Ventas - ALENIA GESTIÓN KONTROL+")
            ventana_desglose.geometry("1000x700")
            ventana_desglose.configure(bg="#0a0f1a")
            ventana_desglose.resizable(True, True)
            ventana_desglose.transient(self)
            ventana_desglose.grab_set()
            
            # Centrar ventana
            ventana_desglose.geometry("+{}+{}".format(
                (ventana_desglose.winfo_screenwidth() // 2) - 500,
                (ventana_desglose.winfo_screenheight() // 2) - 350
            ))
            
            # Crear canvas con scroll
            canvas_desglose = tk.Canvas(ventana_desglose, bg="#0a0f1a", highlightthickness=0)
            scrollbar_desglose = ttk.Scrollbar(ventana_desglose, orient="vertical", command=canvas_desglose.yview)
            frame_contenido = tk.Frame(canvas_desglose, bg="#0a0f1a")
            
            canvas_desglose.configure(yscrollcommand=scrollbar_desglose.set)
            canvas_desglose.pack(side="left", fill="both", expand=True)
            scrollbar_desglose.pack(side="right", fill="y")
            
            canvas_window = canvas_desglose.create_window((0, 0), window=frame_contenido, anchor="nw")
            
            # Header del desglose
            header_frame = tk.Frame(frame_contenido, bg="#1a1f2e", relief="flat", bd=0)
            header_frame.pack(fill="x", padx=20, pady=(20, 10))
            
            lbl_titulo = tk.Label(header_frame, text="📊 DESGLOSE DETALLADO DE VENTAS", 
                                 font=("Montserrat", 20, "bold"), 
                                 bg="#1a1f2e", fg="#00c9df")
            lbl_titulo.pack(pady=(15, 5))
            
            lbl_periodo = tk.Label(header_frame, 
                                  text=f"Período: {datos['fecha_desde'].strftime('%d/%m/%Y')} - {datos['fecha_hasta'].strftime('%d/%m/%Y')}", 
                                  font=("Montserrat", 14), 
                                  bg="#1a1f2e", fg="#e5e7eb")
            lbl_periodo.pack(pady=(0, 15))
            
            # Resumen de métricas
            resumen_frame = tk.Frame(frame_contenido, bg="#1a1f2e", relief="flat", bd=0)
            resumen_frame.pack(fill="x", padx=20, pady=10)
            
            # Métricas en estilo botón
            metricas_frame = tk.Frame(resumen_frame, bg="#1a1f2e")
            metricas_frame.pack(fill="x")
            
            metricas_data = [
                ("💰 Total Ventas", self.formato_moneda(datos['total_dinero']), "#059669"),
                ("🛒 Cantidad Ventas", str(datos['cantidad_ventas']), "#4f46e5"),
                ("📦 Productos Vendidos", str(datos['productos_vendidos']), "#f59e0b"),
                ("📈 Promedio por Venta", self.formato_moneda(datos['promedio']), "#8b5cf6")
            ]
            
            for etiqueta, valor, color in metricas_data:
                metrica_frame = tk.Frame(metricas_frame, bg=color, relief="flat", bd=0)
                metrica_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
                
                lbl_etiqueta = tk.Label(metrica_frame, text=etiqueta, 
                                       font=("Montserrat", 12, "bold"), 
                                       bg=color, fg="#ffffff", pady=8)
                lbl_etiqueta.pack()
                
                lbl_valor = tk.Label(metrica_frame, text=valor, 
                                    font=("Montserrat", 16, "bold"), 
                                    bg=color, fg="#ffffff")
                lbl_valor.pack(pady=(0, 8))
            
            # Tabla detallada de ventas
            tabla_frame = tk.Frame(frame_contenido, bg="#1a1f2e", relief="flat", bd=0)
            tabla_frame.pack(fill="both", expand=True, padx=20, pady=10)
            
            # Header de tabla
            header_tabla = tk.Label(tabla_frame, text="📋 DETALLE DE VENTAS", 
                                   font=("Montserrat", 16, "bold"), 
                                   bg="#1a1f2e", fg="#00c9df")
            header_tabla.pack(pady=(0, 10))
            
            # Crear Treeview para el detalle
            columns = ("Fecha", "Total", "Forma Pago", "Items", "Productos")
            tree_detalle = ttk.Treeview(tabla_frame, columns=columns, show="headings", height=15)
            
            for col in columns:
                tree_detalle.heading(col, text=col)
                tree_detalle.column(col, width=150, anchor="center")
            
            # Scrollbar para la tabla
            scrollbar_tabla = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree_detalle.yview)
            tree_detalle.configure(yscrollcommand=scrollbar_tabla.set)
            
            tree_detalle.pack(side="left", fill="both", expand=True)
            scrollbar_tabla.pack(side="right", fill="y")
            
            # Llenar tabla con datos
            for venta in datos['ventas']:
                total_venta = sum(item['cantidad'] * item['precio'] for item in venta.items)
                productos_str = ", ".join([f"{item['producto'].marca} {item['producto'].descripcion}" for item in venta.items])
                
                tree_detalle.insert("", "end", values=(
                    venta.fecha.strftime("%d/%m/%Y"),
                    self.formato_moneda(total_venta),
                    getattr(venta, 'forma_pago', 'EFECTIVO'),
                    len(venta.items),
                    productos_str[:50] + "..." if len(productos_str) > 50 else productos_str
                ))
            
            # Agregar ventas históricas
            for venta_hist in datos['ventas_historicas']:
                total_venta = sum(item['cantidad'] * item['precio'] for item in venta_hist['items'])
                productos_str = ", ".join([f"{item.get('marca', '')} {item.get('producto', '')}" for item in venta_hist['items']])
                
                tree_detalle.insert("", "end", values=(
                    venta_hist['fecha'],
                    self.formato_moneda(total_venta),
                    venta_hist.get('forma_pago', 'EFECTIVO'),
                    len(venta_hist['items']),
                    productos_str[:50] + "..." if len(productos_str) > 50 else productos_str
                ))
            
            # Botones de acción
            botones_frame = tk.Frame(frame_contenido, bg="#1a1f2e")
            botones_frame.pack(fill="x", padx=20, pady=20)
            
            btn_pdf = tk.Button(botones_frame, text="📄 DESCARGAR PDF", 
                               font=("Montserrat", 12, "bold"),
                               bg="#8b5cf6", fg="#ffffff",
                               command=lambda: generar_pdf_desglose(datos),
                               relief="flat", bd=0, padx=20, pady=10)
            btn_pdf.pack(side="left", padx=(0, 10))
            
            btn_cerrar = tk.Button(botones_frame, text="❌ CERRAR", 
                                  font=("Montserrat", 12, "bold"),
                                  bg="#ef4444", fg="#ffffff",
                                  command=ventana_desglose.destroy,
                                  relief="flat", bd=0, padx=20, pady=10)
            btn_cerrar.pack(side="right")
            
            # Configurar scroll
            frame_contenido.update_idletasks()
            canvas_desglose.configure(scrollregion=canvas_desglose.bbox("all"))
            
            def configurar_scroll(event):
                canvas_desglose.configure(scrollregion=canvas_desglose.bbox("all"))
                canvas_width = event.width
                canvas_desglose.itemconfig(canvas_window, width=canvas_width)
            
            canvas_desglose.bind('<Configure>', configurar_scroll)
        
        def generar_pdf_desglose(datos):
            """Genera PDF del desglose detallado"""
            try:
                from reportlab.lib.pagesizes import A4
                from reportlab.lib import colors
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
                from reportlab.lib.units import inch
                
                # Nombre del archivo
                filename = filedialog.asksaveasfilename(
                    defaultextension=".pdf",
                    filetypes=[("PDF files", "*.pdf")],
                    initialfile=f"desglose_ventas_{datos['fecha_desde'].strftime('%Y%m%d')}_{datos['fecha_hasta'].strftime('%Y%m%d')}_{datetime.datetime.now().strftime('%H%M%S')}.pdf"
                )
                
                if not filename:
                    return
                
                # Crear documento
                doc = SimpleDocTemplate(filename, pagesize=A4, topMargin=0.5*inch)
                story = []
                styles = getSampleStyleSheet()
                
                # Título
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=24,
                    spaceAfter=30,
                    textColor=colors.HexColor('#0f172a'),
                    alignment=1
                )
                
                story.append(Paragraph("📊 DESGLOSE DETALLADO DE VENTAS", title_style))
                story.append(Spacer(1, 20))
                
                # Período
                story.append(Paragraph(f"<b>Período:</b> {datos['fecha_desde'].strftime('%d/%m/%Y')} - {datos['fecha_hasta'].strftime('%d/%m/%Y')}", styles['Normal']))
                story.append(Spacer(1, 20))
                
                # Resumen de métricas
                story.append(Paragraph("<b>RESUMEN DE MÉTRICAS</b>", styles['Heading2']))
                story.append(Spacer(1, 10))
                
                metricas_data = [
                    ["Total Ventas", self.formato_moneda(datos['total_dinero'])],
                    ["Cantidad de Ventas", str(datos['cantidad_ventas'])],
                    ["Productos Vendidos", str(datos['productos_vendidos'])],
                    ["Promedio por Venta", self.formato_moneda(datos['promedio'])]
                ]
                
                tabla_metricas = Table(metricas_data, colWidths=[2*inch, 2*inch])
                tabla_metricas.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#0f172a')),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1'))
                ]))
                
                story.append(tabla_metricas)
                story.append(Spacer(1, 20))
                
                # Detalle de ventas
                story.append(Paragraph("<b>DETALLE DE VENTAS</b>", styles['Heading2']))
                story.append(Spacer(1, 10))
                
                # Preparar datos de la tabla
                tabla_data = [["Fecha", "Total", "Forma Pago", "Items", "Productos"]]
                
                # Agregar ventas actuales
                for venta in datos['ventas_actuales']:
                    total_venta = sum(item['cantidad'] * item['precio'] for item in venta.items)
                    productos_str = ", ".join([f"{item['producto'].marca} {item['producto'].descripcion}" for item in venta.items])
                    
                    tabla_data.append([
                        venta.fecha.strftime("%d/%m/%Y"),
                        self.formato_moneda(total_venta),
                        getattr(venta, 'forma_pago', 'EFECTIVO'),
                        str(len(venta.items)),
                        productos_str[:40] + "..." if len(productos_str) > 40 else productos_str
                    ])
                
                # Agregar ventas históricas
                for venta_hist in datos['ventas_historicas']:
                    total_venta = sum(item['cantidad'] * item['precio'] for item in venta_hist['items'])
                    productos_str = ", ".join([f"{item.get('marca', '')} {item.get('producto', '')}" for item in venta_hist['items']])
                    
                    tabla_data.append([
                        venta_hist['fecha'],
                        self.formato_moneda(total_venta),
                        venta_hist.get('forma_pago', 'EFECTIVO'),
                        str(len(venta_hist['items'])),
                        productos_str[:40] + "..." if len(productos_str) > 40 else productos_str
                    ])
                
                # Crear tabla
                tabla_ventas = Table(tabla_data, colWidths=[1*inch, 1.2*inch, 1*inch, 0.8*inch, 2*inch])
                tabla_ventas.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4f46e5')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#0f172a')),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f1f5f9')])
                ]))
                
                story.append(tabla_ventas)
                
                # Generar PDF
                doc.build(story)
                messagebox.showinfo("PDF Generado", f"El archivo PDF se ha guardado exitosamente en:\n{filename}")
                
            except ImportError:
                messagebox.showerror("Error", "Para generar PDFs, instale: pip install reportlab")
            except Exception as e:
                messagebox.showerror("Error", f"Error al generar PDF: {e}")
        
        def descargar_pdf_reporte():
            """Descarga PDF del reporte actual"""
            if not hasattr(globals(), 'datos_filtrados_actuales') or not datos_filtrados_actuales:
                messagebox.showwarning("Sin Datos", "Primero debe filtrar las ventas para generar el PDF.")
                return
            
            generar_pdf_desglose(datos_filtrados_actuales)
        
        # Configurar comandos de botones
        btn_filtrar.config(command=filtrar_ventas)
        btn_desglose.config(command=mostrar_desglose_detallado)
        btn_pdf.config(command=descargar_pdf_reporte)
        btn_exportar.config(command=exportar_reporte)
        
        # Cargar datos iniciales
        filtrar_ventas()
        
        # Chip volver
        self._chip_volver(self.mostrar_menu_secundario)
        
        # Registrar widgets
        widgets = [header_frame, filters_frame, main_content_frame, summary_frame]
        self.pantalla_widgets.extend(widgets)
        


        

        
        # Barra superior estándar
        self._chip_volver(self.mostrar_menu_secundario)
        
        widgets.extend([header_frame, filters_frame, main_content_frame, summary_frame])
        self.pantalla_widgets.extend(widgets)

    def _pantalla_alta_producto(self, parent):
        """Pantalla para agregar productos con diseño moderno"""
        widgets = []
        
        # === HEADER MODERNO ===
        header_frame = tk.Frame(self.canvas_bg, bg="#0f172a", height=72)
        self.canvas_bg.create_window(640, 50, window=header_frame, width=800, height=72, anchor="center")
        
        lbl_titulo = tk.Label(header_frame, text="📦 AGREGAR NUEVO PRODUCTO", 
                             font=("Montserrat", 16, "bold"), bg="#0f172a", fg="#00ff88")
        lbl_titulo.pack(pady=18)
        
        # === FORMULARIO EN TARJETAS ===
        main_frame = tk.Frame(self.canvas_bg, bg="#0f1629", relief="raised", bd=2)
        self.canvas_bg.create_window(640, 394, window=main_frame, width=1000, height=620, anchor="center")
        
        # Título del formulario
        form_title = tk.Label(main_frame, text="Información del Producto", 
                             font=("Montserrat", 14, "bold"), bg="#0f1629", fg="#e5e7eb")
        form_title.pack(pady=(4, 4))
        
        # Contenedor para las dos columnas
        columns_frame = tk.Frame(main_frame, bg="#0f1629")
        columns_frame.pack(pady=2, padx=54, fill="both", expand=True)
        
        # === COLUMNA IZQUIERDA ===
        left_frame = tk.Frame(columns_frame, bg="#1a3d75", relief="raised", bd=1)
        left_frame.pack(side="left", padx=(0, 4), pady=20, fill="both", expand=True)

        tk.Label(left_frame, text="📝 Información Básica", font=("Montserrat", 12, "bold"),
                bg="#1a3d75", fg="#00ff88").pack(pady=(10, 4))

        campos_izq = ["Marca", "Descripción", "Color", "Talle"]
        entradas = {}
        
        for campo in campos_izq:
            field_frame = tk.Frame(left_frame, bg="#1a3d75")
            field_frame.pack(pady=4, padx=9, fill="x")
            
            lbl = tk.Label(field_frame, text=f"{campo}:", font=("Montserrat", 11, "bold"), 
                          bg="#1a3d75", fg="#e5e7eb")
            lbl.pack(anchor="w", pady=(0, 4))
            
            ent = tk.Entry(field_frame, font=("Montserrat", 11), bg="#ffffff", 
                          fg="#000000", bd=2, relief="ridge", insertbackground="#000000")
            aplicar_estilo_moderno_entry(ent)
            ent.pack(fill="x", ipady=7)
            entradas[campo] = ent
            
            # Agregar placeholders
            placeholders = {
                "Marca": "Ej: Nike, Adidas, Local...",
                "Descripción": "Ej: Remera deportiva, Pantalón jean...",
                "Color": "Ej: Rojo, Azul, Negro...",
                "Talle": "Ej: S, M, L, XL, 42, 44..."
            }
            
            def add_placeholder(entry, placeholder_text):
                entry.insert(0, placeholder_text)
                entry.config(fg="gray")
                
                def on_focus_in(event):
                    if entry.get() == placeholder_text:
                        entry.delete(0, tk.END)
                        entry.config(fg="black")
                
                def on_focus_out(event):
                    if entry.get() == "":
                        entry.insert(0, placeholder_text)
                        entry.config(fg="gray")
                
                entry.bind("<FocusIn>", on_focus_in)
                entry.bind("<FocusOut>", on_focus_out)
            
            add_placeholder(ent, placeholders[campo])
        
        # === COLUMNA DERECHA ===
        right_frame = tk.Frame(columns_frame, bg="#1a3d75", relief="raised", bd=1)
        right_frame.pack(side="right", padx=(9, 0), pady=20, fill="both", expand=True)

        tk.Label(right_frame, text="💰 Información Comercial", font=("Montserrat", 12, "bold"),
                bg="#1a3d75", fg="#00ff88").pack(pady=(10, 9))

        campos_der = ["Cantidad", "Precio Costo", "% Venta", "% Amigo"]
        
        for campo in campos_der:
            field_frame = tk.Frame(right_frame, bg="#1a3d75")
            field_frame.pack(pady=4, padx=9, fill="x")

            lbl = tk.Label(field_frame, text=f"{campo}:", font=("Montserrat", 11, "bold"),
                          bg="#1a3d75", fg="#e5e7eb")
            lbl.pack(anchor="w", pady=(0, 4))
            
            # Frame para entry y unidades
            entry_frame = tk.Frame(field_frame, bg="#1a3d75")
            entry_frame.pack(fill="x")
            
            ent = tk.Entry(entry_frame, font=("Montserrat", 11), bg="#ffffff", 
                          fg="#000000", bd=2, relief="ridge", insertbackground="#000000")
            aplicar_estilo_moderno_entry(ent)
            ent.pack(side="left", fill="x", expand=True, ipady=7)
            entradas[campo] = ent
            
            # Unidades o símbolos
            unidades = {
                "Cantidad": "unidades",
                "Precio Costo": "$",
                "% Venta": "%",
                "% Amigo": "%"
            }
            
            if campo in ["Precio Costo"]:
                simbolo = tk.Label(entry_frame, text="$", font=("Montserrat", 11, "bold"), 
                                 bg="#1a3d75", fg="#00ff88")
                simbolo.pack(side="left", padx=(4, 0))
            elif "%" in campo:
                simbolo = tk.Label(entry_frame, text="%", font=("Montserrat", 11, "bold"), 
                                 bg="#1a3d75", fg="#00ff88")
                simbolo.pack(side="right", padx=(4, 0))
        
        # Valores por defecto
        entradas["% Venta"].insert(0, "50")
        entradas["% Venta"].config(fg="black")
        entradas["% Amigo"].insert(0, "20")
        entradas["% Amigo"].config(fg="black")
        
        # === PANEL DE PRECIOS CALCULADOS ===
        calc_frame = tk.Frame(main_frame, bg="#0a0d1a", relief="raised", bd=2)
        calc_frame.pack(pady=2, padx=36, fill="x")
            
            
        # Borde cian usando highlight (simula borde coloreado)
        calc_frame = tk.Frame(
                main_frame,
                bg="#0a0d1a",
                relief="flat", bd=0,
                highlightthickness=2,
                highlightbackground="#9D00FF",
                highlightcolor="#FF00EA"
            )
        calc_frame.pack(pady=2, padx=36, fill="x")
    
        
        tk.Label(calc_frame, text="💡 Precios Calculados", font=("Montserrat", 12, "bold"), 
                bg="#0a0d1a", fg="#00ff88").pack(pady=(9, 13))
        
        precios_frame = tk.Frame(calc_frame, bg="#0a0d1a")
        precios_frame.pack(pady=(0, 13))
        
        lbl_precio_venta = tk.Label(precios_frame, text=f"Precio Venta: {self.formato_moneda(0)}", 
                                   font=("Montserrat", 11, "bold"), bg="#0a0d1a", fg="#4ade80")
        lbl_precio_venta.pack(side="left", padx=27)
        
        lbl_precio_amigo = tk.Label(precios_frame, text=f"Precio Amigo: {self.formato_moneda(0)}", 
                                   font=("Montserrat", 11, "bold"), bg="#0a0d1a", fg="#60a5fa")
        lbl_precio_amigo.pack(side="right", padx=27)
        
        def calcular_precios(*args):
            """Calcula y muestra los precios en tiempo real"""
            try:
                costo_text = entradas["Precio Costo"].get()
                venta_text = entradas["% Venta"].get()
                amigo_text = entradas["% Amigo"].get()
                
                # Limpiar placeholders y validar
                if costo_text and costo_text != "Ej: 1000, 2500..." and costo_text.replace('.', '').replace(',', '').isdigit():
                    costo = float(costo_text.replace(',', '.'))
                    
                    if venta_text and venta_text.isdigit():
                        venta_pct = float(venta_text)
                        precio_venta = costo * (1 + venta_pct / 100)
                        lbl_precio_venta.config(text=f"Precio Venta: {self.formato_moneda(precio_venta)}")
                    
                    if amigo_text and amigo_text.isdigit():
                        amigo_pct = float(amigo_text)
                        precio_amigo = costo * (1 + amigo_pct / 100)
                        lbl_precio_amigo.config(text=f"Precio Amigo: {self.formato_moneda(precio_amigo)}")
                else:
                    lbl_precio_venta.config(text=f"Precio Venta: {self.formato_moneda(0)}")
                    lbl_precio_amigo.config(text=f"Precio Amigo: {self.formato_moneda(0)}")
            except:
                lbl_precio_venta.config(text=f"Precio Venta: {self.formato_moneda(0)}")
                lbl_precio_amigo.config(text=f"Precio Amigo: {self.formato_moneda(0)}")
        
        # Bind para cálculo automático
        entradas["Precio Costo"].bind('<KeyRelease>', calcular_precios)
        entradas["% Venta"].bind('<KeyRelease>', calcular_precios)
        entradas["% Amigo"].bind('<KeyRelease>', calcular_precios)
        
        def guardar_producto():
            try:
                # Obtener valores limpiando placeholders
                marca = entradas["Marca"].get().strip()
                if marca.startswith("Ej:"):
                    marca = ""
                
                descripcion = entradas["Descripción"].get().strip()
                if descripcion.startswith("Ej:"):
                    descripcion = ""
                
                color = entradas["Color"].get().strip()
                if color.startswith("Ej:"):
                    color = ""
                
                talle = entradas["Talle"].get().strip()
                if talle.startswith("Ej:"):
                    talle = ""
                
                cantidad = int(entradas["Cantidad"].get())
                precio_costo = float(entradas["Precio Costo"].get())
                porcentaje_venta = float(entradas["% Venta"].get())
                porcentaje_amigo = float(entradas["% Amigo"].get())
                
                if not all([marca, descripcion, color, talle]):
                    raise ValueError("Todos los campos de texto son obligatorios")
                
                self.sistema.agregar_producto(marca, descripcion, color, talle, cantidad, 
                                            precio_costo, porcentaje_venta, porcentaje_amigo)
                messagebox.showinfo("Éxito", f"Producto '{descripcion}' agregado correctamente")
                self.mostrar_menu_secundario()
                
            except ValueError as e:
                messagebox.showerror("Error", f"Datos inválidos: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {e}")
        
        def limpiar_formulario():
            """Limpia todos los campos del formulario"""
            for campo, entry in entradas.items():
                entry.delete(0, tk.END)
                if campo in ["Marca", "Descripción", "Color", "Talle"]:
                    placeholders = {
                        "Marca": "Ej: Nike, Adidas, Local...",
                        "Descripción": "Ej: Remera deportiva, Pantalón jean...",
                        "Color": "Ej: Rojo, Azul, Negro...",
                        "Talle": "Ej: S, M, L, XL, 42, 44..."
                    }
                    entry.insert(0, placeholders[campo])
                    entry.config(fg="gray")
                elif campo in ["% Venta", "% Amigo"]:
                    entry.insert(0, "50" if campo == "% Venta" else "20")
                    entry.config(fg="black")
            calcular_precios()
        
        # === BOTONES DE ACCIÓN ===
        buttons_frame = tk.Frame(main_frame, bg="#0f1629")
        buttons_frame.pack(pady=22, fill="x")

        # Subframe para centrar los botones
        center_buttons = tk.Frame(buttons_frame, bg="#0f1629")
        center_buttons.pack()
        
        btn_guardar = tk.Button(center_buttons, text="💾 GUARDAR PRODUCTO", 
                               font=("Montserrat", 12, "bold"), bg="#03985a", fg="#ffffff", 
                               bd=0, relief="flat", command=guardar_producto, cursor="hand2")
        btn_guardar.pack(side="left", padx=13, ipady=11, ipadx=22)
        
        btn_limpiar = tk.Button(center_buttons, text="🔄 LIMPIAR CAMPOS", 
                               font=("Montserrat", 12, "bold"), bg="#6b7280", fg="#ffffff", 
                               bd=0, relief="flat", command=limpiar_formulario, cursor="hand2")
        btn_limpiar.pack(side="left", padx=13, ipady=11, ipadx=22)
        
        # Efectos hover para botones
        def crear_hover_efecto(btn, color_orig, color_hover):
            def on_enter(e):
                btn.config(bg=color_hover)
            def on_leave(e):
                btn.config(bg=color_orig)
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
        
        crear_hover_efecto(btn_guardar, "#03985a", "#047857")
        crear_hover_efecto(btn_limpiar, "#6b7280", "#4b5563")
        
        # Tooltips
        crear_tooltip(btn_guardar, "Guardar el producto en el inventario")
        crear_tooltip(btn_limpiar, "Limpiar todos los campos del formulario")
        
        widgets.extend([header_frame, main_frame, buttons_frame])
        self.pantalla_widgets.extend(widgets)


    def _pantalla_inventario(self, parent):
        """Pantalla para ver inventario con buscador y diseño moderno"""
        widgets = []
        
        # === HEADER MODERNO CON GRADIENT ===
        header_frame = tk.Frame(self.canvas_bg, bg="#111827", height=80)
        self.canvas_bg.create_window(640, 40, window=header_frame, width=600, height=80, anchor="center")
        
        # Título del header
        lbl_titulo = tk.Label(header_frame, text="📦 GESTIÓN DE INVENTARIO", 
                             font=("Montserrat", 18, "bold"), bg="#111827", fg="#00ff88")
        lbl_titulo.pack(pady=20)
        
        # === PANEL DE BÚSQUEDA Y FILTROS ===
        filtros_container = tk.Frame(self.canvas_bg, bg="#0a0f1a")
        self.canvas_bg.create_window(640, 110, window=filtros_container, width=1180, height=90, anchor="center")
        
        marco_filtros = tk.Frame(filtros_container, bg="#1a1f2e", relief="solid", bd=1, highlightbackground="#3b82f6", highlightcolor="#3b82f6", highlightthickness=2)
        marco_filtros.pack(fill="both", expand=True, padx=3, pady=3)
        
        header_filtros = tk.Label(marco_filtros, text="🔎 FILTROS DE BÚSQUEDA", font=("Montserrat", 13, "bold"), bg="#1a1f2e", fg="#60a5fa", pady=6)
        header_filtros.pack(fill="x")
        
        search_frame = tk.Frame(marco_filtros, bg="#1a1f2e")
        search_frame.pack(fill="x", padx=12, pady=4)
        
        # Buscador de productos
        tk.Label(search_frame, text="Buscar:", font=("Montserrat", 12, "bold"), 
                bg="#1a1f2e", fg="#e5e7eb").pack(side="left", padx=(16, 8), pady=(6, 6))
        
        search_var = tk.StringVar()
        ent_buscar = tk.Entry(search_frame, textvariable=search_var, font=("Montserrat", 11), 
                             bg="#ffffff", fg="#000000", bd=1, relief="solid", width=25)
        aplicar_estilo_moderno_entry(ent_buscar)
        ent_buscar.pack(side="left", padx=8, pady=(4, 4), ipady=3)
        
        # Filtro de stock
        tk.Label(search_frame, text="Stock:", font=("Montserrat", 12, "bold"), 
                bg="#1a1f2e", fg="#e5e7eb").pack(side="left", padx=(20, 8), pady=(6, 6))
        
        combo_stock = ttk.Combobox(search_frame, values=["TODOS", "STOCK BAJO (≤5)", "STOCK MEDIO (6-20)", "STOCK ALTO (>20)"], 
                                  font=("Montserrat", 11), state="readonly", width=18)
        aplicar_estilo_moderno_combobox(combo_stock)
        combo_stock.set("TODOS")
        combo_stock.pack(side="left", padx=8, pady=(4, 4))
        
        # Filtro de marca
        tk.Label(search_frame, text="Marca:", font=("Montserrat", 12, "bold"), 
                bg="#1a1f2e", fg="#e5e7eb").pack(side="left", padx=(20, 8), pady=(6, 6))
        
        productos = self.sistema.inventario_actual()
        marcas = list(set([p.marca for p in productos if p.marca]))
        marcas.insert(0, "TODAS")
        combo_marca = ttk.Combobox(search_frame, values=marcas, font=("Montserrat", 11), 
                                  state="readonly", width=15)
        aplicar_estilo_moderno_combobox(combo_marca)
        combo_marca.set("TODAS")
        combo_marca.pack(side="left", padx=8, pady=(4, 4))
        
        # Botón limpiar filtros
        btn_limpiar = tk.Button(search_frame, text="Limpiar", font=("Montserrat", 10, "bold"), 
                               bg="#6b7280", fg="#ffffff", bd=0, relief="flat", cursor="hand2")
        aplicar_estilo_moderno_boton(btn_limpiar, "secundario", hover_efecto=True)
        btn_limpiar.pack(side="right", padx=12, pady=(4, 4))
        
        # === ESTADÍSTICAS RÁPIDAS ===
        stats_frame = tk.Frame(self.canvas_bg, bg="#0a0d1a")
        self.canvas_bg.create_window(640, 200, window=stats_frame, width=1180, height=76, anchor="center")
        
        total_productos = len(productos)
        stock_bajo = len([p for p in productos if p.cantidad <= 5])
        valor_total = sum(p.precio_costo * p.cantidad for p in productos)
        
        # --- NUEVO LAYOUT: TABLA (60% VERTICAL) + ESTADÍSTICAS (40% VERTICAL) AL LADO ---
        # Tamaño de pantalla: 1280x720, área útil: 1180x500 aprox para contenido principal

        # Frame contenedor horizontal para tabla y estadísticas
        contenedor_horizontal = tk.Frame(self.canvas_bg, bg="#0a0d1a")
        # Contenedor principal: altura 500 px para no solapar filtros
        self.canvas_bg.create_window(640, 410, window=contenedor_horizontal, width=1180, height=500, anchor="center")

        # Frame para la tabla (ocupa ~80% izquierdo, vertical)
        frame_tabla = tk.Frame(contenedor_horizontal, bg="#0f1629", width=int(1180*0.80), height=500)
        frame_tabla.pack(side="left", fill="both", expand=False)
        frame_tabla.pack_propagate(False)

        # Frame para las estadísticas (ocupa ~20% derecho, vertical, 1x1)
        frame_stats = tk.Frame(contenedor_horizontal, bg="#111827", width=int(1180*0.20), height=380)
        frame_stats.pack(side="left", padx=(18,0), anchor="n")
        frame_stats.pack_propagate(False)

        # === TABLA DE INVENTARIO ===
        marco_interno_tabla = tk.Frame(frame_tabla, bg="#1a1f2e", relief="solid", bd=1, highlightbackground="#3b82f6", highlightcolor="#3b82f6", highlightthickness=2)
        marco_interno_tabla.pack(fill="both", expand=True, padx=3, pady=3)

        header_tabla = tk.Label(marco_interno_tabla, text="📋 INVENTARIO", font=("Montserrat", 14, "bold"), bg="#1a1f2e", fg="#60a5fa", pady=8)
        header_tabla.pack(fill="x")
        sep_tabla = tk.Frame(marco_interno_tabla, bg="#3b82f6", height=2)
        sep_tabla.pack(fill="x", padx=15, pady=(0, 10))

        tabla_container = tk.Frame(marco_interno_tabla, bg="#1a1f2e", height=430)
        tabla_container.pack(fill="x", expand=False, padx=15, pady=(0, 15))
        # Altura de la tabla optimizada para caber bajo filtros y sobre acciones
        tabla_container.pack_propagate(False)

        cols = ("Marca", "Descripción", "Color", "Talle", "Stock", "Precio Costo", "Precio Venta", "Valor Total")
        tree = ttk.Treeview(tabla_container, columns=cols, show="headings")
        aplicar_estilo_moderno_treeview(tree)
        habilitar_ordenamiento_treeview(tree)

        # Configurar columnas con mejor ancho y header azul corporativo
        anchos = [90, 200, 120, 90, 50, 120, 120, 120]
        for i, col in enumerate(cols):
            tree.heading(col, text=col)
            tree.column(col, width=anchos[i], anchor="center")

        # Tags coherentes con guía: alternancia mediante 'odd'/'even' y colores por estado
        tree.tag_configure('odd', background='#0f172a')
        tree.tag_configure('even', background='#1e293b')
        tree.tag_configure('stock_0', foreground='#ef4444')     # Rojo para stock 0
        tree.tag_configure('stock_1', foreground='#f59e0b')     # Naranja para stock 1
        tree.tag_configure('stock_normal', foreground='#10b981') # Verde para stock normal (2+)

        # --- ESTADÍSTICAS: 3 tarjetas verticales (idénticas al estilo de la imagen) ---
        stats_data = [
            ("📘 Total Productos", str(total_productos), "#4f46e5"),
            ("⚠️ Stock Bajo", str(stock_bajo), "#ef4444"),
            ("💰 Valor Inventario", self.formato_moneda(valor_total), "#10b981"),
        ]

        for i, (titulo, valor, color) in enumerate(stats_data):
            card = tk.Frame(frame_stats, bg=color, bd=2, relief="ridge")
            # Espaciados ajustados y apilado vertical
            pady_top = 10 if i == 0 else 8
            pady_bottom = 8 if i < len(stats_data) - 1 else 10
            card.pack(side="top", fill="x", padx=14, pady=(pady_top, pady_bottom), expand=False)
            card.config(height=110)
            card.pack_propagate(False)

            lbl_titulo = tk.Label(card, text=titulo, font=("Montserrat", 14, "bold"), bg=color, fg="#e5e7eb")
            lbl_titulo.pack(anchor="w", padx=16, pady=(10, 2))

            lbl_valor = tk.Label(card, text=valor, font=("Montserrat", 22, "bold"), bg=color, fg="#ffffff")
            lbl_valor.pack(pady=(2, 10))
        def actualizar_tabla():
            """Actualiza la tabla según los filtros aplicados"""
            # Limpiar tabla
            for item in tree.get_children():
                tree.delete(item)
            
            # Obtener filtros
            busqueda = search_var.get().lower()
            filtro_stock = combo_stock.get()
            filtro_marca = combo_marca.get()
            
            productos_filtrados = productos
            
            # Aplicar filtros
            if busqueda:
                productos_filtrados = [p for p in productos_filtrados 
                                     if busqueda in p.descripcion.lower() or 
                                        busqueda in p.marca.lower() or
                                        busqueda in p.color.lower() or
                                        busqueda in p.talle.lower()]
            
            if filtro_marca != "TODAS":
                productos_filtrados = [p for p in productos_filtrados if p.marca == filtro_marca]
            
            if filtro_stock != "TODOS":
                if filtro_stock == "STOCK BAJO (≤5)":
                    productos_filtrados = [p for p in productos_filtrados if p.cantidad <= 5]
                elif filtro_stock == "STOCK MEDIO (6-20)":
                    productos_filtrados = [p for p in productos_filtrados if 6 <= p.cantidad <= 20]
                elif filtro_stock == "STOCK ALTO (>20)":
                    productos_filtrados = [p for p in productos_filtrados if p.cantidad > 20]
            
            # Llenar tabla con alternancia de filas
            for idx, p in enumerate(productos_filtrados):
                valor_total_prod = p.precio_costo * p.cantidad
                
                # Determinar tags según stock + paridad
                if p.cantidad == 0:
                    estado_tag = 'stock_0'      # Rojo
                elif p.cantidad == 1:
                    estado_tag = 'stock_1'      # Naranja
                else:
                    estado_tag = 'stock_normal' # Verde
                paridad_tag = 'even' if idx % 2 == 0 else 'odd'
                
                tree.insert("", "end", values=(
                    p.marca, p.descripcion, p.color, p.talle, 
                    p.cantidad, self.formato_moneda(p.precio_costo), 
                    self.formato_moneda(p.precio_venta),
                    self.formato_moneda(valor_total_prod)
                ), tags=(estado_tag, paridad_tag))
        
        # Eventos de filtrado en tiempo real
        search_var.trace('w', lambda *args: actualizar_tabla())
        combo_stock.bind('<<ComboboxSelected>>', lambda e: actualizar_tabla())
        combo_marca.bind('<<ComboboxSelected>>', lambda e: actualizar_tabla())
        
        def limpiar_filtros():
            search_var.set("")
            combo_stock.set("TODOS")
            combo_marca.set("TODAS")
            actualizar_tabla()
        
        btn_limpiar.config(command=limpiar_filtros)
        
        # Llenar tabla inicial
        actualizar_tabla()
        
        # Scrollbar para la tabla (usar grid para asegurar visibilidad y distribución)
        scrollbar = ttk.Scrollbar(tabla_container, orient="vertical", command=tree.yview, style="Moderno.Vertical.TScrollbar")
        tree.configure(yscrollcommand=scrollbar.set)

        # Layout con grid: tabla expande, scrollbar fija a la derecha
        tabla_container.grid_rowconfigure(0, weight=1)
        tabla_container.grid_columnconfigure(0, weight=1)
        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # === PANEL DE ACCIONES MODERNO ===
        acciones_container = tk.Frame(self.canvas_bg, bg="#0a0f1a")
        # Bajar 3mm (~11-12 px a 96 DPI)
        self.canvas_bg.create_window(640, 662, window=acciones_container, width=1180, height=96, anchor="center")
        
        marco_acciones = tk.Frame(acciones_container, bg="#1a1f2e", relief="solid", bd=1, highlightbackground="#3b82f6", highlightcolor="#3b82f6", highlightthickness=2)
        marco_acciones.pack(fill="both", expand=True, padx=3, pady=3)
        
        actions_frame = tk.Frame(marco_acciones, bg="#1a1f2e")
        # Centrar botones dentro del frame
        actions_frame.pack(fill="x", padx=14, pady=6)
        actions_frame.grid_columnconfigure(0, weight=1)
        actions_frame.grid_columnconfigure(1, weight=1)
        actions_frame.grid_columnconfigure(2, weight=1)
        actions_frame.grid_columnconfigure(3, weight=1)
        
        # Botones de acción con iconos y estilos modernos
        def modificar_producto():
            seleccion = tree.selection()
            if not seleccion:
                messagebox.showwarning("Modificar", "Seleccione un producto de la lista para modificar.")
                print("[DEBUG] No hay selección en el Treeview para modificar. - main.py:5003")
                return
            # Obtener datos del producto seleccionado
            item = tree.item(seleccion[0])
            valores = item['values']
            print(f"[DEBUG] Valores seleccionados para modificar: {valores} - main.py:5008")
            if len(valores) < 4:
                messagebox.showerror("Error", "No se pudieron obtener los datos del producto seleccionado.")
                print("[DEBUG] Faltan datos en la fila seleccionada del Treeview. - main.py:5011")
                return
            marca, descripcion, color, talle = valores[0], valores[1], valores[2], valores[3]
            # Buscar el producto en el sistema
            producto = self.sistema.buscar_producto(marca, descripcion, color, talle)
            if producto:
                datos = (marca, descripcion, color, talle, producto.cantidad, producto.precio_costo, 
                        producto.porcentaje_venta, producto.porcentaje_amigo)
                print(f"[DEBUG] Producto encontrado para modificar: {datos} - main.py:5019")
                self._pantalla_modificar_producto(datos)
            else:
                messagebox.showerror("Error", "No se encontró el producto en el sistema. Puede que los datos no coincidan exactamente.")
                print(f"[DEBUG] No se encontró el producto en el sistema: {marca}, {descripcion}, {color}, {talle} - main.py:5023")
        
        def eliminar_producto():
            seleccion = tree.selection()
            if not seleccion:
                messagebox.showwarning("Eliminar", "Seleccione uno o más productos de la lista para eliminar.")
                return
            
            # Obtener datos de los productos seleccionados
            productos_a_eliminar = []
            productos_nombres = []
            
            for item_id in seleccion:
                item = tree.item(item_id)
                valores = item['values']
                marca, descripcion, color, talle = valores[0], valores[1], valores[2], valores[3]
                productos_a_eliminar.append((marca, descripcion, color, talle))
                productos_nombres.append(f"{descripcion} - {color} - {talle}")
            
            # Confirmar eliminación
            if len(productos_a_eliminar) == 1:
                respuesta = messagebox.askyesno("Confirmar eliminación", 
                                              f"¿Está seguro de eliminar el producto:\n{productos_nombres[0]}?")
            else:
                lista_productos = "\n".join(productos_nombres[:5])  # Mostrar máximo 5
                if len(productos_nombres) > 5:
                    lista_productos += f"\n... y {len(productos_nombres) - 5} más"
                
                respuesta = messagebox.askyesno("Confirmar eliminación múltiple", 
                                              f"¿Está seguro de eliminar {len(productos_a_eliminar)} productos?\n\n{lista_productos}")
            
            if respuesta:
                # Eliminar todos los productos seleccionados
                self.sistema.eliminar_productos_masivo(productos_a_eliminar)
                
                if len(productos_a_eliminar) == 1:
                    messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
                else:
                    messagebox.showinfo("Éxito", f"{len(productos_a_eliminar)} productos eliminados correctamente.")
                
                self.mostrar_inventario()  # Refrescar pantalla
        
        def exportar_inventario():
            """Exporta el inventario mostrado (filtrado) a CSV"""
            try:
                import csv
                filename = f"inventario_{datetime.date.today().strftime('%Y%m%d')}.csv"
                
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Marca', 'Descripción', 'Color', 'Talle', 'Stock', 
                                   'Precio Costo', 'Precio Venta', 'Valor Total'])
                    
                    for item_id in tree.get_children():
                        vals = tree.item(item_id)['values']
                        writer.writerow(vals)
                
                messagebox.showinfo("Exportación Exitosa", f"Inventario exportado como {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar: {e}")
        
        # Definir botones con estilos modernos
        botones_accion = [
            ("✏️ Modificar", modificar_producto, "#f59e0b", "Modificar producto seleccionado"),
            ("🗑️ Eliminar", eliminar_producto, "#ef4444", "Eliminar productos seleccionados"),
            ("📊 Exportar CSV", exportar_inventario, "#03985a", "Exportar inventario a CSV"),
            ("🔄 Actualizar", lambda: self.mostrar_inventario(), "#4f46e5", "Actualizar vista del inventario")
        ]
        
        # Crear botones con espaciado uniforme
        button_spacing = 200
        start_x = (1180 - (len(botones_accion) * 160 + (len(botones_accion) - 1) * 28)) // 2
        
        for i, (texto, comando, color, tooltip) in enumerate(botones_accion):
            btn = tk.Button(actions_frame, text=texto, font=("Montserrat", 12, "bold"), 
                           bg=color, fg="#ffffff", bd=0, relief="flat", 
                           command=comando, cursor="hand2")
            btn.grid(row=0, column=i, padx=12, pady=10, sticky="n")
            
            # Aplicar efectos hover personalizados
            def crear_hover(btn, color_orig):
                def on_enter(e):
                    if color_orig == "#f59e0b":  # warning
                        btn.config(bg="#d97706")
                    elif color_orig == "#ef4444":  # danger  
                        btn.config(bg="#dc2626")
                    elif color_orig == "#03985a":  # success
                        btn.config(bg="#047857")
                    else:  # primary
                        btn.config(bg="#4338ca")
                
                def on_leave(e):
                    btn.config(bg=color_orig)
                
                return on_enter, on_leave
            
            on_enter, on_leave = crear_hover(btn, color)
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            crear_tooltip(btn, tooltip)
        
        # Registrar todos los widgets
        widgets.extend([header_frame, search_frame, stats_frame, tree, scrollbar, actions_frame])
        self.pantalla_widgets.extend(widgets)

    def _pantalla_cierre_caja(self, parent):
        """Pantalla de cierre de caja - redirige a ventas del día"""
        self.mostrar_ventas_dia()

    def _pantalla_modificar_producto(self, datos):
        """Pantalla para modificar productos con diseño moderno y profesional"""
        # datos: (marca, descripcion, color, talle, cantidad, costo, venta, amigo)
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        self._chip_volver(self.mostrar_inventario)
        
        widgets = []
        
        # === HEADER MODERNO ===
        header_frame = tk.Frame(self.canvas_bg, bg="#111827", height=60)
        self.canvas_bg.create_window(640, 50, window=header_frame, width=600, height=80, anchor="center")
        
        lbl_titulo = tk.Label(header_frame, text="✏️ MODIFICAR PRODUCTO", 
                             font=("Montserrat", 16, "bold"), bg="#111827", fg="#00ff88")
        lbl_titulo.pack(pady=15)
        
        # === PANEL PRINCIPAL CON DISEÑO MODERNO ===
        main_panel = tk.Frame(self.canvas_bg, bg="#1a1f2e", relief="solid", bd=1, 
                             highlightbackground="#3b82f6", highlightcolor="#3b82f6", highlightthickness=2)
        self.canvas_bg.create_window(640, 350, window=main_panel, width=900, height=600, anchor="center")
        
        # === CONTENIDO DEL FORMULARIO ===
        form_container = tk.Frame(main_panel, bg="#1a1f2e")
        form_container.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Título del formulario
        form_title = tk.Label(form_container, text="📝 Datos del Producto", 
                             font=("Montserrat", 14, "bold"), bg="#1a1f2e", fg="#60a5fa")
        form_title.pack(pady=(0, 20))
        
        # === CONTENEDOR DE 2 COLUMNAS ===
        columns_frame = tk.Frame(form_container, bg="#1a1f2e")
        columns_frame.pack(fill="both", expand=True)
        
        # Columna izquierda
        left_column = tk.Frame(columns_frame, bg="#1a1f2e", width=400, height=400)
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))
        left_column.pack_propagate(False)
        
        # Columna derecha
        right_column = tk.Frame(columns_frame, bg="#1a1f2e", width=400, height=400)
        right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))
        right_column.pack_propagate(False)
        
        # Configuración de campos distribuidos en 2 columnas
        campos_columna_izq = [
            ("Marca", "🏷️", "Ingrese la marca del producto"),
            ("Descripción", "📝", "Descripción del producto"),
            ("Color", "🎨", "Color del producto"),
            ("Talle", "📏", "Talle del producto")
        ]
        
        campos_columna_der = [
            ("Cantidad", "📦", "Cantidad en stock"),
            ("Precio de costo", "💰", "Precio de costo"),
            ("% Venta", "📈", "Porcentaje de venta"),
            ("% Amigo", "🤝", "Porcentaje amigo")
        ]
        
        entradas = {}
        
        # Crear campos columna izquierda
        for i, (campo, icono, placeholder) in enumerate(campos_columna_izq):
            # Contenedor para cada campo
            field_container = tk.Frame(left_column, bg="#1a1f2e")
            field_container.pack(fill="x", pady=8)
            
            # Label con icono
            lbl = tk.Label(field_container, text=f"{icono} {campo}:", 
                          font=("Montserrat", 12, "bold"), bg="#1a1f2e", fg="#e5e7eb")
            lbl.pack(anchor="w", pady=(0, 5))
            
            # Entry con estilo moderno
            ent = tk.Entry(field_container, font=("Montserrat", 12), 
                          bg="#374151", fg="#ffffff", bd=0, relief="flat",
                          insertbackground="#60a5fa")
            ent.pack(fill="x", pady=(0, 10), ipady=8)
            
            # Aplicar estilo moderno al entry
            aplicar_estilo_moderno_entry(ent)
            
            # Placeholder visual
            ent.insert(0, placeholder)
            ent.config(fg="#9ca3af")
            
            def on_focus_in(event, entry=ent, placeholder=placeholder):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg="#ffffff")
            
            def on_focus_out(event, entry=ent, placeholder=placeholder):
                if entry.get() == "":
                    entry.insert(0, placeholder)
                    entry.config(fg="#9ca3af")
            
            ent.bind("<FocusIn>", on_focus_in)
            ent.bind("<FocusOut>", on_focus_out)
            
            entradas[campo] = ent
            widgets.extend([lbl, ent])
        
        # Crear campos columna derecha
        for i, (campo, icono, placeholder) in enumerate(campos_columna_der):
            # Contenedor para cada campo
            field_container = tk.Frame(right_column, bg="#1a1f2e")
            field_container.pack(fill="x", pady=8)
            
            # Label con icono
            lbl = tk.Label(field_container, text=f"{icono} {campo}:", 
                          font=("Montserrat", 12, "bold"), bg="#1a1f2e", fg="#e5e7eb")
            lbl.pack(anchor="w", pady=(0, 5))
            
            # Entry con estilo moderno
            ent = tk.Entry(field_container, font=("Montserrat", 12), 
                          bg="#374151", fg="#ffffff", bd=0, relief="flat",
                          insertbackground="#60a5fa")
            ent.pack(fill="x", pady=(0, 10), ipady=8)
            
            # Aplicar estilo moderno al entry
            aplicar_estilo_moderno_entry(ent)
            
            # Placeholder visual
            ent.insert(0, placeholder)
            ent.config(fg="#9ca3af")
            
            def on_focus_in(event, entry=ent, placeholder=placeholder):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg="#ffffff")
            
            def on_focus_out(event, entry=ent, placeholder=placeholder):
                if entry.get() == "":
                    entry.insert(0, placeholder)
                    entry.config(fg="#9ca3af")
            
            ent.bind("<FocusIn>", on_focus_in)
            ent.bind("<FocusOut>", on_focus_out)
            
            entradas[campo] = ent
            widgets.extend([lbl, ent])
        
        # Cargar datos actuales (después de crear los placeholders)
        # Combinar ambas listas de campos para mantener el orden original
        todos_campos = campos_columna_izq + campos_columna_der
        for i, campo in enumerate(todos_campos):
            campo_nombre = campo[0]
            if campo_nombre in entradas:
                # Limpiar placeholder y cargar dato real
                entradas[campo_nombre].delete(0, tk.END)
                entradas[campo_nombre].config(fg="#ffffff")
                entradas[campo_nombre].insert(0, str(datos[i]))
        
        # === PANEL DE PRECIOS CALCULADOS ===
        precios_frame = tk.Frame(main_panel, bg="#1e293b", relief="raised", bd=1)
        precios_frame.pack(fill="x", padx=30, pady=(10, 10))
        
        precios_title = tk.Label(precios_frame, text="💡 Precios Calculados", 
                                font=("Montserrat", 12, "bold"), bg="#1e293b", fg="#00ff88")
        precios_title.pack(pady=8)
        
        # Labels para mostrar precios calculados
        lbl_precio_venta = tk.Label(precios_frame, text="Precio de Venta: $0.00", 
                                   font=("Montserrat", 11), bg="#1e293b", fg="#e5e7eb")
        lbl_precio_venta.pack(pady=2)
        
        lbl_precio_amigo = tk.Label(precios_frame, text="Precio Amigo: $0.00", 
                                   font=("Montserrat", 11), bg="#1e293b", fg="#e5e7eb")
        lbl_precio_amigo.pack(pady=2)
        
        # Función para calcular precios en tiempo real
        def calcular_precios(*args):
            try:
                costo = float(entradas["Precio de costo"].get() or 0)
                porc_venta = float(entradas["% Venta"].get() or 0)
                porc_amigo = float(entradas["% Amigo"].get() or 0)
                
                precio_venta = costo * (1 + porc_venta / 100)
                precio_amigo = costo * (1 + porc_amigo / 100)
                
                lbl_precio_venta.config(text=f"Precio de Venta: {self.formato_moneda(precio_venta)}")
                lbl_precio_amigo.config(text=f"Precio Amigo: {self.formato_moneda(precio_amigo)}")
            except:
                lbl_precio_venta.config(text="Precio de Venta: $0.00")
                lbl_precio_amigo.config(text="Precio Amigo: $0.00")
        
        # Vincular cálculo de precios a los campos relevantes
        entradas["Precio de costo"].bind("<KeyRelease>", calcular_precios)
        entradas["% Venta"].bind("<KeyRelease>", calcular_precios)
        entradas["% Amigo"].bind("<KeyRelease>", calcular_precios)
        
        # Calcular precios iniciales
        calcular_precios()
        
        # === BOTONES DE ACCIÓN (FUERA DEL PANEL PRINCIPAL) ===
        buttons_frame = tk.Frame(self.canvas_bg, bg="#0f172a")
        self.canvas_bg.create_window(640, 520, window=buttons_frame, width=900, height=60, anchor="center")
        
        def guardar():
            try:
                # Validar campos obligatorios
                marca = entradas["Marca"].get().strip()
                descripcion = entradas["Descripción"].get().strip()
                color = entradas["Color"].get().strip()
                talle = entradas["Talle"].get().strip()
                
                if not all([marca, descripcion, color, talle]):
                    messagebox.showwarning("Campos Requeridos", "Todos los campos son obligatorios.")
                    return
                
                cantidad = int(entradas["Cantidad"].get())
                precio_costo = float(entradas["Precio de costo"].get())
                porcentaje_venta = float(entradas["% Venta"].get())
                porcentaje_amigo = float(entradas["% Amigo"].get())
                
                # Validaciones adicionales
                if cantidad < 0:
                    messagebox.showwarning("Error", "La cantidad no puede ser negativa.")
                    return
                if precio_costo < 0:
                    messagebox.showwarning("Error", "El precio de costo no puede ser negativo.")
                    return
                if porcentaje_venta < 0 or porcentaje_amigo < 0:
                    messagebox.showwarning("Error", "Los porcentajes no pueden ser negativos.")
                    return
                
                # Eliminar producto anterior y agregar el modificado
                self.sistema.eliminar_producto(datos[0], datos[1], datos[2], datos[3])
                self.sistema.agregar_producto(marca, descripcion, color, talle, cantidad, precio_costo, porcentaje_venta, porcentaje_amigo)
                
                messagebox.showinfo("✅ Éxito", "Producto modificado correctamente.")
                self.mostrar_inventario()
                
            except ValueError as e:
                messagebox.showerror("❌ Error de Datos", "Por favor, verifique que los campos numéricos contengan valores válidos.")
            except Exception as e:
                messagebox.showerror("❌ Error", f"Error al modificar el producto: {str(e)}")
        
        def cancelar():
            if messagebox.askyesno("Cancelar", "¿Está seguro de que desea cancelar? Los cambios no se guardarán."):
                self.mostrar_inventario()
        
        # Botón Guardar
        btn_guardar = tk.Button(buttons_frame, text="💾 Guardar Cambios", 
                               font=("Montserrat", 12, "bold"), 
                               bg=COLOR_BOTON_SUCCESS, fg="#ffffff", 
                               bd=0, relief="flat", cursor="hand2",
                               command=guardar)
        btn_guardar.pack(side="left", padx=(0, 20))
        aplicar_estilo_moderno_boton(btn_guardar, "success")
        
        # Botón Cancelar
        btn_cancelar = tk.Button(buttons_frame, text="❌ Cancelar", 
                                font=("Montserrat", 12, "bold"), 
                                bg=COLOR_BOTON_DANGER, fg="#ffffff", 
                                bd=0, relief="flat", cursor="hand2",
                                command=cancelar)
        btn_cancelar.pack(side="left", padx=(0, 20))
        aplicar_estilo_moderno_boton(btn_cancelar, "danger")
        
        widgets.extend([main_panel, btn_guardar, btn_cancelar, lbl_precio_venta, lbl_precio_amigo])
        self.pantalla_widgets.extend(widgets)

    def mostrar_centro_ia(self):
        """Centro unificado de todas las funciones de Inteligencia Artificial - Versión Optimizada"""
        print("[DEBUG] mostrar_centro_ia() llamado  OPTIMIZADO - main.py:5397")
        self.limpiar_pantalla()
        # Usar logo especial para Panel IA (ALENRESULTADOS.png)
        if hasattr(self, 'logo_canvas_id') and self.logo_canvas_id:
            self.canvas_bg.delete(self.logo_canvas_id)
            self.logo_canvas_id = None
        self._colocar_logo_panel_ia()
        widgets = []
        
        # === PANEL DE NAVEGACIÓN IA MODERNIZADO ===
        frame_nav = tk.Frame(self.canvas_bg, bg="#0f1629", relief="raised", bd=2)
        self.canvas_bg.create_window(640, 120, window=frame_nav, width=1180, height=65, anchor="center")
        
        # Variable para controlar la vista activa
        self.vista_ia_activa = tk.StringVar(value="dashboard")
        
        # Configuración de botones de navegación con estilo moderno
        nav_buttons_config = [
            ("Dashboard", COLOR_CIAN, "#000000", "dashboard"),
            ("Reposición", "#4CAF50", "#ffffff", "reposicion"),
            ("Precios", "#FF9800", "#000000", "precios"),
            ("Análisis", "#9C27B0", "#ffffff", "analisis"),
            ("Exportar Todo", "#607D8B", "#ffffff", "exportar"),
            ("🔄 Actualizar", "#2196F3", "#ffffff", "actualizar")
        ]
        
        # Posiciones optimizadas para mejor distribución
        x_positions = [30, 180, 330, 480, 630, 820, 970]
        
        for i, (text, bg_color, fg_color, action) in enumerate(nav_buttons_config):
            if action == "exportar":
                command = self._exportar_centro_ia
            elif action == "actualizar":
                command = self._actualizar_centro_ia
            else:
                command = lambda a=action: self._cambiar_vista_ia(a)
            
            btn = tk.Button(frame_nav, text=text, font=("Montserrat", 12, "bold"), 
                           bg=bg_color, fg=fg_color, bd=0, relief="flat", cursor="hand2",
                           command=command)
            btn.place(x=x_positions[i], y=8, width=130, height=38)
            
            # Efectos hover optimizados
            if action == "dashboard":
                btn.bind("<Enter>", lambda e: e.widget.config(bg="#00E5FF"))
                btn.bind("<Leave>", lambda e: e.widget.config(bg=COLOR_CIAN))
            elif action == "reposicion":
                btn.bind("<Enter>", lambda e: e.widget.config(bg="#66BB6A"))
                btn.bind("<Leave>", lambda e: e.widget.config(bg="#4CAF50"))
            elif action == "precios":
                btn.bind("<Enter>", lambda e: e.widget.config(bg="#FFB74D"))
                btn.bind("<Leave>", lambda e: e.widget.config(bg="#FF9800"))
            elif action == "analisis":
                btn.bind("<Enter>", lambda e: e.widget.config(bg="#BA68C8"))
                btn.bind("<Leave>", lambda e: e.widget.config(bg="#9C27B0"))
            elif action == "exportar":
                btn.bind("<Enter>", lambda e: e.widget.config(bg="#78909C"))
                btn.bind("<Leave>", lambda e: e.widget.config(bg="#607D8B"))
            elif action == "actualizar":
                btn.bind("<Enter>", lambda e: e.widget.config(bg="#42A5F5"))
                btn.bind("<Leave>", lambda e: e.widget.config(bg="#2196F3"))
        
        # === ÁREA DE CONTENIDO DINÁMICO OPTIMIZADA ===
        self.frame_contenido_ia = tk.Frame(self.canvas_bg, bg=COLOR_FONDO)
        self.canvas_bg.create_window(640, 420, window=self.frame_contenido_ia, width=1200, height=520, anchor="center")
        
        # Cargar vista inicial
        self._cambiar_vista_ia("dashboard")
        
        # Chip volver en Centro IA
        self._chip_volver(self.mostrar_menu_secundario)
        
        widgets.extend([frame_nav])
        self.pantalla_widgets.extend(widgets)
    
    def mostrar_crear_ofertas(self):
        """Pantalla para crear y gestionar ofertas"""
        print("[DEBUG] mostrar_crear_ofertas() llamado  NEW - main.py:5474")
        if not self.require_role(["admin"]):
            return
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        self._chip_volver(self.mostrar_menu_secundario)
        self._chip_logout()
        self._pantalla_crear_ofertas(self.canvas_bg)

    def _pantalla_crear_ofertas(self, parent, solo_ofertas_activas=False):
        """Pantalla para crear y gestionar ofertas en productos - Versión optimizada y moderna"""
        widgets = []
        
        # === HEADER MODERNO ===
        header_frame = tk.Frame(self.canvas_bg, bg="#111827", height=60)
        self.canvas_bg.create_window(640, 50, window=header_frame, width=600, height=80, anchor="center")
        
        titulo_texto = "🎁 OFERTAS ACTIVAS" if solo_ofertas_activas else "🎁 CREAR Y GESTIONAR OFERTAS"
        lbl_titulo = tk.Label(header_frame, text=titulo_texto, 
                             font=("Montserrat", 16, "bold"), bg="#111827", fg="#00ff88")
        lbl_titulo.pack(pady=15)
        
        # === PANEL DE CONTROLES Y ESTADÍSTICAS ===
        controles_frame = tk.Frame(self.canvas_bg, bg="#0f1629", relief="raised", bd=2)
        self.canvas_bg.create_window(640, 110, window=controles_frame, width=1180, height=80, anchor="center")
        
        # Estadísticas de ofertas
        productos = self.sistema.inventario_actual()
        ofertas_activas = [p for p in productos if p.oferta and p.oferta.get('tipo')]
        total_productos = len(productos)
        
        stats_container = tk.Frame(controles_frame, bg="#0f1629")
        stats_container.pack(side="left", padx=20, pady=10)
        
        tk.Label(stats_container, text="📊 ESTADÍSTICAS:", font=("Montserrat", 13, "bold"), 
                bg="#0f1629", fg="#00ff88").pack(side="left", padx=(0, 10))
        
        tk.Label(stats_container, text=f"Total productos: {total_productos}", 
                font=("Montserrat", 12, "bold"), bg="#0f1629", fg="#e5e7eb").pack(side="left", padx=5)
        
        tk.Label(stats_container, text=f"Con ofertas: {len(ofertas_activas)}", 
                font=("Montserrat", 12, "bold"), bg="#0f1629", fg="#4ade80").pack(side="left", padx=5)
        
        porcentaje_ofertas = (len(ofertas_activas) / total_productos * 100) if total_productos > 0 else 0
        tk.Label(stats_container, text=f"({porcentaje_ofertas:.1f}%)", 
                font=("Montserrat", 12), bg="#0f1629", fg="#94a3b8").pack(side="left", padx=5)

        # Botón de cambio de vista
        btn_container = tk.Frame(controles_frame, bg="#0f1629")
        btn_container.pack(side="right", padx=20, pady=10)
        
        if solo_ofertas_activas:
            btn_vista = tk.Button(btn_container, text="📋 VER TODOS LOS PRODUCTOS", 
                                 font=("Montserrat", 10, "bold"), bg="#4f46e5", fg="#ffffff", 
                                 bd=0, relief="flat", cursor="hand2", padx=15, pady=6,
                                 command=lambda: self.mostrar_crear_ofertas())
        else:
            btn_vista = tk.Button(btn_container, text="🎁 VER SOLO OFERTAS ACTIVAS", 
                                 font=("Montserrat", 10, "bold"), bg="#059669", fg="#ffffff", 
                                 bd=0, relief="flat", cursor="hand2", padx=15, pady=6,
                                 command=lambda: self._mostrar_ofertas_activas())
        
        aplicar_estilo_moderno_boton(btn_vista, "primario" if solo_ofertas_activas else "success", hover_efecto=True)
        btn_vista.pack()
        
        # === MENSAJE SI NO HAY OFERTAS ACTIVAS ===
        if solo_ofertas_activas and not ofertas_activas:
            mensaje_frame = tk.Frame(self.canvas_bg, bg="#1e293b", relief="raised", bd=2)
            self.canvas_bg.create_window(640, 360, window=mensaje_frame, width=600, height=200, anchor="center")
            
            tk.Label(mensaje_frame, text="🎁", font=("Montserrat", 48), 
                    bg="#1e293b", fg="#6b7280").pack(pady=(20, 10))
            
            tk.Label(mensaje_frame, text="No hay ofertas activas", 
                    font=("Montserrat", 18, "bold"), bg="#1e293b", fg="#e5e7eb").pack(pady=5)
            
            tk.Label(mensaje_frame, text="Utilice 'VER TODOS LOS PRODUCTOS' para crear nuevas ofertas", 
                    font=("Montserrat", 12), bg="#1e293b", fg="#94a3b8").pack(pady=10)
            
            widgets.extend([header_frame, controles_frame, mensaje_frame])
            self.pantalla_widgets.extend(widgets)
            return
        
        # === CONFIGURACIÓN DE PRODUCTOS A MOSTRAR ===
        productos_a_mostrar = ofertas_activas if solo_ofertas_activas else productos
        
        # === LAYOUT DE DOS COLUMNAS ===
        # Columna izquierda: Lista de productos
        productos_frame = tk.Frame(self.canvas_bg, bg="#1a3d75", relief="raised", bd=2)
        productos_width = 750 if solo_ofertas_activas else 720
        self.canvas_bg.create_window(50, 180, window=productos_frame, 
                                   width=productos_width, height=520, anchor="nw")
        
        # Header de la tabla de productos
        productos_header = tk.Frame(productos_frame, bg="#1a3d75", height=40)
        productos_header.pack(fill="x", padx=8, pady=(8, 0))
        
        header_text = "🎁 PRODUCTOS CON OFERTAS ACTIVAS" if solo_ofertas_activas else "📋 SELECCIONAR PRODUCTOS"
        tk.Label(productos_header, text=header_text, font=("Montserrat", 14, "bold"), 
                bg="#1a3d75", fg="#00ff88").pack(pady=8)
        
        # TreeView de productos
        tree_container = tk.Frame(productos_frame, bg="#1a3d75")
        tree_container.pack(fill="both", expand=True, padx=8, pady=8)
        
        cols = ("Marca", "Descripción", "Color", "Talle", "Stock", "Precio", "Oferta")
        tree_productos = ttk.Treeview(tree_container, columns=cols, show="headings", height=18)
        aplicar_estilo_moderno_treeview(tree_productos)
        habilitar_ordenamiento_treeview(tree_productos)
        
        # Configurar columnas con anchos optimizados
        anchos = [90, 140, 70, 50, 50, 80, 140]
        for col, ancho in zip(cols, anchos):
            tree_productos.heading(col, text=col, anchor="center")
            tree_productos.column(col, width=ancho, anchor="center")
        
        # Scrollbar para la tabla
        scrollbar_productos = ttk.Scrollbar(tree_container, orient="vertical", command=tree_productos.yview)
        tree_productos.configure(yscrollcommand=scrollbar_productos.set)
        
        tree_productos.pack(side="left", fill="both", expand=True)
        scrollbar_productos.pack(side="right", fill="y")
        
        # Llenar datos de productos con colores de estado
        for p in productos_a_mostrar:
            oferta_actual = "Sin oferta"
            if p.oferta and p.oferta.get('tipo'):
                if p.oferta['tipo'] == 'porcentaje':
                    oferta_actual = f"🏷️ Desc. {p.oferta['valor']}%"
                elif p.oferta['tipo'] == 'cantidad':
                    oferta_actual = f"🎯 Oferta {p.oferta['valor']}"
                elif p.oferta['tipo'] == 'precio_manual':
                    oferta_actual = f"💰 Precio {self.formato_moneda(p.oferta['valor'])}"
            
            item_id = tree_productos.insert("", "end", values=(
                p.marca, p.descripcion, p.color, p.talle, p.cantidad,
                self.formato_moneda(p.precio_venta), oferta_actual
            ))
            
            # Colorear filas según el estado de la oferta
            if p.oferta and p.oferta.get('tipo'):
                tree_productos.set(item_id, "Oferta", oferta_actual)
        
        widgets.extend([header_frame, controles_frame, productos_frame])
        
        # === PANEL DE CONFIGURACIÓN DE OFERTAS (COLUMNA DERECHA) ===
        if not solo_ofertas_activas:
            ofertas_frame = tk.Frame(self.canvas_bg, bg="#1a3d75", relief="raised", bd=2)
            self.canvas_bg.create_window(800, 180, window=ofertas_frame, width=430, height=520, anchor="nw")
            
            # Header del panel de ofertas
            ofertas_header = tk.Frame(ofertas_frame, bg="#1a3d75", height=40)
            ofertas_header.pack(fill="x", padx=8, pady=(8, 0))

            tk.Label(ofertas_header, text="⚙️ CONFIGURAR OFERTA",
                    font=("Montserrat", 14, "bold"), bg="#1a3d75", fg="#00ff88").pack(pady=8)

            # Contenido del panel
            contenido_ofertas = tk.Frame(ofertas_frame, bg="#1a3d75")
            contenido_ofertas.pack(fill="both", expand=True, padx=15, pady=10)
            
            # === SECCIÓN TIPO DE OFERTA ===
            tipo_section = tk.Frame(contenido_ofertas, bg="#0a0d1a", relief="raised", bd=1)
            tipo_section.pack(fill="x", pady=(0, 15))
            
            tk.Label(tipo_section, text="🏷️ Tipo de Oferta:", font=("Montserrat", 12, "bold"), 
                    bg="#0a0d1a", fg="#e5e7eb").pack(pady=(10, 5), padx=15, anchor="w")
            
            tipo_var = tk.StringVar(value="porcentaje")
            combo_tipo = ttk.Combobox(tipo_section, textvariable=tipo_var, 
                                     values=["porcentaje", "cantidad", "precio_manual"], 
                                     font=("Montserrat", 11), state="readonly", width=25)
            aplicar_estilo_moderno_combobox(combo_tipo)
            combo_tipo.pack(pady=(0, 10), padx=15)
            
            # === SECCIÓN VALOR DE LA OFERTA ===
            valor_section = tk.Frame(contenido_ofertas, bg="#0a0d1a", relief="raised", bd=1)
            valor_section.pack(fill="x", pady=(0, 15))
            
            tk.Label(valor_section, text="💰 Valor de la Oferta:", font=("Montserrat", 12, "bold"), 
                    bg="#0a0d1a", fg="#e5e7eb").pack(pady=(10, 5), padx=15, anchor="w")
            
            valor_var = tk.StringVar()
            ent_valor = tk.Entry(valor_section, textvariable=valor_var, font=("Montserrat", 11), 
                                bg="#ffffff", fg="#000000", bd=2, relief="ridge")
            aplicar_estilo_moderno_entry(ent_valor)
            ent_valor.pack(pady=(0, 10), padx=15, fill="x")
            
            # === SECCIÓN INSTRUCCIONES DINÁMICAS ===
            instrucciones_section = tk.Frame(contenido_ofertas, bg="#0f1629", relief="raised", bd=1)
            instrucciones_section.pack(fill="x", pady=(0, 20))
            
            tk.Label(instrucciones_section, text="ℹ️ Instrucciones:", font=("Montserrat", 13, "bold"), 
                    bg="#0f1629", fg="#00ff88").pack(pady=(8, 5), padx=12, anchor="w")
            
            lbl_instrucciones = tk.Label(instrucciones_section, text="", font=("Montserrat", 12), 
                                        bg="#0f1629", fg="#e5e7eb", wraplength=350, justify="left")
            lbl_instrucciones.pack(pady=(0, 8), padx=12, anchor="w")
            
            def actualizar_instrucciones(event=None):
                tipo = tipo_var.get()
                if tipo == "porcentaje":
                    texto = "• Ingrese el porcentaje de descuento (ej: 20 para 20% off)\n• Se aplicará sobre el precio de venta actual\n• Valores válidos: 1-99"
                elif tipo == "cantidad":
                    texto = "• Formato: CompraXPaga (ej: 3x2, 2x1)\n• El cliente compra X unidades y paga Y\n• Ejemplo: 3x2 = compra 3, paga 2"
                elif tipo == "precio_manual":
                    texto = "• Ingrese el precio especial en pesos\n• Reemplazará completamente el precio normal\n• Debe ser menor al precio actual"
                lbl_instrucciones.config(text=texto)
            
            combo_tipo.bind("<<ComboboxSelected>>", actualizar_instrucciones)
            actualizar_instrucciones()  # Mostrar instrucciones iniciales
            
            # === BOTONES DE ACCIÓN ===
            botones_frame = tk.Frame(contenido_ofertas, bg="#1a3d75")
            botones_frame.pack(fill="x", pady=(10, 0))
            
            btn_aplicar = tk.Button(botones_frame, text="✅ APLICAR OFERTA", 
                                   font=("Montserrat", 12, "bold"), bg="#059669", fg="#ffffff", 
                                   bd=0, relief="flat", cursor="hand2", pady=10)
            aplicar_estilo_moderno_boton(btn_aplicar, "success", hover_efecto=True)
            btn_aplicar.pack(fill="x", pady=(0, 8))
            
            btn_quitar = tk.Button(botones_frame, text="❌ QUITAR OFERTA", 
                                  font=("Montserrat", 12, "bold"), bg="#ef4444", fg="#ffffff", 
                                  bd=0, relief="flat", cursor="hand2", pady=10)
            aplicar_estilo_moderno_boton(btn_quitar, "danger", hover_efecto=True)
            btn_quitar.pack(fill="x", pady=(0, 8))
            
            btn_limpiar = tk.Button(botones_frame, text="🔄 LIMPIAR CAMPOS", 
                                   font=("Montserrat", 11, "bold"), bg="#6b7280", fg="#ffffff", 
                                   bd=0, relief="flat", cursor="hand2", pady=8)
            aplicar_estilo_moderno_boton(btn_limpiar, "secundario", hover_efecto=True)
            btn_limpiar.pack(fill="x")
            
            def limpiar_campos():
                """Limpia los campos del formulario"""
                valor_var.set("")
                combo_tipo.set("porcentaje")
                actualizar_instrucciones()
                tree_productos.selection_remove(tree_productos.selection())
            
            btn_limpiar.config(command=limpiar_campos)
            
            widgets.append(ofertas_frame)
            
            # === FUNCIONES DE LÓGICA MEJORADAS ===
            def aplicar_oferta():
                seleccion = tree_productos.selection()
                if not seleccion:
                    messagebox.showwarning("⚠️ Selección Requerida", 
                                         "Por favor, seleccione al menos un producto de la lista para aplicar la oferta.")
                    return
                
                tipo = tipo_var.get()
                valor_str = valor_var.get().strip()
                
                if not valor_str:
                    messagebox.showwarning("⚠️ Valor Requerido", 
                                         "Por favor, ingrese el valor de la oferta en el campo correspondiente.")
                    return
                
                try:
                    valor = None
                    
                    # Validar y procesar según el tipo de oferta
                    if tipo == "porcentaje":
                        valor = float(valor_str)
                        if valor <= 0 or valor >= 100:
                            raise ValueError("El porcentaje debe estar entre 1 y 99")
                    elif tipo == "cantidad":
                        if 'x' not in valor_str.lower():
                            raise ValueError("Use el formato CompraXPaga (ejemplo: 3x2, 2x1)")
                        partes = valor_str.lower().split('x')
                        if len(partes) != 2:
                            raise ValueError("Formato incorrecto. Use CompraXPaga")
                        compra, paga = int(partes[0]), int(partes[1])
                        if compra <= paga or compra <= 0 or paga <= 0:
                            raise ValueError("La cantidad a comprar debe ser mayor a la cantidad a pagar")
                        valor = valor_str.upper()
                    elif tipo == "precio_manual":
                        valor = float(valor_str)
                        if valor <= 0:
                            raise ValueError("El precio debe ser mayor a 0")
                    
                    if valor is None:
                        raise ValueError("Tipo de oferta no válido")
                    
                    # Aplicar oferta a productos seleccionados
                    productos_modificados = 0
                    productos_con_error = []
                    
                    for item_id in seleccion:
                        item = tree_productos.item(item_id)
                        valores = item['values']
                        marca, descripcion, color, talle = valores[0], valores[1], valores[2], valores[3]
                        
                        producto = self.sistema.buscar_producto(marca, descripcion, color, talle)
                        if producto:
                            # Validación adicional para precio manual
                            if tipo == "precio_manual" and valor >= producto.precio_venta:
                                productos_con_error.append(f"{descripcion} {color} {talle}")
                                continue
                            
                            producto.oferta = {'tipo': tipo, 'valor': valor}
                            productos_modificados += 1
                    
                    # Guardar cambios si hay modificaciones
                    if productos_modificados > 0:
                        self.sistema.guardar_productos()
                        
                        mensaje = f"✅ Oferta aplicada exitosamente a {productos_modificados} producto(s)."
                        if productos_con_error:
                            mensaje += f"\n\n⚠️ Productos omitidos (precio especial >= precio actual):\n" + "\n".join(productos_con_error)
                        
                        messagebox.showinfo("Éxito", mensaje)
                        limpiar_campos()
                        self.mostrar_crear_ofertas()  # Refrescar pantalla
                    else:
                        messagebox.showwarning("Sin Cambios", "No se pudo aplicar la oferta a ningún producto.")
                    
                except ValueError as e:
                    messagebox.showerror("❌ Error de Validación", f"Valor inválido: {e}")
                except Exception as e:
                    messagebox.showerror("❌ Error", f"Error inesperado: {e}")
            
            def quitar_oferta():
                seleccion = tree_productos.selection()
                if not seleccion:
                    messagebox.showwarning("⚠️ Selección Requerida", 
                                         "Por favor, seleccione al menos un producto para quitar la oferta.")
                    return
                
                # Confirmar acción
                respuesta = messagebox.askyesno("🗑️ Confirmar Eliminación", 
                                              f"¿Está seguro de que desea quitar las ofertas de {len(seleccion)} producto(s) seleccionado(s)?")
                if not respuesta:
                    return
                
                productos_modificados = 0
                for item_id in seleccion:
                    item = tree_productos.item(item_id)
                    valores = item['values']
                    marca, descripcion, color, talle = valores[0], valores[1], valores[2], valores[3]
                    
                    producto = self.sistema.buscar_producto(marca, descripcion, color, talle)
                    if producto and producto.oferta:
                        producto.oferta = {}
                        productos_modificados += 1
                
                if productos_modificados > 0:
                    self.sistema.guardar_productos()
                    messagebox.showinfo("✅ Éxito", f"Oferta eliminada de {productos_modificados} producto(s).")
                    limpiar_campos()
                    self.mostrar_crear_ofertas()  # Refrescar pantalla
                else:
                    messagebox.showinfo("ℹ️ Sin Cambios", "Los productos seleccionados no tenían ofertas activas.")
            
            # Asignar comandos a botones
            btn_aplicar.config(command=aplicar_oferta)
            btn_quitar.config(command=quitar_oferta)
        
        # === VISTA DE OFERTAS ACTIVAS - PANEL DE ACCIONES ===
        else:
            if ofertas_activas:
                acciones_frame = tk.Frame(self.canvas_bg, bg="#1e293b", relief="raised", bd=2)
                self.canvas_bg.create_window(800, 180, window=acciones_frame, width=430, height=200, anchor="nw")
                
                # Header del panel de acciones
                acciones_header = tk.Frame(acciones_frame, bg="#0f1629", height=40)
                acciones_header.pack(fill="x", padx=8, pady=(8, 0))
                
                tk.Label(acciones_header, text="🔧 ACCIONES RÁPIDAS", 
                        font=("Montserrat", 14, "bold"), bg="#0f1629", fg="#00ff88").pack(pady=8)
                
                # Contenido del panel de acciones
                contenido_acciones = tk.Frame(acciones_frame, bg="#1e293b")
                contenido_acciones.pack(fill="both", expand=True, padx=15, pady=15)
                
                # Información de ofertas
                info_frame = tk.Frame(contenido_acciones, bg="#0a0d1a", relief="raised", bd=1)
                info_frame.pack(fill="x", pady=(0, 15))
                
                tk.Label(info_frame, text="📊 Resumen de Ofertas Activas:", 
                        font=("Montserrat", 11, "bold"), bg="#0a0d1a", fg="#e5e7eb").pack(pady=(8, 5), padx=12, anchor="w")
                
                # Contar tipos de ofertas
                ofertas_por_tipo = {"porcentaje": 0, "cantidad": 0, "precio_manual": 0}
                for producto in ofertas_activas:
                    tipo = producto.oferta.get('tipo', '')
                    if tipo in ofertas_por_tipo:
                        ofertas_por_tipo[tipo] += 1
                
                tipos_texto = f"• Descuentos por porcentaje: {ofertas_por_tipo['porcentaje']}\n"
                tipos_texto += f"• Ofertas por cantidad: {ofertas_por_tipo['cantidad']}\n"
                tipos_texto += f"• Precios especiales: {ofertas_por_tipo['precio_manual']}"
                
                tk.Label(info_frame, text=tipos_texto, font=("Montserrat", 10), 
                        bg="#0a0d1a", fg="#94a3b8", justify="left").pack(pady=(0, 8), padx=12, anchor="w")
                
                # Botón para quitar ofertas seleccionadas
                btn_quitar_seleccionadas = tk.Button(contenido_acciones, text="🗑️ QUITAR OFERTAS SELECCIONADAS", 
                                                    font=("Montserrat", 12, "bold"), bg="#ef4444", fg="#ffffff", 
                                                    bd=0, relief="flat", cursor="hand2", pady=10)
                aplicar_estilo_moderno_boton(btn_quitar_seleccionadas, "danger", hover_efecto=True)
                btn_quitar_seleccionadas.pack(fill="x", pady=(0, 8))
                
                # Botón para quitar TODAS las ofertas
                btn_quitar_todas = tk.Button(contenido_acciones, text="⚠️ QUITAR TODAS LAS OFERTAS", 
                                            font=("Montserrat", 11, "bold"), bg="#7c2d12", fg="#ffffff", 
                                            bd=0, relief="flat", cursor="hand2", pady=8)
                aplicar_estilo_moderno_boton(btn_quitar_todas, "danger", hover_efecto=True)
                btn_quitar_todas.pack(fill="x")
                
                def quitar_ofertas_seleccionadas():
                    seleccion = tree_productos.selection()
                    if not seleccion:
                        messagebox.showwarning("⚠️ Selección Requerida", 
                                             "Por favor, seleccione al menos un producto para quitar la oferta.")
                        return
                    
                    respuesta = messagebox.askyesno("🗑️ Confirmar Eliminación", 
                                                  f"¿Está seguro de que desea quitar las ofertas de {len(seleccion)} producto(s) seleccionado(s)?")
                    if not respuesta:
                        return
                    
                    productos_modificados = 0
                    for item_id in seleccion:
                        item = tree_productos.item(item_id)
                        valores = item['values']
                        marca, descripcion, color, talle = valores[0], valores[1], valores[2], valores[3]
                        
                        producto = self.sistema.buscar_producto(marca, descripcion, color, talle)
                        if producto and producto.oferta:
                            producto.oferta = {}
                            productos_modificados += 1
                    
                    if productos_modificados > 0:
                        self.sistema.guardar_productos()
                        messagebox.showinfo("✅ Éxito", f"Oferta eliminada de {productos_modificados} producto(s).")
                        self._mostrar_ofertas_activas()  # Refrescar vista
                    else:
                        messagebox.showinfo("ℹ️ Sin Cambios", "Los productos seleccionados no tenían ofertas activas.")
                
                def quitar_todas_las_ofertas():
                    respuesta = messagebox.askyesno("⚠️ CONFIRMACIÓN CRÍTICA", 
                                                  f"¿Está COMPLETAMENTE SEGURO de que desea quitar TODAS las {len(ofertas_activas)} ofertas activas?\n\nEsta acción NO se puede deshacer.")
                    if not respuesta:
                        return
                    
                    productos_modificados = 0
                    for producto in ofertas_activas:
                        if producto.oferta:
                            producto.oferta = {}
                            productos_modificados += 1
                    
                    if productos_modificados > 0:
                        self.sistema.guardar_productos()
                        messagebox.showinfo("✅ Completado", f"Se eliminaron todas las ofertas ({productos_modificados} productos afectados).")
                        self._mostrar_ofertas_activas()  # Refrescar vista
                
                btn_quitar_seleccionadas.config(command=quitar_ofertas_seleccionadas)
                btn_quitar_todas.config(command=quitar_todas_las_ofertas)
                
                widgets.append(acciones_frame)
        
        # === TOOLTIPS INFORMATIVOS ===
        if not solo_ofertas_activas:
            crear_tooltip(btn_aplicar, "Aplicar la oferta configurada a los productos seleccionados")
            crear_tooltip(btn_quitar, "Quitar ofertas de los productos seleccionados")
            crear_tooltip(btn_limpiar, "Limpiar todos los campos del formulario")
            crear_tooltip(combo_tipo, "Seleccione el tipo de oferta que desea crear")
            crear_tooltip(ent_valor, "Ingrese el valor según el tipo de oferta seleccionado")
        
        self.pantalla_widgets.extend(widgets)
    
    def _mostrar_ofertas_activas(self):
        """Función auxiliar para mostrar solo las ofertas activas"""
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        self._pantalla_crear_ofertas(self.canvas_bg, solo_ofertas_activas=True)
        
        # Chip volver para la vista de ofertas activas
        self._chip_volver(self.mostrar_menu_secundario)
    
    def _cambiar_vista_ia(self, vista):
        """Cambia entre las diferentes vistas del centro IA"""
        self.vista_ia_activa.set(vista)
        
        # Limpiar contenido anterior
        for widget in self.frame_contenido_ia.winfo_children():
            widget.destroy()
        
        if vista == "dashboard":
            self._mostrar_dashboard_ia()
        elif vista == "reposicion":
            self._mostrar_reposicion_ia()
        elif vista == "precios":
            self._mostrar_precios_ia()
        elif vista == "analisis":
            self._mostrar_analisis_ia()
    
    def _mostrar_dashboard_ia(self):
        """Dashboard principal con métricas generales - Versión Visual Optimizada y Moderna"""
        # Limpiar contenido anterior
        for widget in self.frame_contenido_ia.winfo_children():
            widget.destroy()
        
        # === TÍTULO DE SECCIÓN OPTIMIZADO ===
        titulo_dashboard = tk.Label(self.frame_contenido_ia, 
                                   text="📊 DASHBOARD EJECUTIVO", 
                                   font=("Montserrat", 16, "bold"), 
                                   bg="#1a3d75", 
                                   fg="#00E5FF")
        titulo_dashboard.place(x=600, y=10, anchor="center")
        
        # === PANELES DE MÉTRICAS PRINCIPALES (FILA SUPERIOR) ===
        # Panel de alertas críticas - más compacto
        frame_alertas = tk.Frame(self.frame_contenido_ia, bg="#dc2626", relief="flat", bd=0)
        frame_alertas.place(x=20, y=40, width=280, height=100)
        
        # Sombra sutil para alertas
        shadow_alertas = tk.Frame(self.frame_contenido_ia, bg="#991b1b", relief="flat", bd=0)
        shadow_alertas.place(x=22, y=42, width=280, height=100)
        self.frame_contenido_ia.update()
        frame_alertas.lift()
        
        lbl_alertas_titulo = tk.Label(frame_alertas, 
                                     text="🚨 ALERTAS CRÍTICAS", 
                                     font=("Montserrat", 11, "bold"), 
                                     bg="#dc2626", 
                                     fg="#ffffff")
        lbl_alertas_titulo.pack(pady=(8,3))
        
        # Calcular alertas con formato compacto
        productos_criticos = self._obtener_productos_criticos()
        texto_alertas = f"• {len(productos_criticos)} productos críticos\n• Requiere atención inmediata"
        
        lbl_alertas = tk.Label(frame_alertas, 
                              text=texto_alertas, 
                              font=("Montserrat", 9), 
                              bg="#dc2626", 
                              fg="#ffffff", 
                              justify="left")
        lbl_alertas.pack(pady=3)
        
        # Panel productos estrella - optimizado
        frame_estrella = tk.Frame(self.frame_contenido_ia, bg="#059669", relief="flat", bd=0)
        frame_estrella.place(x=320, y=40, width=280, height=100)
        
        # Sombra para productos estrella
        shadow_estrella = tk.Frame(self.frame_contenido_ia, bg="#047857", relief="flat", bd=0)
        shadow_estrella.place(x=322, y=42, width=280, height=100)
        self.frame_contenido_ia.update()
        frame_estrella.lift()
        
        lbl_estrella_titulo = tk.Label(frame_estrella, 
                                      text="⭐ PRODUCTOS ESTRELLA", 
                                      font=("Montserrat", 11, "bold"), 
                                      bg="#059669", 
                                      fg="#ffffff")
        lbl_estrella_titulo.pack(pady=(8,3))
        
        productos_estrella = self._obtener_productos_estrella()
        texto_estrella = f"• {len(productos_estrella)} productos top\n• Alta rotación confirmada"
        
        lbl_estrella = tk.Label(frame_estrella, 
                               text=texto_estrella, 
                               font=("Montserrat", 9), 
                               bg="#059669", 
                               fg="#ffffff", 
                               justify="left")
        lbl_estrella.pack(pady=3)
        
        # Panel métricas generales - compacto
        frame_metricas = tk.Frame(self.frame_contenido_ia, bg="#1d4ed8", relief="flat", bd=0)
        frame_metricas.place(x=620, y=40, width=280, height=100)
        
        # Sombra para métricas
        shadow_metricas = tk.Frame(self.frame_contenido_ia, bg="#1e40af", relief="flat", bd=0)
        shadow_metricas.place(x=622, y=42, width=280, height=100)
        self.frame_contenido_ia.update()
        frame_metricas.lift()
        
        lbl_metricas_titulo = tk.Label(frame_metricas, 
                                      text="📈 MÉTRICAS IA", 
                                      font=("Montserrat", 11, "bold"), 
                                      bg="#1d4ed8", 
                                      fg="#ffffff")
        lbl_metricas_titulo.pack(pady=(8,3))
        
        total_productos = len(self.sistema.productos)
        productos_movimiento = len([p for p in self.sistema.productos if self._obtener_ventas_producto(p, 30) > 0])
        porcentaje_activo = (productos_movimiento / max(1, total_productos)) * 100
        
        texto_metricas = f"• {total_productos} productos totales\n• {porcentaje_activo:.1f}% productos activos"
        
        lbl_metricas = tk.Label(frame_metricas, 
                               text=texto_metricas, 
                               font=("Montserrat", 9), 
                               bg="#1d4ed8", 
                               fg="#ffffff", 
                               justify="left")
        lbl_metricas.pack(pady=3)
        
        # Panel estado IA - nuevo
        frame_ia_status = tk.Frame(self.frame_contenido_ia, bg="#7c3aed", relief="flat", bd=0)
        frame_ia_status.place(x=920, y=40, width=260, height=100)
        
        # Sombra para estado IA
        shadow_ia_status = tk.Frame(self.frame_contenido_ia, bg="#6d28d9", relief="flat", bd=0)
        shadow_ia_status.place(x=922, y=42, width=260, height=100)
        self.frame_contenido_ia.update()
        frame_ia_status.lift()
        
        lbl_ia_titulo = tk.Label(frame_ia_status, 
                                text="🤖 ESTADO IA", 
                                font=("Montserrat", 11, "bold"), 
                                bg="#7c3aed", 
                                fg="#ffffff")
        lbl_ia_titulo.pack(pady=(8,3))
        
        texto_ia = "• Sistema operativo al 100%\n• Análisis en tiempo real"
        
        lbl_ia = tk.Label(frame_ia_status, 
                         text=texto_ia, 
                         font=("Montserrat", 9), 
                         bg="#7c3aed", 
                         fg="#ffffff", 
                         justify="left")
        lbl_ia.pack(pady=3)
        
        # === TABLA RESUMEN EJECUTIVO OPTIMIZADA ===
        frame_tabla = tk.Frame(self.frame_contenido_ia, bg="#1a3d75", relief="raised", bd=2)
        frame_tabla.place(x=20, y=160, width=1160, height=520)
        
        lbl_resumen = tk.Label(frame_tabla, 
                              text="📋 RESUMEN EJECUTIVO - ANÁLISIS INTELIGENTE", 
                              font=("Montserrat", 14, "bold"), 
                              bg="#1a3d75", 
                              fg="#45cdff")
        lbl_resumen.pack(pady=(10,8))
        
        # Frame para la tabla con espaciado optimizado
        tabla_frame = tk.Frame(frame_tabla, bg="#1e293b")
        tabla_frame.pack(fill="both", expand=True, padx=10, pady=(0,5))
        
        cols = ("📊 Categoría", "Cantidad", "Estado", "Acción Sugerida IA", "Prioridad")
        tree_resumen = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=8)
        aplicar_estilo_moderno_treeview(tree_resumen)
        
        # Anchos optimizados para mejor distribución
        anchos = [200, 90, 110, 300, 110]
        for col, ancho in zip(cols, anchos):
            tree_resumen.heading(col, text=col, anchor="center")
            tree_resumen.column(col, width=ancho, anchor="center")
        
        tree_resumen.pack(fill="both", expand=True)
        
        # Llenar datos del resumen con información actualizada
        datos_resumen = [
            ("🔴 Stock Crítico", str(len(productos_criticos)), "CRÍTICO", "Reposición inmediata requerida", "ALTA"),
            ("⭐ Productos Estrella", str(len(productos_estrella)), "EXCELENTE", "Mantener stock alto - son ganadores", "ALTA"),
            ("💰 Oportunidades Precio", "Analizando...", "PROCESO", "Revisar márgenes automáticamente", "MEDIA"),
            ("📈 Tendencias Alcistas", "Monitoreando...", "ACTIVO", "Aumentar stock preventivamente", "MEDIA"),
            ("📉 Productos Lentos", "Evaluando...", "ATENCIÓN", "Activar promociones inteligentes", "MEDIA"),
            ("🤖 IA Operativa", "100%", "ONLINE", "Sistema funcionando correctamente", "INFO"),
            ("📊 Análisis Completo", f"{total_productos} items", "ACTUALIZADO", "Datos procesados exitosamente", "INFO")
        ]
        
        # Agregar filas con iconos de prioridad mejorados
        for item in datos_resumen:
            item_id = tree_resumen.insert("", "end", values=item)
            if item[4] == "ALTA":
                tree_resumen.set(item_id, "Prioridad", "🔥 ALTA")
            elif item[4] == "MEDIA":
                tree_resumen.set(item_id, "Prioridad", "⚡ MEDIA")
            else:
                tree_resumen.set(item_id, "Prioridad", "ℹ️ INFO")
    
    def _mostrar_reposicion_ia(self):
        """Vista de sugerencias de reposición - Versión Visual Optimizada y Moderna"""
        # Limpiar contenido anterior
        for widget in self.frame_contenido_ia.winfo_children():
            widget.destroy()
        
        # === TÍTULO DE SECCIÓN OPTIMIZADO ===
        titulo_reposicion = tk.Label(self.frame_contenido_ia, 
                                    text="📦 ANÁLISIS INTELIGENTE DE REPOSICIÓN", 
                                    font=("Montserrat", 16, "bold"), 
                                    bg=COLOR_FONDO, 
                                    fg="#38A169")
        titulo_reposicion.place(x=600, y=10, anchor="center")
        
        # === PANEL DE CONFIGURACIÓN COMPACTO ===
        frame_config = tk.Frame(self.frame_contenido_ia, bg="#1e293b", relief="raised", bd=2)
        frame_config.place(x=20, y=40, width=1160, height=60)
        
        # Sombra para el panel de configuración
        shadow_config = tk.Frame(self.frame_contenido_ia, bg="#0f172a", relief="flat", bd=0)
        shadow_config.place(x=22, y=42, width=1160, height=60)
        self.frame_contenido_ia.update()
        frame_config.lift()
        
        # Título del panel de configuración
        lbl_config_titulo = tk.Label(frame_config, 
                                     text="⚙️ CONFIGURACIÓN DEL ANÁLISIS", 
                                     font=("Montserrat", 11, "bold"), 
                                     bg="#1e293b", 
                                     fg="#f1f5f9")
        lbl_config_titulo.place(x=25, y=8)
        
        # Controles de configuración con layout optimizado
        tk.Label(frame_config, 
                text="Período:", 
                font=("Montserrat", 10, "bold"), 
                bg="#1e293b", 
                fg="#cbd5e1").place(x=25, y=32)
        
        dias_var = tk.StringVar(value="30")
        combo_dias = ttk.Combobox(frame_config, 
                                 textvariable=dias_var, 
                                 values=["7", "15", "30", "60", "90"], 
                                 font=("Montserrat", 10), 
                                 state="readonly", 
                                 width=8)
        aplicar_estilo_moderno_combobox(combo_dias)
        combo_dias.place(x=90, y=32)
        
        tk.Label(frame_config, 
                text="Stock mín (%):", 
                font=("Montserrat", 10, "bold"), 
                bg="#1e293b", 
                fg="#cbd5e1").place(x=200, y=32)
        
        umbral_var = tk.StringVar(value="20")
        combo_umbral = ttk.Combobox(frame_config, 
                                   textvariable=umbral_var, 
                                   values=["10", "15", "20", "25", "30"], 
                                   font=("Montserrat", 10), 
                                   state="readonly", 
                                   width=8)
        aplicar_estilo_moderno_combobox(combo_umbral)
        combo_umbral.place(x=300, y=32)
        
        # Indicador de estado IA
        lbl_ia_status = tk.Label(frame_config, 
                                text="🤖 IA Analizando...", 
                                font=("Montserrat", 10, "bold"), 
                                bg="#1e293b", 
                                fg="#00E5FF")
        lbl_ia_status.place(x=420, y=32)
        
        # Botón de análisis manual
        btn_analizar = tk.Button(frame_config, 
                                text="🔄 Analizar", 
                                font=("Montserrat", 9, "bold"), 
                                bg="#059669", 
                                fg="#ffffff", 
                                bd=0, 
                                relief="flat", 
                                cursor="hand2")
        btn_analizar.place(x=600, y=28, width=100, height=25)
        
        # Panel de estadísticas rápidas
        lbl_stats = tk.Label(frame_config, 
                            text="📊 Productos críticos: Calculando...", 
                            font=("Montserrat", 10), 
                            bg="#1e293b", 
                            fg="#94a3b8")
        lbl_stats.place(x=720, y=32)
        
        # === TABLA DE REPOSICIÓN OPTIMIZADA ===
        frame_tabla = tk.Frame(self.frame_contenido_ia, bg="#1e293b", relief="raised", bd=2)
        frame_tabla.place(x=20, y=120, width=1160, height=300)
        
        # Título de la tabla
        lbl_tabla_titulo = tk.Label(frame_tabla, 
                                   text="📊 SUGERENCIAS INTELIGENTES DE REPOSICIÓN", 
                                   font=("Montserrat", 12, "bold"), 
                                   bg="#1e293b", 
                                   fg="#f1f5f9")
        lbl_tabla_titulo.pack(pady=(8,5))
        
        # Frame para la tabla
        tabla_frame = tk.Frame(frame_tabla, bg="#1e293b")
        tabla_frame.pack(fill="both", expand=True, padx=12, pady=(0,12))
        
        cols = ("🚨 Urgencia", "Marca", "Producto", "Color/Talle", "Stock Actual", 
                "Velocidad/día", "Días Restantes", "💡 Sugerencia IA")
        tree_reposicion = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=10)
        aplicar_estilo_moderno_treeview(tree_reposicion)
        
        # Anchos optimizados para mejor visualización
        anchos = [70, 100, 180, 100, 90, 100, 110, 150]
        for col, ancho in zip(cols, anchos):
            tree_reposicion.heading(col, text=col, anchor="center")
            tree_reposicion.column(col, width=ancho, anchor="center")
        
        tree_reposicion.pack(fill="both", expand=True)
        
        # Función de actualización optimizada
        def actualizar_reposicion():
            # Actualizar indicador de estado
            lbl_ia_status.config(text="🤖 Procesando...", fg="#FFA500")
            self.frame_contenido_ia.update()
            
            dias = int(dias_var.get())
            umbral = float(umbral_var.get()) / 100
            sugerencias = self._calcular_sugerencias_ia(dias, umbral)
            
            # Limpiar tabla
            for item in tree_reposicion.get_children():
                tree_reposicion.delete(item)
            
            # Actualizar estadísticas
            productos_criticos_count = len([s for s in sugerencias if s.get('dias_restantes', 999) <= 7 or s.get('stock_actual', 999) <= 5])
            lbl_stats.config(text=f"📊 Productos críticos: {productos_criticos_count} | Total analizados: {len(sugerencias)}")
            
            # Llenar tabla con datos optimizados
            for sugerencia in sugerencias[:20]:  # Limitar para mejor rendimiento
                p = sugerencia['producto']
                urgencia = (
                    '🔴 CRÍTICO' if sugerencia['dias_restantes'] <= 3 else
                    '🟡 URGENTE' if sugerencia['dias_restantes'] <= 7 else
                    '🟢 NORMAL' if sugerencia['dias_restantes'] <= 14 else
                    'ℹ️ BAJA'
                )
                tree_reposicion.insert("", "end", values=(
                    urgencia,
                    p.marca,
                    (p.descripcion[:25] + "...") if len(p.descripcion) > 25 else p.descripcion,
                    f"{p.color}/{p.talle}",
                    sugerencia['stock_actual'],
                    round(sugerencia['velocidad_venta'], 1),
                    sugerencia['dias_restantes'],
                    f"Comprar {max(0, sugerencia['cantidad_sugerida'])}"
                ))
            
            # Actualizar estado final
            lbl_ia_status.config(text="🤖 IA Operativa", fg="#00E5FF")
        
        # Asignar comando al botón
        btn_analizar.config(command=actualizar_reposicion)
        
        # Ejecutar análisis inicial
        actualizar_reposicion()
    
    def _mostrar_precios_ia(self):
        """Vista de optimización de precios - Versión Visual Optimizada y Moderna"""
        # Limpiar contenido anterior
        for widget in self.frame_contenido_ia.winfo_children():
            widget.destroy()
        
        # === TÍTULO DE SECCIÓN OPTIMIZADO ===
        titulo_precios = tk.Label(self.frame_contenido_ia, 
                                 text="💰 OPTIMIZACIÓN INTELIGENTE DE PRECIOS", 
                                 font=("Montserrat", 16, "bold"), 
                                 bg=COLOR_FONDO, 
                                 fg="#F6AD55")
        titulo_precios.place(x=600, y=10, anchor="center")
        
        # === PANEL DE MÉTRICAS EJECUTIVO COMPACTO ===
        frame_resumen = tk.Frame(self.frame_contenido_ia, bg="#1e293b", relief="raised", bd=2)
        frame_resumen.place(x=20, y=40, width=1160, height=70)
        
        # Sombra para el resumen
        shadow_resumen = tk.Frame(self.frame_contenido_ia, bg="#0f172a", relief="flat", bd=0)
        shadow_resumen.place(x=22, y=42, width=1160, height=70)
        self.frame_contenido_ia.update()
        frame_resumen.lift()
        
        # Métricas de precios
        productos = self.sistema.inventario_actual()
        total_productos = len(productos)
        productos_alto_margen = len([p for p in productos if ((p.precio_venta - p.precio_costo) / max(1, p.precio_venta)) > 0.4])
        productos_bajo_margen = len([p for p in productos if ((p.precio_venta - p.precio_costo) / max(1, p.precio_venta)) < 0.2])
        
        # Paneles de métricas compactos
        metric_panels = [
            ("📊 Total", str(total_productos), "#1d4ed8", "productos"),
            ("📈 Alto Margen", str(productos_alto_margen), "#059669", "rentables"),
            ("📉 Bajo Margen", str(productos_bajo_margen), "#dc2626", "revisar"),
            ("🤖 IA Activa", "100%", "#7c3aed", "análisis")
        ]
        
        x_positions = [30, 320, 610, 900]
        for i, (titulo, valor, color, descripcion) in enumerate(metric_panels):
            panel = tk.Frame(frame_resumen, bg=color, relief="flat", bd=0, width=180, height=50)
            panel.place(x=x_positions[i], y=10)
            
            tk.Label(panel, text=titulo, font=("Montserrat", 9, "bold"), 
                    bg=color, fg="#ffffff").place(x=90, y=5, anchor="center")
            tk.Label(panel, text=valor, font=("Montserrat", 14, "bold"), 
                    bg=color, fg="#ffffff").place(x=90, y=22, anchor="center")
            tk.Label(panel, text=descripcion, font=("Montserrat", 8), 
                    bg=color, fg="#ffffff").place(x=90, y=37, anchor="center")
        
        # === TABLA DE OPORTUNIDADES OPTIMIZADA ===
        frame_tabla = tk.Frame(self.frame_contenido_ia, bg="#1e293b", relief="raised", bd=2)
        frame_tabla.place(x=20, y=130, width=1160, height=290)
        
        # Título de la tabla
        lbl_tabla_titulo = tk.Label(frame_tabla, 
                                   text="💡 OPORTUNIDADES DE OPTIMIZACIÓN", 
                                   font=("Montserrat", 12, "bold"), 
                                   bg="#1e293b", 
                                   fg="#f1f5f9")
        lbl_tabla_titulo.pack(pady=(8,5))
        
        # Frame para la tabla
        tabla_frame = tk.Frame(frame_tabla, bg="#1e293b")
        tabla_frame.pack(fill="both", expand=True, padx=12, pady=(0,12))
        
        cols = ("📊 Estado", "Producto", "Precio Actual", "Margen %", 
                "Rotación", "💰 Precio Sugerido", "🎯 Estrategia IA")
        tree_precios = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=10)
        aplicar_estilo_moderno_treeview(tree_precios)
        
        # Anchos optimizados
        anchos = [70, 200, 100, 80, 90, 110, 250]
        for col, ancho in zip(cols, anchos):
            tree_precios.heading(col, text=col, anchor="center")
            tree_precios.column(col, width=ancho, anchor="center")
        
        tree_precios.pack(fill="both", expand=True)
        
        # Análisis de precios con lógica optimizada
        productos_analizados = productos[:20]  # Limitar para mejor rendimiento
        
        for producto in productos_analizados:
            try:
                ventas_30d = self._obtener_ventas_producto(producto, 30)
                
                # Calcular rotación más precisa
                if ventas_30d > 15:
                    rotacion = "🔥 Muy Alta"
                    rotacion_nivel = "muy_alta"
                elif ventas_30d > 8:
                    rotacion = "📈 Alta"
                    rotacion_nivel = "alta"
                elif ventas_30d > 3:
                    rotacion = "📊 Media"
                    rotacion_nivel = "media"
                elif ventas_30d > 0:
                    rotacion = "📉 Baja"
                    rotacion_nivel = "baja"
                else:
                    rotacion = "❌ Sin Ventas"
                    rotacion_nivel = "sin_ventas"
                
                # Calcular margen con validación
                if producto.precio_venta > 0 and producto.precio_costo > 0:
                    margen = ((producto.precio_venta - producto.precio_costo) / producto.precio_venta * 100)
                else:
                    margen = 0
                
                # Lógica de sugerencias IA optimizada
                if rotacion_nivel == "sin_ventas" and margen > 30:
                    icono = "🔻"
                    precio_sugerido = producto.precio_venta * 0.85  # Reducir 15%
                    estrategia = "Reducir precio - activar demanda"
                elif rotacion_nivel == "baja" and margen > 40:
                    icono = "⚡"
                    precio_sugerido = producto.precio_venta * 0.92  # Reducir 8%
                    estrategia = "Ajuste moderado"
                elif rotacion_nivel in ["alta", "muy_alta"] and margen < 25:
                    icono = "🔺"
                    precio_sugerido = producto.precio_venta * 1.12  # Aumentar 12%
                    estrategia = "Aumentar margen"
                elif rotacion_nivel == "muy_alta" and margen < 35:
                    icono = "💎"
                    precio_sugerido = producto.precio_venta * 1.08  # Aumentar 8%
                    estrategia = "Optimizar ganancia"
                elif margen < 15:
                    icono = "⚠️"
                    precio_sugerido = producto.precio_venta * 1.15  # Aumentar 15%
                    estrategia = "URGENTE: Margen bajo"
                else:
                    icono = "✅"
                    precio_sugerido = producto.precio_venta
                    estrategia = "Precio óptimo"
                
                # Determinar estado general
                if icono == "⚠️":
                    estado = "🔴 CRÍTICO"
                elif icono in ["🔻", "🔺"]:
                    estado = "🟡 OPTIMIZAR"
                elif icono == "💎":
                    estado = "🌟 ESTRELLA"
                else:
                    estado = "🟢 ÓPTIMO"
                
                # Producto truncado para mejor visualización
                producto_display = f"{producto.descripcion} {producto.color}/{producto.talle}"
                if len(producto_display) > 30:
                    producto_display = producto_display[:27] + "..."
                
                tree_precios.insert("", "end", values=(
                    estado,
                    producto_display,
                    self.formato_moneda(producto.precio_venta),
                    f"{margen:.1f}%",
                    rotacion,
                    self.formato_moneda(precio_sugerido),
                    estrategia
                ))
                
            except Exception as e:
                print(f"[DEBUG] Error en análisis de precios para {producto.descripcion}: {e} - main.py:6482")
                continue
    
    def _mostrar_analisis_ia(self):
        """Vista de análisis avanzado y tendencias - Versión Visual Optimizada y Moderna"""
        # Limpiar contenido anterior
        for widget in self.frame_contenido_ia.winfo_children():
            widget.destroy()
        
        # === TÍTULO DE SECCIÓN OPTIMIZADO ===
        titulo_analisis = tk.Label(self.frame_contenido_ia, 
                                  text="📈 ANÁLISIS AVANZADO Y TENDENCIAS IA", 
                                  font=("Montserrat", 16, "bold"), 
                                  bg=COLOR_FONDO, 
                                  fg="#9F7AEA")
        titulo_analisis.place(x=600, y=10, anchor="center")
        
        # === PANELES DE TENDENCIAS SUPERIORES OPTIMIZADOS ===
        # Panel de tendencias por marca - compacto
        frame_marcas = tk.Frame(self.frame_contenido_ia, bg="#6366f1", relief="flat", bd=0)
        frame_marcas.place(x=20, y=40, width=280, height=140)
        
        # Sombra para marcas
        shadow_marcas = tk.Frame(self.frame_contenido_ia, bg="#4f46e5", relief="flat", bd=0)
        shadow_marcas.place(x=22, y=42, width=280, height=140)
        self.frame_contenido_ia.update()
        frame_marcas.lift()
        
        lbl_marcas = tk.Label(frame_marcas, 
                             text="🏷️ TOP MARCAS", 
                             font=("Montserrat", 11, "bold"), 
                             bg="#6366f1", 
                             fg="#ffffff")
        lbl_marcas.pack(pady=(10,8))
        
        # Análisis por marca optimizado
        marcas_ventas = {}
        marcas_ingresos = {}
        for venta in self.sistema.ventas:
            for item in venta.items:
                marca = item['producto'].marca
                cantidad = item['cantidad']
                precio = item['precio']
                
                if marca not in marcas_ventas:
                    marcas_ventas[marca] = 0
                    marcas_ingresos[marca] = 0
                marcas_ventas[marca] += cantidad
                marcas_ingresos[marca] += cantidad * precio
        
        # Top 3 marcas con métricas compactas
        top_marcas = sorted(marcas_ventas.items(), key=lambda x: x[1], reverse=True)[:3]
        
        frame_marcas_content = tk.Frame(frame_marcas, bg="#6366f1")
        frame_marcas_content.pack(fill="both", expand=True, padx=12, pady=(0,12))
        
        for i, (marca, ventas) in enumerate(top_marcas, 1):
            ingresos = marcas_ingresos.get(marca, 0)
            emoji_ranking = ["🥇", "🥈", "🥉"][i-1]
            
            texto_marca = f"{emoji_ranking} {marca}"
            texto_detalle = f"{ventas} uds • {self.formato_moneda(ingresos)}"
            
            tk.Label(frame_marcas_content, 
                    text=texto_marca, 
                    font=("Montserrat", 9, "bold"), 
                    bg="#6366f1", 
                    fg="#ffffff", 
                    anchor="w").pack(fill="x", pady=1)
            tk.Label(frame_marcas_content, 
                    text=texto_detalle, 
                    font=("Montserrat", 8), 
                    bg="#6366f1", 
                    fg="#e0e7ff", 
                    anchor="w").pack(fill="x", pady=(0,6))
        
        # Panel de productos críticos - compacto
        frame_criticos = tk.Frame(self.frame_contenido_ia, bg="#dc2626", relief="flat", bd=0)
        frame_criticos.place(x=320, y=40, width=280, height=140)
        
        # Sombra para críticos
        shadow_criticos = tk.Frame(self.frame_contenido_ia, bg="#b91c1c", relief="flat", bd=0)
        shadow_criticos.place(x=322, y=42, width=280, height=140)
        self.frame_contenido_ia.update()
        frame_criticos.lift()
        
        lbl_criticos = tk.Label(frame_criticos, 
                               text="⚠️ PRODUCTOS CRÍTICOS", 
                               font=("Montserrat", 11, "bold"), 
                               bg="#dc2626", 
                               fg="#ffffff")
        lbl_criticos.pack(pady=(10,8))
        
        # Análisis de productos críticos
        productos_sin_movimiento = []
        productos_stock_bajo = []
        
        for producto in self.sistema.productos:
            ventas_60d = self._obtener_ventas_producto(producto, 60)
            if ventas_60d == 0:
                productos_sin_movimiento.append(producto)
            if producto.cantidad <= 5:
                productos_stock_bajo.append(producto)
        
        frame_criticos_content = tk.Frame(frame_criticos, bg="#dc2626")
        frame_criticos_content.pack(fill="both", expand=True, padx=12, pady=(0,12))
        
        tk.Label(frame_criticos_content, 
                text=f"🚫 {len(productos_sin_movimiento)} sin ventas (60d)", 
                font=("Montserrat", 9, "bold"), 
                bg="#dc2626", 
                fg="#ffffff", 
                anchor="w").pack(fill="x", pady=2)
        tk.Label(frame_criticos_content, 
                text=f"📉 {len(productos_stock_bajo)} stock bajo", 
                font=("Montserrat", 9, "bold"), 
                bg="#dc2626", 
                fg="#ffffff", 
                anchor="w").pack(fill="x", pady=2)
        tk.Label(frame_criticos_content, 
                text="💡 Recomendaciones:\n• Promociones especiales\n• Revisión de precios", 
                font=("Montserrat", 8), 
                bg="#dc2626", 
                fg="#fecaca", 
                anchor="w",
                justify="left").pack(fill="x", pady=(8,0))
        
        # Panel de métricas IA - compacto
        frame_metricas_ia = tk.Frame(self.frame_contenido_ia, bg="#059669", relief="flat", bd=0)
        frame_metricas_ia.place(x=620, y=40, width=280, height=140)
        
        # Sombra para métricas IA
        shadow_metricas_ia = tk.Frame(self.frame_contenido_ia, bg="#047857", relief="flat", bd=0)
        shadow_metricas_ia.place(x=622, y=42, width=280, height=140)
        self.frame_contenido_ia.update()
        frame_metricas_ia.lift()
        
        lbl_metricas_ia = tk.Label(frame_metricas_ia, 
                                  text="🤖 MÉTRICAS DE IA", 
                                  font=("Montserrat", 11, "bold"), 
                                  bg="#059669", 
                                  fg="#ffffff")
        lbl_metricas_ia.pack(pady=(10,8))
        
        # Cálculos de métricas IA
        total_productos = len(self.sistema.productos)
        productos_con_ventas = len([p for p in self.sistema.productos if self._obtener_ventas_producto(p, 30) > 0])
        efectividad_ia = (productos_con_ventas / max(1, total_productos)) * 100
        
        frame_metricas_content = tk.Frame(frame_metricas_ia, bg="#059669")
        frame_metricas_content.pack(fill="both", expand=True, padx=12, pady=(0,12))
        
        tk.Label(frame_metricas_content, 
                text=f"📊 {total_productos} productos analizados", 
                font=("Montserrat", 9, "bold"), 
                bg="#059669", 
                fg="#ffffff", 
                anchor="w").pack(fill="x", pady=2)
        tk.Label(frame_metricas_content, 
                text=f"✅ {efectividad_ia:.1f}% efectividad IA", 
                font=("Montserrat", 9, "bold"), 
                bg="#059669", 
                fg="#ffffff", 
                anchor="w").pack(fill="x", pady=2)
        tk.Label(frame_metricas_content, 
                text="🔄 Análisis en tiempo real\n🎯 Sugerencias automatizadas", 
                font=("Montserrat", 8), 
                bg="#059669", 
                fg="#d1fae5", 
                anchor="w",
                justify="left").pack(fill="x", pady=(8,0))
        
        # Panel de estadísticas globales - nuevo
        frame_estadisticas = tk.Frame(self.frame_contenido_ia, bg="#7c3aed", relief="flat", bd=0)
        frame_estadisticas.place(x=920, y=40, width=260, height=140)
        
        # Sombra para estadísticas
        shadow_estadisticas = tk.Frame(self.frame_contenido_ia, bg="#6d28d9", relief="flat", bd=0)
        shadow_estadisticas.place(x=922, y=42, width=260, height=140)
        self.frame_contenido_ia.update()
        frame_estadisticas.lift()
        
        lbl_estadisticas = tk.Label(frame_estadisticas, 
                                   text="📈 ESTADÍSTICAS", 
                                   font=("Montserrat", 11, "bold"), 
                                   bg="#7c3aed", 
                                   fg="#ffffff")
        lbl_estadisticas.pack(pady=(10,8))
        
        # Calcular estadísticas generales
        total_ventas = len(self.sistema.ventas)
        ingresos_totales = sum(sum(it['cantidad'] * it['precio'] for it in v.items) for v in self.sistema.ventas)
        
        frame_estadisticas_content = tk.Frame(frame_estadisticas, bg="#7c3aed")
        frame_estadisticas_content.pack(fill="both", expand=True, padx=12, pady=(0,12))
        
        tk.Label(frame_estadisticas_content, 
                text=f"📊 {total_ventas} ventas totales", 
                font=("Montserrat", 11, "bold"), 
                bg="#7c3aed", 
                fg="#ffffff", 
                anchor="w").pack(fill="x", pady=2)
        tk.Label(frame_estadisticas_content, 
                text=f"💰 {self.formato_moneda(ingresos_totales)}", 
                font=("Montserrat", 11, "bold"), 
                bg="#7c3aed", 
                fg="#ffffff", 
                anchor="w").pack(fill="x", pady=2)
        tk.Label(frame_estadisticas_content, 
                text="🚀 Sistema optimizado\n🎯 Rendimiento máximo", 
                font=("Montserrat", 10, "bold"), 
                bg="#7c3aed", 
                fg="#e9d5ff", 
                anchor="w",
                justify="left").pack(fill="x", pady=(8,0))
        
        # === TABLA DE ANÁLISIS DETALLADO ===
        frame_tabla_analisis = tk.Frame(self.frame_contenido_ia, bg="#1e293b", relief="raised", bd=2)
        frame_tabla_analisis.place(x=20, y=200, width=1160, height=300)
        
        lbl_tabla_analisis = tk.Label(frame_tabla_analisis, 
                                     text="🔍 ANÁLISIS DETALLADO POR PRODUCTO", 
                                     font=("Montserrat", 12, "bold"), 
                                     bg="#1e293b", 
                                     fg="#f1f5f9")
        lbl_tabla_analisis.pack(pady=(8,5))
        
        # Frame para la tabla de análisis
        tabla_analisis_frame = tk.Frame(frame_tabla_analisis, bg="#1e293b")
        tabla_analisis_frame.pack(fill="both", expand=True, padx=12, pady=(0,12))
        
        cols_analisis = ("Producto", "Marca", "Stock", "Ventas 30d", "Tendencia", "Estado", "Acción Recomendada")
        tree_analisis = ttk.Treeview(tabla_analisis_frame, columns=cols_analisis, show="headings", height=12)
        aplicar_estilo_moderno_treeview(tree_analisis)
        
        # Anchos optimizados para análisis
        anchos_analisis = [180, 100, 70, 90, 100, 100, 200]
        for col, ancho in zip(cols_analisis, anchos_analisis):
            tree_analisis.heading(col, text=col, anchor="center")
            tree_analisis.column(col, width=ancho, anchor="center")
        
        tree_analisis.pack(fill="both", expand=True)
        
        # Llenar datos de análisis detallado
        productos_analizar = self.sistema.productos[:15]  # Limitar para mejor rendimiento
        
        for producto in productos_analizar:
            try:
                ventas_30d = self._obtener_ventas_producto(producto, 30)
                ventas_15d = self._obtener_ventas_producto(producto, 15)
                
                # Determinar tendencia
                if ventas_15d > ventas_30d / 2:
                    tendencia = "📈 Alcista"
                elif ventas_15d < ventas_30d / 3:
                    tendencia = "📉 Bajista"
                else:
                    tendencia = "📊 Estable"
                
                # Determinar estado del producto
                if producto.cantidad <= 3:
                    estado = "🔴 Crítico"
                    accion = "Reposición urgente"
                elif ventas_30d > 20:
                    estado = "🌟 Estrella"
                    accion = "Mantener stock alto"
                elif ventas_30d == 0:
                    estado = "⚠️ Sin ventas"
                    accion = "Revisar precio/promoción"
                elif producto.cantidad > 50:
                    estado = "📦 Exceso"
                    accion = "Promocionar o reducir precio"
                else:
                    estado = "✅ Normal"
                    accion = "Continuar monitoreo"
                
                # Truncar nombre del producto si es muy largo
                producto_display = producto.descripcion
                if len(producto_display) > 25:
                    producto_display = producto_display[:22] + "..."
                
                tree_analisis.insert("", "end", values=(
                    producto_display,
                    producto.marca,
                    producto.cantidad,
                    ventas_30d,
                    tendencia,
                    estado,
                    accion
                ))
                
            except Exception as e:
                print(f"[DEBUG] Error en análisis detallado para {producto.descripcion}: {e} - main.py:6774")
                continue
    
    def _actualizar_centro_ia(self):
        """Actualiza los datos del centro IA"""
        self._cambiar_vista_ia(self.vista_ia_activa.get())
        from tkinter import messagebox
        messagebox.showinfo("IA Actualizada", "Todos los análisis han sido actualizados con los datos más recientes.")
    
    def _exportar_centro_ia(self):
        """Exporta un reporte completo de todas las funciones IA"""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                initialfile=f"Centro_IA_Completo_{datetime.date.today().strftime('%Y-%m-%d')}.csv"
            )
            
            if filename:
                import csv
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Encabezado
                    writer.writerow(['CENTRO DE INTELIGENCIA ARTIFICIAL - REPORTE COMPLETO'])
                    writer.writerow(['Fecha:', datetime.date.today().strftime('%Y-%m-%d')])
                    writer.writerow([''])
                    
                    # Sección de reposición
                    writer.writerow(['=== ANÁLISIS DE REPOSICIÓN ==='])
                    sugerencias = self._calcular_sugerencias_ia(30, 0.2)
                    writer.writerow(['Producto', 'Stock Actual', 'Velocidad Venta', 'Días Restantes', 'Cantidad Sugerida'])
                    for s in sugerencias:
                        p = s['producto']
                        writer.writerow([
                            f"{p.descripcion} {p.color}/{p.talle}",
                            s['stock_actual'],
                            f"{s['velocidad_venta']:.1f}",
                            s['dias_restantes'],
                            s['cantidad_sugerida']
                        ])
                    
                    writer.writerow([''])
                    writer.writerow(['=== ANÁLISIS DE PRECIOS ==='])
                    writer.writerow(['Producto', 'Precio Actual', 'Margen %', 'Rotación', 'Recomendación'])
                    
                    # Exportar más datos...
                    
                from tkinter import messagebox
                messagebox.showinfo("Exportación Exitosa", f"Reporte completo exportado a:\n{filename}")
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Error al exportar: {e}")
    
    def _obtener_productos_criticos(self):
        """Obtiene productos con stock crítico"""
        criticos = []
        for producto in self.sistema.productos:
            ventas_30d = self._obtener_ventas_producto(producto, 30)
            velocidad = ventas_30d / 30
            dias_restantes = producto.cantidad / velocidad if velocidad > 0 else 999
            if dias_restantes <= 7 or producto.cantidad <= 5:
                criticos.append(producto)
        return criticos
    
    def _obtener_productos_estrella(self):
        """Obtiene productos con mejor performance"""
        estrellas = []
        for producto in self.sistema.productos:
            ventas_30d = self._obtener_ventas_producto(producto, 30)
            if ventas_30d >= 10:  # Criterio para producto estrella
                estrellas.append(producto)
        return estrellas
    
    def _calcular_sugerencias_ia(self, dias_analisis, umbral_stock):
        """Algoritmo de IA para calcular sugerencias de reposición"""
        sugerencias = []
        productos = self.sistema.inventario_actual()
        
        for producto in productos:
            try:
                # Calcular ventas en el período
                ventas_periodo = self._obtener_ventas_producto(producto, dias_analisis)
                
                # Calcular velocidad de venta promedio
                velocidad_venta = ventas_periodo / dias_analisis if dias_analisis > 0 else 0
                
                # Calcular días restantes con stock actual
                dias_restantes = producto.cantidad / velocidad_venta if velocidad_venta > 0 else 999
                
                # Determinar si necesita reposición
                stock_minimo = max(5, int(velocidad_venta * 14))  # Stock para 2 semanas
                necesita_reposicion = (producto.cantidad <= stock_minimo or 
                                     dias_restantes <= 14 or 
                                     producto.cantidad / max(1, ventas_periodo) <= umbral_stock)
                
                if necesita_reposicion:
                    # Calcular cantidad sugerida (stock para 30 días)
                    cantidad_sugerida = max(10, int(velocidad_venta * 30) - producto.cantidad)
                    
                    sugerencias.append({
                        'producto': producto,
                        'stock_actual': producto.cantidad,
                        'ventas_periodo': ventas_periodo,
                        'velocidad_venta': velocidad_venta,
                        'dias_restantes': max(0, int(dias_restantes)),
                        'cantidad_sugerida': cantidad_sugerida,
                        'prioridad': self._calcular_prioridad(dias_restantes, velocidad_venta)
                    })
            
            except Exception as e:
                print(f"[DEBUG] Error calculando sugerencia para {producto.descripcion}: {e} - main.py:6886")
                continue
        
        # Ordenar por prioridad (críticos primero)
        sugerencias.sort(key=lambda x: x['prioridad'], reverse=True)
        
        return sugerencias
    
    def _obtener_ventas_producto(self, producto, dias):
        """Obtiene las ventas de un producto en los últimos N días"""
        try:
            fecha_limite = datetime.date.today() - datetime.timedelta(days=dias)
            ventas_total = 0
            
            for venta in self.sistema.ventas:
                if venta.fecha >= fecha_limite:
                    for item in venta.items:
                        if (item['producto'].descripcion == producto.descripcion and 
                            item['producto'].color == producto.color and 
                            item['producto'].talle == producto.talle):
                            ventas_total += item['cantidad']
            
            return ventas_total
        except Exception:
            return 0
    
    def _calcular_prioridad(self, dias_restantes, velocidad_venta):
        """Calcula la prioridad de reposición (mayor número = más urgente)"""
        if dias_restantes <= 0:
            return 100  # Crítico - sin stock
        elif dias_restantes <= 3:
            return 80   # Muy urgente
        elif dias_restantes <= 7:
            return 60   # Urgente
        elif dias_restantes <= 14:
            return 40   # Atención
        else:
            return 20   # Normal

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
        self.pantalla_widgets.append(bar)

    def _chip_volver(self, on_volver, x=50, y=20):
        """Crea el botón volver con alta visibilidad en esquina superior derecha"""
        btn = tk.Button(self.canvas_bg, text="←VOLVER", font=("Montserrat", 13, "bold"),
                        bg="#b506e0", fg="#ffffff", bd=3, relief="raised",
                        cursor="hand2", command=on_volver, pady=8, padx=12)
        aplicar_estilo_moderno_boton(btn, "danger", hover_efecto=True)
        
        # Crear el botón en esquina superior derecha, siempre visible
        btn_canvas_id = self.canvas_bg.create_window(x, y, window=btn, width=120, height=40, anchor="nw")
        
        # Asegurar que el botón esté completamente al frente
        self.canvas_bg.tag_raise(btn_canvas_id)
        self.canvas_bg.tag_raise(btn_canvas_id)  # Doble raise para asegurar
        
        # Registrar tanto el botón como su ID en el canvas
        self.pantalla_widgets.extend([btn, btn_canvas_id])
        
        print(f"[DEBUG] Botón VOLVER creado en esquina superior derecha ({x}, {y}) - main.py:6956")

    def require_role(self, allowed_roles):
        """Devuelve True si la sesión tiene un rol permitido, si no, muestra mensaje y retorna False."""
        try:
            if self.session is None or not hasattr(self.session, 'role'):
                messagebox.showerror("Permisos", "No hay sesión activa.")
                return False
            if self.session.role not in allowed_roles:
                messagebox.showwarning("Acceso restringido", "No tiene permisos para esta acción.")
                return False
            return True
        except Exception:
            return False

    def _chip_logout(self, x=1120, y=20):
        if not self.session or not self.session.is_logged_in():
            return
        btn = tk.Button(self.canvas_bg, text=f"Salir ({self.session.username})", font=("Montserrat", 11, "bold"),
                        bg=COLOR_BOTON_DANGER, fg="#ffffff", bd=2, relief="raised",
                        cursor="hand2", pady=6, padx=12, command=self._perform_logout)
        aplicar_estilo_moderno_boton(btn, "danger", hover_efecto=True)
        btn_id = self.canvas_bg.create_window(1020, y, window=btn, width=220, height=36, anchor="nw")
        self.pantalla_widgets.extend([btn, btn_id])

    def _perform_logout(self):
        try:
            if self.session:
                self.session.logout()
        except Exception:
            pass
        self.destroy()

    def mostrar_gestion_usuarios(self):
        if not self.require_role(["admin"]):
            return
        from auth import AuthManager
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        self._chip_volver(self.mostrar_menu_secundario)
        self._chip_logout()

        auth = AuthManager()

        header = tk.Frame(self.canvas_bg, bg="#111827")
        self.canvas_bg.create_window(640, 60, window=header, width=600, height=130, anchor="center")
        lbl = tk.Label(header, text="👥 GESTIÓN DE USUARIOS", font=("Montserrat", 18, "bold"), bg="#111827", fg=COLOR_CIAN)
        lbl.pack(pady=18)

        actions = tk.Frame(self.canvas_bg, bg="#0f1629", bd=2, relief="raised")
        self.canvas_bg.create_window(320, 220, window=actions, width=580, height=260, anchor="center")

        tk.Label(actions, text="Usuario", font=("Montserrat", 11, "bold"), bg="#0f1629", fg=COLOR_TEXTO).place(x=20, y=20)
        ent_user = tk.Entry(actions)
        aplicar_estilo_moderno_entry(ent_user)
        ent_user.place(x=120, y=20, width=200, height=28)

        tk.Label(actions, text="Contraseña", font=("Montserrat", 11, "bold"), bg="#0f1629", fg=COLOR_TEXTO).place(x=20, y=60)
        ent_pass = tk.Entry(actions, show="*")
        aplicar_estilo_moderno_entry(ent_pass)
        ent_pass.place(x=120, y=60, width=200, height=28)

        tk.Label(actions, text="Rol", font=("Montserrat", 11, "bold"), bg="#0f1629", fg=COLOR_TEXTO).place(x=20, y=100)
        combo_rol = ttk.Combobox(actions, values=["vendedor", "admin"], state="readonly")
        aplicar_estilo_moderno_combobox(combo_rol)
        combo_rol.place(x=120, y=100, width=200, height=28)
        combo_rol.set("vendedor")

        btn_crear = tk.Button(actions, text="➕ Crear Usuario", font=("Montserrat", 13, "bold"), cursor="hand2")
        aplicar_estilo_moderno_boton(btn_crear, "success", True)
        btn_crear.place(x=350, y=20, width=200, height=44)

        tk.Label(actions, text="Usuario", font=("Montserrat", 11, "bold"), bg="#0f1629", fg=COLOR_TEXTO).place(x=20, y=160)
        ent_user_cp = tk.Entry(actions)
        aplicar_estilo_moderno_entry(ent_user_cp)
        ent_user_cp.place(x=120, y=160, width=200, height=28)

        tk.Label(actions, text="Nueva Pass", font=("Montserrat", 11, "bold"), bg="#0f1629", fg=COLOR_TEXTO).place(x=20, y=200)
        ent_newpass = tk.Entry(actions, show="*")
        aplicar_estilo_moderno_entry(ent_newpass)
        ent_newpass.place(x=120, y=200, width=200, height=28)

        btn_setpass = tk.Button(actions, text="🔐 Cambiar Contraseña", font=("Montserrat", 13, "bold"), cursor="hand2")
        aplicar_estilo_moderno_boton(btn_setpass, "warning", True)
        btn_setpass.place(x=350, y=160, width=200, height=44)

        table_frame = tk.Frame(self.canvas_bg, bg="#1a3d75", bd=2, relief="raised")
        self.canvas_bg.create_window(930, 260, window=table_frame, width=620, height=340, anchor="center")
        cols = ("usuario", "rol", "activo", "último login")
        tree_users = ttk.Treeview(table_frame, columns=cols, show="headings", height=16)
        aplicar_estilo_moderno_treeview(tree_users)
        for col in cols:
            tree_users.heading(col, text=col.capitalize())
            tree_users.column(col, anchor="center", width=140)
        tree_users.pack(fill="both", expand=True)

        btns = tk.Frame(self.canvas_bg, bg="#1a3d75")
        self.canvas_bg.create_window(930, 460, window=btns, width=620, height=60, anchor="center")

        btn_toggle = tk.Button(btns, text="✅ Activar / ❌ Desactivar", cursor="hand2")
        aplicar_estilo_moderno_boton(btn_toggle, "secundario", True)
        btn_toggle.place(x=20, y=12, width=220, height=36)

        btn_role = tk.Button(btns, text="♻ Cambiar Rol", cursor="hand2")
        aplicar_estilo_moderno_boton(btn_role, "primario", True)
        btn_role.place(x=260, y=12, width=160, height=36)

        def refrescar_tabla():
            for it in tree_users.get_children():
                tree_users.delete(it)
            try:
                users = auth.list_users()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar usuarios: {e}")
                users = []
            for u in users:
                tree_users.insert("", "end", values=(
                    u.get("username"), u.get("role"), "Sí" if u.get("is_active") else "No", u.get("last_login") or "—"
                ))

        def crear_usuario():
            try:
                username = ent_user.get().strip()
                password = ent_pass.get()
                role = combo_rol.get()
                if not username or not password:
                    messagebox.showwarning("Validación", "Usuario y contraseña son obligatorios.")
                    return
                auth.register_user(username, password, role)
                messagebox.showinfo("Éxito", "Usuario creado.")
                ent_user.delete(0, tk.END)
                ent_pass.delete(0, tk.END)
                combo_rol.set("vendedor")
                refrescar_tabla()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        def set_password():
            try:
                username = ent_user_cp.get().strip()
                newpass = ent_newpass.get()
                if not username or not newpass:
                    messagebox.showwarning("Validación", "Ingrese usuario y nueva contraseña.")
                    return
                auth.set_password(username, newpass)
                messagebox.showinfo("Éxito", "Contraseña actualizada.")
                ent_user_cp.delete(0, tk.END)
                ent_newpass.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        def toggle_user():
            sel = tree_users.selection()
            if not sel:
                messagebox.showwarning("Seleccione", "Seleccione un usuario de la tabla.")
                return
            username = tree_users.item(sel[0])['values'][0]
            target_active = None
            for u in auth.users:
                if u.get("username") == username:
                    target_active = not u.get("is_active", True)
                    break
            try:
                if target_active:
                    auth.activate_user(username)
                else:
                    auth.deactivate_user(username)
                refrescar_tabla()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        def cambiar_rol():
            sel = tree_users.selection()
            if not sel:
                messagebox.showwarning("Seleccione", "Seleccione un usuario de la tabla.")
                return
            username = tree_users.item(sel[0])['values'][0]
            current_role = None
            for u in auth.users:
                if u.get("username") == username:
                    current_role = u.get("role", "vendedor")
                    break
            nuevo = "admin" if current_role == "vendedor" else "vendedor"
            try:
                auth.set_role(username, nuevo)
                refrescar_tabla()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        btn_crear.config(command=crear_usuario)
        btn_setpass.config(command=set_password)
        btn_toggle.config(command=toggle_user)
        btn_role.config(command=cambiar_rol)

        refrescar_tabla()


def habilitar_ordenamiento_treeview(tree: ttk.Treeview):
    def try_float(value: str):
        try:
            # Normaliza formato moneda $12.345,67 -> 12345.67
            cleaned = value.replace("$", "").replace(".", "").replace(",", ".").strip()
            return float(cleaned)
        except Exception:
            try:
                return float(value)
            except Exception:
                return value.lower() if isinstance(value, str) else value

    def sort_by(col: str, reverse: bool = False):
        data = [(tree.set(item_id, col), item_id) for item_id in tree.get_children("")]
        data.sort(key=lambda t: try_float(t[0]), reverse=reverse)
        for index, (_, item_id) in enumerate(data):
            tree.move(item_id, "", index)
        tree.heading(col, command=lambda: sort_by(col, not reverse))

    for col in tree["columns"]:
        tree.heading(col, command=lambda c=col: sort_by(c, False))

if __name__ == "__main__":
    # ---------------- Pantallas de Onboarding/Login (Fase 1) ----------------
    def _interpolar_hex(color1: str, color2: str, t: float) -> str:
        c1 = tuple(int(color1[i:i+2], 16) for i in (1, 3, 5))
        c2 = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))
        c = tuple(int(c1[j] + (c2[j] - c1[j]) * t) for j in range(3))
        return f'#{c[0]:02x}{c[1]:02x}{c[2]:02x}'

    def run_onboarding_ui(auth_manager: "AuthManager"):
        """Pantalla de registro por primera vez - Optimizada 640x480"""
        root = tk.Tk()
        root.title("KONTROL+ - Registro Inicial")
        root.geometry("640x480")
        root.resizable(False, False)
        root.configure(bg=COLOR_FONDO)
        
        # Centrar ventana
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (640 // 2)
        y = (root.winfo_screenheight() // 2) - (480 // 2)
        root.geometry(f"640x480+{x}+{y}")
        
        # Fondo con gradiente
        canvas_bg = tk.Canvas(root, width=640, height=480, highlightthickness=0, bd=0, bg=COLOR_FONDO)
        canvas_bg.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Crear gradiente de fondo
        for i in range(0, 480, 2):
            color = _interpolar_hex(COLOR_GRADIENTE_1, COLOR_GRADIENTE_2, i/480)
            canvas_bg.create_rectangle(0, i, 640, i+2, outline="", fill=color, tags="fondo")
        
        # Logo en la parte superior
        try:
            from PIL import Image, ImageTk
            import os, sys
            logo_path = os.path.join(sys._MEIPASS, "LOGO_APP.png") if hasattr(sys, '_MEIPASS') else "screenshot/LOGO_APP.png"
            if os.path.exists(logo_path):
                logo_img = Image.open(logo_path).convert("RGBA")
                # Redimensionar para 640x480
                logo_width = int(640 * 0.4)  # 40% del ancho
                logo_height = int(logo_img.height * (logo_width / logo_img.width))
                if logo_height > 120:  # Altura máxima
                    logo_height = 120
                    logo_width = int(logo_img.width * (logo_height / logo_img.height))
                
                logo_img = logo_img.resize((logo_width, logo_height), Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS)
                logo_tk = ImageTk.PhotoImage(logo_img)
                logo_id = canvas_bg.create_image(320, 40, image=logo_tk, anchor="n")
                canvas_bg.tag_raise(logo_id)
        except Exception as e:
            canvas_bg.create_text(320, 40, text="ALEN.IA", font=("Orbitron", 24, "bold"), 
                                fill=COLOR_CIAN, anchor="n")
        
        # Frame principal centrado
        main_frame = tk.Frame(root, bg=COLOR_FONDO)
        main_frame.place(relx=0.5, rely=0.65, anchor="center")
        
        resultado = {"username": None, "password": None, "confirm": None}
        
        # Usuario
        tk.Label(main_frame, text="👤 Usuario:", font=("Montserrat", 12, "bold"), 
                bg=COLOR_FONDO, fg=COLOR_CIAN).grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        ent_user = tk.Entry(main_frame, font=("Montserrat", 12), width=25)
        aplicar_estilo_moderno_entry(ent_user)
        ent_user.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        # Contraseña
        tk.Label(main_frame, text="🔒 Contraseña:", font=("Montserrat", 12, "bold"), 
                bg=COLOR_FONDO, fg=COLOR_CIAN).grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        ent_pass = tk.Entry(main_frame, font=("Montserrat", 12), show="*", width=25)
        aplicar_estilo_moderno_entry(ent_pass)
        ent_pass.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        # Confirmar contraseña
        tk.Label(main_frame, text="🔐 Confirmar:", font=("Montserrat", 12, "bold"), 
                bg=COLOR_FONDO, fg=COLOR_CIAN).grid(row=4, column=0, sticky="w", pady=(0, 5))
        
        ent_confirm = tk.Entry(main_frame, font=("Montserrat", 12), show="*", width=25)
        aplicar_estilo_moderno_entry(ent_confirm)
        ent_confirm.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        # Estado
        estado = tk.Label(main_frame, text="", font=("Montserrat", 10), 
                         bg=COLOR_FONDO, fg="#f59e0b")
        estado.grid(row=6, column=0, columnspan=2, pady=(0, 10))
        
        def validar_registro():
            username = ent_user.get().strip()
            password = ent_pass.get()
            confirm = ent_confirm.get()
            
            if not username or not password or not confirm:
                estado.config(text="Todos los campos son obligatorios.", fg="#ef4444")
                return
            
            if len(username) < 3:
                estado.config(text="El usuario debe tener al menos 3 caracteres.", fg="#ef4444")
                return
            
            if len(password) < 6:
                estado.config(text="La contraseña debe tener al menos 6 caracteres.", fg="#ef4444")
                return
            
            if password != confirm:
                estado.config(text="Las contraseñas no coinciden.", fg="#ef4444")
                return
            
            # Intentar crear usuario
            try:
                auth_manager.register_admin(username, password)
                estado.config(text="✅ Usuario creado exitosamente!", fg="#10b981")
                resultado["username"] = username
                root.after(1500, root.destroy)
            except Exception as e:
                estado.config(text=f"Error: {str(e)}", fg="#ef4444")
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg=COLOR_FONDO)
        btn_frame.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        btn_crear = tk.Button(btn_frame, text="🚀 CREAR CUENTA", cursor="hand2", width=20)
        aplicar_estilo_moderno_boton(btn_crear, "primario", True)
        btn_crear.pack(side="left", padx=(0, 10))
        btn_crear.config(command=validar_registro)
        
        btn_cancel = tk.Button(btn_frame, text="❌ SALIR", cursor="hand2", width=15)
        aplicar_estilo_moderno_boton(btn_cancel, "danger", True)
        btn_cancel.pack(side="right")
        btn_cancel.config(command=root.destroy)
        
        # Eventos
        ent_user.bind("<Return>", lambda e: ent_pass.focus())
        ent_pass.bind("<Return>", lambda e: ent_confirm.focus())
        ent_confirm.bind("<Return>", lambda e: validar_registro())
        ent_user.focus_set()
        
        # Configurar ventana principal
        root.focus_set()
        
        root.mainloop()
        return resultado["username"]

    def run_login_ui(auth_manager: "AuthManager"):
        """Pantalla de inicio de sesión - Optimizada 640x480"""
        root = tk.Tk()
        root.title("KONTROL+ - Inicio de Sesión")
        root.geometry("640x480")
        root.resizable(False, False)
        root.configure(bg=COLOR_FONDO)
        
        # Centrar ventana
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (640 // 2)
        y = (root.winfo_screenheight() // 2) - (480 // 2)
        root.geometry(f"640x480+{x}+{y}")
        
        # Fondo con gradiente
        canvas_bg = tk.Canvas(root, width=640, height=480, highlightthickness=0, bd=0, bg=COLOR_FONDO)
        canvas_bg.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Crear gradiente de fondo
        for i in range(0, 480, 2):
            color = _interpolar_hex(COLOR_GRADIENTE_1, COLOR_GRADIENTE_2, i/480)
            canvas_bg.create_rectangle(0, i, 640, i+2, outline="", fill=color, tags="fondo")
        
        # Logo en la parte superior
        try:
            from PIL import Image, ImageTk
            import os, sys
            logo_path = os.path.join(sys._MEIPASS, "LOGO_APP.png") if hasattr(sys, '_MEIPASS') else "screenshot/LOGO_APP.png"
            if os.path.exists(logo_path):
                logo_img = Image.open(logo_path).convert("RGBA")
                # Redimensionar para 640x480
                logo_width = int(640 * 0.4)  # 40% del ancho
                logo_height = int(logo_img.height * (logo_width / logo_img.width))
                if logo_height > 140:  # Altura máxima
                    logo_height = 140
                    logo_width = int(logo_img.width * (logo_height / logo_img.height))
                
                logo_img = logo_img.resize((logo_width, logo_height), Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS)
                logo_tk = ImageTk.PhotoImage(logo_img)
                logo_id = canvas_bg.create_image(320, 40, image=logo_tk, anchor="n")
                canvas_bg.tag_raise(logo_id)
        except Exception as e:
            canvas_bg.create_text(320, 40, text="ALEN.IA", font=("Orbitron", 24, "bold"), 
                                fill=COLOR_CIAN, anchor="n")
        
        # Frame principal centrado
        main_frame = tk.Frame(root, bg=COLOR_FONDO)
        main_frame.place(relx=0.5, rely=0.65, anchor="center")
        
        resultado = {"username": None}
        
        # Usuario
        tk.Label(main_frame, text="👤 Usuario:", font=("Montserrat", 12, "bold"), 
                bg=COLOR_FONDO, fg=COLOR_CIAN).grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        ent_user = tk.Entry(main_frame, font=("Montserrat", 16), width=25)
        aplicar_estilo_moderno_entry(ent_user)
        ent_user.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 15))
        
        # Contraseña
        tk.Label(main_frame, text="🔒 Contraseña:", font=("Montserrat", 12, "bold"), 
                bg=COLOR_FONDO, fg=COLOR_CIAN).grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        frame_pass = tk.Frame(main_frame, bg=COLOR_FONDO)
        frame_pass.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(0, 15))
        
        ent_pass = tk.Entry(frame_pass, font=("Montserrat", 16), show="*", width=24)
        aplicar_estilo_moderno_entry(ent_pass)
        ent_pass.pack(side="left", fill="x", expand=True)
        
        def toggle_show():
            ent_pass.config(show="" if ent_pass.cget("show") == "*" else "*")
        
        btn_toggle = tk.Button(frame_pass, text="👁️VER", cursor="hand2", width=4)
        aplicar_estilo_moderno_boton(btn_toggle, "secundario", True)
        btn_toggle.pack(side="right", padx=(5, 0))
        btn_toggle.config(command=toggle_show)
        
        # Estado
        estado = tk.Label(main_frame, text="", font=("Montserrat", 10), 
                         bg=COLOR_FONDO, fg="#f59e0b")
        estado.grid(row=4, column=0, columnspan=3, pady=(0, 15))
        
        def intentar_login(event=None):
            username = ent_user.get().strip()
            password = ent_pass.get()
            
            if not username or not password:
                estado.config(text="Ingrese usuario y contraseña.", fg="#ef4444")
                return
            
            can, wait = auth_manager.can_attempt(username)
            if not can:
                estado.config(text=f"Demasiados intentos. Espere {wait}s…", fg="#f59e0b")
                return
            
            user = auth_manager.authenticate(username, password)
            if user:
                estado.config(text="✅ Acceso concedido", fg="#10b981")
                resultado["username"] = user["username"]
                root.after(1000, root.destroy)
            else:
                auth_manager.register_failure(username)
                can2, wait2 = auth_manager.can_attempt(username)
                if not can2:
                    estado.config(text=f"Incorrecto. Espere {wait2}s para reintentar.", fg="#f59e0b")
                    btn_login.config(state="disabled")
                    root.after(wait2 * 1000, lambda: (btn_login.config(state="normal"), estado.config(text="")))
                else:
                    estado.config(text="Usuario o contraseña incorrectos.", fg="#ef4444")
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg=COLOR_FONDO)
        btn_frame.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(10, 0))
        
        btn_login = tk.Button(btn_frame, text="🚀 ENTRAR", cursor="hand2", width=20)
        aplicar_estilo_moderno_boton(btn_login, "primario", True)
        btn_login.pack(side="left", padx=(0, 10))
        btn_login.config(command=intentar_login)
        
        btn_cancel = tk.Button(btn_frame, text="❌ SALIR", cursor="hand2", width=15)
        aplicar_estilo_moderno_boton(btn_cancel, "danger", True)
        btn_cancel.pack(side="right")
        btn_cancel.config(command=root.destroy)
        
        # Eventos
        ent_user.bind("<Return>", intentar_login)
        ent_pass.bind("<Return>", intentar_login)
        ent_user.focus_set()
        
        # Configurar ventana principal
        root.focus_set()
        
        root.mainloop()
        return resultado["username"]

    print("[DEBUG] Iniciando flujo de autenticación - main.py:7455")
    auth = AuthManager()
    session = SessionManager()

    while True:
        logged_username = None
        if auth.is_first_run():
            created = run_onboarding_ui(auth)
            if not created:
                print("[INFO] Onboarding cancelado. Saliendo… - main.py:7464")
                break
            logged_username = created
        else:
            logged = run_login_ui(auth)
            if not logged:
                print("[INFO] Login cancelado. Saliendo… - main.py:7470")
                break
            logged_username = logged

        print("[DEBUG] Usuario autenticado: - main.py:7474", logged_username)
        user_rec = {"username": logged_username, "role": "admin" if auth.is_first_run() else None}
        # Recuperar el rol del archivo
        try:
            from auth import AuthManager as _AM
            _tmp_am = _AM()
            for u in _tmp_am.users:
                if u.get("username","" ).lower() == logged_username.lower():
                    user_rec["role"] = u.get("role", "vendedor")
                    break
        except Exception:
            user_rec["role"] = "vendedor"

        session.login(user_rec)
        print("[DEBUG] Creando instancia de SistemaGestion...  postauth - main.py:7488")
        sistema = SistemaGestion()
        print("[DEBUG] SistemaGestion creado. Creando AppPilchero...  postauth - main.py:7490")
        app = AppPilchero(sistema, session=session)
        print("[DEBUG] AppPilchero creado. Ejecutando mainloop...  postauth - main.py:7492")
        app.mainloop()
        print("[DEBUG] mainloop finalizado  postauth - main.py:7494")

        if session.is_logged_in():
            # Si sigue logueado después de cerrar la ventana, salir
            break
        else:
            # Si hizo logout (session.logout() llamado), reiniciar ciclo (volverá a login)
            continue

