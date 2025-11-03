# ============================================================
# 🌐 Módulo de Rotas — API REST
# ============================================================
# Este módulo implementa a API REST do Escala360,
# oferecendo endpoints para substituições e notificações.
# ============================================================

from flask import Blueprint, jsonify, request
from .. import db
from ..models import Substituicao

# Criação do Blueprint
bp = Blueprint("api", __name__)

# ------------------------------------------------------------
# 🔹 GET /api/substituicoes
# ------------------------------------------------------------
@bp.get("/substituicoes")
def listar_substituicoes():
    """Retorna as substituições pendentes em formato JSON."""
    pendentes = Substituicao.query.filter_by(status="pendente").all()
    data = [
        {
            "id": s.id,
            "id_escala": s.id_escala_original,
            "solicitante": s.id_profissional_solicitante,
            "substituto": s.id_profissional_substituto,
            "status": s.status,
            "data_solicitacao": s.data_solicitacao.isoformat(),
        }
        for s in pendentes
    ]
    return jsonify(data), 200


# ------------------------------------------------------------
# 🔹 POST /api/substituicoes
# ------------------------------------------------------------
@bp.post("/substituicoes")
def criar_substituicao():
    """Cria uma nova solicitação de substituição."""
    payload = request.get_json(force=True)

    nova_sub = Substituicao(
        id_escala_original=payload["id_escala_original"],
        id_profissional_solicitante=payload["id_profissional_solicitante"],
        id_profissional_substituto=payload["id_profissional_substituto"],
        status=payload.get("status", "pendente"),
    )

    db.session.add(nova_sub)
    db.session.commit()

    return jsonify({"message": "Substituição criada", "id": nova_sub.id}), 201


# ------------------------------------------------------------
# 🔹 POST /api/notificacoes/email
# ------------------------------------------------------------
@bp.post("/notificacoes/email")
def enviar_email():
    """Simula o envio de notificação por e-mail."""
    data = request.get_json(force=True)
    destinatario = data.get("to")
    assunto = data.get("subject", "Notificação Escala360")
    print(f"[📧 E-mail Simulado] Para: {destinatario} | Assunto: {assunto}")
    return jsonify({"message": "E-mail simulado enviado com sucesso", "to": destinatario}), 202


# ------------------------------------------------------------
# 🔹 POST /api/notificacoes/whatsapp
# ------------------------------------------------------------
@bp.post("/notificacoes/whatsapp")
def enviar_whatsapp():
    """Simula o envio de mensagem WhatsApp."""
    data = request.get_json(force=True)
    destinatario = data.get("to")
    mensagem = data.get("mensagem", "Mensagem automática Escala360")
    print(f"[💬 WhatsApp Simulado] Para: {destinatario} | Mensagem: {mensagem}")
    return jsonify({"message": "WhatsApp simulado enviado com sucesso", "to": destinatario}), 202
