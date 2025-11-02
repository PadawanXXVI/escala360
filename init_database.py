"""
===========================================================
ESCALA360 - Inicialização do Banco de Dados (PostgreSQL)
Autor: Anderson de Matos Guimarães
Data: 02/11/2025
===========================================================

Descrição:
Cria o banco de dados PostgreSQL com base nas definições do ORM
(models.py) e carrega o script SQL oficial (escala360.sql)
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
    Exclusivo para PostgreSQL.
    """
    with app.app_context():
        logger.info("🧩 Iniciando verificação do banco de dados PostgreSQL...")
        inspector = inspect(db.engine)

        try:
            existing_tables = inspector.get_table_names()
            if existing_tables:
                print(f"ℹ Banco já contém {len(existing_tables)} tabelas. Nenhuma criação necessária.")
                logger.info(f"Banco já contém {len(existing_tables)} tabelas. Nenhuma criação necessária.")
            else:
                print("📭 Banco de dados vazio — criando estrutura ORM...")
                db.create_all()
                logger.info("✅ Estrutura ORM criada com sucesso no PostgreSQL.")
        except OperationalError as e:
            logger.critical(f"❌ Erro de conexão com o PostgreSQL: {e}")
            raise SystemExit(f"Falha de conexão com o banco: {e}")
        except Exception as e:
            logger.critical(f"❌ Erro inesperado ao verificar tabelas: {e}")
            raise

        # ---------------------------------------------
        # 📦 Importação de dados SQL (se necessário)
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
                            logger.warning(f"⚠ Erro SQL (ignorado): {e}")
                            print(f"⚠ Erro SQL: {e}")
                        except Exception as e:
                            logger.error(f"Erro inesperado no SQL: {e}")
                            print(f"⚠ Erro inesperado no SQL: {e}")

                db.session.commit()
                print("✅ Dados importados com sucesso para o PostgreSQL.")
                logger.info("Dados importados com sucesso do arquivo escala360.sql.")
        else:
            print("⚠ Arquivo escala360.sql não encontrado. Nenhum dado inicial foi importado.")
            logger.warning("Arquivo escala360.sql não encontrado.")

        print("💾 Banco de dados PostgreSQL pronto para uso.")
        logger.info("Banco de dados PostgreSQL pronto para uso.")


# =========================================================
# 🚀 Execução direta (via terminal)
# =========================================================
if __name__ == "_main_":
    from app import app  # Import tardio para evitar import circular
    init_database(app)
