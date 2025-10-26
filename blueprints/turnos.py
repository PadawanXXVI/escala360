from flask import Blueprint, jsonify, request, render_template
from models import db, Turno

turnos_bp = Blueprint("turnos_bp", __name__, url_prefix="/turnos")

# =========================================
# 🔹 Página de interface
# =========================================
@turnos_bp.route("/")
def view_turnos():
    """Página de gestão de turnos."""
    return render_template("turnos.html", title="Gestão de Turnos")

# =========================================
# 🔹 Listar turnos
# =========================================
@turnos_bp.get("/api")
def listar_turnos():
    turnos = Turno.query.all()
    data = [{"id": t.id, "nome": t.nome, "inicio": t.horario_inicio, "fim": t.horario_fim} for t in turnos]
    return jsonify(data)

# =========================================
# 🔹 Criar turno
# =========================================
@turnos_bp.post("/api")
def criar_turno():
    payload = request.get_json(silent=True) or {}
    try:
        nome = payload.get("nome")
        inicio = payload.get("inicio")
        fim = payload.get("fim")

        if not nome or not inicio or not fim:
            return jsonify({"ok": False, "error": "Campos obrigatórios ausentes"}), 400

        turno = Turno(nome=nome, horario_inicio=inicio, horario_fim=fim)
        db.session.add(turno)
        db.session.commit()
        return jsonify({"ok": True, "id": turno.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"ok": False, "error": str(e)}), 400
