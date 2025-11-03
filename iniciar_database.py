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
# ⚙️ Função 2 — Verifica se as tabelas existem
# ================================================================
def get_existing_tables(dbname, user, password, host, port):
    """Retorna a lista de tabelas já existentes no banco."""
    conn = psycopg2.connect(
        dbname=dbname, user=user, password=password, host=host, port=port
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public';
    """)
    tables = [t[0] for t in cur.fetchall()]
    cur.close()
    conn.close()
    return tables


# ================================================================
# 📊 Função 3 — Conta registros em uma tabela
# ================================================================
def count_records(dbname, user, password, host, port, table):
    """Conta o número de registros em uma tabela."""
    conn = psycopg2.connect(
        dbname=dbname, user=user, password=password, host=host, port=port
    )
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {table};")
    total = cur.fetchone()[0]
    cur.close()
    conn.close()
    return total


# ================================================================
# ⚙️ Função 4 — Executa apenas o necessário do SQL
# ================================================================
def execute_sql_file_conditionally(dbname, user, password, host, port, sql_path):
    """Executa o SQL apenas para tabelas ausentes ou vazias."""
    with open(sql_path, "r", encoding="utf-8") as f:
        sql_script = f.read()

    commands = [cmd.strip() for cmd in sql_script.split(";") if cmd.strip()]

    expected_tables = ["profissionais", "plantoes", "escalas", "substituicoes", "auditoria"]
    existing_tables = get_existing_tables(dbname, user, password, host, port)

    # Executa apenas se faltar tabela ou se alguma estiver vazia
    should_execute = False
    for table in expected_tables:
        if table not in existing_tables:
            print(f"🆕 Tabela '{table}' não existe — será criada.")
            should_execute = True
            break
        elif count_records(dbname, user, password, host, port, table) == 0:
            print(f"⚠️ Tabela '{table}' existe mas está vazia — será populada.")
            should_execute = True
            break

    if not should_execute:
        print("✅ Todas as tabelas já existem e estão populadas. Nenhuma ação necessária.")
        return

    conn = psycopg2.connect(
        dbname=dbname, user=user, password=password, host=host, port=port
    )
    cur = conn.cursor()

    for command in commands:
        try:
            cur.execute(command)
        except Exception as e:
            print(f"⚠️ Erro ao executar comando: {e}")
            print(f"Comando problemático: {command[:120]}...")

    conn.commit()
    cur.close()
    conn.close()
    print("📜 Script SQL aplicado com sucesso (apenas onde necessário).")


# ================================================================
# 📊 Função 5 — Relatório final de carga
# ================================================================
def report_table_counts(dbname, user, password, host, port):
    """Imprime a contagem final de registros em cada tabela."""
    tabelas = ["profissionais", "plantoes", "escalas", "substituicoes", "auditoria"]
    print("\n📊 Estado atual do banco de dados:")
    for tabela in tabelas:
        try:
            total = count_records(dbname, user, password, host, port, tabela)
            print(f"   {tabela:<15}: {total} registros")
        except Exception:
            print(f"   {tabela:<15}: (não existe)")
    print()


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

    # 2️⃣ Executa apenas se for preciso (tabelas faltando ou vazias)
    execute_sql_file_conditionally(db, user, pwd, host, port, sql_file)

    # 3️⃣ Mostra relatório final de status
    report_table_counts(db, user, pwd, host, port)
