-- Grupos vulneráveis
INSERT INTO Grupo_Vulneravel (Nome, Descricao) VALUES
('Pessoas com deficiência', 'Pessoas com limitação física ou intelectual'),
('Refugiados', 'Indivíduos deslocados por crises humanitárias'),
('Negros e pardos', 'Grupos étnico-raciais historicamente marginalizados'),
('LGBTQIA+', 'Pessoas com diversidade de orientação ou identidade'),
('Egressos do sistema prisional', 'Pessoas que cumpriram pena e estão em liberdade'),
('Mães solo', 'Mulheres que criam filhos sem apoio de um parceiro'),
('Pessoas em situação de rua', 'Indivíduos sem moradia fixa'),
('Jovens em primeiro emprego', 'Jovens com pouca ou nenhuma experiência profissional formal'),
('Pessoas 50+', 'Profissionais com mais de 50 anos em busca de recolocação'),
('Mães solteiras', 'Mães solteiras em busca de emprego com pouco ou nenhuma experiência'),
('Comunidades indígenas', 'Membros de povos originários');

-- Empresas
INSERT INTO Empresa (CNPJ, Nome, Razao_Social, Site, Endereco, Telefone, Email) VALUES
('00111222000100', 'IncluirTech', 'IncluirTech LTDA', 'www.incluirtech.com.br', 'Rua A, 123', '85999999999', 'contato@incluirtech.com.br'),
('00222333000111', 'DiversiJobs', 'DiversiJobs S.A.', 'www.diversijobs.com', 'Av B, 456', '85988888888', 'rh@diversijobs.com'),
('00333444000122', 'InovaSolucoes', 'Inova Soluções Tecnológicas Ltda', 'www.inovasolucoes.com.br', 'Rua C, 789', '85977777777', 'contato@inovasolucoes.com.br'),
('00444555000133', 'GlobalConnect', 'Global Connect S.A.', 'www.globalconnect.com', 'Av D, 1011', '85966666666', 'rh@globalconnect.com'),
('00555666000144', 'FuturoVerde', 'Futuro Verde Ambiental', 'www.futuroverde.org', 'Praça E, 12', '85955555555', 'sustentabilidade@futuroverde.org'),
('00666777000155', 'SaudeMais', 'Saúde Mais Hospitalar', 'www.saudemais.com.br', 'Rua F, 321', '85944444444', 'atendimento@saudemais.com.br'),
('00777888000166', 'EducaTech', 'EducaTech Educação Digital', 'www.educatech.online', 'Av G, 55', '85933333333', 'cursos@educatech.online'),
('00888999000177', 'LogisticaExpress', 'Logística Express Ltda', 'www.logisticaexpress.com', 'Rua H, 99', '85922222222', 'operacoes@logisticaexpress.com'),
('00999000000188', 'ArteDesign', 'Arte & Design Criativo', 'www.artedesign.com.br', 'Travessa I, 7', '85911111111', 'contato@artedesign.com.br'),
('01010101000199', 'ConstruMais', 'ConstruMais Engenharia', 'www.construmais.com', 'Av J, 200', '85900000000', 'engenharia@construmais.com');

-- Vagas
INSERT INTO Vaga (Titulo, Descricao, Salario, Beneficios, Status_Vaga) VALUES
('Dev Júnior', 'Desenvolvedor iniciante para frontend', 2500.00, 'VR, VT', 'aberta'),
('Analista RH', 'Inclusão e diversidade', 3000.00, 'VR, Plano de Saúde', 'aberta'),
('Estagiário Marketing', 'Criação de conteúdo e mídias sociais', 1200.00, 'VT, Auxílio Alimentação', 'aberta'), 
('Assistente Administrativo', 'Suporte geral de escritório', 1800.00, 'VR, VT', 'aberta'),
('Analista de Dados Jr.', 'Análise e relatórios de dados', 2800.00, 'Plano de Saúde, VR', 'aberta'),
('Desenvolvedor Backend Pleno', 'Experiência em Node.js e APIs', 4500.00, 'Plano de Saúde, VR, Bônus', 'aberta'),
('Designer Gráfico', 'Criação de peças visuais', 2200.00, 'VT', 'aberta'),
('Técnico de Enfermagem', 'Atendimento hospitalar', 2000.00, 'Adicional Noturno, VT', 'aberta'),
('Professor de Inglês', 'Aulas online para iniciantes', 2000.00, 'Flexibilidade de Horário', 'aberta'),
('Gerente de Projetos', 'Liderança de equipe e projetos de TI', 6000.00, 'Plano de Saúde, VR, PLR', 'aberta');


-- Publica
INSERT INTO Publica (Id_Vaga, CNPJ_Empresa) VALUES
(1, '00111222000100'),
(2, '00222333000111'),
(3, '00333444000122'),
(4, '00444555000133'),
(5, '00111222000100'), 
(6, '00333444000122'),
(7, '00999000000188'),
(8, '00666777000155'), 
(9, '00777888000166'),
(10, '00111222000100');


-- Vaga_Grupo
INSERT INTO Vaga_Grupo (Id_Vaga, Id_Grupo, Percentual_Vaga) VALUES
(1, 1, 50.00),
(1, 2, 50.00),
(2, 3, 100.00),
(3, 4, 100.00),
(4, 5, 70.00),
(5, 6, 50.00),
(6, 1, 100.00),
(7, 7, 80.00), 
(8, 8, 100.00),
(9, 9, 60.00), 
(10, 10, 100.00); 

-- Candidatos
INSERT INTO Candidato (CPF, Nome, Email, Pretensao_Salarial, Endereco, Telefone, Data_Nascimento, Curriculo) VALUES
('12345678900', 'João Silva', 'joao@email.com', 2000.00, 'Rua C, 111', '85977777777', '1995-04-23', 'Experiência em suporte'),
('98765432100', 'Maria Oliveira', 'maria@email.com', 3000.00, 'Rua D, 222', '85966666666', '1993-09-15', 'Analista de RH sênior'),
('11122233344', 'Carlos Mendes', 'carlos@email.com', 2200.00, 'Rua E, 333', '85955554444', '1998-11-01', 'Experiência em marketing digital'),
('44455566677', 'Ana Pereira', 'ana@email.com', 1500.00, 'Av F, 444', '85944443333', '2000-07-20', 'Estudante de administração'),
('77788899900', 'Pedro Costa', 'pedro@email.com', 3500.00, 'Rua G, 555', '85933332222', '1990-02-10', 'Cientista de dados júnior'),
('22233344455', 'Mariana Santos', 'mariana@email.com', 4000.00, 'Av H, 666', '85922221111', '1988-06-05', 'Desenvolvedora Java'),
('55566677788', 'Fernanda Lima', 'fernanda@email.com', 2500.00, 'Rua I, 777', '85911110000', '1992-03-18', 'Designer UI/UX'),
('88899900011', 'Rafael Souza', 'rafael@email.com', 1800.00, 'Av J, 888', '85900009999', '1999-08-25', 'Técnico em eletrônica'),
('33344455566', 'Julia Almeida', 'julia@email.com', 2000.00, 'Rua K, 999', '85987654321', '1997-01-30', 'Licenciada em Letras'),
('66677788899', 'Lucas Rocha', 'lucas@email.com', 5500.00, 'Av L, 1010', '85912345678', '1985-12-12', 'Engenheiro de software sênior');

-- Candidato_Grupo
INSERT INTO Candidato_Grupo (CPF_Candidato, Id_Grupo, Comprovante, Data_Inclusao, Status_Validacao) VALUES
('12345678900', 1, 'arquivo1.pdf', '2025-01-20', 'validado'),
('98765432100', 3, 'arquivo2.pdf', '2025-01-22', 'em análise'),
('11122233344', 4, 'comprovante_lgbt.pdf', '2025-02-01', 'validado'),
('44455566677', 8, 'comprovante_jovem.pdf', '2025-02-05', 'em análise'),
('77788899900', 1, 'laudo_medico.pdf', '2025-02-10', 'validado'),
('22233344455', 6, 'declaracao_mae.pdf', '2025-02-15', 'validado'),
('55566677788', 7, 'declaracao_rua.pdf', '2025-02-20', 'em análise'),
('88899900011', 9, 'rg_idade.pdf', '2025-02-25', 'validado'),
('33344455566', 2, 'comprovante_refugiado_extra.pdf', '2025-03-01', 'validado'),
('66677788899', 5, 'comprovante_egresso_extra.pdf', '2025-03-05', 'em análise');

-- Candidatura
INSERT INTO Candidatura (CPF_Candidato, Id_Vaga, Data_Candidatura, Status, Feedback_Empresa) VALUES
('12345678900', 1, '2025-03-01', 'em análise', NULL),
('98765432100', 2, '2025-03-02', 'rejeitado', 'Experiência insuficiente'),
('11122233344', 3, '2025-03-05', 'em análise', NULL),
('44455566677', 4, '2025-03-06', 'pendente', NULL),
('77788899900', 5, '2025-03-07', 'selecionado', 'Ótimo perfil técnico.'),
('22233344455', 6, '2025-03-08', 'rejeitado', 'Experiência em outra stack.'),
('55566677788', 7, '2025-03-09', 'em análise', NULL),
('88899900011', 9, '2025-03-10', 'pendente', NULL),
('33344455566', 8, '2025-03-11', 'selecionado', 'Boa comunicação.'),
('66677788899', 10, '2025-03-12', 'em análise', NULL);

-- Denuncia
INSERT INTO Denuncia (CPF_Candidato, Id_Vaga, Data_Denuncia, Descricao, Status_Denuncia, Acoes_Tomadas) VALUES
('12345678900', 1, '2025-03-05', 'Comentário preconceituoso na entrevista', 'aberta', NULL),
('44455566677', 4, '2025-03-15', 'Discriminação por idade na entrevista.', 'aberta', NULL),
('77788899900', 5, '2025-03-16', 'Promessa de vaga não cumprida.', 'em análise', NULL),
('22233344455', 6, '2025-03-17', 'Assédio moral durante o processo seletivo.', 'resolvida', 'Empresa notificada e advertida.'),
('55566677788', 7, '2025-03-18', 'Vaga falsa para coleta de dados.', 'rejeitada', 'Informações insuficientes.'),
('88899900011', 9, '2025-03-19', 'Exigência de experiência não relacionada.', 'aberta', NULL),
('33344455566', 8, '2025-03-20', 'Ambiente de trabalho hostil.', 'em análise', NULL),
('66677788899', 10, '2025-03-21', 'Falta de acessibilidade no local da entrevista.', 'aberta', NULL),
('12345678900', 3, '2025-03-22', 'Comentário inadequado sobre deficiência.', 'resolvida', 'Empresa em processo de treinamento.'),
('11122233344', 6, 'Falta de oportunidade para LGBTQIA+ na vaga.', '2025-03-25', 'aberta');

-- Curso
INSERT INTO Curso (Titulo, Descricao, Carga_Horaria, Modalidade, Instituicao, Link) VALUES
('Introdução à Programação', 'Lógica e Python', 40, 'Online', 'Alura', 'https://alura.com.br/curso1'),
('Diversidade nas Empresas', 'Curso de inclusão e RH', 20, 'Presencial', 'SEBRAE', 'https://sebrae.com.br/curso2'),
('Desenvolvimento Web com React', 'Construa interfaces modernas', 60, 'Online', 'Rocketseat', 'https://rocketseat.com.br/react'),
('Fundamentos de Banco de Dados', 'SQL e modelagem de dados', 30, 'Online', 'DIO', 'https://dio.me/db'),
('Gestão de Pessoas e Liderança', 'Desenvolva habilidades de gestão', 40, 'Presencial', 'FGV', 'https://fgv.br/gestao'),
('Introdução à Análise de Dados', 'Estatística e Python para dados', 50, 'Online', 'Data Science Academy', 'https://datascienceacademy.com.br/analise'),
('Design Thinking para Inovação', 'Metodologias de design para problemas', 25, 'Online', 'Udemy', 'https://udemy.com/design'),
('Segurança da Informação Básica', 'Proteja seus dados e sistemas', 35, 'Online', 'Coursera', 'https://coursera.org/seguranca'),
('Comunicação Assertiva no Trabalho', 'Melhore sua comunicação profissional', 20, 'Presencial', 'SENAC', 'https://senac.br/comunicacao'),
('Introdução à Inteligência Artificial', 'Conceitos e aplicações de IA', 45, 'Online', 'Google AI', 'https://ai.google/courses');

-- Inscrição Curso
INSERT INTO Inscricao_Curso (CPF_Candidato, Id_Curso, Data_Inscricao, Comentario_Avaliacao, Status) VALUES
('12345678900', 1, '2025-04-01', 'Muito bom curso', 'concluído'),
('98765432100', 2, '2025-04-03', 'Material excelente', 'em andamento'),
('11122233344', 3, '2025-04-05', 'Ótimo para iniciantes.', 'concluído'),
('44455566677', 4, '2025-04-06', 'Desafiador, mas muito bom.', 'em andamento'),
('77788899900', 5, '2025-04-07', 'Excelente conteúdo prático.', 'concluído'),
('22233344455', 6, '2025-04-08', 'Aprendi muito sobre liderança.', 'em andamento'),
('55566677788', 7, '2025-04-09', 'Aulas muito dinâmicas.', 'concluído'),
('88899900011', 8, '2025-04-10', 'Essencial para o mercado atual.', 'em andamento'),
('33344455566', 9, '2025-04-11', 'Melhorei minha comunicação.', 'concluído'),
('66677788899', 10, '2025-04-12', 'Conceitos claros e bem explicados.', 'em andamento');

-- Responsável Inclusão
INSERT INTO Responsavel_Inclusao (Email, CNPJ_Empresa, Nome, Departamento, Cargo) VALUES
('inclusao@incluirtech.com.br', '00111222000100', 'Carla Lima', 'Recursos Humanos', 'Coordenadora de Inclusão'),
('joana.santos@inovasolucoes.com.br', '00333444000122', 'Joana Santos', 'Recursos Humanos', 'Analista de RH Sênior'),
('marcos.alves@globalconnect.com', '00444555000133', 'Marcos Alves', 'Diversidade e Inclusão', 'Especialista em D&I'),
('patricia.gomes@futuroverde.org', '00555666000144', 'Patrícia Gomes', 'Sustentabilidade', 'Coordenadora de Projetos Sociais'),
('roberto.silva@saudemais.com.br', '00666777000155', 'Roberto Silva', 'Recursos Humanos', 'Gerente de RH'),
('claudia.ferreira@educatech.online', '00777888000166', 'Cláudia Ferreira', 'Educação Corporativa', 'Consultora de Treinamento'),
('andre.costa@logisticaexpress.com', '00888999000177', 'André Costa', 'Operações', 'Coordenador de Logística'),
('beatriz.lima@artedesign.com.br', '00999000000188', 'Beatriz Lima', 'Criação', 'Diretora de Arte'),
('fernando.melo@construmais.com', '01010101000199', 'Fernando Melo', 'Engenharia', 'Engenheiro de RH'),
('inclusao.nova@diversijobs.com', '00222333000111', 'Ana Clara', 'Diversidade', 'Analista de Inclusão');
