#!/usr/bin/env python3
"""
Railway Start Script - Aplicación CRM para captura de leads
"""
import os
import sys

# Agregar el directorio actual al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar la aplicación Flask
from crm_app import app

# Railway necesita que la app esté disponible en el módulo
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
