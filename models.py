"""
===========================================================
ESCALA360 - Modelos ORM (SQLAlchemy)
Autor: Anderson de Matos Guimarães
Data: 02/11/2025
===========================================================

Descrição:
Mapeia as tabelas do banco de dados PostgreSQL utilizando SQLAlchemy.
O schema reflete exatamente a estrutura definida no arquivo escala360.sql.
===========================================================
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Instância global do SQLAlchemy
db = SQLAlchemy()


# =========================================================
# 🔧 Inicializador do ORM
# =========================================================
def init_app(app):
    """Inicializa o SQLAlchemy com o contexto Flask."""
    db.init_app(app)
    with app.app_context():
        db.create_all()


# =========================================================
# 👩‍⚕ Modelo: Profissional
# =========================================================
class Profissional(db.Model):
    __tablename__ = "profissionais"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cargo = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(20))
    ativo = db.Column(db.Boolean, default=True)

    # Relacionamentos
    escalas = db.relationship("Escala", back_populates="profissional", lazy=True)
    substituicoes_solicitadas = db.relationship(
        "Substituicao",
        foreign_keys="Substituicao.id_profissional_solicitante",
        back_populates="profissional_solicitante",
        lazy=True,
    )
    substituicoes_substituto = db.relationship(
        "Substituicao",
        foreign_keys="Substituicao.id_profissional_substituto",
        back_populates="profissional_substituto",
        lazy=True,
    )

    def _repr_(self):
        return f"<Profissional {self.nome} ({'ativo' if self.ativo else 'inativo'})>"


# =========================================================
# 🕒 Modelo: Plantão
# =========================================================
class Plantao(db.Model):
    __tablename__ = "plantoes"

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)
    id_funcao = db.Column(db.Integer, nullable=False)
    id_local = db.Column(db.Integer, nullable=False)

    # Relacionamentos
    escalas = db.relationship("Escala", back_populates="plantao", lazy=True)

    def _repr_(self):
        return f"<Plantão {self.data} {self.hora_inicio}-{self.hora_fim}>"


# =========================================================
# 📅 Modelo: Escala
# =========================================================
class Escala(db.Model):
    __tablename__ = "escalas"

    id = db.Column(db.Integer, primary_key=True)
    id_plantao = db.Column(db.Integer, db.ForeignKey("plantoes.id"), nullable=False)
    id_profissional = db.Column(db.Integer, db.ForeignKey("profissionais.id"), nullable=False)
    status = db.Column(db.String(50), default="ativo")
    data_alocacao = db.Column(db.DateTime, default=datetime.now)

    # Relacionamentos
    plantao = db.relationship("Plantao", back_populates="escalas")
    profissional = db.relationship("Profissional", back_populates="escalas")
    substituicoes = db.relationship("Substituicao", back_populates="escala", lazy=True)

    def _repr_(self):
        return f"<Escala Plantão={self.id_plantao}, Profissional={self.id_profissional}, Status={self.status}>"


# =========================================================
# 🔁 Modelo: Substituição
# =========================================================
class Substituicao(db.Model):
    __tablename__ = "substituicoes"

    id = db.Column(db.Integer, primary_key=True)
    id_escala_original = db.Column(db.Integer, db.ForeignKey("escalas.id"), nullable=False)
    id_profissional_solicitante = db.Column(db.Integer, db.ForeignKey("profissionais.id"), nullable=False)
    id_profissional_substituto = db.Column(db.Integer, db.ForeignKey("profissionais.id"), nullable=False)
    data_solicitacao = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(50), default="pendente")

    # Relacionamentos
    escala = db.relationship("Escala", back_populates="substituicoes")
    profissional_solicitante = db.relationship(
        "Profissional",
        foreign_keys=[id_profissional_solicitante],
        back_populates="substituicoes_solicitadas",
    )
    profissional_substituto = db.relationship(
        "Profissional",
        foreign_keys=[id_profissional_substituto],
        back_populates="substituicoes_substituto",
    )

    def _repr_(self):
        return f"<Substituição Escala={self.id_escala_original}, Status={self.status}>"


# =========================================================
# 🧾 Modelo: Auditoria
# =========================================================
class Auditoria(db.Model):
    __tablename__ = "auditoria"

    id = db.Column(db.Integer, primary_key=True)
    entidade = db.Column(db.String(100), nullable=False)
    id_entidade = db.Column(db.Integer, nullable=False)
    acao = db.Column(db.String(50), nullable=False)
    usuario = db.Column(db.String(100), nullable=False)
    data_hora = db.Column(db.DateTime, default=datetime.now)

    def _repr_(self):
        return f"<Auditoria {self.entidade} {self.acao} por {self.usuario}>"
    