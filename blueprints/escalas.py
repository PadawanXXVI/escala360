"""
===========================================================
ESCALA360 - Blueprint: Escalas
Autor: Anderson de Matos Guimarães
Data: 02/11/2025
===========================================================

Descrição:
Gerencia as escalas e consolida os dados para o Painel BI
(interativo no index.html). Totalmente compatível com
o banco escala360.sql e os modelos ORM atualizados.
===========================================================
"""

from flask import Blueprint, render_template, jsonify, current_app
from models import db, Escala, Profissional, Plantao, Substituicao
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

# Blueprint principal
escalas_bp = Blueprint("escalas_bp", __name__, url_prefix="/escalas")

# =========================================================
# 🧩 Página principal
# =========================================================
@escalas_bp.route("/")
def view_escalas():
    """Renderiza a página de gestão de escalas (modo CRUD futuro)."""
    profissionais = Profissional.query.filter_by(ativo=True).order_by(Profissional.nome.asc()).all()
    plantoes = Plantao.query.order_by(Plantao.data.asc()).all()
    current_app.logger.info("🗓️ Acesso à página de gestão de escalas.")
    return render_template(
        "escalas.html",
        title="Gestão de Escalas",
        profissionais=profissionais,
        plantoes=plantoes,
    )

# =========================================================
# 📈 Endpoint do Painel BI (Dashboard)
# =========================================================
@escalas_bp.get("/api/dashboard")
def dashboard():
    """Retorna dados consolidados para o Painel de Produtividade (BI)."""
    try:
        total_profissionais = db.session.query(func.count(Profissional.id)).scalar() or 0
        total_plantoes = db.session.query(func.count(Plantao.id)).scalar() or 0
        total_escalas = db.session.query(func.count(Escala.id)).scalar() or 0
        total_substituicoes = db.session.query(func.count(Substituicao.id)).scalar() or 0

        total_vagos = max(total_plantoes - total_escalas, 0)
        produtividade = round((total_escalas / total_plantoes * 100), 2) if total_plantoes else 0

        grafico = {
            "dias": ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"],
            "alocados": [12, 14, 11, 15, 13, 9, 6],
            "vagos": [3, 2, 4, 1, 2, 3, 5],
            "substituicoes": [1, 0, 2, 1, 1, 0, 1],
        }

        dados = {
            "kpis": {
                "profissionais": total_profissionais,
                "plantoes": total_plantoes,
                "alocados": total_escalas,
                "vagos": total_vagos,
                "substituicoes": total_substituicoes,
                "produtividade": produtividade,
            },
            "grafico": grafico,
        }

        current_app.logger.info(
            f"📊 Dashboard BI carregado: {total_profissionais} profs, {total_plantoes} plantoes, "
            f"{total_escalas} escalas, {total_substituicoes} substituições."
        )
        return jsonify(dados), 200

    except SQLAlchemyError as e:
        current_app.logger.error(f"❌ Erro ao gerar dados do BI: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

# =========================================================
# 📋 Listar Escalas (API)
# =========================================================
@escalas_bp.get("/api")
def listar_escalas():
    """Retorna todas as escalas com JOIN de profissional e plantão."""
    try:
        escalas = (
            db.session.query(Escala, Profissional, Plantao)
            .join(Profissional, Escala.id_profissional == Profissional.id)
            .join(Plantao, Escala.id_plantao == Plantao.id)
            .order_by(Plantao.data.asc())
            .all()
        )

        data = [
            {
                "id": e.id,
                "profissional": p.nome,
                "cargo": p.cargo or "-",
                "data": pl.data.strftime("%Y-%m-%d"),
                "hora_inicio": pl.hora_inicio.strftime("%H:%M"),
                "hora_fim": pl.hora_fim.strftime("%H:%M"),
                "status": e.status,
            }
            for e, p, pl in escalas
        ]

        current_app.logger.info(f"📋 {len(data)} escalas listadas com sucesso.")
        return jsonify(data), 200

    except SQLAlchemyError as e:
        current_app.logger.error(f"❌ Erro ao listar escalas: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500
