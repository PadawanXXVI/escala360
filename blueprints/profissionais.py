"""
===========================================================
ESCALA360 - Blueprint: Profissionais
Autor: Anderson de Matos Guimarães
Data: 31/10/2025
===========================================================

Descrição:
Gerencia os profissionais de saúde do sistema Escala360,
permitindo cadastro, listagem, edição e exclusão.

Base de dados: Tabela 'profissionais' (ver escala360.sql)
Campos principais:
- id, nome, cargo, email, telefone, ativo

Rotas principais:
- /profissionais/ → página principal (template)
- /profissionais/api → CRUD via JSON (GET, POST, PUT, DELETE)
===========================================================
"""

from flask import Blueprint, jsonify, request, render_template, current_app
from models import db, Profissional  # ✅ novo modelo ajustado
from sqlalchemy.exc import SQLAlchemyError

profissionais_bp = Blueprint("profissionais_bp", __name__, url_prefix="/profissionais")


# =========================================================
# 🔹 Página de interface
# =========================================================
@profissionais_bp.route("/")
def view_profissionais():
    """Renderiza a página de gestão de profissionais."""
    current_app.logger.info("👥 Acesso à página de gestão de profissionais.")
    return render_template("profissionais.html", title="Gestão de Profissionais")


# =========================================================
# 🔹 Listar profissionais (GET)
# =========================================================
@profissionais_bp.get("/api")
def listar_profissionais():
    """Retorna todos os profissionais cadastrados."""
    try:
        profissionais = Profissional.query.order_by(Profissional.nome.asc()).all()
        data = [
            {
                "id": p.id,
                "nome": p.nome,
                "cargo": p.cargo,
                "email": p.email,
                "telefone": p.telefone,
                "ativo": p.ativo,
            }
            for p in profissionais
        ]
        current_app.logger.info(f"📋 {len(data)} profissionais listados.")
        return jsonify(data), 200
    except SQLAlchemyError as e:
        current_app.logger.error(f"❌ Erro ao listar profissionais: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================================================
# 🆕 Criar profissional (POST)
# =========================================================
@profissionais_bp.post("/api")
def criar_profissional():
    """
    Cria um novo profissional.
    Exemplo de payload:
    {
        "nome": "Ana Souza",
        "cargo": "Enfermeira",
        "email": "ana.souza@example.com",
        "telefone": "11999990001",
        "ativo": true
    }
    """
    payload = request.get_json(silent=True) or {}
    try:
        nome = payload.get("nome")
        cargo = payload.get("cargo")
        email = payload.get("email")
        telefone = payload.get("telefone")
        ativo = bool(payload.get("ativo", True))

        if not nome or not cargo or not email:
            return jsonify({"ok": False, "error": "Campos obrigatórios ausentes."}), 400

        novo_prof = Profissional(
            nome=nome,
            cargo=cargo,
            email=email,
            telefone=telefone,
            ativo=ativo,
        )

        db.session.add(novo_prof)
        db.session.commit()
        current_app.logger.info(f"✅ Profissional criado: {novo_prof.nome}")
        return jsonify({"ok": True, "id": novo_prof.id}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"❌ Erro ao criar profissional: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================================================
# ✏️ Atualizar profissional (PUT)
# =========================================================
@profissionais_bp.put("/api/<int:id>")
def atualizar_profissional(id):
    """Atualiza os dados de um profissional."""
    payload = request.get_json(silent=True) or {}
    try:
        prof = Profissional.query.get_or_404(id)

        if "nome" in payload:
            prof.nome = payload["nome"]
        if "cargo" in payload:
            prof.cargo = payload["cargo"]
        if "email" in payload:
            prof.email = payload["email"]
        if "telefone" in payload:
            prof.telefone = payload["telefone"]
        if "ativo" in payload:
            prof.ativo = bool(payload["ativo"])

        db.session.commit()
        current_app.logger.info(f"✏️ Profissional atualizado: {prof.id}")
        return jsonify({"ok": True, "message": "Profissional atualizado com sucesso."}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"❌ Erro ao atualizar profissional {id}: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================================================
# 🗑️ Excluir profissional (DELETE)
# =========================================================
@profissionais_bp.delete("/api/<int:id>")
def excluir_profissional(id):
    """Remove um profissional pelo ID."""
    try:
        prof = Profissional.query.get_or_404(id)
        db.session.delete(prof)
        db.session.commit()
        current_app.logger.warning(f"🗑️ Profissional excluído: {id}")
        return jsonify({"ok": True, "message": "Profissional excluído com sucesso."}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"❌ Erro ao excluir profissional {id}: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500
