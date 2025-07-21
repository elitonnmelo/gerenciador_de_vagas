# models.py
from sqlalchemy import Column, String, Integer, ForeignKey, Text, Numeric, Date
from sqlalchemy.orm import relationship # Importar 'relationship'

from database import Base

class Candidato(Base):
    __tablename__ = 'candidato'
    cpf = Column(String, primary_key=True)
    nome = Column(String)
    email = Column(String)
    telefone = Column(String)
    pretensao_salarial = Column(Numeric)
    endereco = Column(String)
    data_nascimento = Column(Date)
    curriculo = Column(String) # Mudei para String se for caminho de arquivo ou URL

    # Relacionamentos para as extras do Candidato
    candidaturas = relationship("Candidatura", back_populates="candidato")
    inscricoes_cursos = relationship("InscricaoCurso", back_populates="candidato")
    denuncias = relationship("Denuncia", back_populates="candidato")
    grupos_candidato = relationship("CandidatoGrupo", back_populates="candidato") # Relacionamento com CandidatoGrupo

class Empresa(Base):
    __tablename__ = 'empresa'
    cnpj = Column(String, primary_key=True)
    nome = Column(String)
    razao_social = Column(String)
    site = Column(String)
    endereco = Column(String)
    telefone = Column(String)
    email = Column(String)

    # Relacionamentos para as extras da Empresa
    vagas_publicadas = relationship("Publica", back_populates="empresa")
    responsaveis_inclusao = relationship("ResponsavelInclusao", back_populates="empresa")

class Vaga(Base):
    __tablename__ = 'vaga'
    id_vaga = Column(Integer, primary_key=True, autoincrement=True) # Autoincrement para SERIAL
    titulo = Column(String(100))
    descricao = Column(Text)
    salario = Column(Numeric(10, 2))
    beneficios = Column(Text)
    status_vaga = Column(String(30))

    # Relacionamentos da Vaga
    publicada_por = relationship("Publica", back_populates="vaga")
    candidaturas = relationship("Candidatura", back_populates="vaga")
    vagas_grupo = relationship("VagaGrupo", back_populates="vaga")
    denuncias = relationship("Denuncia", back_populates="vaga")

class Candidatura(Base):
    __tablename__ = 'candidatura'
    cpf_candidato = Column(String, ForeignKey('candidato.cpf'), primary_key=True)
    id_vaga = Column(Integer, ForeignKey('vaga.id_vaga'), primary_key=True)
    data_candidatura = Column(Date)
    status = Column(String(30))
    feedback_empresa = Column(Text)

    # Relacionamentos
    candidato = relationship("Candidato", back_populates="candidaturas")
    vaga = relationship("Vaga", back_populates="candidaturas")

class Curso(Base):
    __tablename__ = 'curso'
    id_curso = Column(Integer, primary_key=True, autoincrement=True) # Autoincrement para SERIAL
    titulo = Column(String(100))
    descricao = Column(Text)
    carga_horaria = Column(Integer)
    modalidade = Column(String(30))
    instituicao = Column(String(100))
    link = Column(Text)

    # Relacionamentos
    inscricoes = relationship("InscricaoCurso", back_populates="curso")

class InscricaoCurso(Base):
    __tablename__ = 'inscricao_curso'
    cpf_candidato = Column(String, ForeignKey('candidato.cpf'), primary_key=True)
    id_curso = Column(Integer, ForeignKey('curso.id_curso'), primary_key=True)
    data_inscricao = Column(Date)
    comentario_avaliacao = Column(Text)
    status = Column(String(30))

    # Relacionamentos
    candidato = relationship("Candidato", back_populates="inscricoes_cursos")
    curso = relationship("Curso", back_populates="inscricoes")

class Denuncia(Base):
    __tablename__ = 'denuncia'
    id_denuncia = Column(Integer, primary_key=True, autoincrement=True)
    cpf_candidato = Column(String, ForeignKey('candidato.cpf'))
    id_vaga = Column(Integer, ForeignKey('vaga.id_vaga'))
    data_denuncia = Column(Date)
    descricao = Column(Text)
    status_denuncia = Column(String(30))
    acoes_tomadas = Column(Text)

    # Relacionamentos
    candidato = relationship("Candidato", back_populates="denuncias")
    vaga = relationship("Vaga", back_populates="denuncias")

class GrupoVulneravel(Base):
    __tablename__ = 'grupo_vulneravel'
    id_grupo = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100))
    descricao = Column(Text)

    vagas_grupo = relationship("VagaGrupo", back_populates="grupo_vulneravel")
    candidatos_grupo = relationship("CandidatoGrupo", back_populates="grupo_vulneravel")

class VagaGrupo(Base):
    __tablename__ = 'vaga_grupo'
    id_vaga = Column(Integer, ForeignKey('vaga.id_vaga'), primary_key=True)
    id_grupo = Column(Integer, ForeignKey('grupo_vulneravel.id_grupo'), primary_key=True)
    percentual_vaga = Column(Numeric(5,2))

    vaga = relationship("Vaga", back_populates="vagas_grupo")
    grupo_vulneravel = relationship("GrupoVulneravel", back_populates="vagas_grupo")

class Publica(Base):
    __tablename__ = 'publica'
    id_vaga = Column(Integer, ForeignKey('vaga.id_vaga'), primary_key=True)
    cnpj_empresa = Column(String, ForeignKey('empresa.cnpj'), primary_key=True)

    vaga = relationship("Vaga", back_populates="publicada_por")
    empresa = relationship("Empresa", back_populates="vagas_publicadas")

class CandidatoGrupo(Base):
    __tablename__ = 'candidato_grupo'
    cpf_candidato = Column(String, ForeignKey('candidato.cpf'), primary_key=True)
    id_grupo = Column(Integer, ForeignKey('grupo_vulneravel.id_grupo'), primary_key=True)
    comprovante = Column(Text)
    data_inclusao = Column(Date)
    status_validacao = Column(String(30))

    candidato = relationship("Candidato", back_populates="grupos_candidato")
    grupo_vulneravel = relationship("GrupoVulneravel", back_populates="candidatos_grupo")

class ResponsavelInclusao(Base):
    __tablename__ = 'responsavel_inclusao'
    email = Column(String, primary_key=True)
    cnpj_empresa = Column(String, ForeignKey('empresa.cnpj'), primary_key=True)
    nome = Column(String(100))
    departamento = Column(String(100))
    cargo = Column(String(100))

    empresa = relationship("Empresa", back_populates="responsaveis_inclusao")
