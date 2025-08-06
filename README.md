# 📚 Biblioteca de livros

Esta API implementada em Python com FastAPI extrai informações de livros do site [Books to Scrape](https://books.toscrape.com/), armazena os dados no arquivo "books.csv" e fornece rotas para consulta.

## 📦 Requisitos

- Python 3.8+
- pip

## 📄 Requirements.txt
- Todas as bibliotecas utilizadas no projeto estão informados nesse arquivo.

## 🔧 Instalação e configuração

1. Clone o repositório ou copie os arquivos.

2. Crie um ambiente virtual e ative:

- python -m venv venv
- source venv/bin/activate  # Linux/macOS
- venv\Scripts\activate     # Windows

- pip install -r requirements.txt

## 🔧 Inicie o servidor
- uvicorn main:app --reload
- O script automaticamente realizará a extração das páginas informadas no filtro de parametros e criará um arquivo data/books.csv.


## 🚀 Rotas da API

✅ Health Check
- GET /api/v1/health
- Verifica se a API está ativa e o número de livros disponíveis.


📚 Listar Todos os Livros
- GET /api/v1/books
- Retorna todos os livros armazenados.


🔍 Buscar Livro por ID
- GET /api/v1/books/{id}
- Retorna os detalhes de um livro específico pelo ID.


🔎 Buscar por Título e/ou Categoria
- GET /api/v1/books/search?title=foo&category=bar
- Filtra os livros por título e/ou categoria


📂 Listar Categorias
- GET /api/v1/categories
- Retorna uma lista de todas as categorias disponíveis.

## ✅ Para realizadas as funcionalidades disponiveis
- curl http://127.0.0.1:8000/api/v1/books
- http://127.0.0.1:8000/docs


📁 Estrutura de Arquivos
```bash
├── data/
│   └── books.csv
├── main.py
├── requirements.txt
└── README.md