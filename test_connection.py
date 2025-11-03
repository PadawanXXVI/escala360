# ============================================================
# Script de Teste de Conexão com Banco de Dados (Neon)
# ============================================================
# Verifica se a aplicação Flask conecta corretamente
# ao PostgreSQL remoto (Neon) usando SQLAlchemy.
# ============================================================

import sys
from sqlalchemy import text
from app import create_app, db

def test_database_connection():
    """Testa a conexão com o banco de dados configurado no .env."""
    app = create_app()

    with app.app_context():
        print("Testando conexão com o banco de dados...")

        try:
            # Teste simples de consulta de versão
            result = db.session.execute(text("SELECT version();"))
            version = result.fetchone()[0]

            print("Conexão com o banco Neon estabelecida com sucesso!")
            print(f"Versão do PostgreSQL: {version}")
            print("--------------------------------------------------")

            # (Opcional) Teste de criação de tabelas
            try:
                db.create_all()
                print("Tabelas verificadas/criadas com sucesso!")
            except Exception as table_error:
                print("Aviso: erro ao criar tabelas:", table_error)

        except Exception as conn_error:
            print("Erro ao conectar ao banco de dados:")
            print(conn_error)
            sys.exit(1)

        finally:
            db.session.close()
            print("Sessão encerrada.")

if __name__ == "__main__":
    test_database_connection()
