Plataforma de Inclusão e Diversidade para Vagas de Emprego

Este repositório contém o código-fonte de uma aplicação web interativa desenvolvida em Python, projetada para promover a inclusão e diversidade no mercado de trabalho. A plataforma permite o gerenciamento de candidatos, empresas, cursos e grupos vulneráveis, facilitando a conexão entre talentos diversos e oportunidades de emprego.
Funcionalidades Principais

    Gerenciamento de Candidatos:

        CRUD (Criar, Ler, Atualizar, Deletar) de dados do candidato.

        Visualização de candidaturas, cursos inscritos e denúncias.

        Inscrição e cancelamento de candidaturas a vagas.

        Inscrição e gerenciamento de status de cursos.

        Registro de denúncias.

        Inscrição e saída de grupos vulneráveis.

    Gerenciamento de Empresas:

        CRUD de dados da empresa.

        Gerenciamento de vagas publicadas (CRUD de vagas).

        Gerenciamento de responsáveis por inclusão (CRUD de responsáveis).

        Visualização de feedbacks de candidaturas.

        Gerenciamento e atualização do status de denúncias recebidas.

        Visualização e atualização do status de candidatos por vaga.

    Gerenciamento de Cursos:

        CRUD de dados do curso.

        Visualização de inscrições no curso.

        Inscrição de candidatos em cursos.

        Atualização e cancelamento de inscrições de candidatos.

    Gerenciamento de Grupos Vulneráveis:

        CRUD de grupos vulneráveis.

        Gerenciamento de associações entre candidatos e grupos (atualização de status de validação e comprovantes).

Tecnologias Utilizadas

    Backend/Frontend (Python Framework): Panel

    Banco de Dados: PostgreSQL

    ORM (Object-Relational Mapper): SQLAlchemy

    Manipulação de Dados: Pandas

Estrutura do Projeto

    app.py: Ponto de entrada principal da aplicação Panel, organiza as telas em abas.

    database.py: Configuração da conexão com o banco de dados (SQLAlchemy engine e Session).

    models.py: Definições dos modelos de dados (tabelas) e seus relacionamentos.

    tela_candidato.py: Lógica e interface para o gerenciamento de candidatos.

    tela_empresa.py: Lógica e interface para o gerenciamento de empresas.

    tela_cursos.py: Lógica e interface para o gerenciamento de cursos.

    tela_grupos_vulneraveis.py: Lógica e interface para o gerenciamento de grupos vulneráveis.

    criacao_tabelas: Script SQL para criação das tabelas no banco de dados.

    insercao_tabelas: Script SQL para inserção de dados de exemplo nas tabelas.

Configuração e Instalação

    Clone o repositório:

    git https://github.com/elitonnmelo/gerenciador_de_vagas.git
    cd gerenciador_de_vagas

    Crie e ative um ambiente virtual (recomendado):

    python -m venv venv
    # No Windows
    .\venv\Scripts\activate
    # No macOS/Linux
    source venv/bin/activate

    Instale as dependências:

    pip install -r requirements.txt


    Configure o Banco de Dados:

        Certifique-se de ter um servidor PostgreSQL em execução.

        Atualize a DATABASE_URL em database.py com suas credenciais e detalhes do banco de dados. Exemplo:

        DATABASE_URL = "postgresql+psycopg2://usuario:senha@localhost/nome_do_banco"

        Crie as tabelas: Execute o script criacao_tabelas no seu banco de dados.

        Insira dados de exemplo: Execute o script insercao_tabelas para popular o banco com dados de teste.

Como Executar

Após a configuração do banco de dados e a instalação das dependências, execute a aplicação Panel:

panel serve app.py --show

Isso abrirá a aplicação no seu navegador padrão.
