




# Guía para Agentes de IA — ALENIA-GESTION-KONTROL+ v2.3 (2025)

## Arquitectura y Componentes Clave

### Sistema Desktop Principal (main.py)
- **Framework**: Tkinter con canvas fijo 1280x720 y gradiente de fondo automatizado
- **Navegación estricta**: Métodos `mostrar_*()` → `limpiar_pantalla()` → `_colocar_logo()` → `_pantalla_*()`
- **UI moderna**: Paleta oscura definida en constantes `COLOR_*` (líneas 12-35), fuente Montserrat, efectos hover
- **Gestión de widgets**: Lista `self.pantalla_widgets` para limpieza automática entre pantallas

### Sistema Web CRM & Landing
- **Frontend**: `docs/landing_kontrol.html` con formularios AJAX puros (sin frameworks)
- **Backend**: `crm_app.py` - API Flask REST (`/api/lead`, `/api/leads`) desplegada en Railway
- **Panel Admin**: `docs/crm_panel_demo.html` para consulta/exportación de leads
- **Deploy**: GitHub Pages para frontend, Railway para backend Flask

### Modelo de Datos Core
- **Productos**: Identificación por clave compuesta `(marca, descripcion, color, talle)`
- **Sistema de ofertas**: 3 tipos - `porcentaje` (descuento %), `cantidad` (3x2), `precio_manual`
- **Ventas**: Registro con carrito, múltiples formas de pago, IVA automático (21%)
- **Persistencia**: JSON local (`productos.json`, `ventas.json`) + archivos históricos anuales

## Patrones de Desarrollo Críticos

### Navegación UI Obligatoria
```python
def mostrar_nueva_pantalla(self):
    self.limpiar_pantalla()                    # SIEMPRE primero
    self._colocar_logo(pantalla_principal=False)  # Logo apropiado
    self._chip_volver(self.metodo_anterior)     # Navegación consistente
    self._pantalla_nueva_pantalla(self.canvas_bg)  # Contenido específico
```

### Sistema de Estilos Modernos
- **Botones**: `aplicar_estilo_moderno_boton(btn, tipo, hover_efecto=True)` donde tipo = `primario|secundario|success|warning|danger`
- **Tooltips**: `crear_tooltip(widget, texto)` en TODOS los elementos interactivos
- **Validación visual**: Verde/rojo inmediato con `validar_campo_visual(entry, es_valido, mensaje)`
- **Treeviews**: `aplicar_estilo_moderno_treeview(tree)` + `habilitar_ordenamiento_treeview(tree)`

### Lógica de Negocio Específica
- **Ofertas 3x2**: Lógica especial en carrito que modifica cantidad a cobrar, no precio unitario
- **Stock crítico**: Alertas automáticas ≤5 unidades, destacado visual en inventario
- **Cierre de caja**: Archiva ventas del día en `ventas_historico_YYYY.json`, mantiene actual limpio
- **Carga masiva**: Plantilla `modelo_productos.csv` con validación estricta de campos

## Flujos de Trabajo y Comandos

### Debug y Desarrollo
- **Trazabilidad**: `print("[DEBUG] descripción - main.py:línea")` en cada flujo importante
- **Ejecución**: `python main.py` desde raíz del proyecto
- **Testing**: Usar datos de ejemplo en `productos.json` y `ventas.json`

### Integración CRM
- **Frontend → Backend**: Solo AJAX con `fetch()`, nunca formularios síncronos
- **Validación dual**: JavaScript en frontend + Flask en backend
- **URLs hardcodeadas**: Backend Railway en archivos HTML (actualizar en deploy)

### Deployment y Distribución
- **Local**: `python main.py` o ejecutable `Alen.iA.exe`
- **Web**: GitHub Pages (`docs/`) + Railway (backend Flask)
- **Assets**: Logos específicos por pantalla (`LOGO APP.png`, `7.png`, `ALENRESULTADOS.png`)

## Reglas Arquitecturales Inmutables

1. **UI consistency**: Paleta `COLOR_*`, Montserrat, gradientes, efectos hover obligatorios
2. **Widget management**: Registrar en `self.pantalla_widgets`, limpiar antes de nueva pantalla
3. **Data persistence**: Llamar `guardar_productos()`/`guardar_ventas()` tras cada modificación
4. **Navigation pattern**: Método `mostrar_*` → método `_pantalla_*`, chip volver siempre presente
5. **Error handling**: Usar `messagebox` para feedback usuario, `print("[DEBUG]")` para desarrollador

## Centro IA y Análisis Avanzado

- **Dashboard**: Métricas en tiempo real, alertas de stock crítico, productos estrella
- **Reposición inteligente**: Algoritmo basado en velocidad de venta y días restantes
- **Optimización precios**: Sugerencias basadas en rotación y márgenes
- **Análisis tendencias**: Evaluación por marca, productos lentos, categorización automática

## Referencias Críticas para Desarrollo

- **UI patterns**: `docs/MEJORAS_VISUALES_UI.md` - checklist de estilos modernos
- **User flows**: `GUIA_USUARIO_COMPLETA.md` - flujos completos paso a paso  
- **Deploy status**: `DEPLOY_STATUS.md` - estado Railway y próximos pasos
- **Visual guide**: `GUIA_VISUAL_USUARIO.html` - capturas y explicaciones detalladas
