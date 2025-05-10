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
