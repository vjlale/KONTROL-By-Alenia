## Plan de trabajo: Autenticación con usuarios y contraseñas (registro admin y roles)

### Resumen
Incorporar autenticación local al sistema con registro inicial de administrador, login posterior para todos los usuarios y control de permisos por rol (RBAC). Persistencia en `usuarios.json` con contraseñas hasheadas y sales. Integración visual con la paleta y estilos actuales (`aplicar_estilo_moderno_*`).

### Alcance
- Registro inicial (primer arranque): crear usuario ADMIN.
- Login para accesos posteriores (ADMIN/VENDEDOR).
- Control de sesión y visibilidad por rol en menús y pantallas.
- Atribución de vendedor en ventas y compatibilidad con reportes (actual + histórico).
- Gestión de usuarios (solo ADMIN): alta, cambio de contraseña, activar/desactivar.

## Arquitectura propuesta

### Archivos y persistencia
- `usuarios.json` (local JSON), un objeto por usuario:
  - `username: string`
  - `role: "admin" | "vendedor"`
  - `password_hash: string` (hex/base64)
  - `salt: string` (hex/base64)
  - `created_at: ISO8601`
  - `last_login: ISO8601 | null`
  - `is_active: bool`
- Seguridad de contraseña:
  - PBKDF2-HMAC-SHA256: `hashlib.pbkdf2_hmac('sha256', password, salt, 200_000)`
  - `salt = os.urandom(16)` por usuario.
  - Almacenar `salt` y `password_hash` en hex/base64. No guardar contraseñas en claro.

### Servicios de lógica
- `AuthManager` (nuevo módulo/clase):
  - `load_users()`, `save_users()`
  - `is_first_run()` — no hay admin registrado
  - `register_admin(username, password)` — valida y crea ADMIN
  - `register_user(username, password, role)` — ADMIN-only
  - `authenticate(username, password) -> User | None`
  - `change_password(username, old_password, new_password)`
  - `deactivate_user(username)` — ADMIN-only
  - Retardo progresivo por intentos fallidos (throttling)
- `Session`/`SessionManager`:
  - `current_user`, `role`, `login_time`
  - Helpers: `is_admin()`, `require_role()`

### Integración con el UI (Tkinter)
- Pantalla Onboarding (solo primera ejecución): crear ADMIN (usuario, contraseña, confirmación).
- Pantalla Login: usuario + contraseña, “Entrar”, errores amigables, botón mostrar/ocultar contraseña.
- Cerrar sesión: chip superior “Salir” que vuelve al Login.
- Gestión de usuarios (solo ADMIN) en Menú Gestión: lista, crear usuario, cambiar contraseña, activar/desactivar.
- Reutilizar paleta y estilos: `aplicar_estilo_moderno_boton`, `entry`, `label`, `combobox`, `treeview`.

### Control de permisos (RBAC)
- ADMIN: acceso a todas las pantallas y acciones.
- VENDEDOR: Venta, Ventas del día, Inventario (solo lectura/export), Reportes (solo lectura), Ofertas (solo lectura o según política).
- Aplicación:
  - Filtrar botones en `mostrar_menu_secundario()` según `session.role`.
  - Bloquear llamadas directas: métodos sensibles validan rol y abortan con mensaje si no hay permiso.

### Ventas/Reportes
- Registrar `vendedor` al confirmar venta: `venta.vendedor = session.username`.
- Persistir `vendedor` en `ventas.json` y en `ventas_historico_YYYY.json` (en cierre/archivo).
- Reportes: el filtro por vendedor ya existe para ventas actuales; extender a histórico:
  - Leer `vendedor` cuando esté disponible y aplicar el filtro.
  - Fallback “Sin especificar” en históricos antiguos sin `vendedor`.

## Flujo de inicio
- `if AuthManager.is_first_run():` → mostrar Onboarding → crear ADMIN → login automático → cargar `AppPilchero`.
- Else → mostrar Login → autenticar → `AppPilchero` con `session` inyectada.
- Cerrar sesión: destruir `AppPilchero` y volver a Login.

## Plan por fases (iterativo)

### Fase 1: Autenticación base
- Implementar `AuthManager` con hash/salt PBKDF2 y `usuarios.json`.
- Onboarding (crear admin) + Login (validación, errores, throttling básico).
- Integración mínima: tras login, lanzar app actual.
- Entregables: módulo `auth`, pantallas Onboarding/Login, `usuarios.json` generado.

### Fase 2: Sesión y RBAC
- `SessionManager` y almacenamiento de usuario/rol logueado.
- Ocultar/mostrar botones y bloquear accesos por rol.
- Botón “Cerrar sesión”.
- Entregables: menús adaptados por rol, middleware de autorización en métodos.

### Fase 3: Ventas con vendedor y reportes
- Setear `venta.vendedor` al registrar ventas.
- Incluir `vendedor` en `guardar_ventas()` y `archivar_ventas_dia()`.
- Reportes: aplicar filtro de vendedor también sobre histórico.
- Entregables: ventas atribuidas, reportes unificados (actual + histórico) por vendedor.

### Fase 4: Gestión de usuarios (ADMIN)
- Pantalla de administración: tabla de usuarios (usuario, rol, activo, último login).
- Crear usuario (rol), cambio de contraseña, desactivar usuario.
- Entregables: UI de gestión de usuarios, validación de contraseñas.

### Fase 5: Hardening y pruebas
- Fuerza de contraseña (longitud mínima, mayúsc/minúsc/dígito/símbolo) y validadores UI.
- Throttling progresivo en login (3→5s, 5→30s).
- Pruebas unitarias de `AuthManager` y de integración de flujo.
- Documentación en `docs/MANUAL_TECNICO_MAIN.md` (nueva sección Autenticación y Roles).

## Criterios de aceptación
- Primera ejecución exige crear un ADMIN y accede a la app.
- Login requerido en ejecuciones posteriores; contraseñas nunca en claro.
- RBAC efectivo: usuarios ven solo lo permitido y no pueden invocar métodos restringidos.
- Todas las ventas se atribuyen a un usuario y aparecen en reportes actuales e históricos con filtro por vendedor.

## Pruebas
- Unitarias `AuthManager`:
  - Registro admin/usuario, hash correcto, verificación, cambio de contraseña, usuario inactivo.
- Integración:
  - Onboarding → Login → flujo ADMIN.
  - Login VENDEDOR → botones restringidos → restricciones en métodos.
  - Registrar venta y validar `vendedor` en JSON/histórico.
  - Reportes: filtros por fecha, forma de pago, marca y vendedor (actual + histórico).
- UX/Visual:
  - DPI/escala Windows, estilo consistente en nuevas pantallas.

## Riesgos y mitigaciones
- Olvido de contraseña admin: procedimiento manual (reset en `usuarios.json` o crear admin temporal con token local).
- JSON corrupto: backups simples (copias con timestamp al guardar usuarios/ventas).
- Crecimiento de histórico: mantener lectura por año (ya implementado en reportes).

## Checklist de implementación
- [ ] `AuthManager` con PBKDF2+salt y `usuarios.json`
- [ ] Onboarding (crear admin)
- [ ] Login (throttling básico)
- [ ] `SessionManager` e inyección de sesión en `AppPilchero`
- [ ] RBAC en menús y métodos
- [ ] Atribución de `vendedor` en ventas y persistencia
- [ ] Reportes: filtro vendedor también en histórico
- [ ] Gestión de usuarios (ADMIN)
- [ ] Fuerza de contraseñas y validadores UI
- [ ] Pruebas y documentación

### Notas de implementación
- Reutilizar funciones de estilo para mantener fidelidad visual.
- No introducir dependencias externas; usar solo bibliotecas estándar.
- Considerar `usuarios.json` fuera del control de versiones si se versiona el proyecto.

