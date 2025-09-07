## Descrição
API RESTful desenvolvida com **FastAPI**, **SQLAlchemy** e **SQLite**,  
utilizando dados de barragens do portal [dados.gov.br](https://dados.gov.br/).  
Permite consultar informações de minas, municípios, UFs e empreendedores.  

## Dataset
- **Fonte:** [Portal Dados Abertos](https://dados.gov.br/dataset)  
- **Formato:** CSV  
- **Periodicidade:** Anual  
- **Entidades usadas:** UF, Município, Nome da Mina, Empreendedor  

## Requisitos
- Python 3.11+  
- FastAPI  
- SQLAlchemy  
- SQLite  
- python-jose (para JWT)  

## Como executar
```bash
# Clonar o repositório
git clone https://github.com/MatheusLealCard/Trabalho_quarta_faculdade
cd entrega_api

# Criar ambiente virtual
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Rodar servidor FastAPI
uvicorn endpoints:app --reload

