"""
===========================================================
ESCALA360 - Sistema de Gestão de Escalas e Produtividade
Autor: Anderson de Matos Guimarães
Data: 26/10/2025
Framework: Flask 3.1.2
===========================================================

Descrição:
Aplicação web modular com Blueprints (escalas, usuarios),
integração a SQLite/SQLAlchemy, rotas de status e tratamento
de erros customizados.
===========================================================
"""

from flask import Flask, render_template, jsonify, request
from config import Config
from models import init_app as init_db, popular_banco_inicial
import logging

# =========================================================
# 🔧 Inicialização da Aplicação Flask
# =========================================================
app = Flask(__name__)
app.config.from_object(Config)

# Banco de dados
init_db(app)
popular_banco_inicial(app)

# =========================================================
# 🧾 Logging
# =========================================================
logging.basicConfig(
    filename=Config.LOG_FILE,
    level=getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)
app.logger.info("✅ Configurações carregadas. DB inicializado.")

# =========================================================
# 🧩 Registro de Blueprints
# =========================================================
from blueprints.escalas import escalas_bp
from blueprints.usuarios import usuarios_bp

app.register_blueprint(escalas_bp)   # /escalas/...
app.register_blueprint(usuarios_bp)  # /usuarios/...

# =========================================================
# 🔹 Rotas “core”
# =========================================================
@app.get("/")
def index():
    """Página inicial com o painel de produtividade (KPI + gráfico Plotly)."""
    app.logger.info("Acesso ao Painel de Produtividade (index.html)")
    return render_template("index.html", title="Painel Escala360")


@app.get("/api/status")
def status():
    """Retorna o status da aplicação (útil para monitoramento)."""
    app.logger.info("Verificação de status do sistema")
    return jsonify(
        {
            "status": "online",
            "app": Config.APP_NAME,
            "version": Config.APP_VERSION,
            "environment": Config.FLASK_ENV,
        }
    )


@app.get("/erro500")
def erro_teste():
    """Rota para simular um erro interno (testar o template 500.html)."""
    raise Exception("Erro interno simulado para testes.")

# =========================================================
# ❗ Tratamento de Erros
# =========================================================
@app.errorhandler(404)
def page_not_found(e):
    app.logger.warning(f"Erro 404 - Página não encontrada: {request.path}")
    return render_template("404.html", title="Página não encontrada"), 404


@app.errorhandler(500)
def internal_error(e):
    app.logger.error(f"Erro 500 - Falha interna: {e}")
    return render_template("500.html", title="Erro Interno"), 500


# =========================================================
# 🚀 Execução Local
# =========================================================
if __name__ == "__main__":
    app.logger.info("🚀 Servidor ESCALA360 iniciado em modo debug.")
    app.run(debug=Config.FLASK_DEBUG, host=Config.HOST, port=Config.PORT)
