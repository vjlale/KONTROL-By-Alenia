# KONTROL+ CRM - Deploy Railway

## Archivos necesarios para Railway:

- `requirements.txt` ✅
- `Procfile` ✅  
- `railway_start.py` ✅
- `crm_app.py` ✅

## Comando de deploy Railway:

```bash
railway login
railway link
railway up
```

## URLs actuales:
- **Principal**: https://alenia-gestion-production-ae2f.up.railway.app
- **Fallback**: https://alenia-gestion-production.up.railway.app

## Endpoints disponibles:
- `POST /api/lead` - Recibir leads del formulario
- `GET /api/leads` - Obtener todos los leads (JSON)
- `GET /leads` - Panel básico HTML

## Test local:
```bash
python test_crm_local.py
```

## Variables de entorno Railway:
- `PORT` (automática)
- `PYTHONPATH=.` (opcional)
