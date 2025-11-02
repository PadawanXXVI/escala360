"""
===========================================================
Blueprint: Escalas
Autor: Anderson de Matos Guimarães
Data: 02/11/2025
===========================================================

Descrição:
Gerencia as escalas de trabalho, vinculando profissionais e plantões.
Integra-se ao painel BI para exibir indicadores de produtividade.
===========================================================
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import func
from models import db, Escala, Profissional, Plantao

escalas_bp = Blueprint("escalas_bp", __name__, url_prefix="/escalas")

# =========================================================
# 📋 Listar escalas
# =========================================================
@escalas_bp.route("/")
def listar_escalas():
    escalas = (
        db.session.query(
            Escala,
            Profissional.nome.label("profissional"),
            Profissional.cargo.label("cargo"),
            Plantao.data,
            Plantao.hora_inicio,
            Plantao.hora_fim,
        )
        .join(Profissional, Escala.id_profissional == Profissional.id)
        .join(Plantao, Escala.id_plantao == Plantao.id)
        .order_by(Plantao.data.asc())
        .all()
    )
    return render_template("escalas/listar.html", escalas=escalas, title="Escalas – ESCALA360")


# =========================================================
# ➕ Cadastrar nova escala
# =========================================================
@escalas_bp.route("/nova", methods=["GET", "POST"])
def nova_escala():
    profissionais = Profissional.query.filter_by(ativo=True).all()
    plantoes = Plantao.query.all()

    if request.method == "POST":
        id_profissional = request.form["id_profissional"]
        id_plantao = request.form["id_plantao"]
        status = request.form.get("status", "ativo")

        nova = Escala(id_profissional=id_profissional, id_plantao=id_plantao, status=status)
        db.session.add(nova)
        db.session.commit()

        flash("✅ Escala criada com sucesso!", "success")
        return redirect(url_for("escalas_bp.listar_escalas"))

    return render_template("escalas/nova.html", profissionais=profissionais, plantoes=plantoes, title="Nova Escala – ESCALA360")


# =========================================================
# ✏ Editar escala
# =========================================================
@escalas_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_escala(id):
    escala = Escala.query.get_or_404(id)
    profissionais = Profissional.query.filter_by(ativo=True).all()
    plantoes = Plantao.query.all()

    if request.method == "POST":
        escala.id_profissional = request.form["id_profissional"]
        escala.id_plantao = request.form["id_plantao"]
        escala.status = request.form.get("status", "ativo")
        db.session.commit()
        flash("✏ Escala atualizada com sucesso!", "info")
        return redirect(url_for("escalas_bp.listar_escalas"))

    return render_template("escalas/editar.html", escala=escala, profissionais=profissionais, plantoes=plantoes, title="Editar Escala – ESCALA360")


# =========================================================
# ❌ Excluir escala
# =========================================================
@escalas_bp.route("/excluir/<int:id>", methods=["POST"])
def excluir_escala(id):
    escala = Escala.query.get_or_404(id)
    db.session.delete(escala)
    db.session.commit()
    flash("🗑 Escala removida com sucesso.", "warning")
    return redirect(url_for("escalas_bp.listar_escalas"))


# =========================================================
# 📊 API – Dados para o Painel de BI
# =========================================================
@escalas_bp.route("/api/dashboard", methods=["GET"])
def dashboard_api():
    """Retorna dados agregados para o painel Plotly"""
    total_escalas = db.session.query(func.count(Escala.id)).scalar()
    total_ativos = db.session.query(func.count(Escala.id)).filter(Escala.status == "ativo").scalar()
    total_vagos = db.session.query(func.count(Escala.id)).filter(Escala.status != "ativo").scalar()

    # Gráfico diário
    grafico = (
        db.session.query(
            Plantao.data,
            func.count(Escala.id).label("total")
        )
        .join(Plantao, Escala.id_plantao == Plantao.id)
        .group_by(Plantao.data)
        .order_by(Plantao.data)
        .all()
    )

    dias = [g.data.strftime("%d/%m") for g in grafico]
    alocados = [g.total for g in grafico]

    kpis = {
        "total_escalas": total_escalas,
        "ativos": total_ativos,
        "vagos": total_vagos,
        "produtividade": round((total_ativos / total_escalas * 100), 1) if total_escalas else 0
    }

    return jsonify({"kpis": kpis, "grafico": {"dias": dias, "alocados": alocados}})
