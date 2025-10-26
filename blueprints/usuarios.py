from flask import Blueprint, jsonify, request
from models import db, Funcionario

usuarios_bp = Blueprint("usuarios_bp", __name__, url_prefix="/usuarios")

# API - listar funcionários
@usuarios_bp.get("/api")
def list_funcionarios():
    users = Funcionario.query.all()
    data = [{"id": f.id, "nome": f.nome, "cargo": f.cargo, "email": f.email, "ativo": f.ativo} for f in users]
    return jsonify(data)

# API - criar funcionário (JSON)
# payload: { "nome": "...", "cargo": "...", "email": "...", "ativo": true }
@usuarios_bp.post("/api")
def create_funcionario():
    payload = request.get_json(silent=True) or {}
    try:
        f = Funcionario(
            nome=payload.get("nome"),
            cargo=payload.get("cargo"),
            email=payload.get("email"),
            ativo=bool(payload.get("ativo", True)),
        )
        db.session.add(f)
        db.session.commit()
        return jsonify({"ok": True, "id": f.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"ok": False, "error": str(e)}), 400)
