# CRM KONTROL+ - Captura de Leads

Sistema Flask para capturar leads de KONTROL+ y gestionar descargas.

## Endpoints disponibles
- `POST /api/lead` - Registrar nuevo lead
- `GET /api/leads` - Obtener todos los leads (JSON)
- `GET /leads` - Panel básico de administración

## Deploy en Railway (raíz del repo)
- Usa `railway.toml` (Nixpacks) y `railway_start.py` que expone `app` desde `crm_app.py`.
- Comando de arranque: `gunicorn railway_start:app --bind 0.0.0.0:$PORT`.

### CLI (PowerShell)
```powershell
railway login
cd "C:\Users\Alejandro\Desktop\ML\ALENIA\APP\ALENIA-GESTION-KONTROL +V2.2"
railway up
railway open
```

## Persistencia de datos
SQLite del contenedor es efímero. Opciones:
- Volume: crea un volumen en Railway y configura la variable `DB=/data/crm_leads.db`.
- Postgres: crea un plugin Postgres y migra (recomendado para producción).

La app ya lee `DB` si está presente y crea la carpeta si hace falta.
