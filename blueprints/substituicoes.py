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
- id, titular_id, substituto_id, plantao_id, data
===========================================================
"""

from flask import Blueprint, jsonify, request, render_template, current_app
from models import db, Substituicao, Profissional, Plantao
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

substituicoes_bp = Blueprint("substituicoes_bp", __name__, url_prefix="/substituicoes")


# =========================================================
# 🧩 Página principal
# =========================================================
@substituicoes_bp.route("/")
def view_substituicoes():
    """Renderiza a página de gestão de substituições."""
    current_app.logger.info("🔄 Acesso à página de Substituições.")
    return render_template("substituicoes.html", title="Gestão de Substituições")


# =========================================================
# 📋 Listar Substituições (GET)
# =========================================================
@substituicoes_bp.get("/api")
def listar_substituicoes():
    """Lista todas as substituições com dados descritivos (JOINs)."""
    try:
        substituicoes = (
            db.session.query(Substituicao, Profissional, Plantao)
            .join(Profissional, Profissional.id == Substituicao.titular_id)
            .join(Plantao, Plantao.id == Substituicao.plantao_id)
            .order_by(Substituicao.data.desc())
            .all()
        )

        data = [
            {
                "id": s.Substituicao.id,
                "data": s.Substituicao.data.strftime("%Y-%m-%d"),
                "plantao_id": s.Substituicao.plantao_id,
                "plantao": s.Plantao.nome,
                "titular_id": s.Substituicao.titular_id,
                "titular": s.Profissional.nome,
                "substituto_id": s.Substituicao.substituto_id,
                "substituto": Profissional.query.get(s.Substituicao.substituto_id).nome
                if s.Substituicao.substituto_id
                else "",
            }
            for s in substituicoes
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
        titular_id = payload.get("titular_id")
        substituto_id = payload.get("substituto_id")
        plantao_id = payload.get("plantao_id")
        data_str = payload.get("data")

        if not all([titular_id, substituto_id, plantao_id, data_str]):
            return jsonify({"ok": False, "error": "Campos obrigatórios ausentes."}), 400

        data = datetime.strptime(data_str, "%Y-%m-%d").date()

        nova_sub = Substituicao(
            titular_id=titular_id,
            substituto_id=substituto_id,
            plantao_id=plantao_id,
            data=data,
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

        if "titular_id" in payload:
            sub.titular_id = payload["titular_id"]
        if "substituto_id" in payload:
            sub.substituto_id = payload["substituto_id"]
        if "plantao_id" in payload:
            sub.plantao_id = payload["plantao_id"]
        if "data" in payload:
            sub.data = datetime.strptime(payload["data"], "%Y-%m-%d").date()

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
