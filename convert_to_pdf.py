import markdown
from weasyprint import HTML, CSS
from pathlib import Path

def markdown_to_pdf(markdown_file, pdf_file):
    """Convierte un archivo markdown a PDF con estilo profesional"""
    
    # Leer el archivo markdown
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convertir markdown a HTML
    html_content = markdown.markdown(markdown_content, extensions=['tables', 'fenced_code'])
    
    # CSS para estilo profesional
    css_style = """
    @page {
        size: A4;
        margin: 2cm;
        @top-center {
            content: "PLAN ESTRATÉGICO KONTROL+ | Alen.iA";
            font-size: 10pt;
            color: #666;
        }
        @bottom-center {
            content: "Página " counter(page) " de " counter(pages);
            font-size: 10pt;
            color: #666;
        }
    }
    
    body {
        font-family: "Segoe UI", Arial, sans-serif;
        line-height: 1.6;
        color: #333;
        font-size: 11pt;
    }
    
    h1 {
        color: #0033cc;
        font-size: 24pt;
        margin-bottom: 20px;
        border-bottom: 3px solid #0033cc;
        padding-bottom: 10px;
    }
    
    h2 {
        color: #258305;
        font-size: 18pt;
        margin-top: 30px;
        margin-bottom: 15px;
        background: linear-gradient(90deg, #258305, #34a805);
        color: white;
        padding: 10px 15px;
        border-radius: 5px;
    }
    
    h3 {
        color: #e89c2c;
        font-size: 14pt;
        margin-top: 20px;
        margin-bottom: 10px;
        border-left: 4px solid #e89c2c;
        padding-left: 10px;
    }
    
    h4 {
        color: #666;
        font-size: 12pt;
        margin-top: 15px;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    pre {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 5px;
        padding: 15px;
        margin: 15px 0;
        font-size: 10pt;
        overflow-x: auto;
    }
    
    code {
        background: #f8f9fa;
        padding: 2px 4px;
        border-radius: 3px;
        font-size: 10pt;
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
    }
    
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    
    th {
        background: #0033cc;
        color: white;
        font-weight: bold;
    }
    
    ul, ol {
        margin: 10px 0;
        padding-left: 20px;
    }
    
    li {
        margin: 5px 0;
    }
    
    blockquote {
        border-left: 4px solid #0033cc;
        margin: 15px 0;
        padding-left: 15px;
        color: #555;
        font-style: italic;
    }
    
    .highlight {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .success {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .warning {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .danger {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .page-break {
        page-break-before: always;
    }
    """
    
    # HTML completo con CSS
    full_html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Plan Estratégico KONTROL+ | Alen.iA</title>
        <style>{css_style}</style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Generar PDF
    try:
        HTML(string=full_html).write_pdf(pdf_file)
        print(f"✅ PDF generado exitosamente: {pdf_file}")
        return True
    except Exception as e:
        print(f"❌ Error generando PDF: {e}")
        return False

if __name__ == "__main__":
    # Archivos de entrada y salida
    markdown_file = "PLAN_LANZAMIENTO_KONTROL_PLUS.md"
    pdf_file = "PLAN_LANZAMIENTO_KONTROL_PLUS.pdf"
    
    # Verificar que existe el archivo markdown
    if Path(markdown_file).exists():
        success = markdown_to_pdf(markdown_file, pdf_file)
        if success:
            print(f"🎉 Plan estratégico convertido a PDF: {pdf_file}")
            print(f"📄 Archivo listo para presentar a stakeholders")
        else:
            print("💥 Error en la conversión")
    else:
        print(f"❌ No se encontró el archivo: {markdown_file}")
