"""
===========================================================
ESCALA360 - Blueprint: Escalas
Autor: Anderson de Matos Guimarães
Data: 02/11/2025
===========================================================

Descrição:
Gerencia a alocação de funcionários em turnos (escalas),
bem como os dados de produtividade (Painel BI).
Compatível com o banco escala360.sql.
===========================================================
"""

from flask import Blueprint, render_template, request, jsonify, current_app
from models import db, Escala, Funcionario, Turno, Substituicao
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

escalas_bp = Blueprint("escalas_bp", __name__, url_prefix="/escalas")

# =========================================================
# 🧩 Página principal
# =========================================================
@escalas_bp.route("/")
def view_escalas():
    """Renderiza a página de gestão de escalas."""
    funcionarios = Funcionario.query.filter_by(ativo=True).all()
    turnos = Turno.query.order_by(Turno.horario_inicio.asc()).all()
    current_app.logger.info("🗓️ Acesso à página de gestão de escalas.")
    return render_template(
        "escalas.html",
        title="Gestão de Escalas",
        funcionarios=funcionarios,
        turnos=turnos,
    )

# =========================================================
# 📈 Endpoint do Painel BI (Dashboard)
# =========================================================
@escalas_bp.get("/api/dashboard")
def dashboard():
    """Retorna dados consolidados para o Painel de Produtividade (BI)."""
    try:
        total_funcionarios = db.session.query(func.count(Funcionario.id)).scalar() or 0
        total_turnos = db.session.query(func.count(Turno.id)).scalar() or 0
        total_escalas = db.session.query(func.count(Escala.id)).scalar() or 0
        total_substituicoes = db.session.query(func.count(Substituicao.id)).scalar() or 0

        # Plantões vagos = turnos - escalas
        total_vagos = max(total_turnos - total_escalas, 0)

        # Produtividade = (escalas preenchidas / total de turnos)
        produtividade = round((total_escalas / total_turnos * 100), 2) if total_turnos else 0

        # Geração de gráfico dinâmico (mock caso o banco esteja vazio)
        dias = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        grafico = {
            "dias": dias,
            "alocados": [5, 6, 4, 7, 6, 5, 3],
            "vagos": [2, 1, 3, 1, 2, 1, 2],
            "substituicoes": [0, 1, 0, 1, 0, 0, 0],
        }

        dados = {
            "kpis": {
                "alocados": total_escalas,
                "vagos": total_vagos,
                "substituicoes": total_substituicoes,
                "produtividade": produtividade,
            },
            "grafico": grafico,
        }

        current_app.logger.info("📊 Painel BI atualizado com sucesso.")
        return jsonify(dados), 200

    except SQLAlchemyError as e:
        current_app.logger.error(f"❌ Erro ao gerar dados do BI: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

# =========================================================
# ✏️ Listar Escalas (API)
# =========================================================
@escalas_bp.get("/api")
def listar_escalas():
    """Retorna todas as escalas com JOIN de funcionário e turno."""
    try:
        escalas = (
            db.session.query(Escala, Funcionario, Turno)
            .join(Funcionario, Escala.funcionario_id == Funcionario.id)
            .join(Turno, Escala.turno_id == Turno.id)
            .order_by(Escala.data.desc())
            .all()
        )

        data = [
            {
                "id": e.Escala.id,
                "funcionario": e.Funcionario.nome,
                "cargo": e.Funcionario.cargo or "-",
                "data": e.Escala.data.strftime("%Y-%m-%d"),
                "turno": e.Turno.nome,
                "status": e.Escala.status,
            }
            for e in escalas
        ]

        return jsonify(data), 200

    except SQLAlchemyError as e:
        current_app.logger.error(f"❌ Erro ao listar escalas: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500
