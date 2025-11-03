import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
from pathlib import Path

# ================================================================
# 🧠 Função 1 — Cria o banco de dados se não existir
# ================================================================
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


# ================================================================
# ⚙️ Função 2 — Executa todas as instruções do arquivo SQL
# ================================================================
def execute_sql_file(dbname, user, password, host, port, sql_path):
    """Executa cada comando SQL do arquivo escala360.sql separadamente."""
    with open(sql_path, "r", encoding="utf-8") as f:
        sql_script = f.read()

    commands = [cmd.strip() for cmd in sql_script.split(";") if cmd.strip()]

    conn = psycopg2.connect(
        dbname=dbname, user=user, password=password, host=host, port=port
    )
    cur = conn.cursor()

    for command in commands:
        try:
            cur.execute(command)
        except Exception as e:
            print(f"⚠️ Erro ao executar comando: {e}")
            print(f"Comando problemático (início): {command[:120]}...")

    conn.commit()
    cur.close()
    conn.close()
    print("📜 Script SQL completo executado com sucesso!")


# ================================================================
# 📊 Função 3 — Verifica e imprime contagem de registros
# ================================================================
def verificar_carga(dbname, user, password, host, port):
    """Conta quantos registros existem em cada tabela principal."""
    conn = psycopg2.connect(
        dbname=dbname, user=user, password=password, host=host, port=port
    )
    cur = conn.cursor()

    tabelas = ["profissionais", "plantoes", "escalas", "substituicoes", "auditoria"]
    print("\n📊 Tabelas populadas:")

    for tabela in tabelas:
        cur.execute(f"SELECT COUNT(*) FROM {tabela};")
        total = cur.fetchone()[0]
        print(f"   {tabela}: {total} registros")

    cur.close()
    conn.close()


# ================================================================
# 🚀 Execução principal
# ================================================================
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

    # 1️⃣ Cria o banco (se necessário)
    create_database_if_not_exists(db, user, pwd, host, port)

    # 2️⃣ Executa o script SQL completo
    execute_sql_file(db, user, pwd, host, port, sql_file)

    # 3️⃣ Exibe contagem de registros nas tabelas
    verificar_carga(db, user, pwd, host, port)
