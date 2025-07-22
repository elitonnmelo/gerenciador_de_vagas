-- Tabela Grupo_Vulneravel
CREATE TABLE Grupo_Vulneravel (
    Id_Grupo SERIAL PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Descricao TEXT
);

-- Tabela Empresa
CREATE TABLE Empresa (
    CNPJ VARCHAR(20) PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Razao_Social VARCHAR(100),
    Site VARCHAR(100),
    Endereco VARCHAR(150),
    Telefone VARCHAR(20),
    Email VARCHAR(100) UNIQUE
);

-- Tabela Vaga
CREATE TABLE Vaga (
    Id_Vaga SERIAL PRIMARY KEY,
    Titulo VARCHAR(100) NOT NULL,
    Descricao TEXT,
    Salario NUMERIC(10,2),
    Beneficios TEXT,
    Status_Vaga VARCHAR(30)
);

-- Relação Publica (vaga publicada por empresa)
CREATE TABLE Publica (
    Id_Vaga INT REFERENCES Vaga(Id_Vaga),
    CNPJ_Empresa VARCHAR(20) REFERENCES Empresa(CNPJ),
    PRIMARY KEY (Id_Vaga, CNPJ_Empresa)
);

-- Tabela Candidato
CREATE TABLE Candidato (
    CPF VARCHAR(14) PRIMARY KEY,
    Nome VARCHAR(100),
    Email VARCHAR(100),
    Pretensao_Salarial NUMERIC(10,2),
    Endereco VARCHAR(150),
    Telefone VARCHAR(20),
    Data_Nascimento DATE,
    Curriculo TEXT
);

-- Tabela Vaga_Grupo (vaga associada a grupos vulneráveis)
CREATE TABLE Vaga_Grupo (
    Id_Vaga INT REFERENCES Vaga(Id_Vaga),
    Id_Grupo INT REFERENCES Grupo_Vulneravel(Id_Grupo),
    Percentual_Vaga NUMERIC(5,2),
    PRIMARY KEY (Id_Vaga, Id_Grupo)
);

-- Tabela Candidato_Grupo (grupo ao qual o candidato pertence)
CREATE TABLE Candidato_Grupo (
    CPF_Candidato VARCHAR(14) REFERENCES Candidato(CPF),
    Id_Grupo INT REFERENCES Grupo_Vulneravel(Id_Grupo),
    Comprovante TEXT,
    Data_Inclusao DATE,
    Status_Validacao VARCHAR(30),
    PRIMARY KEY (CPF_Candidato, Id_Grupo)
);

-- Tabela Candidatura
CREATE TABLE Candidatura (
    CPF_Candidato VARCHAR(14) REFERENCES Candidato(CPF),
    Id_Vaga INT REFERENCES Vaga(Id_Vaga),
    Data_Candidatura DATE,
    Status VARCHAR(30),
    Feedback_Empresa TEXT,
    PRIMARY KEY (CPF_Candidato, Id_Vaga)
);

-- Tabela Denuncia
CREATE TABLE Denuncia (
    Id_Denuncia SERIAL PRIMARY KEY,
    CPF_Candidato VARCHAR(14) REFERENCES Candidato(CPF),
    Id_Vaga INT REFERENCES Vaga(Id_Vaga),
    Data_Denuncia DATE,
    Descricao TEXT,
    Status_Denuncia VARCHAR(30),
    Acoes_Tomadas TEXT
);

-- Tabela Curso
CREATE TABLE Curso (
    Id_Curso SERIAL PRIMARY KEY,
    Titulo VARCHAR(100),
    Descricao TEXT,
    Carga_Horaria INT,
    Modalidade VARCHAR(30),
    Instituicao VARCHAR(100),
    Link TEXT
);

-- Tabela Inscricao_Curso
CREATE TABLE Inscricao_Curso (
    CPF_Candidato VARCHAR(14) REFERENCES Candidato(CPF),
    Id_Curso INT REFERENCES Curso(Id_Curso),
    Data_Inscricao DATE,
    Comentario_Avaliacao TEXT,
    Status VARCHAR(30),
    PRIMARY KEY (CPF_Candidato, Id_Curso)
);

-- Tabela Responsavel_Inclusao
CREATE TABLE Responsavel_Inclusao (
    Email VARCHAR(100),
    CNPJ_Empresa VARCHAR(20) REFERENCES Empresa(CNPJ),
    Nome VARCHAR(100),
    Departamento VARCHAR(100),
    Cargo VARCHAR(100),
    PRIMARY KEY (Email, CNPJ_Empresa)
);