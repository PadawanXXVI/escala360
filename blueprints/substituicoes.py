"""
===========================================================
ESCALA360 - Blueprint: Substituições
Autor: Anderson de Matos Guimarães
Data: 31/10/2025
===========================================================

Descrição:
Gerencia as solicitações de substituição entre profissionais,
seguindo as regras definidas na Prova Prática:

1. Substituições devem ser solicitadas com no mínimo 12h de antecedência.
2. O sistema sugere automaticamente 3 substitutos disponíveis
   com menor carga horária semanal.
3. Toda solicitação e decisão (aprovação/rejeição) é registrada
   na tabela 'auditoria'.

Base de dados: Tabela 'substituicoes' (ver escala360.sql)
Campos:
- id, id_escala_original, id_profissional_solicitante,
  id_profissional_substituto, data_solicitacao, status
===========================================================
"""

from flask import Blueprint, jsonify, request, render_template, current_app
from models import db, Substituicao, Escala, Profissional, Plantao, Auditoria
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

substituicoes_bp = Blueprint("substituicoes_bp", __name__, url_prefix="/substituicoes")


# =========================================================
# 🧩 Página principal
# =========================================================
@substituicoes_bp.route("/")
def view_substituicoes():
    """Renderiza a página de gestão de substituições."""
    substituicoes = Substituicao.query.order_by(Substituicao.data_solicitacao.desc()).all()
    return render_template(
        "substituicoes.html",
        title="Gestão de Substituições",
        substituicoes=substituicoes,
    )


# =========================================================
# 📋 Listar Substituições (GET)
# =========================================================
@substituicoes_bp.get("/api")
def listar_substituicoes():
    """Lista todas as substituições."""
    try:
        subs = (
            db.session.query(Substituicao, Escala, Profissional)
            .join(Escala, Escala.id == Substituicao.id_escala_original)
            .join(Profissional, Profissional.id == Substituicao.id_profissional_solicitante)
            .all()
        )

        data = [
            {
                "id": s.Substituicao.id,
                "escala_id": s.Escala.id,
                "solicitante": s.Profissional.nome,
                "substituto_id": s.Substituicao.id_profissional_substituto,
                "data_solicitacao": s.Substituicao.data_solicitacao.strftime("%Y-%m-%d %H:%M"),
                "status": s.Substituicao.status,
            }
            for s in subs
        ]
        return jsonify(data), 200

    except SQLAlchemyError as e:
        current_app.logger.error(f"❌ Erro ao listar substituições: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================================================
# 🆕 Criar Solicitação de Substituição (POST)
# =========================================================
@substituicoes_bp.post("/api")
def criar_substituicao():
    """
    Cria uma nova solicitação de substituição.
    Exemplo de payload:
    {
        "id_escala_original": 3,
        "id_profissional_solicitante": 2,
        "id_profissional_substituto": 5
    }
    """
    payload = request.get_json(silent=True) or {}
    try:
        id_escala_original = payload.get("id_escala_original")
        id_solicitante = payload.get("id_profissional_solicitante")
        id_substituto = payload.get("id_profissional_substituto")

        if not all([id_escala_original, id_solicitante, id_substituto]):
            return jsonify({"ok": False, "error": "Campos obrigatórios ausentes."}), 400

        escala = Escala.query.get_or_404(id_escala_original)
        plantao = Plantao.query.get_or_404(escala.id_plantao)

        # 1️⃣ Regra: substituição deve ser feita com no mínimo 12h de antecedência
        data_plantao = datetime.combine(plantao.data, plantao.hora_inicio)
        if data_plantao - datetime.now() < timedelta(hours=12):
            return jsonify(
                {"ok": False, "error": "Substituições só podem ser feitas com 12h de antecedência."}
            ), 400

        nova_sub = Substituicao(
            id_escala_original=id_escala_original,
            id_profissional_solicitante=id_solicitante,
            id_profissional_substituto=id_substituto,
            data_solicitacao=datetime.now(),
            status="pendente",
        )

        db.session.add(nova_sub)
        db.session.commit()

        # Auditoria
        log = Auditoria(
            entidade="substituicao",
            id_entidade=nova_sub.id,
            acao="criada",
            usuario="sistema",
            data_hora=datetime.now(),
        )
        db.session.add(log)
        db.session.commit()

        current_app.logger.info(f"✅ Substituição criada: {nova_sub.id}")
        return jsonify({"ok": True, "id": nova_sub.id}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"❌ Erro ao criar substituição: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================================================
# 🔍 Sugerir Substitutos (GET)
# =========================================================
@substituicoes_bp.get("/api/sugestoes/<int:id_escala>")
def sugerir_substitutos(id_escala):
    """Retorna até 3 substitutos disponíveis com menor carga horária semanal."""
    try:
        escala = Escala.query.get_or_404(id_escala)
        plantao = Plantao.query.get_or_404(escala.id_plantao)

        semana_ini = plantao.data - timedelta(days=plantao.data.weekday())
        semana_fim = semana_ini + timedelta(days=6)

        # Carga horária total por profissional na semana
        carga_query = db.session.query(
            Profissional.id,
            Profissional.nome,
            func.coalesce(
                func.sum(
                    (func.julianday(Plantao.hora_fim) - func.julianday(Plantao.hora_inicio)) * 24
                ),
                0,
            ).label("horas_semanais"),
        ).outerjoin(Escala, Profissional.id == Escala.id_profissional
        ).outerjoin(Plantao, Escala.id_plantao == Plantao.id
        ).group_by(Profissional.id)

        candidatos = []
        for p in carga_query.all():
            # Verificar se o profissional tem conflito de horário
            conflito = (
                db.session.query(Escala)
                .join(Plantao, Escala.id_plantao == Plantao.id)
                .filter(
                    Escala.id_profissional == p.id,
                    Plantao.data == plantao.data,
                    func.time(Plantao.hora_inicio) < plantao.hora_fim,
                    func.time(Plantao.hora_fim) > plantao.hora_inicio,
                )
                .first()
            )
            if not conflito:
                candidatos.append(p)

        candidatos_ordenados = sorted(candidatos, key=lambda x: x.horas_semanais)[:3]

        sugestoes = [
            {"id": c.id, "nome": c.nome, "horas_semanais": round(c.horas_semanais, 1)}
            for c in candidatos_ordenados
        ]

        return jsonify({"sugestoes": sugestoes}), 200

    except SQLAlchemyError as e:
        current_app.logger.error(f"❌ Erro ao sugerir substitutos: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================================================
# ✏️ Atualizar Status da Substituição (PUT)
# =========================================================
@substituicoes_bp.put("/api/<int:id>")
def atualizar_substituicao(id):
    """
    Aprova ou rejeita uma solicitação de substituição.
    Payload:
    {"status": "aprovado"}  ou {"status": "rejeitado"}
    """
    payload = request.get_json(silent=True) or {}
    try:
        substituicao = Substituicao.query.get_or_404(id)
        status = payload.get("status")

        if status not in ["aprovado", "rejeitado"]:
            return jsonify({"ok": False, "error": "Status inválido."}), 400

        substituicao.status = status
        db.session.commit()

        # Auditoria
        log = Auditoria(
            entidade="substituicao",
            id_entidade=id,
            acao=f"status_{status}",
            usuario="sistema",
            data_hora=datetime.now(),
        )
        db.session.add(log)
        db.session.commit()

        current_app.logger.info(f"🔄 Substituição {id} atualizada: {status}")
        return jsonify({"ok": True, "message": f"Substituição {status} com sucesso."}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"❌ Erro ao atualizar substituição {id}: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500
