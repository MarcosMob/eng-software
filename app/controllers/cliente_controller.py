from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app.dao.cliente_dao import ClienteDAO
from app.models.cliente import Cliente

cliente_bp = Blueprint('cliente', __name__)
cliente_dao = ClienteDAO()

@cliente_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = cliente_dao.get_all()
    return render_template('clientes/listar.html', clientes=clientes)

@cliente_bp.route('/clientes/novo', methods=['GET'])
def novo_cliente():
    return render_template('clientes/novo.html')

@cliente_bp.route('/clientes', methods=['POST'])
def criar_cliente():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    
    cliente = Cliente(None, nome, email, senha)
    cliente_dao.create(cliente)
    
    return redirect(url_for('cliente.listar_clientes'))

@cliente_bp.route('/clientes/<int:id_cliente>/editar', methods=['GET'])
def editar_cliente(id_cliente):
    cliente = cliente_dao.get_by_id(id_cliente)
    return render_template('clientes/editar.html', cliente=cliente)

@cliente_bp.route('/clientes/<int:id_cliente>', methods=['POST'])
def atualizar_cliente(id_cliente):
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    
    cliente = Cliente(id_cliente, nome, email, senha)
    cliente_dao.update(cliente)
    
    return redirect(url_for('cliente.listar_clientes'))

@cliente_bp.route('/clientes/<int:id_cliente>/excluir', methods=['POST'])
def excluir_cliente(id_cliente):
    cliente_dao.delete(id_cliente)
    return redirect(url_for('cliente.listar_clientes'))

