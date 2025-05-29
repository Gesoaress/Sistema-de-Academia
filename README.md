# Sistema de Gerenciamento de Academia

Este é um sistema simples de gerenciamento de academia desenvolvido em Python, utilizando Programação Orientada a Objetos (POO) e o ORM SQLAlchemy para persistência de dados em um banco de dados SQLite.

## Funcionalidades Principais

O sistema oferece as seguintes funcionalidades através de uma interface de linha de comando (CLI):

*   **Gerenciamento de Alunos:**
    *   Listar todos os alunos cadastrados.
    *   Adicionar um novo aluno (nome, idade, matrícula).
    *   Editar dados de um aluno existente.
    *   Apagar um aluno do sistema (remove também suas matrículas).
*   **Gerenciamento de Instrutores:**
    *   Listar todos os instrutores cadastrados.
    *   Adicionar um novo instrutor (nome, idade, CREF).
    *   Editar dados de um instrutor existente.
    *   Apagar um instrutor do sistema.
*   **Gerenciamento de Modalidades:**
    *   Listar todas as modalidades oferecidas.
    *   Adicionar uma nova modalidade.
    *   (Edição e exclusão de modalidades podem ser adicionadas futuramente, seguindo o padrão de Alunos/Instrutores).
*   **Gerenciamento de Matrículas:**
    *   Matricular um aluno existente em uma modalidade disponível.
    *   Listar todas as modalidades em que um aluno específico está matriculado.

## Tecnologias Utilizadas

*   **Linguagem:** Python 3
*   **Banco de Dados:** SQLite 3
*   **ORM:** SQLAlchemy
*   **Conceitos de POO:** Herança (Aluno e Instrutor herdam de Pessoa), Encapsulamento (uso de properties e atributos privados como `_nome`), Polimorfismo (método `exibir_detalhes` - embora não usado diretamente no menu atual).

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

```
/raiz_do_projeto
│
├── main.py             # Script principal com a interface de linha de comando e lógica do menu
├── create_tables.py    # Script opcional para criar as tabelas (geralmente não necessário se Base.metadata.create_all for usado)
├── academia.db         # Arquivo do banco de dados SQLite (criado na primeira execução)
│
└── models/             # Pacote contendo as definições das classes/modelos SQLAlchemy
    ├── __init__.py
    ├── base.py         # Configuração da Base declarativa e da sessão SQLAlchemy
    ├── pessoa.py       # Classe base abstrata Pessoa
    ├── aluno.py        # Classe Aluno (herda de Pessoa)
    ├── instrutor.py    # Classe Instrutor (herda de Pessoa)
    ├── modalidade.py   # Classe Modalidade
    └── matricula.py    # Classe de associação Matricula (entre Aluno e Modalidade)
```

## Pré-requisitos

*   Python 3.x instalado.
*   `pip` (gerenciador de pacotes Python) instalado.

## Instalação e Configuração

1.  **Clone o repositório ou copie os arquivos:** Certifique-se de que todos os arquivos (`main.py`, `create_tables.py`) e a pasta `models/` com seu conteúdo estejam na mesma pasta raiz.

2.  **Instale as dependências:** Abra o terminal na pasta raiz do projeto e instale o SQLAlchemy:
    ```bash
    pip install sqlalchemy
    ```

3.  **Banco de Dados:** O banco de dados SQLite (`academia.db`) e suas tabelas serão criados automaticamente na primeira vez que você executar o `main.py`, graças à linha `Base.metadata.create_all(engine)` no arquivo `models/base.py` (assumindo que ela esteja presente e configurada corretamente).
    *   Opcionalmente, você pode executar `python create_tables.py` (se este script estiver configurado para criar as tabelas) antes de rodar o `main.py` pela primeira vez.

## Como Executar

1.  Navegue até a pasta raiz do projeto no seu terminal.
2.  Execute o script principal:
    ```bash
    python main.py
    ```
3.  Siga as instruções apresentadas no menu interativo para utilizar as funcionalidades do sistema.

## Exemplo de Uso

Após iniciar o sistema (`python main.py`), você verá um menu como este:

```
========= Sistema de Gerenciamento Academia ==========
--- Listar ---
 1 - Listar Alunos
 2 - Listar Instrutores
 3 - Listar Modalidades
 4 - Listar Modalidades de um Aluno
--- Adicionar ---
 5 - Adicionar Aluno
 6 - Adicionar Instrutor
 7 - Adicionar Modalidade
--- Matricular ---
 8 - Matricular Aluno em Modalidade
--- Editar ---
 9 - Editar Aluno
10 - Editar Instrutor
--- Apagar ---
11 - Apagar Aluno
12 - Apagar Instrutor
--- Sair ---
13 - Sair
====================================================
Escolha uma opção: _
```

Digite o número da opção desejada e pressione Enter. O sistema solicitará as informações necessárias para cada operação.

## Autores

*   Geovane Soares da Silva
*   Richard Ferreira 
*   Ryan 

---

