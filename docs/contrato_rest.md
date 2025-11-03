# 🌐 Contrato REST — Escala360

## 📄 Visão Geral

Este documento define o **contrato de comunicação RESTful** do sistema **Escala360**, descrevendo os endpoints públicos e internos utilizados para a gestão de substituições e envio de notificações automáticas (simuladas via API).

Todas as rotas seguem o padrão:

```
https://<host>:<porta>/api/<recurso>
```

A comunicação é feita via **HTTP/HTTPS**, com dados em **JSON**.

---

## ⚙️ Padrões Gerais da API

| Item | Descrição |
|------|------------|
| **Protocolo** | HTTP / HTTPS |
| **Formato de dados** | JSON |
| **Autenticação** | Não aplicável nesta versão acadêmica |
| **Status HTTP** | `200 OK`, `201 Created`, `400 Bad Request`, `404 Not Found`, `500 Internal Server Error` |
| **Content-Type** | `application/json` |

---

## 1️⃣ GET `/api/substituicoes`

### 📘 Descrição
Retorna a lista de **substituições cadastradas**, com opção de filtragem por status (pendente, aprovado, recusado).

### 🔧 Parâmetros de Consulta (Query Params)
| Nome | Tipo | Obrigatório | Descrição |
|------|------|--------------|------------|
| `status` | string | ❌ | Filtra as substituições pelo status atual. |

### 🧠 Exemplo de Requisição
```
GET /api/substituicoes?status=pendente
```

### 📦 Exemplo de Resposta
```json
[
  {
    "id": 1,
    "id_escala_original": 2,
    "solicitante": "Carlos Lima",
    "substituto": "Daniel Oliveira",
    "status": "pendente"
  },
  {
    "id": 3,
    "id_escala_original": 5,
    "solicitante": "Fernanda Costa",
    "substituto": "Helena Duarte",
    "status": "aprovado"
  }
]
```

### 🔢 Códigos de Resposta
| Código | Descrição |
|---------|------------|
| `200 OK` | Lista retornada com sucesso. |
| `204 No Content` | Nenhuma substituição encontrada. |
| `500 Internal Server Error` | Erro interno do servidor. |

---

## 2️⃣ POST `/api/substituicoes`

### 📘 Descrição
Cria uma **nova solicitação de substituição**.  
Os dados são enviados no corpo da requisição em formato JSON.

### 🧩 Corpo da Requisição
```json
{
  "id_escala_original": 2,
  "id_profissional_solicitante": 4,
  "id_profissional_substituto": 6
}
```

### 📦 Exemplo de Resposta
```json
{
  "message": "Substituição criada com sucesso.",
  "id": 8,
  "status": "pendente"
}
```

### 🔢 Códigos de Resposta
| Código | Descrição |
|---------|------------|
| `201 Created` | Substituição registrada com sucesso. |
| `400 Bad Request` | Corpo da requisição inválido ou campos ausentes. |
| `500 Internal Server Error` | Erro interno ao inserir no banco de dados. |

---

## 3️⃣ POST `/api/notificacoes/email`

### 📘 Descrição
Simula o envio de um **e-mail automático** para o profissional envolvido em uma substituição (solicitante ou substituto).

### 🧩 Corpo da Requisição
```json
{
  "destinatario": "fernanda.costa@example.com",
  "assunto": "Substituição de Plantão — Escala360",
  "mensagem": "Olá, sua solicitação de substituição foi aprovada pelo supervisor."
}
```

### 📦 Exemplo de Resposta
```json
{
  "message": "E-mail enviado com sucesso (simulado).",
  "status": "OK"
}
```

### 🔢 Códigos de Resposta
| Código | Descrição |
|---------|------------|
| `200 OK` | E-mail simulado com sucesso. |
| `400 Bad Request` | Campos obrigatórios ausentes. |
| `500 Internal Server Error` | Erro no serviço de notificação. |

---

## 4️⃣ POST `/api/notificacoes/whatsapp`

### 📘 Descrição
Simula o envio de uma **notificação via WhatsApp** para o profissional substituto.

### 🧩 Corpo da Requisição
```json
{
  "numero": "+55 11 99999-0000",
  "mensagem": "Nova substituição aprovada! Confira seu próximo plantão no Escala360."
}
```

### 📦 Exemplo de Resposta
```json
{
  "message": "Mensagem WhatsApp enviada com sucesso (simulado).",
  "status": "OK"
}
```

### 🔢 Códigos de Resposta
| Código | Descrição |
|---------|------------|
| `200 OK` | Notificação enviada (simulada). |
| `400 Bad Request` | Campos inválidos ou número incorreto. |
| `500 Internal Server Error` | Falha na simulação da API WhatsApp. |

---

## 5️⃣ Erros Comuns (Aplicáveis a Todos os Endpoints)

| Código | Tipo | Exemplo de Resposta |
|---------|------|----------------------|
| `400` | **Requisição Inválida** | `{"error": "Campo obrigatório ausente."}` |
| `404` | **Não encontrado** | `{"error": "Recurso não encontrado."}` |
| `500` | **Erro interno** | `{"error": "Erro inesperado no servidor."}` |

---

## 📘 Estrutura de Diretórios Relacionada

```
app/
 └── routes/
     └── api.py          # Implementação dos endpoints
docs/
 └── contrato_rest.md    # Este documento
```

---

## 📚 Observações Técnicas

- Todas as requisições devem incluir o cabeçalho:  
  `Content-Type: application/json`
- Os endpoints de notificação são **simulados** (não enviam e-mails reais).  
- Os endpoints REST estão disponíveis dentro do **blueprint `api.py`**, já registrado no `__init__.py`.

---

## ✅ Conclusão

O presente contrato define formalmente as interações entre o **frontend**, o **backend Flask**, e **sistemas externos** (futuros).  
Serve também como **documento de referência técnica e acadêmica** para avaliação do sistema Escala360, garantindo rastreabilidade e padronização das comunicações.
