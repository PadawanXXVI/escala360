from datetime import datetime
from . import db

# ==============================
# MODELOS DO BANCO ESCALA360
# ==============================


class Profissional(db.Model):
    """Tabela de profissionais cadastrados no sistema."""
    __tablename__ = "profissionais"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    cargo = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    telefone = db.Column(db.String(20))
    ativo = db.Column(db.Boolean, default=True)

    # Relacionamentos
    escalas = db.relationship("Escala", back_populates="profissional", lazy="selectin")
    solicitacoes = db.relationship(
        "Substituicao",
        foreign_keys="Substituicao.id_profissional_solicitante",
        back_populates="solicitante",
        lazy="selectin",
    )
    substituicoes = db.relationship(
        "Substituicao",
        foreign_keys="Substituicao.id_profissional_substituto",
        back_populates="substituto",
        lazy="selectin",
    )

    def __repr__(self):
        return f"<Profissional {self.id} - {self.nome}>"


class Plantao(db.Model):
    """Tabela de plantões disponíveis."""
    __tablename__ = "plantoes"

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)
    id_funcao = db.Column(db.Integer, nullable=False)
    id_local = db.Column(db.Integer, nullable=False)

    # Relacionamento reverso
    escalas = db.relationship("Escala", back_populates="plantao", lazy="selectin")

    def __repr__(self):
        return f"<Plantao {self.id} - {self.data} ({self.hora_inicio} às {self.hora_fim})>"


class Escala(db.Model):
    """Tabela que liga profissionais aos plantões (escala de trabalho)."""
    __tablename__ = "escalas"

    id = db.Column(db.Integer, primary_key=True)
    id_plantao = db.Column(db.Integer, db.ForeignKey("plantoes.id"), nullable=False)
    id_profissional = db.Column(db.Integer, db.ForeignKey("profissionais.id"), nullable=False)
    status = db.Column(db.String(50), default="ativo")
    data_alocacao = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos bidirecionais
    plantao = db.relationship("Plantao", back_populates="escalas")
    profissional = db.relationship("Profissional", back_populates="escalas")
    substituicoes = db.relationship("Substituicao", back_populates="escala_original", lazy="selectin")

    def __repr__(self):
        return f"<Escala {self.id} - Profissional {self.id_profissional} - Plantão {self.id_plantao}>"


class Substituicao(db.Model):
    """Tabela de solicitações de substituições de plantões."""
    __tablename__ = "substituicoes"

    id = db.Column(db.Integer, primary_key=True)
    id_escala_original = db.Column(db.Integer, db.ForeignKey("escalas.id"), nullable=False)
    id_profissional_solicitante = db.Column(db.Integer, db.ForeignKey("profissionais.id"), nullable=False)
    id_profissional_substituto = db.Column(db.Integer, db.ForeignKey("profissionais.id"), nullable=False)
    data_solicitacao = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="pendente")

    # Relacionamentos
    escala_original = db.relationship("Escala", back_populates="substituicoes")
    solicitante = db.relationship(
        "Profissional", foreign_keys=[id_profissional_solicitante], back_populates="solicitacoes"
    )
    substituto = db.relationship(
        "Profissional", foreign_keys=[id_profissional_substituto], back_populates="substituicoes"
    )

    def __repr__(self):
        return f"<Substituicao {self.id} - Escala {self.id_escala_original} - Status {self.status}>"


class Auditoria(db.Model):
    """Tabela de auditoria de operações (logs do sistema)."""
    __tablename__ = "auditoria"

    id = db.Column(db.Integer, primary_key=True)
    entidade = db.Column(db.String(100), nullable=False)
    id_entidade = db.Column(db.Integer, nullable=False)
    acao = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(120), nullable=False)
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Auditoria {self.entidade}#{self.id_entidade} - {self.acao}>"
