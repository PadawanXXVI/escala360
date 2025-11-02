"""
===========================================================
ESCALA360 - Modelos de Dados (SQLAlchemy)
Autor: Anderson de Matos Guimarães
Data: 31/10/2025
===========================================================

Descrição:
Modelos 100% compatíveis com o banco oficial escala360.sql.
Define as entidades: Profissional, Plantao, Escala,
Substituicao e Auditoria.
===========================================================
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import Config

db = SQLAlchemy()

# =========================================================
# 👥 PROFISSIONAIS
# =========================================================
class Profissional(db.Model):
    """Tabela de profissionais cadastrados."""
    __tablename__ = "profissionais"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    cargo = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    telefone = db.Column(db.String(20))
    ativo = db.Column(db.Boolean, default=True)

    escalas = db.relationship("Escala", back_populates="profissional", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Profissional {self.nome}>"


# =========================================================
# 🕒 PLANTÕES
# =========================================================
class Plantao(db.Model):
    """Tabela de plantões disponíveis (equivalente aos turnos)."""
    __tablename__ = "plantoes"

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)
    id_funcao = db.Column(db.Integer)
    id_local = db.Column(db.Integer)

    escalas = db.relationship("Escala", back_populates="plantao", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Plantao {self.data} ({self.hora_inicio}-{self.hora_fim})>"


# =========================================================
# 📅 ESCALAS
# =========================================================
class Escala(db.Model):
    """Tabela principal: vínculo entre profissional e plantão."""
    __tablename__ = "escalas"

    id = db.Column(db.Integer, primary_key=True)
    id_profissional = db.Column(
        db.Integer, db.ForeignKey("profissionais.id", ondelete="CASCADE"), nullable=False
    )
    id_plantao = db.Column(
        db.Integer, db.ForeignKey("plantoes.id", ondelete="CASCADE"), nullable=False
    )
    status = db.Column(db.String(50), default="Ativo")
    observacao = db.Column(db.String(255))
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)

    profissional = db.relationship("Profissional", back_populates="escalas")
    plantao = db.relationship("Plantao", back_populates="escalas")
    substituicoes = db.relationship("Substituicao", back_populates="escala", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Escala Prof:{self.id_profissional} - Plantao:{self.id_plantao} - {self.status}>"


# =========================================================
# 🔁 SUBSTITUIÇÕES
# =========================================================
class Substituicao(db.Model):
    """Tabela de substituições de escalas."""
    __tablename__ = "substituicoes"

    id = db.Column(db.Integer, primary_key=True)
    id_escala_original = db.Column(
        db.Integer,
        db.ForeignKey("escalas.id", ondelete="CASCADE"),
        nullable=False
    )
    id_profissional_solicitante = db.Column(
        db.Integer,
        db.ForeignKey("profissionais.id", ondelete="CASCADE"),
        nullable=False
    )
    id_profissional_substituto = db.Column(
        db.Integer,
        db.ForeignKey("profissionais.id", ondelete="CASCADE"),
        nullable=False
    )
    status = db.Column(db.String(50), default="pendente")
    data_solicitacao = db.Column(db.DateTime, default=datetime.utcnow)
    motivo = db.Column(db.String(200))

    escala = db.relationship("Escala", back_populates="substituicoes", foreign_keys=[id_escala_original])
    solicitante = db.relationship("Profissional", foreign_keys=[id_profissional_solicitante])
    substituto = db.relationship("Profissional", foreign_keys=[id_profissional_substituto])

    def __repr__(self):
        return f"<Substituicao Escala:{self.id_escala_original} Subst:{self.id_profissional_substituto}>"


# =========================================================
# 🧾 AUDITORIA
# =========================================================
class Auditoria(db.Model):
    """Tabela de registro de ações realizadas no sistema."""
    __tablename__ = "auditoria"

    id = db.Column(db.Integer, primary_key=True)
    entidade = db.Column(db.String(50), nullable=False)
    id_entidade = db.Column(db.Integer, nullable=False)
    acao = db.Column(db.String(255), nullable=False)
    usuario = db.Column(db.String(100), nullable=False)
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Auditoria {self.entidade}:{self.id_entidade} ({self.acao})>"


# =========================================================
# ⚙️ Inicialização do Banco
# =========================================================
def init_app(app):
    """Inicializa o contexto do banco na aplicação Flask."""
    db.init_app(app)
    app.logger.info(f"💾 Banco {Config.DB_NAME} ({Config.DB_ENGINE}) inicializado com sucesso.")
