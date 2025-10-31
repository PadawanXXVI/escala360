"""
===========================================================
ESCALA360 - Inicialização do Banco de Dados
Autor: Anderson de Matos Guimarães
Data: 31/10/2025
===========================================================

Descrição:
Cria o banco de dados (SQLite) com base nas definições do ORM
(models.py) e carrega o script SQL oficial (escala360.sql)
caso o banco esteja vazio.
===========================================================
"""

import os
from pathlib import Path
from sqlalchemy import text
from app import app
from models import db
from config import Config

# =========================================================
# 📁 Caminhos principais
# =========================================================
BASE_DIR = Path(__file__).resolve().parent
SQL_FILE = BASE_DIR / "escala360.sql"
DB_FILE = BASE_DIR / Config.DB_NAME

# =========================================================
# ⚙️ Função principal
# =========================================================
def init_database():
    """Cria o banco de dados e importa o script SQL se necessário."""
    with app.app_context():
        # 1️⃣ Cria o banco vazio se não existir
        if not DB_FILE.exists():
            print(f"📁 Criando banco de dados: {DB_FILE}")
            db.create_all()
            print("✅ Estrutura ORM criada com sucesso.")
        else:
            print("ℹ️ Banco já existe, verificando necessidade de importação...")

        # 2️⃣ Importa o SQL inicial (apenas se o banco estiver vazio)
        if SQL_FILE.exists():
            # Verifica se o banco já contém tabelas
            existing_tables = db.engine.table_names()
            if existing_tables:
                print("ℹ️ Banco já contém tabelas. Ignorando importação do SQL inicial.")
            else:
                print(f"📦 Importando dados de {SQL_FILE.name}...")
                with open(SQL_FILE, "r", encoding="utf-8") as f:
                    sql_script = f.read()

                # Executa com segurança (usando text() para múltiplos comandos)
                for statement in sql_script.split(";"):
                    stmt = statement.strip()
                    if stmt:
                        db.session.execute(text(stmt))

                db.session.commit()
                print("✅ Dados importados com sucesso do arquivo escala360.sql.")
        else:
            print("⚠️ Arquivo escala360.sql não encontrado. Nenhum dado inicial foi importado.")

        print("💾 Banco de dados pronto para uso.")


# =========================================================
# 🚀 Execução direta (via terminal)
# =========================================================
if __name__ == "__main__":
    init_database()
