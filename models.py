"""
===========================================================
ESCALA360 - Modelos de Dados (SQLAlchemy)
Autor: Anderson de Matos Guimarães
Data: 31/10/2025
===========================================================

Descrição:
Define as entidades principais do sistema Escala360 e suas
relações, utilizando SQLAlchemy ORM. O banco padrão é SQLite,
mas o sistema é compatível com MySQL e PostgreSQL.
===========================================================
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time
from config import Config

db = SQLAlchemy()

# =========================================================
# 🧩 MODELOS PRINCIPAIS
# =========================================================
class Funcionario(db.Model):
    """Tabela de profissionais cadastrados no sistema."""
    __tablename__ = "funcionarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    cargo = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    ativo = db.Column(db.Boolean, default=True)

    escalas = db.relationship(
        "Escala", back_populates="funcionario", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Funcionario {self.nome}>"


class Turno(db.Model):
    """Tabela de turnos de trabalho (plantões disponíveis)."""
    __tablename__ = "turnos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    horario_inicio = db.Column(db.Time, nullable=False)
    horario_fim = db.Column(db.Time, nullable=False)

    escalas = db.relationship(
        "Escala", back_populates="turno", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Turno {self.nome} ({self.horario_inicio}-{self.horario_fim})>"


class Escala(db.Model):
    """Tabela principal de escalas (vínculo funcionário-turno-data)."""
    __tablename__ = "escalas"

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    funcionario_id = db.Column(db.Integer, db.ForeignKey("funcionarios.id"))
    turno_id = db.Column(db.Integer, db.ForeignKey("turnos.id"))
    status = db.Column(db.String(50), default="Ativo")

    funcionario = db.relationship("Funcionario", back_populates="escalas")
    turno = db.relationship("Turno", back_populates="escalas")
    substituicoes = db.relationship(
        "Substituicao", back_populates="escala", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Escala {self.data} - Func {self.funcionario_id} - {self.status}>"


class Substituicao(db.Model):
    """Tabela de substituições (registro de trocas de plantões)."""
    __tablename__ = "substituicoes"

    id = db.Column(db.Integer, primary_key=True)
    escala_id = db.Column(db.Integer, db.ForeignKey("escalas.id"))
    substituto_id = db.Column(db.Integer, db.ForeignKey("funcionarios.id"))
    motivo = db.Column(db.String(200))
    data_solicitacao = db.Column(db.DateTime, default=datetime.utcnow)

    escala = db.relationship("Escala", back_populates="substituicoes")
    substituto = db.relationship("Funcionario")

    def __repr__(self):
        return f"<Substituicao Func {self.substituto_id} - {self.motivo}>"

# =========================================================
# 🧱 Funções auxiliares
# =========================================================
def popular_banco_inicial(app):
    """Cria o banco e popula dados básicos na primeira execução."""
    with app.app_context():
        db.create_all()

        # Evita duplicar dados
        if not Funcionario.query.first():
            f1 = Funcionario(nome="João Silva", cargo="Técnico", email="joao@tjsp.gov.br")
            f2 = Funcionario(nome="Maria Souza", cargo="Analista", email="maria@tjsp.gov.br")
            f3 = Funcionario(nome="Carlos Lima", cargo="Supervisor", email="carlos@tjsp.gov.br")

            t1 = Turno(nome="Matutino", horario_inicio=time(7, 0), horario_fim=time(13, 0))
            t2 = Turno(nome="Vespertino", horario_inicio=time(13, 0), horario_fim=time(19, 0))
            t3 = Turno(nome="Noturno", horario_inicio=time(19, 0), horario_fim=time(23, 59))

            e1 = Escala(data=datetime(2025, 10, 26), funcionario=f1, turno=t1, status="Ativo")
            e2 = Escala(data=datetime(2025, 10, 26), funcionario=f2, turno=t2, status="Substituto")
            e3 = Escala(data=datetime(2025, 10, 26), funcionario=f3, turno=t3, status="Vago")

            db.session.add_all([f1, f2, f3, t1, t2, t3, e1, e2, e3])
            db.session.commit()
            print("✅ Banco de dados inicial populado com sucesso!")
        else:
            print("ℹ️ Banco de dados já contém registros iniciais.")


def init_app(app):
    """Inicializa o contexto do banco na aplicação Flask."""
    db.init_app(app)
    app.logger.info(f"💾 Banco de dados inicializado em {Config.DB_ENGINE.upper()} ({Config.DB_NAME})")
