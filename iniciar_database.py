import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
from pathlib import Path

# -------------------------
# Função 1 - Criação do banco
# -------------------------
def create_database_if_not_exists(dbname, user, password, host, port):
    """Cria o banco de dados se ainda não existir."""
    conn = psycopg2.connect(
        dbname="postgres", user=user, password=password, host=host, port=port
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (dbname,))
    exists = cur.fetchone()
    if not exists:
        cur.execute(f'CREATE DATABASE "{dbname}"')
        print(f"✅ Banco '{dbname}' criado com sucesso.")
    else:
        print(f"ℹ️ Banco '{dbname}' já existe.")
    cur.close()
    conn.close()

# -------------------------
# Função 2 - Checagem de tabelas existentes
# -------------------------
def get_existing_tables(dbname, user, password, host, port):
    """Retorna uma lista com os nomes das tabelas já existentes no banco."""
    conn = psycopg2.connect(
        dbname=dbname, user=user, password=password, host=host, port=port
    )
    cur = conn.cursor()
    cur.execute(
        """
        SELECT table_name 
        FROM information_schema.tables
        WHERE table_schema = 'public';
        """
    )
    tables = [t[0] for t in cur.fetchall()]
    cur.close()
    conn.close()
    return tables

# -------------------------
# Função 3 - Execução condicional do SQL
# -------------------------
def execute_sql_if_missing(dbname, user, password, host, port, sql_path):
    """Executa apenas as partes do SQL que ainda não existem no banco."""
    with open(sql_path, "r", encoding="utf-8") as f:
        sql_script = f.read()

    # Tabelas principais esperadas
    expected_tables = ["profissionais", "plantoes", "escalas", "substituicoes", "auditoria"]
    existing_tables = get_existing_tables(dbname, user, password, host, port)

    missing_tables = [t for t in expected_tables if t not in existing_tables]
    if not missing_tables:
        print("✅ Todas as tabelas principais já existem. Nenhuma ação necessária.")
        return

    print(f"⚙️ Criando tabelas ausentes: {', '.join(missing_tables)}")

    conn = psycopg2.connect(
        dbname=dbname, user=user, password=password, host=host, port=port
    )
    cur = conn.cursor()
    cur.execute("BEGIN;")

    # Divide o script em blocos para executar seletivamente
    statements = [stmt.strip() for stmt in sql_script.split(";") if stmt.strip()]
    for stmt in statements:
        for table in missing_tables:
            if table in stmt.lower():
                try:
                    cur.execute(stmt + ";")
                    print(f"🆕 Tabela '{table}' criada.")
                except Exception as e:
                    print(f"⚠️ Erro ao criar '{table}': {e}")
                break

    conn.commit()
    cur.close()
    conn.close()
    print("📜 Criação de tabelas ausentes concluída com sucesso.")

# -------------------------
# Execução principal
# -------------------------
if __name__ == "__main__":
    load_dotenv()

    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "escala360")
    user = os.getenv("POSTGRES_USER", "postgres")
    pwd = os.getenv("POSTGRES_PASSWORD", "123456")

    sql_file = Path(__file__).parent / "escala360.sql"
    if not sql_file.exists():
        raise FileNotFoundError("❌ Arquivo escala360.sql não encontrado na raiz do projeto.")

    create_database_if_not_exists(db, user, pwd, host, port)
    execute_sql_if_missing(db, user, pwd, host, port, sql_file)
