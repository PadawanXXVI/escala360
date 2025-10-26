"""
==============================================
⚙️ ESCALA360 - Configuração da Aplicação Flask
==============================================

Este módulo centraliza todas as configurações da aplicação,
carregando variáveis do arquivo .env e definindo parâmetros
para o ambiente, banco de dados, logs e integrações futuras.

Autor: Anderson de Matos Guimarães
Versão: 1.0.0
Data: 2025-10-26
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ---------------------------------------------
# 🔹 Carregamento do .env
# ---------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env", override=True)

# ---------------------------------------------
# 🔹 Classe principal de configuração
# ---------------------------------------------
class Config:
    """Configurações principais da aplicação ESCALA360."""

    # 🌐 Configurações do Flask
    FLASK_APP = os.getenv("FLASK_APP", "app.py")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "changeme123")

    # 🌎 Servidor
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))

    # 💾 Banco de Dados
    DB_ENGINE = os.getenv("DB_ENGINE", "sqlite")
    DB_NAME = os.getenv("DB_NAME", "escala360.db")

    if DB_ENGINE == "sqlite":
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / DB_NAME}"
    else:
        DB_USER = os.getenv("DB_USER", "")
        DB_PASSWORD = os.getenv("DB_PASSWORD", "")
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_PORT = os.getenv("DB_PORT", "3306")
        SQLALCHEMY_DATABASE_URI = (
            f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 📊 Configurações do BI
    ENABLE_BI = os.getenv("ENABLE_BI", "true").lower() == "true"
    PLOTLY_THEME = os.getenv("PLOTLY_THEME", "plotly_dark")

    # 🧠 Metadados
    APP_NAME = os.getenv("APP_NAME", "ESCALA360")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    AUTHOR = os.getenv("AUTHOR", "Anderson de Matos Guimarães")

    # 🧾 Logs
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", str(BASE_DIR / "logs" / "escala360.log"))

    # 📬 Integrações (futuro)
    ENABLE_EMAIL = os.getenv("ENABLE_EMAIL", "false").lower() == "true"
    ENABLE_WHATSAPP = os.getenv("ENABLE_WHATSAPP", "false").lower() == "true"

    # 🧱 Caminhos
    BASE_DIR = BASE_DIR


# ---------------------------------------------
# 🔹 Configuração de log (auto-criação do diretório)
# ---------------------------------------------
def ensure_log_dir():
    """Garante que o diretório de logs exista."""
    log_dir = Path(Config.LOG_FILE).parent
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)


ensure_log_dir()
