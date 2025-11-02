"""
===========================================================
Blueprint: Profissionais
Autor: Anderson de Matos Guimarães
Data: 02/11/2025
===========================================================

Descrição:
Gerencia as operações CRUD de profissionais.
===========================================================
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Profissional

profissionais_bp = Blueprint("profissionais_bp", __name__, url_prefix="/profissionais")


# =========================================================
# 📋 Listar profissionais
# =========================================================
@profissionais_bp.route("/")
def listar_profissionais():
    profissionais = Profissional.query.order_by(Profissional.nome).all()
    return render_template("profissionais/listar.html", profissionais=profissionais, title="Profissionais – ESCALA360")


# =========================================================
# ➕ Cadastrar novo profissional
# =========================================================
@profissionais_bp.route("/novo", methods=["GET", "POST"])
def novo_profissional():
    if request.method == "POST":
        nome = request.form["nome"]
        cargo = request.form["cargo"]
        email = request.form["email"]
        telefone = request.form.get("telefone")
        ativo = bool(request.form.get("ativo", True))

        novo = Profissional(nome=nome, cargo=cargo, email=email, telefone=telefone, ativo=ativo)
        db.session.add(novo)
        db.session.commit()
        flash("✅ Profissional cadastrado com sucesso!", "success")
        return redirect(url_for("profissionais_bp.listar_profissionais"))

    return render_template("profissionais/novo.html", title="Novo Profissional – ESCALA360")


# =========================================================
# ✏ Editar profissional
# =========================================================
@profissionais_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_profissional(id):
    profissional = Profissional.query.get_or_404(id)

    if request.method == "POST":
        profissional.nome = request.form["nome"]
        profissional.cargo = request.form["cargo"]
        profissional.email = request.form["email"]
        profissional.telefone = request.form["telefone"]
        profissional.ativo = bool(request.form.get("ativo"))
        db.session.commit()
        flash("✏ Dados atualizados com sucesso!", "info")
        return redirect(url_for("profissionais_bp.listar_profissionais"))

    return render_template("profissionais/editar.html", profissional=profissional, title="Editar Profissional – ESCALA360")


# =========================================================
# ❌ Excluir profissional
# =========================================================
@profissionais_bp.route("/excluir/<int:id>", methods=["POST"])
def excluir_profissional(id):
    profissional = Profissional.query.get_or_404(id)
    db.session.delete(profissional)
    db.session.commit()
    flash("🗑 Profissional removido com sucesso.", "warning")
    return redirect(url_for("profissionais_bp.listar_profissionais"))


# =========================================================
# 🔍 API: Listar em formato JSON
# =========================================================
@profissionais_bp.route("/api/listar", methods=["GET"])
def api_profissionais():
    profissionais = Profissional.query.all()
    return jsonify([{
        "id": p.id,
        "nome": p.nome,
        "cargo": p.cargo,
        "email": p.email,
        "telefone": p.telefone,
        "ativo": p.ativo
    } for p in profissionais])
