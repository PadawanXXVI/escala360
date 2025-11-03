# 🧩 Lógica de Sugestão de Substitutos — Escala360

## 🎯 Objetivo

O objetivo deste módulo é definir a **lógica de decisão automatizada** para sugerir o **melhor profissional substituto** quando ocorre uma ausência, cancelamento ou impossibilidade de comparecimento a um plantão.

Essa lógica será usada futuramente no backend do Escala360 (módulo `substituicoes.py` e `/api/substituicoes`), garantindo **imparcialidade, eficiência e coerência** nas substituições.

---

## ⚙️ Critérios de Seleção

A escolha do profissional substituto deve respeitar **critérios hierarquizados**, garantindo a continuidade operacional sem sobrecarregar a equipe.

| Critério | Descrição | Prioridade |
|-----------|------------|------------|
| 🩺 **Cargo/Função compatível** | O substituto deve possuir o mesmo cargo ou função do profissional ausente. | Alta |
| ⏰ **Disponibilidade no horário** | O substituto não pode estar escalado para outro plantão no mesmo horário. | Alta |
| 📊 **Menor carga de plantões ativos** | Prefere-se o profissional com menos plantões ativos. | Média |
| ✅ **Status ativo** | O substituto deve estar com status “ativo” no sistema. | Alta |
| 🕒 **Preferência por experiência recente** *(opcional)* | Em casos de empate, considerar quem atuou mais recentemente. | Baixa |

---

## 🧠 Lógica de Funcionamento

A lógica é dividida em **cinco etapas principais**:

1. **Identificar a ausência**
   - O sistema detecta uma solicitação de substituição (manual ou automática).
   - São extraídas as informações do plantão original: data, horário e cargo do profissional ausente.

2. **Filtrar profissionais elegíveis**
   - Consulta-se a tabela `profissionais` filtrando por:
     - `cargo = cargo_do_ausente`
     - `ativo = TRUE`

3. **Verificar disponibilidade**
   - Para cada profissional elegível, verifica-se na tabela `escalas` se há conflito de horário.
   - O profissional é considerado **disponível** se não estiver escalado em outro plantão que se sobreponha ao intervalo `hora_inicio`–`hora_fim`.

4. **Avaliar carga de plantões**
   - Conta-se quantos plantões ativos cada profissional possui (`COUNT(*)` na tabela `escalas` com `status='ativo'`).
   - Os profissionais são ordenados em ordem crescente de carga.

5. **Selecionar o substituto ideal**
   - O primeiro da lista (menor carga e disponível) é sugerido.
   - O sistema registra a sugestão na tabela `substituicoes` com status “pendente”.

---

## 🧮 Exemplo de Execução

**Situação:**
- A enfermeira *Helena Duarte* informou ausência no plantão de 14:00 às 20:00.

**Candidatos compatíveis:**

| Profissional | Cargo | Plantões ativos | Disponível? | Status |
|---------------|--------|------------------|--------------|---------|
| Fernanda Costa | Enfermeira | 2 | ✅ | Ativo |
| Vanessa Campos | Enfermeira | 4 | ✅ | Ativo |
| Isabela Farias | Enfermeira | 3 | ✅ | Ativo |

✅ **Resultado:**  
O sistema sugere automaticamente **Fernanda Costa**, pois:
- É do mesmo cargo (enfermeira),
- Está disponível no horário,
- Possui a menor carga de plantões,
- Está com status ativo.

---

## 💻 Pseudocódigo

```text
Algoritmo: Sugerir Substituto Ideal

Entrada:
  id_profissional_solicitante
  id_plantao
  data, hora_inicio, hora_fim

Processo:
1. cargo_ausente ← SELECT cargo FROM profissionais WHERE id = id_profissional_solicitante
2. candidatos ← SELECT * FROM profissionais WHERE cargo = cargo_ausente AND ativo = TRUE
3. disponiveis ← []
4. PARA cada profissional EM candidatos:
       conflito ← SELECT COUNT(*) FROM escalas
                  WHERE id_profissional = profissional.id
                    AND data = data
                    AND (hora_inicio < hora_fim_plantao AND hora_fim > hora_inicio_plantao)
       SE conflito = 0:
           disponiveis.adicionar(profissional)
5. PARA cada profissional EM disponiveis:
       carga ← SELECT COUNT(*) FROM escalas WHERE id_profissional = profissional.id AND status = 'ativo'
6. disponiveis ← ordenar(disponiveis, por carga crescente)
7. substituto ← disponiveis[0]
8. registrar_substituicao(substituto.id, id_plantao, status="pendente")

Saída:
  substituto (id, nome, cargo, disponibilidade)

---

🧭 Fluxograma (resumo)

[Início]
   ↓
[Profissional ausente identificado]
   ↓
[Filtrar profissionais com mesmo cargo e ativos]
   ↓
[Verificar disponibilidade no horário]
   ↓
[Calcular carga de plantões ativos]
   ↓
[Selecionar quem tem menor carga]
   ↓
[Registrar substituição sugerida]
   ↓
[Fim]

---

📘 Observações Técnicas

A lógica é idempotente: se executada novamente, a mesma ausência resultará na mesma sugestão até que o contexto mude (ex.: outro profissional assume o plantão).

O algoritmo poderá ser implementado no backend como uma função Python em substituicoes.py (ex.: def sugerir_substituto(id_solicitante, id_plantao):).

Essa função poderá futuramente ser chamada pela rota REST /api/substituicoes/sugerir.
