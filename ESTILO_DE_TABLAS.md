# 📊 GUÍA DE ESTILO DE TABLAS - ALENIA GESTIÓN KONTROL+

## 🎯 Propósito del Documento

Esta guía técnica documenta el estilo moderno y profesional implementado en la tabla del **DESGLOSE DETALLADO** del sistema de cierre de caja. El objetivo es estandarizar este diseño para todas las tablas del software, manteniendo consistencia visual y profesionalismo.

---

## 🎨 Paleta de Colores Estándar

### Colores Base del Sistema
```python
COLOR_FONDO_PRINCIPAL = "#0a0f1a"       # Fondo oscuro principal
COLOR_MARCO_INTERNO = "#1a1f2e"         # Fondo interno de contenedores
COLOR_TEXTO_PRINCIPAL = "#e5e7eb"       # Texto principal claro
```

### Colores Específicos para Tablas
```python
# Marco y Bordes
COLOR_BORDE_TABLA = "#3b82f6"           # Azul profesional para bordes
COLOR_HIGHLIGHT = "#3b82f6"             # Highlight para efectos focus

# Headers de Tabla
COLOR_HEADER_BG = "#2563eb"             # Fondo azul corporativo para headers
COLOR_HEADER_TEXT = "#ffffff"           # Texto blanco en headers

# Filas de Datos (Alternadas)
COLOR_FILA_PAR = "#1e293b"              # Filas pares (más claro)
COLOR_FILA_IMPAR = "#0f172a"            # Filas impares (más oscuro)

# Separadores y Líneas
COLOR_SEPARADOR = "#3b82f6"             # Líneas de separación azul elegante
```

### Colores Semánticos para Datos
```python
# Indicadores de Rendimiento
COLOR_MARGEN_EXCELENTE = "#10b981"      # Verde para márgenes >30%
COLOR_MARGEN_BUENO = "#f59e0b"          # Naranja para márgenes 15-30%
COLOR_MARGEN_BAJO = "#ef4444"           # Rojo para márgenes <15%

# Datos Monetarios
COLOR_MONTOS = "#93c5fd"                # Azul claro para valores monetarios
```

---

## 🏗️ Estructura Técnica de Implementación

### 1. Marco Principal
```python
def crear_tabla_profesional(parent, altura=350):
    """Crea el contenedor principal de la tabla"""
    # Frame principal con fondo oscuro
    tabla_frame = tk.Frame(parent, bg="#0a0f1a", relief="flat", bd=0, height=altura)
    tabla_frame.pack(fill="both", expand=True, padx=20, pady=10)
    tabla_frame.pack_propagate(False)  # Mantener altura fija
    
    # Marco interno con diseño profesional - BORDE SUTIL
    marco_interno = tk.Frame(tabla_frame, bg="#1a1f2e", relief="solid", bd=1)
    marco_interno.pack(fill="both", expand=True, padx=3, pady=3)
    marco_interno.config(highlightbackground="#3b82f6", highlightcolor="#3b82f6", highlightthickness=2)
    
    return marco_interno
```

### 2. Header Profesional
```python
def crear_header_tabla(parent, titulo, icono="📊"):
    """Crea el header con título y separador elegante"""
    # Header con efecto neon mejorado
    header_label = tk.Label(parent, text=f"{icono} {titulo}", 
                          font=("Montserrat", 18, "bold"), 
                          bg="#1a1f2e", fg="#60a5fa", pady=15)
    header_label.pack(fill="x")
    
    # Línea separadora elegante
    separador = tk.Frame(parent, bg="#3b82f6", height=2)
    separador.pack(fill="x", padx=15, pady=(0, 10))
    
    return header_label
```

### 3. Headers de Columnas
```python
def crear_headers_columnas(parent, headers_config):
    """
    Crea los headers de las columnas de la tabla
    
    Args:
        parent: Widget contenedor
        headers_config: Lista de tuplas (texto, ancho)
                       Ej: [("Producto", 30), ("Cant.", 8), ("Vendido", 15)]
    """
    header_row = tk.Frame(parent, bg="#2563eb", relief="flat", bd=0)
    header_row.pack(fill="x", pady=(0, 5))
    
    for i, (header_text, width) in enumerate(headers_config):
        lbl_header = tk.Label(header_row, text=header_text, 
                             font=("Montserrat", 12, "bold"), 
                             bg="#2563eb", fg="#ffffff", 
                             width=width, pady=8)
        lbl_header.pack(side="left", padx=1)
    
    return header_row
```

### 4. Filas de Datos con Alternancia
```python
def crear_fila_datos(parent, valores_config, indice_fila):
    """
    Crea una fila de datos con colores alternados
    
    Args:
        parent: Widget contenedor
        valores_config: Lista de tuplas (valor, ancho, tipo_dato)
                       tipo_dato: 'texto', 'monto', 'margen', 'cantidad'
        indice_fila: Índice para determinar color alternado
    """
    # Color alternado para las filas
    bg_color = "#1e293b" if indice_fila % 2 == 0 else "#0f172a"
    
    row_frame = tk.Frame(parent, bg=bg_color, relief="flat", bd=0)
    row_frame.pack(fill="x", pady=1)
    
    for i, (valor, width, tipo_dato) in enumerate(valores_config):
        # Determinar color del texto según el tipo de dato
        text_color = obtener_color_por_tipo(valor, tipo_dato)
        
        lbl_valor = tk.Label(row_frame, text=valor, 
                           font=("Montserrat", 11), 
                           bg=bg_color, fg=text_color, 
                           width=width, pady=6)
        lbl_valor.pack(side="left", padx=1)
    
    return row_frame

def obtener_color_por_tipo(valor, tipo_dato):
    """Determina el color del texto según el tipo de dato"""
    if tipo_dato == "margen":
        try:
            margen_num = float(valor.replace("%", ""))
            if margen_num > 30:
                return "#10b981"  # Verde
            elif margen_num > 15:
                return "#f59e0b"  # Naranja
            else:
                return "#ef4444"  # Rojo
        except:
            return "#e5e7eb"
    elif tipo_dato == "monto":
        return "#93c5fd"  # Azul claro para montos
    else:
        return "#e5e7eb"  # Color estándar
```

---

## 📐 Especificaciones de Diseño

### Tipografía
- **Fuente principal**: Montserrat
- **Headers**: 12pt Bold (#ffffff sobre #2563eb)
- **Datos**: 11pt Regular (colores variables según tipo)
- **Títulos de sección**: 18pt Bold (#60a5fa)

### Espaciado y Márgenes
```python
# Contenedor principal
PADDING_EXTERNO = 20        # Margen del contenedor principal
PADDING_INTERNO = 3         # Margen interno del marco

# Elementos internos
PADDING_HEADER = 15         # Padding del título
PADDING_CELDA = 6           # Padding vertical de celdas
SEPARACION_FILAS = 1        # Espaciado entre filas

# Bordes y destacados
GROSOR_BORDE = 1            # Grosor del borde principal
GROSOR_HIGHLIGHT = 2        # Grosor del highlight
ALTURA_SEPARADOR = 2        # Altura de líneas separadoras
```

### Anchos de Columna Estándar
```python
ANCHOS_COLUMNA = {
    "producto_largo": 30,    # Nombres de productos
    "producto_corto": 20,    # Códigos o nombres cortos
    "cantidad": 8,           # Cantidades numéricas
    "monto": 15,            # Valores monetarios
    "porcentaje": 10,       # Porcentajes y ratios
    "fecha": 12,            # Fechas
    "estado": 10            # Estados o categorías
}
```

---

## 🔧 Implementación Práctica

### Ejemplo Completo: Tabla de Productos Top
```python
def crear_tabla_productos_top(parent, datos_productos):
    """Implementación completa del estilo de tabla estándar"""
    
    # 1. Crear marco principal
    marco = crear_tabla_profesional(parent, altura=350)
    
    # 2. Crear header con título
    crear_header_tabla(marco, "TOP PRODUCTOS VENDIDOS", "🏆")
    
    # 3. Contenedor de la tabla
    tabla_container = tk.Frame(marco, bg="#1a1f2e")
    tabla_container.pack(fill="both", expand=True, padx=15, pady=(5, 20))
    
    # 4. Headers de columnas
    headers_config = [
        ("Producto", 30),
        ("Cant.", 8), 
        ("Vendido", 15),
        ("Costo", 15),
        ("Margen", 10)
    ]
    crear_headers_columnas(tabla_container, headers_config)
    
    # 5. Filas de datos
    for idx, producto in enumerate(datos_productos):
        valores_config = [
            (producto['nombre'][:28] + "..." if len(producto['nombre']) > 28 else producto['nombre'], 30, "texto"),
            (str(producto['cantidad']), 8, "cantidad"),
            (formato_moneda(producto['vendido']), 15, "monto"),
            (formato_moneda(producto['costo']), 15, "monto"),
            (f"{producto['margen']:.1f}%", 10, "margen")
        ]
        crear_fila_datos(tabla_container, valores_config, idx)
    
    return marco
```

---

## 🎯 Casos de Uso Específicos

### 1. Tablas de Inventario
- **Headers**: Producto, Stock, Precio Costo, Precio Venta, Estado
- **Colores especiales**: Stock crítico en rojo (#ef4444)
- **Ancho recomendado**: 25, 8, 15, 15, 12

### 2. Tablas de Ventas
- **Headers**: Fecha, Cliente, Productos, Total, Forma Pago
- **Colores especiales**: Totales en azul claro (#93c5fd)
- **Ancho recomendado**: 12, 20, 25, 15, 12

### 3. Tablas de Reportes
- **Headers**: Período, Ventas, Gastos, Ganancia, ROI
- **Colores especiales**: ROI con sistema de colores por rendimiento
- **Ancho recomendado**: 15, 15, 15, 15, 10

---

## ✅ Checklist de Implementación

Al implementar una nueva tabla, verificar:

- [ ] **Marco principal** con colores estándar (#0a0f1a, #1a1f2e)
- [ ] **Borde profesional** con highlight azul (#3b82f6)
- [ ] **Header con separador** elegante
- [ ] **Headers de columna** con fondo azul corporativo (#2563eb)
- [ ] **Filas alternadas** (#1e293b / #0f172a)
- [ ] **Colores semánticos** para tipos de datos específicos
- [ ] **Tipografía Montserrat** en todos los elementos
- [ ] **Espaciado consistente** según especificaciones
- [ ] **Anchos de columna** apropiados para el tipo de contenido

---

## 🔄 Funciones Utilitarias

### Función Helper para Formato Monetario
```python
def formato_moneda(valor):
    """Formatea valores monetarios según estándar del sistema"""
    try:
        valor_num = float(valor)
    except:
        return "$0"
    entero = int(round(valor_num))
    signo = "-" if entero < 0 else ""
    miles = f"{abs(entero):,}".replace(",", ".")
    return f"{signo}${miles}"
```

### Función Helper para Validación de Márgenes
```python
def clasificar_margen(margen_porcentaje):
    """Clasifica el margen y retorna el color apropiado"""
    if margen_porcentaje > 30:
        return "#10b981", "EXCELENTE"
    elif margen_porcentaje > 15:
        return "#f59e0b", "BUENO"
    else:
        return "#ef4444", "BAJO"
```

---

## 📝 Notas de Mantenimiento

1. **Consistencia**: Todas las tablas deben seguir esta guía para mantener la identidad visual
2. **Escalabilidad**: Los anchos de columna pueden ajustarse según el contenido específico
3. **Accesibilidad**: Los colores elegidos mantienen suficiente contraste para legibilidad
4. **Performance**: Usar `pack_propagate(False)` para alturas fijas evita recálculos innecesarios

---

**Versión**: 1.0  
**Fecha**: 17 de Agosto de 2025  
**Sistema**: ALENIA GESTIÓN KONTROL+ v2.3  
**Autor**: Equipo de Desarrollo Alen.iA
