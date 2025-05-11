# Conteúdo do README.md com instruções do projeto SISPAR

readme_content = """

## SISPAR - Sistema de Reembolsos

API desenvolvida com Flask para cadastro de colaboradores e controle de solicitações de reembolso.

## 🔧 Tecnologias Utilizadas

- Python 3.11
- Flask
- SQLAlchemy
- MySQL
- Flask-CORS
- python-dotenv

## 🚀 Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio


2. Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate   # Windows

3. Instalar dependências
pip install -r requirements.txt

4. Configurar variáveis de ambiente
SQLALCHEMY_DATABASE_URI=mysql+pymysql://usuario:senha@host/banco

5. Executar o projeto
python run.py


📫 Rotas disponíveis
Colaboradores
POST /colaborador/cadastrar - Cadastrar colaborador
## 📫 Rotas disponíveis

### Colaboradores
- `POST /colaborador/cadastrar` - Cadastrar novo colaborador
  ```json
  {
    "nome": "Fulano",
    "email": "fulano@empresa.com",
    "senha": "senha123",
    "cargo": "Desenvolvedor",
    "salario": 5000.00
  }

POST /colaborador/login - Login de colaborador
{
  "email": "fulano@empresa.com",
  "senha": "senha123"
}

GET /colaborador/todos-colaboradores - Listar todos os colaboradores

Reembolso
POST /reembolso/solicitar - Criar nova solicitação de reembolso ✅
{
  "colaborador": "Fulano",
  "empresa": "Empresa X",
  "num_prestacao": 12345,
  "tipo_reembolso": "Transporte",
  "valor_faturado": 150.50,
  "id_colaborador": 1
  // outros campos obrigatórios
}

GET /reembolso/prestacao/<num> - Buscar reembolso por número de prestação ✅

### 5. Configuração do Banco de Dados

**config.py:**
Atualizar para usar variáveis de ambiente corretamente:

```python
from os import environ
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL', 'mysql+pymysql://usuario:senha@localhost/nome_banco')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = environ.get('SECRET_KEY', 'segredo-desenvolvimento')

POST /reembolso/enviar/<id> - Enviar para análise

POST /reembolso/cancelar/<id> - Cancelar reembolso

DELETE /reembolso/linha/<id> - Excluir uma linha de reembolso

POST /reembolso/criar-tabelas - Criar tabelas do banco

📦 Deploy
API: Render.com

Interface: Vercel

✅ Checklist
 Estrutura MVC

 Variáveis de ambiente com .env

 Rotas obrigatórias implementadas

 JWT Token (em breve)

 Swagger (em breve)

 Validações com Marshmallow (em breve)

📄 Licença
Projeto de estudo - Fullstack Be Digital (VNW)
"""






