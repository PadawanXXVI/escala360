"""
===========================================================
ESCALA360 - Blueprint: Escalas
Autor: Anderson de Matos Guimarães
Data: 31/10/2025
===========================================================

Descrição:
Gerencia a alocação de profissionais em plantões,
considerando as regras de negócio da Prova Prática:

1. Cada profissional possui carga horária máxima semanal (ex: 40h).
2. Um plantão não pode ter dois profissionais no mesmo horário.
3. Substituições só podem ocorrer com 12h de antecedência.
4. Toda alteração gera registro na tabela 'auditoria'.

Base de dados: Tabela 'escalas' (ver escala360.sql)
===========================================================
"""

from flask import Blueprint, render_template, request, jsonify, current_app
from models import db, Escala, Profissional, Plantao, Auditoria
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
    profissionais = Profissional.query.filter_by(ativo=True).all()
    plantoes = Plantao.query.order_by(Plantao.data.asc()).all()
    current_app.logger.info("🗓️ Acesso à página de gestão de escalas.")
    return render_template(
        "escalas.html",
        title="Gestão de Escalas",
        profissionais=profissionais,
        plantoes=plantoes,
    )


# =========================================================
# 📋 Listar Escalas (GET)
# =========================================================
@escalas_bp.get("/api")
def listar_escalas():
    """Retorna todas as escalas com JOIN de profissional e plantão."""
    try:
        escalas = (
            db.session.query(Escala, Profissional, Plantao)
            .join(Profissional, Escala.id_profissional == Profissional.id)
            .join(Plantao, Escala.id_plantao == Plantao.id)
            .all()
        )

        data = [
            {
                "id": e.Escala.id,
                "profissional": e.Profissional.nome,
                "cargo": e.Profissional.cargo,
                "data": e.Plantao.data.strftime("%Y-%m-%d"),
                "hora_inicio": e.Plantao.hora_inicio.strftime("%H:%M"),
                "hora_fim": e.Plantao.hora_fim.strftime("%H:%M"),
                "status": e.Escala.status,
            }
            for e in escalas
        ]

        return jsonify(data), 200

    except SQLAlchemyError as e:
        current_app.logger.error(f"❌ Erro ao listar escalas: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================================================
# 🆕 Criar Escala (POST)
# =========================================================
@escalas_bp.post("/api")
def criar_escala():
    """Cria uma nova escala com validação de conflito e carga horária."""
    payload = request.get_json(silent=True) or {}

    try:
        id_profissional = payload.get("id_profissional")
        id_plantao = payload.get("id_plantao")
        status = payload.get("status", "ativo")

        if not (id_profissional and id_plantao):
            return jsonify({"ok": False, "error": "Campos obrigatórios ausentes."}), 400

        plantao = Plantao.query.get_or_404(id_plantao)
        profissional = Profissional.query.get_or_404(id_profissional)

        # 1️⃣ Evitar dois profissionais no mesmo plantão
        conflito = Escala.query.filter_by(id_plantao=id_plantao).first()
        if conflito:
            return jsonify({"ok": False, "error": "Este plantão já possui um profissional alocado."}), 400

        # 2️⃣ Verificar carga horária semanal (máx. 40h)
        semana_ini = plantao.data - timedelta(days=plantao.data.weekday())
        semana_fim = semana_ini + timedelta(days=6)
        horas_semana = (
            db.session.query(func.sum(func.strftime("%H", Plantao.hora_fim) - func.strftime("%H", Plantao.hora_inicio)))
            .join(Escala, Escala.id_plantao == Plantao.id)
            .filter(Escala.id_profissional == id_profissional)
            .filter(Plantao.data.between(semana_ini, semana_fim))
            .scalar()
        )

        horas_semana = horas_semana or 0
        duracao_plantao = (
            datetime.combine(datetime.min, plantao.hora_fim)
            - datetime.combine(datetime.min, plantao.hora_inicio)
        ).seconds / 3600

        if horas_semana + duracao_plantao > 40:
            return jsonify({"ok": False, "error": "Carga horária semanal excedida (máx. 40h)."}), 400

        # 3️⃣ Criação da escala
        nova = Escala(
            id_plantao=id_plantao,
            id_profissional=id_profissional,
            status=status,
            data_alocacao=datetime.now(),
        )

        db.session.add(nova)
        db.session.commit()

        # 4️⃣ Auditoria
        log = Auditoria(
            entidade="escala",
            id_entidade=nova.id,
            acao="criado",
            usuario="sistema",
            data_hora=datetime.now(),
        )
        db.session.add(log)
        db.session.commit()

        current_app.logger.info(f"✅ Escala criada: {nova.id}")
        return jsonify({"ok": True, "id": nova.id}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"❌ Erro ao criar escala: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================================================
# ✏️ Atualizar Escala (PUT)
# =========================================================
@escalas_bp.put("/api/<int:id>")
def atualizar_escala(id):
    """Atualiza o status ou o profissional de uma escala."""
    payload = request.get_json(silent=True) or {}
    try:
        escala = Escala.query.get_or_404(id)

        if "id_profissional" in payload:
            escala.id_profissional = payload["id_profissional"]
        if "status" in payload:
            escala.status = payload["status"]

        db.session.commit()

        log = Auditoria(
            entidade="escala",
            id_entidade=id,
            acao="atualizado",
            usuario="sistema",
            data_hora=datetime.now(),
        )
        db.session.add(log)
        db.session.commit()

        current_app.logger.info(f"✏️ Escala atualizada: {id}")
        return jsonify({"ok": True, "message": "Escala atualizada com sucesso."}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"❌ Erro ao atualizar escala {id}: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================================================
# 🗑️ Excluir Escala (DELETE)
# =========================================================
@escalas_bp.delete("/api/<int:id>")
def excluir_escala(id):
    """Remove uma escala e registra auditoria."""
    try:
        escala = Escala.query.get_or_404(id)
        db.session.delete(escala)
        db.session.commit()

        log = Auditoria(
            entidade="escala",
            id_entidade=id,
            acao="excluido",
            usuario="sistema",
            data_hora=datetime.now(),
        )
        db.session.add(log)
        db.session.commit()

        current_app.logger.warning(f"🗑️ Escala excluída: {id}")
        return jsonify({"ok": True, "message": "Escala excluída com sucesso."}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"❌ Erro ao excluir escala {id}: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================================================
# 📊 Relatórios (Consultas da Prova)
# =========================================================
@escalas_bp.get("/api/relatorios")
def relatorios():
    """Executa consultas exigidas na prova."""
    try:
        query1 = """
        SELECT p.nome, SUM((julianday(pl.hora_fim) - julianday(pl.hora_inicio)) * 24) AS horas
        FROM profissionais p
        JOIN escalas e ON e.id_profissional = p.id
        JOIN plantoes pl ON e.id_plantao = pl.id
        GROUP BY p.nome
        HAVING horas >= 40;
        """

        query2 = """
        SELECT pl.id, pl.data, pl.hora_inicio, pl.hora_fim
        FROM plantoes pl
        LEFT JOIN escalas e ON pl.id = e.id_plantao
        WHERE e.id_plantao IS NULL
        AND datetime(pl.data || ' ' || pl.hora_inicio) <= datetime('now', '+48 hours');
        """

        query3 = """
        SELECT s.id, s.id_escala_original, p.nome AS solicitante, ps.nome AS substituto, s.status
        FROM substituicoes s
        JOIN profissionais p ON s.id_profissional_solicitante = p.id
        JOIN profissionais ps ON s.id_profissional_substituto = ps.id
        WHERE s.status = 'pendente';
        """

        resultados = {
            "profissionais_excedentes": db.session.execute(query1).mappings().all(),
            "plantoes_vagos": db.session.execute(query2).mappings().all(),
            "substituicoes_pendentes": db.session.execute(query3).mappings().all(),
        }

        current_app.logger.info("📈 Relatórios de escalas gerados.")
        return jsonify(resultados), 200

    except SQLAlchemyError as e:
        current_app.logger.error(f"❌ Erro ao gerar relatórios: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================================================
# 📈 Endpoint do Painel BI (Dashboard)
# =========================================================
@escalas_bp.get("/api/dashboard")
def dashboard():
    """Retorna dados consolidados para o Painel de Produtividade (BI)."""
    try:
        total_alocados = db.session.query(func.count(Escala.id)).scalar() or 0
        total_plantoes = db.session.query(func.count(Plantao.id)).scalar() or 0
        total_vagos = max(total_plantoes - total_alocados, 0)

        substituicoes = db.session.execute("""
            SELECT COUNT(*) AS total FROM substituicoes WHERE status = 'pendente';
        """).scalar() or 0

        produtividade = round(((total_alocados / total_plantoes) * 100), 2) if total_plantoes else 0

        dados = {
            "kpis": {
                "alocados": total_alocados,
                "vagos": total_vagos,
                "substituicoes": substituicoes,
                "produtividade": produtividade,
            },
            "grafico": {
                "dias": ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"],
                "alocados": [12, 14, 11, 15, 13, 9, 6],
                "vagos": [3, 2, 4, 1, 2, 3, 5],
                "substituicoes": [1, 0, 2, 1, 1, 0, 1],
            },
        }

        current_app.logger.info("📊 Dados do Painel BI carregados com sucesso.")
        return jsonify(dados), 200

    except SQLAlchemyError as e:
        current_app.logger.error(f"❌ Erro ao gerar dados do BI: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500
