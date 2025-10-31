"""
===========================================================
ESCALA360 - Sistema de Gestão de Escalas e Produtividade
Autor: Anderson de Matos Guimarães
Data: 31/10/2025
Framework: Flask 3.1.2
===========================================================

Descrição:
Aplicação web modular baseada em Blueprints (escalas, profissionais,
plantões, substituições e auditoria), integrada a SQLite/SQLAlchemy,
com logs persistentes, tratamento de erros customizados e contexto global.
===========================================================
"""

import logging
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from config import Config
from models import init_app as init_db, popular_banco_inicial

# =========================================================
# 🔧 Inicialização da Aplicação Flask
# =========================================================
app = Flask(__name__)
app.config.from_object(Config)

# Inicializa e popula o banco de dados
init_db(app)
popular_banco_inicial(app)

# =========================================================
# 🧾 Logging e Monitoramento
# =========================================================
logging.basicConfig(
    filename=Config.LOG_FILE,
    level=getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO),
    format=Config.LOG_FORMAT if hasattr(Config, "LOG_FORMAT") else "%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)
app.logger.info("✅ Configurações carregadas e banco inicializado com sucesso.")

# =========================================================
# 🧩 Registro de Blueprints
# =========================================================
from blueprints.escalas import escalas_bp
from blueprints.profissionais import profissionais_bp
from blueprints.plantoes import plantoes_bp
from blueprints.substituicoes import substituicoes_bp
from blueprints.auditoria import auditoria_bp

app.register_blueprint(escalas_bp)        # /escalas/...
app.register_blueprint(profissionais_bp)  # /profissionais/...
app.register_blueprint(plantoes_bp)       # /plantoes/...
app.register_blueprint(substituicoes_bp)  # /substituicoes/...
app.register_blueprint(auditoria_bp)      # /auditoria/...

# =========================================================
# 🕓 Contexto Global (para {{ now() }} em templates Jinja)
# =========================================================
@app.context_processor
def inject_now():
    """Permite usar {{ now() }} nos templates Jinja."""
    return {"now": datetime.now}

# =========================================================
# 🔹 Rotas principais (core)
# =========================================================
@app.get("/")
def index():
    """Renderiza o painel de produtividade principal (KPI + BI Plotly)."""
    app.logger.info("🟢 Acesso ao Painel de Produtividade (index.html)")
    return render_template("index.html", title="Painel de Produtividade – Escala360")


@app.get("/api/status")
def status():
    """Retorna o status geral da aplicação (monitoramento e health check)."""
    app.logger.info("🔍 Verificação de status do sistema")
    return jsonify(
        {
            "status": "online",
            "app": Config.APP_NAME,
            "version": Config.APP_VERSION,
            "environment": getattr(Config, "FLASK_ENV", "production"),
            "author": Config.AUTHOR,
        }
    )


@app.get("/erro500")
def erro_teste():
    """Rota de teste para disparar o template 500.html."""
    raise Exception("Erro interno simulado para testes do template 500.html.")

# =========================================================
# ❗ Tratamento de Erros Customizados
# =========================================================
@app.errorhandler(404)
def page_not_found(e):
    """Erro 404 - Página não encontrada."""
    app.logger.warning(f"⚠️ Erro 404 - Página não encontrada: {request.path}")
    return render_template("404.html", title="Página não encontrada – Escala360"), 404


@app.errorhandler(500)
def internal_error(e):
    """Erro 500 - Falha interna do servidor."""
    app.logger.error(f"❌ Erro 500 - Falha interna: {e}")
    return render_template("500.html", title="Erro interno – Escala360"), 500

# =========================================================
# 🚀 Execução Local (modo desenvolvimento)
# =========================================================
if __name__ == "__main__":
    app.logger.info(
        f"🚀 Servidor ESCALA360 iniciado em {Config.FLASK_ENV.upper()} "
        f"({Config.HOST}:{Config.PORT}) com debug={Config.FLASK_DEBUG}"
    )
    app.run(debug=Config.FLASK_DEBUG, host=Config.HOST, port=Config.PORT)
