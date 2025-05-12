from os import environ # Traz para o arquivo o acesso as variáveis de ambiente
from dotenv import load_dotenv # Traz a funçõa para carregar as variaveis de ambiente nesse arquivo 

load_dotenv() # Carrega as variaveis de ambiente para este arquivo

class Config():
    DEBUG = True  # ou False, conforme necessário
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI', 'mysql+pymysql://root:020521@localhost/sispar_t1')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 