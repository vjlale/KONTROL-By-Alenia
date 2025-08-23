import markdown
import pathlib
from datetime import datetime

def create_html_from_markdown():
    """Convierte el markdown a HTML con estilo profesional"""
    
    # Leer el archivo markdown
    with open("PLAN_LANZAMIENTO_KONTROL_PLUS.md", 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convertir markdown a HTML
    html_content = markdown.markdown(markdown_content, extensions=['tables', 'fenced_code'])
    
    # CSS profesional para el plan
    css_style = """
    <style>
        @media print {
            @page {
                size: A4;
                margin: 1.5cm;
            }
            body { font-size: 11pt; }
            h1 { font-size: 20pt; }
            h2 { font-size: 16pt; }
            h3 { font-size: 14pt; }
            .no-break { page-break-inside: avoid; }
        }
        
        body {
            font-family: "Segoe UI", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 21cm;
            margin: 0 auto;
            padding: 20px;
            background: white;
        }
        
        h1 {
            color: #0033cc;
            font-size: 28px;
            margin-bottom: 25px;
            border-bottom: 3px solid #0033cc;
            padding-bottom: 15px;
            text-align: center;
        }
        
        h2 {
            color: #258305;
            font-size: 20px;
            margin-top: 35px;
            margin-bottom: 20px;
            background: linear-gradient(90deg, #258305, #34a805);
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        h3 {
            color: #e89c2c;
            font-size: 16px;
            margin-top: 25px;
            margin-bottom: 15px;
            border-left: 5px solid #e89c2c;
            padding-left: 15px;
            background: rgba(232, 156, 44, 0.05);
            padding: 10px 15px;
        }
        
        h4 {
            color: #666;
            font-size: 14px;
            margin-top: 20px;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: bold;
        }
        
        pre {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 20px;
            margin: 20px 0;
            font-size: 12px;
            overflow-x: auto;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
        }
        
        code {
            background: #f8f9fa;
            padding: 3px 6px;
            border-radius: 4px;
            font-size: 13px;
            color: #e83e8c;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        
        th {
            background: #0033cc;
            color: white;
            font-weight: bold;
        }
        
        tr:nth-child(even) {
            background: #f8f9fa;
        }
        
        ul, ol {
            margin: 15px 0;
            padding-left: 25px;
        }
        
        li {
            margin: 8px 0;
        }
        
        li strong {
            color: #0033cc;
        }
        
        blockquote {
            border-left: 5px solid #0033cc;
            margin: 20px 0;
            padding-left: 20px;
            color: #555;
            font-style: italic;
            background: rgba(0, 51, 204, 0.05);
            padding: 15px 20px;
            border-radius: 0 6px 6px 0;
        }
        
        .header-info {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            border: 1px solid #e9ecef;
        }
        
        .success-box {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 15px;
            border-radius: 6px;
            margin: 15px 0;
        }
        
        .warning-box {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 15px;
            border-radius: 6px;
            margin: 15px 0;
        }
        
        .danger-box {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 15px;
            border-radius: 6px;
            margin: 15px 0;
        }
        
        .info-box {
            background: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
            padding: 15px;
            border-radius: 6px;
            margin: 15px 0;
        }
        
        .footer {
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid #0033cc;
            text-align: center;
            color: #666;
            font-style: italic;
        }
        
        .page-break {
            page-break-before: always;
        }
        
        /* Emojis y iconos */
        .emoji {
            font-size: 1.2em;
            margin-right: 5px;
        }
        
        /* Highlights especiales */
        mark {
            background: #fff3cd;
            padding: 2px 4px;
            border-radius: 3px;
        }
        
        strong {
            color: #0033cc;
            font-weight: 600;
        }
        
        /* Responsive para pantalla */
        @media screen and (max-width: 768px) {
            body {
                padding: 10px;
                font-size: 14px;
            }
            h1 { font-size: 24px; }
            h2 { font-size: 18px; }
            h3 { font-size: 16px; }
        }
    </style>
    """
    
    # HTML completo
    full_html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Plan Estratégico KONTROL+ | Alen.iA</title>
        {css_style}
    </head>
    <body>
        <div class="header-info">
            <h1>🚀 PLAN ESTRATÉGICO DE LANZAMIENTO<br>KONTROL+ por Alen.iA</h1>
            <p style="text-align: center; margin: 0; color: #666;">
                <strong>Fecha de creación:</strong> {datetime.now().strftime('%d de %B de %Y')}<br>
                <strong>Versión:</strong> 1.0 - Lanzamiento Oficial Instagram<br>
                <strong>Responsable:</strong> Alen.iA Team
            </p>
        </div>
        
        {html_content}
        
        <div class="footer">
            <p><strong>Plan Estratégico KONTROL+</strong> - Generado por GitHub Copilot para Alen.iA</p>
            <p>Documento confidencial - Solo para uso interno</p>
        </div>
        
        <script>
            // Script para imprimir automáticamente si se desea
            function printPlan() {{
                window.print();
            }}
            
            // Agregar botón de impresión
            document.addEventListener('DOMContentLoaded', function() {{
                const printBtn = document.createElement('button');
                printBtn.innerHTML = '🖨️ Imprimir PDF';
                printBtn.style.cssText = `
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: #0033cc;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    cursor: pointer;
                    font-weight: bold;
                    z-index: 1000;
                `;
                printBtn.onclick = printPlan;
                document.body.appendChild(printBtn);
                
                // Ocultar botón al imprimir
                window.addEventListener('beforeprint', function() {{
                    printBtn.style.display = 'none';
                }});
                
                window.addEventListener('afterprint', function() {{
                    printBtn.style.display = 'block';
                }});
            }});
        </script>
    </body>
    </html>
    """
    
    # Guardar HTML
    with open("PLAN_LANZAMIENTO_KONTROL_PLUS.html", 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print("✅ Archivo HTML generado: PLAN_LANZAMIENTO_KONTROL_PLUS.html")
    print("📄 Abre el archivo en tu navegador y usa Ctrl+P para generar el PDF")
    print("🎯 Configuración recomendada de impresión:")
    print("   - Tamaño: A4")
    print("   - Márgenes: Mínimos")
    print("   - Incluir gráficos de fondo: SÍ")
    print("   - Escala: 100%")

if __name__ == "__main__":
    try:
        create_html_from_markdown()
        print("\n🚀 Plan estratégico listo para presentar!")
    except Exception as e:
        print(f"❌ Error: {e}")
