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

# Expondo a variável app para servidores WSGI (Gunicorn, uWSGI, etc.)
if __name__ == "__main__":
    app.run()
