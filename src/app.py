from flask import Flask, jsonify
from flasgger import Swagger, LazyString, LazyJSONEncoder
from src.controller.colaborador_controller import bp_colaborador
from src.controller.reembolso_controller import bp_reembolso
from src.model import db
from config import Config
from flask_cors import CORS
from src.security.security import bcrypt
from datetime import datetime

def create_app():
    # Inicialização do Flask
    app = Flask(__name__)
    app.config['SWAGGER'] = {
        'title': "Minha API",
        'headers': []
    }
    
    # ========== CONFIGURAÇÕES GERAIS ==========
    app.json_encoder = LazyJSONEncoder
    app.config.from_object(Config)
    app.config['DEBUG'] = Config.DEBUG  # Usar valor do config.py
    
    # ========== CONFIGURAÇÃO DO SWAGGER ==========
    swagger_config = {
        'title': 'SISPAR API',
        'uiversion': 3,
        'specs_route': '/apidocs',
        'static_url_path': '/flasgger_static',
        'specs': [{
            'endpoint': 'apispec',
            'route': '/apispec.json',
            'rule_filter': lambda rule: True,
            'model_filter': lambda tag: True,
        }],
        'openapi': '3.0.3'
    }
    
    swagger_template = {
        'info': {
            'title': 'SISPAR API',
            'version': '1.0.0',
            'description': 'API para gestão de colaboradores e solicitações de reembolso',
            'contact': {
                'email': 'suporte@sispar.com'
            }
        },
        'servers': [{
            'url': 'http://localhost:5000',
            'description': 'Servidor de desenvolvimento'
        }]
    }
    
    # ========== INICIALIZAÇÃO DE EXTENSÕES ==========
    CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})
    bcrypt.init_app(app)
    db.init_app(app)
    
    # Inicializando Swagger
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # ========== REGISTRO DE BLUEPRINTS ==========
    app.register_blueprint(bp_colaborador, url_prefix='/api/v1')
    app.register_blueprint(bp_reembolso, url_prefix='/api/v1')
    
    # ========== ROTAS GLOBAIS ==========
    @app.route('/health', methods=['GET'])
    def health_check():
        """
        Endpoint de verificação de saúde
        ---
        tags:
          - Monitoramento
        responses:
          200:
            description: Status do serviço
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    status:
                      type: string
                    database:
                      type: string
                    version:
                      type: string
        """
        try:
            db_status = 'connected' if db.session.execute('SELECT 1').first() else 'disconnected'
            return jsonify({
                'status': 'healthy',
                'database': db_status,
                'version': '1.0.0',
                'timestamp': datetime.utcnow().isoformat()
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }), 500
    
    # ========== INICIALIZAÇÃO DO BANCO ==========
    with app.app_context():
        try:
            db.create_all()
            print("✅ Tabelas do banco de dados criadas com sucesso")
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {str(e)}")
        
    return app
