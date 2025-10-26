"""
===========================================================
ESCALA360 - Blueprint: Usuários
Autor: Anderson de Matos Guimarães
Data: 27/10/2025
===========================================================

Descrição:
Gerencia os funcionários (usuários internos) da aplicação.
Inclui endpoints de API compatíveis com o front-end main.js
para listagem, criação e (opcionalmente) exclusão.
===========================================================
"""

from flask import Blueprint, jsonify, request, render_template
from models import db, Funcionario

usuarios_bp = Blueprint("usuarios_bp", __name__, url_prefix="/usuarios")


# =========================================================
# 🔹 Página de interface
# =========================================================
@usuarios_bp.route("/")
def view_usuarios():
    """Renderiza a página de gestão de funcionários."""
    return render_template("usuarios.html", title="Gestão de Funcionários")


# =========================================================
# 🔹 Listar funcionários (GET)
# =========================================================
@usuarios_bp.get("/api")
def listar_funcionarios():
    """Retorna todos os funcionários cadastrados."""
    funcionarios = Funcionario.query.order_by(Funcionario.nome.asc()).all()
    data = [
        {
            "id": f.id,
            "nome": f.nome,
            "cargo": f.cargo,
            "email": f.email,
            "ativo": f.ativo,
        }
        for f in funcionarios
    ]
    return jsonify(data)


# =========================================================
# 🔹 Criar funcionário (POST)
# =========================================================
@usuarios_bp.post("/api")
def criar_funcionario():
    """
    Cria um novo funcionário.
    Exemplo de payload:
    {
        "nome": "João Silva",
        "cargo": "Analista",
        "email": "joao@empresa.com",
        "ativo": true
    }
    """
    payload = request.get_json(silent=True) or {}
    try:
        nome = payload.get("nome")
        cargo = payload.get("cargo")
        email = payload.get("email")
        ativo = bool(payload.get("ativo", True))

        if not nome or not email:
            return jsonify({"ok": False, "error": "Campos obrigatórios ausentes"}), 400

        novo_func = Funcionario(nome=nome, cargo=cargo, email=email, ativo=ativo)
        db.session.add(novo_func)
        db.session.commit()

        return jsonify({"ok": True, "id": novo_func.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"ok": False, "error": str(e)}), 400


# =========================================================
# 🔹 Excluir funcionário (DELETE)
# =========================================================
@usuarios_bp.delete("/api/<int:id>")
def excluir_funcionario(id):
    """Exclui um funcionário pelo ID."""
    try:
        funcionario = Funcionario.query.get_or_404(id)
        db.session.delete(funcionario)
        db.session.commit()
        return jsonify({"ok": True, "message": "Funcionário excluído com sucesso."})
    except Exception as e:
        db.session.rollback()
        return jsonify({"ok": False, "error": str(e)}), 400
