"""
===========================================================
ESCALA360 - Pacote de Blueprints
Autor: Anderson de Matos Guimarães
Data: 31/10/2025
===========================================================

Descrição:
Centraliza o registro e a inicialização dos módulos
(blueprints) da aplicação ESCALA360.

Inclui:
- profissionais.py
- plantoes.py
- escalas.py
- substituicoes.py
- auditoria.py
===========================================================
"""

from flask import Flask

# Importa os módulos individuais
from .profissionais import profissionais_bp
from .plantoes import plantoes_bp
from .escalas import escalas_bp
from .substituicoes import substituicoes_bp
from .auditoria import auditoria_bp


def register_blueprints(app: Flask):
    """
    Registra todos os blueprints da aplicação Flask.
    """
    app.register_blueprint(profissionais_bp)
    app.register_blueprint(plantoes_bp)
    app.register_blueprint(escalas_bp)
    app.register_blueprint(substituicoes_bp)
    app.register_blueprint(auditoria_bp)

    # Log informativo
    app.logger.info("✅ Blueprints registrados com sucesso:")
    app.logger.info("   - profissionais_bp")
    app.logger.info("   - plantoes_bp")
    app.logger.info("   - escalas_bp")
    app.logger.info("   - substituicoes_bp")
    app.logger.info("   - auditoria_bp")
