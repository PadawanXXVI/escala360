"""
==============================================
⚙️ ESCALA360 - Configuração da Aplicação Flask
==============================================

Este módulo centraliza todas as configurações da aplicação,
carregando variáveis do arquivo .env e definindo parâmetros
para o ambiente, banco de dados, logs e integrações futuras.

Autor: Anderson de Matos Guimarães
Versão: 1.0.1
Data: 2025-10-31
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ---------------------------------------------
# 🔹 Carregamento do .env
# ---------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

# ---------------------------------------------
# 🔹 Classe principal de configuração
# ---------------------------------------------
class Config:
    """Configurações principais da aplicação ESCALA360."""

    # 🌐 Flask
    FLASK_APP = os.getenv("FLASK_APP", "app.py")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "escala360_secretkey")

    # 🌎 Servidor
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 5050))

    # 💾 Banco de Dados
    DB_ENGINE = os.getenv("DB_ENGINE", "sqlite")
    DB_NAME = os.getenv("DB_NAME", "escala360.db")
    DB_PATH = os.getenv("DB_PATH", str(BASE_DIR / "instance" / DB_NAME))

    # Garante que o diretório 'instance' exista
    instance_dir = Path(DB_PATH).parent
    instance_dir.mkdir(parents=True, exist_ok=True)

    if DB_ENGINE == "sqlite":
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    else:
        DB_USER = os.getenv("DB_USER", "")
        DB_PASSWORD = os.getenv("DB_PASSWORD", "")
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_PORT = os.getenv("DB_PORT", "")
        SQLALCHEMY_DATABASE_URI = (
            f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 📊 Plotly / BI
    ENABLE_BI = os.getenv("ENABLE_BI", "true").lower() == "true"
    PLOTLY_THEME = os.getenv("PLOTLY_THEME", "plotly_dark")

    # 🧠 Metadados
    APP_NAME = os.getenv("APP_NAME", "ESCALA360")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    AUTHOR = os.getenv("AUTHOR", "Anderson de Matos Guimarães")
    APP_DESCRIPTION = os.getenv(
        "APP_DESCRIPTION", "Sistema de gestão e visualização de escalas e produtividade"
    )

    # 🧾 Logs
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", str(BASE_DIR / "logs" / "escala360.log"))
    LOG_FORMAT = os.getenv(
        "LOG_FORMAT", "%(asctime)s - %(levelname)s - %(message)s"
    )

    # Garante diretório de logs
    Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)

    # 📬 Integrações futuras
    ENABLE_EMAIL = os.getenv("ENABLE_EMAIL", "false").lower() == "true"
    ENABLE_WHATSAPP = os.getenv("ENABLE_WHATSAPP", "false").lower() == "true"

    # ⚙️ Feature Flags
    ENABLE_AUDIT = os.getenv("ENABLE_AUDIT", "true").lower() == "true"
    ENABLE_SUBSTITUICOES = os.getenv("ENABLE_SUBSTITUICOES", "true").lower() == "true"
    ENABLE_PLANTOES = os.getenv("ENABLE_PLANTOES", "true").lower() == "true"

    # 🧱 Caminhos
    BASE_DIR = BASE_DIR
    ENV_PATH = ENV_PATH


# ---------------------------------------------
# 🔹 Auto-criação de diretórios necessários
# ---------------------------------------------
def ensure_directories():
    """Garante que diretórios de logs e banco existam."""
    Path(Config.LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    Path(Config.DB_PATH).parent.mkdir(parents=True, exist_ok=True)


ensure_directories()
