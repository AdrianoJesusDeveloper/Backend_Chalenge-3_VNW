from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reembolso.db'  # Altere conforme seu banco
db = SQLAlchemy(app)

bp_reembolso = Blueprint('reembolso', __name__, url_prefix='/reembolso')

# MODELOS
class Reembolso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120))
    status = db.Column(db.String(50), default="em análise")
    # Outros campos podem ser adicionados

class LinhaReembolso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reembolso_id = db.Column(db.Integer, db.ForeignKey('reembolso.id'), nullable=False)
    descricao = db.Column(db.String(200))
    valor = db.Column(db.Float)
    data = db.Column(db.Date)
    # Outros campos podem ser adicionados

# ROTA PARA EXCLUIR LINHA (LIXEIRA)
@app.route('/api/reembolso/linha/<int:linha_id>', methods=['DELETE'])
def deletar_linha_reembolso(linha_id):
    linha = LinhaReembolso.query.get(linha_id)
    if not linha:
        return jsonify({'mensagem': 'Linha de reembolso não encontrada'}), 404

    db.session.delete(linha)
    db.session.commit()
    return jsonify({'mensagem': 'Linha de reembolso excluída com sucesso'}), 200

# ROTA PARA ENVIAR SOLICITAÇÃO PARA ANÁLISE
@app.route('/api/reembolso/enviar/<int:reembolso_id>', methods=['POST'])
def enviar_para_analise(reembolso_id):
    reembolso = Reembolso.query.get(reembolso_id)
    if not reembolso:
        return jsonify({'mensagem': 'Solicitação não encontrada'}), 404

    reembolso.status = 'Em Análise'
    db.session.commit()
    return jsonify({'mensagem': 'Solicitação enviada para análise com sucesso'}), 200

# ROTA PARA CANCELAR SOLICITAÇÃO
@app.route('/api/reembolso/cancelar/<int:reembolso_id>', methods=['POST'])
def cancelar_reembolso(reembolso_id):
    reembolso = Reembolso.query.get(reembolso_id)
    if not reembolso:
        return jsonify({'mensagem': 'Solicitação não encontrada'}), 404

    reembolso.status = 'Cancelada'
    db.session.commit()
    return jsonify({'mensagem': 'Solicitação cancelada com sucesso'}), 200

# Inicialização opcional do banco de dados
@app.cli.command()
def criar_tabelas():
    db.create_all()

# Rodar a aplicação
if __name__ == '__main__':
    app.run(debug=True)
