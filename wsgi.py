"""
===========================================================
ESCALA360 - WSGI Entry Point
Autor: Anderson de Matos Guimarães
Data: 31/10/2025
===========================================================

Descrição:
Ponto de entrada WSGI para execução em servidores de produção.
Importa a instância principal do Flask definida em app.py.
===========================================================
"""

from app import app
import os

# Expondo a variável app para o servidor WSGI (Gunicorn, Vercel, etc.)
application = app  # compatível com servidores que esperam `application`

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5050))
    print(f"🚀 Servidor ESCALA360 iniciado em http://{host}:{port}")
    app.run(host=host, port=port)
