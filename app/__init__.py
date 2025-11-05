import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text
from dotenv import load_dotenv

# ============================================================
# 🔹 Instâncias globais
# ============================================================
db = SQLAlchemy()
migrate = Migrate()


# ============================================================
# 🔹 Fábrica da aplicação Flask
# ============================================================
def create_app():
    """Cria e configura a aplicação Flask Escala360."""
    load_dotenv()

    app = Flask(__name__)

    # -----------------------------
    # Configurações principais
    # -----------------------------
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev_secret")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = os.getenv("SQLALCHEMY_ECHO", "False") == "True"

    # -----------------------------
    # Configuração do PostgreSQL (Neon)
    # -----------------------------
    pg_user = os.getenv("POSTGRES_USER", "neondb_owner")
    pg_pwd = os.getenv("POSTGRES_PASSWORD", "")
    pg_host = os.getenv("POSTGRES_HOST", "localhost")
    pg_port = os.getenv("POSTGRES_PORT", "5432")
    pg_db = os.getenv("POSTGRES_DB", "escala360")

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql+psycopg2://{pg_user}:{pg_pwd}@{pg_host}:{pg_port}/{pg_db}"
    )

    # -----------------------------
    # Inicialização das extensões
    # -----------------------------
    db.init_app(app)
    migrate.init_app(app, db)

    # Teste de conexão diferido (dentro do contexto)
    with app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
            print("✅ Conexão com o banco Neon estabelecida com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao conectar ao banco Neon: {e}")

    # -----------------------------
    # Importa os modelos e rotas
    # -----------------------------
    from . import models  # noqa: F401
    from .routes.profissionais import bp as profissionais_bp
    from .routes.plantoes import bp as plantoes_bp
    from .routes.escalas import bp as escalas_bp
    from .routes.substituicoes import bp as substituicoes_bp
    from .routes.api import bp as api_bp

    app.register_blueprint(profissionais_bp, url_prefix="/profissionais")
    app.register_blueprint(plantoes_bp, url_prefix="/plantoes")
    app.register_blueprint(escalas_bp, url_prefix="/escalas")
    app.register_blueprint(substituicoes_bp, url_prefix="/substituicoes")
    app.register_blueprint(api_bp, url_prefix="/api")

    # -----------------------------
    # Rota principal (Painel BI)
    # -----------------------------
    @app.route("/")
    def index():
        """Página inicial (Painel BI - Fase 6)."""
        try:
            q1 = text(
                """
                SELECT p.nome, COUNT(e.id) AS total_plantoes
                FROM profissionais p
                LEFT JOIN escalas e ON e.id_profissional = p.id
                GROUP BY p.nome
                ORDER BY total_plantoes DESC
                """
            )

            q2 = text(
                """
                SELECT status, COUNT(*) AS total
                FROM substituicoes
                GROUP BY status
                ORDER BY total DESC
                """
            )

            q3 = text(
                """
                SELECT data::date AS dia, COUNT(*) AS total
                FROM plantoes
                GROUP BY dia
                ORDER BY dia
                """
            )

            r1 = db.session.execute(q1).mappings().all()
            r2 = db.session.execute(q2).mappings().all()
            r3 = db.session.execute(q3).mappings().all()

            # Converte resultados
            carga_labels = [row["nome"] for row in r1]
            carga_values = [int(row["total_plantoes"] or 0) for row in r1]

            pizza_labels = [row["status"] for row in r2]
            pizza_values = [int(row["total"] or 0) for row in r2]

            linha_labels = [row["dia"].isoformat() for row in r3]
            linha_values = [int(row["total"] or 0) for row in r3]

            return render_template(
                "index.html",
                carga_labels=carga_labels,
                carga_values=carga_values,
                pizza_labels=pizza_labels,
                pizza_values=pizza_values,
                linha_labels=linha_labels,
                linha_values=linha_values,
            )

        except Exception as e:
            print(f"❌ Erro ao renderizar index(): {e}")
            return render_template("erro.html", erro=str(e)), 500

    return app