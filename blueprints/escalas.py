from flask import Blueprint, render_template, request, jsonify
from models import db, Escala, Funcionario, Turno

escalas_bp = Blueprint("escalas_bp", __name__, url_prefix="/escalas")

# ============================================
# 🔹 Página de Gestão de Escalas
# ============================================
@escalas_bp.route("/")
def view_escalas():
    """Renderiza a página principal de gestão de escalas."""
    funcionarios = Funcionario.query.all()
    turnos = Turno.query.all()
    return render_template("escalas.html", title="Gestão de Escalas", funcionarios=funcionarios, turnos=turnos)


# ============================================
# 🔹 API: Listar Escalas
# ============================================
@escalas_bp.get("/api")
def listar_escalas():
    escalas = Escala.query.all()
    data = [
        {
            "id": e.id,
            "funcionario": e.funcionario.nome if e.funcionario else "—",
            "turno": e.turno.nome if e.turno else "—",
            "data": e.data.strftime("%d/%m/%Y"),
            "status": e.status,
        }
        for e in escalas
    ]
    return jsonify(data)


# ============================================
# 🔹 API: Criar Escala
# ============================================
@escalas_bp.post("/api")
def criar_escala():
    payload = request.get_json(silent=True) or {}
    try:
        funcionario_id = payload.get("funcionario_id")
        turno_id = payload.get("turno_id")
        data = payload.get("data")
        status = payload.get("status", "Ativo")

        if not (funcionario_id and turno_id and data):
            return jsonify({"ok": False, "error": "Campos obrigatórios ausentes"}), 400

        nova = Escala(funcionario_id=funcionario_id, turno_id=turno_id, data=data, status=status)
        db.session.add(nova)
        db.session.commit()
        return jsonify({"ok": True, "id": nova.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"ok": False, "error": str(e)}), 400
