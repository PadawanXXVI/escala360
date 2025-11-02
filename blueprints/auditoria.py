"""
===========================================================
ESCALA360 - Blueprint: Auditoria
Autor: Anderson de Matos Guimarães
Data: 02/11/2025
===========================================================

Descrição:
Exibe e fornece via API todos os registros de auditoria
gerados automaticamente nas operações CRUD dos módulos
do sistema Escala360 (profissionais, plantões, escalas,
substituições etc).

Base de dados: Tabela 'auditoria' (ver escala360.sql)
Campos:
- id, entidade, id_entidade, acao, usuario, data_hora
===========================================================
"""

from flask import Blueprint, jsonify, request, render_template, current_app
from models import db, Auditoria
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

auditoria_bp = Blueprint("auditoria_bp", __name__, url_prefix="/auditoria")


# =========================================================
# 🧩 Página principal
# =========================================================
@auditoria_bp.route("/")
def view_auditoria():
    """Renderiza a página de registros de auditoria."""
    current_app.logger.info("📜 Acesso à página de auditoria.")
    return render_template("auditoria.html", title="Registros de Auditoria")


# =========================================================
# 📋 Listar Auditoria (GET)
# =========================================================
@auditoria_bp.get("/api")
def listar_auditoria():
    """
    Retorna todos os registros de auditoria ou filtrados por parâmetros:
    ?entidade=escala&usuario=sistema&inicio=2025-10-01&fim=2025-10-31
    """
    try:
        entidade = request.args.get("entidade")
        usuario = request.args.get("usuario")
        inicio = request.args.get("inicio")
        fim = request.args.get("fim")

        query = Auditoria.query

        if entidade:
            query = query.filter(Auditoria.entidade.ilike(f"%{entidade}%"))
        if usuario:
            query = query.filter(Auditoria.usuario.ilike(f"%{usuario}%"))

        if inicio or fim:
            try:
                data_ini = datetime.strptime(inicio, "%Y-%m-%d") if inicio else datetime(1900, 1, 1)
                data_fim = datetime.strptime(fim, "%Y-%m-%d") if fim else datetime.utcnow()
                query = query.filter(Auditoria.data_hora.between(data_ini, data_fim))
            except ValueError:
                return jsonify({"ok": False, "error": "Datas inválidas. Use o formato YYYY-MM-DD."}), 400

        auditorias = query.order_by(Auditoria.data_hora.desc()).all()

        data = [
            {
                "id": a.id,
                "entidade": a.entidade,
                "id_entidade": a.id_entidade,
                "acao": a.acao,
                "usuario": a.usuario,
                "data_hora": a.data_hora.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for a in auditorias
        ]

        current_app.logger.info(f"📋 {len(data)} registros de auditoria listados com sucesso.")
        return jsonify(data), 200

    except SQLAlchemyError as e:
        current_app.logger.error(f"❌ Erro ao listar auditoria: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================================================
# 📊 Estatísticas Resumidas (GET)
# =========================================================
@auditoria_bp.get("/api/resumo")
def resumo_auditoria():
    """Retorna estatísticas básicas de auditoria (contagem por entidade e ação)."""
    try:
        resumo_query = text("""
            SELECT entidade, acao, COUNT(*) AS total
            FROM auditoria
            GROUP BY entidade, acao
            ORDER BY entidade, acao;
        """)

        resumo = db.session.execute(resumo_query).mappings().all()
        total = sum([r["total"] for r in resumo])

        resposta = {
            "total_registros": total,
            "entidades_unicas": len(set([r["entidade"] for r in resumo])),
            "resumo": [dict(r) for r in resumo],
        }

        current_app.logger.info(f"📊 Resumo de auditoria gerado ({total} registros totais).")
        return jsonify(resposta), 200

    except SQLAlchemyError as e:
        current_app.logger.error(f"❌ Erro ao gerar resumo de auditoria: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================================================
# ⚠️ Detalhar Registro (GET)
# =========================================================
@auditoria_bp.get("/api/<int:id>")
def detalhar_auditoria(id):
    """Retorna os detalhes de um registro de auditoria específico."""
    try:
        a = Auditoria.query.get_or_404(id)
        data = {
            "id": a.id,
            "entidade": a.entidade,
            "id_entidade": a.id_entidade,
            "acao": a.acao,
            "usuario": a.usuario,
            "data_hora": a.data_hora.strftime("%Y-%m-%d %H:%M:%S"),
        }
        current_app.logger.info(f"ℹ️ Detalhamento de auditoria retornado: ID {id}")
        return jsonify(data), 200

    except SQLAlchemyError as e:
        current_app.logger.error(f"❌ Erro ao detalhar auditoria {id}: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500
