from flask import Flask, request, render_template_string, redirect, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Permitir requests desde GitHub Pages
DB = 'crm_leads.db'

# Inicializar la base de datos
conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    rubro TEXT NOT NULL,
    fecha TEXT NOT NULL
)''')
conn.commit()
conn.close()

# Endpoint para recibir datos del formulario (POST)
@app.route('/api/lead', methods=['POST'])
def api_lead():
    email = request.form.get('email')
    rubro = request.form.get('rubro')
    if not email or not rubro:
        return {'ok': False, 'error': 'Faltan datos'}, 400
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('INSERT INTO leads (email, rubro, fecha) VALUES (?, ?, ?)', (email, rubro, fecha))
    conn.commit()
    conn.close()
    return {'ok': True}

# Endpoint para obtener todos los leads en formato JSON (para el panel CRM)
@app.route('/api/leads', methods=['GET'])
def api_leads():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT email, rubro, fecha FROM leads ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    # Opcional: agregar campo nombre si lo tienes en la base
    leads = [
        {"email": email, "rubro": rubro, "fecha": fecha, "nombre": ""} for email, rubro, fecha in rows
    ]
    return jsonify(leads)

# Panel simple para ver los leads
@app.route('/leads')
def leads():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT email, rubro, fecha FROM leads ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    html = '''
    <h2>Leads registrados</h2>
    <table border="1" cellpadding="8">
        <tr><th>Email</th><th>Rubro</th><th>Fecha</th></tr>
        {% for email, rubro, fecha in rows %}
        <tr><td>{{email}}</td><td>{{rubro}}</td><td>{{fecha}}</td></tr>
        {% endfor %}
    </table>
    <p>Total descargas: <b>{{rows|length}}</b></p>
    '''
    return render_template_string(html, rows=rows)

# Exponer la app para Gunicorn/Railway
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

# Instrucciones para publicar en GitHub Pages
'''
1. Crear la carpeta docs/ en tu repositorio si no existe
2. Copiar landing_kontrol.html y CARTA_PRESENTACION_GESTION_KONTROL.html dentro de docs/
3. Hacer commit y push de esos archivos al repositorio
4. Activar GitHub Pages desde la rama main y la carpeta /docs
5. Probar la URL pública que te da GitHub Pages
'''
