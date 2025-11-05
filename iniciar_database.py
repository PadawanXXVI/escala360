import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
from pathlib import Path

def create_database_if_not_exists(dbname, user, password, host, port):
    """Cria o banco de dados se ainda não existir."""
    conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host, port=port)
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

def execute_sql_file(dbname, user, password, host, port, sql_file):
    """Executa o arquivo SQL de criação de tabelas."""
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    cur = conn.cursor()
    with open(sql_file, "r", encoding="utf-8") as f:
        commands = [cmd.strip() for cmd in f.read().split(";") if cmd.strip()]
    for cmd in commands:
        try:
            cur.execute(cmd)
        except Exception as e:
            print(f"⚠️ Erro em comando: {e}")
    conn.commit()
    cur.close()
    conn.close()
    print("📜 Script SQL executado com sucesso.")

if __name__ == "__main__":
    load_dotenv()

    db = os.getenv("POSTGRES_DB", "escala360")
    user = os.getenv("POSTGRES_USER", "postgres")
    pwd = os.getenv("POSTGRES_PASSWORD", "123456")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    sql_file = Path(__file__).parent / "escala360.sql"

    if not sql_file.exists():
        raise FileNotFoundError("❌ Arquivo 'escala360.sql' não encontrado na raiz.")

    create_database_if_not_exists(db, user, pwd, host, port)
    execute_sql_file(db, user, pwd, host, port, sql_file)
