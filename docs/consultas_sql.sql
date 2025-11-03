-- ======================================================
-- 📊 CONSULTAS SQL — ESCALA360
-- ======================================================
-- Este arquivo contém as principais consultas SQL
-- utilizadas pelo Painel BI e relatórios administrativos.
-- ======================================================


-- 1️⃣ Profissionais com carga máxima de plantões
SELECT p.nome, COUNT(e.id) AS total_plantões
FROM profissionais p
JOIN escalas e ON e.id_profissional = p.id
GROUP BY p.nome
ORDER BY total_plantões DESC;


-- 2️⃣ Plantões vagos (sem profissional alocado)
SELECT id, data, hora_inicio, hora_fim
FROM plantoes
WHERE id NOT IN (SELECT id_plantao FROM escalas);


-- 3️⃣ Substituições pendentes
SELECT s.id, 
       p1.nome AS solicitante, 
       p2.nome AS substituto, 
       s.status
FROM substituicoes s
JOIN profissionais p1 ON s.id_profissional_solicitante = p1.id
JOIN profissionais p2 ON s.id_profissional_substituto = p2.id
WHERE s.status = 'pendente';
