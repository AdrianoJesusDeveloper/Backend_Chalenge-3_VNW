# RESPONSÁVEL PELA CRIAÇÃO DA INSTÂNCIA E CONFIGURAR O FLASK
# CREATE_APP() -> 
from flask import Flask
from src.controller.colaborador_controller import bp_colaborador
from src.controller.reembolso_controller import bp_reembolso
from src.model import db
from config import Config
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, origins='*') # <---- Ative o CORS para todas as rotas da API
    app.register_blueprint(bp_colaborador)
    app.register_blueprint(bp_reembolso)
    
    
    app.config.from_object(Config) # Trouxemos a configuração do ambiente de desenvolvimento
    db.init_app(app) # Se inicia a conexão com o banco de dados
    
    with app.app_context():
        db.create_all() #Cria as tabelas caso elas não existam

    return app