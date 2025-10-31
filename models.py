"""
===========================================================
ESCALA360 - Modelos de Dados (SQLAlchemy)
Autor: Anderson de Matos Guimarães
Data: 31/10/2025
===========================================================

Descrição:
Modelos compatíveis com o banco de dados oficial escala360.sql
fornecido pelo professor. Inclui entidades:
Profissional, Plantao, Escala, Substituicao e Auditoria.
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
    email = db.Column(db.String(120), unique=True, nullable=False)
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
    local = db.Column(db.String(100))
    funcao = db.Column(db.String(80))

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
    profissional_id = db.Column(db.Integer, db.ForeignKey("profissionais.id"), nullable=False)
    plantao_id = db.Column(db.Integer, db.ForeignKey("plantoes.id"), nullable=False)
    status = db.Column(db.String(50), default="Ativo")
    observacao = db.Column(db.String(255))
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)

    profissional = db.relationship("Profissional", back_populates="escalas")
    plantao = db.relationship("Plantao", back_populates="escalas")
    substituicoes = db.relationship("Substituicao", back_populates="escala", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Escala Prof:{self.profissional_id} - Plantao:{self.plantao_id} - {self.status}>"


# =========================================================
# 🔁 SUBSTITUIÇÕES
# =========================================================
class Substituicao(db.Model):
    """Tabela de substituições de escalas."""
    __tablename__ = "substituicoes"

    id = db.Column(db.Integer, primary_key=True)
    escala_id = db.Column(db.Integer, db.ForeignKey("escalas.id"), nullable=False)
    substituto_id = db.Column(db.Integer, db.ForeignKey("profissionais.id"), nullable=False)
    motivo = db.Column(db.String(200))
    data_solicitacao = db.Column(db.DateTime, default=datetime.utcnow)

    escala = db.relationship("Escala", back_populates="substituicoes")
    substituto = db.relationship("Profissional")

    def __repr__(self):
        return f"<Substituicao Escala:{self.escala_id} -> Substituto:{self.substituto_id}>"


# =========================================================
# 🧾 AUDITORIA
# =========================================================
class Auditoria(db.Model):
    """Tabela de registro de ações realizadas no sistema."""
    __tablename__ = "auditoria"

    id = db.Column(db.Integer, primary_key=True)
    acao = db.Column(db.String(255), nullable=False)
    usuario = db.Column(db.String(100), nullable=False)
    data_acao = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Auditoria {self.usuario}: {self.acao}>"


# =========================================================
# ⚙️ Inicialização do Banco
# =========================================================
def init_app(app):
    """Inicializa o contexto do banco na aplicação Flask."""
    db.init_app(app)
    app.logger.info(f"💾 Banco {Config.DB_NAME} ({Config.DB_ENGINE}) inicializado com sucesso.")
