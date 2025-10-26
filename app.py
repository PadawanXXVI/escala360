"""
===========================================================
ESCALA360 - Sistema de Gestão de Escalas e Produtividade
Autor: Anderson de Matos Guimarães
Data: 26/10/2025
Framework: Flask 3.1.2
===========================================================

Descrição:
Aplicação web modular para gestão de escalas, substituições e produtividade
de profissionais em plantões. Inclui rotas principais, integração com banco
SQLite, API simulada e tratamento de erros customizados, com design moderno.
===========================================================
"""

from flask import Flask, render_template, jsonify, request
from config import Config
from models import db, init_app, popular_banco_inicial
import logging

# =========================================================
# 🔧 Inicialização da Aplicação Flask
# =========================================================
app = Flask(__name__)
app.config.from_object(Config)

# Inicializa o banco de dados (SQLAlchemy)
init_app(app)

# =========================================================
# 🧾 Configuração de Logging
# =========================================================
logging.basicConfig(
    filename=Config.LOG_FILE,
    level=getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S"
)
app.logger.info("✅ Configurações carregadas e banco inicializado.")

# Popula o banco de dados com dados de exemplo (caso vazio)
popular_banco_inicial(app)

# =========================================================
# 🔹 Rotas Principais
# =========================================================
@app.route('/')
def index():
    """Página inicial com o painel de produtividade (KPI + gráfico Plotly)."""
    app.logger.info("Acesso ao Painel de Produtividade (index.html)")
    return render_template('index.html', title='Painel Escala360')


@app.route('/escalas')
def escalas():
    """Página de gestão de escalas e substituições."""
    app.logger.info("Acesso à página de Escalas (escalas.html)")
    return render_template('escalas.html', title='Gestão de Escalas')


# =========================================================
# 🔹 API simulada / real (dados do banco)
# =========================================================
@app.route('/api/escalas')
def api_escalas():
    """
    Retorna todas as escalas do banco de dados (mock inicial).
    Substitui os dados estáticos anteriores por dados reais.
    """
    app.logger.info("Consulta à API /api/escalas (banco de dados)")

    from models import Escala, Funcionario, Turno
    escalas = Escala.query.all()
    resultado = [
        {
            "id": e.id,
            "data": e.data.strftime("%d/%m/%Y"),
            "servidor": e.funcionario.nome if e.funcionario else "—",
            "turno": e.turno.nome if e.turno else "—",
            "status": e.status
        }
        for e in escalas
    ]
    return jsonify(resultado)


# =========================================================
# 🔹 Rotas auxiliares e diagnósticas
# =========================================================
@app.route('/api/status')
def status():
    """Retorna o status da aplicação (útil para monitoramento)."""
    app.logger.info("Verificação de status do sistema")
    return jsonify({
        "status": "online",
        "app": Config.APP_NAME,
        "version": Config.APP_VERSION,
        "environment": Config.FLASK_ENV
    })


@app.route('/erro500')
def erro_teste():
    """Rota para simular um erro interno (testar o template 500.html)."""
    raise Exception("Erro interno simulado para testes.")


# =========================================================
# 🔹 Tratamento de Erros Customizados
# =========================================================
@app.errorhandler(404)
def page_not_found(e):
    """Erro 404 - Página não encontrada."""
    app.logger.warning(f"Erro 404 - Página não encontrada: {request.path}")
    return render_template('404.html', title='Página não encontrada'), 404


@app.errorhandler(500)
def internal_error(e):
    """Erro 500 - Falha interna do servidor."""
    app.logger.error(f"Erro 500 - Falha interna: {e}")
    return render_template('500.html', title='Erro Interno'), 500


# =========================================================
# 🚀 Execução Local / Deploy
# =========================================================
if __name__ == '__main__':
    app.logger.info("🚀 Servidor ESCALA360 iniciado em modo debug.")
    app.run(
        debug=Config.FLASK_DEBUG,
        host=Config.HOST,
        port=Config.PORT
    )
