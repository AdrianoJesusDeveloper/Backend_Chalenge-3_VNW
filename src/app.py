# RESPONSAVEL POR CRIAR A APLICAÇÃO 

from flask import Flask
from src.controller.colaborador_controller import bp_colaborador
from src.controller.reembolso_controller import bp_reembolso
from src.model import db
from config import Config
from flask_cors import CORS
from flasgger import Swagger
from src.security.security import bcrypt

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec", # <-- Da um nome de referencia para a documentacao
            "route": "/apispec.json/", # <- Rota do arquivo JSON para a construção da documentação
            "rule_filter": lambda rule: True, # <-- Todas as rotas/endpoints serão documentados
            "model_filter": lambda tag: True, # <-- Especificar quuais modelos da entidade serão documentados
        }
    ],
    "static_url_path": "/flasgger_static", # <-- URL para acessar a documentação
    "swagger_ui": True, # <-- Habilita a interface do Swagger UI
    "specs_route": "/apidocs/", # <-- URL para acessar a documentação
}

def create_app():
    app = Flask(__name__) # <-- instancia do Flask
    app.config['DEBUG'] = True # <-- Habilita o modo debug
    CORS(app, origins="*") # <---- A politica de CORS seja implementada em TODA A APLICAÇÃO 
    app.register_blueprint(bp_colaborador) # Registra o blueprint -> colaborador
    app.register_blueprint(bp_reembolso) # Registra o blueprint -> reembolso
    app.config.from_object(Config)
    bcrypt.init_app(app)
    
    db.init_app(app) # Inicia a conexão com o banco de dados
    
    Swagger(app, config=swagger_config)  # Inicializa o Swagger com a configuração definida
        
    print("Rotas disponíveis:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.methods} {rule}")
    
    with app.app_context(): # Se as tabelas não existem, crie.
        db.create_all()
    return app