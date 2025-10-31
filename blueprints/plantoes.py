"""
===========================================================
ESCALA360 - Blueprint: Plantões
Autor: Anderson de Matos Guimarães
Data: 31/10/2025
===========================================================

Descrição:
Gerencia os plantões de trabalho da aplicação Escala360,
permitindo a criação, listagem, atualização e exclusão
de registros de plantão.

Base de dados: Tabela 'plantoes' (ver escala360.sql)
Campos principais:
- id, data, hora_inicio, hora_fim, id_funcao, id_local

Rotas principais:
- /plantoes/ → página principal (template)
- /plantoes/api → CRUD via JSON (GET, POST, PUT, DELETE)
===========================================================
"""

from flask import Blueprint, jsonify, request, render_template, current_app
from models import db, Plantao  # ✅ modelo atualizado
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

plantoes_bp = Blueprint("plantoes_bp", __name__, url_prefix="/plantoes")


# =========================================================
# 🔹 Página de Interface
# =========================================================
@plantoes_bp.route("/")
def view_plantoes():
    """Renderiza a página de gestão de plantões."""
    current_app.logger.info("🕒 Acesso à página de gestão de plantões.")
    return render_template("plantoes.html", title="Gestão de Plantões")


# =========================================================
# 🔹 Listar Plantões (GET)
# =========================================================
@plantoes_bp.get("/api")
def listar_plantoes():
    """Retorna todos os plantões em formato JSON."""
    try:
        plantoes = Plantao.query.order_by(Plantao.data.asc()).all()
        data = [
            {
                "id": p.id,
                "data": p.data.strftime("%Y-%m-%d") if p.data else None,
                "hora_inicio": p.hora_inicio.strftime("%H:%M") if p.hora_inicio else None,
                "hora_fim": p.hora_fim.strftime("%H:%M") if p.hora_fim else None,
                "id_funcao": p.id_funcao,
                "id_local": p.id_local,
            }
            for p in plantoes
        ]
        current_app.logger.info(f"📋 {len(data)} plantões listados com sucesso.")
        return jsonify(data), 200

    except SQLAlchemyError as e:
        current_app.logger.error(f"❌ Erro ao listar plantões: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================================================
# 🆕 Criar Plantão (POST)
# =========================================================
@plantoes_bp.post("/api")
def criar_plantao():
    """
    Cria um novo plantão.
    Exemplo de payload:
    {
        "data": "2025-07-01",
        "hora_inicio": "08:00",
        "hora_fim": "14:00",
        "id_funcao": 1,
        "id_local": 1
    }
    """
    payload = request.get_json(silent=True) or {}
    try:
        data_str = payload.get("data")
        hora_inicio = payload.get("hora_inicio")
        hora_fim = payload.get("hora_fim")
        id_funcao = payload.get("id_funcao")
        id_local = payload.get("id_local")

        if not all([data_str, hora_inicio, hora_fim, id_funcao, id_local]):
            return jsonify({"ok": False, "error": "Campos obrigatórios ausentes."}), 400

        data = datetime.strptime(data_str, "%Y-%m-%d").date()
        hora_inicio_dt = datetime.strptime(hora_inicio, "%H:%M").time()
        hora_fim_dt = datetime.strptime(hora_fim, "%H:%M").time()

        novo_plantao = Plantao(
            data=data,
            hora_inicio=hora_inicio_dt,
            hora_fim=hora_fim_dt,
            id_funcao=id_funcao,
            id_local=id_local,
        )

        db.session.add(novo_plantao)
        db.session.commit()
        current_app.logger.info(f"✅ Plantão criado: {data_str} ({hora_inicio}-{hora_fim})")
        return jsonify({"ok": True, "id": novo_plantao.id}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"❌ Erro ao criar plantão: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500
    except Exception as e:
        current_app.logger.error(f"⚠️ Erro inesperado ao criar plantão: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================================================
# ✏️ Atualizar Plantão (PUT)
# =========================================================
@plantoes_bp.put("/api/<int:id>")
def atualizar_plantao(id):
    """Atualiza os dados de um plantão existente."""
    payload = request.get_json(silent=True) or {}
    try:
        plantao = Plantao.query.get_or_404(id)

        if "data" in payload:
            plantao.data = datetime.strptime(payload["data"], "%Y-%m-%d").date()
        if "hora_inicio" in payload:
            plantao.hora_inicio = datetime.strptime(payload["hora_inicio"], "%H:%M").time()
        if "hora_fim" in payload:
            plantao.hora_fim = datetime.strptime(payload["hora_fim"], "%H:%M").time()
        if "id_funcao" in payload:
            plantao.id_funcao = payload["id_funcao"]
        if "id_local" in payload:
            plantao.id_local = payload["id_local"]

        db.session.commit()
        current_app.logger.info(f"✏️ Plantão atualizado: {id}")
        return jsonify({"ok": True, "message": "Plantão atualizado com sucesso."}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"❌ Erro ao atualizar plantão {id}: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================================================
# 🗑️ Excluir Plantão (DELETE)
# =========================================================
@plantoes_bp.delete("/api/<int:id>")
def excluir_plantao(id):
    """Remove um plantão existente pelo ID."""
    try:
        plantao = Plantao.query.get_or_404(id)
        db.session.delete(plantao)
        db.session.commit()
        current_app.logger.warning(f"🗑️ Plantão excluído: {id}")
        return jsonify({"ok": True, "message": "Plantão excluído com sucesso."}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"❌ Erro ao excluir plantão {id}: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500
