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

from app import app
from models import db
from config import Config
from pathlib import Path
import os

# Caminhos
BASE_DIR = Path(__file__).resolve().parent
SQL_FILE = BASE_DIR / "escala360.sql"
DB_FILE = BASE_DIR / Config.DB_NAME

def init_database():
    """Cria o banco e importa o conteúdo SQL se necessário."""
    with app.app_context():
        # 1️⃣ Cria o banco vazio se não existir
        if not DB_FILE.exists():
            print(f"📁 Criando banco de dados: {DB_FILE}")
            db.create_all()
            print("✅ Estrutura ORM criada com sucesso.")
        else:
            print("ℹ️ Banco já existe, verificando conteúdo...")

        # 2️⃣ Importa o SQL inicial (se existir)
        if SQL_FILE.exists():
            print(f"📦 Importando dados de {SQL_FILE.name}...")
            with open(SQL_FILE, "r", encoding="utf-8") as f:
                sql_script = f.read()
                db.session.execute(sql_script)
                db.session.commit()
            print("✅ Dados importados com sucesso do arquivo escala360.sql.")
        else:
            print("⚠️ Arquivo escala360.sql não encontrado. Nenhum dado inicial foi importado.")

        print("💾 Banco pronto para uso.")


if __name__ == "__main__":
    init_database()
