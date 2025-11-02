"""
===========================================================
⚙ ESCALA360 - Configuração da Aplicação Flask (PostgreSQL)
===========================================================

Autor: Anderson de Matos Guimarães
Data: 02/11/2025

Descrição:
Carrega variáveis de ambiente do arquivo .env, define as
configurações principais da aplicação Flask e constrói a
string de conexão com o banco de dados PostgreSQL.
===========================================================
"""

import os
from pathlib import Path
from dotenv import load_dotenv


# =========================================================
# 📁 Diretórios principais
# =========================================================
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

# Carrega o arquivo .env
load_dotenv(dotenv_path=ENV_PATH, override=True)


# =========================================================
# ⚙ Classe principal de configuração
# =========================================================
class Config:
    """Configurações globais da aplicação ESCALA360."""

    # Flask
    FLASK_APP = os.getenv("FLASK_APP", "app.py")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "escala360_secretkey")

    # Servidor
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 5050))

    # Banco de Dados
    DB_ENGINE = os.getenv("DB_ENGINE", "postgresql")
    DB_NAME = os.getenv("DB_NAME", "escala360")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")

    # Construção dinâmica da URI de conexão
    SQLALCHEMY_DATABASE_URI = (
        f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Logs
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", str(BASE_DIR / "logs" / "escala360.log"))
    LOG_FORMAT = os.getenv(
        "LOG_FORMAT", "%(asctime)s - %(levelname)s - %(message)s"
    )

    # BI / Plotly
    ENABLE_BI = os.getenv("ENABLE_BI", "true").lower() == "true"
    PLOTLY_THEME = os.getenv("PLOTLY_THEME", "plotly_dark")

    # Metadados
    APP_NAME = "ESCALA360"
    APP_VERSION = "1.0.0"
    AUTHOR = "Anderson de Matos Guimarães"
    APP_DESCRIPTION = (
        "Sistema de gestão e visualização de escalas e produtividade"
    )

    # Garante diretórios de logs
    Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)


# =========================================================
# 🧱 Criação automática de diretórios essenciais
# =========================================================
def ensure_directories():
    """Garante a existência de pastas para logs."""
    Path(Config.LOG_FILE).parent.mkdir(parents=True, exist_ok=True)


ensure_directories()
