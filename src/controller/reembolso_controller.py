# Novo conteúdo do reembolso_controller.py com rotas obrigatórias incluídas
reembolso_controller_code = """
from flask import request, jsonify, Blueprint
from src.model.reembolso_model import Reembolso
from src.model import db

bp_reembolso = Blueprint('reembolso', __name__, url_prefix='/reembolso')

# ROTA PARA EXCLUIR LINHA DE REEMBOLSO
@bp_reembolso.route('/linha/<int:linha_id>', methods=['DELETE'])
def deletar_linha_reembolso(linha_id):
    linha = db.session.get(Reembolso, linha_id)
    if not linha:
        return jsonify({'mensagem': 'Linha de reembolso não encontrada'}), 404

    db.session.delete(linha)
    db.session.commit()
    return jsonify({'mensagem': 'Linha de reembolso excluída com sucesso'}), 200

# NOVA ROTA: SOLICITAR REEMBOLSO
@bp_reembolso.route('/solicitar', methods=['POST'])
def solicitar_reembolso():
    dados = request.get_json()
    try:
        novo_reembolso = Reembolso(**dados)
        db.session.add(novo_reembolso)
        db.session.commit()
        return jsonify({'mensagem': 'Solicitação de reembolso registrada com sucesso'}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

# NOVA ROTA: CONSULTAR POR NUM PRESTAÇÃO
@bp_reembolso.route('/prestacao/<int:num>', methods=['GET'])
def consultar_por_prestacao(num):
    reembolso = db.session.execute(
        db.select(Reembolso).where(Reembolso.num_prestacao == num)
    ).scalar()

    if not reembolso:
        return jsonify({'mensagem': 'Reembolso não encontrado'}), 404

    return jsonify({
        'id': reembolso.id,
        'colaborador': reembolso.colaborador,
        'empresa': reembolso.empresa,
        'num_prestacao': reembolso.num_prestacao,
        'descricao': reembolso.descricao,
        'status': reembolso.status
    }), 200

# ROTA PARA ENVIAR SOLICITAÇÃO PARA ANÁLISE
@bp_reembolso.route('/enviar/<int:reembolso_id>', methods=['POST'])
def enviar_para_analise(reembolso_id):
    reembolso = db.session.get(Reembolso, reembolso_id)
    if not reembolso:
        return jsonify({'mensagem': 'Solicitação não encontrada'}), 404

    reembolso.status = 'Em Análise'
    db.session.commit()
    return jsonify({'mensagem': 'Solicitação enviada para análise com sucesso'}), 200

# ROTA PARA CANCELAR SOLICITAÇÃO
@bp_reembolso.route('/cancelar/<int:reembolso_id>', methods=['POST'])
def cancelar_reembolso(reembolso_id):
    reembolso = db.session.get(Reembolso, reembolso_id)
    if not reembolso:
        return jsonify({'mensagem': 'Solicitação não encontrada'}), 404

    reembolso.status = 'Cancelada'
    db.session.commit()
    return jsonify({'mensagem': 'Solicitação cancelada com sucesso'}), 200

# ROTA OPCIONAL PARA CRIAR AS TABELAS DO BANCO DE DADOS
@bp_reembolso.route('/criar-tabelas', methods=['POST'])
def criar_tabelas_reembolso():
    try:
        db.create_all()
        return jsonify({'mensagem': 'Tabelas criadas com sucesso'}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
"""

# Caminho do arquivo
reembolso_path = "/mnt/data/sispar_atualizado/src/controller/reembolso_controller.py"

# Salvar o novo código
with open(reembolso_path, "w") as f:
    f.write(reembolso_controller_code)

reembolso_path
