"""
===========================================================
ESCALA360 - Blueprint: Escalas
Autor: Anderson de Matos Guimarães
Data: 27/10/2025
===========================================================

Descrição:
Módulo responsável por gerenciar as escalas de trabalho.
Inclui as rotas para CRUD completo e endpoints em JSON
para integração com o front-end (AJAX).
===========================================================
"""

from flask import Blueprint, render_template, request, jsonify
from models import db, Escala, Funcionario, Turno
from datetime import datetime

escalas_bp = Blueprint("escalas_bp", __name__, url_prefix="/escalas")


# =========================================================
# 🔹 Página principal
# =========================================================
@escalas_bp.route("/")
def view_escalas():
    """Renderiza a página de gestão de escalas."""
    funcionarios = Funcionario.query.all()
    turnos = Turno.query.all()
    return render_template(
        "escalas.html",
        title="Gestão de Escalas",
        funcionarios=funcionarios,
        turnos=turnos
    )


# =========================================================
# 🔹 API - Listar todas as escalas
# =========================================================
@escalas_bp.get("/api")
def listar_escalas():
    escalas = Escala.query.all()
    data = [
        {
            "id": e.id,
            "data": e.data.strftime("%Y-%m-%d"),
            "funcionario": e.funcionario.nome if e.funcionario else "—",
            "funcionario_id": e.funcionario.id if e.funcionario else None,
            "turno": e.turno.nome if e.turno else "—",
            "turno_id": e.turno.id if e.turno else None,
            "status": e.status,
        }
        for e in escalas
    ]
    return jsonify(data)


# =========================================================
# 🔹 API - Criar nova escala
# =========================================================
@escalas_bp.post("/api")
def criar_escala():
    payload = request.get_json(silent=True) or {}
    try:
        funcionario_id = payload.get("funcionario_id")
        turno_id = payload.get("turno_id")
        data_str = payload.get("data")
        status = payload.get("status", "Ativo")

        if not (funcionario_id and turno_id and data_str):
            return jsonify({"ok": False, "error": "Campos obrigatórios ausentes"}), 400

        data = datetime.strptime(data_str, "%Y-%m-%d").date()

        nova = Escala(
            funcionario_id=funcionario_id,
            turno_id=turno_id,
            data=data,
            status=status,
        )
        db.session.add(nova)
        db.session.commit()
        return jsonify({"ok": True, "id": nova.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"ok": False, "error": str(e)}), 400


# =========================================================
# 🔹 API - Atualizar escala existente
# =========================================================
@escalas_bp.put("/api/<int:id>")
def atualizar_escala(id):
    payload = request.get_json(silent=True) or {}
    try:
        escala = Escala.query.get_or_404(id)

        if "funcionario_id" in payload:
            escala.funcionario_id = payload["funcionario_id"]
        if "turno_id" in payload:
            escala.turno_id = payload["turno_id"]
        if "data" in payload:
            escala.data = datetime.strptime(payload["data"], "%Y-%m-%d").date()
        if "status" in payload:
            escala.status = payload["status"]

        db.session.commit()
        return jsonify({"ok": True, "message": "Escala atualizada com sucesso"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"ok": False, "error": str(e)}), 400


# =========================================================
# 🔹 API - Excluir escala
# =========================================================
@escalas_bp.delete("/api/<int:id>")
def excluir_escala(id):
    try:
        escala = Escala.query.get_or_404(id)
        db.session.delete(escala)
        db.session.commit()
        return jsonify({"ok": True, "message": "Escala excluída com sucesso"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"ok": False, "error": str(e)}), 400
