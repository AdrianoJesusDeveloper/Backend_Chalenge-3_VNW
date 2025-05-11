# Blueprint 
from flask import Blueprint, request, jsonify
from src.model.colaborador_model import Colaborador
from src.model import db
from src.security.security import hash_senha, checar_senha
from src.schemas import ColaboradorSchema
colaborador_schema = ColaboradorSchema()

bp_colaborador = Blueprint('colaborador', __name__, url_prefix='/colaborador')

dados = [
    {'id': 1, 'nome': 'Samuel Silvério', 'cargo': 'Desenvolvedor Back-end', 'cracha': 'BE12310'},
    {'id': 2, 'nome': 'Karynne Moreira', 'cargo': 'Desenvolvedora Front-end', 'cracha': 'FE21310'},
    {'id': 3, 'nome': 'Joy Assis', 'cargo': 'Desenvolvedora Fullstack', 'cracha': 'FS12110'},
]

@bp_colaborador.route('/todos-colaboradores', methods=['GET'])
def pegar_dados_todos_colaboradores():
    
    colaboradores = db.session.execute(
        db.select(Colaborador)
    ).scalars().all()
    
                    #Expressão                  item            iteravel 
    colaboradores = [ colaborador.all_data() for colaborador in colaboradores ]
    
    return jsonify(colaboradores), 200


# TAREFA -> VALIDAÇÃO DO CAMPO CRACHA. NÃO PODEMOS TER DUPLICATAS

@bp_colaborador.route('/cadastrar', methods=['POST'])
def cadastrar_colaborador():
    dados_requisicao = request.get_json()
    
    erros = colaborador_schema.validate(dados_requisicao)
    if erros:
        return jsonify(erros), 400

    novo_colaborador = Colaborador(
        nome=dados_requisicao['nome'],
        email=dados_requisicao['email'],
        senha=hash_senha(dados_requisicao['senha']),
        cargo=dados_requisicao['cargo'],
        salario=dados_requisicao['salario']
    )

    db.session.add(novo_colaborador)
    db.session.commit()
    
    return jsonify({'mensagem': 'Colaborador cadastrado com sucesso'}), 201
    
# # TAREFA -> VALIDAÇÃO DO USUARIO. VERIFICAÇÃO DE USUARIO NO BANCO DE DADOS (MOCKADO)

@bp_colaborador.route('/atualizar/<int:id_colaborador>', methods=['PUT'])
def atualizar_dados_colaborador(id_colaborador):
    
    dados_colaborador = request.get_json()
    
    for colaborador in dados:
        if colaborador['id'] == id_colaborador:
            colaborador_encontrado = colaborador
            break
    
    if 'nome' in dados_colaborador:
        colaborador_encontrado['nome'] = dados_colaborador['nome']
    if 'cargo' in dados_colaborador:
        colaborador_encontrado['cargo'] = dados_colaborador['cargo']
    if 'cracha' in dados_colaborador:
        colaborador_encontrado['cracha'] = dados_colaborador['cracha']

    return jsonify( {'mensagem': 'Dados do colaborador atualizados com sucesso'}), 200


@bp_colaborador.route('/login', methods=['POST'])
def login():
    
    dados_requisicao = request.get_json()
    email = dados_requisicao.get('email')
    senha = dados_requisicao.get('senha')
    
    if not email or not senha:
        return jsonify({'mensagem': 'Todos os campos devem ser preenchidos'}), 400
                                        # Query para o banco de dados
    colaborador = db.session.execute(db.select(Colaborador).where(Colaborador.email == email)).scalar() # Retornar um único resultado ou None
    
    if not colaborador:
        return jsonify({'mensagem': 'O usuário não foi encontrado'}), 404
    
    colaborador = colaborador.to_dict()    
    
    if colaborador.get('email') == email and checar_senha(senha, colaborador.get('senha')):
        return jsonify({'mensagem': 'Login realizado com sucesso'}), 200

