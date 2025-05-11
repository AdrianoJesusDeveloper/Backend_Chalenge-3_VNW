from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
jwt = JWTManager()

def hash_senha(senha):
    return bcrypt.generate_password_hash(senha).decode('utf-8')

def checar_senha(senha, senha_hash):
    return bcrypt.check_password_hash(senha_hash, senha)
