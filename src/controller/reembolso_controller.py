# reembolso_controller.py - Versão corrigida (com a limpeza e algumas melhorias menores)

from flask import request, jsonify, Blueprint
from datetime import date, datetime # Importar datetime para parsear a string de data
from src.model.reembolso_model import Reembolso
from src.model.colaborador_model import Colaborador
from src.model import db
from flasgger import swag_from

bp_reembolso = Blueprint('reembolso', __name__, url_prefix='/reembolso')

# ROTA PARA EXCLUIR LINHA DE REEMBOLSO
@bp_reembolso.route('/linha/<int:linha_id>', methods=['DELETE'])
@swag_from("../docs/reebolso/deletar_linha_reembolso.yaml")
def deletar_linha_reembolso(linha_id):
    linha = db.session.get(Reembolso, linha_id)
    if not linha:
        return jsonify({'mensagem': 'Linha de reembolso não encontrada'}), 404

    db.session.delete(linha)
    db.session.commit()
    return jsonify({'mensagem': 'Linha de reembolso excluída com sucesso'}), 200

# NOVA ROTA: SOLICITAR REEMBOLSO
@bp_reembolso.route('/solicitar', methods=['POST'])
@swag_from('../docs/reebolso/solicitação_reebolso.yml') # Verifique se o caminho do arquivo YML está correto
def solicitar_reembolso():
    dados = request.get_json()

    # Verificar se colaborador existe
    colaborador = db.session.get(Colaborador, dados.get('id_colaborador'))
    if not colaborador:
        return jsonify({'mensagem': 'Colaborador não encontrado'}), 404

    try:
        # Tratar a data de string para objeto date
        reembolso_data_str = dados.get('data')
        reembolso_data = date.today() # Valor padrão

        if reembolso_data_str:
            try:
                # Assumindo o formato YYYY-MM-DD. Ajuste se necessário.
                reembolso_data = datetime.strptime(reembolso_data_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'erro': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400

        novo_reembolso = Reembolso(
            # CUIDADO: Você está passando colaborador.nome, mas o modelo tem colaborador_id e um relacionamento.
            # Se o relacionamento ccolaborador_rel deve ser usado para acessar o objeto Colaborador,
            # você não precisa armazenar o nome aqui.
            colaborador=colaborador.nome, # Considere remover ou ajustar isso dependendo do seu modelo
            empresa=dados.get('empresa'),
            num_prestacao=dados.get('num_prestacao'),
            descricao=dados.get('descricao'),
            data=reembolso_data, # Use a data processada
            tipo_reembolso=dados.get('tipo_reembolso'),
            centro_custo=dados.get('centro_custo'),
            ordem_interna=dados.get('ordem_interna'),
            divisao=dados.get('divisao'),
            pep=dados.get('pep'),
            moeda=dados.get('moeda'),
            distancia_km=dados.get('distancia_km'),
            valor_km=dados.get('valor_km'),
            valor_faturado=dados.get('valor_faturado'),
            despesa=dados.get('despesa'),
            id_colaborador=dados.get('id_colaborador') # Isso mapeia para a ForeignKey
        )

        db.session.add(novo_reembolso)
        db.session.commit()
        return jsonify({'mensagem': 'Solicitação de reembolso registrada com sucesso'}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao solicitar reembolso: {e}") # Logar o erro para depuração
        return jsonify({'erro': 'Ocorreu um erro interno ao processar sua solicitação.'}), 500 # Mensagem genérica para o usuário


# NOVA ROTA: CONSULTAR POR NUM PRESTAÇÃO
@bp_reembolso.route('/prestacao/<int:num>', methods=['GET'])
@swag_from("../docs/reebolso/consultar_por_prestacao.yaml")
def consultar_por_prestacao(num):
    reembolso = db.session.execute(
        db.select(Reembolso).where(Reembolso.num_prestacao == num)
    ).scalar()

    if not reembolso:
        return jsonify({'mensagem': 'Reembolso não encontrado'}), 404

    # Considere adicionar um método .to_dict() ao modelo Reembolso para serialização
    return jsonify({
        'id': reembolso.id,
        'colaborador': reembolso.colaborador, # Verifique se isso deve ser o nome ou vir do relacionamento
        'empresa': reembolso.empresa,
        'num_prestacao': reembolso.num_prestacao,
        'descricao': reembolso.descricao,
        'status': reembolso.status
    }), 200

# ROTA PARA ENVIAR SOLICITAÇÃO PARA ANÁLISE
@bp_reembolso.route('/enviar/<int:reembolso_id>', methods=['POST'])
@swag_from("../docs/reebolso/enviar_para_analise.yaml")
def enviar_para_analise(reembolso_id):
    reembolso = db.session.get(Reembolso, reembolso_id)
    if not reembolso:
        return jsonify({'mensagem': 'Solicitação não encontrada'}), 404

    reembolso.status = 'Em Análise'
    db.session.commit()
    return jsonify({'mensagem': 'Solicitação enviada para análise com sucesso'}), 200

# ROTA PARA CANCELAR SOLICITAÇÃO
@bp_reembolso.route('/cancelar/<int:reembolso_id>', methods=['POST'])
@swag_from("../docs/reebolso/cancelar_reembolso.yaml")
def cancelar_reembolso(reembolso_id):
    reembolso = db.session.get(Reembolso, reembolso_id)
    if not reembolso:
        return jsonify({'mensagem': 'Solicitação não encontrada'}), 404

    reembolso.status = 'Cancelada'
    db.session.commit()
    return jsonify({'mensagem': 'Solicitação cancelada com sucesso'}), 200

# ROTA OPCIONAL PARA CRIAR AS TABELAS DO BANCO DE DADOS
# Esta rota é redundante se você já chama db.create_all() em create_app()
# e pode causar problemas de contexto se chamada de forma isolada.
# É recomendado remover esta rota e confiar na inicialização em app.py.
# @bp_reembolso.route('/criar-tabelas', methods=['POST'])
# def criar_tabelas_reembolso():
#     try:
#         # db.create_all() precisa de um contexto de aplicação ativo.
#         # Chamar diretamente aqui pode falhar dependendo de como a rota é acessada.
#         db.create_all()
#         return jsonify({'mensagem': 'Tabelas criadas com sucesso'}), 201
#     except Exception as e:
#         print(f"Erro ao criar tabelas pela rota: {e}")
#         return jsonify({'erro': 'Ocorreu um erro ao criar as tabelas.'}), 500