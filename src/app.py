# RESPONSÁVEL PELA CRIAÇÃO DA INSTÂNCIA E CONFIGURAR O FLASK
# CREATE_APP() -> 
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
    "specs":[
        {
            "endpoint": 'apispec', # referencia da api
            "route": '/apispec.json/',
            "rule_filter": lambda rule:True, # < indica que todas as rotas vão estar na documentação
            "model_filter": lambda tag: True, #< entidades que serão mostradas
        }],
    "static_url_path": "/flasgger_static", #ira trazer o que voce tem padronizado na sua estilização, para a funcionalidade
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}
def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True # <-- Habilita o modo debug
    CORS(app, origins='*') # <---- Ative o CORS para todas as rotas da API
    app.register_blueprint(bp_colaborador)
    app.register_blueprint(bp_reembolso)
    
    
    app.config.from_object(Config) # Trouxemos a configuração do ambiente de desenvolvimento
    bcrypt.init_app(app)
    db.init_app(app) # Se inicia a conexão com o banco de dados
    Swagger(app, config=swagger_config)  # Inicializa o Swagger com a configuração definida
    print("Rotas disponíveis:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.methods} {rule}")
    
    with app.app_context():
        db.create_all() #Cria as tabelas caso elas não existam
        

    return app