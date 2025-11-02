"""
===========================================================
Blueprint: Auditoria
Autor: Anderson de Matos Guimarães
Data: 02/11/2025
===========================================================

Descrição:
Registra e exibe logs de atividades do sistema,
mantendo rastreabilidade total das ações em escalas,
substituições e plantões.
===========================================================
"""

from flask import Blueprint, render_template, jsonify
from models import db, Auditoria
from datetime import datetime

auditoria_bp = Blueprint("auditoria_bp", __name__, url_prefix="/auditoria")

# =========================================================
# 📋 Listar auditoria
# =========================================================
@auditoria_bp.route("/")
def listar_auditoria():
    """Lista todos os registros de auditoria em ordem decrescente."""
    logs = Auditoria.query.order_by(Auditoria.data_hora.desc()).limit(200).all()
    return render_template("auditoria/listar.html", logs=logs, title="Auditoria – ESCALA360")


# =========================================================
# 🔍 API JSON – Retornar auditoria
# =========================================================
@auditoria_bp.route("/api/listar", methods=["GET"])
def api_auditoria():
    """Retorna os registros de auditoria em formato JSON."""
    registros = Auditoria.query.order_by(Auditoria.data_hora.desc()).limit(200).all()
    return jsonify([
        {
            "id": r.id,
            "entidade": r.entidade,
            "id_entidade": r.id_entidade,
            "acao": r.acao,
            "usuario": r.usuario,
            "data_hora": r.data_hora.isoformat(),
        }
        for r in registros
    ])


# =========================================================
# 🧹 API – Limpar auditoria (para administradores)
# =========================================================
@auditoria_bp.route("/api/limpar", methods=["DELETE"])
def limpar_auditoria():
    """Limpa a tabela de auditoria (uso restrito)."""
    db.session.query(Auditoria).delete()
    db.session.commit()
    return jsonify({"message": "🧹 Auditoria limpa com sucesso!", "timestamp": datetime.now().isoformat()})
