"""
===========================================================
ESCALA360 - Inicialização do Banco de Dados (PostgreSQL ou SQLite)
Autor: Anderson de Matos Guimarães
Data: 02/11/2025
===========================================================

Descrição:
Cria o banco de dados (PostgreSQL ou SQLite) com base nas definições
do ORM (models.py) e carrega o script SQL oficial (escala360.sql)
caso o banco esteja vazio. Registra logs automáticos.
===========================================================
"""

import os
import logging
from pathlib import Path
from sqlalchemy import text, inspect
from sqlalchemy.exc import OperationalError, ProgrammingError
from models import db
from config import Config

# =========================================================
# 📁 Caminhos principais
# =========================================================
BASE_DIR = Path(__file__).resolve().parent
SQL_FILE = BASE_DIR / "escala360.sql"

# Define o caminho do banco (somente usado no SQLite)
if Config.DB_ENGINE == "sqlite":
    DB_FILE = Path(getattr(Config, "DB_PATH", BASE_DIR / "instance" / "escala360.db"))
else:
    # PostgreSQL não tem arquivo físico, mas mantemos para log
    DB_FILE = Path(BASE_DIR / f"{Config.DB_NAME}.db")

LOG_FILE = Path(Config.LOG_FILE)

# =========================================================
# 🧾 Logging
# =========================================================
os.makedirs(LOG_FILE.parent, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)
logger = logging.getLogger(__name__)

# =========================================================
# ⚙ Função principal
# =========================================================
def init_database(app):
    """
    Cria o banco de dados e importa o script SQL inicial, se necessário.
    Compatível com PostgreSQL e SQLite.
    """
    with app.app_context():
        engine = db.engine
        inspector = inspect(engine)
        logger.info(f"🧩 Iniciando verificação do banco ({Config.DB_ENGINE})...")

        # Verifica se há tabelas existentes
        existing_tables = []
        try:
            existing_tables = inspector.get_table_names()
            if existing_tables:
                logger.info(f"🔍 Banco já contém {len(existing_tables)} tabelas.")
            else:
                logger.info("📭 Banco de dados vazio — iniciando criação de tabelas.")
        except Exception as e:
            logger.warning(f"⚠ Falha ao inspecionar tabelas: {e}")

        # ---------------------------------------------
        # 🏗 Criação das tabelas via ORM
        # ---------------------------------------------
        try:
            db.create_all()
            print(f"✅ Estrutura ORM criada/verificada com sucesso ({Config.DB_ENGINE}).")
            logger.info("✅ Estrutura ORM criada/verificada com sucesso.")
        except Exception as e:
            logger.critical(f"❌ Erro crítico ao criar tabelas: {e}")
            raise

        # ---------------------------------------------
        # 📦 Importação de dados do arquivo escala360.sql
        # ---------------------------------------------
        if SQL_FILE.exists():
            if existing_tables:
                print("ℹ Banco já contém tabelas. Ignorando importação do SQL inicial.")
                logger.info("Banco já contém tabelas. Nenhuma importação realizada.")
            else:
                print(f"📦 Importando dados de {SQL_FILE.name}...")
                logger.info(f"Iniciando importação de {SQL_FILE.name}...")

                with open(SQL_FILE, "r", encoding="utf-8") as f:
                    sql_script = f.read()

                for statement in sql_script.split(";"):
                    stmt = statement.strip()
                    if stmt:
                        try:
                            db.session.execute(text(stmt))
                        except (OperationalError, ProgrammingError) as e:
                            logger.error(f"Erro SQL (ignorado): {stmt[:120]}... → {e}")
                            print(f"⚠ Erro ao executar SQL: {e}")
                        except Exception as e:
                            logger.error(f"Erro inesperado no SQL: {stmt[:120]}... → {e}")

                db.session.commit()
                print(f"✅ Dados importados com sucesso de {SQL_FILE.name}.")
                logger.info("✅ Dados importados com sucesso.")
        else:
            print("⚠ Arquivo escala360.sql não encontrado. Nenhum dado inicial foi importado.")
            logger.warning("Arquivo escala360.sql não encontrado.")

        print(f"💾 Banco de dados {Config.DB_ENGINE.upper()} pronto para uso.")
        logger.info(f"Banco de dados {Config.DB_ENGINE.upper()} pronto para uso.")

# =========================================================
# 🚀 Execução direta (via terminal)
# =========================================================
if __name__ == "_main_":
    from app import app  # Import tardio para evitar import circular
    init_database(app)
