# CRM KONTROL+ - Captura de Leads

Sistema Flask para capturar leads de KONTROL+ y gestionar descargas.

## Endpoints disponibles:
- `POST /api/lead` - Registrar nuevo lead
- `GET /api/leads` - Obtener todos los leads (JSON)
- `GET /leads` - Panel básico de administración

## Deploy en Railway:
1. Conectar repositorio GitHub
2. Railway detecta automáticamente Flask
3. Variables de entorno se configuran automáticamente
4. Base de datos SQLite se inicializa automáticamente

## Uso:
El sistema captura leads desde el landing page y los almacena en SQLite local.
Panel CRM consume la API para mostrar leads en tiempo real.
