## Manual técnico para desarrolladores — `main.py`

- Nombre del producto: Alen.iA - Gestión Inteligente de Stock y Ventas
- Tecnología principal: Python 3.x con GUI en Tkinter/ttk
- Persistencia: Archivos JSON locales
- Enfoque: App de escritorio con paneles de gestión, ventas, reportes, ofertas y “Centro IA” con heurísticas de reposición y precios

### Índice
- Requisitos y dependencias
- Arquitectura y capas
- Estilos, paleta y utilidades de UI
- Modelo de dominio y persistencia
- Aplicación principal y navegación
- Pantallas funcionales (ventas, cierre, carga masiva, reportes, alta/actualización, inventario, ofertas)
- Centro IA (dashboard, reposición, precios, análisis)
- Flujo de datos y formatos
- Ejecución local y empaquetado
- Puntos de extensión y buenas prácticas
- Limitaciones conocidas
- Extractos y referencias de código


## Requisitos y dependencias

- Python 3.8+ recomendado
- Bibliotecas estándar: `datetime`, `json`, `csv`, `os`, `sys`, `tkinter`, `tkinter.ttk`, `tkinter.filedialog`, `tkinter.messagebox`, `tkinter.font`
- Biblioteca externa: `Pillow` (PIL) para manejo de imágenes (logos/íconos)
- Plataforma: Windows (Tkinter nativo). Maneja `sys._MEIPASS` para recursos cuando se empaqueta (PyInstaller)

Recursos esperados en el mismo directorio de ejecución:
- Imágenes: `screenshot/LOGO_APP.png` (principal), `7.png` (secundarias), `screenshot/ALENRESULTADOS.png` (logo chico/panel IA)
- Datos: `productos.json`, `ventas.json` (creados/actualizados en runtime)
- Histórico: `ventas_historico_YYYY.json` (generado en cierre de caja)


## Arquitectura y capas

- Utilidades de UI: estilos, tooltips, animaciones, carga de íconos
- Dominio: `Producto`, `Venta`, `SistemaGestion` (memoria + persistencia JSON)
- Presentación: `AppPilchero` como raíz Tk (`Tk`), pantallas en un `Canvas` con “ventanas” para layout y navegación por métodos
- IA (heurísticas): métodos privados en `AppPilchero` para reposición, precios y análisis


## Estilos, paleta y utilidades de UI

- Paleta de colores y constantes globales:
```12:20:main.py
# Paleta moderna (modo oscuro)
COLOR_GRADIENTE_1 = "#0f172a"
COLOR_GRADIENTE_2 = "#111827"
COLOR_CIAN = "#e5e7eb"        # Texto principal claro
COLOR_AZUL = "#0f172a"
COLOR_FONDO = COLOR_AZUL
COLOR_BOTON = "#4f46e5"       # Indigo
COLOR_BOTON_SECUNDARIO = "#6b7280"
COLOR_TOTAL_IVA_BG = "#1f2937"   # Panels grises
```

- Colores para tipos de botón:
```29:35:main.py
COLOR_BOTON_MODERNO = "#4f46e5"         # primario
COLOR_BOTON_HOVER_MODERNO = "#4338ca"
COLOR_BOTON_SUCCESS = "#03985a"         # verde moderno
COLOR_BOTON_WARNING = "#f59e0b"         # naranja moderno
COLOR_BOTON_DANGER = "#ef4444"          # rojo moderno
COLOR_BOTON_SECONDARY = "#6b7280"       # gris moderno
```

- Estilos reutilizables:
  - `aplicar_estilo_moderno_boton(boton, tipo, hover_efecto)`
  - `aplicar_estilo_moderno_entry(entry)`
  - `aplicar_estilo_moderno_label(label, tipo)`
  - `aplicar_estilo_moderno_combobox(combo)`
  - `aplicar_estilo_moderno_treeview(tree)`
  - `habilitar_ordenamiento_treeview(tree)` (click en encabezados para ordenar)

Extractos:
```41:98:main.py
def aplicar_estilo_moderno_boton(boton, tipo="primario", hover_efecto=True):
    """
    Aplica estilo moderno a un botón con bordes redondeados y efectos
    """
    # ... existing code ...
```

```173:199:main.py
def aplicar_estilo_moderno_treeview(tree):
    try:
        style = ttk.Style()
        style.theme_use('clam')
        # ... existing code ...
```

```200:259:main.py
class Tooltip:
    """Clase para crear tooltips informativos modernos"""
    def __init__(self, widget, text, delay=500):
        # ... existing code ...

def crear_tooltip(widget, texto):
    return Tooltip(widget, texto)
```

```261:304:main.py
def agregar_icono_a_boton(boton, ruta_icono, tamaño=(24, 24)):
    from PIL import Image, ImageTk
    # ... existing code ...
```

```305:321:main.py
def validar_campo_visual(entry, es_valido, mensaje_error=""):
    """Aplica validación visual a un campo Entry"""
    # ... existing code ...
```


## Modelo de dominio y persistencia

- `Producto`: datos base, precios derivados, soporte de `oferta` (`{'tipo': ..., 'valor': ...}`)
```335:348:main.py
class Producto:
    def __init__(self, marca: str, descripcion: str, color: str, talle: str, cantidad: int, precio_costo: float, porcentaje_venta: float = 50, porcentaje_amigo: float = 20, oferta: dict = {}):
        # ... existing code ...
    def calcular_precio_venta(self):
        return round(self.precio_costo * (1 + self.porcentaje_venta / 100), 2)
```

- `Venta`: describe una operación con items (producto/cantidad/precio) y forma de pago
```360:366:main.py
class Venta:
    def __init__(self, descripcion: str, items: list, fecha: datetime.date, forma_pago: str = "EFECTIVO"):
        # ... existing code ...
```

- `SistemaGestion`: capa repositorio + persistencia JSON
```367:399:main.py
class SistemaGestion:
    def __init__(self):
        self.productos: List[Producto] = []
        self.ventas: List[Venta] = []
        self.cargar_datos()
    def cargar_datos(self):
        if os.path.exists("productos.json"):
            # ... existing code ...
```

- Guardados y archivo histórico por año en cierre de caja:
```415:433:main.py
def guardar_ventas(self):
    with open("ventas.json", "w", encoding="utf-8") as f:
        json.dump([
            # ... existing code ...
        ], f, ensure_ascii=False, indent=2)
```

```462:504:main.py
def archivar_ventas_dia(self, fecha):
    """Archiva las ventas del día en un archivo histórico y las elimina del día actual"""
    archivo_historico = f"ventas_historico_{fecha.strftime('%Y')}.json"
    # ... existing code ...
```


## Aplicación principal y navegación

Punto de entrada:
```4612:4619:main.py
if __name__ == "__main__":
    print("[DEBUG] Creando instancia de SistemaGestion... - main.py:4613")
    sistema = SistemaGestion()
    print("[DEBUG] SistemaGestion creado. Creando AppPilchero... - main.py:4615")
    app = AppPilchero(sistema)
    print("[DEBUG] AppPilchero creado. Ejecutando mainloop... - main.py:4617")
    app.mainloop()
```

Inicialización y layout (`Canvas` con gradiente, registro de widgets de pantalla):
```605:616:main.py
def crear_widgets(self):
    self.canvas_bg = tk.Canvas(self, width=1280, height=720, highlightthickness=0, bd=0)
    # ... existing code ...
    self.mostrar_menu_principal()
```

Menú principal (botones principales):
```1073:1180:main.py
def mostrar_menu_principal(self):
    # ... existing code ...
```

Menú gestión (dos columnas + Panel IA):
```860:965:main.py
def mostrar_menu_secundario(self):
    # ... existing code ...
```


## Pantallas funcionales

- Nueva venta (autocompletar, ofertas, IVA, totales, forma de pago):
```1219:1249:main.py
def _pantalla_venta(self, parent):
    """Pantalla de ventas optimizada con diseño moderno y profesional"""
    # ... existing code ...
```

- Ventas del día y cierre de caja:
```1642:1677:main.py
def _pantalla_ventas_dia(self, parent):
    # ... existing code ...
```

- Exportar CSV del cierre y archivo histórico:
```1749:1815:main.py
def generar_csv_cierre(self, ventas_hoy, fecha):
    """Genera archivo CSV con el resumen del día"""
    # ... existing code ...
```

- Carga masiva CSV (modelo y carga validada):
```1823:1875:main.py
def carga_masiva_productos(self):
    # ... existing code ...
```

- Reportes (filtros avanzados, estadísticas y exportación, incluye ventas históricas del período):
```1876:1891:main.py
def mostrar_reportes(self):
    """Pantalla de reportes con diseño moderno y filtros avanzados"""
    # ... existing code ...
```

```2077:2136:main.py
def filtrar_ventas():
    """Filtra las ventas según los criterios seleccionados"""
    # ... existing code ...
```

- Alta de producto (placeholders, cálculo dinámico de precios):
```2307:2331:main.py
def _pantalla_alta_producto(self, parent):
    """Pantalla para agregar productos con diseño moderno"""
    # ... existing code ...
```

```2464:2484:main.py
def calcular_precios(*args):
    """Calcula y muestra los precios en tiempo real"""
    # ... existing code ...
```

- Nota sobre actualización de precio: Esta función se realiza desde Inventario → Modificar producto. La antigua pantalla de "Actualizar Precio" fue eliminada y cualquier acceso se redirige automáticamente al Inventario para mantener compatibilidad y estilo.

- Inventario (buscador, filtros, acciones masivas, exportación):
```2957:2964:main.py
cols = ("Marca", "Descripción", "Color", "Talle", "Stock", "Precio Costo", "Precio Venta", "Valor Total")
```

```3079:3118:main.py
def eliminar_producto():
    # ... existing code ...
```

- Ofertas (porcentaje, cantidad 3x2, precio manual):
```3308:3316:main.py
def _pantalla_crear_ofertas(self, parent, solo_ofertas_activas=False):
    """Pantalla para crear y gestionar ofertas en productos"""
    # ... existing code ...
```

```3455:3513:main.py
def aplicar_oferta():
    # ... existing code ...
```


## Centro IA (heurísticas)

Vistas IA y navegación:
```3600:3616:main.py
def _cambiar_vista_ia(self, vista):
    """Cambia entre las diferentes vistas del centro IA"""
    # ... existing code ...
```

- Reposición (configuración, tabla, urgencia/prioridad):
```3780:3796:main.py
def _mostrar_reposicion_ia(self):
    """Vista de sugerencias de reposición - Versión Visual Optimizada"""
    # ... existing code ...
```

```3897:3941:main.py
def actualizar_reposicion():
    # ... existing code ...
```

- Precios (margen/rotación y recomendaciones):
```4039:4095:main.py
# Análisis de precios con lógica mejorada
# ... existing code ...
```

- Análisis (categorización por performance, días de stock y recomendaciones):
```4339:4378:main.py
# Análisis detallado con categorización IA avanzada
# ... existing code ...
```

- Heurísticas base:
```4481:4496:main.py
def _calcular_sugerencias_ia(self, dias_analisis, umbral_stock):
    """Algoritmo de IA para calcular sugerencias de reposición"""
    # ... existing code ...
```

```4501:4524:main.py
# Ordenar por prioridad (críticos primero)
# ... existing code ...
```

```4526:4541:main.py
def _obtener_ventas_producto(self, producto, dias):
    """Obtiene las ventas de un producto en los últimos N días"""
    # ... existing code ...
```


## Flujo de datos y formatos

- `productos.json`: lista de productos con `marca`, `descripcion`, `color`, `talle`, `cantidad`, `precio_costo`, `% venta`, `% amigo` (precios derivados se recalculan al cargar)
- `ventas.json`: ventas activas del período (mientras no se cierre). Cada venta serializa items con descripción/color/talle (no ID), cantidad y precio
- `ventas_historico_YYYY.json`: generado en cierre de caja (mueve ventas del día y limpia las actuales)
- CSV:
  - Cierre de caja: resumen por forma de pago y detalle por línea
  - Reportes: exporta la tabla de resultados
  - Inventario: exporta stock y valorización

Formateo moneda (punto miles, coma decimales, 3 decimales):
```1204:1216:main.py
def formato_moneda(self, valor):
    # ... existing code ...
```


## Ejecución local y empaquetado

- Requisitos: `pip install pillow`
- Ejecutar: `python main.py`
- Archivos generados en el working dir: `productos.json`, `ventas.json`, CSVs exportados, `ventas_historico_YYYY.json`
- Empaquetado (PyInstaller): el código detecta `sys._MEIPASS` para cargar imágenes desde el bundle; incluir recursos en el spec

Cargas de logos con soporte a empaquetado:
```625:633:main.py
if hasattr(sys, '_MEIPASS'):
    logo_path = os.path.join(sys._MEIPASS, "LOGO APP.png")
# ... existing code ...
```

```716:721:main.py
logo_path = os.path.join(sys._MEIPASS, "ALENRESULTADOS.png") if hasattr(sys, "_MEIPASS") else "ALENRESULTADOS.png"
```


## Puntos de extensión y buenas prácticas

- Persistencia de `oferta`: actualmente no se guarda en `productos.json`. Para persistir, extender `guardar_productos` y `cargar_datos`
- Identificadores de producto: hoy se usan 4 campos como “clave”. Considere un ID único para trazabilidad robusta
- Reportes: `venta.total` se calcula on-the-fly. Persistir `total` si requiere consultas directas sin recalcular
- Validaciones: centralizar y reutilizar `validar_campo_visual` y tooltips en nuevas pantallas
- IA: extraer heurísticas a un módulo/clase independiente para tests unitarios y mantenimiento
- Internacionalización: centralizar textos para futuras traducciones
- Rendimiento: paginación/virtualización en tablas si escala de datos crece
- Concurrencia: evitar I/O pesado en el hilo de UI; usar hilos si agregan tareas largas


## Limitaciones conocidas

- Ofertas no persistidas en JSON por defecto
- Items de venta guardan descripción/color/talle sin ID (riesgo si cambian textos)
- No hay bloqueo concurrente de archivos JSON
- DPI/escala: la ventana es fija 1280x720; monitores con alto DPI podrían requerir ajustes


## Extractos y utilidades adicionales

- Ordenamiento en `Treeview` por encabezado:
```4590:4611:main.py
def habilitar_ordenamiento_treeview(tree: ttk.Treeview):
    def try_float(value: str):
        # Normaliza formato moneda $12.345,67 -> 12345.67
        # ... existing code ...
    def sort_by(col: str, reverse: bool = False):
        # ... existing code ...
    for col in tree["columns"]:
        tree.heading(col, command=lambda c=col: sort_by(c, False))
```

- Botón universal “Volver” (chip):
```4571:4589:main.py
def _chip_volver(self, on_volver, x=50, y=20):
    """Crea el botón volver con alta visibilidad en esquina superior derecha"""
    # ... existing code ...
```

- Estilo `Combobox` personalizado:
```135:144:main.py
def aplicar_estilo_moderno_combobox(combo):
    style = ttk.Style()
    style.theme_use('default')
    # ... existing code ...
```

- Lógica de ofertas en carrito (3x2):
```1538:1554:main.py
# Aplicar lógica de ofertas por cantidad (ej: 3x2)
# ... existing code ...
```

- Cierre de caja con confirmación de descarga CSV:
```1693:1744:main.py
def mostrar_ventana_descarga_csv(self, ventas_hoy, fecha):
    # ... existing code ...
```


---

Este documento resume y enlaza los puntos clave de `main.py` para acelerar el onboarding y el trabajo de mantenimiento. Use las citas para navegar rápidamente a las secciones relevantes del código dentro del editor.
