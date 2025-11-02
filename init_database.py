"""
===========================================================
ESCALA360 - Inicialização do Banco de Dados
Autor: Anderson de Matos Guimarães
Data: 31/10/2025
===========================================================

Descrição:
Cria o banco de dados (SQLite) com base nas definições do ORM
(models.py) e carrega o script SQL oficial (escala360.sql)
caso o banco esteja vazio. Registra logs automáticos.
===========================================================
"""

import os
import logging
from pathlib import Path
from sqlalchemy import text, inspect
from app import app
from models import db
from config import Config

# =========================================================
# 📁 Caminhos principais
# =========================================================
BASE_DIR = Path(__file__).resolve().parent
SQL_FILE = BASE_DIR / "escala360.sql"
DB_FILE = Path(Config.DB_PATH)
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
def init_database():
    """Cria o banco de dados e importa o script SQL se necessário."""
    with app.app_context():
        inspector = inspect(db.engine)

        # ⚠ Obter tabelas existentes só se o banco existir
        existing_tables = []
        if DB_FILE.exists():
            try:
                existing_tables = inspector.get_table_names()
            except Exception:
                existing_tables = []

        # 1️⃣ Criação inicial se o banco não existir
        if not DB_FILE.exists():
            print(f"📁 Criando banco de dados: {DB_FILE}")
            logger.info(f"Criando banco de dados: {DB_FILE}")
            db.create_all()
            print("✅ Estrutura ORM criada com sucesso.")
            logger.info("Estrutura ORM criada com sucesso.")
        else:
            print(f"ℹ Banco já existe em {DB_FILE}. Verificando necessidade de importação...")
            logger.info(f"Banco já existe em {DB_FILE}. Verificando necessidade de importação...")

        # 2️⃣ Importa o SQL inicial apenas se o banco estiver vazio
        if SQL_FILE.exists():
            if existing_tables:
                print("ℹ Banco já contém tabelas. Ignorando importação do SQL inicial.")
                logger.info("Banco já contém tabelas. Nenhuma importação realizada.")
            else:
                print(f"📦 Importando dados de {SQL_FILE.name}...")
                logger.info(f"Iniciando importação de {SQL_FILE.name}...")

                with open(SQL_FILE, "r", encoding="utf-8") as f:
                    sql_script = f.read()

                # Divide o script e executa apenas comandos válidos
                for statement in sql_script.split(";"):
                    stmt = statement.strip()
                    if stmt:
                        try:
                            db.session.execute(text(stmt))
                        except Exception as e:
                            logger.error(f"Erro ao executar comando SQL: {stmt[:80]}... → {e}")
                            print(f"⚠ Erro ao executar comando SQL: {e}")

                db.session.commit()
                print("✅ Dados importados com sucesso do arquivo escala360.sql.")
                logger.info("Dados importados com sucesso do arquivo escala360.sql.")
        else:
            print("⚠ Arquivo escala360.sql não encontrado. Nenhum dado inicial foi importado.")
            logger.warning("Arquivo escala360.sql não encontrado.")

        print("💾 Banco de dados pronto para uso.")
        logger.info("Banco de dados pronto para uso.")


# =========================================================
# 🚀 Execução direta (via terminal)
# =========================================================
if __name__ == "_main_":
    init_database()