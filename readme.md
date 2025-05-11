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

POST /colaborador/login - Login de colaborador

GET /colaborador/todos-colaboradores - Listar todos os colaboradores

Reembolso
POST /reembolso/solicitar - Criar nova solicitação de reembolso ✅

GET /reembolso/prestacao/<num> - Buscar reembolso por número de prestação ✅

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






