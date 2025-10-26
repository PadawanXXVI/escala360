"""
===========================================================
ESCALA360 - Modelos de Dados (SQLAlchemy)
Autor: Anderson de Matos Guimarães
Data: 26/10/2025
===========================================================

Descrição:
Define as entidades principais do sistema Escala360 e suas
relações, utilizando SQLAlchemy ORM. O banco padrão é SQLite,
mas o sistema é compatível com outros SGBDs.
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
    __tablename__ = "funcionarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    cargo = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    ativo = db.Column(db.Boolean, default=True)

    escalas = db.relationship("Escala", back_populates="funcionario", cascade="all, delete")

    def __repr__(self):
        return f"<Funcionario {self.nome}>"


class Turno(db.Model):
    __tablename__ = "turnos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    horario_inicio = db.Column(db.Time, nullable=False)
    horario_fim = db.Column(db.Time, nullable=False)

    escalas = db.relationship("Escala", back_populates="turno", cascade="all, delete")

    def __repr__(self):
        return f"<Turno {self.nome} ({self.horario_inicio}-{self.horario_fim})>"


class Escala(db.Model):
    __tablename__ = "escalas"

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    funcionario_id = db.Column(db.Integer, db.ForeignKey("funcionarios.id"))
    turno_id = db.Column(db.Integer, db.ForeignKey("turnos.id"))
    status = db.Column(db.String(50), default="Ativo")

    funcionario = db.relationship("Funcionario", back_populates="escalas")
    turno = db.relationship("Turno", back_populates="escalas")
    substituicoes = db.relationship("Substituicao", back_populates="escala", cascade="all, delete")

    def __repr__(self):
        return f"<Escala {self.data} - {self.funcionario_id} - {self.status}>"


class Substituicao(db.Model):
    __tablename__ = "substituicoes"

    id = db.Column(db.Integer, primary_key=True)
    escala_id = db.Column(db.Integer, db.ForeignKey("escalas.id"))
    substituto_id = db.Column(db.Integer, db.ForeignKey("funcionarios.id"))
    motivo = db.Column(db.String(200))
    data_solicitacao = db.Column(db.DateTime, default=datetime.utcnow)

    escala = db.relationship("Escala", back_populates="substituicoes")
    substituto = db.relationship("Funcionario")

    def __repr__(self):
        return f"<Substituicao {self.substituto_id} - {self.motivo}>"

# =========================================================
# 🧱 Função auxiliar
# =========================================================
def popular_banco_inicial(app):
    with app.app_context():
        db.create_all()

        if not Funcionario.query.first():
            f1 = Funcionario(nome="João Silva", cargo="Técnico", email="joao@tjsp.gov.br")
            f2 = Funcionario(nome="Maria Souza", cargo="Analista", email="maria@tjsp.gov.br")
            f3 = Funcionario(nome="Carlos Lima", cargo="Supervisor", email="carlos@tjsp.gov.br")

            t1 = Turno(nome="Matutino", horario_inicio=time(7, 0), horario_fim=time(13, 0))
            t2 = Turno(nome="Vespertino", horario_inicio=time(13, 0), horario_fim=time(19, 0))
            t3 = Turno(nome="Noturno", horario_inicio=time(19, 0), horario_fim=time(1, 0))

            e1 = Escala(data=datetime(2025, 10, 26), funcionario=f1, turno=t1, status="Ativo")
            e2 = Escala(data=datetime(2025, 10, 26), funcionario=f2, turno=t2, status="Substituto")
            e3 = Escala(data=datetime(2025, 10, 26), funcionario=f3, turno=t3, status="Vago")

            db.session.add_all([f1, f2, f3, t1, t2, t3, e1, e2, e3])
            db.session.commit()
            print("✅ Banco de dados inicial populado com sucesso!")
        else:
            print("ℹ️ Banco de dados já contém registros.")

# =========================================================
# ⚙️ Inicialização
# =========================================================
def init_app(app):
    db.init_app(app)
    app.logger.info("Banco de dados inicializado (SQLAlchemy).")
