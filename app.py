"""
===========================================================
ESCALA360 - Sistema de Gestão de Escalas e Produtividade
Autor: Anderson de Matos Guimarães
Data: 02/11/2025
Framework: Flask 3.1.2
===========================================================

Descrição:
Aplicação web modular baseada em Blueprints (escalas, profissionais,
plantões, substituições e auditoria), integrada ao PostgreSQL via SQLAlchemy,
com logs persistentes, tratamento de erros customizados e painel BI.
===========================================================
"""

import os
import logging
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from config import Config
from models import init_app as init_db
from init_database import init_database


# =========================================================
# 🔧 Inicialização da Aplicação Flask
# =========================================================
app = Flask(__name__)
app.config.from_object(Config)


# =========================================================
# 🧾 Logging
# =========================================================
os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)
logging.basicConfig(
    filename=Config.LOG_FILE,
    level=getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO),
    format=getattr(Config, "LOG_FORMAT", "%(asctime)s [%(levelname)s] %(message)s"),
    datefmt="%d/%m/%Y %H:%M:%S",
)
logger = logging.getLogger("ESCALA360")
logger.info("🚀 Iniciando aplicação ESCALA360...")


# =========================================================
# 💾 Banco de Dados (PostgreSQL)
# =========================================================
try:
    init_db(app)
    init_database(app)
    logger.info("✅ Banco de dados PostgreSQL conectado e inicializado com sucesso.")
except Exception as e:
    logger.critical(f"❌ Falha crítica ao inicializar o banco de dados: {e}")
    raise


# =========================================================
# 🧩 Registro de Blueprints
# =========================================================
try:
    from blueprints.escalas import escalas_bp
    from blueprints.profissionais import profissionais_bp
    from blueprints.plantoes import plantoes_bp
    from blueprints.substituicoes import substituicoes_bp
    from blueprints.auditoria import auditoria_bp

    app.register_blueprint(escalas_bp)
    app.register_blueprint(profissionais_bp)
    app.register_blueprint(plantoes_bp)
    app.register_blueprint(substituicoes_bp)
    app.register_blueprint(auditoria_bp)

    logger.info("🧩 Blueprints registrados com sucesso.")
except Exception as e:
    logger.warning(f"⚠ Nenhum blueprint encontrado ou erro ao registrar: {e}")


# =========================================================
# 🕓 Contexto Global (para {{ now() }} em templates Jinja)
# =========================================================
@app.context_processor
def inject_now():
    return {"now": datetime.now}


# =========================================================
# 🌐 Rotas Principais
# =========================================================
@app.route("/")
def index():
    """Painel principal do sistema."""
    logger.info("🟢 Acesso ao painel principal (index.html)")
    return render_template("index.html", title="Painel de Produtividade – ESCALA360")


@app.route("/api/status")
def status():
    """Rota de monitoramento (health check)."""
    return jsonify(
        {
            "status": "online",
            "app": Config.APP_NAME,
            "version": Config.APP_VERSION,
            "author": Config.AUTHOR,
            "database": Config.DB_NAME,
            "engine": Config.DB_ENGINE,
        }
    )


@app.route("/erro500")
def erro_teste():
    """Simula erro interno para testar o template 500.html."""
    raise Exception("Erro interno simulado para testes.")


# =========================================================
# ❗ Tratamento de Erros Customizados
# =========================================================
@app.errorhandler(404)
def page_not_found(e):
    logger.warning(f"⚠ Erro 404 - Página não encontrada: {request.path}")
    return render_template("404.html", title="Página não encontrada – ESCALA360"), 404


@app.errorhandler(500)
def internal_error(e):
    logger.error(f"❌ Erro 500 - Falha interna: {e}")
    return render_template("500.html", title="Erro interno – ESCALA360"), 500


# =========================================================
# 🚀 Execução Local
# =========================================================
if __name__ == "_main_":
    logger.info(
        f"🚀 Servidor ESCALA360 iniciado ({Config.HOST}:{Config.PORT}) - Ambiente: {Config.FLASK_ENV.upper()}"
    )
    app.run(debug=Config.FLASK_DEBUG, host=Config.HOST, port=Config.PORT)
