"""
===========================================================
Blueprint: Substituições
Autor: Anderson de Matos Guimarães
Data: 02/11/2025
===========================================================

Descrição:
Gerencia solicitações de substituição entre profissionais,
mantendo histórico e integração com auditoria.
===========================================================
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Substituicao, Profissional, Escala, Auditoria
from datetime import datetime

substituicoes_bp = Blueprint("substituicoes_bp", __name__, url_prefix="/substituicoes")

# =========================================================
# 📋 Listar substituições
# =========================================================
@substituicoes_bp.route("/")
def listar_substituicoes():
    substituicoes = (
        db.session.query(
            Substituicao,
            Escala.id.label("escala"),
            Profissional.nome.label("solicitante"),
            Profissional.nome.label("substituto")
        )
        .join(Escala, Substituicao.id_escala_original == Escala.id)
        .join(Profissional, Substituicao.id_profissional_solicitante == Profissional.id)
        .order_by(Substituicao.data_solicitacao.desc())
        .all()
    )

    return render_template(
        "substituicoes/listar.html",
        substituicoes=substituicoes,
        title="Substituições – ESCALA360"
    )


# =========================================================
# ➕ Nova solicitação de substituição
# =========================================================
@substituicoes_bp.route("/nova", methods=["GET", "POST"])
def nova_substituicao():
    profissionais = Profissional.query.filter_by(ativo=True).all()
    escalas = Escala.query.all()

    if request.method == "POST":
        id_escala_original = request.form["id_escala_original"]
        id_profissional_solicitante = request.form["id_profissional_solicitante"]
        id_profissional_substituto = request.form["id_profissional_substituto"]
        status = request.form.get("status", "pendente")

        nova = Substituicao(
            id_escala_original=id_escala_original,
            id_profissional_solicitante=id_profissional_solicitante,
            id_profissional_substituto=id_profissional_substituto,
            status=status,
            data_solicitacao=datetime.now()
        )

        db.session.add(nova)
        db.session.commit()

        # Log de auditoria
        auditoria = Auditoria(
            entidade="substituicao",
            id_entidade=nova.id,
            acao="criado",
            usuario="sistema",
            data_hora=datetime.now()
        )
        db.session.add(auditoria)
        db.session.commit()

        flash("✅ Substituição registrada com sucesso!", "success")
        return redirect(url_for("substituicoes_bp.listar_substituicoes"))

    return render_template(
        "substituicoes/nova.html",
        profissionais=profissionais,
        escalas=escalas,
        title="Nova Substituição – ESCALA360"
    )


# =========================================================
# ✏ Atualizar status da substituição
# =========================================================
@substituicoes_bp.route("/atualizar/<int:id>", methods=["POST"])
def atualizar_status(id):
    substituicao = Substituicao.query.get_or_404(id)
    novo_status = request.form["status"]
    substituicao.status = novo_status
    db.session.commit()

    auditoria = Auditoria(
        entidade="substituicao",
        id_entidade=substituicao.id,
        acao=novo_status,
        usuario="supervisor",
        data_hora=datetime.now()
    )
    db.session.add(auditoria)
    db.session.commit()

    flash("✏ Status da substituição atualizado com sucesso!", "info")
    return redirect(url_for("substituicoes_bp.listar_substituicoes"))


# =========================================================
# 🔍 API JSON: listar substituições
# =========================================================
@substituicoes_bp.route("/api/listar", methods=["GET"])
def api_substituicoes():
    substituicoes = Substituicao.query.all()
    return jsonify([
        {
            "id": s.id,
            "escala_original": s.id_escala_original,
            "solicitante": s.id_profissional_solicitante,
            "substituto": s.id_profissional_substituto,
            "status": s.status,
            "data_solicitacao": s.data_solicitacao.isoformat(),
        }
        for s in substituicoes
    ])
