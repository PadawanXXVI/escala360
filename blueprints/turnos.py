"""
===========================================================
ESCALA360 - Blueprint: Turnos
Autor: Anderson de Matos Guimarães
Data: 27/10/2025
===========================================================

Descrição:
Gerencia os turnos de trabalho da aplicação Escala360.
Inclui rotas de interface e API (CRUD parcial) compatíveis
com o front-end em main.js.
===========================================================
"""

from flask import Blueprint, jsonify, request, render_template
from models import db, Turno

turnos_bp = Blueprint("turnos_bp", __name__, url_prefix="/turnos")

# =========================================================
# 🔹 Página de Interface
# =========================================================
@turnos_bp.route("/")
def view_turnos():
    """Renderiza a página de gestão de turnos."""
    return render_template("turnos.html", title="Gestão de Turnos")


# =========================================================
# 🔹 Listar Turnos (GET)
# =========================================================
@turnos_bp.get("/api")
def listar_turnos():
    """Retorna todos os turnos em formato JSON."""
    turnos = Turno.query.order_by(Turno.id.asc()).all()
    data = [
        {
            "id": t.id,
            "nome": t.nome,
            "inicio": t.horario_inicio.strftime("%H:%M") if t.horario_inicio else "",
            "fim": t.horario_fim.strftime("%H:%M") if t.horario_fim else "",
        }
        for t in turnos
    ]
    return jsonify(data)


# =========================================================
# 🔹 Criar Turno (POST)
# =========================================================
@turnos_bp.post("/api")
def criar_turno():
    """Cria um novo turno."""
    payload = request.get_json(silent=True) or {}
    try:
        nome = payload.get("nome")
        inicio = payload.get("inicio")
        fim = payload.get("fim")

        if not nome or not inicio or not fim:
            return jsonify({"ok": False, "error": "Campos obrigatórios ausentes"}), 400

        novo_turno = Turno(nome=nome, horario_inicio=inicio, horario_fim=fim)
        db.session.add(novo_turno)
        db.session.commit()

        return jsonify({"ok": True, "id": novo_turno.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"ok": False, "error": str(e)}), 400


# =========================================================
# 🔹 Excluir Turno (DELETE)
# =========================================================
@turnos_bp.delete("/api/<int:id>")
def excluir_turno(id):
    """Remove um turno existente pelo ID."""
    try:
        turno = Turno.query.get_or_404(id)
        db.session.delete(turno)
        db.session.commit()
        return jsonify({"ok": True, "message": "Turno excluído com sucesso."})
    except Exception as e:
        db.session.rollback()
        return jsonify({"ok": False, "error": str(e)}), 400
