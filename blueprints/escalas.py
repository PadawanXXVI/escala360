from flask import Blueprint, render_template, jsonify, request
from models import db
from models import Escala, Funcionario, Turno
from datetime import datetime

escalas_bp = Blueprint("escalas_bp", __name__, url_prefix="/escalas")

# UI
@escalas_bp.get("/")
def view_escalas():
    """Página de gestão de escalas e substituições."""
    return render_template("escalas.html", title="Gestão de Escalas")

# API - listar escalas
@escalas_bp.get("/api")
def list_escalas():
    escalas = Escala.query.all()
    data = [
        {
            "id": e.id,
            "data": e.data.strftime("%d/%m/%Y"),
            "servidor": e.funcionario.nome if e.funcionario else "—",
            "turno": e.turno.nome if e.turno else "—",
            "status": e.status,
        }
        for e in escalas
    ]
    return jsonify(data)

# API - criar escala (JSON)
# payload exemplo:
# { "data": "2025-10-26", "funcionario_id": 1, "turno_id": 2, "status": "Ativo" }
@escalas_bp.post("/api")
def create_escala():
    payload = request.get_json(silent=True) or {}
    try:
        data = datetime.fromisoformat(payload.get("data")).date()
        func_id = payload.get("funcionario_id")
        turno_id = payload.get("turno_id")
        status = payload.get("status", "Ativo")

        escala = Escala(data=data, funcionario_id=func_id, turno_id=turno_id, status=status)
        db.session.add(escala)
        db.session.commit()
        return jsonify({"ok": True, "id": escala.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"ok": False, "error": str(e)}), 400
