"""
===========================================================
ESCALA360 - Blueprint: Substituições
Autor: Anderson de Matos Guimarães
Data: 02/11/2025
===========================================================

Descrição:
Gerencia as substituições entre profissionais em plantões,
permitindo registrar, editar e excluir substituições.

Compatível com substituicoes.html (formulário e tabela).

Base de dados: Tabela 'substituicoes' (ver escala360.sql)
Campos:
- id, id_escala_original, id_profissional_solicitante,
  id_profissional_substituto, status, data_solicitacao, motivo
===========================================================
"""

from flask import Blueprint, jsonify, request, render_template, current_app
from models import db, Substituicao, Escala, Profissional, Plantao
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

substituicoes_bp = Blueprint("substituicoes_bp", __name__, url_prefix="/substituicoes")

# =========================================================
# 🧩 Página principal
# =========================================================
@substituicoes_bp.route("/")
def view_substituicoes():
    """Renderiza a página de gestão de substituições."""
    profissionais = Profissional.query.filter_by(ativo=True).order_by(Profissional.nome.asc()).all()
    current_app.logger.info("🔄 Acesso à página de Substituições.")
    return render_template(
        "substituicoes.html",
        title="Gestão de Substituições",
        profissionais=profissionais,
    )


# =========================================================
# 📋 Listar Substituições (GET)
# =========================================================
@substituicoes_bp.get("/api")
def listar_substituicoes():
    """Lista todas as substituições com JOIN de escala, profissional e plantão."""
    try:
        substituicoes = (
            db.session.query(Substituicao, Escala, Profissional, Plantao)
            .join(Escala, Substituicao.id_escala_original == Escala.id)
            .join(Profissional, Substituicao.id_profissional_substituto == Profissional.id)
            .join(Plantao, Escala.id_plantao == Plantao.id)
            .order_by(Substituicao.data_solicitacao.desc())
            .all()
        )

        data = [
            {
                "id": s.id,
                "data_solicitacao": s.data_solicitacao.strftime("%Y-%m-%d %H:%M"),
                "profissional_solicitante": Profissional.query.get(s.id_profissional_solicitante).nome,
                "profissional_substituto": p.nome,
                "data_plantao": pl.data.strftime("%Y-%m-%d"),
                "hora_inicio": pl.hora_inicio.strftime("%H:%M"),
                "hora_fim": pl.hora_fim.strftime("%H:%M"),
                "status": s.status,
                "motivo": s.motivo or "-",
            }
            for s, e, p, pl in substituicoes
        ]

        current_app.logger.info(f"📋 {len(data)} substituições listadas.")
        return jsonify(data), 200

    except SQLAlchemyError as e:
        current_app.logger.error(f"❌ Erro ao listar substituições: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================================================
# 🆕 Criar Substituição (POST)
# =========================================================
@substituicoes_bp.post("/api")
def criar_substituicao():
    """Registra uma nova substituição."""
    payload = request.get_json(silent=True) or {}
    try:
        id_escala = payload.get("id_escala_original")
        id_solicitante = payload.get("id_profissional_solicitante")
        id_substituto = payload.get("id_profissional_substituto")
        motivo = payload.get("motivo", "")
        status = payload.get("status", "pendente")

        if not all([id_escala, id_solicitante, id_substituto]):
            return jsonify({"ok": False, "error": "Campos obrigatórios ausentes."}), 400

        nova_sub = Substituicao(
            id_escala_original=id_escala,
            id_profissional_solicitante=id_solicitante,
            id_profissional_substituto=id_substituto,
            motivo=motivo,
            status=status,
            data_solicitacao=datetime.utcnow(),
        )

        db.session.add(nova_sub)
        db.session.commit()
        current_app.logger.info(f"✅ Substituição criada: {nova_sub.id}")
        return jsonify({"ok": True, "id": nova_sub.id}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"❌ Erro ao criar substituição: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================================================
# ✏️ Atualizar Substituição (PUT)
# =========================================================
@substituicoes_bp.put("/api/<int:id>")
def atualizar_substituicao(id):
    """Atualiza uma substituição existente."""
    payload = request.get_json(silent=True) or {}
    try:
        sub = Substituicao.query.get_or_404(id)

        if "id_profissional_solicitante" in payload:
            sub.id_profissional_solicitante = payload["id_profissional_solicitante"]
        if "id_profissional_substituto" in payload:
            sub.id_profissional_substituto = payload["id_profissional_substituto"]
        if "status" in payload:
            sub.status = payload["status"]
        if "motivo" in payload:
            sub.motivo = payload["motivo"]

        db.session.commit()
        current_app.logger.info(f"✏️ Substituição {id} atualizada com sucesso.")
        return jsonify({"ok": True, "message": "Substituição atualizada."}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"❌ Erro ao atualizar substituição {id}: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================================================
# 🗑️ Excluir Substituição (DELETE)
# =========================================================
@substituicoes_bp.delete("/api/<int:id>")
def excluir_substituicao(id):
    """Remove uma substituição pelo ID."""
    try:
        sub = Substituicao.query.get_or_404(id)
        db.session.delete(sub)
        db.session.commit()
        current_app.logger.warning(f"🗑️ Substituição removida: {id}")
        return jsonify({"ok": True, "message": "Substituição excluída com sucesso."}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"❌ Erro ao excluir substituição {id}: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500
