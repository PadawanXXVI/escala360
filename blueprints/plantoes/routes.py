"""
===========================================================
Blueprint: Plantões
Autor: Anderson de Matos Guimarães
Data: 02/11/2025
===========================================================

Descrição:
Gerencia o CRUD de plantões (datas, horários, funções e locais).
===========================================================
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Plantao

plantoes_bp = Blueprint("plantoes_bp", __name__, url_prefix="/plantoes")


# =========================================================
# 📋 Listar plantões
# =========================================================
@plantoes_bp.route("/")
def listar_plantoes():
    plantoes = Plantao.query.order_by(Plantao.data, Plantao.hora_inicio).all()
    return render_template("plantoes/listar.html", plantoes=plantoes, title="Plantões – ESCALA360")


# =========================================================
# ➕ Cadastrar novo plantão
# =========================================================
@plantoes_bp.route("/novo", methods=["GET", "POST"])
def novo_plantao():
    if request.method == "POST":
        data = request.form["data"]
        hora_inicio = request.form["hora_inicio"]
        hora_fim = request.form["hora_fim"]
        id_funcao = request.form["id_funcao"]
        id_local = request.form["id_local"]

        novo = Plantao(
            data=data,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim,
            id_funcao=id_funcao,
            id_local=id_local
        )

        db.session.add(novo)
        db.session.commit()
        flash("✅ Plantão cadastrado com sucesso!", "success")
        return redirect(url_for("plantoes_bp.listar_plantoes"))

    return render_template("plantoes/novo.html", title="Novo Plantão – ESCALA360")


# =========================================================
# ✏ Editar plantão
# =========================================================
@plantoes_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_plantao(id):
    plantao = Plantao.query.get_or_404(id)

    if request.method == "POST":
        plantao.data = request.form["data"]
        plantao.hora_inicio = request.form["hora_inicio"]
        plantao.hora_fim = request.form["hora_fim"]
        plantao.id_funcao = request.form["id_funcao"]
        plantao.id_local = request.form["id_local"]

        db.session.commit()
        flash("✏ Plantão atualizado com sucesso!", "info")
        return redirect(url_for("plantoes_bp.listar_plantoes"))

    return render_template("plantoes/editar.html", plantao=plantao, title="Editar Plantão – ESCALA360")


# =========================================================
# ❌ Excluir plantão
# =========================================================
@plantoes_bp.route("/excluir/<int:id>", methods=["POST"])
def excluir_plantao(id):
    plantao = Plantao.query.get_or_404(id)
    db.session.delete(plantao)
    db.session.commit()
    flash("🗑 Plantão removido com sucesso.", "warning")
    return redirect(url_for("plantoes_bp.listar_plantoes"))


# =========================================================
# 🔍 API: Listar em formato JSON
# =========================================================
@plantoes_bp.route("/api/listar", methods=["GET"])
def api_plantoes():
    plantoes = Plantao.query.all()
    return jsonify([{
        "id": p.id,
        "data": p.data.isoformat(),
        "hora_inicio": str(p.hora_inicio),
        "hora_fim": str(p.hora_fim),
        "id_funcao": p.id_funcao,
        "id_local": p.id_local
    } for p in plantoes])
