# Sistema CRUD de Supermercado

Sistema completo de gerenciamento de supermercado desenvolvido em Python com Flask, PostgreSQL e arquitetura MVC+DAO.

## Funcionalidades

- **CRUD de Clientes**: Criar, listar, editar e excluir clientes
- **CRUD de Produtos**: Criar, listar, editar e excluir produtos
- **Interface Web**: Interface responsiva com Bootstrap
- **Banco de Dados**: PostgreSQL para persistência de dados
- **Testes de Unidade**: Cobertura completa de testes

## Arquitetura

O projeto segue a arquitetura MVC+DAO:

- **Models**: Representação das entidades (Cliente, Produto)
- **DAO (Data Access Object)**: Camada de acesso aos dados
- **Controllers**: Lógica de controle e rotas
- **Views**: Templates HTML com Jinja2

## Estrutura do Projeto

```
supermercado_crud/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── cliente_controller.py
│   │   └── produto_controller.py
│   ├── dao/
│   │   ├── __init__.py
│   │   ├── cliente_dao.py
│   │   └── produto_dao.py
│   └── models/
│       ├── __init__.py
│       ├── cliente.py
│       └── produto.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── clientes/
│   │   ├── listar.html
│   │   ├── novo.html
│   │   └── editar.html
│   └── produtos/
│       ├── listar.html
│       ├── novo.html
│       └── editar.html
├── tests/
│   ├── test_cliente.py
│   ├── test_produto.py
│   ├── test_cliente_dao.py
│   ├── test_produto_dao.py
│   └── run_tests.py
├── app.py
├── requirements.txt
└── README.md
```

## Pré-requisitos

- Python 3.8+
- PostgreSQL 12+
- pip

## Instalação

1. **Clone ou extraia o projeto**

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure o PostgreSQL**:
   ```sql
   CREATE DATABASE supermercado_db;
   CREATE USER supermercado_user WITH PASSWORD 'password';
   GRANT ALL PRIVILEGES ON DATABASE supermercado_db TO supermercado_user;
   ```

4. **Crie as tabelas**:
   ```sql
   -- Conecte-se ao banco supermercado_db
   \c supermercado_db;
   
   CREATE TABLE IF NOT EXISTS clientes (
       id_cliente SERIAL PRIMARY KEY,
       nome VARCHAR(255) NOT NULL,
       email VARCHAR(255) UNIQUE NOT NULL,
       senha VARCHAR(255) NOT NULL
   );
   
   CREATE TABLE IF NOT EXISTS produtos (
       id_produto SERIAL PRIMARY KEY,
       nome VARCHAR(255) NOT NULL,
       preco NUMERIC(10, 2) NOT NULL,
       estoque INTEGER NOT NULL
   );
   ```

## Execução

1. **Execute a aplicação**:
   ```bash
   python app.py
   ```

2. **Acesse no navegador**:
   ```
   http://localhost:5000
   ```

## Testes

Para executar todos os testes de unidade:

```bash
cd tests
python run_tests.py
```

Para executar testes individuais:

```bash
python -m unittest tests.test_cliente
python -m unittest tests.test_produto
python -m unittest tests.test_cliente_dao
python -m unittest tests.test_produto_dao
```

## Uso

### Página Inicial
- Acesse `http://localhost:5000` para ver a página inicial
- Navegue entre Clientes e Produtos usando o menu

### Gerenciamento de Clientes
- **Listar**: `/clientes` - Visualiza todos os clientes
- **Criar**: `/clientes/novo` - Adiciona novo cliente
- **Editar**: `/clientes/{id}/editar` - Edita cliente existente
- **Excluir**: Botão na listagem de clientes

### Gerenciamento de Produtos
- **Listar**: `/produtos` - Visualiza todos os produtos
- **Criar**: `/produtos/novo` - Adiciona novo produto
- **Editar**: `/produtos/{id}/editar` - Edita produto existente
- **Excluir**: Botão na listagem de produtos

## Tecnologias Utilizadas

- **Backend**: Python 3.11, Flask 3.0
- **Banco de Dados**: PostgreSQL 14
- **Frontend**: HTML5, CSS3, Bootstrap 5.1
- **Template Engine**: Jinja2
- **Testes**: unittest, mock
- **Arquitetura**: MVC + DAO

## Diagrama de Classes

O sistema implementa as seguintes classes principais:

- **Cliente**: Representa um cliente do supermercado
- **Produto**: Representa um produto do supermercado
- **ClienteDAO**: Acesso aos dados de clientes
- **ProdutoDAO**: Acesso aos dados de produtos
- **Controllers**: Controladores para cada entidade
