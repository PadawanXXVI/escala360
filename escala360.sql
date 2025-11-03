-- ===================================
-- Tabelas
-- ===================================

CREATE TABLE profissionais (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    cargo TEXT NOT NULL,
    email TEXT NOT NULL,
    telefone TEXT,
    ativo BOOLEAN DEFAULT true
);

CREATE TABLE plantoes (
    id SERIAL PRIMARY KEY,
    data DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fim TIME NOT NULL,
    id_funcao INTEGER NOT NULL,
    id_local INTEGER NOT NULL
);

CREATE TABLE escalas (
    id SERIAL PRIMARY KEY,
    id_plantao INTEGER NOT NULL REFERENCES plantoes(id),
    id_profissional INTEGER NOT NULL REFERENCES profissionais(id),
    status TEXT DEFAULT 'ativo',
    data_alocacao TIMESTAMP DEFAULT now()
);

CREATE TABLE substituicoes (
    id SERIAL PRIMARY KEY,
    id_escala_original INTEGER NOT NULL REFERENCES escalas(id),
    id_profissional_solicitante INTEGER NOT NULL REFERENCES profissionais(id),
    id_profissional_substituto INTEGER NOT NULL REFERENCES profissionais(id),
    data_solicitacao TIMESTAMP DEFAULT now(),
    status TEXT DEFAULT 'pendente'
);

CREATE TABLE auditoria (
    id SERIAL PRIMARY KEY,
    entidade TEXT NOT NULL,
    id_entidade INTEGER NOT NULL,
    acao TEXT NOT NULL,
    usuario TEXT NOT NULL,
    data_hora TIMESTAMP DEFAULT now()
);

-- ===================================
-- Profissionais (30 registros)
-- ===================================

INSERT INTO profissionais (nome, cargo, email, telefone, ativo) VALUES
('Ana Souza', 'Enfermeira', 'ana.souza@example.com', '11999990001', true),
('Carlos Lima', 'Médico', 'carlos.lima@example.com', '11999990002', true),
('Beatriz Santos', 'Técnico de Enfermagem', 'beatriz.santos@example.com', '11999990003', true),
('Daniel Oliveira', 'Médico', 'daniel.oliveira@example.com', '11999990004', true),
('Fernanda Costa', 'Enfermeira', 'fernanda.costa@example.com', '11999990005', true),
('Gustavo Nunes', 'Médico', 'gustavo.nunes@example.com', '11999990006', true),
('Helena Duarte', 'Enfermeira', 'helena.duarte@example.com', '11999990007', true),
('Igor Martins', 'Técnico de Enfermagem', 'igor.martins@example.com', '11999990008', true),
('Juliana Rocha', 'Enfermeira', 'juliana.rocha@example.com', '11999990009', true),
('Kaique Barbosa', 'Médico', 'kaique.barbosa@example.com', '11999990010', true),
('Larissa Ribeiro', 'Enfermeira', 'larissa.ribeiro@example.com', '11999990011', true),
('Marcelo Vieira', 'Médico', 'marcelo.vieira@example.com', '11999990012', true),
('Natália Almeida', 'Técnico de Enfermagem', 'natalia.almeida@example.com', '11999990013', true),
('Otávio Mendes', 'Enfermeiro', 'otavio.mendes@example.com', '11999990014', true),
('Patrícia Neves', 'Médica', 'patricia.neves@example.com', '11999990015', true),
('Rafael Cunha', 'Médico', 'rafael.cunha@example.com', '11999990016', true),
('Sabrina Lopes', 'Enfermeira', 'sabrina.lopes@example.com', '11999990017', true),
('Thiago Freitas', 'Técnico de Enfermagem', 'thiago.freitas@example.com', '11999990018', true),
('Vanessa Campos', 'Enfermeira', 'vanessa.campos@example.com', '11999990019', true),
('William Costa', 'Médico', 'william.costa@example.com', '11999990020', true),
('Yasmin Pires', 'Enfermeira', 'yasmin.pires@example.com', '11999990021', true),
('Zeca Ferreira', 'Técnico de Enfermagem', 'zeca.ferreira@example.com', '11999990022', true),
('Bruno Teixeira', 'Médico', 'bruno.teixeira@example.com', '11999990023', true),
('Clara Cardoso', 'Enfermeira', 'clara.cardoso@example.com', '11999990024', true),
('Diego Melo', 'Médico', 'diego.melo@example.com', '11999990025', true),
('Eduarda Batista', 'Enfermeira', 'eduarda.batista@example.com', '11999990026', true),
('Felipe Braga', 'Médico', 'felipe.braga@example.com', '11999990027', true),
('Giovana Reis', 'Técnico de Enfermagem', 'giovana.reis@example.com', '11999990028', true),
('Hugo Sales', 'Médico', 'hugo.sales@example.com', '11999990029', true),
('Isabela Farias', 'Enfermeira', 'isabela.farias@example.com', '11999990030', true);

-- ===================================
-- Plantões (20 registros)
-- ===================================

INSERT INTO plantoes (data, hora_inicio, hora_fim, id_funcao, id_local) VALUES
('2025-07-01', '08:00', '14:00', 1, 1),
('2025-07-01', '14:00', '20:00', 1, 1),
('2025-07-02', '08:00', '14:00', 2, 1),
('2025-07-02', '14:00', '20:00', 2, 1),
('2025-07-03', '08:00', '14:00', 1, 1),
('2025-07-03', '14:00', '20:00', 1, 1),
('2025-07-04', '08:00', '14:00', 2, 1),
('2025-07-04', '14:00', '20:00', 2, 1),
('2025-07-05', '08:00', '14:00', 1, 1),
('2025-07-05', '14:00', '20:00', 1, 1),
('2025-07-06', '08:00', '14:00', 2, 1),
('2025-07-06', '14:00', '20:00', 2, 1),
('2025-07-07', '08:00', '14:00', 1, 1),
('2025-07-07', '14:00', '20:00', 1, 1),
('2025-07-08', '08:00', '14:00', 2, 1),
('2025-07-08', '14:00', '20:00', 2, 1),
('2025-07-09', '08:00', '14:00', 1, 1),
('2025-07-09', '14:00', '20:00', 1, 1),
('2025-07-10', '08:00', '14:00', 2, 1),
('2025-07-10', '14:00', '20:00', 2, 1);

-- ===================================
-- Escalas (20 registros)
-- ===================================

INSERT INTO escalas (id_plantao, id_profissional, status) VALUES
(1, 1, 'ativo'),
(2, 2, 'ativo'),
(3, 3, 'ativo'),
(4, 4, 'ativo'),
(5, 5, 'ativo'),
(6, 6, 'ativo'),
(7, 7, 'ativo'),
(8, 8, 'ativo'),
(9, 9, 'ativo'),
(10, 10, 'ativo'),
(11, 11, 'ativo'),
(12, 12, 'ativo'),
(13, 13, 'ativo'),
(14, 14, 'ativo'),
(15, 15, 'ativo'),
(16, 16, 'ativo'),
(17, 17, 'ativo'),
(18, 18, 'ativo'),
(19, 19, 'ativo'),
(20, 20, 'ativo');

-- ===================================
-- Substituições (7 registros)
-- ===================================

INSERT INTO substituicoes (id_escala_original, id_profissional_solicitante, id_profissional_substituto, status) VALUES
(2, 2, 4, 'pendente'),
(3, 3, 5, 'aprovado'),
(4, 4, 6, 'pendente'),
(5, 5, 7, 'pendente'),
(6, 6, 8, 'aprovado'),
(7, 7, 9, 'pendente'),
(8, 8, 10, 'aprovado');

-- ===================================
-- Auditoria (15 registros)
-- ===================================

INSERT INTO auditoria (entidade, id_entidade, acao, usuario) VALUES
('substituicao', 1, 'criado', 'sistema'),
('substituicao', 2, 'aprovado', 'supervisor'),
('substituicao', 3, 'criado', 'sistema'),
('substituicao', 4, 'criado', 'sistema'),
('substituicao', 5, 'criado', 'sistema'),
('substituicao', 6, 'criado', 'sistema'),
('substituicao', 7, 'aprovado', 'supervisor'),
('escala', 1, 'criado', 'sistema'),
('escala', 2, 'criado', 'sistema'),
('escala', 3, 'criado', 'sistema'),
('escala', 4, 'criado', 'sistema'),
('escala', 5, 'criado', 'sistema'),
('escala', 6, 'criado', 'sistema'),
('escala', 7, 'criado', 'sistema'),
('escala', 8, 'criado', 'sistema');
